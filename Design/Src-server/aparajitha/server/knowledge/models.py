from types import *
import json


__all__ = [
    "CMObject", "Domain",
]

def assertType (x, typeObject) :
    if type(x) is not typeObject :
        msg = "expected type %s, received invalid type  %s" % (typeObject, type(x))
        raise TypeError(msg)

class CMObject(object) :
    # def toStructure(self) :
    #   raise NotImplementedError()

    # def fromStructure(klass, data) :
    #   raise NotImplementedError()

    def toJSON(self) :
        data = self.toStructure()
        return json.dumps(data)
    @classmethod
    def fromJSON(klass, jsonData) :
        data = json.loads(jsonData)
        return klass.fromStructure(data)


class Domain(CMObject) :
    def __init__(self, domainId, domainName, isActive) :
        self.domainId = domainId
        self.domainName = domainName
        self.isActive = isActive
        self.verify()

    def verify(self) :
        assertType(self.domainId, IntType)
        assertType(self.domainName, StringType)
        assertType(self.isActive, IntType)

    def toStructure(self) :
        return {
            "domain_id": self.domainId,
            "domain_name": self.domainName,
            "is_active": self.isActive
        }

    @classmethod
    def fromStructure(klass, data) :
        domainId = data.get("domain_id")
        assertType(domainId, IntType)
        domainName = data.get("domain_name")
        assertType(domainName, StringType)
        isActive = data.get("is_active")
        assertType(isActive, IntType) 
        return klass(domainId, domainName, isActive)

    def __repr__(self) :
        return str(self.toStructure())

