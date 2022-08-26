# dynamic_list_of_widgets_pyqt5
PyQt5 custom widget to store custom given elements in the form of list. Presentation video (of version 1.0): https://www.youtube.com/watch?v=OIqxCw0OQ4k

# Modules:
- DLW_GUIList.py - contains classes related to dynamic list and items for the list
- DLW_EventHandler.py - contains event handler class to allow communication between items present on the list and list object itself
- main.py - example of use

# Features of list
List class ("DLW_List") supports following:
- adding elements programmatically (using '+=' operator on the list object)
- deleting elements programmatically (using '-=') 
- deleting elements using GUI - every list item has context menu (under mouse right-clik) with "Delete" option
- selecting elements by mouse left-click; state of the element is remembered untill another selection
- only single-selection supported so far.

# Interface
Basically there is a need only to interact with "DLW_List" class. "DLW_ListElement" class is created for internal use of "DLW_List".

"DLW_List" useful attributes:
- elements - python list of "DLW_ListElement" objects currently added to list
- selected_element - reference to currently selected "DLW_ListElement" object.
- selected_element_changed_handler - 'DLW_EventHandler' class instance to provide automatic notifications on changes of currently selected list item. Just subscribe to it by adding relevant function using "+=" operator. This function(s) will be invoked always when selected element changes, and the reference to this element will be passed as an argument. Check the main.py - example of use.

"DLW_List" useful operators:
- += - accepts "QLayout" object type and creates "DLW_ListElement" object based on it internally (automatically). When building custom objects to be stored in a list it is recommended to use classes that inherit from "QLayout" directly.
- -= - accepts "DLW_ListElement" object or string uuid of it. Deletes object from list immediately.

"DLW_ListElement" useful attributes:
- id - string uuid of the object, unique in the scope of current "DLW_List" object
- main_layout - layout attribute which the source layout passed to the "+=" "DLW_List" operator is assigned to



