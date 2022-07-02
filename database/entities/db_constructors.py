from envars.envars import Envars
from database.db_attributes import DbId
from database import db_templates
from common_utils.users import Users
from database.db_statuses import DbStatuses
from database.db_defaults import DbDefaults
from common_utils.date_time import DateTime
from database.utils.db_version_control import DBVersionControl
from database.entities.db_properties import DbProjectBranch, DbSyncTasks, DbTasks


class DbProjectCode:
    """Generates a unique code for the project"""
    data: str

    def __init__(self, data):
        self.data = data

    def code(self) -> str:
        addition = "this is a code" # TODO: build a code generator
        return self.data+"-"+addition


class DbConstructors(object):

    @staticmethod
    def project_construct(name, entity_id, project_type="vfx"):
        entity_attributes = dict(
            _id=entity_id,
            show_code=DbProjectCode(data=name).code(),
            entry_name=name,
            structure=db_templates.show_structure(),
            show_defaults=dict(asset_definition=db_templates.entry_definition("build"),
                               shots_definition=db_templates.entry_definition("shot"),
                               characters_tasks=db_templates.tasks_schema("character"),
                               props_tasks=db_templates.tasks_schema("prop"),
                               environments_tasks=db_templates.tasks_schema("environment"),
                               characters_definition=db_templates.entry_definition("build"),
                               props_definition=db_templates.entry_definition("build"),
                               environments_definition=db_templates.entry_definition("build"),
                               shots_tasks=db_templates.tasks_schema("shot")),
            active=True,
            date=DateTime().return_date,
            time=DateTime().return_time,
            owner=Users.get_current_user(),
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
            sync_tasks=DbSyncTasks().create_from_template(),
            master_bundle=dict(main_stream=[]),
            active=True,
            definition=DbDefaults().get_show_defaults(DbDefaults().root_definitions),
            date=DateTime().return_date,
            time=DateTime().return_time,
            owner=Users.get_current_user()
        )
        return entity_id, entity_attributes

    @staticmethod
    def work_session_construct(self):
        pass

    @staticmethod
    def bundle_construct():
        status = DbStatuses.pending_rev
        entity_tasks = DbTasks().get_tasks()
        version = DBVersionControl().db_master_bundle_ver_increase()
        common_id = DbId.get_master_bundle_id(version)
        set_display_name = "_".join([Envars.entry_name, "bundle", version])

        entity_attributes = dict(
            _id=common_id,
            show_name=Envars.show_name,
            branch_name=Envars.branch_name,
            category=Envars.category,
            entry_name=Envars.entry_name,
            display_name=set_display_name,
            artist=Users.get_current_user(),
            status=status,
            version=version,
            date=DateTime().return_date,
            time=DateTime().return_time,
            master_bundle=dict.fromkeys(entity_tasks, [])
        )
        return common_id, entity_attributes
