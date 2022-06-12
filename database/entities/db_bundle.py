from database import db_connection as mdbconn
from database.db_ids import DbIds
from database.db_paths import DbPaths
from database.db_references import DbRef
from database.entities.db_project import DbProject
from database.entities.properties.db_tasks import DbTasks
from database.db_versions_control import DBVersionControl
from envars.envars import Envars
from common_utils.date_time import DateTime
from common_utils.users import Users


class OriginBundle(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create_bundle_slot(self, name):
        pass

    def add_to_bundle(self, entity_id, bundle_id, slot):

        DbRef.add_db_id_reference("bundles",
                                        bundle_id,
                                        "master_bundle.{}".format(slot),
                                        entity_id,
                                        DbProject().get_branch_type,
                                        replace=True)
        return bundle_id

    def remove_bundle_slot(self, name):
        pass

    def update_bundle_slot(self, name):
        pass

    def update_master_bundle(self):
        pass

    def set_as_current(self, bundle_id, add_to_stream="main_stream"):

        DbRef.add_db_id_reference(DbProject().get_branch_type,
                                        DbIds.db_entry_id(),
                                        "master_bundle.{}".format(add_to_stream),
                                        bundle_id,
                                        "bundles",
                                        replace=True)
        return bundle_id

    def set_slot_state(self, state):
        statuses = ["renderable", "non-renderable", "matte_object"]

        pass

    def db_validate_bundle(self):
        pass

    def db_health_check(self):
        pass

    def db_create_bundle_stream(self, name):
        try:
            asset_id = DbPaths().db_entry_path()
            cursor = self.db[DbProject().get_branch_type]
            db_path = DbPaths.origin_path(DbPaths.db_asset_master_bundle_path(), (name+"_"+"stream"))

            cursor.update_one({"_id": asset_id}, {"$set": {db_path:[]}})
            print("{} Bundle Stream  created!".format(name))
            return name

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def db_move_to_stream(self, from_stream, to_stream):
        try:
            task_path = DbPaths.db_task_pub()
            print(task_path)
            cursor = self.db[DbProject().get_branch_type]
            cursor.update_one({"_id": DbIds.db_entry_id()}, {"$unset": {task_path: 1}})
            cursor.update_one({"_id": DbIds.db_entry_id()}, {"$set": {task_path: {}}})
        except:
            pass

    def db_create_bundle(self):
        status = "PENDING-REVIEW"
        entity_tasks = DbTasks().get_tasks()
        version = DBVersionControl().db_master_bundle_ver_increase()
        common_id = DbIds.db_master_bundle_id(version)
        set_display_name = "_".join([Envars.entry_name, "bundle"])

        save_content=dict(
            _id=common_id,
            show_name=Envars.show_name,
            entry_name=Envars.entry_name,
            category=Envars.category,
            branch=Envars.branch_name,
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
