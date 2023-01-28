import re
import os


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


def next_file_version(path_to_query, delimiter="_"):
    all_versions = []
    for dir_path, dir_names, file_names in os.walk(path_to_query):
        for file_name in file_names:
            get_file_name = file_name.split(".")[0]
            get_file_version = get_file_name.split(delimiter)[-1]
            all_versions.append(get_file_version)

    next_version = version_increment(all_versions)

    return next_version


if __name__ == "__main__":
    v = next_file_version("D:\\projects\\Origin_Tasks_Templates\\characters")
    print (v)