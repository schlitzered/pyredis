class Subscribe(object):
    """Mixin for Redis subscription client commands (e.g. SUBSCRIBE, UNSUBSCRIBE)."""

    def write(self, *args):
        raise NotImplementedError

    def psubscribe(self, *args):
        return self.write(
            *[b"PSUBSCRIBE", *args]
        )

    def punsubscribe(self, *args):
        return self.write(
            *[b"PUNSUBSCRIBE", *args]
        )

    def subscribe(self, *args):
        return self.write(
            *[b"SUBSCRIBE", *args]
        )

    def unsubscribe(self, *args):
        return self.write(
            *[b"UNSUBSCRIBE", *args]
        )
