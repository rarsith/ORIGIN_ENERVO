class BranchTypes(object):
    @classmethod
    def build(cls):
        return "build"

    @classmethod
    def sequences(cls):
        return "shots"

    @classmethod
    def library(cls):
        return 'lib_asset'

    @classmethod
    def reference(cls):
        return 'ref_asset'


class CategoryTypes(object):
    @classmethod
    def characters(cls):
        return "characters"

    @classmethod
    def props(cls):
        return "props"

    @classmethod
    def environments(cls):
        return 'environments'


class EntityTypes(object):

    @classmethod
    def build(cls):
        return "build"

    @classmethod
    def shot(cls):
        return "shots"


class TaskTypes(object):

    @classmethod
    def characters(cls):
        return "character"

    @classmethod
    def props(cls):
        return 'prop'

    @classmethod
    def environments(cls):
        return 'environment'

    @classmethod
    def shots(cls):
        return 'shot'



if __name__ == "__main__":
    x = BranchTypes.sequences()
    print (x)