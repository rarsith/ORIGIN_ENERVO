from envars.envars import Envars

class DbPaths(object):

    @classmethod
    def origin_path(cls, *data):
        id_elements = list()
        for elem in data:
            id_elements.append(elem)
        return str(".".join(id_elements))

    @classmethod
    def db_branch_path(cls):
        return cls.origin_path(Envars.show_name,
                               Envars.branch_name
                               )

    @classmethod
    def db_category_path(cls):
        return cls.origin_path(Envars.show_name,
                               Envars.branch_name,
                               Envars.category
                               )

    @classmethod
    def db_entry_path(cls):
        return cls.origin_path(Envars.show_name,
                               Envars.branch_name,
                               Envars.category,
                               Envars.entry_name)

    @classmethod
    def db_task_path(cls):
        return "tasks"

    @classmethod
    def db_sync_task_path(cls):
        return "sync_tasks"

    @classmethod
    def db_task_imp_from(cls):
        return cls.origin_path("tasks", Envars.task_name, 'imports_from')

    @classmethod
    def db_task_pub(cls):
        return cls.origin_path("tasks", Envars.task_name, 'pub_slots')

    @classmethod
    def db_sync_slot_path(cls):
        return cls.origin_path("sync_tasks", Envars.task_name)

    @classmethod
    def db_task_pub_used_by(cls):
        return cls.origin_path("tasks", Envars.task_name, 'pub_slots')

    @classmethod
    def db_asset_definition_path(cls):
        return "definition"

    @classmethod
    def db_asset_master_bundle_path(cls):
        return "master_bundle"

    @classmethod
    def db_asset_assignment_path(cls):
        return "assignment"

if __name__ == '__main__':
    Envars.show_name="Test"
    Envars.branch_name="momo"
    Envars.category="bubu"
    Envars.entry_name="koko"
    Envars.task_name="modeling"


    pp = DbPaths()
    pp_path = pp.db_task_pub()
    print (pp_path)