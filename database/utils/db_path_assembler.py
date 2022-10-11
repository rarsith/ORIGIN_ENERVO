def make_path(*data, **kwargs):
    if data:
        id_elements = list()
        for elem in data:
            id_elements.append(elem)
        dotted_path = str(".".join(id_elements))
        return dotted_path
    return kwargs
