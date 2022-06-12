from bson import ObjectId
from database import db_connection as mdbconn
from database.db_versions_control import DBVersionControl
from database.db_ids import DbIds
from common_utils.users import Users
from common_utils.output_paths import OutputPaths
from common_utils.date_time import DateTime
from database.db_references import DbReferences
from database.entities.properties.db_pub_slot import DbPubSlot
from database.entities.db_project import DbProject
from database.entities.properties.db_sync_tasks import DbSyncTasks
from envars.envars import Envars

class DbPublish(object):
    def __init__(self):
        self.db = mdbconn.server[mdbconn.database_name]

    def get_db_publishes_ids(self, collection, show_name=None, branch_name=None, category_name=None, entry_name=None, task_name=None, view_limit=0):
        #TODO change this to database aggregations
        store_value = list()

        cursor = self.db[collection]

        if show_name and branch_name and category_name and entry_name and task_name:
            test = cursor.find(
                {"show_name": show_name, "branch": branch_name, "category": category_name, "entry_name": entry_name,
                 "task_name": task_name}).limit(view_limit)
            for publishes in test:
                store_value.append(str(publishes["_id"]))
        elif show_name and branch_name and category_name and entry_name:
            test = cursor.find({"show_name": show_name, "branch": branch_name, "category": category_name,
                                "entry_name": entry_name}).limit(view_limit)
            for publishes in test:
                store_value.append(str(publishes["_id"]))

        elif show_name and branch_name and category_name:
            test = cursor.find({"show_name": show_name, "branch": branch_name, "category": category_name}).limit(
                view_limit)
            for publishes in test:
                store_value.append(str(publishes["_id"]))

        elif show_name and branch_name:
            test = cursor.find({"show_name": show_name, "branch": branch_name}).limit(view_limit)
            for publishes in test:
                store_value.append(str(publishes["_id"]))

        elif show_name:
            test = cursor.find({"show_name": show_name}).limit(view_limit)
            for publishes in test:
                store_value.append(str(publishes["_id"]))

        else:
            test = cursor.find({}).limit(view_limit)
            for publishes in test:
                store_value.append(str(publishes["_id"]))

        return store_value

    def get_db_values(self, collection, document_id, value_to_return):
        if not collection or not document_id or collection == None or document_id == None:
            return
        else:
            selected_document = self.db[collection].find_one({"_id": ObjectId(document_id)})
            return (selected_document[value_to_return])

    def db_main_publish(self):

        version = DBVersionControl().db_task_ver_increase()
        set_display_name = "_".join([Envars.entry_name, "main_publish"])

        common_id = DbIds.db_main_pub_id(version)
        collection_name = "publishes"

        save_content = dict(
            _id= common_id,
            reviewable_component= "insert_movie",
            show_name= Envars.show_name,
            entry_name= Envars.entry_name,
            category= Envars.category,
            branch= Envars.branch_name,
            task_name= Envars.task_name,
            status= "PENDING_REVIEW",
            description= [],
            artist= Users.get_current_user(),
            version= version,
            date= DateTime().return_date,
            time= DateTime().return_time,
            publish_packaging= "main",
            publishing_slots= [],
            display_name= set_display_name
        )


        published = self.db[collection_name].insert_one(save_content)

        print("{0} Main Publish Done!".format(set_display_name))
        return published.inserted_id, collection_name

    def db_slot_publish(self, pub_slot):
        #TODO check if slot is active

        collection_name = "_".join(["publish", "slots", Envars.task_name])
        version = DBVersionControl().db_pubslot_ver_increase(collection_name, pub_slot)
        set_display_name = "_".join(["pubslot", pub_slot, Envars.task_name])
        build_server_path = [Envars.show_name,
                             Envars.branch_name,
                             Envars.category,
                             Envars.entry_name,
                             Envars.task_name,
                             version,
                             pub_slot]

        common_id = DbIds.db_slot_pub_id(pub_slot, version)
        bundle = 'current_bundle'


        save_content = dict(
            _id=common_id,
            reviewable_component = "insert_movie_path",
            slot_thumbnail= "insert_thumbnail_path",
            show_name= Envars.show_name,
            entry_name= Envars.entry_name,
            category= Envars.category,
            branch= Envars.branch_name,
            task_name= Envars.task_name,
            update_type="non-critical",
            artist= Users.get_current_user(),
            slot_name= pub_slot,
            status= "PENDING-REVIEW",
            version_origin= "created",
            version= version,
            date= DateTime().return_date,
            time= DateTime().return_time,
            publish_packaging= "slots",
            parent_collection= collection_name,
            display_name= set_display_name ,
            output_path= build_server_path,
            components= dict(path=OutputPaths(version, pub_slot, "cache.abc").main_publish_path(),
                             rc_source_images=OutputPaths(version, pub_slot, "image.%04d.exr").original_images_path(),
                             rc_source_video= OutputPaths(version, pub_slot, "video.mov").review_video_path(),
                             rc_preview= OutputPaths(version, pub_slot, "video.mov").preview_video_path(),
                             template= OutputPaths().used_template_path(),
                             work_file= OutputPaths(version, "work_scene.ext").work_file_path(),
                             chain= OutputPaths().origin(),
                             bundle= bundle,
                             rc_output_path="_path"))

        published_slot = self.db[collection_name].insert_one(save_content)

        print("{0} slot {1} has been published".format(pub_slot, version))
        return published_slot.inserted_id, collection_name

    def db_publish(self):
        task_pub_slots = DbPubSlot().get_pub_slots()
        current_task = Envars().task_name

        main_publish = self.db_main_publish()
        for pub_slot in task_pub_slots:

            get_sync_path = ".".join(["sync_tasks", current_task, pub_slot])

            pub_slots_publish = self.db_slot_publish(pub_slot)

            DbReferences.add_db_id_reference(collection=main_publish[1],
                                      parent_doc_id=main_publish[0],
                                      destination_slot="publishing_slots",
                                      id_to_add=pub_slots_publish[0],
                                      from_collection=pub_slots_publish[1])

            DbReferences.add_db_id_reference(collection=DbProject().get_branch_type,
                                      parent_doc_id=DbIds.db_entry_id(),
                                      destination_slot=get_sync_path,
                                      id_to_add=pub_slots_publish[0],
                                      from_collection=pub_slots_publish[1],
                                      replace=True)

        return main_publish

    def db_publish_sel(self, sel_pub_slots=[]):
        current_task = Envars().task_name
        print (current_task)
        task_pub_slots = DbPubSlot().get_pub_slots()
        get_sync_tasks = DbSyncTasks().capture_all()
        print (get_sync_tasks)
        sync_to_curr_task = get_sync_tasks[current_task]
        print (sync_to_curr_task)

        if len(sel_pub_slots)==0:
            sel_pub_slots = task_pub_slots

        for sync_slot in sel_pub_slots:
             del sync_to_curr_task[sync_slot]

        main_publish = self.db_main_publish()

        for pub_slot in sel_pub_slots:

            get_sync_path = ".".join(["sync_tasks", current_task, pub_slot])

            pub_slots_publish = self.db_slot_publish(pub_slot)

            DbReferences.add_db_id_reference(collection=main_publish[1],
                                      parent_doc_id=main_publish[0],
                                      destination_slot="publishing_slots",
                                      id_to_add=pub_slots_publish[0],
                                      from_collection=pub_slots_publish[1])

            DbReferences.add_db_id_reference(collection=DbProject().get_branch_type,
                                      parent_doc_id=DbIds.db_entry_id(),
                                      destination_slot=get_sync_path,
                                      id_to_add=pub_slots_publish[0],
                                      from_collection=pub_slots_publish[1],
                                      replace=True)

        for inherited_slot in sync_to_curr_task.items():
            get_collection = inherited_slot[1].split(",")

            DbReferences.add_db_id_reference(collection=main_publish[1],
                                      parent_doc_id=main_publish[0],
                                      destination_slot="publishing_slots",
                                      id_to_add=get_collection[1],
                                      from_collection=get_collection[0])





        return main_publish

    def db_work_file_save(self, file_name):
        version = DBVersionControl().db_wip_files_version_increase("work_files")
        set_display_name = "_".join([Envars.entry_name,Envars.task_name, "work_file", version])

        common_id = DbIds.db_wip_file_id(version)
        collection_name = "work_files"

        save_content = dict(
            _id=common_id,
            show_name=Envars.show_name,
            entry_name=Envars.entry_name,
            category=Envars.category,
            branch=Envars.branch_name,
            task_name=Envars.task_name,
            status="WIP",
            description=[],
            artist=Users.get_current_user(),
            version=version,
            date=DateTime().return_date,
            time=DateTime().return_time,
            publish_packaging="wip_scene",
            display_name=set_display_name,
            origin=[],
            components=dict(main_path=OutputPaths(version, output_file_name=file_name).wip_file_path()),
            session=[]

        )

        published = self.db[collection_name].insert_one(save_content)

        print("{0} Saved!".format(set_display_name))
        return published.inserted_id, collection_name