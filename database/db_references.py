from database import db_connection as mdbconn
from database.utils import db_ref

class DbRef(object):
    def __init__(self):
        self.db = mdbconn.server.xchange

    @classmethod
    def add_db_id_reference(cls, collection, parent_doc_id, destination_slot, id_to_add, from_collection, replace=False):
        db = mdbconn.server.xchange
        if not replace:
            db[collection].update_one({"_id": parent_doc_id},
                                      {"$push": {destination_slot: db_ref.DbRef(from_collection, id_to_add).odbref}})
        else:
            db[collection].update_one({"_id": parent_doc_id},
                                      {"$set": {destination_slot: db_ref.DbRef(from_collection, id_to_add).odbref}})