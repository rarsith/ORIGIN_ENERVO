from database.utils import db_find_key
from envars.envars import Envars
from common_utils import version_increment as version_up


class DBVersionControl(object):

    def db_task_ver_increase(self):
        get_versions = db_find_key.db_find_key("publishes", "version",
                                         show_name=Envars.show_name,
                                         category=Envars.category,
                                         entry_name=Envars.entry_name,
                                         task_name=Envars.task_name,
                                         )
        new_version = version_up.version_increment(get_versions)
        return new_version

    def db_pubslot_ver_increase(self, collection_name, slot_name):

        get_versions = db_find_key.db_find_key(collection_name, "version",
                                         show_name=Envars.show_name,
                                         category=Envars.category,
                                         entry_name=Envars.entry_name,
                                         task_name=Envars.task_name,
                                         slot_name=slot_name
                                         )

        new_version = version_up.version_increment(get_versions)
        return new_version

    def db_master_bundle_ver_increase(self):

        get_versions = db_find_key.db_find_key("bundles", "version",
                                         show_name=Envars.show_name,
                                         category=Envars.category,
                                         entry_name=Envars.entry_name
                                         )

        new_version = version_up.version_increment(get_versions)
        return new_version

    def db_sync_tasks_ver_increase(self):

        get_versions = db_find_key.db_find_key("task_sync", "version",
                                         show_name=Envars.show_name,
                                         category=Envars.category,
                                         entry_name=Envars.entry_name
                                         )

        new_version = version_up.version_increment(get_versions)
        return new_version

    def db_wip_files_version_increase(self, collection_name):
        get_versions = db_find_key.db_find_key(collection_name, "version",
                                         show_name=Envars.show_name,
                                         category=Envars.category,
                                         entry_name=Envars.entry_name,
                                         task_name=Envars.task_name
                                         )
        new_version = version_up.version_increment(get_versions)
        return new_version
