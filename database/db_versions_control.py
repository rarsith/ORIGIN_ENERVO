from database.utils import db_find_key
from database.db_paths import DbPaths
from database.db_collections import DbCollections
from envars.envars import Envars
from common_utils import version_increment as version_up


class DBVersionControl(object):

    def db_main_pub_ver_increase(self):
        get_versions = db_find_key.db_find(db_collection=DbCollections.main_publishes(),
                                           item_to_search="version",
                                           **DbPaths.path_root(dict_packed=True)
                                           )
        new_version = version_up.version_increment(get_versions)
        return new_version

    def db_pubslot_ver_increase(self, collection_name, slot_name):
        get_versions = db_find_key.db_find(collection_name,
                                           item_to_search="version",
                                           **DbPaths.path_root(dict_packed=True),
                                           slot_name=slot_name
                                           )

        new_version = version_up.version_increment(get_versions)
        return new_version

    def db_master_bundle_ver_increase(self):

        get_versions = db_find_key.db_find(db_collection=DbCollections.bundles(),
                                           item_to_search="version",
                                           **DbPaths.path_to_entry(dict_packed=True)
                                           )

        new_version = version_up.version_increment(get_versions)
        return new_version

    def db_sync_tasks_ver_increase(self):

        get_versions = db_find_key.db_find(db_collection=DbCollections.sync_tasks(),
                                           item_to_search="version",
                                           **DbPaths.path_to_entry(dict_packed=True)
                                           )

        new_version = version_up.version_increment(get_versions)
        return new_version

    def db_wip_files_version_increase(self, collection_name):

        get_versions = db_find_key.db_find(db_collection=collection_name,
                                           item_to_search="version",
                                           show_name=Envars.show_name,
                                           branch_name=Envars.branch_name,
                                           category=Envars.category,
                                           entry_name=Envars.entry_name,
                                           task_name=Envars.task_name
                                           )
        new_version = version_up.version_increment(get_versions)
        return new_version

if __name__ == '__main__':
    Envars.show_name = "Test"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "hulk"
    Envars.task_name = "modeling"

    xx = DBVersionControl()
    cc = xx.db_master_bundle_ver_increase()
    print (cc)