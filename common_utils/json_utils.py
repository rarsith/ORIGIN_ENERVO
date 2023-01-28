import os
import json


def open_json(source_file):
    with open(source_file, 'r') as json_read:
        read_buffer = json.load(json_read)
    return read_buffer

def write_json(target_path, target_file, data, file_extension=".json"):
    json_object = json.dumps(data, indent=4)

    if not os.path.exists(target_path):
        try:
            os.makedirs(target_path)
        except Exception as e:
            print(e)
            raise
    with open(os.path.join(target_path, target_file+file_extension), 'w') as outfile:
        outfile.write(json_object)

def read_dictionary(source_data, attribute_to_read):
    return source_data[attribute_to_read]

if __name__=="__main__":
    json_load = open_json("../database/defaults/tasks_default_schemas.json")
    tasks_read = read_dictionary(json_load, 'prop')
    print (tasks_read)


