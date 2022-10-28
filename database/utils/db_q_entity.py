from envars.envars import Envars
from database import db_connection as mdbconn
from database.entities.db_attributes import (DbProjectAttrPaths,
                                             DbEntityAttrPaths,
                                             DbTaskAttrPaths,
                                             DbPubSlotsAttrPaths,
                                             DbMainPubAttrPaths,
                                             DbBundleAttrPaths)
from database.db_ids import DbIds


class From:

    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def branch_type(self):
        branch_name = Envars.branch_name
        try:
            cursor = self.db.show.find({"_id": DbIds.curr_project_id()},
                                       {'_id': 0, DbProjectAttrPaths.structure(): 1})
            for each in list(cursor):
                return each['structure'][branch_name]["type"]

        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    @property
    def projects(self):
        return "show"

    @property
    def builds(cls):
        return "build"

    @property
    def shots(self):
        return "sequences"

    @property
    def entities(self):
        return self.branch_type()

    @property
    def publishes(self):
        return "publishes"

    @property
    def bundles(self):
        return "bundles"

    @property
    def sync_tasks(self):
        return "sync_tasks"

    @property
    def work_files(self):
        return "work_files"


class QEntity:
    def __init__(self, db_collection: From(), entry_id: DbIds(), attribute: (DbProjectAttrPaths,
                                                                             DbEntityAttrPaths,
                                                                             DbTaskAttrPaths,
                                                                             DbPubSlotsAttrPaths,
                                                                             DbMainPubAttrPaths,
                                                                             DbBundleAttrPaths)):
        self.db = mdbconn.server[mdbconn.database_name]
        self.collection = db_collection
        self.attribute = attribute
        self.db_id = entry_id

    def _string_to_list(self, data, splitter="."):
        """ @data: takes in string with OR without a separator (".", "_"...)
            @splitter: default splitter used
            @returns: if multiple resulting splits -> a list,
                      else-> the initial @data value
        """

        if not splitter in data:
            return data
        get_path_entities = data.split(splitter)
        return get_path_entities

    def _get_deep_value(self, data: dict, path_list: list) -> dict:
        """ @data: takes a nested dictionary
            @path_list: takes a list or a single string
            @returns: the value that is corresponding to the last list element in the path_list
        """
        # print(">>>>", data)

        if isinstance(path_list, str):
            result = data.get(path_list)
            return result
        elif isinstance(path_list, list) and len(path_list) == 1:
            result = data.get(path_list[0])
            return result
        else:
            for index, entity in enumerate(path_list):
                if isinstance(path_list, list) and len(path_list) > 1:
                    level = data.get(entity)
                    path_list.pop(index)
                    return self._get_deep_value(level, path_list)

    def _get_values(self, results: dict):
        for result in results:
            get_list = self._string_to_list(self.attribute)
            values = self._get_deep_value(data=result, path_list=get_list)
            return values

    def _get_keys(self, results: dict):
        data = self._get_values(results)
        if isinstance(data, dict):
            return list(data)
        return data

    def db_results(self):
        results = self.db[self.collection].find({"_id": self.db_id}, {"_id": 0, self.attribute: 1})
        return results

    def get(self,
            attrib_names: bool = False,
            attrib_values: bool = False,
            all: bool = False,
            all_active: bool = False):
        """
            will find all the key values from a collection and returns them as a dictionary
        """
        results = self.db[self.collection].find({"_id": self.db_id}, {"_id": 0, self.attribute: 1})

        if attrib_names and attrib_values and all and all_active:
            raise ValueError ("Choose either attrib_names or attrib_values, or leave default!")

        elif attrib_names:
            return self._get_keys(results)

        elif attrib_values:
            return self._get_values(results)

        elif all:
            result = [x[self.attribute] for x in self.db[self.collection].find({}, {"_id": 0, self.attribute: 1})]
            return result

        elif all_active:
            result = [x[self.attribute] for x in self.db[self.collection].find({"active":True}, {"_id": 0, self.attribute: 1})]
            return result

        else:
            for result in results:
                return result

    def get_attr_names(self):
        return self._get_keys(self.db_results())

    def get_attr_values(self):
        return self._get_values(self.db_results())

    def get_all(self):
        result = [x[self.attribute] for x in self.db[self.collection].find({}, {"_id": 0, self.attribute: 1})]
        return result

    def get_all_active(self):
        result = [x[self.attribute] for x in self.db[self.collection].find({"active": True}, {"_id": 0, self.attribute: 1})]
        return result

    def update(self, data):
        self.db[self.collection].update_one({"_id": self.db_id}, {"$set": {self.attribute: data}})
        return data

    def add_property(self, name, add_data=[]):
        insert_path = ".".join([self.attribute, name])
        self.db[self.collection].update_one({"_id": self.db_id}, {"$set": {insert_path:add_data}})
        return insert_path

    def add(self, data):
        if not isinstance(data, list):
            self.db[self.collection].update_one({"_id": self.db_id}, {"$push": {self.attribute: data}})
        else:
            for each in data:
                self.db[self.collection].update_one({"_id": self.db_id}, {"$push": {self.attribute: each}})

    def remove(self):
        #TODO: to clean and delete
        self.db[self.collection].update_one({"_id": self.db_id}, {"$unset": {self.attribute: 1}})
        self.db[self.collection].update_one({"_id": self.db_id}, {"$set": {self.attribute: {}}})

    def remove_value(self, data):
        #TODO: to clean and delete
        self.db[self.collection].update_one({"_id": self.db_id}, {"$pull": {self.attribute: data}})

    def remove_property(self):
        """Removes the entire property with all its content. This action is not recoverable"""
        self.db[self.collection].update_one({"_id": self.db_id}, {"$unset": {self.attribute: 1}})

    def remove_entity(self):
        """Removes a Database Entry from a given Collection. This action is not recoverable"""
        self.db[self.collection].delete_one({"_id": self.db_id})

    def clear(self):
        #TODO:need to find out how to query data filed type (need to get field type and restore with the original type)
        """Removes the full content of an attribute by first removing the full atrribute and then recreating it empty"""
        self.db[self.collection].update_one({"_id": self.db_id}, {"$unset": {self.attribute: 1}})
        self.db[self.collection].update_one({"_id": self.db_id}, {"$set": {self.attribute: {}}})


class DbRef:
    def __init__(self, collection="", entity_id=""):
        self.collection = collection
        self.entity_id = entity_id
        self.db = mdbconn.server[mdbconn.database_name]

    @property
    def db_ref(self):
        gen_id = ",".join([self.collection, self.entity_id])
        return str(gen_id)

    def db_deref(self, ref_string, get_field=None):
        extr_collection, extr_entity_id = ref_string.split(",")
        if not get_field:
            return extr_collection, extr_entity_id
        elif get_field:
            cursor = self.db[extr_collection]
            db_field = cursor.find_one({"_id":extr_entity_id})
            return db_field[get_field]


class DbReferences:
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    @classmethod
    def add_db_id_reference(cls, collection, parent_doc_id, destination_slot, id_to_add, from_collection, replace=False):
        db = mdbconn.server[mdbconn.database_name]
        if not replace:
            db[collection].update_one({"_id": parent_doc_id},
                                      {"$push": {destination_slot: DbRef(from_collection, id_to_add).db_ref}})
        else:
            db[collection].update_one({"_id": parent_doc_id},
                                      {"$set": {destination_slot: DbRef(from_collection, id_to_add).db_ref}})

    def get_db_referenced_attr(self, src_collection, src_id, src_attr, attr_to_find):
        list_attr = list()
        if not src_id or src_id == None:
            return
        else:
            id_list = self.db[src_collection].find_one({"_id": src_id})
            for each_id in id_list[src_attr]:
                attr_data = DbRef().db_deref(each_id, attr_to_find)
                list_attr.append(attr_data)
            return list_attr


#TODO: refactor Origin to From --> create a decoarator to return data from the database
if __name__ == '__main__':

    from database.entities.db_attributes import DbEntityAttrPaths, DbTaskAttrPaths, DbPubSlotsAttrPaths
    from database.entities.db_attributes import DbMainPubAttrPaths

    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "blue_hulk"
    Envars.task_name = "modeling"


    origin = QEntity(db_collection=From().projects, entry_id=DbIds().curr_project_id(), attribute=DbProjectAttrPaths.curr_branch()).get()

    print (origin)
    # print ("FROM ?<<{0}>> database collection,\n SELECT entity with _ID -- {1} -- ,\n use this STRING -- {2} --  to go to tasks and get them.\n\n----RESULT----\n{3} ".format(source ,entity, attr, origin))

    # db = mdbconn.server[mdbconn.database_name]
    # vv = db["show"].find({"active": True, "_id":"root.Test"}, {"_id": 0, "structure.assets": 1})
    # for i in vv:
    #
    #     print (i)

    # result = [x["structure.assets"] for x in db["show"].find({"active": True}, {"_id": 0, "structure.assets": 1})]
    # print(result)
