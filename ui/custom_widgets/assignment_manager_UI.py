from PySide2 import QtWidgets, QtCore, QtGui


class AssignmentManagerBuild(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(AssignmentManagerBuild, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setHeaderHidden(True)

        self.expandAll()
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)


class AssignmentManagerUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AssignmentManagerUI, self).__init__(parent)
        self.setMinimumWidth(150)
        self.setMaximumWidth(160)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.assignemnt_manager_lb = QtWidgets.QLabel("Assignment Manager")
        my_font = QtGui.QFont()
        my_font.setBold(True)
        self.assignemnt_manager_lb.setFont(my_font)
        self.assignemnt_manager_lb.setStyleSheet("color: red")

        self.project_tree_viewer_wdg = AssignmentManagerBuild()
        self.save_btn = QtWidgets.QPushButton("Commit")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.assignemnt_manager_lb)
        main_layout.addWidget(self.project_tree_viewer_wdg)
        main_layout.addWidget(self.save_btn)
        main_layout.addWidget(self.refresh_btn)


if __name__ == '__main__':
    import sys
    import pprint

    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())
    test_dialog = AssignmentManagerUI()
    test_dialog.show()
    sys.exit(app.exec_())