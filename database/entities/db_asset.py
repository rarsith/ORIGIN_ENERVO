from database import db_connection as mdbconn
from database.db_ids import DbIds
from database.db_paths import DbPaths
from database.db_defaults import DbDefaults
from database.db_references import DbReferences
from database.entities.db_project import DbProject
from database.entities.properties.db_sync_tasks import DbSyncTasks
from envars.envars import Envars
from common_utils.date_time import DateTime
from common_utils.users import Users


class DbAsset(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self, name):
        root_id = DbIds.db_show_id()
        print (root_id)
        asset_id = DbPaths.origin_path(DbPaths.db_category_path(), name)
        print(asset_id)
        collection = self.db[DbProject().get_branch_type]
        get_tasks_config = DbDefaults().get_show_defaults(DbDefaults().root_tasks)

        entity_attributes = dict(
            _id= asset_id,
            show_name= Envars().show_name,
            entry_name= name,
            type= DbProject().get_branch_type,
            category= Envars().category,
            status= " ",
            assignment= {},
            tasks= get_tasks_config[0],
            sync_tasks= DbSyncTasks().create_from_template(),
            master_bundle=dict(main_stream=[]),
            active= True,
            definition= DbDefaults().get_show_defaults(DbDefaults().root_definitions),
            date= DateTime().return_date,
            time= DateTime().return_time,
            owner= Users.get_current_user()

        )

        try:
            collection.insert_one(entity_attributes)

            insert_entry = DbPaths.origin_path("structure", Envars().branch_name, Envars().category)
            print (insert_entry)
            DbReferences.add_db_id_reference("show", root_id, insert_entry, asset_id, DbProject().get_branch_type)
            print("{} Origin Asset created!".format(name))

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def get_definition(self):
        try:
            cursor = self.db[DbProject().get_branch_type]
            definitions_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, 'definition': 1})
            for definitions in definitions_list:
                return definitions['definition']
        except:
            pass

    def get_entry_type(self):
        try:
            cursor = self.db[DbProject().get_branch_type]
            definitions_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, 'type': 1})
            for definitions in definitions_list:
                return definitions['type']
        except:
            pass

    def get_assignment(self):
        try:
            cursor = self.db[DbProject().get_branch_type]
            definitions_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, 'assignment': 1})
            for definitions in definitions_list:
                return definitions['assignment']
        except:
            pass

    def set_active(self, is_active=True):
        cursor = self.db[DbProject().get_branch_type]
        cursor.update_one({"_id": DbIds.db_entry_id()},{"$set": {"active": is_active}})
        print("{0} active Status set to {1}!".format(DbIds.db_entry_id(), is_active))

    def set_definition(self, definition):
        cursor = self.db[DbProject().get_branch_type]
        cursor.update({"_id": DbIds.db_entry_id()}, {"$set": {"definition": definition}})
        print("{} Definition Updated!".format(Envars.entry_name))

    def remove(self, show_name, branch_category, entry_category, entry_name):
        #TODO: refactor code to use fully the Envars
        try:
            entry_path = "structure" + "." + branch_category + "." + entry_category + "." + entry_name
            self.db.show.update({"show_name": show_name}, {"$unset": {entry_path: 1}})

            # remove entry from its collection
            cursor = self.db[DbProject().get_branch_type]
            cursor.remove({"_id": DbIds.db_entry_id()})
            print('entry {} deleted from {} collection and removed from {} show structure'.format(entry_name,
                                                                                                  branch_category,
                                                                                                  show_name))

        except:
            pass



if __name__ == '__main__':
    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    # Envars.category = "some_category"

    asset = DbAsset()
    asset.create(name="bruce")