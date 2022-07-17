from envars.envars import Envars
from database import db_templates
from database.db_defaults import DbDefaults
from database.db_attributes import (DbEntitiesId,
                                    DbTaskAttributes,
                                    DbEntityAttributes,
                                    DbSyncTaskAttributes,
                                    DbPubSlotsAttributes)
from database.utils.db_q_entity import From, QEntity


class DbTasks(object):
    def create(self, name):
        QEntity(From().entities,
                DbEntitiesId.curr_entry_id(),
                DbEntityAttributes.tasks()
                ).add_property(name=name, add_data=db_templates.task_defaults())

        QEntity(From().entities,
                DbEntitiesId.curr_entry_id(),
                DbEntityAttributes.sync_tasks()
                ).add_property(name=name, add_data={})

        print("{} Origin Asset Task created!".format(name))
        return name

    def get_tasks(self) -> list:
        try:
            tasks_list = QEntity(From().entities,
                                 DbEntitiesId.curr_entry_id(),
                                 DbEntityAttributes.tasks()
                                 ).get(attrib_names=True)

            return tasks_list

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    def get_tasks_full(self) -> dict:
        try:
            tasks_list = QEntity(From().entities,
                                 DbEntitiesId.curr_entry_id(),
                                 DbEntityAttributes.tasks()
                                 ).get()

            return tasks_list
        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @property
    def is_active(self) -> bool:
        try:
            is_active_data = QEntity(From().entities,
                                     DbEntitiesId.curr_entry_id(),
                                     DbTaskAttributes.is_active()
                                     ).get(attrib_values=True)
            return is_active_data

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @is_active.setter
    def is_active(self, is_active) -> None:
        try:
            QEntity(From().entities,
                    DbEntitiesId.curr_entry_id(),
                    DbTaskAttributes.is_active()
                    ).update(data=is_active)

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @property
    def status(self) -> str:
        try:
            status_data = QEntity(From().entities,
                                  DbEntitiesId.curr_entry_id(),
                                  DbTaskAttributes.status()
                                  ).get(attrib_values=True)
            return status_data

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @status.setter
    def status(self, task_status: str) -> None:
        QEntity(From().entities,
                DbEntitiesId.curr_entry_id(),
                DbTaskAttributes.status()
                ).update(data=task_status)

    @property
    def task_user(self) -> str:
        user = QEntity(From().entities,
                       DbEntitiesId.curr_entry_id(),
                       DbTaskAttributes.artist()
                       ).get(attrib_values=True)
        return user

    @task_user.setter
    def task_user(self, artist_name: str) -> None:
        QEntity(From().entities,
                DbEntitiesId.curr_entry_id(),
                DbTaskAttributes.artist()
                ).update(data=artist_name)

    @property
    def imports_from(self) -> list:
        try:
            imports_from_data = QEntity(From().entities,
                                        DbEntitiesId.curr_entry_id(),
                                        DbTaskAttributes.imports_from()
                                        ).get(attrib_values=True)
            return imports_from_data
        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    @imports_from.setter
    def imports_from(self, imports_from: list) -> None:
        for each in imports_from:
            QEntity(From().entities,
                    DbEntitiesId.curr_entry_id(),
                    DbTaskAttributes.imports_from()
                    ).add(data=each)
            print("{} task added as import_source".format(each))

    def rem_import_slots(self) -> None:
        try:
            QEntity(From().entities,
                    DbEntitiesId.curr_entry_id(),
                    DbTaskAttributes.imports_from()
                    ).clear()
        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))


class DbSyncTasks(object):
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
            tasks_list = QEntity(From().entities,
                                 DbEntitiesId.curr_entry_id(),
                                 DbEntityAttributes.sync_tasks()
                                 ).get(attrib_values=True)
            return tasks_list

        except ValueError as e:
            print("{} Error! Nothing Done!".format(e))

    def add(self, data: dict):
        existing_sync_tasks = self.capture_all()
        return existing_sync_tasks.update(data)

    def add_sync_task(self, name: str) -> None:
        QEntity(From().entities,
                DbEntitiesId.curr_entry_id(),
                DbEntityAttributes.sync_tasks()
                ).add_property(name=name, add_data={})

        print("{} Sync Tasks saved!".format(name))

    def add_sync_task_slot(self, name: str) -> None:
        QEntity(From().entities,
                DbEntitiesId.curr_entry_id(),
                DbSyncTaskAttributes.sync_pub_slots()
                ).add_property(name=name, add_data={})

        print("{} Sync Slot saved!".format(name))

    def get_sync_task_slots(self) -> dict:
        try:
            tasks_list = QEntity(From().entities,
                                 DbEntitiesId.curr_entry_id(),
                                 DbSyncTaskAttributes.sync_pub_slots()
                                 ).get(attrib_values=True)

            return tasks_list

        except ValueError as vale:
            print(vale)


class DbPubSlot(object):
    def create(self, name: str) -> str:
        QEntity(From().entities,
                DbEntitiesId.curr_entry_id(),
                DbTaskAttributes.pub_slots()
                ).add_property(name=name, add_data=db_templates.tasks_pub_slot_schema())

        DbSyncTasks().add_sync_task_slot(name)
        print("{} Task Pub Slot created!".format(name))
        return name

    def add_multiple(self, pub_slot: list) -> None:
        for each in pub_slot:
            self.create(each)
            print("{} added as pub_slot".format(each))

    def add_dict(self, pub_slot: list) -> None:
        for each in pub_slot:
            get_slot_name = (list(each.keys()))
            get_slot_param = (list(each.values()))

            QEntity(From().entities,
                    DbEntitiesId.curr_entry_id(),
                    DbTaskAttributes.pub_slots()
                    ).add_property(name=get_slot_name[0], add_data=get_slot_param[0])

        print("Publish Slot added succesfully!")

    def get_pub_slots(self) -> list:
        try:
            pub_slots_data = QEntity(From().entities,
                                     DbEntitiesId.curr_entry_id(),
                                     DbTaskAttributes.pub_slots()
                                     ).get(attrib_names=True)
            return pub_slots_data

        except Exception as e:
            print("{} Error! Nothing Created!".format(e))

    def get_type(self, pub_slot: str) -> str:
        try:
            pub_slots_data = QEntity(From().entities,
                                     DbEntitiesId.curr_entry_id(),
                                     DbPubSlotsAttributes(publish_slot=pub_slot).type()
                                     ).get(attrib_values=True)
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def get_method(self, pub_slot: str) -> str:
        try:
            pub_slots_data = QEntity(From().entities,
                                     DbEntitiesId.curr_entry_id(),
                                     DbPubSlotsAttributes(publish_slot=pub_slot).method()
                                     ).get(attrib_values=True)
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def get_used_by(self, pub_slot: str) -> list:
        try:
            pub_slots_data = QEntity(From().entities,
                                     DbEntitiesId.curr_entry_id(),
                                     DbPubSlotsAttributes(publish_slot=pub_slot).used_by()
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
            pub_slots_data = QEntity(From().entities,
                                     DbEntitiesId.curr_entry_id(),
                                     DbPubSlotsAttributes(publish_slot=pub_slot).is_reviewable()
                                     ).get(attrib_values=True)
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def get_is_active(self, pub_slot: str) -> None:
        try:
            pub_slots_data = QEntity(From().entities,
                                     DbEntitiesId.curr_entry_id(),
                                     DbPubSlotsAttributes(publish_slot=pub_slot).is_active()
                                     ).get(attrib_values=True)
            return pub_slots_data

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))

    def set_used_by(self, pub_slot: str, used_by: str, remove_action: bool=False) -> None:
        used_by_data = QEntity(From().entities,
                               DbEntitiesId.curr_entry_id(),
                               DbPubSlotsAttributes(publish_slot=pub_slot).used_by()
                               ).get(attrib_values=True)

        if not remove_action:
            if used_by not in used_by_data:
                QEntity(From().entities,
                        DbEntitiesId.curr_entry_id(),
                        DbPubSlotsAttributes(publish_slot=pub_slot).used_by()
                        ).add(data=used_by)

        else:
            if used_by in used_by_data:
                QEntity(From().entities,
                        DbEntitiesId.curr_entry_id(),
                        DbPubSlotsAttributes(publish_slot=pub_slot).used_by()
                        ).remove_value(data=used_by)

    def remove_all(self) -> None:
        try:
            QEntity(From().entities,
                    DbEntitiesId.curr_entry_id(),
                    DbTaskAttributes.pub_slots(),
                    ).clear()

        except Exception as e:
            raise ValueError("Error! Nothing Done! -- {}".format(e))


if __name__ == "__main__":
    from database.db_statuses import DbStatuses
    import pprint

    Envars.show_name = "Cicles"
    Envars.branch_name = "assets"
    Envars.category = "characters"
    Envars.entry_name = "circle"
    Envars.task_name = "rigging"

    imports_from_menu = [
        "modeling.rend_geo",
        "modeling.proxy_geo",
        "modeling.utility",
        "facs.main_shapes",
        "facs.correctives"

    ]

    pub_slots_pool = [
        "locatores",
        "curves",
        "points"
    ]

    s = DbPubSlot()
    # s.is_active = False
    t = s.remove_all()
    pprint.pprint(t)