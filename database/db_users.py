from database import db_connection as mdbconn
from database.db_ids import DbIds
from database.db_paths import DbPaths
from database.entities.db_project import DbProject
from envars.envars import Envars
from common_utils.date_time import DateTime


class DbUsers(object):
    def __init__(self):
        self.db = mdbconn.server.xchange

    def create_user(self, first_name, name, personal_email, job_title, access_level):
        self.db.users.insert_one(
            {
                "first_name": first_name,
                "name": name,
                "active": True,
                "access_type":access_level,
                "personal_email": personal_email,
                "job_title": job_title,
                "user_name": {},
                "internal_email": {},
                "date": DateTime().return_date,
                "time": DateTime().return_time
            }
        )
        print(" user for {} created!".format(first_name + " " + name))
        pass

    def get_user(self):
        try:
            task_path = DbPaths.origin_path("tasks", Envars.task_name, "artist")
            cursor = self.db[DbProject().get_branch_type]
            tasks_list = cursor.find({"_id": DbIds.db_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]['artist']

        except:
            pass
