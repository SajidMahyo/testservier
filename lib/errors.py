from distutils.log import error


class SchemaNotMatchingData(Exception):
    pass

class UnknownType(Exception):
    pass

class NotHandledFileExtension(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"\"{self.message}\" is not a handeled file type"