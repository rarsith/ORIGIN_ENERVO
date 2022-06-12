import json


def open_json(source_file):
    with open(source_file, 'r') as json_read:
        read_buffer = json.load(json_read)
    return read_buffer


def read_dictionary(source_data, attribute_to_read):
    return source_data[attribute_to_read]

if __name__=="__main__":
    import pprint
    json_load = open_json("../database/defaults/tasks_schemas.json")
    tasks_read = read_dictionary(json_load, 'prop')
    print (tasks_read)

    # gog = tasks_read["task"]

    # pprint.pprint(gog)


