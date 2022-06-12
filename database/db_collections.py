class DbCollections(object):

    @classmethod
    def show(cls):
        return "show"

    @classmethod
    def main_publishes(cls):
        return 'publishes'

    @classmethod
    def bundles(cls):
        return 'bundles'

    @classmethod
    def task_sync(cls):
        return 'task_sync'

    @classmethod
    def wip(cls):
        return 'wip_scenes'

if __name__ == '__main__':
    c = DbCollections.main_publishes()
    print (c)