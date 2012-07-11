class BaseTransport(object):
    """
    Base class that implements shared methods between various transports.
    """

    def __init__(self, host, port, handler, *args, **kwargs):
        super(BaseTransport, self).__init__(*args, **kwargs)

        self.host = host
        self.port = port
        self.handler = handler

    def request(self, body):
        raise NotImplementedError
