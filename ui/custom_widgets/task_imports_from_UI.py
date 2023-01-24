from PySide2 import QtWidgets, QtGui


class ImportsFromWidgetBuild(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(ImportsFromWidgetBuild, self).__init__(parent)
        self.widget_build()

    def widget_build(self):
        self.setAlternatingRowColors(True)
        self.setHeaderLabels(['task'])
        self.setMinimumWidth(200)
        # self.setMaximumWidth(150)
        # self.setMinimumHeight(300)
        self.setColumnWidth(0, 130)


class ImportsFromAssignmentsWidgetBuild(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super(ImportsFromAssignmentsWidgetBuild, self).__init__(parent)
        self.widget_build()

    def widget_build(self):
        self.setAlternatingRowColors(True)
        self.setHeaderLabels(['assigned asset'])
        self.setMinimumWidth(200)
        # self.setMaximumWidth(150)
        # self.setMinimumHeight(300)
        self.setColumnWidth(0, 130)


class ListEntryTasksBuild(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(ListEntryTasksBuild, self).__init__(parent)
        self.widget_build()

    def widget_build(self):
        self.setMinimumWidth(160)
        # self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)


class TasksImportFromUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TasksImportFromUI, self).__init__(parent)
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.imports_from_wdg = ImportsFromWidgetBuild()
        self.imports_from_assignments = ImportsFromAssignmentsWidgetBuild()
        self.existing_tasks_lwd = ListEntryTasksBuild()


        self.tasks_existing_lb = QtWidgets.QLabel("--select task--")
        my_font = QtGui.QFont()
        my_font.setBold(True)
        self.tasks_existing_lb.setFont(my_font)
        self.tasks_existing_lb.setStyleSheet("color: red")


        self.tasks_imports_from_properties_lb = QtWidgets.QLabel("--select task--")
        my_font = QtGui.QFont()
        my_font.setBold(True)
        self.tasks_imports_from_properties_lb.setFont(my_font)
        self.tasks_imports_from_properties_lb.setStyleSheet("color: red")


        self.move_to_right_btn = QtWidgets.QPushButton(">")
        self.move_to_right_btn.setMinimumHeight(150)
        self.move_to_right_btn.setMinimumWidth(20)
        self.move_to_right_btn.setMaximumWidth(20)
        self.rem_sel_item_btn = QtWidgets.QPushButton("Remove Selected")
        self.save_btn = QtWidgets.QPushButton("Commit")
        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def create_layout(self):
        import_from_layout = QtWidgets.QVBoxLayout()
        import_from_layout.addWidget(self.tasks_imports_from_properties_lb)
        import_from_layout.addWidget(self.imports_from_wdg)
        import_from_layout.addWidget(self.imports_from_assignments)

        move_button_layout = QtWidgets.QHBoxLayout()
        move_button_layout.addWidget(self.move_to_right_btn)

        existing_tasks_layout = QtWidgets.QVBoxLayout()
        existing_tasks_layout.addWidget(self.tasks_existing_lb)
        existing_tasks_layout.addWidget(self.existing_tasks_lwd)

        widget_buttons_layout = QtWidgets.QVBoxLayout()
        widget_buttons_layout.addWidget(self.rem_sel_item_btn)
        widget_buttons_layout.addWidget(self.save_btn)
        widget_buttons_layout.addWidget(self.refresh_btn)

        windows_layout = QtWidgets.QHBoxLayout()
        windows_layout.addLayout(existing_tasks_layout)
        windows_layout.addLayout(move_button_layout)
        windows_layout.addLayout(import_from_layout)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(windows_layout)
        main_layout.addLayout(widget_buttons_layout)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    test_dialog = TasksImportFromUI()
    test_dialog.show()
    sys.exit(app.exec_())