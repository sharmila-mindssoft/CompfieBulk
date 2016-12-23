from protocol.jsonvalidators import (parse_dictionary, parse_static_list)

class Response(object):
    def to_structure(self):
        name = type(self).__name__
        inner = self.to_inner_structure()
        return [name, inner]

    def to_inner_structure(self):
        raise NotImplementedError

    @staticmethod
    def parse_structure(data):
        data = parse_static_list(data, 2)
        name, data = data
        if _Response_class_map.get(name) is None:
            msg = "invalid request: " + name
            raise ValueError(msg)
        return _Response_class_map[name].parse_inner_structure(data)

    @staticmethod
    def parse_inner_structure(data):
        raise NotImplementedError

class TransactionExists(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return TransactionExists()

    def to_inner_structure(self):
        return {
        }

class UploadFailed(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return UploadFailed()

    def to_inner_structure(self):
        return {
        }

class InvalidFile(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return InvalidFile()

    def to_inner_structure(self):
        return {
        }

class FileIsEmpty(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return FileIsEmpty()

    def to_inner_structure(self):
        return {
        }

class FileMaxLimitExceed(Response):
    def __init__(self):
        pass

    @staticmethod
    def parse_inner_structure(data):
        data = parse_dictionary(data)
        return FileMaxLimitExceed()

    def to_inner_structure(self):
        return {
        }

def _init_Response_class_map():
    classes = [
        TransactionExists, UploadFailed, InvalidFile, FileIsEmpty,
        FileMaxLimitExceed
    ]
    class_map = {}
    for c in classes:
        class_map[c.__name__] = c
    return class_map

_Response_class_map = _init_Response_class_map()
