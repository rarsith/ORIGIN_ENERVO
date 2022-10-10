from envars.envars import Envars


class DbIds:
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
    def create_project_id(cls, name):
        return cls.create_id("root", name)

    @classmethod
    def create_entity_id(cls, name):
        entry_id = cls.create_id(DbEntitiesAttrPaths.to_category(), name)
        return entry_id

    @classmethod
    def create_main_pub_id(cls, version):
        return cls.create_id(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             Envars.task_name,
                             "main_pub",
                             version)

    @classmethod
    def create_pub_slot_id(cls, pub_slot, version):
        return cls.create_id(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             Envars.task_name,
                             pub_slot,
                             version)

    @classmethod
    def create_master_bundle_id(cls, version):
        return cls.create_id(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             "bundle",
                             version)

    @classmethod
    def create_sync_tasks_id(cls, version):
        return cls.create_id(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             "sync_tasks",
                             version)

    @classmethod
    def create_wip_file_id(cls, version):
        return cls.create_id(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             Envars.task_name,
                             "wip",
                             version)

    @classmethod
    def curr_project_id(cls):
        return cls.create_id("root", Envars.show_name)

    @classmethod
    def all_in_collection(cls):
        return {}

    @classmethod
    def curr_entry_id(cls):
        return cls.create_id(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name)

    @classmethod
    def get_wip_file_id(cls, version):
        return cls.create_id(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             Envars.task_name,
                             "wip",
                             version)

    @classmethod
    def get_main_pub_id(cls, version):
        return cls.create_id(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             Envars.task_name,
                             "main_pub",
                             version)

    @classmethod
    def get_pub_slot_id(cls, pub_slot, version):
        return cls.create_id(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             Envars.task_name,
                             pub_slot,
                             version)

    @classmethod
    def get_master_bundle_id(cls, version):
        return cls.create_id(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             "bundle",
                             version)

    @classmethod
    def get_sync_tasks_id(cls, version):
        return cls.create_id(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             "sync_tasks",
                             version)


class DbEntitiesAttrPaths:

    @classmethod
    def make_path(cls, *data, **kwargs):
        if data:
            id_elements = list()
            for elem in data:
                id_elements.append(elem)
            dotted_path = str(".".join(id_elements))
            return dotted_path
        return kwargs

    @property
    def get_path(self, *data, **kwargs):
        if data:
            id_elements = list()
            for elem in data:
                id_elements.append(elem)
            dotted_path = str(".".join(id_elements))
            return dotted_path
        return kwargs

    @classmethod
    def to_base(cls, dict_packed=False):
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
    def to_root_full(cls, dict_packed=False):
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
    def to_branch(cls, dict_packed=False):
        if dict_packed:
            return cls.make_path(show_name=Envars.show_name,
                                 branch_name=Envars.branch_name)

        return cls.make_path(Envars.show_name,
                             Envars.branch_name
                             )

    @classmethod
    def to_category(cls, dict_packed=False):
        if dict_packed:
            return cls.make_path(show_name=Envars.show_name,
                                 branch_name=Envars.branch_name,
                                 category=Envars.category)

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category
                             )

    @classmethod
    def to_entry(cls, dict_packed=False):
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
    def to_task(cls, relative=True):
        if relative:
            return cls.make_path("tasks", Envars.task_name)

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                               "tasks",
                             Envars.task_name)

    @classmethod
    def to_sync_tasks(cls, relative=True):
        if relative:
            return "sync_tasks"

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                               "sync_tasks")

    @classmethod
    def to_task_imports_from(cls, relative=True):
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
    def to_sync_task_slot(cls, relative=True):
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
    def to_pub_slots(cls, relative=True):
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
    def to_pub_slot_used_by(cls, pub_slot, relative=True):
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
    def to_entry_definition(cls, relative=True):
        if relative:
            return "definition"
        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                               "definition"
                             )

    @classmethod
    def to_master_bundle(cls, relative=True):
        if relative:
            return "master_bundle"

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             "master_bundle"
                             )

    @classmethod
    def to_entry_assignment(cls, relative=True):
        if relative:
            return "assignment"

        return cls.make_path(Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             "assignment"
                             )


class DbProjectAttrPaths:

    @classmethod
    def custom(cls, attr):
        """returns the @attr parameter as inputted"""
        return attr

    @classmethod
    def structure(cls):
        """Access path the full structure of the current project """
        return "structure"

    @classmethod
    def name(cls):
        """Access path project name property"""
        return "show_name"

    @classmethod
    def branches(cls):
        """Access path to all branches of the current project"""
        return "structure"

    @classmethod
    def categories(cls):
        """Access path to all categories of the current branch"""
        access_path = DbEntitiesAttrPaths.make_path("structure", Envars.branch_name)
        return access_path

    @classmethod
    def curr_branch(cls):
        """Access path to current branch of the current project"""
        curr_branch_path = DbEntitiesAttrPaths.make_path("structure", Envars.branch_name)
        return curr_branch_path

    @classmethod
    def curr_category(cls):
        """Access path to current category of the current project"""
        curr_category_path = DbEntitiesAttrPaths.make_path("structure", Envars.branch_name, Envars.category)
        return curr_category_path

    @classmethod
    def category_entries(cls):
        """Access path for categories of the branch"""
        access_path = DbEntitiesAttrPaths.make_path("structure", Envars.branch_name, Envars.category)
        return access_path

    @classmethod
    def show_defaults(cls):
        """Access path for show_defaults attribute of the current project"""
        return "show_defaults"

    @classmethod
    def entry(cls):
        """Access path for entries referenced inside the category"""
        access_path = DbEntitiesAttrPaths.make_path("structure", Envars.branch_name, Envars.category)
        return access_path

    @classmethod
    def is_active(cls):
        """Access path to is_active property of current project"""
        return "active"

    @classmethod
    def type(cls):
        """Access path to get project Type"""
        return "show_type"


class DbEntityAttrPaths:

    @classmethod
    def custom(cls, attr):
        """Access path to get the Type of an Entity"""
        return attr

    @classmethod
    def is_active(cls):
        """Access path to get if an Entity is active"""
        return "active"

    @classmethod
    def type(cls):
        """Access path to get the Type of an Entity"""
        return "type"

    @classmethod
    def tasks(cls):
        """Access path for tasks of the entry"""
        return "tasks"

    @classmethod
    def sync_tasks(cls):
        """Access path for tasks of the entry"""
        return "sync_tasks"

    @classmethod
    def assignments(cls):
        """Access path for tasks of the entry"""
        return "assignment"

    @classmethod
    def definition(cls):
        """Access path for tasks of the entry"""
        return "definition"

    @classmethod
    def master_bundle(cls):
        """Access path for tasks of the entry"""
        return "master_bundle"


class DbTaskAttrPaths:

    @classmethod
    def custom(cls, attr):
        """Access path to get the Type of an Entity"""
        return attr

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
    def is_active(cls):
        return cls.make_path("tasks", Envars.task_name,"active")

    @classmethod
    def status(cls):
        return cls.make_path("tasks", Envars.task_name,"status")

    @classmethod
    def artist(cls):
        return cls.make_path("tasks", Envars.task_name,"artist")

    @classmethod
    def imports_from(cls):
        return cls.make_path("tasks", Envars.task_name, "imports_from")

    @classmethod
    def pub_slots(cls):
        return cls.make_path("tasks", Envars.task_name, "pub_slots")


class DbSyncTaskAttrPaths:

    @classmethod
    def custom(cls, attr):
        """Access path to get the Type of an Entity"""
        return attr

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
    def sync_pub_slots(cls):
        return cls.make_path("sync_tasks", Envars.task_name)


class DbMainPubAttrPaths:

    @classmethod
    def custom(cls, attr):
        """Access path to get the Type of an Entity"""
        return attr

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
    def version(cls):
        return "version"


class DbPubSlotsAttrPaths:
    def __init__(self, publish_slot):
        self.pub_slot_name = publish_slot

    # def _pub_slot(self):
    #     return self.pub_slot_name

    def custom(self, attr):
        """Access path to get the Type of an Entity"""
        return attr

    def make_path(self, *data, **kwargs):
        if data:
            id_elements = list()
            for elem in data:
                id_elements.append(elem)
            dotted_path = str(".".join(id_elements))
            return dotted_path
        return kwargs

    def is_active(self):
        return self.make_path("tasks", Envars.task_name, "pub_slots", self.pub_slot_name, "active")

    def is_reviewable(self):
        return self.make_path("tasks", Envars.task_name, "pub_slots", self.pub_slot_name, "reviewable")

    def used_by(self):
        return self.make_path("tasks", Envars.task_name, "pub_slots", self.pub_slot_name, "used_by")

    def method(self):
        return self.make_path("tasks", Envars.task_name, "pub_slots", self.pub_slot_name, "method")

    def type(self):
        return self.make_path("tasks", Envars.task_name, "pub_slots", self.pub_slot_name, "type")


class DbBundleAttrPaths:
    def __init__(self, pub_slot):
        self.pub_slot_name = pub_slot

    def _pub_slot(self):
        return self.pub_slot_name

    @classmethod
    def custom(cls, attr):
        """Access path to get the Type of an Entity"""
        return attr

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
    def is_active(cls):
        return cls.make_path(cls._pub_slot, Envars.task_name,"active")

    @classmethod
    def is_reviewable(cls):
        return cls.make_path(cls._pub_slot, Envars.task_name, "reviewable")

    @classmethod
    def used_by(cls):
        return cls.make_path(cls._pub_slot, Envars.task_name, "used_by")

    @classmethod
    def method(cls):
        return cls.make_path(cls._pub_slot, Envars.task_name, "method")

    @classmethod
    def type(cls):
        return cls.make_path(cls._pub_slot, Envars.task_name, "type")



if __name__ == '__main__':
    Envars.show_name="Cicles"
    Envars.branch_name="assets"
    Envars.category="characters"
    Envars.entry_name="circle"
    Envars.task_name="rigging"

    # pp_path = pp.db_task_pub(relative=False, dict_packed=True)
    # print (pp_path)
    asset_id = DbPubSlotsAttrPaths(publish_slot="cmuscle_rig").type()

    print (asset_id)
