class From(object):

    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]


    def dummy(self, dum):
        return dum

    @property
    def entity(self):
        db_collection = DbProjectBranch().get_type
        results = self.db[db_collection].find({"_id": DbIds.curr_entry_id()})
        for item in results:
            return item

    @classmethod
    def builds(cls):
        return "build"

    @property
    def publishes(self):
        # list_of = list()
        cursor = self.db["publishes"]
        to_return = cursor.find({"show_name": Envars.show_name})
        return to_return
            # list_of.append(item)
        # return list_of

    @property
    def bundles(self):
        list_of = list()
        cursor = self.db["bundles"]
        for item in cursor.find({"show_name": Envars.show_name}, {"_id": 0, self.attr: 1}):
            list_of.append(item)
        return list_of

    @bundles.setter
    def bundles(self, attr):
        self.attr = attr

    @property
    def project(self) -> dict:
        results = self.db["show"].find({"_id": DbIds.curr_project_id()})
        for item in results:
            return item

    @property
    def active_projects(self) -> list:
        list_of = list()
        cursor = self.db["show"]
        for item in cursor.find({"active": True}, {"_id": 0, self.attr:1}):
            list_of.append(item[self.attr])
        return list_of

    @active_projects.setter
    def active_projects(self, attr):
        self.attr = attr

    @property
    def work_files(self):
        list_of = list()
        cursor = self.db["work_files"]
        for item in cursor.find({"show_name": Envars.show_name}, {"_id": 0, self.attr: 1}):
            list_of.append(item)
        return list_of

    @work_files.setter
    def work_files(self, attr):
        self.attr = attr
