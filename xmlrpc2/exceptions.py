class Fault(Exception):

    def __init__(self, msg, code=None, *args, **kwargs):
        super(Fault, self).__init__(*[msg] + list(args), **kwargs)

        self.code = code
