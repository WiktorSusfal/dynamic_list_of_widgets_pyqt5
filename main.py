import DLW_GUIList
import DLW_GUIList as dlwgl
from PyQt5 import QtWidgets as qtw


# test function to return simple layouts for dynamic list of widgets ('dlwgl.DLW_List()' object)
def returnSimpleLayout(i: int = 0) -> qtw.QLayout:
    name_label = qtw.QLabel('Custom Text Label ' + str(i))
    l_fpath_btn = qtw.QPushButton('Button ' + str(i))
    d_btn = qtw.QPushButton('Del Button')

    main_layout = qtw.QHBoxLayout()
    main_layout.addWidget(name_label)
    main_layout.addWidget(l_fpath_btn)
    main_layout.addWidget(d_btn)

    return main_layout


# class representing main app window - for presentation and testing purposes
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        # declare 'dlwgl.DLW_List()' object - dynamic list of custom widgets defined by user
        self.list_of_elements = dlwgl.DLW_List()
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
        if element is not None:
            print("Current element's id: " + str(element.id))
        else:
            print("Current element's id: None")


if __name__ == '__main__':
    # invoke the application
    app = qtw.QApplication([])
    app_main_gui = MainWindow()
    app.exec_()





