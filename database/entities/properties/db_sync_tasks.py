from database import db_connection as mdbconn
from database.db_ids import DbIds
from database.db_paths import DbPaths
from database.db_defaults import DbDefaults
from database.entities.db_project import DbProject
from database.db_versions_control import DBVersionControl
from envars.envars import Envars
from common_utils.date_time import DateTime
from common_utils.users import Users


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
            cursor = self.db[DbProject().get_branch_type]
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, 'sync_tasks': 1})
            for elements in tasks_list:
                return (elements["sync_tasks"])
        except:
            pass

    def add(self, data={}):
        existing_sync_tasks = self.capture_all()
        return existing_sync_tasks.update(data)

    def add_sync_task(self, name):
        asset_id = DbPaths().db_entry_path()
        cursor = self.db[DbProject().get_branch_type]
        sync_task_db_path = DbPaths.origin_path(DbPaths.db_sync_task_path(), name)
        cursor.update_one({"_id": asset_id}, {"$set": {sync_task_db_path:{}}})
        print("{} Sync Tasks saved!".format(name))

    def add_sync_task_slot(self, name):
        asset_id = DbIds().db_entry_id()
        cursor = self.db[DbProject().get_branch_type]
        sync_task_db_path = DbPaths.origin_path(DbPaths.db_sync_slot_path(), name)
        cursor.update_one({"_id": asset_id}, {"$set": {sync_task_db_path: {}}})
        print("{} Sync Slot saved!".format(name))

    def publish_sync_state(self):
        existing_sync_tasks = self.capture_all()
        version = DBVersionControl().db_sync_tasks_ver_increase()
        print (version)
        entity_id = DbIds.db_sync_tasks_id(version)

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
            self.db.task_sync.insert_one(entity_attributes)

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def get_sync_task_slots(self):
        try:
            cursor = self.db[DbProject().get_branch_type]
            sync_task_db_path = DbPaths.origin_path(DbPaths.db_sync_slot_path())
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, sync_task_db_path: 1})
            for elements in tasks_list:
                sync_task_values = list(elements["sync_tasks"].values())[0]
                sync_task_slots = list(sync_task_values.keys())
                return sync_task_slots
        except ValueError as vale:
            print(vale)


    # def update(self, data):
    #     update_sync = self.add(data)
    #     self.commit(update_sync)
