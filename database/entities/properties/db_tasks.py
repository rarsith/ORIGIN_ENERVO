from database import db_connection as mdbconn
from database.db_ids import DbIds
from database.db_paths import DbPaths
from database import db_templates
from database.utils.db_update import DbUpdate
from database.entities.db_project import DbProject
from database.entities.properties.db_sync_tasks import DbSyncTasks
from envars.envars import Envars


class DbTasks(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self, name):
        asset_id = DbPaths().path_to_entry()
        cursor = self.db[DbProject().get_branch_type]
        task_db_path = DbPaths.make_path(DbPaths.path_to_task(), name)
        tasks_defaults = db_templates.task_defaults()

        cursor.update_one({"_id": asset_id}, {"$set": {task_db_path: tasks_defaults}})

        DbSyncTasks().add_sync_task(name)
        print("{} Origin Asset Task created!".format(name))

        return name

    def get_tasks(self):
        try:
            cursor = self.db[DbProject().get_branch_type]
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, 'tasks': 1})
            for elements in tasks_list:
                return list(elements["tasks"].keys())
        except:
            pass

    def get_tasks_full(self):
        try:
            cursor = self.db[DbProject().get_branch_type]
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, 'tasks': 1})
            for elements in tasks_list:
                return elements["tasks"]
        except:
            pass

    def get_definition(self, task=Envars.task_name):
        # TODO, needs to be checked for what it is used
        try:
            task_path = DbPaths.make_path("tasks", task)
            cursor = self.db[DbProject().get_branch_type]
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return (tasks["tasks"][task])
        except:
            pass

    def get_imports_from(self):
        try:
            task_path = DbPaths.make_path("tasks", Envars.task_name, "imports_from")
            cursor = self.db[DbProject().get_branch_type]
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                for tsk, tsk_name in tasks.items():
                    return list(tsk_name[Envars.task_name]['imports_from'])

        except:
            pass

    def get_status(self):
        try:
            task_path = DbPaths.make_path("tasks", Envars.task_name, "status")
            cursor = self.db[DbProject().get_branch_type]
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]['status']

        except:
            pass

    def get_is_active(self):
        try:
            task_path = DbPaths.make_path("tasks", Envars.task_name, "active")
            cursor = self.db[DbProject().get_branch_type]
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]['active']

        except:
            pass

    def set_imports_from(self, imports_from=[]):
        for each in imports_from:
            task_imports_from_address = DbPaths.make_path(DbPaths.path_to_task_imports_from(), each)
            asset_id = DbIds.db_entry_id()
            DbUpdate().origin_update(asset_id, task_imports_from_address)
            print("{} task added as import_source".format(each))

    def set_status(self, task_status):
        asset_id = DbPaths().path_to_entry()
        db_collection = self.db[DbProject().get_branch_type]
        db_address = DbPaths.make_path(DbPaths.path_to_task(), "status")
        db_collection.update_one({"_id": asset_id}, {'$set': {db_address: task_status}})

    def set_user(self, artist_name):
        asset_id = DbPaths().path_to_entry()
        db_collection = self.db[DbProject().get_branch_type]
        db_address = DbPaths.make_path(DbPaths.path_to_task(), "artist")
        db_collection.update_one({"_id": asset_id}, {'$set': {db_address: artist_name}})

    def set_is_active(self, is_active=True):
        db_collection = self.db[DbProject().get_branch_type]
        db_address = DbPaths.make_path(DbPaths.path_to_task(), "active")
        db_collection.update_one({"_id": DbIds.db_entry_id()}, {'$set': {db_address: is_active}})

    def rem_import_slots(self):
        try:
            task_path = DbPaths.path_to_task_imports_from()
            cursor = self.db[DbProject().get_branch_type]
            cursor.update_one({"_id": DbIds.db_entry_id()}, {"$unset": {task_path: 1}})
            cursor.update_one({"_id": DbIds.db_entry_id()}, {"$set": {task_path: {}}})
        except:
            pass

