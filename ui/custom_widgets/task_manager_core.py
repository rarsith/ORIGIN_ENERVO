import sys
from PySide2 import QtWidgets
from envars.envars import Envars

from ui.custom_widgets.task_imports_from_core import TasksImportFromCore
from ui.custom_widgets.task_publishing_slots_core import PublishSlotsWidgetCore
from ui.custom_widgets.task_viewer_core import TaskViewerCore


class OriginControlCenterUI(QtWidgets.QWidget):
    def __init__(self):
        super(OriginControlCenterUI, self).__init__()
        self.setMinimumHeight(800)
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.get_tasks()

    def create_widgets(self):
        self.tasks_view_lwd = TaskViewerCore()
        self.tasks_imports_from_properties_wdg = TasksImportFromCore()
        self.tasks_pub_slots_properties_wdg = PublishSlotsWidgetCore()
        self.refresh_btn = QtWidgets.QPushButton("Refresh")
        self.to_category_btn = QtWidgets.QPushButton("...Propagate To Category")
        self.propagate_to_all_in_category_btn = QtWidgets.QPushButton("...Propagate To All Category Entries ")
        self.to_templates_btn = QtWidgets.QPushButton("...Propagate Templates ")
        self.import_tasks_scehma_btn = QtWidgets.QPushButton("Import Tasks Schema ")

    def create_layout(self):

        views_layout = QtWidgets.QHBoxLayout()
        views_layout.setContentsMargins(1, 1, 1, 1)
        views_layout.addWidget(self.tasks_view_lwd)
        views_layout.addWidget(self.tasks_imports_from_properties_wdg)
        views_layout.addWidget(self.tasks_pub_slots_properties_wdg)

        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.to_category_btn)
        button_layout.addWidget(self.propagate_to_all_in_category_btn)
        button_layout.addWidget(self.to_templates_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.import_tasks_scehma_btn)
        main_layout.addLayout(views_layout)
        main_layout.setContentsMargins(1, 1, 1, 1)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.tasks_pub_slots_properties_wdg.clear_selection)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.populate_task_import_schema)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.populate_pub_slots)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.get_selected_type)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.tasks_pub_slots_properties_wdg.change_label_pub_slots)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect( self.tasks_imports_from_properties_wdg.change_label_existing_tasks)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect( self.tasks_imports_from_properties_wdg.change_label_imports_from)

    def get_task_type(self):
        task_name = self.tasks_view_lwd.get_selected_task()
        if task_name:
            task_type = "task"
            return task_type

    def populate_task_import_schema(self):
        self.tasks_imports_from_properties_wdg.populate_main_widget()

    def get_tasks(self):
        self.tasks_view_lwd.populate_tasks()

    def get_selected_type(self):
        task_selected = self.tasks_view_lwd.task_viewer_wdg.hasFocus()

        if task_selected:
            task_type = self.get_task_type()
            return task_type

    def populate_pub_slots(self):
        self.tasks_pub_slots_properties_wdg.populate_main_widget()


class MainUI(QtWidgets.QMainWindow):
    WINDOW_TITLE = "Origin Task Manager"

    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.setWindowTitle(self.window_context_details())
        central_widget = OriginControlCenterUI()
        self.setCentralWidget(central_widget)

    def window_context_details(self):
        show_name = Envars().show_name
        branch_name = Envars().branch_name
        category = Envars().category
        entity_name = Envars().entry_name

        window_name = "-> ".join([self.WINDOW_TITLE, show_name, branch_name, category, entity_name])
        return window_name




if __name__ == "__main__":
    Envars.show_name = "Green"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "frog"

    app = QtWidgets.QApplication(sys.argv)

    test_dialog = MainUI()
    test_dialog.show()
    sys.exit(app.exec_())
