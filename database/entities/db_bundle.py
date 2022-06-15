from database import db_connection as mdbconn
from envars.envars import Envars
from database.db_ids import DbIds
from database.db_paths import DbPaths
from database.db_references import DbReferences
from database.entities.db_project import DbProject
from database.entities.properties.db_tasks import DbTasks
from database.db_versions_control import DBVersionControl
from common_utils.date_time import DateTime
from common_utils.users import Users

# class DbStatuses(object):
#     #TODO: to remove after method impementation in "./database/db_statuses.py"
#     wip: str = "WIP"
#     init: str = "INIT"
#     in_progress: str = "IN PROGRESS"
#     pending_rev: str = "PENDING-REVIEW"
#     approved_internal: str = "APPROVED_INT"
#     approved_client: str = "APPROVED_CLIENT"
#     approved_temp: str = "APPROVED_TEMP"
#     approved_tech: str = "APPROVED_TECH"
#
#
# class Bundle(object):
#
#     collection:str = "bundles"
#
#     _id: str = common_id
#     show_name: str = DbAttributes.show_name
#     entry_name: str = DbAttributes.entry_name
#     category: str = DbAttributes.category
#     branch: str = DbAttributes.branch_name
#     display_name: str = "_".join([DbAttributes.entry_name, "bundle", version])
#     artist: str = Users.get_current_user()
#     status: str = DbStatuses.pending_rev
#     version: str = DBVersionControl().db_master_bundle_ver_increase()
#     date: str = DateTime().return_date,
#     time: str = DateTime().return_time,
#     master_bundle: dict = dict.fromkeys(entity_tasks, [])



class DbBundle(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self):
        status = "PENDING-REVIEW"
        entity_tasks = DbTasks().get_tasks()
        version = DBVersionControl().db_master_bundle_ver_increase()
        common_id = DbIds.db_master_bundle_id(version)
        set_display_name = "_".join([Envars.entry_name, "bundle"])

        save_content=dict(
            _id=common_id,
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name=Envars.entry_name,
            display_name=set_display_name,
            artist=Users.get_current_user(),
            status=status,
            version=version,
            date=DateTime().return_date,
            time=DateTime().return_time,
            master_bundle=dict.fromkeys(entity_tasks,[])
        )

        master_bundle = self.db.bundles.insert_one(save_content)

        print("{0}, {1} has been published".format(set_display_name, version))
        return master_bundle.inserted_id

    def create_stream(self, name):
        try:
            asset_id = DbPaths.path_to_entry()
            cursor = self.db[DbProject().get_branch_type]
            db_path = DbPaths.make_path(DbPaths.path_to_master_bundle(), (name + "_" + "stream"))

            cursor.update_one({"_id": asset_id}, {"$set": {db_path:[]}})
            print("{} Bundle Stream  created!".format(name))
            return name

        except ValueError as e:
            print("{} Error! Nothing Created!".format(e))

    def add_slot(self, name):
        pass

    def add_to_bundle(self, entity_id, bundle_id, slot):

        DbReferences.add_db_id_reference("bundles",
                                        bundle_id,
                                        "master_bundle.{}".format(slot),
                                        entity_id,
                                        DbProject().get_branch_type,
                                        replace=True)
        return bundle_id

    def rem_slot(self, name):
        pass

    def update_slot(self, name):
        pass

    def update_master(self):
        pass

    def set_as_current(self, bundle_id, add_to_stream="main_stream"):

        DbReferences.add_db_id_reference(DbProject().get_branch_type,
                                        DbIds.db_entry_id(),
                                        "master_bundle.{}".format(add_to_stream),
                                        bundle_id,
                                        "bundles",
                                        replace=True)
        return bundle_id

    def set_slot_state(self, state):
        statuses = ["renderable", "matte_object"]
        pass

    def validate_bundle(self):
        pass

    def health_check(self):
        pass

    def mv_to_stream(self, from_stream, to_stream):
        try:
            task_path = DbPaths.path_to_task_pub_slots()
            print(task_path)
            cursor = self.db[DbProject().get_branch_type]
            cursor.update_one({"_id": DbIds.db_entry_id()}, {"$unset": {task_path: 1}})
            cursor.update_one({"_id": DbIds.db_entry_id()}, {"$set": {task_path: {}}})
        except:
            pass

if __name__ == '__main__':
    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "hulk"
    Envars.task_name = "modeling"

    bb = DbBundle()
    name = "GOGO"
    bb.create()


