from database import db_connection as mdbconn
from database.entities.db_project import DbProject

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

class Combiner(object):
    def __copy__(self):
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
        cursor = self.db[DbProject().get_branch_type]
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

