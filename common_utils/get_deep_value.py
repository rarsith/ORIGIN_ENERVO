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