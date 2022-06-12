from envars.envars import Envars

class DbIds(object):
    """
    Takes a list and joins the elements into a string
    Ex: list = ["element1", "element2"] >>>> result > "element1.element2"
    To be used for generating ids for entities at creation time
    """

    @classmethod
    def create_id(cls, *data):
        id_elements = list()
        for elem in data:
            id_elements.append(elem)
        return str(".".join(id_elements))

    @classmethod
    def db_show_id(cls):
        return cls.create_id("root", Envars.show_name)

    @classmethod
    def db_entry_id(cls):
        return cls.create_id(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name)

    @classmethod
    def db_wip_file_id(cls, version):
        return cls.create_id(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             Envars.task_name,
                             "wip",
                             version)

    @classmethod
    def db_main_pub_id(cls, version):
        return cls.create_id("main_pub",
                             Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             Envars.task_name,
                             version)

    @classmethod
    def db_slot_pub_id(cls, pub_slot,version):
        return cls.create_id("slot_pub",
                             pub_slot,
                             Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             Envars.task_name,
                             version)

    @classmethod
    def db_master_bundle_id(cls, version):
        return cls.create_id("bundle",
                             Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             version)

    @classmethod
    def db_sync_tasks_id(cls, version):
        return cls.create_id("sync_tasks",
                             Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             version)
