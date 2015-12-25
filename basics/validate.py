from sets import Set
from types import (
    RecordType, EnumType, VariantType
)

class Validate(object):
    def __init__(self, modules):
        assert(len(modules) > 0)
        self._modules = modules
        self._modules.sort(key=lambda m: m.module_name())
        self._structures = []
        temp = Set()
        for module in self._modules:
            temp = temp.union(
                module.structures()
            )
        for t in temp:
            if type(t) in (
                RecordType, VariantType,  EnumType
            ):
                self._structures.append(t)
        assert len(self._structures) > 0
        self._structures.sort(key=lambda s: s.name())

    def _verify_type_names(self, defs) :
        for k, v in defs.iteritems() :
            if type(v) in (RecordType, VariantType,  EnumType) :
                if k != v.name() :
                    assert False, "name mismatch: %s, %s" % (k, v.name())

    def _is_type_found_in_all(self, t):
        for module in self._modules:
            if module.is_cls_found(t):
                return module.module_name()
        assert False, "module not found: %s" % (t,)

    def validate(self, globals):
        self._verify_type_names(globals)
        for t in self._structures:
            self._is_type_found_in_all(t)
