def make_path(*data, **kwargs):
    if data:
        dotted_path = str(".".join(data))
        return dotted_path
    return kwargs

