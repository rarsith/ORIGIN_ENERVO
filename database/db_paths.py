from envars.envars import Envars
from database.db_collections import DbCollections

class DbPaths(object):

    @classmethod
    def make_path(cls, *data, **kwargs):
        if data:
            id_elements = list()
            for elem in data:
                id_elements.append(elem)
            dotted_path = str(".".join(id_elements))
            return dotted_path
        return kwargs


    @classmethod
    def path_root(cls, dict_packed=False):
        if dict_packed:
            return cls.make_path(show_name=Envars.show_name,
                                 branch_name=Envars.branch_name,
                                 category=Envars.category,
                                 entry_name=Envars.entry_name)

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name)

    @classmethod
    def path_root_full(cls, dict_packed=False):
        if dict_packed:
            return cls.make_path(show_name=Envars.show_name,
                                 branch_name=Envars.branch_name,
                                 category=Envars.category,
                                 entry_name=Envars.entry_name,
                                 task_name=Envars.task_name)

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             Envars.task_name
                             )


    @classmethod
    def path_to_branch(cls, dict_packed=False):
        if dict_packed:
            return cls.make_path(show_name=Envars.show_name,
                                 branch_name=Envars.branch_name)

        return cls.make_path(Envars.show_name,
                             Envars.branch_name
                             )

    @classmethod
    def path_to_category(cls, dict_packed=False):
        if dict_packed:
            return cls.make_path(show_name=Envars.show_name,
                                 branch_name=Envars.branch_name,
                                 category=Envars.category)

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category
                             )

    @classmethod
    def path_to_entry(cls, dict_packed=False):
        if dict_packed:
            return cls.make_path(show_name = Envars.show_name,
                                 branch_name = Envars.branch_name,
                                 category = Envars.category,
                                 entry_name = Envars.entry_name)

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name)

    @classmethod
    def path_to_task(cls, relative=True):
        if relative:
            return cls.make_path("tasks", Envars.task_name)

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                               "tasks",
                             Envars.task_name)

    @classmethod
    def path_to_sync_tasks(cls, relative=True):
        if relative:
            return "sync_tasks"

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                               "sync_tasks")

    @classmethod
    def path_to_task_imports_from(cls, relative=True):
        if relative:
            return cls.make_path("tasks", Envars.task_name, "imports_from")

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                               "tasks",
                             Envars.task_name,
                               "imports_from"
                             )

    @classmethod
    def path_to_task_pub_slots(cls, relative=True):
        if relative:
            return cls.make_path("tasks", Envars.task_name, 'pub_slots')

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                               "tasks",
                             Envars.task_name,
                               "pub_slots"
                             )

    @classmethod
    def path_to_sync_task_slot(cls, relative=True):
        if relative:
            return cls.make_path("sync_tasks", Envars.task_name)

        return cls.make_path(Envars.show_name,
                             Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                               "sync_tasks",
                             Envars.task_name,
                             )

    @classmethod
    def path_to_pub_slot_used_by(cls, pub_slot, relative=True):
        if relative:
            return cls.make_path("tasks", Envars.task_name, 'pub_slots', pub_slot, "used_by")

        return cls.make_path(Envars.show_name,
                             Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                               "tasks",
                             Envars.task_name,
                               "pub_slots",
                             pub_slot,
                               "used_by"
                             )

    @classmethod
    def path_to_entry_definition(cls, relative=True):
        if relative:
            return "definition"
        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                               "definition"
                             )

    @classmethod
    def path_to_master_bundle(cls, relative=True):
        if relative:
            return "master_bundle"

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                               "master_bundle"
                             )

    @classmethod
    def path_to_entry_assignment(cls, relative=True):
        if relative:
            return "assignment"

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                           "assignment"
                             )


if __name__ == '__main__':
    Envars.show_name="Test"
    Envars.branch_name="assets"
    Envars.category="characters"
    Envars.entry_name="hulk"
    Envars.task_name="modeling"

    import pprint
    from database.utils.db_find_key import db_find
    from database.db_types import Entity

    pp = DbPaths()
    pp_path = pp.path_root(dict_packed=True)
    # get_pub_slots = db_find(Entity.build(), pp.path_to_task_pub_slots(), **pp_path)
    # print (get_pub_slots[0]["modeling"])

    # for slot in get_pub_slots_list:
    #     x = fkey(Entity.build(), pp.path_to_pub_slot_used_by(slot), **pp_path)
    #     pprint.pprint (x[0])


    # pp_path = pp.db_task_pub(relative=False, dict_packed=True)
    # print (pp_path)
    asset_id = DbPaths.path_to_entry()
    xxx = pp.path_to_entry(dict_packed=False)
    print (asset_id)
