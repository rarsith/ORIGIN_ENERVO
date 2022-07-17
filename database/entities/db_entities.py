from envars.envars import Envars
from database import db_connection as mdbconn
from database.utils.db_utils import DbRef, DbReferences
from database.utils.db_q_entity import From, QEntity
from database.entities.db_structures import DbProjectBranch, DbAssetCategories
from database.entities.db_constructors import DbConstructors
from database.db_attributes import DbEntitiesAttrPaths, DbEntitiesId, DbProjectAttributes, DbEntityAttributes


class DbProject(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self, name):
        entity_id = DbEntitiesId.create_id("root", name)
        created_id, save_data = DbConstructors().project_construct(name=name, entity_id=entity_id)

        try:
            self.db.show.insert_one(save_data)
            print("{} Project created!".format(name))

        except ValueError as e:
            print("{} Error! Nothing created!".format(e))

    @staticmethod
    def get_entities_names():
        entities_found = list()

        origin_q = QEntity(From().projects,
                           DbEntitiesId.curr_project_id(),
                           DbProjectAttributes.category_entries()
                           ).get(attrib_names=True)

        for entity in origin_q:
            name = DbRef().oderef(ref_string=entity, get_field="entry_name")
            entities_found.append(name)

        return entities_found

    @staticmethod
    def get_type():
        try:
            show_type = QEntity(From().projects,
                                DbEntitiesId.curr_project_id(),
                                DbProjectAttributes.type()
                                ).get(attrib_names=True)
            return show_type
        except ValueError as val:
            print ("{} Nothing Done!".format(val))

    @staticmethod
    def is_active():
        try:
            is_active = QEntity(From().projects,
                                DbEntitiesId.curr_project_id(),
                                DbProjectAttributes.is_active()
                                ).get(attrib_names=True)
            return is_active
        except ValueError as val:
            print ("{} Nothing Done!".format(val))


class DbAsset(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self, name):
        collection = self.db[From().entities]
        created_id, save_data = DbConstructors().asset_construct(name=name,
                                                                 entity_id=DbEntitiesId.create_entity_id(name))

        try:
            collection.insert_one(save_data)

            insert_entry = DbEntitiesAttrPaths.make_path("structure",
                                                         Envars().branch_name,
                                                         Envars().category)

            DbReferences.add_db_id_reference("show",
                                             DbEntitiesId.curr_project_id(),
                                             insert_entry,
                                             created_id,
                                             DbProjectBranch().get_type)

            print("{} Origin Asset created!".format(name))

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    @staticmethod
    def get_definition():
        try:
            result = QEntity(From().entities,
                             DbEntitiesId.curr_entry_id(),
                             DbEntityAttributes.definition()
                             ).get(attrib_names=True)
            return result
        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    @staticmethod
    def get_entry_type():
        try:
            result = QEntity(From().entities,
                             DbEntitiesId.curr_entry_id(),
                             DbEntityAttributes.type()
                             ).get(attrib_names=True)
            return result
        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    @staticmethod
    def get_assignment():
        try:
            result = QEntity(From().entities,
                             DbEntitiesId.curr_entry_id(),
                             DbEntityAttributes.assignments()
                             ).get(attrib_names=True)
            return result
        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    @staticmethod
    def set_active(is_active=True):
        QEntity(From().entities,
                DbEntitiesId.curr_entry_id(),
                DbEntityAttributes.is_active()
                ).update(is_active)

        print("{0} active Status set to {1}!".format(DbEntitiesId.curr_entry_id(), is_active))

    @staticmethod
    def set_definition(data):
        QEntity(From().entities,
                DbEntitiesId.curr_entry_id(),
                DbEntityAttributes.definition
                ).update(data)
        print("{} Definition Updated!".format(Envars.entry_name))

    def remove(self):
        #TODO: refactor code to use fully the Envars
        try:
            QEntity(From().projects,
                    DbEntitiesId.curr_project_id(),
                    DbProjectAttributes.entry()
                    ).remove()

            QEntity(From().entities,
                    DbEntitiesId.curr_entry_id(),
                    DbEntityAttributes.type()
                    ).remove()

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
            asset_id = DbEntitiesId.curr_entry_id()
            cursor = self.db[DbProjectBranch().get_type]
            db_path = DbEntitiesAttrPaths.make_path(DbEntitiesAttrPaths.to_master_bundle(),
                                                    (name + "_" + "stream"))

            cursor.update_one({"_id": asset_id}, {"$set": {db_path:[]}})
            print("{} Bundle Stream  created!".format(name))
            return name

        except ValueError as e:
            print("{} Error! Nothing Created!".format(e))

    @staticmethod
    def add_to_bundle(entity_id, bundle_id, slot):
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

    @staticmethod
    def set_as_current(bundle_id, add_to_stream="main_stream"):

        DbReferences.add_db_id_reference(DbProjectBranch().get_type,
                                         DbEntitiesId.curr_entry_id(),
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
            task_path = DbEntitiesAttrPaths.to_pub_slots()
            print(task_path)
            cursor = self.db[DbProjectBranch().get_type]
            cursor.update_one({"_id": DbEntitiesId.curr_entry_id()}, {"$unset": {task_path: 1}})
            cursor.update_one({"_id": DbEntitiesId.curr_entry_id()}, {"$set": {task_path: {}}})
        except:
            pass


if __name__ == '__main__':
    from database.entities.db_structures import DbAssetCategories
    from database.db_types import TaskTypes

    Envars.show_name = "Cicles"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "circle"
    Envars.task_name = "rigging"

    definition ={"crap":"mofo"}


    xx = DbAsset().remove()
    print (xx)