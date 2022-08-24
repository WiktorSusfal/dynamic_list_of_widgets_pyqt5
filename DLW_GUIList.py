from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets as qtw
import uuid
import DLW_EventHandler as eh
from enum import *

# default opacities for list elements when selected and unselected
LIST_ITEM_NOT_SELECTED_OPACITY = 0.7
LIST_ITEM_SELECTED_OPACITY = 1.0


# enum for storing different request types that list items ('DLW_ListElement' objects)
# can send to list object ('DLW_List') via event handler ('DLW_EventHandler.DLW_EventHandler')
class DLW_Requests(Enum):
    SELECTION = 0
    DELETION = 1


# enum for storing different key values for dictionary which is sent as event argument during list usage
class DLW_Event_Attributes(Enum):
    EVENT_ACTOR = 0
    REQUEST_TYPE = 1


# function to build event arguments based on predefined keys and values;
# list of values provided must conform the order of keys stored in enum 'DLW_Event_Attributes'
def buildEventArgs(values: list) -> dict:
    args, i = {}, 0
    for attribute in DLW_Event_Attributes:
        args[attribute.value] = values[i]
        i += 1

    return args


# class for common representation of list element
class DLW_ListElement(qtw.QWidget):

    def __init__(self, element_layout: qtw.QLayout, uid: str, s_handler: eh.DLW_EventHandler):
        super().__init__()

        # unique id of element - in the scope of current list
        self.id = uid
        # flag indicating if particular list element is already selected
        self.selected = False
        # object and method used to adjust the opacity of list element - based on its 'selected' state
        self.opacity_effect = qtw.QGraphicsOpacityEffect()
        self.setListItemOpacity()

        # add context menu to list item to allow for object deletion
        self.c_menu = qtw.QMenu(self)
        delete_action = qtw.QAction('Delete Item', self)
        delete_action.triggered.connect(self.deleteObjectFromList)
        self.c_menu.addAction(delete_action)

        # event handler object for real-time management of list elements
        self.selection_handler = s_handler
        self.selection_handler += self.itemRequestHandler

        # setting main layout of the list element based on constructor argument
        self.main_layout = element_layout
        self.setLayout(self.main_layout)

    # function is automatically called when mouse-release event is captured on the list item
    def mouseReleaseEvent(self, event):
        # relevant event is triggered only by mouse left-button
        if event.button() == qtc.Qt.LeftButton:
            # trigger the event handler object and pass created argument's dictionary
            event_arguments = buildEventArgs([self, DLW_Requests.SELECTION.value])
            self.selection_handler(event_arguments)

    # function is automatically called when mouse-right-click event is captured on the list item
    def contextMenuEvent(self, event):
        self.c_menu.popup(qtg.QCursor.pos())

    # function is bind to every item's contex menu option - for object deleting;
    # it triggers the event handler with proper request type (DELETION)
    def deleteObjectFromList(self):
        event_arguments = buildEventArgs([self, DLW_Requests.DELETION.value])
        # important to unsubscribe from event handler before deleting object
        self.selection_handler -= self.itemRequestHandler
        self.selection_handler(event_arguments)

    # function is called when event handler object is triggered by some list item;
    def itemRequestHandler(self, event_arguments):
        # parse event arguments
        event_actor = event_arguments[DLW_Event_Attributes.EVENT_ACTOR.value]
        request_type = event_arguments[DLW_Event_Attributes.REQUEST_TYPE.value]
        # if the request type was 'SELECTION', do the following:
        if request_type == DLW_Requests.SELECTION.value:
            # if the event handler is triggered by this list item - change the state of 'selected' flag;
            # if event handler is triggered by other list item - set 'selected' as false
            self.selected = not self.selected if event_actor.id == self.id else False
            # adjust list item opacity based on the 'selected' flag
            self.setListItemOpacity()

    # function to adjust list item opacity based on the 'selected' flag
    def setListItemOpacity(self):
        if self.selected:
            self.opacity_effect.setOpacity(LIST_ITEM_SELECTED_OPACITY)
        else:
            self.opacity_effect.setOpacity(LIST_ITEM_NOT_SELECTED_OPACITY)

        self.setGraphicsEffect(self.opacity_effect)


# delete all widgets from given layout - used to empty the list of widgets
def clearLayout(layout):
    while layout.count() > 0:
        item = layout.itemAt(0)
        widget = item.widget()
        layout.removeWidget(widget)


# class for representation of dynamic list
class DLW_List(qtw.QWidget):

    def __init__(self):
        super().__init__()

        # array of all elements stored in the list ('DLW_ListElement' objects)
        self.elements = []
        # current selected element - by the mouse-release event
        self.selected_element = None
        # event handler object for real-time management of list elements
        self.selection_handler = eh.DLW_EventHandler()
        self.selection_handler += self.requestHandler

        # setting main layout of the list
        self.main_layout = qtw.QVBoxLayout()
        self.setLayout(self.main_layout)

    # overload of '+=' operator to add elements to list
    # operator accepts 'QLayout' object types and creates 'DLW_ListElement' objects based on them internally.
    # this way it is easier to assign proper event handler for every list item (in the constructor of list item)
    def __iadd__(self, element: qtw.QLayout):
        element_id = str(uuid.uuid4())
        self.elements.append(DLW_ListElement(element, element_id, self.selection_handler))
        # update the gui of the list - clear all the widgets and add them once again
        self.updateListGUI()

        return self

    # overload of '-=' operator to remove elements from list
    # support for removing items by item object reference or item string uuid
    def __isub__(self, element):
        if isinstance(element, str):
            element_to_remove = None
            for list_element in self.elements:
                if list_element.id == element:
                    element_to_remove = list_element
                    break
            # if object that is being deleted is currently selected, reset the class attribute
            self.selected_element = None if element_to_remove == self.selected_element else self.selected_element
            self.elements.remove(element_to_remove)

        elif isinstance(element, DLW_ListElement):
            self.selected_element = None if element == self.selected_element else self.selected_element
            self.elements.remove(element)

        # update the gui of the list - clear all the widgets and add them once again
        self.updateListGUI()

        return self

    # function to clear and draw all list items once again
    def updateListGUI(self):
        clearLayout(self.main_layout)
        for element in self.elements:
            self.main_layout.addWidget(element)

        self.main_layout.addStretch()

    # this function is called when event handler object is triggered by some list item;
    # event handler stores callback functions in a python list, so they are called always in the adding order.
    # this function is called always before callbacks from list items.
    # perform relevant action based on the value of request type sent from list item
    def requestHandler(self, event_arguments: dict):
        # parse event arguments
        event_actor = event_arguments[DLW_Event_Attributes.EVENT_ACTOR.value]
        request_type = event_arguments[DLW_Event_Attributes.REQUEST_TYPE.value]

        if request_type == DLW_Requests.SELECTION.value:
            # update the reference to the current selected item
            self.updateSelectedItem(event_actor)
        elif request_type == DLW_Requests.DELETION.value:
            # delete element from list
            self -= event_actor

    # method to update the reference to the current selected item
    def updateSelectedItem(self, event_actor):
        # if the list item, which the mouse event was captured on, wasn't selected before, it is the selected item now
        # if the list item was selected before, it is unchecked now and there is no selected item
        if not event_actor.selected:
            self.selected_element = event_actor
        else:
            self.selected_element = None
