import getpass

class Users(object):

    @staticmethod
    def get_current_user():
        username = getpass.getuser()
        return username