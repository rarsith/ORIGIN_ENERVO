from database import db_connection as mdbconn
from database.db_ids import DbIds
from database.db_paths import DbPaths
from database import db_templates
from database.entities.db_project import DbProject
from database.utils.db_update import DbUpdate
from database.entities.properties.db_sync_tasks import DbSyncTasks
from envars.envars import Envars


class DbPubSlot(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self, name):
        asset_id = DbPaths().path_to_entry()
        cursor = self.db[DbProject().get_branch_type]
        task_pub_slot_db_path = DbPaths.make_path(DbPaths.path_to_task_pub_slots(), name)
        tasks_pub_slot_defaults = db_templates.tasks_pub_slot_schema()

        cursor.update_one({"_id": asset_id}, {"$set": {task_pub_slot_db_path: tasks_pub_slot_defaults}})

        DbSyncTasks().add_sync_task_slot(name)
        print("{} Task Pub Slot created!".format(name))
        return name

    def add(self, pub_slot=[]):
        for each in pub_slot:
            task_imports_from_address = DbPaths.make_path(DbPaths.path_to_task_pub_slots(), each)
            asset_id = DbIds.db_entry_id()
            DbUpdate().origin_update(asset_id, task_imports_from_address)
            print("{} added as pub_slot".format(each))

    def add_dict(self, pub_slot=[]):
        asset_id = DbIds.db_entry_id()
        for each in pub_slot:
            get_slot_name = (list(each.keys()))
            get_slot_param = (list(each.values()))
            pub_slot_path = DbPaths.make_path(DbPaths.path_to_task_pub_slots(), get_slot_name[0])
            DbUpdate().origin_update(asset_id, pub_slot_path, get_slot_param[0])
        print("Publish Slot added succesfully!")

    def get_pub_slots(self):
        try:
            task_path = DbPaths.make_path("tasks", Envars.task_name, "pub_slots")
            cursor = self.db[DbProject().get_branch_type]
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                for tsk, tsk_name in tasks.items():
                    return list(tsk_name[Envars.task_name]['pub_slots'])

        except:
            pass

    def get_type(self, pub_slot):
        try:
            task_path = DbPaths.make_path("tasks", Envars.task_name, "pub_slots", pub_slot, "type")
            cursor = self.db[DbProject().get_branch_type]
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]["pub_slots"][pub_slot]["type"]

        except:
            pass

    def get_method(self, pub_slot):
        try:
            task_path = DbPaths.make_path("tasks", Envars.task_name, "pub_slots", pub_slot, "method")
            cursor = self.db[DbProject().get_branch_type]
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]["pub_slots"][pub_slot]["method"]

        except:
            pass

    def get_used_by(self, pub_slot):
        try:
            task_path = DbPaths.make_path("tasks", Envars.task_name, "pub_slots", pub_slot, "used_by")
            cursor = self.db[DbProject().get_branch_type]
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]["pub_slots"][pub_slot]["used_by"]

        except:
            pass

    def get_used_by_task(self, data, task_name):
        get_pub_slots = []
        get_slots = list(data.keys())
        for x in get_slots:
            if task_name in data[x]['used_by']:
                get_pub_slots.append(x)
        return get_pub_slots

    def get_is_reviewable(self, pub_slot):
        try:
            task_path = DbPaths.make_path("tasks", Envars.task_name, "pub_slots", pub_slot, "reviewable")
            cursor = self.db[DbProject().get_branch_type]
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]["pub_slots"][pub_slot]["reviewable"]

        except:
            pass

    def get_is_active(self, pub_slot):
        try:
            task_path = DbPaths.make_path("tasks", Envars.task_name, "pub_slots", pub_slot, "active")
            cursor = self.db[DbProject().get_branch_type]
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]["pub_slots"][pub_slot]["active"]

        except:
            pass

    def set_used_by(self, pub_slot, used_by, remove_action=False):
        cursor = self.db[DbProject().get_branch_type]
        pub_slot_path = DbPaths.make_path(DbPaths().path_to_task_pub_slots(), pub_slot, "used_by")
        asset_id = DbIds.db_entry_id()

        existing_data = cursor.find_one({"_id": asset_id}, {'_id': 0, pub_slot_path: 1})
        existing_assignment = existing_data['tasks'][Envars.task_name]['pub_slots'][pub_slot]['used_by']
        if not remove_action:
            if used_by not in existing_assignment:
                cursor.update_one({"_id": asset_id}, {"$push": {pub_slot_path: used_by}})
        else:
            if used_by in existing_assignment:
                cursor.update_one({"_id": asset_id}, {"$pull": {pub_slot_path: used_by}})

    def remove(self):
        try:
            task_path = DbPaths.path_to_task_pub_slots()
            print(task_path)
            cursor = self.db[DbProject().get_branch_type]
            cursor.update_one({"_id": DbIds.db_entry_id()}, {"$unset": {task_path: 1}})
            cursor.update_one({"_id": DbIds.db_entry_id()}, {"$set": {task_path: {}}})
        except:
            pass

