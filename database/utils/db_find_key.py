from database import db_connection as mdbconn


def db_find(db_collection, item_to_search, **kwargs) -> list:
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

def db_find_kk(db_collection, item_to_search, **kwargs) -> list:
    """
    will find all the key values from a collection and returns them as a dictionary
    """
    db = mdbconn.server[mdbconn.database_name]
    cursor = db[db_collection]
    results = cursor.find(kwargs, {"_id": 0, item_to_search: 1})
    for result in results:
        return result





if __name__ == '__main__':

    def string_to_list(data, splitter="."):
        """ @data: takes in string with OR without a separator (".", "_"...)
            @splitter: default splitter used
            @returns: if multiple resulting splits -> a list,
                      else-> the initial @data value """

        if not splitter in data:
            return data
        get_path_entities = data.split(splitter)
        return get_path_entities


    def get_deep_value(data: dict, path_list: list) -> dict:
        """ @data: takes a nested dictionary
            @path_list: takes a list or a single string
            @returns: the value that is corresponding to the last list element in the path_list"""

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
                    return get_deep_value(level, path_list)




    pp = {'show_name': 'Test', 'branch_name': 'assets', 'category': 'characters', 'entry_name': 'noir'}

    path_to_search = "tasks.surfacing.imports_from"

    cc = db_find_kk("build", path_to_search, **pp)

    get_list = string_to_list(data=path_to_search)
    nn = get_deep_value(data=cc, path_list=get_list)

    print("RESULT OUTSIDE",nn)

