from database.entities.db_project import DbProject
from database.entities.db_asset import DbAsset
from database.entities.db_bundle import DbBundle
from database.entities.properties.db_pub_slot import DbPubSlot
from database.entities.properties.db_sync_tasks import DbSyncTasks
from database.entities.properties.db_tasks import DbTasks
from database.publishing.db_publish import DbPublish
from database.db_types import Branch, Tasks

from envars.envars import Envars

existing_modeling_pub_slots = ['rend_geo', 'proxy_geo', 'utility', 'lidar', 'proj_geo', 'vport_mat', 'tex_object', 'curvature_map', 'ao_map', 'selection_map']

Envars.show_name = "Test"
Envars.branch_name = "assets"
Envars.category = "characters"
Envars.entry_name = "hulk"
Envars.task_name = "modeling"

print(Envars().show_name, Envars().branch_name, Envars().category, Envars().entry_name, Envars().task_name)

project = DbProject()
assets = DbAsset()
publish = DbPublish()


# CREATORS
# project.create("Test")
# project.add_branch(name="references", branch_type=Branch.reference())
# project.add_category(name="grass`", tasks_type=Tasks.props())

# assets.create(name="hulk")
# publish.db_publish_sel(sel_pub_slots=["rend_geo", "proxy_geo"])
publish.db_work_file_save(file_name="cache.abc")

# PROJECT METHODS
project_type = project.get_project_type()
print(project_type)
branch_type = project.get_branch_type
print (branch_type)
project_struct = project.get_structure()
print (project_struct)

proj_branches=project.get_branches()
print (proj_branches)
branch_categories = project.get_categories(branch=Envars().branch_name)
print (branch_categories)
assets_names = project.get_entities_names(Envars().branch_name, Envars().category)
print(assets_names)

# ASSET METHODS
asset_type = assets.get_entry_type()
print (asset_type)
asset_definition=assets.get_definition()
print (asset_definition[0])
asset_is_active=assets.set_active(is_active=True)
print (asset_is_active)





