class BaseCommand(object):
    def __init__(self):
        self._cluster = False

    def execute(self, *args, **kwargs):
        raise NotImplementedError
