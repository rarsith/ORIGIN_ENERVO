from database import db_templates
from database.db_types import BranchTypes, TaskTypes
from database.utils.db_q_entity import From, QEntity
from database.db_attributes import DbEntitiesId, DbProjectAttributes


class DbProjectBranch(object):

    @staticmethod
    def add_branch(name: str, branch_type: BranchTypes) -> str:

        QEntity(From().projects,
                DbEntitiesId.curr_project_id(),
                DbProjectAttributes.structure()
                ).add_property(name=name,
                               add_data=dict({"type": branch_type}))

        print("{} Origin Branch created!".format(name))
        return name

    @staticmethod
    def get_branches():
        branches = QEntity(From().projects,
                           DbEntitiesId.curr_project_id(),
                           DbProjectAttributes.branches()
                           ).get(attrib_names=True)
        return branches

    @staticmethod
    def get_structure():
        try:
            structure = QEntity(From().projects,
                                DbEntitiesId.curr_project_id(),
                                DbProjectAttributes.structure()
                                ).get(attrib_values=True)
            return structure

        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    @property
    def get_type(self):
        branch_type = From().entities
        return branch_type


class DbAssetCategories(object):

    @staticmethod
    def add_category(name: str, tasks_type: TaskTypes) -> str:
        category_tasks_type = name + "_tasks"
        category_definition = name + "_definition"

        QEntity(From().projects,
                DbEntitiesId.curr_project_id(),
                DbProjectAttributes.curr_branch()
                ).add_property(name=name)

        QEntity(From().projects,
                DbEntitiesId.curr_project_id(),
                DbProjectAttributes.show_defaults()
                ).add_property(name=category_tasks_type,
                               add_data=db_templates.tasks_schema(tasks_type))

        QEntity(From().projects,
                DbEntitiesId.curr_project_id(),
                DbProjectAttributes.show_defaults()
                ).add_property(name=category_definition,
                               add_data=db_templates.entry_definition(tasks_type))

        print("{} Origin Category created!".format(name))
        return name

    @staticmethod
    def get_categories():
        categories = QEntity(From().projects,
                             DbEntitiesId.curr_project_id(),
                             DbProjectAttributes.categories()
                             ).get(attrib_names=True)
        categories.remove("type")
        return categories



if __name__ == '__main__':
    from envars.envars import Envars

    Envars.show_name = "Cicles"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "hulk"
    Envars.task_name = "surfacing"

    cc = DbProjectBranch().add_branch("super_b", BranchTypes.build())

