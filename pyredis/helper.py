__author__ = 'schlitzer'


def dict_from_list(source):
    return dict(zip(*[iter(source)]*2))
