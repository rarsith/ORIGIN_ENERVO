from envars.envars import Envars
from database.origin import Origin, From
from database import db_connection as mdbconn
from database.utils.db_utils import DbRef, DbReferences
from database.entities.db_structures import DbProjectBranch
from database.entities.db_constructors import DbConstructors
from database.db_components import DbPath, DbId, DbProjectAttributes, DbEntityAttributes


class DbProject(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self, name):
        entity_id = DbId.create_id("root", name)
        created_id, save_data = DbConstructors().project_construct(name=name, entity_id=entity_id)

        try:
            self.db.show.insert_one(save_data)
            print("{} Project created!".format(name))

        except ValueError as e:
            print("{} Error! Nothing created!".format(e))

    def get_entities_names(self):
        entities_found = list()
        origin_q = Origin(From().project, DbId.curr_project_id(), DbProjectAttributes.entries()).get(attrib_names=True)
        for entity in origin_q:
            name = DbRef().oderef(ref_string=entity, get_field="entry_name")
            entities_found.append(name)
        return entities_found

    def get_type(self):
        try:
            show_type = Origin(From().project, DbId.curr_project_id(), DbProjectAttributes.type()).get(attrib_names=True)
            return show_type
        except ValueError as val:
            print ("{} Nothing Done!".format(val))

    def is_active(self):
        try:
            is_active = Origin(From().project, DbId.curr_project_id(), DbProjectAttributes.type()).get(attrib_names=True)
            return is_active
        except ValueError as val:
            print ("{} Nothing Done!".format(val))


class DbAsset(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self, name):
        collection = self.db[From().entities]
        entity_id = DbId.create_id(DbPath.to_category(), name)

        created_id, save_data = DbConstructors().asset_construct(name=name, entity_id=entity_id)

        try:
            collection.insert_one(save_data)
            insert_entry = DbPath.make_path("structure",
                                            Envars().branch_name,
                                            Envars().category)

            DbReferences.add_db_id_reference("show",
                                             DbId.curr_project_id(),
                                             insert_entry,
                                             created_id,
                                             DbProjectBranch().get_type)

            print("{} Origin Asset created!".format(name))

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def get_definition(self):
        try:
            result = Origin(From().entities, DbId.curr_entry_id(), DbEntityAttributes.definition()).get(attrib_names=True)
            return result
        except ValueError as val:
            raise("{} Error! Nothing created!".format(val))

    def get_entry_type(self):
        try:
            result = Origin(From().entities, DbId.curr_entry_id(), DbEntityAttributes.type()).get(attrib_names=True)
            return result
        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    def get_assignment(self):
        try:
            result = Origin(From().entities, DbId.curr_entry_id(), DbEntityAttributes.assignments()).get(attrib_names=True)
            return result
        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    def set_active(self, is_active=True):
        cursor = self.db[DbProjectBranch().get_type]
        cursor.update_one({"_id": DbId.curr_entry_id()}, {"$set": {"active": is_active}})
        print("{0} active Status set to {1}!".format(DbId.curr_entry_id(), is_active))

    def set_definition(self, definition):
        cursor = self.db[DbProjectBranch().get_type]
        cursor.update({"_id": DbId.curr_entry_id()}, {"$set": {"definition": definition}})
        print("{} Definition Updated!".format(Envars.entry_name))

    def remove(self, show_name, branch_category, entry_category, entry_name):
        #TODO: refactor code to use fully the Envars
        try:
            entry_path = "structure" + "." + branch_category + "." + entry_category + "." + entry_name
            self.db.show.update({"show_name": show_name}, {"$unset": {entry_path: 1}})

            # remove entry from its collection
            cursor = self.db[DbProjectBranch().get_type]
            cursor.remove({"_id": DbId.curr_entry_id()})
            print('entry {} deleted from {} collection and removed from {} show structure'.format(entry_name,
                                                                                                  branch_category,
                                                                                                  show_name))
        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))


class DbBundle(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self):
        inserted_id, save_content = DbConstructors().bundle_construct()
        master_bundle = self.db.bundles.insert_one(save_content)
        print("{0}, has been published".format(inserted_id))
        return master_bundle.inserted_id

    def create_stream(self, name):
        try:
            asset_id = DbId.curr_entry_id()
            cursor = self.db[DbProjectBranch().get_type]
            db_path = DbPath.make_path(DbPath.to_master_bundle(), (name + "_" + "stream"))

            cursor.update_one({"_id": asset_id}, {"$set": {db_path:[]}})
            print("{} Bundle Stream  created!".format(name))
            return name

        except ValueError as e:
            print("{} Error! Nothing Created!".format(e))

    def add_to_bundle(self, entity_id, bundle_id, slot):
        DbReferences.add_db_id_reference("bundles",
                                         bundle_id,
                                        "master_bundle.{}".format(slot),
                                         entity_id,
                                         DbProjectBranch().get_type,
                                         replace=True)
        return bundle_id

    def add_slot(self, name):
        pass

    def rem_slot(self, name):
        pass

    def update_slot(self, name):
        pass

    def update_master(self):
        pass

    def set_as_current(self, bundle_id, add_to_stream="main_stream"):
        DbReferences.add_db_id_reference(DbProjectBranch().get_type,
                                         DbId.curr_entry_id(),
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
        #TODO: finish the method
        try:
            task_path = DbPath.to_pub_slots()
            print(task_path)
            cursor = self.db[DbProjectBranch().get_type]
            cursor.update_one({"_id": DbId.curr_entry_id()}, {"$unset": {task_path: 1}})
            cursor.update_one({"_id": DbId.curr_entry_id()}, {"$set": {task_path: {}}})
        except:
            pass


if __name__ == '__main__':
    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "red_hulk"
    Envars.task_name = "rigging"

    xx = DbAsset().get_assignment()
    print (xx)