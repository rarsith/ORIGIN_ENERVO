class DbAttributes(object):

    @classmethod
    def show_name(cls):
        return "show_name"

    @classmethod
    def branch(cls):
        return 'branch'

    @classmethod
    def category(cls):
        return 'category'

    @classmethod
    def entry_name(cls):
        return 'entry_name'

    @classmethod
    def task_sync(cls):
        return 'task_sync'

    @classmethod
    def wip(cls):
        return 'wip_scenes'

if __name__ == '__main__':
    c = DbAttributes.show_name()
    print (c)


