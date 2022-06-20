from database.entities.db_project import DbProject
from database.entities.db_asset import DbAsset
from database.entities.db_bundle import DbBundle
from database.entities.db_properties import DbPubSlot
from database.entities.db_structures import DbProjectBranch
from database.entities.properties.db_asset_categories import DbAssetCategories
from database.entities.properties.db_sync_tasks import DbSyncTasks
from database.entities.properties.db_tasks import DbTasks
from database.publishing.db_publish import DbPublish
from envars.envars import Envars

existing_modeling_pub_slots = ['rend_geo', 'proxy_geo', 'utility', 'lidar', 'proj_geo', 'vport_mat', 'tex_object', 'curvature_map', 'ao_map', 'selection_map']

Envars.show_name = "Test"
Envars.branch_name = "assets"
Envars.category = "characters"
Envars.entry_name = "hulk"
Envars.task_name = "surfacing"

#print(Envars().show_name, Envars().branch_name, Envars().category, Envars().entry_name, Envars().task_name)


# OBJECTS
project = DbProject()
assets = DbAsset()
tasks = DbTasks()
sync_tasks = DbSyncTasks()
pub_slot = DbPubSlot()
publish = DbPublish()
bundle = DbBundle()



# SWITHCHES
test_project = False
test_assets = False
test_tasks = False
test_sync_tasks = False
test_pub_slot = False
test_publish = True
test_bundle = False


# PROJECT METHODS
if test_project:
    project.create("Green")
    # DbProjectBranch().add_branch(name="references", branch_type=Branch.reference())
    # DbAssetCategories().add_category(name="grass`", tasks_type=Tasks.props())
    project_type = project.get_type()
    branch_type = DbProjectBranch().get_type
    project_struct = DbProjectBranch().get_structure()
    # print(project_type)
    # print (branch_type, "<<")
    # print (project_struct)

    proj_branches=DbProjectBranch().get_branches()
    branch_categories = DbAssetCategories().get_categories()
    # assets_names = project.get_entities_names()
    # print (proj_branches)
    # print (branch_categories)
    print(assets_names)

# ASSET METHODS
if test_assets:
    assets_list = ["red_hulk", "blue_hulk", "yellow_hulk"]
    for asset in assets_list:
        assets.create(name=asset)
    asset_type = assets.get_entry_type()
    asset_definition=assets.get_definition()
    asset_is_active=assets.set_active(is_active=True)
    print (asset_type)
    print (asset_definition[0])
    print (asset_is_active)


# TASKS METHODS
if test_tasks:
    # tasks.create("painting")
    tasks_asset = tasks.get_tasks()
    full_tasks_asset = tasks.get_tasks_full()
    tasks_imp_from = tasks.get_imports_from()
    task_status=tasks.get_status()
    task_active=tasks.get_is_active()
    tasks.set_is_active(is_active=True)
    print (task_active)
    print (task_status)
    print (tasks_imp_from)
    print(tasks_asset)
    print(full_tasks_asset)

if test_publish:

    publish.db_publish_sel()
    # publish.db_work_file_save(file_name="cache.abc")
    pass

# BUNDLES METHODS

if test_bundle:
    # bundle.create_stream("BUBU")
    bundle.create()
    pass