class Tasks(object):

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


class Branch(object):
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


class Entity(object):

    @classmethod
    def build(cls):
        return "build"

    @classmethod
    def shot(cls):
        return "shots"


if __name__ == "__main__":
    x = Branch.sequences()
    print (x)