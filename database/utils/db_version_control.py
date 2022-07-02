from common_utils import version_increment as vup
from database.db_attributes import DbPath
from database.utils.db_q_collection import DbQCollection
from database.utils.db_q_entity import From


class DBVersionControl(object):

    @staticmethod
    def db_main_pub_ver_increase():
        get_versions = DbQCollection().db_find(db_collection=From().publishes,
                                               item_to_search="version",
                                               **DbPath.to_base(dict_packed=True)
                                               )
        new_version = vup.version_increment(get_versions)
        return new_version

    @staticmethod
    def db_pubslot_ver_increase(collection_name, slot_name):
        get_versions = DbQCollection().db_find(db_collection=collection_name,
                                               item_to_search="version",
                                               **DbPath.to_base(dict_packed=True),
                                               slot_name=slot_name
                                               )

        new_version = vup.version_increment(get_versions)
        return new_version

    @staticmethod
    def db_master_bundle_ver_increase():
        get_versions = DbQCollection().db_find(db_collection=From().bundles,
                                               item_to_search="version",
                                               **DbPath.to_entry(dict_packed=True)
                                               )

        new_version = vup.version_increment(get_versions)
        return new_version

    @staticmethod
    def db_sync_tasks_ver_increase():
        get_versions = DbQCollection().db_find(db_collection=From().sync_tasks,
                                               item_to_search="version",
                                               **DbPath.to_entry(dict_packed=True)
                                               )

        new_version = vup.version_increment(get_versions)
        return new_version

    @staticmethod
    def db_wip_files_version_increase(collection_name):
        get_versions = DbQCollection().db_find(db_collection=collection_name,
                                               item_to_search="version",
                                               **DbPath.to_root_full(dict_packed=True)
                                               )
        new_version = vup.version_increment(get_versions)
        return new_version
