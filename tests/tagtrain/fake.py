class Author(object):
    name = None

    def __init__(self, name):
        self.name = name


class Message(object):
    body = None
    author = None

    def __init__(self, body, name):
        self.body = body
        self.author = Author(name)


def create(body, name):
    return Message(body, name)
