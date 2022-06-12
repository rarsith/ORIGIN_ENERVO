import os

class Envars():

    @property
    def os_root(self):
        return os.environ.get('ORIGIN_ROOT')

    @os_root.setter
    def os_root(self, root_path):
        os.environ.get['ORIGIN_ROOT'] = root_path

    @property
    def origin_id(self):
        return os.environ.get('ORIGIN_ID')

    @origin_id.setter
    def origin_id(self, origin_id):
        os.environ['ORIGIN_ID'] = origin_id

    @property
    def show_name(self):
        return os.environ.get('ORIGIN_PROJECT')

    @show_name.setter
    def show_name(self, project):
        os.environ['ORIGIN_PROJECT'] = project

    @property
    def branch_name(self):
        return os.environ.get('ORIGIN_PROJECT_BRANCH')

    @branch_name.setter
    def branch_name(self, branch):
        os.environ['ORIGIN_PROJECT_BRANCH'] = branch

    @property
    def category(self):
        return os.environ.get('ORIGIN_PROJECT_CATEGORY')

    @category.setter
    def category(self, category):
        os.environ['ORIGIN_PROJECT_CATEGORY'] = category

    @property
    def entry_name(self):
        return os.environ.get('ORIGIN_PROJECT_ENTITY')

    @entry_name.setter
    def entry_name(self, entity):
        os.environ['ORIGIN_PROJECT_ENTITY'] = entity

    @property
    def task_name(self):
        return os.environ.get('ORIGIN_ENTITY_TASK')

    @task_name.setter
    def task_name(self, task):
        os.environ['ORIGIN_ENTITY_TASK'] = task

    @property
    def build_current_master_bundle(self):
        return os.environ.get('ORIGIN_BUILD_MASTER')

    @build_current_master_bundle.setter
    def build_current_master_bundle(self, master_id):
        os.environ['ORIGIN_BUILD_MASTER'] = master_id

    @property
    def shot_current_master_bundle(self):
        return os.environ.get('ORIGIN_SHOT_MASTER')

    @shot_current_master_bundle.setter
    def shot_current_master_bundle(self, master_id):
        os.environ['ORIGIN_SHOT_MASTER'] = master_id

    @property
    def bundle_stream(self):
        return os.environ.get('ORIGIN_BUNDLE_STREAM')

    @bundle_stream.setter
    def bundle_stream(self, stream):
        os.environ['ORIGIN_BUNDLE_STREAM'] = stream

    def taget_path(self, *args):
        path = '.'.join(args)
        return path
