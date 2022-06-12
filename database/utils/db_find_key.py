from database import db_connection as mdbconn

def db_find_key(db_collection, item_to_search, **kwargs):
    """
    will find all the key values from a collection and returns them as a dictionary
    """
    items = []
    db = mdbconn.server[mdbconn.database_name]
    cursor = db[db_collection]
    results = cursor.find(kwargs, {"_id": 0, item_to_search: 1})
    for result in results:
        for k, v in result.items():
            items.append(v)

    return items