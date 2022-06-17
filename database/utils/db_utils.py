from database import db_connection as mdbconn
from database.entities.db_structures import DbProjectBranch


class DbUpdate(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def origin_update(self, entity_id, db_path, data=[]):
        cursor = self.db[DbProjectBranch().get_branch_type]
        cursor.update_one({"_id": entity_id}, {"$set": {db_path: data}})


class DbRef(object):
    def __init__(self, collection="", entity_id=""):
        self.collection = collection
        self.entity_id = entity_id
        self.db = mdbconn.server[mdbconn.database_name]


    @property
    def odbref(self):
        id_list = [self.collection, self.entity_id]
        gen_id = ",".join(id_list)
        return str(gen_id)


    def oderef(self, ref_string, get_field=None):
        extr_collection, extr_entity_id = ref_string.split(",")
        if not get_field:
            return extr_collection, extr_entity_id
        elif get_field:
            cursor = self.db[extr_collection]
            db_field = cursor.find_one({"_id":extr_entity_id})
            return db_field[get_field]


class DbReferences(object):
    @classmethod
    def add_db_id_reference(cls, collection, parent_doc_id, destination_slot, id_to_add, from_collection, replace=False):
        db = mdbconn.server[mdbconn.database_name]
        if not replace:
            db[collection].update_one({"_id": parent_doc_id},
                                      {"$push": {destination_slot: DbRef(from_collection, id_to_add).db_ref}})
        else:
            db[collection].update_one({"_id": parent_doc_id},
                                      {"$set": {destination_slot: DbRef(from_collection, id_to_add).db_ref}})


class DBVersionControl(object):

    def db_main_pub_ver_increase(self):
        get_versions = db_find_key.db_find(db_collection=DbCollections.main_publishes(),
                                           item_to_search="version",
                                           **DbPath.to_base(dict_packed=True)
                                           )
        new_version = version_up.version_increment(get_versions)
        return new_version

    def db_pubslot_ver_increase(self, collection_name, slot_name):
        get_versions = db_find_key.db_find(collection_name,
                                           item_to_search="version",
                                           **DbPath.to_base(dict_packed=True),
                                           slot_name=slot_name
                                           )

        new_version = version_up.version_increment(get_versions)
        return new_version

    def db_master_bundle_ver_increase(self):

        get_versions = db_find_key.db_find(db_collection=DbCollections.bundles(),
                                           item_to_search="version",
                                           **DbPath.to_entry(dict_packed=True)
                                           )

        new_version = version_up.version_increment(get_versions)
        return new_version

    def db_sync_tasks_ver_increase(self):

        get_versions = db_find_key.db_find(db_collection=DbCollections.sync_tasks(),
                                           item_to_search="version",
                                           **DbPath.to_entry(dict_packed=True)
                                           )

        new_version = version_up.version_increment(get_versions)
        return new_version

    def db_wip_files_version_increase(self, collection_name):

        get_versions = db_find_key.db_find(db_collection=collection_name,
                                           item_to_search="version",
                                           show_name=Envars.show_name,
                                           branch_name=Envars.branch_name,
                                           category=Envars.category,
                                           entry_name=Envars.entry_name,
                                           task_name=Envars.task_name
                                           )
        new_version = version_up.version_increment(get_versions)
        return new_version


class Combiner(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def db_find_key(self, db_collection, item_to_search, **kwargs):
        """
        will find all the key values from a collection and returns them as a dictionary
        """
        items = []

        cursor = self.db[db_collection]
        results = cursor.find(kwargs, {"_id": 0, item_to_search: 1})
        for result in results:
            for k, v in result.items():
                items.append(v)
        return items


    def origin_update(self, entity_id, db_path, data=[]):
        cursor = self.db[DbProjectBranch().get_branch_type]
        cursor.update_one({"_id": entity_id}, {"$set": {db_path: data}})


    @classmethod
    def combine(cls, *data, **kwargs):
        if data:
            id_elements = list()
            for elem in data:
                id_elements.append(elem)
            dotted_path = str(".".join(id_elements))
            return dotted_path
        return kwargs


class DbFindKey(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]


    def db_find(self, db_collection, item_to_search, **kwargs) -> list:
        """
        will find all the key values from a collection and returns them as a dictionary
        """
        items = []
        cursor = self.db[db_collection]
        results = cursor.find(kwargs, {"_id": 0, item_to_search: 1})
        for result in results:
            for k, v in result.items():
                items.append(v)

        return items

    def db_find_kk(self, db_collection, item_to_search, **kwargs) -> list:
        """
        will find all the key values from a collection and returns them as a dictionary
        """
        cursor = self.db[db_collection]
        results = cursor.find(kwargs, {"_id": 0, item_to_search: 1})
        for result in results:
            return result