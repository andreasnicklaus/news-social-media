from . import nyt


def get_all():
    return [nyt.get_most_popular()]


def get_one():
    return nyt.get_most_popular()
