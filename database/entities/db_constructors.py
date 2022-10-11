from envars.envars import Envars
from database.entities.db_attributes import DbIds
from database.entities.db_structures import DbProjectBranch
from database import db_templates
from common_utils.users import Users
from database.db_statuses import DbStatuses
from database.db_defaults import DbDefaults
from common_utils.date_time import DateTime
from database.utils.db_version_control import DBVersionControl
from common_utils.output_paths import OutputPaths
from database.entities.db_properties import DbSyncTasksProperties, DbTasksProperties


class DbProjectCode:
    """Generates a unique code for the project"""
    data: str

    def __init__(self, data):
        self.data = data

    def code(self) -> str:
        addition = "this is a code" # TODO: build a code generator
        return self.data+"-"+addition


class DbConstructors(object):

    def project_defaults(self):
        proj_defaults = dict(asset_definition=db_templates.entry_definition("build"),
                             shots_definition=db_templates.entry_definition("shot"),
                             characters_tasks=db_templates.tasks_schema("character"),
                             props_tasks=db_templates.tasks_schema("prop"),
                             environments_tasks=db_templates.tasks_schema("environment"),
                             characters_definition=db_templates.entry_definition("build"),
                             props_definition=db_templates.entry_definition("build"),
                             environments_definition=db_templates.entry_definition("build"),
                             shots_tasks=db_templates.tasks_schema("shot"))

        return proj_defaults

    def project_construct(self, name, entity_id, project_type="vfx"):
        entity_attributes = dict(
            _id=entity_id,
            show_code=DbProjectCode(data=name).code(),
            entry_name=name,
            structure=db_templates.show_structure(),
            show_defaults=self.project_defaults(),
            active=True,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user(),
            show_type=project_type)

        return entity_id, entity_attributes

    @staticmethod
    def asset_construct(name, entity_id):
        entity_attributes = dict(
            _id=entity_id,
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name=name,
            type=DbProjectBranch().get_type,
            status=" ",
            assignment={},
            tasks=DbDefaults().get_show_defaults(DbDefaults().root_tasks)[0],
            sync_tasks=DbSyncTasksProperties().create_from_template(),
            master_bundle=dict(main_stream=[]),
            active=True,
            definition=DbDefaults().get_show_defaults(DbDefaults().root_definitions),
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user()
        )
        return entity_id, entity_attributes

    @staticmethod
    def work_session_construct(file_name):
        version = DBVersionControl().db_wip_files_version_increase("work_files")
        set_display_name = "_".join([Envars.entry_name, Envars.task_name, "work_file", version])
        common_id = DbIds.get_wip_file_id(version)

        save_content = dict(
            _id=common_id,
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name=Envars.entry_name,
            task_name=Envars.task_name,
            status="WIP",
            description=[],
            artist=Users.curr_user(),
            version=version,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            publish_packaging="wip_scene",
            display_name=set_display_name,
            origin=[],
            components=dict(main_path=OutputPaths(version, output_file_name=file_name).wip_file_path()),
            session=[]
        )

        return common_id, save_content
        pass

    @staticmethod
    def bundle_construct():
        status = DbStatuses.pending_rev
        entity_tasks = DbTasksProperties().get_tasks()
        version = DBVersionControl().db_master_bundle_ver_increase()
        common_id = DbIds.get_master_bundle_id(version)
        set_display_name = "_".join([Envars.entry_name, "bundle", version])

        entity_attributes = dict(
            _id=common_id,
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name=Envars.entry_name,
            display_name=set_display_name,
            artist=Users.curr_user(),
            status=status,
            version=version,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            master_bundle=dict.fromkeys(entity_tasks, [])
        )
        return common_id, entity_attributes

    @staticmethod
    def main_publish_construct():
        version = DBVersionControl().db_main_pub_ver_increase()
        set_display_name = "_".join([Envars.entry_name, "main_publish"])
        common_id = DbIds.get_main_pub_id(version)

        save_content = dict(
            _id=common_id,
            reviewable_component="insert_movie",
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name=Envars.entry_name,
            task_name=Envars.task_name,
            status="PENDING_REVIEW",
            description=[],
            artist=Users.curr_user(),
            version=version,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            publish_packaging="main",
            publishing_slots=[],
            display_name=set_display_name
        )

        return common_id, save_content

    @staticmethod
    def slot_publish_construct(pub_slot):
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

        common_id = DbIds.get_pub_slot_id(pub_slot, version)
        bundle = 'current_bundle'

        save_content = dict(
            _id=common_id,
            reviewable_component="insert_movie_path",
            slot_thumbnail="insert_thumbnail_path",
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name=Envars.entry_name,
            task_name=Envars.task_name,
            update_type="non-critical",
            artist=Users.curr_user(),
            slot_name=pub_slot,
            status="PENDING-REVIEW",
            version_origin="created",
            version=version,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            publish_packaging="slots",
            parent_collection=collection_name,
            display_name=set_display_name,
            output_path=build_server_path,
            components=dict(path=OutputPaths(version, pub_slot, "cache.abc").main_publish_path(),
                            rc_source_images=OutputPaths(version, pub_slot, "image.%04d.exr").original_images_path(),
                            rc_source_video=OutputPaths(version, pub_slot, "video.mov").review_video_path(),
                            rc_preview=OutputPaths(version, pub_slot, "video.mov").preview_video_path(),
                            template=OutputPaths().used_template_path(),
                            work_file=OutputPaths(version, "work_scene.ext").work_file_path(),
                            chain=OutputPaths().origin(),
                            bundle=bundle,
                            rc_output_path="_path"))

        return common_id, save_content

    @staticmethod
    def sync_tasks_capture_construct(current_syncs: dict):
        # TODO: cohesion check!!
        version = DBVersionControl().db_sync_tasks_ver_increase()
        entity_id = DbIds.get_sync_tasks_id(version)

        entity_attributes = dict(
            _id=entity_id,
            show_name=Envars.show_name,
            entry_name=Envars.entry_name,
            category=Envars.category,
            version=version,
            sync_tasks=current_syncs,
            date=DateTime().curr_date,
            time=DateTime().curr_time,
            owner=Users.curr_user()
        )
        return entity_id, entity_attributes
