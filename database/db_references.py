from database import db_connection as mdbconn
from database.utils.db_ref import DbRef

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