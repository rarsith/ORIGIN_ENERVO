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
    def sync_tasks(cls):
        return 'sync_tasks'

    @classmethod
    def wip(cls):
        return 'wip_scenes'

if __name__ == '__main__':
    c = DbCollections.main_publishes()
    print (c)