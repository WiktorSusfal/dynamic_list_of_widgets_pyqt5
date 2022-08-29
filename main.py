import DLW_GUIList
import DLW_GUIList as dlwgl
from PyQt5 import QtWidgets as qtw


def returnSimpleLayout(i: int = 0) -> qtw.QLayout:
    """
    Test function to return simple layouts for dynamic list of widgets ('dlwgl.DLW_List()' object)
    :param i: Custom number to differentiate the layouts - for presentation purposes.
    :return:
    """
    name_label = qtw.QLabel('Custom Text Label ' + str(i))
    l_fpath_btn = qtw.QPushButton('Button ' + str(i))
    d_btn = qtw.QPushButton('Del Button')

    main_layout = qtw.QHBoxLayout()
    main_layout.addWidget(name_label)
    main_layout.addWidget(l_fpath_btn)
    main_layout.addWidget(d_btn)

    return main_layout


class MainWindow(qtw.QMainWindow):
    """
    Class representing main app window - for presentation and testing purposes
    """
    def __init__(self):
        super().__init__()
        # Declare 'dlwgl.DLW_List()' object - dynamic list of custom widgets defined by user
        self.list_of_elements = dlwgl.DLW_List()
        # Subscribe to event handler to receive notifications about selected element's changes.
        # Pass custom function - in this example to print selected element's id in the screen
        self.list_of_elements.selected_element_changed_handler += self.printCurrentSelectedElementID

        # prepare main window to display the list of widgets
        self.setWindowTitle('Dynamic GUI List Tests')
        self.setCentralWidget(self.list_of_elements)
        self.setFixedSize(600, 480)

        # fill the 'dlwgl.DLW_List()' object with some layouts
        for i in range(5):
            self.list_of_elements += returnSimpleLayout(i)

        self.show()

    @staticmethod
    def printCurrentSelectedElementID(element: dlwgl.DLW_ListElement):
        """
        Test function called every time there is a notification from DLW_List's event handler - every time the current
        selected element changes.
        :param element: Reference to current selected element (DLW_ListElement object)
        :return:
        """
        if element is not None:
            print("Current element's id: " + str(element.id))
        else:
            print("Current element's id: None")


if __name__ == '__main__':
    # invoke the application
    app = qtw.QApplication([])
    app_main_gui = MainWindow()
    app.exec_()





