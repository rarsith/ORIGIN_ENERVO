from database import db_connection as mdbconn
from database.entities.db_project import DbProject


class DbUpdate(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def origin_update(self, entity_id, db_path, data=[]):
        cursor = self.db[DbProject().get_branch_type]
        cursor.update_one({"_id": entity_id}, {"$set": {db_path: data}})
