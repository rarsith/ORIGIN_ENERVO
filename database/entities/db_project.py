from database import db_connection as mdbconn
from database import db_templates
from database.db_ids import DbIds
from database.utils.db_ref import DbRef
from database.db_paths import DbPaths
from envars.envars import Envars
from common_utils.date_time import DateTime
from common_utils.users import Users


class GenerateProjectCode:
    """Generates a unique code for the project"""
    data: str

    def __init__(self, data):
        self.data = data

    def code(self) -> str:
        addition = "this is a code"
        return self.data+"-"+addition


class DbProject(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self, name):
        entity_id = DbIds.create_id("root", name)
        save_data = dict(
            _id= entity_id,
            show_code=GenerateProjectCode(data=name).code(),
            show_name=name,
            structure=db_templates.show_structure(),
            show_defaults= dict(asset_definition=db_templates.entry_definition("build"),
                                shots_definition=db_templates.entry_definition("shot"),
                                characters_tasks=db_templates.tasks_schema("character"),
                                props_tasks=db_templates.tasks_schema("prop"),
                                environments_tasks=db_templates.tasks_schema("environment"),
                                characters_definition=db_templates.entry_definition("build"),
                                props_definition=db_templates.entry_definition("build"),
                                environments_definition=db_templates.entry_definition("build"),
                                shots_tasks=db_templates.tasks_schema("shot")),
            active=True,
            date=DateTime().return_date,
            time=DateTime().return_time,
            owner=Users.get_current_user(),
            show_type="vfx")



        try:
            self.db.show.insert_one(save_data)
            print("{} show created!".format(name))

        except Exception as e:
            print("{} Error! Nothing created!".format(e))

    def add_branch(self, name, branch_type):
        root_id = DbIds().db_show_id()
        insert_entry = "structure" + "." + name
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_entry: {"type": branch_type}}})
        print("{} Origin Branch created!".format(name))
        return name

    def add_category(self, name, tasks_type):
        root_id = DbIds().db_show_id()
        insert_entry = DbPaths.make_path("structure", Envars.branch_name, name)
        insert_tasks_definition = DbPaths.make_path("show_defaults", (name + "_tasks"))
        insert_definition = DbPaths.make_path("show_defaults", (name + "_definition"))
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_entry: []}})
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_tasks_definition: db_templates.tasks_schema(tasks_type)}})
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_definition: db_templates.entry_definition(tasks_type)}})
        print("{} Origin Category created!".format(name))
        return name

    def get_structure(self):
        try:
            all_assets = self.db.show.find({"_id": DbIds.db_show_id(), "active": True},
                                           {'_id': 0, 'structure': 1})
            for each in list(all_assets):
                return each['structure']
        except:
            pass

    def get_branches(self):
        show_structure = self.get_structure()
        return list(show_structure.keys())

    def get_categories(self, branch):
        show_structure = self.get_structure()
        full_list = list(show_structure[branch])
        full_list.remove("type")
        return full_list

    def get_entities_names(self, branch, category):
        entities_found = list()
        show_structure = self.get_structure()
        all_referenced_entities = list(show_structure[branch][category])
        for entity in all_referenced_entities:
            name = DbRef().db_deref(ref_string=entity, get_field="entry_name")
            entities_found.append(name)
        return entities_found

    @property
    def get_branch_type(self):
        branch_name = Envars.branch_name
        try:
            show_structure = self.db.show.find({"_id": DbIds.db_show_id(), "active": True},
                                               {'_id': 0, 'structure': 1})
            for each in list(show_structure):
                return each['structure'][branch_name]["type"]
        except:
            pass

    def get_project_type(self):
        try:
            show_type = self.db.show.find({"_id": DbIds.db_show_id(), "active": True},
                                          {'_id': 0, 'show_type': 1})
            for each in list(show_type):
                return each['show_type']
        except:
            pass

    def get_active(self):
        try:
            shows_list = []
            all_shows = self.db.show.find({"active": True}, {'_id': 0, 'show_name': 1})
            for each in all_shows:
                get_values = list(each.values())
                shows_list.append(get_values[0])
            return shows_list

        except:
            pass

if __name__ == '__main__':



    proj = DbProject()
    proj.create(name="Black")