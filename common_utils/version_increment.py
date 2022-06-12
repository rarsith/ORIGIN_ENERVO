import re

def version_increment(versions_list=[]):
    if not len(versions_list) < 1:
        conv_to_int = []

        for versions in versions_list:
            conv_to_int.append(versions)

        highest = max(conv_to_int)
        get_digit = re.findall('\d+', highest)

        return "{0}{1:04d}".format("v", (int(get_digit[0]) + 1))

    else:
        return "{0}{1:04d}".format("v", (int(1)))