from envars.envars import Envars
from common_utils.users import Users
from common_utils.date_time import DateTime
from database.db_versions_control import DBVersionControl



class DbAttributes(object):

    @classmethod
    def show_name(cls):
        return Envars.show_name

    @classmethod
    def branch_name(cls):
        return Envars.branch_name

    @classmethod
    def category(cls):
        return Envars.category

    @classmethod
    def entry_name(cls):
        return Envars.entry_name

    @classmethod
    def artist(cls):
        return Users.get_current_user()

    @classmethod
    def date(cls):
        return DateTime().return_date

    @classmethod
    def time(cls):
        return DateTime().return_time

    @classmethod
    def version(cls):
        return DBVersionControl().db_master_bundle_ver_increase()


if __name__ == '__main__':
    Envars.entry_name="hulk"
    c = DbAttributes.entry_name()
    print (c)


