from common_utils import read_json

def show_structure():
    json_load = read_json.open_json("../../database/defaults/show_structure.json")
    structure_read = read_json.read_dictionary(json_load, 'structure')
    return structure_read

def task_defaults():
    json_load = read_json.open_json("../../database/templates/task_template.json")
    tasks_read = read_json.read_dictionary(json_load, 'root')
    return tasks_read["task"]

def tasks_schema(category):
    json_load = read_json.open_json("../../database/defaults/tasks_schemas.json")
    tasks_read = read_json.read_dictionary(json_load, category)
    return tasks_read["tasks"]

def tasks_pub_slot_schema():
    json_load = read_json.open_json("../../database/defaults/tasks_pub_slot_schemas.json")
    tasks_read = read_json.read_dictionary(json_load, "pub_slot")
    return tasks_read

def entry_definition(category):
    json_load = read_json.open_json("../../database/defaults/entries_definition.json")
    tasks_read = read_json.read_dictionary(json_load, category)
    return tasks_read["definition"]


if __name__=="__main__":
    import pprint

    tt = show_structure()
    tt = task_defaults()
    tt = tasks_schema(category="prop")
    pprint.pprint (tt)