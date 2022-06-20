from envars.envars import Envars
from database import db_templates
from database.origin import From, Origin
from database.db_components import DbPath, DbId, DbProjectAttributes
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
        branches = Origin(From().project, DbId.curr_project_id(), DbProjectAttributes.branches()).get(attrib_names=True)
        return branches

    def get_structure(self):
        try:
            structure = Origin(From().project, DbId.curr_project_id(), DbProjectAttributes.structure()).get(attrib_values=True)
            return structure

        except ValueError as val:
            raise("{} Error! Nothing created!".format(val))

    @property
    def get_type(self):
        branch_type = From().entities
        return branch_type


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
        categories = Origin(From().project, DbId.curr_project_id(), DbProjectAttributes.categories()).get(attrib_names=True)
        categories.remove("type")
        return categories



if __name__ == '__main__':
    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "hulk"
    Envars.task_name = "surfacing"

    cc = DbAssetCategories().get_categories()
    print (cc)

