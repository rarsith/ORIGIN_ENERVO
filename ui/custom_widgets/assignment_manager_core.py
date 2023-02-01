from PySide2 import QtWidgets, QtGui, QtCore
from envars.envars import Envars
from ui.custom_widgets.assignment_manager_UI import AssignmentManagerUI
from database.entities.db_entities import DbProject
from database.entities.db_structures import DbProjectBranch
from common_utils import get_deep_value as gdeepval


class AssignmentManagerCore(AssignmentManagerUI):

    def __init__(self, parent=None):
        super(AssignmentManagerCore, self).__init__(parent)

        self.create_connections()
        self.refresh_tree_widget()

    def create_connections(self):
        self.project_tree_viewer_wdg.itemClicked.connect(self.get_selected_entry_name)

# POPULATE THE WIDGET -- START
    def refresh_tree_widget(self):
        try:
            self.project_tree_viewer_wdg.clear()
            get_branches = DbProjectBranch.get_branches()
            for branch in sorted(get_branches):
                item = self.show_tree_create_item(branch)
                self.project_tree_viewer_wdg.addTopLevelItem(item)
            self.project_tree_viewer_wdg.expandAll()
        except:
            print ("Something wrong in refresh_tree_widget")

    def show_tree_create_item(self, name):
        iso_name = self.get_entry_name_from_id(name)
        item = QtWidgets.QTreeWidgetItem([iso_name])
        self.add_children(item)
        return item

    def get_entry_name_from_id(self, name: str, delimiter=".") -> str:
        if delimiter not in name:
            return name
        isolate_last = name.split(delimiter)[-1]
        return isolate_last

    def add_children(self, item):
        get_children = gdeepval.deep_values(item.text(0), self.get_show_structure())
        for children in get_children:
            for child in sorted(children):
                is_ref = self.is_entity_reference(child)
                if child != "type":
                    child_item = self.show_tree_create_item(child)
                    if is_ref:
                        child_item.setCheckState(0, QtCore.Qt.Unchecked)
                    item.addChild(child_item)

    def is_entity_reference(self, string_to_check, delimiter=","):
        if delimiter in string_to_check:
            return True


    def get_show_structure(self):
        try:
            entity = DbProject.get_structure()
            return entity
        except:
            print ("shit Happened!! in GET_SHOW_STRUCTURE_FUNC")

# POPULATE THE WIDGET -- END

# SELECTION METHODS - START
    def get_selected(self):
        selected = self.project_tree_viewer_wdg.selectedItems()
        return selected

    def get_selected_entry(self):
        names = []
        get_selected_objects = self.project_tree_viewer_wdg.selectedItems()
        if len(get_selected_objects) == 0:
            return []
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                names.append(item.text(0))
            return names[0]

    def get_selected_entry_name(self):
        names = []
        get_selected_objects = self.project_tree_viewer_wdg.selectedItems()
        if len(get_selected_objects) == 0:
            return []
        elif len(get_selected_objects) >= 1:
            for item in get_selected_objects:
                names.append(item.text(0))
            return names[0]

# SELECTION METHODS - END

# Label - START
    def update_label(self):
        current_entity_name = Envars().entry_name
        my_font = QtGui.QFont()
        my_font.setBold(True)

        self.assignemnt_manager_lb.clear()
        self.assignemnt_manager_lb.setText("{0}\nAssigned To".format(current_entity_name.upper()))
        self.assignemnt_manager_lb.setFont(my_font)
        self.assignemnt_manager_lb.setStyleSheet("color: red")


if __name__ == '__main__':
    import sys

    Envars.show_name = "Green"
    Envars.branch_name = "assets"
    Envars.category = "props"
    Envars.entry_name = "red_knife"
    Envars.task_name = "modeling"

    # from envars.envars import Envars
    app = QtWidgets.QApplication(sys.argv)
    font = app.instance().setFont(QtGui.QFont())

    # Envars.show_name = "Test"
    # Envars.branch_name = "sequences"
    # Envars.category = "GooGoo"
    # Envars.entry_name = "circle"
    # Envars.task_name = "rigging"

    test_dialog = AssignmentManagerCore()

    # test_dialog.current_show()
    # test_dialog.comboBox_shows()
    # test_dialog.set_show_to()
    test_dialog.show()
    sys.exit(app.exec_())