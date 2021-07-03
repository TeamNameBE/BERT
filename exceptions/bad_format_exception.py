class BadFormatException(Exception):
    """An exception occuring in case the argument does not have the wanted format"""

    def __init__(self, msg):
        self.msg = msg
        super().__init__()

    def __repr__(self):
        return self.msg

    def __str__(self):
        return self.__repr__()
