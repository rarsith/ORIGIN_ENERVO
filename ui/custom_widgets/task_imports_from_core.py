import sys
from PySide2 import QtWidgets, QtCore
from envars.envars import Envars

from ui.custom_widgets.task_imports_from_UI import TasksImportFromUI
from database.entities.db_entities import DbProject, DbTasks, DbPubSlot


class TasksImportFromCore(TasksImportFromUI):
    def __init__(self, parent=None):
        super(TasksImportFromCore, self).__init__(parent)

        self.create_connections()
        # self.populate_main_widget()

    def create_connections(self):
        self.save_btn.clicked.connect(self.save_to_database)
        self.rem_sel_item_btn.clicked.connect(self.remove_import_task_slot)
        # self.rem_sel_item_btn.clicked.connect(self.populate_main_widget)
        self.refresh_btn.clicked.connect(self.populate_main_widget)
        self.move_to_right_btn.clicked.connect(self.move_selection_to_right)

    def populate_main_widget(self):
        self.populate_existing_tasks()
        self.populate_task_import_schema()
        self.remove_already_assigned()
        self.remove_self_task()

# ImportsFromWidget -- START
    def populate_task_import_schema(self):
        get_schema = self.get_saved_import_schema()
        get_active_tasks = []
        self.imports_from_wdg.clear()
        for task in get_schema:
            is_active = DbTasks().is_active(task=task)

            if is_active:
                get_active_tasks.append(task)

        self.add_items_to_list(get_active_tasks)

    def add_items_to_list(self, items):
        for active_task in items:
            imp_from_pub_slots_schema = DbPubSlot().get_pub_slots(task_name=active_task)
            item = QtWidgets.QTreeWidgetItem([active_task])
            self.imports_from_wdg.addTopLevelItem(item)
            slot_used_by = self.get_pub_used_by(imp_from_pub_slots_schema)

            try:
                for k, v in imp_from_pub_slots_schema.items():
                    self.x = QtWidgets.QTreeWidgetItem([k])
                    item.addChild(self.x)

                    if self.x.text(0) in slot_used_by:
                        self.x.setCheckState(0, QtCore.Qt.Checked)
                    else:
                        self.x.setCheckState(0, QtCore.Qt.Unchecked)

            except:
                pass

    def handle_item_changed(self, item, column):
        item_parent = item.parent()
        try:
            if item.checkState(column) == QtCore.Qt.Checked:
                print('{0} Item Checked, with {1} Parent'.format(item.text(0), item_parent.text(0)))
            elif item.checkState(column) == QtCore.Qt.Unchecked:
                print('{0} Item Unchecked, with {1} Parent'.format(item.text(0), item_parent.text(0)))
        except:
            pass

    def get_saved_import_schema(self):
        existing_imports_from = DbTasks().imports_from
        if existing_imports_from == None:
            return []
        else:
            return existing_imports_from

    def get_pub_imports(self, task_name):
        pub_imports = DbPubSlot().get_pub_slots(task_name=task_name)
        return pub_imports

    def get_pub_used_by(self, extract):
        rel_task = DbPubSlot().get_used_by_task(data=extract)
        return rel_task

    def get_wdg_top_level_items_list(self):
        list_all = []
        nnn = self.imports_from_wdg.topLevelItemCount()
        ccc = self.imports_from_wdg.invisibleRootItem()
        for each_item in (range(nnn)):
            sel = ccc.child(each_item)
            list_all.append(sel.text(0))
        return list_all

    def get_all_items(self):
        checked = dict()
        root = self.imports_from_wdg.invisibleRootItem()
        signal_count = root.childCount()

        for i in range(signal_count):
            signal = root.child(i)
            checked_sweeps = list()
            num_children = signal.childCount()

            for n in range(num_children):
                child = signal.child(n)
                checked_sweeps.append(child.text(0))
                checked[signal.text(0)] = checked_sweeps

        return checked

    def get_wdg_checked_items(self):
        checked = dict()
        root = self.imports_from_wdg.invisibleRootItem()
        signal_count = root.childCount()

        for i in range(signal_count):
            signal = root.child(i)
            checked_sweeps = list()
            num_children = signal.childCount()

            for n in range(num_children):
                child = signal.child(n)

                if child.checkState(0) == QtCore.Qt.Checked:
                    checked_sweeps.append(child.text(0))
            checked[signal.text(0)] = checked_sweeps
        return checked

    def get_wdg_unchecked_items(self):
        unchecked = dict()
        root = self.imports_from_wdg.invisibleRootItem()
        signal_count = root.childCount()

        for i in range(signal_count):
            signal = root.child(i)
            checked_sweeps = list()
            num_children = signal.childCount()

            for n in range(num_children):
                child = signal.child(n)

                if child.checkState(0) == QtCore.Qt.Unchecked:
                    checked_sweeps.append(child.text(0))
            unchecked[signal.text(0)] = checked_sweeps
        return unchecked

    def write_wdg_checked_items(self):
        current_task = Envars().task_name
        checked_items = self.get_wdg_checked_items()
        unchecked_items = self.get_wdg_unchecked_items()
        for k, v in checked_items.items():
            for each in v:
                DbPubSlot().set_used_by(task_name=k,
                                        pub_slot=each,
                                        used_by=current_task)

        for k, v in unchecked_items.items():
            for each in v:
                DbPubSlot().set_used_by(task_name=k,
                                        pub_slot=each,
                                        used_by=current_task,
                                        remove_action=True)

    def clean_wdg(self, sel_item):
        checked = dict()
        signal_count = sel_item.childCount()
        checked_sweeps = list()
        for i in range(signal_count):
            signal = sel_item.child(i)
            if signal.checkState(0) == QtCore.Qt.Checked:
                checked_sweeps.append(signal.text(0))
            checked[sel_item.text(0)] = checked_sweeps

        for k, v in checked.items():
            for each in v:
                DbPubSlot().set_used_by(task_name=k, pub_slot=each, remove_action=True)

    def remove_import_task_slot(self):
        listItems = self.imports_from_wdg.currentItem()
        self.clean_wdg(listItems)
        selected_index = self.imports_from_wdg.indexFromItem(listItems)
        remove_it = selected_index.row()
        self.imports_from_wdg.takeTopLevelItem(remove_it)

    def save_to_database(self):
        self.write_wdg_checked_items()
        DbTasks().rem_import_slots()
        DbTasks().imports_from = self.get_wdg_top_level_items_list()

# ImportsFromWidget -- END

# ListEntryTasks -- START

    def populate_existing_tasks(self):
        self.existing_tasks_lwd.clear()
        all_tasks = self.get_all_tasks()
        if all_tasks == None:
            return []

        else:
            for i in all_tasks:
                QtWidgets.QListWidgetItem(i, self.existing_tasks_lwd)

    def get_all_tasks(self):
        tasks = DbTasks().get_tasks()
        if tasks != None:
            return tasks
        else:
            return ["-- no tasks --"]

    def remove_self_task(self):
        current_task = Envars().task_name
        entries = self.existing_tasks_lwd.findItems(current_task, QtCore.Qt.MatchFixedString)
        for entry in entries:
            indexes = self.existing_tasks_lwd.indexFromItem(entry)
            self.existing_tasks_lwd.takeItem(indexes.row())

# ListEntryTasks -- START

    def get_imports_from(self):
        list_all = []
        nnn = self.imports_from_wdg.topLevelItemCount()
        ccc = self.imports_from_wdg.invisibleRootItem()
        for each_item in (range(nnn)):
            sel = ccc.child(each_item)
            list_all.append(sel.text(0))
        return list_all

    def remove_already_assigned(self):
        existing_assignments = self.get_imports_from()
        for task_name in existing_assignments:
            entries = self.existing_tasks_lwd.findItems(task_name, QtCore.Qt.MatchFixedString)
            for entry in entries:
                indexes = self.existing_tasks_lwd.indexFromItem(entry)
                self.existing_tasks_lwd.takeItem(indexes.row())

    def move_selection_to_right(self):
        text = self.existing_tasks_lwd.selectedItems()
        for item in text:
            self.add_items_to_list([item.text()])
            print ("{0} item added to schema".format (item.text()))
            self.existing_tasks_lwd.takeItem(self.existing_tasks_lwd.row(item))
            self.imports_from_wdg.collapseAll()


if __name__ == "__main__":


    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "new_monster"
    Envars.task_name = "groom"

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = TasksImportFromCore()

    test_dialog.populate_main_widget()
    test_dialog.show()
    sys.exit(app.exec_())