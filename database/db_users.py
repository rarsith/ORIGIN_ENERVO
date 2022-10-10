from database.entities.db_attributes import DbIds, DbEntitiesAttrPaths
from envars.envars import Envars
from common_utils.date_time import DateTime
from database import db_connection as mdbconn
from database.entities.db_structures import DbProjectBranch


class DbUsers(object):
    def __init__(self, first_name, last_name, personal_email, job_title, access_level):
        self.db = mdbconn.server.xchange
        self.main_domain = "origin.com"

        self.first_name = first_name
        self.last_name = last_name
        self.personal_email = personal_email
        self.job_title = job_title
        self.access_level = access_level


    def create_user(self):
        self.db.users.insert_one(
            {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "active": True,
                "access_type":self.access_level,
                "personal_email": self.personal_email,
                "job_title": self.job_title(),
                "user_name": self.user_internal(),
                "internal_email": self.user_company_email(),
                "date": DateTime().curr_date,
                "time": DateTime().curr_time
            }
        )
        print(" user for {} created!".format(self.first_name + " " + self.last_name))
        pass

    def user_company_email(self):
        pass

    def user_internal(self):
        pass

    def get_user(self):
        try:
            task_path = DbEntitiesAttrPaths.make_path("tasks", Envars.task_name, "artist")
            cursor = self.db[DbProjectBranch().get_type]
            tasks_list = cursor.find({"_id": DbIds.curr_entry_id()}, {'_id': 0, task_path: 1})
            for tasks in tasks_list:
                return tasks['tasks'][Envars.task_name]['artist']

        except:
            pass
