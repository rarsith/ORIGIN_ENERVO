import sys
from PySide2 import QtWidgets, QtCore

from database.entities.db_entities import DbTasks, DbAsset
from database.db_statuses import DbStatuses
from ui.custom_widgets.task_imports_from_core import TasksImportFromCore
from ui.custom_widgets.task_publishing_slots_core import PublishSlotsWidgetCore
from ui.custom_widgets.main_publishes_view_core import MainPublishesViewCore
from ui.custom_widgets.slots_publishes_view_core import SlotPublishesViewCore
from ui.custom_widgets.slot_component_viewer_core import SlotComponentsViewerCore
from ui.custom_widgets.project_tree_viewer_core import ProjectTreeViewerCore
from ui.custom_widgets.task_viewer_core import TaskViewerCore
from ui.custom_widgets.entry_properties_editor_UI import EntryPropertiesEditorUI
from ui.custom_widgets.assignment_manager_core import AssignmentManagerMainUI


class BundleViewListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super(BundleViewListWidget, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.sortItems(QtCore.Qt.AscendingOrder)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)


class BundleViewWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(BundleViewWidget, self).__init__(parent)

        self.widget_build()

    def widget_build(self):

        self.setColumnCount(9)
        self.setRowCount(50)
        self.setColumnWidth(0, 30)
        self.setColumnWidth(1, 60)
        for row in range(self.rowCount()):
            self.setRowHeight(row, 20)
        self.setAlternatingRowColors(True)
        self.setMinimumWidth(850)
        self.setHorizontalHeaderLabels(['', '',
                                        'task01',
                                        'task02',
                                        'task03',
                                        'task04',
                                        'task05',
                                        'task06',
                                        'task07'])


class ContentViewWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(ContentViewWidget, self).__init__(parent)

        self.widget_build()

    def widget_build(self):
        self.setMaximumWidth(437)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Asset Name", "Category", "status", "health"])
        self.setShowGrid(True)
        self.setRowCount(20)
        self.setAlternatingRowColors(True)
        # header = self.shot_content_twd.verticalHeader()
        # header.hide()
        self.setColumnWidth(0, 135)
        self.setColumnWidth(1, 135)
        self.setColumnWidth(2, 80)
        self.setColumnWidth(3, 67)
        for row in range(self.rowCount()):
            self.setRowHeight(row, 5)


class ButtonsWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ButtonsWidget, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QPushButton("Button 01"))
        layout.addWidget(QtWidgets.QPushButton("Button 02"))
        layout.addWidget(QtWidgets.QPushButton("Button 03"))
        layout.addWidget(QtWidgets.QPushButton("Button 04"))


class NotesWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(NotesWidget, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel("Label"))
        layout.addWidget(QtWidgets.QPushButton("Button"))
        layout.addWidget(QtWidgets.QCheckBox("Check Box"))
        layout.addWidget(QtWidgets.QLineEdit())


class OriginControlCenterUI(QtWidgets.QWidget):
    WINDOW_TITLE = "Origin Control Center"

    def __init__(self):
        super(OriginControlCenterUI, self).__init__()

        self.setWindowTitle(self.WINDOW_TITLE)

        self.setMinimumHeight(1000)
        self.setMinimumWidth(2200)

        self.create_widgets()

        self.create_layout()
        self.create_connections()
        self.task_properties_UI()
        self.publishes_properties_UI()
        self.shot_definition_UI()
        self.populate_main_publishes()

    def create_widgets(self):
        self.menu_bar = QtWidgets.QMenuBar()
        self.show_view_twd = ProjectTreeViewerCore()
        self.tasks_view_lwd = TaskViewerCore()

        self.empty_stack = QtWidgets.QWidget()
        self.entry_task_properties_stack = QtWidgets.QWidget()
        self.publishes_viewer_wdg = QtWidgets.QWidget()
        self.shots_definition_properties_stack = QtWidgets.QWidget()
        self.assets_definition_properties_stack = QtWidgets.QWidget()

        self.shot_bundle_view_lwd = BundleViewListWidget()
        self.shot_bundle_edit_btn = QtWidgets.QPushButton('Edit Bundle')
        self.asset_bundle_view_lwd = BundleViewListWidget()
        self.asset_bundle_edit_btn = QtWidgets.QPushButton('Edit Bundle')

        self.shot_bundle_view_lwd = BundleViewListWidget()

        # ----------------------------------------------
        self.versions_view_tvw = MainPublishesViewCore()
        self.slots_publishes_tvw = SlotPublishesViewCore()
        self.bundle_view_tvw = BundleViewWidget()
        self.graph_view_lw = QtWidgets.QListWidget()

        self.stacked_properties_wdg = QtWidgets.QStackedWidget()
        self.stacked_properties_wdg.addWidget(self.empty_stack)
        self.stacked_properties_wdg.addWidget(self.shots_definition_properties_stack)
        self.stacked_properties_wdg.addWidget(self.entry_task_properties_stack)

        self.middle_tabmenu_tab = QtWidgets.QTabWidget()
        self.middle_tabmenu_tab.addTab(self.publishes_viewer_wdg, "Publishes")
        self.middle_tabmenu_tab.addTab(self.stacked_properties_wdg, "Properties")
        self.middle_tabmenu_tab.addTab(self.bundle_view_tvw, "Bundle View")
        self.middle_tabmenu_tab.addTab(self.graph_view_lw, "Graph View")

        self.properties_wdg = EntryPropertiesEditorUI()

        # StackWidget for Entry Tasks Properties
        self.task_is_active_properties_ckb = QtWidgets.QCheckBox()
        self.task_status_properties_cb = QtWidgets.QComboBox()
        self.task_status_properties_cb.addItems(DbStatuses().list_all())

        self.task_edit_user_properties_btn = QtWidgets.QPushButton("Edit")
        self.tasks_pub_slots_edit_properties_btn = QtWidgets.QPushButton("Edit")
        self.task_user_properties_wdg = QtWidgets.QLineEdit()

        # Create the individual Widgets that will be part of the Layout
        self.tasks_imports_from_properties_wdg = TasksImportFromCore()
        self.tasks_imports_from_edit_properties_btn = QtWidgets.QPushButton("Edit")
        self.tasks_imports_from_commit_btn = QtWidgets.QPushButton('Commit')

        self.tasks_pub_slots_properties_wdg = PublishSlotsWidgetCore()

        # StackWidget for Asset definition
        # Create the individual Widgets that will be part of the Layout
        self.asset_lod_le = QtWidgets.QLabel()
        self.asset_assembly_chk = QtWidgets.QCheckBox()
        self.asset_assembly_chk.setDisabled(True)
        self.asset_edit_definition_btn = QtWidgets.QPushButton("Edit")

        # StackWidget for Shot definition
        # Create the individual Widgets that will be part of the Layout
        self.shot_edit_definitions_btn = QtWidgets.QPushButton("Edit")

        # widgets for Shot Content----START
        self.shot_content_lb = QtWidgets.QLabel("Content")
        self.shot_content_twd = ContentViewWidget()
        # widgets for Shot Content----END

        # Construct the Links Tab
        self.links_wdg = ButtonsWidget()
        self.components_wdg = SlotComponentsViewerCore()

        # Construct the Notes Tab
        self.notes_wdg = NotesWidget()

        # Assembling the Right Side Tab Menu
        self.details_tabmenu_tab = QtWidgets.QTabWidget()
        self.details_tabmenu_tab.setTabPosition(QtWidgets.QTabWidget.North)
        # self.details_tabmenu_tab.addTab(self.components_wdg, "Components")
        self.details_tabmenu_tab.addTab(self.links_wdg, "Links")
        self.details_tabmenu_tab.addTab(self.notes_wdg, "Notes")

        self.all_tab = QtWidgets.QTabWidget()
        self.all_tab.setTabPosition(QtWidgets.QTabWidget.West)

        self.refresh_btn = QtWidgets.QPushButton("Refresh")

    def create_layout(self):
        views_layout = QtWidgets.QHBoxLayout()
        views_layout.setContentsMargins(2, 2, 2, 2)
        views_layout.setSpacing(2)
        views_layout.addWidget(self.show_view_twd)
        views_layout.addWidget(self.tasks_view_lwd)
        views_layout.addWidget(self.middle_tabmenu_tab)
        views_layout.addWidget(self.details_tabmenu_tab)

        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(self.refresh_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(views_layout)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.show_view_twd.show_select_cb.currentIndexChanged.connect(self.populate_main_publishes)
        self.show_view_twd.show_select_cb.currentIndexChanged.connect(self.get_tasks)
        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.populate_slot_publishes)
        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.populate_slot_components)
        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.populate_main_publishes)

        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.populate_main_publishes)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.populate_slot_publishes)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.tasks_pub_slots_properties_wdg.clear_selection)

        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.tasks_pub_slots_properties_wdg.change_label_pub_slots)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.tasks_imports_from_properties_wdg.change_label_existing_tasks)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.tasks_imports_from_properties_wdg.change_label_imports_from)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.tasks_imports_from_properties_wdg.change_label_imports_from_assignments)

        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.get_tasks)
        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.update_entry_properties_list)
        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.get_selected_type)
        self.show_view_twd.project_tree_viewer_wdg.itemClicked.connect(self.switch_stack)

        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.populate_task_import_schema)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.populate_task_details)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.populate_pub_slots)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.get_selected_type)
        self.tasks_view_lwd.task_viewer_wdg.itemSelectionChanged.connect(self.switch_stack)

        self.versions_view_tvw.connect_to_slot(self.populate_slot_publishes)
        self.versions_view_tvw.connect_to_slot(self.populate_slot_components)
        self.slots_publishes_tvw.connect_to_slot(self.populate_slot_components)

        self.task_is_active_properties_ckb.clicked.connect(self.set_task_is_active)
        self.task_is_active_properties_ckb.clicked.connect(self.populate_task_details)

        self.refresh_btn.clicked.connect(self.show_view_twd.refresh_shows)
        self.refresh_btn.clicked.connect(self.show_view_twd.refresh_tree_widget)

    def get_task_type(self):
        task_name = self.tasks_view_lwd.get_selected_task()
        if task_name:
            task_type = "task"
            return task_type

    def set_task_status(self):
        read_selected_status = self.task_status_properties_cb.currentText()
        try:
            DbTasks().status = read_selected_status
        except:
            pass
        print('{} status changed to {}'.format(self.get_selected_task(), read_selected_status))

    def set_task_is_active(self):
        is_active = self.task_is_active_properties_ckb.isChecked()
        try:
            DbTasks().current_is_active = is_active
            self.populate_task_details()
        except:
            pass
        print('{} status changed to {}'.format(self.tasks_view_lwd.get_selected_task(), is_active))

    def get_task_status(self):
        try:
            task_status = DbTasks().status
            return task_status
        except:
            pass

    def get_task_is_active(self):
        try:
            task_is_active = DbTasks().current_is_active
            return task_is_active
        except:
            pass

    def populate_task_import_schema(self):
        self.tasks_imports_from_properties_wdg.populate_main_widget()

    def populate_main_publishes(self):
        main_pub_show_name = self.show_view_twd.show_select_cb.currentText()

        main_pub_branch_name = ''
        main_pub_category_name = ''
        main_pub_entry_name = ''
        main_pub_task_name = ''

        try:
            main_pub_branch_name = self.show_view_twd.get_sel_data()[1]
            main_pub_category_name = self.show_view_twd.get_sel_data()[2]
            main_pub_entry_name = self.show_view_twd.get_sel_data()[3]
            main_pub_task_name = self.tasks_view_lwd.get_selected_task()
        except:
            pass

        self.versions_view_tvw.show_name = main_pub_show_name
        self.versions_view_tvw.branch_name = main_pub_branch_name
        self.versions_view_tvw.category_name = main_pub_category_name
        self.versions_view_tvw.entry_name = main_pub_entry_name
        self.versions_view_tvw.task_name = main_pub_task_name
        self.versions_view_tvw.populate_main_widget()
        self.versions_view_tvw.publish_view_tw.clearSelection()

    def populate_slot_publishes(self):
        pub_id = self.versions_view_tvw.get_selection_id()
        self.slots_publishes_tvw.main_pub_id = pub_id
        self.slots_publishes_tvw.populate_main_widget()
        self.slots_publishes_tvw.slot_publish_view_tw.clearSelection()

    def populate_slot_components(self):
        slot_id = self.slots_publishes_tvw.get_selection_id()
        slot_collection = self.slots_publishes_tvw.get_selection_collection()
        self.components_wdg.slot_pub_id = slot_id
        self.components_wdg.slot_collection = slot_collection
        self.components_wdg.populate_main_widget()
        self.components_wdg.slot_component_viewer_tw.clearSelection()

    def get_tasks(self):
        self.tasks_view_lwd.populate_tasks()

    def get_selected_type(self):
        entry_selected = self.show_view_twd.project_tree_viewer_wdg.hasFocus()
        task_selected = self.tasks_view_lwd.task_viewer_wdg.hasFocus()

        if entry_selected:
            get_selected_objects_type = DbAsset().get_entry_type()
            return get_selected_objects_type

        elif task_selected:
            task_type = self.get_task_type()
            return task_type

    def update_entry_properties_list(self):
        properties = self.get_entry_properties()
        self.properties_wdg.create_properties(properties)

    def get_entry_properties(self):
        spare_it = []
        definitions_list = DbAsset().get_definition()

        if definitions_list is None:
            return spare_it
        else:
            try:
                if len(definitions_list) == 0:
                    return spare_it
                elif len(definitions_list) >= 1:
                    return definitions_list
            except:
                pass

    def populate_task_details(self):
        task_status = self.get_task_status()
        task_is_active = self.get_task_is_active()
        if task_status or task_is_active is not None:
            self.task_status_properties_cb.setCurrentText(task_status)
            self.task_is_active_properties_ckb.setChecked(task_is_active)

    def populate_pub_slots(self):
        self.tasks_pub_slots_properties_wdg.populate_main_widget()

    def publishes_properties_UI(self):
        main_pub_layout = QtWidgets.QHBoxLayout()
        main_pub_layout.addWidget(self.versions_view_tvw)

        slots_and_components_layout = QtWidgets.QVBoxLayout()
        slots_and_components_layout.addWidget(self.slots_publishes_tvw)
        slots_and_components_layout.addWidget(self.components_wdg)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(main_pub_layout)
        main_layout.addLayout(slots_and_components_layout)

        self.publishes_viewer_wdg.setLayout(main_layout)

    def task_properties_UI(self):
        task_user_btn_layout = QtWidgets.QHBoxLayout()
        task_user_btn_layout.addWidget(self.task_user_properties_wdg)
        task_user_btn_layout.addWidget(self.task_edit_user_properties_btn)

        top_data_form = QtWidgets.QFormLayout()
        top_data_form.addRow("Active", self.task_is_active_properties_ckb)
        top_data_form.addRow("Status", self.task_status_properties_cb)
        top_data_form.addRow("User", task_user_btn_layout)
        top_data_form.setFormAlignment(QtCore.Qt.AlignLeft)
        top_data_form.setLabelAlignment(QtCore.Qt.AlignLeft)
        top_data_form.setSpacing(5)

        top_data_layout = QtWidgets.QVBoxLayout()
        top_data_layout.addLayout(top_data_form)

        imports_from_layout = QtWidgets.QVBoxLayout()
        imports_from_layout.addWidget(self.tasks_imports_from_properties_wdg)

        imports_from_layout.setSpacing(5)

        publishing_slots_layout = QtWidgets.QVBoxLayout()
        publishing_slots_layout.addWidget(self.tasks_pub_slots_properties_wdg)
        publishing_slots_layout.setSpacing(5)

        lists_layout = QtWidgets.QHBoxLayout()
        lists_layout.addLayout(imports_from_layout)
        lists_layout.addLayout(publishing_slots_layout)
        lists_layout.setAlignment(QtCore.Qt.AlignLeft)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(top_data_layout)
        main_layout.addLayout(lists_layout)

        self.entry_task_properties_stack.setLayout(main_layout)

    def shot_definition_UI(self):

        bundle_layout = QtWidgets.QVBoxLayout()
        bundle_layout.addWidget(self.shot_bundle_view_lwd)
        bundle_layout.addWidget(self.shot_bundle_edit_btn)

        shot_def_new = QtWidgets.QVBoxLayout()
        shot_def_new.addWidget(self.properties_wdg)
        shot_def_new.addWidget(self.shot_edit_definitions_btn)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(shot_def_new)
        # main_layout.addLayout(bundle_layout)

        self.shots_definition_properties_stack.setLayout(main_layout)

    def switch_stack(self):
        switch_index = self.properties_UI_switcher()
        if switch_index:
            self.stacked_properties_wdg.setCurrentIndex(switch_index)
        else:
            self.stacked_properties_wdg.setCurrentIndex(0)

    def properties_UI_switcher(self):
        current_selection_type = self.get_selected_type()

        if current_selection_type is None:
            assets_index = self.stacked_properties_wdg.indexOf(self.shots_definition_properties_stack)
            return assets_index

        if current_selection_type == "build" or current_selection_type == "shots":
            assets_index = self.stacked_properties_wdg.indexOf(self.shots_definition_properties_stack)
            return assets_index

        elif current_selection_type == "task":
            task_index = self.stacked_properties_wdg.indexOf(self.entry_task_properties_stack)
            return task_index


class MainUI(QtWidgets.QMainWindow):
    WINDOW_TITLE = "ORIGIN"

    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent)
        self.setWindowTitle(self.WINDOW_TITLE)

        central_widget = OriginControlCenterUI()
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    test_dialog = MainUI()
    test_dialog.show()
    sys.exit(app.exec_())