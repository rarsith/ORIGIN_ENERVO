import sys
from PySide2 import QtWidgets, QtCore, QtGui
from envars.envars import Envars

from ui.custom_widgets.task_publishing_slot_used_by_view_UI import TaskPubSlotUsedByUI
from database.entities.db_entities import DbAsset, DbTasks, DbPubSlot


class TasksPubSlotUsedByCore(TaskPubSlotUsedByUI):
    def __init__(self, parent=None):
        super(TasksPubSlotUsedByCore, self).__init__(parent)

        self.create_connections()

    def create_connections(self):
        self.imports_from_wdg.itemClicked.connect(self.populate_task_dependent_schema)

    def populate_main_widget(self):
        self.populate_existing_tasks()
        self.remove_self_task()
        self.imports_from_wdg.expandAll()

# ImportsFromWidget -- START

    def populate_task_dependent_schema(self):
        get_entry_tasks_names = self.get_all_tasks()
        get_active_tasks = []

        self.all_pub_slots_wdg.clear()

        for task in get_entry_tasks_names:
            is_active = DbTasks().is_active(task=task)

            if is_active:
                get_active_tasks.append(task)

        self.add_tasks_to_list(get_active_tasks)

    def add_tasks_to_list(self, tasks_list):
        for active_task in tasks_list:
            imp_from_pub_slots_schema = DbPubSlot().get_pub_slots(task_name=active_task)
            item = QtWidgets.QTreeWidgetItem([active_task])
            item.setFlags(item.flags() | QtGui.Qt.ItemIsUserCheckable | QtGui.Qt.ItemIsEnabled)
            self.all_pub_slots_wdg.addTopLevelItem(item)

            slot_used_by = self.get_pub_used_by(imp_from_pub_slots_schema)

            try:
                for pub_slot, pub_slot_content in imp_from_pub_slots_schema.items():
                    pub_slot_item = QtWidgets.QTreeWidgetItem([pub_slot])
                    item.addChild(pub_slot_item)

                    if pub_slot_item.text(0) in slot_used_by:
                        pub_slot_item.setCheckState(0, QtCore.Qt.Checked)
                    else:
                        pub_slot_item.setCheckState(0, QtCore.Qt.Unchecked)

            except:
                pass

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

    def get_wdg_checked_items(self):
        checked = dict()
        root = self.imports_from_wdg.invisibleRootItem()
        signal_count = root.childCount()

        for idx in range(signal_count):
            signal = root.child(idx)
            checked_sweeps = list()
            num_children = signal.childCount()

            for child_idx in range(num_children):
                child = signal.child(child_idx)

                if child.checkState(0) == QtCore.Qt.Checked:
                    checked_sweeps.append(child.text(0))
            checked[signal.text(0)] = checked_sweeps
        return checked

    def get_wdg_unchecked_items(self):
        unchecked = dict()
        root = self.imports_from_wdg.invisibleRootItem()
        signal_count = root.childCount()

        for idx in range(signal_count):
            signal = root.child(idx)
            checked_sweeps = list()
            num_children = signal.childCount()

            for child_idx in range(num_children):
                child = signal.child(child_idx)

                if child.checkState(0) == QtCore.Qt.Unchecked:
                    checked_sweeps.append(child.text(0))
            unchecked[signal.text(0)] = checked_sweeps
        return unchecked

    def write_wdg_checked_items(self):
        current_task = Envars().task_name
        checked_items = self.get_wdg_checked_items()
        unchecked_items = self.get_wdg_unchecked_items()
        for task_name, task_pub_slots in checked_items.items():
            for pub_slot in task_pub_slots:
                DbPubSlot().set_used_by(task_name=task_name,
                                        pub_slot=pub_slot,
                                        used_by_data=current_task)

        for task_name, task_pub_slots in unchecked_items.items():
            for pub_slot in task_pub_slots:
                DbPubSlot().set_used_by(task_name=task_name,
                                        pub_slot=pub_slot,
                                        used_by_data=current_task,
                                        remove_action=True)

    def clean_wdg(self, sel_item):
        current_task = Envars().task_name
        checked = dict()
        signal_count = sel_item.childCount()
        checked_sweeps = list()

        for i in range(signal_count):
            signal = sel_item.child(i)
            if signal.checkState(0) == QtCore.Qt.Checked:
                checked_sweeps.append(signal.text(0))
            checked[sel_item.text(0)] = checked_sweeps

        for task_name, task_pub_slots in checked.items():
            for pub_slot in task_pub_slots:
                DbPubSlot().set_used_by(task_name=task_name,
                                        pub_slot=pub_slot,
                                        used_by_data=current_task,
                                        remove_action=True)

    def save_to_database(self):
        self.write_wdg_checked_items()
        DbTasks().rem_import_slots()
        DbTasks().imports_from = self.get_wdg_top_level_items_list()
        self.populate_main_widget()

# ImportsFromWidget -- END

    def get_all_tasks(self):
        tasks = DbTasks().get_tasks()
        if tasks is not None:
            return tasks
        else:
            return ["-- no tasks --"]


if __name__ == "__main__":
    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "red_knife"
    Envars.task_name = "modeling"

    app = QtWidgets.QApplication(sys.argv)
    test_dialog = TasksPubSlotUsedByCore()

    test_dialog.populate_main_widget()
    test_dialog.show()
    sys.exit(app.exec_())