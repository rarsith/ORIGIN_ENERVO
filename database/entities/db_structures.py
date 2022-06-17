from envars.envars import Envars
from database import db_templates
from database.db_components import DbPath, DbId
from database import db_connection as mdbconn


class DbProjectBranch(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def add_branch(self, name, branch_type):
        root_id = DbId().curr_project_id()
        insert_entry = "structure" + "." + name
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_entry: {"type": branch_type}}})
        print("{} Origin Branch created!".format(name))
        return name

    def get_branches(self):
        show_structure = self.get_structure()
        return list(show_structure.keys())

    def get_structure(self):
        try:
            all_assets = self.db.show.find({"_id": DbId.curr_project_id(), "active": True},
                                           {'_id': 0, 'structure': 1})
            for each in list(all_assets):
                return each['structure']
        except:
            pass

    @property
    def get_branch_type(self):
        branch_name = Envars.branch_name
        try:
            show_structure = self.db.show.find({"_id": DbId.curr_project_id()},
                                               {'_id': 0, 'structure': 1})
            for each in list(show_structure):
                return each['structure'][branch_name]["type"]
        except:
            pass


class DbAssetCategories(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def add_category(self, name, tasks_type):
        root_id = DbId().curr_project_id()

        insert_entry = DbPath.make_path("structure", Envars.branch_name, name)
        insert_tasks_definition = DbPath.make_path("show_defaults", (name + "_tasks"))
        insert_definition = DbPath.make_path("show_defaults", (name + "_definition"))

        self.db.show.update_one({"_id": root_id}, {"$set": {insert_entry: []}})
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_tasks_definition: db_templates.tasks_schema(tasks_type)}})
        self.db.show.update_one({"_id": root_id}, {"$set": {insert_definition: db_templates.entry_definition(tasks_type)}})

        print("{} Origin Category created!".format(name))
        return name

    def get_categories(self):
        branch = Envars().branch_name
        show_structure = DbProjectBranch().get_structure()
        full_list = list(show_structure[branch])
        full_list.remove("type")
        return full_list


if __name__ == '__main__':
    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "hulk"
    Envars.task_name = "surfacing"

    cc = DbProjectBranch().get_branch_type
    print (cc)