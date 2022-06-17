from database import db_templates
from database.utils.db_utils import DbUpdate, DBVersionControl
from database import db_connection as mdbconn
from database.db_components import DbId, DbPath
from database.db_defaults import DbDefaults
from database.entities.db_structures import DbProjectBranch
from envars.envars import Envars
from common_utils.date_time import DateTime
from common_utils.users import Users


class DbTasks(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self, name):
        asset_id = DbPath().to_entry()
        cursor = self.db[DbProjectBranch().get_branch_type]
        task_db_path = DbPath.make_path(DbPath.to_task(), name)
        tasks_defaults = db_templates.task_defaults()

        cursor.update_one({"_id": asset_id}, {"$set": {task_db_path: tasks_defaults}})

        DbSyncTasks().add_sync_task(name)
        print("{} Origin Asset Task created!".format(name))

        return name

    def get_tasks(self):
        try:
            cursor = self.db[DbProjectBranch().get_branch_type]
            tasks_list = cursor.find({"_id": DbId.curr_entry_id()}, {'_id': 0, 'tasks': 1})
            for elements in tasks_list:
                return list(elements["tasks"].keys())
        except:
            pass

    def get_tasks_full(self):
        try:
            cursor = self.db[DbProjectBranch().get_branch_type]
            tasks_list = cursor.find({"_id": DbId.curr_entry_id()}, {'_id': 0, 'tasks': 1})
            for elements in tasks_list:
                return elements["tasks"]
        except:
            pass

    def get_definition(self, task=Envars.task_name):
        # TODO, needs to be checked for what it is used
        try:
            task_path = DbPath.make_path("tasks", task)
            cursor = self.db[DbProjectBranch().get_branch_type]
            tasks_list = cursor.find({"_id": DbId.curr_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return (tasks["tasks"][task])
        except:
            pass

    def get_imports_from(self):
        try:
            task_path = DbPath.make_path("tasks", Envars.task_name, "imports_from")
            cursor = self.db[DbProjectBranch().get_branch_type]
            tasks_list = cursor.find({"_id": DbId.curr_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                for tsk, tsk_name in tasks.items():
                    return list(tsk_name[Envars.task_name]['imports_from'])

        except:
            pass

    def get_status(self):
        try:
            task_path = DbPath.make_path("tasks", Envars.task_name, "status")
            cursor = self.db[DbProjectBranch().get_branch_type]
            tasks_list = cursor.find({"_id": DbId.curr_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]['status']

        except:
            pass

    def get_is_active(self):
        try:
            task_path = DbPath.make_path("tasks", Envars.task_name, "active")
            cursor = self.db[DbProjectBranch().get_branch_type]
            tasks_list = cursor.find({"_id": DbId.curr_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]['active']

        except:
            pass

    def set_imports_from(self, imports_from=[]):
        for each in imports_from:
            task_imports_from_address = DbPath.make_path(DbPath.to_task_imports_from(), each)
            asset_id = DbId.curr_entry_id()
            DbUpdate().origin_update(asset_id, task_imports_from_address)
            print("{} task added as import_source".format(each))

    def set_status(self, task_status):
        asset_id = DbPath().to_entry()
        db_collection = self.db[DbProjectBranch().get_branch_type]
        db_address = DbPath.make_path(DbPath.to_task(), "status")
        db_collection.update_one({"_id": asset_id}, {'$set': {db_address: task_status}})

    def set_user(self, artist_name):
        asset_id = DbPath().to_entry()
        db_collection = self.db[DbProjectBranch().get_branch_type]
        db_address = DbPath.make_path(DbPath.to_task(), "artist")
        db_collection.update_one({"_id": asset_id}, {'$set': {db_address: artist_name}})

    def set_is_active(self, is_active=True):
        db_collection = self.db[DbProjectBranch().get_branch_type]
        db_address = DbPath.make_path(DbPath.to_task(), "active")
        db_collection.update_one({"_id": DbId.curr_entry_id()}, {'$set': {db_address: is_active}})

    def rem_import_slots(self):
        try:
            task_path = DbPath.to_task_imports_from()
            cursor = self.db[DbProjectBranch().get_branch_type]
            cursor.update_one({"_id": DbId.curr_entry_id()}, {"$unset": {task_path: 1}})
            cursor.update_one({"_id": DbId.curr_entry_id()}, {"$set": {task_path: {}}})
        except:
            pass


class DbSyncTasks(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    @staticmethod
    def create_from_template():
        get_tasks_config = DbDefaults().get_show_defaults(DbDefaults().root_tasks)
        entity_tasks = list(get_tasks_config[0])
        save_elements_list = dict()
        for task in entity_tasks:
            task_definition = (get_tasks_config[0][task])
            task_pub_slots = (list(task_definition["pub_slots"].keys()))
            make_dictionary = dict.fromkeys(task_pub_slots, {})
            nest_slot = {task: make_dictionary}
            save_elements_list.update(nest_slot)

        return save_elements_list

    def capture_all(self):
        try:
            cursor = self.db[DbProjectBranch().get_branch_type]
            tasks_list = cursor.find({"_id": DbId.curr_entry_id()}, {'_id': 0, 'sync_tasks': 1})
            for elements in tasks_list:
                return (elements["sync_tasks"])
        except:
            pass

    def add(self, data={}):
        existing_sync_tasks = self.capture_all()
        return existing_sync_tasks.update(data)

    def add_sync_task(self, name):
        asset_id = DbPath().to_entry()
        cursor = self.db[DbProjectBranch().get_branch_type]
        sync_task_db_path = DbPath.make_path(DbPath.to_sync_tasks(), name)
        cursor.update_one({"_id": asset_id}, {"$set": {sync_task_db_path:{}}})
        print("{} Sync Tasks saved!".format(name))

    def add_sync_task_slot(self, name):
        asset_id = DbId().curr_entry_id()
        cursor = self.db[DbProjectBranch().get_branch_type]
        sync_task_db_path = DbPath.make_path(DbPath.to_sync_task_slot(), name)
        cursor.update_one({"_id": asset_id}, {"$set": {sync_task_db_path: {}}})
        print("{} Sync Slot saved!".format(name))

    def publish_sync_state(self):
        existing_sync_tasks = self.capture_all()
        version = DBVersionControl().db_sync_tasks_ver_increase()
        print (version)
        entity_id = DbId.get_sync_tasks_id(version)

        entity_attributes = dict(
            _id= entity_id,
            show_name= Envars.show_name,
            entry_name= Envars.entry_name,
            category= Envars.category,
            version=version,
            sync_tasks= existing_sync_tasks,
            date=DateTime().return_date,
            time=DateTime().return_time,
            owner= Users.get_current_user()

        )

        try:
            self.db.sync_tasks.insert_one(entity_attributes)

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def get_sync_task_slots(self):
        try:
            cursor = self.db[DbProjectBranch().get_branch_type]
            sync_task_db_path = DbPath.make_path(DbPath.to_sync_task_slot())
            tasks_list = cursor.find({"_id": DbId.curr_entry_id()}, {'_id': 0, sync_task_db_path: 1})
            for elements in tasks_list:
                sync_task_values = list(elements["sync_tasks"].values())[0]
                sync_task_slots = list(sync_task_values.keys())
                return sync_task_slots
        except ValueError as vale:
            print(vale)


    # def update(self, data):
    #     update_sync = self.add(data)
    #     self.commit(update_sync)


class DbPubSlot(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self, name):
        asset_id = DbPath().to_entry()
        cursor = self.db[DbProjectBranch().get_branch_type]
        task_pub_slot_db_path = DbPath.make_path(DbPath.to_pub_slots(), name)
        tasks_pub_slot_defaults = db_templates.tasks_pub_slot_schema()

        cursor.update_one({"_id": asset_id}, {"$set": {task_pub_slot_db_path: tasks_pub_slot_defaults}})

        DbSyncTasks().add_sync_task_slot(name)
        print("{} Task Pub Slot created!".format(name))
        return name

    def add(self, pub_slot=[]):
        for each in pub_slot:
            task_imports_from_address = DbPath.make_path(DbPath.to_pub_slots(), each)
            asset_id = DbId.curr_entry_id()
            DbUpdate().origin_update(asset_id, task_imports_from_address)
            print("{} added as pub_slot".format(each))

    def add_dict(self, pub_slot=[]):
        asset_id = DbId.curr_entry_id()
        for each in pub_slot:
            get_slot_name = (list(each.keys()))
            get_slot_param = (list(each.values()))
            pub_slot_path = DbPath.make_path(DbPath.to_pub_slots(), get_slot_name[0])
            DbUpdate().origin_update(asset_id, pub_slot_path, get_slot_param[0])
        print("Publish Slot added succesfully!")

    def get_pub_slots(self):
        try:
            task_path = DbPath.make_path("tasks", Envars.task_name, "pub_slots")
            cursor = self.db[DbProjectBranch().get_branch_type]
            tasks_list = cursor.find({"_id": DbId.curr_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                for tsk, tsk_name in tasks.items():
                    return list(tsk_name[Envars.task_name]['pub_slots'])

        except:
            pass

    def get_type(self, pub_slot):
        try:
            task_path = DbPath.make_path("tasks", Envars.task_name, "pub_slots", pub_slot, "type")
            cursor = self.db[DbProjectBranch().get_branch_type]
            tasks_list = cursor.find({"_id": DbId.curr_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]["pub_slots"][pub_slot]["type"]

        except:
            pass

    def get_method(self, pub_slot):
        try:
            task_path = DbPath.make_path("tasks", Envars.task_name, "pub_slots", pub_slot, "method")
            cursor = self.db[DbProjectBranch().get_branch_type]
            tasks_list = cursor.find({"_id": DbId.curr_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]["pub_slots"][pub_slot]["method"]

        except:
            pass

    def get_used_by(self, pub_slot):
        try:
            task_path = DbPath.make_path("tasks", Envars.task_name, "pub_slots", pub_slot, "used_by")
            cursor = self.db[DbProjectBranch().get_branch_type]
            tasks_list = cursor.find({"_id": DbId.curr_entry_id()}, {'_id': 0, task_path: 1})
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
            task_path = DbPath.make_path("tasks", Envars.task_name, "pub_slots", pub_slot, "reviewable")
            cursor = self.db[DbProjectBranch().get_branch_type]
            tasks_list = cursor.find({"_id": DbId.curr_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]["pub_slots"][pub_slot]["reviewable"]

        except:
            pass

    def get_is_active(self, pub_slot):
        try:
            task_path = DbPath.make_path("tasks", Envars.task_name, "pub_slots", pub_slot, "active")
            cursor = self.db[DbProjectBranch().get_branch_type]
            tasks_list = cursor.find({"_id": DbId.curr_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]["pub_slots"][pub_slot]["active"]

        except:
            pass

    def set_used_by(self, pub_slot, used_by, remove_action=False):
        cursor = self.db[DbProjectBranch().get_branch_type]
        pub_slot_path = DbPath.make_path(DbPath().to_pub_slots(), pub_slot, "used_by")
        asset_id = DbId.curr_entry_id()

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
            task_path = DbPath.to_pub_slots()
            print(task_path)
            cursor = self.db[DbProjectBranch().get_branch_type]
            cursor.update_one({"_id": DbId.curr_entry_id()}, {"$unset": {task_path: 1}})
            cursor.update_one({"_id": DbId.curr_entry_id()}, {"$set": {task_path: {}}})
        except:
            pass


class DbCollections(object):

    @classmethod
    def show(cls):
        return "show"

    @classmethod
    def main_publishes(cls):
        return 'publishes'

    @classmethod
    def bundles(cls):
        return 'bundles'

    @classmethod
    def sync_tasks(cls):
        return 'sync_tasks'

    @classmethod
    def wip(cls):
        return 'wip_scenes'
