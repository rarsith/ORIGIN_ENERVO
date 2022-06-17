from database import db_connection as mdbconn


class From(object):

    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    @property
    def project(self):
        return "show"

    @property
    def builds(cls):
        return "build"

    @property
    def shots(self):
        return "sequences"

    @property
    def publishes(self):
        return "publishes"

    @property
    def bundles(self):
        return "bundles"

    @property
    def work_files(self):
        return "work_files"


class Origin(object):

    def __init__(self, db_collection, db_id, attribute):
        self.db = mdbconn.server[mdbconn.database_name]
        self.collection = db_collection
        self.attribute = attribute
        self.db_id = db_id

    def _string_to_list(self, data, splitter="."):
        """ @data: takes in string with OR without a separator (".", "_"...)
            @splitter: default splitter used
            @returns: if multiple resulting splits -> a list,
                      else-> the initial @data value
        """

        if not splitter in data:
            return data
        get_path_entities = data.split(splitter)
        return get_path_entities

    def _get_deep_value(self, data: dict, path_list: list) -> dict:
        """ @data: takes a nested dictionary
            @path_list: takes a list or a single string
            @returns: the value that is corresponding to the last list element in the path_list
        """

        if isinstance(path_list, str):
            result = data.get(path_list)
            return result
        elif isinstance(path_list, list) and len(path_list) == 1:
            result = data.get(path_list[0])
            return result
        else:
            for index, entity in enumerate(path_list):
                if isinstance(path_list, list) and len(path_list) > 1:
                    level = data.get(entity)
                    path_list.pop(index)
                    return self._get_deep_value(level, path_list)

    def _get_values(self, results: dict):
        for result in results:
            get_list = self._string_to_list(self.attribute)
            values = self._get_deep_value(data=result, path_list=get_list)
            return values

    def _get_keys(self, results: dict):
        data = self._get_values(results)
        return list(data)

    def get(self, attrib_names: bool = False ,attrib_values: bool = False):
        """
            will find all the key values from a collection and returns them as a dictionary
        """
        results = self.db[self.collection].find({"_id": self.db_id}, {"_id": 0, self.attribute: 1})

        if attrib_names and attrib_values:
            raise ValueError ("Choose either keys or values or leave default!")

        elif attrib_names:
            return self._get_keys(results)

        elif attrib_values:
            return self._get_values(results)

        else:
            for result in results:
                return result

    def update(self,*data):
        self.db[self.collection].update_one({"_id": self.db_id}, {"$set": {self.attribute: data}})

    def add(self, multiple_values=False, data=[]):
        if not multiple_values:
            self.db[self.collection].update_one({"_id": self.db_id}, {"$push": {self.attribute: data}})
        for each in data:
            self.db[self.collection].update_one({"_id": self.db_id}, {"$push": {self.attribute: each}})

    def remove(self, data=[]):
        self.db[self.collection].update_one({"_id": self.db_id}, {"$unset": {self.attribute: data}})

    def clear(self):
        self.db[self.collection].update_one({"_id": self.db_id}, {"$unset": {self.attribute: 1}})
        self.db[self.collection].update_one({"_id": self.db_id}, {"$set": {self.attribute: {}}})


if __name__ == '__main__':
    import pprint
    from envars.envars import Envars
    from database.db_components import DbId, DbAttr

    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "red_hulk"
    Envars.task_name = "rigging"

    # active_names = cc.active_projects
    # for items in cc:
    #     pprint.pprint (items)
    # entry_id = DbIds.curr_project_id()
    # attribute_to_q = DbAttr.entries()

    # db = mdbconn.server[mdbconn.database_name]
    # list_of = list()
    # cursor = db["show"]
    # for item in cursor.find({},{"_id":0,"show_name":1}):
    #     list_of.append(item)
    # pprint.pprint(list_of)

    # vv = DbIds.curr_entry_id()
    # print(vv)

    source = From().builds
    entity = DbId.curr_entry_id()
    attr = DbAttr.task_curr()
    print (attr)

    origin = Origin(source, entity, attr).get(attrib_names=True)
    # print (origin)
    # for i in origin:
    #     print(i)
    # origin = Origin(projects, entry_id, attribute_to_q).get(as_names=True)
    # origin = Origin(cc, 'Test.assets.characters.hulk.modeling.main_pub.v0001', "publishing_slots").get(as_names=True)
    # pprint.pprint (origin)
    print ("FROM <<{0}>> database collection,\n SELECT entity with _ID -- {1} -- ,\n use this STRING -- {2} --  to go to tasks and get them.\n\n----RESULT----\n{3} ".format(source ,entity, attr, origin))
