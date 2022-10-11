from database.db_defaults import DbDefaults
from envars.envars import Envars
from database import db_connection as mdbconn, db_templates
from database.utils.db_q_entity import From, QEntity, DbRef, DbReferences
from database.entities.db_structures import DbProjectBranch
from database.entities.db_constructors import DbConstructors
from database.entities.db_attributes import (DbEntitiesAttrPaths,
                                             DbProjectAttrPaths,
                                             DbEntityAttrPaths,
                                             DbTaskAttrPaths,
                                             DbSyncTaskAttrPaths,
                                             DbPubSlotsAttrPaths)
from database.db_ids import DbIds
from database.utils import db_path_assembler


class DbProject:
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self, name):
        entity_id = db_path_assembler.make_path("root", name)
        created_id, save_data = DbConstructors().project_construct(name=name, entity_id=entity_id)

        try:
            self.db.show.insert_one(save_data)
            print("{} Project created!".format(name))

        except ValueError as e:
            print("{} Error! Nothing created!".format(e))

    def get_all(self):
        """Returns all assets names in the current category"""
        try:
            result = QEntity(From().projects,
                             DbIds.all_in_collection(),
                             DbProjectAttrPaths.name()
                             ).get(all=True)
            return result
        except ValueError as val:
            raise ("{} Error! Nothing Done!".format(val))

    @staticmethod
    def get_structure():
        try:
            structure = QEntity(From().projects,
                                DbIds.curr_project_id(),
                                DbProjectAttrPaths.structure()
                                ).get(attrib_values=True)
            return structure

        except ValueError as val:
            raise ("{} Error! Nothing Done!".format(val))

    @staticmethod
    def get_entities_names():
        entities_found = list()

        origin_q = QEntity(From().projects,
                           DbIds.curr_project_id(),
                           DbProjectAttrPaths.category_entries()
                           ).get(attrib_names=True)

        for entity in origin_q:
            name = DbRef().db_deref(ref_string=entity, get_field="entry_name")
            entities_found.append(name)

        return entities_found

    @staticmethod
    def get_type():
        try:
            show_type = QEntity(From().projects,
                                DbIds.curr_project_id(),
                                DbProjectAttrPaths.type()
                                ).get(attrib_names=True)
            return show_type
        except ValueError as val:
            print ("{} Nothing Done!".format(val))

    @staticmethod
    def is_active():
        try:
            is_active = QEntity(From().projects,
                                DbIds.curr_project_id(),
                                DbProjectAttrPaths.is_active()
                                ).get(attrib_names=True)
            return is_active
        except ValueError as val:
            print ("{} Nothing Done!".format(val))


class DbAsset:
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self, name):
        collection = self.db[From().entities]
        created_id, save_data = DbConstructors().asset_construct(name=name,
                                                                 entity_id=DbIds.create_entity_id(name))

        try:
            collection.insert_one(save_data)

            insert_entry = db_path_assembler.make_path("structure",
                                                        Envars().branch_name,
                                                        Envars().category)

            DbReferences.add_db_id_reference(collection="show",
                                             parent_doc_id=DbIds.curr_project_id(),
                                             destination_slot=insert_entry,
                                             id_to_add=created_id,
                                             from_collection=DbProjectBranch().get_type,
                                             replace=False)

            print("{} Origin Asset created!".format(name))

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def get_all(self, is_active=True):
        """Returns all assets names in the current category"""
        try:
            result = QEntity(db_collection=From().projects,
                             entry_id=DbIds.curr_project_id(),
                             attribute=DbProjectAttrPaths.category_entries()
                             ).get(attrib_names=True, all_active=is_active)
            return result
        except ValueError as val:
            raise ("{} Error! Nothing Done!".format(val))

    @staticmethod
    def get_definition():
        try:
            result = QEntity(db_collection=From().entities,
                             entry_id=DbIds.curr_entry_id(),
                             attribute=DbEntityAttrPaths.definition()
                             ).get(attrib_names=True)
            return result
        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    @staticmethod
    def get_entry_type():
        try:
            result = QEntity(db_collection=From().entities,
                             entry_id=DbIds.curr_entry_id(),
                             attribute=DbEntityAttrPaths.type()
                             ).get(attrib_names=True)
            return result
        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    @staticmethod
    def get_assignment():
        try:
            result = QEntity(db_collection=From().entities,
                             entry_id=DbIds.curr_entry_id(),
                             attribute=DbEntityAttrPaths.assignments()
                             ).get(attrib_names=True)
            return result
        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))

    @staticmethod
    def set_active(is_active=True):
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute=DbEntityAttrPaths.is_active()
                ).update(is_active)

        print("{0} active Status set to {1}!".format(DbIds.curr_entry_id(), is_active))

    @staticmethod
    def set_definition(data):
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute=DbEntityAttrPaths.definition
                ).update(data)
        print("{} Definition Updated!".format(Envars.entry_name))

    def remove(self):
        #TODO: refactor code to use fully the Envars
        try:
            QEntity(db_collection=From().projects,
                    entry_id=DbIds.curr_project_id(),
                    attribute=DbProjectAttrPaths.entry()
                    ).remove()

            QEntity(db_collection=From().entities,
                    entry_id=DbIds.curr_entry_id(),
                    attribute=DbEntityAttrPaths.type()
                    ).remove()

        except ValueError as val:
            raise("{} Error! Nothing Done!".format(val))


class DbTasks:
    def create(self, name):
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute=DbEntityAttrPaths.tasks()
                ).add_property(name=name, add_data=db_templates.task_defaults())

        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute=DbEntityAttrPaths.sync_tasks()
                ).add_property(name=name, add_data={})

        print("{} Origin Asset Task created!".format(name))
        return name

    def get_tasks(self) -> list:
        try:
            tasks_list = QEntity(db_collection=From().entities,
                                 entry_id=DbIds.curr_entry_id(),
                                 attribute=DbEntityAttrPaths.tasks()
                                 ).get(attrib_names=True)

            return tasks_list

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    def get_tasks_full(self) -> dict:
        try:
            tasks_list = QEntity(db_collection=From().entities,
                                 entry_id=DbIds.curr_entry_id(),
                                 attribute=DbEntityAttrPaths.tasks()
                                 ).get()

            return tasks_list
        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @property
    def is_active(self) -> bool:
        try:
            is_active_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute=DbTaskAttrPaths.is_active()
                                     ).get(attrib_values=True)
            return is_active_data

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @is_active.setter
    def is_active(self, is_active) -> None:
        try:
            QEntity(db_collection=From().entities,
                    entry_id=DbIds.curr_entry_id(),
                    attribute=DbTaskAttrPaths.is_active()
                    ).update(data=is_active)

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @property
    def status(self) -> str:
        try:
            status_data = QEntity(db_collection=From().entities,
                                  entry_id=DbIds.curr_entry_id(),
                                  attribute=DbTaskAttrPaths.status()
                                  ).get(attrib_values=True)
            return status_data

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @status.setter
    def status(self, task_status: str) -> None:
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute=DbTaskAttrPaths.status()
                ).update(data=task_status)

    @property
    def task_user(self) -> str:
        user = QEntity(db_collection=From().entities,
                       entry_id=DbIds.curr_entry_id(),
                       attribute=DbTaskAttrPaths.artist()
                       ).get(attrib_values=True)
        return user

    @task_user.setter
    def task_user(self, artist_name: str) -> None:
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute=DbTaskAttrPaths.artist()
                ).update(data=artist_name)

    @property
    def imports_from(self) -> list:
        try:
            imports_from_data = QEntity(db_collection=From().entities,
                                        entry_id=DbIds.curr_entry_id(),
                                        attribute=DbTaskAttrPaths.imports_from()
                                        ).get(attrib_values=True)
            return imports_from_data
        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @imports_from.setter
    def imports_from(self, imports_from: list) -> None:
        for each in imports_from:
            QEntity(db_collection=From().entities,
                    entry_id=DbIds.curr_entry_id(),
                    attribute=DbTaskAttrPaths.imports_from()
                    ).add(data=each)
            print("{} task added as import_source".format(each))

    def rem_import_slots(self) -> None:
        try:
            QEntity(db_collection=From().entities,
                    entry_id=DbIds.curr_entry_id(),
                    attribute=DbTaskAttrPaths.imports_from()
                    ).clear()
        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))


class DbPubSlot:
    def create(self, name: str) -> str:
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute=DbTaskAttrPaths.pub_slots()
                ).add_property(name=name, add_data=db_templates.tasks_pub_slot_schema())

        DbSyncTasks().add_sync_task_slot(name)
        print("{} Task Pub Slot created!".format(name))
        return name

    def add_multiple(self, pub_slot: list) -> None:
        for each in pub_slot:
            self.create(each)
            print("{} added as pub_slot".format(each))

    def add_dict(self, pub_slot: dict) -> None:
        for each in pub_slot:
            get_slot_name = (list(each.keys()))
            get_slot_param = (list(each.values()))

            QEntity(db_collection=From().entities,
                    entry_id=DbIds.curr_entry_id(),
                    attribute=DbTaskAttrPaths.pub_slots()
                    ).add_property(name=get_slot_name[0], add_data=get_slot_param[0])

        print("Publish Slot added succesfully!")

    def get_pub_slots(self) -> list:
        try:
            pub_slots_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute=DbTaskAttrPaths.pub_slots()
                                     ).get(attrib_names=True)
            return pub_slots_data

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def get_type(self, pub_slot: str) -> str:
        try:
            pub_slots_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute=DbPubSlotsAttrPaths(publish_slot=pub_slot).type()
                                     ).get(attrib_values=True)
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def get_method(self, pub_slot: str) -> str:
        try:
            pub_slots_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute=DbPubSlotsAttrPaths(publish_slot=pub_slot).method()
                                     ).get(attrib_values=True)
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def get_used_by(self, pub_slot: str) -> list:
        try:
            pub_slots_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute=DbPubSlotsAttrPaths(publish_slot=pub_slot).used_by()
                                     ).get(attrib_values=True)
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def get_used_by_task(self, data, task_name):
        get_pub_slots = []
        get_slots = list(data.keys())
        for x in get_slots:
            if task_name in data[x]['used_by']:
                get_pub_slots.append(x)
        return get_pub_slots

    def get_is_reviewable(self, pub_slot: str) -> bool:
        try:
            pub_slots_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute=DbPubSlotsAttrPaths(publish_slot=pub_slot).is_reviewable()
                                     ).get(attrib_values=True)
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def get_is_active(self, pub_slot: str) -> None:
        try:
            pub_slots_data = QEntity(db_collection=From().entities,
                                     entry_id=DbIds.curr_entry_id(),
                                     attribute=DbPubSlotsAttrPaths(publish_slot=pub_slot).is_active()
                                     ).get(attrib_values=True)
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def set_used_by(self, pub_slot: str, used_by: str, remove_action: bool=False) -> None:
        used_by_data = QEntity(db_collection=From().entities,
                               entry_id=DbIds.curr_entry_id(),
                               attribute=DbPubSlotsAttrPaths(publish_slot=pub_slot).used_by()
                               ).get(attrib_values=True)

        if not remove_action:
            if used_by not in used_by_data:
                QEntity(db_collection=From().entities,
                        entry_id=DbIds.curr_entry_id(),
                        attribute=DbPubSlotsAttrPaths(publish_slot=pub_slot).used_by()
                        ).add(data=used_by)

        else:
            if used_by in used_by_data:
                QEntity(db_collection=From().entities,
                        entry_id=DbIds.curr_entry_id(),
                        attribute=DbPubSlotsAttrPaths(publish_slot=pub_slot).used_by()
                        ).remove_value(data=used_by)

    def remove_all(self) -> None:
        try:
            QEntity(db_collection=From().entities,
                    entry_id=DbIds.curr_entry_id(),
                    attribute=DbTaskAttrPaths.pub_slots(),
                    ).clear()

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))


class DbSyncTasks:
    @staticmethod
    def create_from_template():
        get_tasks_config = DbDefaults().get_show_defaults(DbDefaults().root_tasks)
        entity_tasks = list(get_tasks_config[0])
        save_elements_list = dict()
        for task in entity_tasks:
            task_definition = (get_tasks_config[0][task])
            task_pub_slots = (list(task_definition["pub_slots"].keys()))
            make_dictionary = dict.fromkeys(task_pub_slots, {})
            nest_slot = {task: make_dictionary}
            save_elements_list.update(nest_slot)

        return save_elements_list

    def capture_all(self) -> dict:
        try:
            tasks_list = QEntity(db_collection=From().entities,
                                 entry_id=DbIds.curr_entry_id(),
                                 attribute=DbEntityAttrPaths.sync_tasks()
                                 ).get(attrib_values=True)
            return tasks_list

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    def add(self, data: dict):
        existing_sync_tasks = self.capture_all()
        return existing_sync_tasks.update(data)

    def add_sync_task(self, name: str) -> None:
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute=DbEntityAttrPaths.sync_tasks()
                ).add_property(name=name, add_data={})

        print("{} Sync Tasks saved!".format(name))

    def add_sync_task_slot(self, name: str) -> None:
        QEntity(db_collection=From().entities,
                entry_id=DbIds.curr_entry_id(),
                attribute=DbSyncTaskAttrPaths.sync_pub_slots()
                ).add_property(name=name, add_data={})

        print("{} Sync Slot saved!".format(name))

    def get_sync_task_slots(self) -> dict:
        try:
            tasks_list = QEntity(db_collection=From().entities,
                                 entry_id=DbIds.curr_entry_id(),
                                 attribute=DbSyncTaskAttrPaths.sync_pub_slots()
                                 ).get(attrib_values=True)

            return tasks_list

        except ValueError as vale:
            print(vale)


class DbBundle:
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def create(self):
        inserted_id, save_content = DbConstructors().bundle_construct()
        master_bundle = self.db.bundles.insert_one(save_content)
        print("{0}, has been published".format(inserted_id))
        return master_bundle.inserted_id

    def create_stream(self, name):
        try:
            asset_id = DbIds.curr_entry_id()
            cursor = self.db[DbProjectBranch().get_type]
            db_path = db_path_assembler.make_path(DbEntitiesAttrPaths.to_master_bundle(),
                                                    (name + "_" + "stream"))

            cursor.update_one({"_id": asset_id}, {"$set": {db_path:[]}})
            print("{} Bundle Stream  created!".format(name))
            return name

        except ValueError as e:
            print("{} Error! Nothing Created!".format(e))

    @staticmethod
    def add_to_bundle(entity_id, bundle_id, slot):
        DbReferences.add_db_id_reference("bundles",
                                         bundle_id,
                                         "master_bundle.{}".format(slot),
                                         entity_id,
                                         DbProjectBranch().get_type,
                                         replace=True)
        return bundle_id

    def add_slot(self, name):
        pass

    def rem_slot(self, name):
        pass

    def update_slot(self, name):
        pass

    def update_master(self):
        pass

    @staticmethod
    def set_as_current(bundle_id, add_to_stream="main_stream"):

        DbReferences.add_db_id_reference(DbProjectBranch().get_type,
                                         DbIds.curr_entry_id(),
                                         "master_bundle.{}".format(add_to_stream),
                                         bundle_id,
                                         "bundles",
                                         replace=True)
        return bundle_id

    def set_slot_state(self, state):
        statuses = ["renderable", "matte_object"]
        pass

    def validate_bundle(self):
        pass

    def health_check(self):
        pass

    def mv_to_stream(self, from_stream, to_stream):
        #TODO: finish the method
        try:
            task_path = DbEntitiesAttrPaths.to_pub_slots()
            print(task_path)
            cursor = self.db[DbProjectBranch().get_type]
            cursor.update_one({"_id": DbIds.curr_entry_id()}, {"$unset": {task_path: 1}})
            cursor.update_one({"_id": DbIds.curr_entry_id()}, {"$set": {task_path: {}}})
        except:
            pass


if __name__ == '__main__':
    Envars.show_name = "Green"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "circle"
    Envars.task_name = "rigging"

    definition ={"crap":"mofo"}


    xx = DbProject().get_all()
    print (xx)






