from sets import Set
from basics.types import (
    BooleanType, SignedIntegerType, UnsignedIntegerType,
    CustomIntegerType, FloatType, DoubleType,
    BytesType, TextType, CustomTextType, OptionalType,
    StaticArrayType, TupleType, VectorType, SetType,
    MapType, EnumType, RecordType, VariantType
)


class Module(object):
    def __init__(
        self, module, module_name
    ):
        self._module = module
        self._module_name = module_name
        self._classes = []
        self._structures = Set()
        assert(len(module.__all__) > 0)
        for x in module.__all__:
            cls = getattr(module, x)
            if type(cls) in (
                EnumType, RecordType
            ):
                self._classes.append(cls)
            elif type(cls) is VariantType:
                self._classes.append(cls)
                for option in cls.options():
                    self._classes.append(option)
            else:
                msg = "Invalid type found in __all__: %s" % (
                    cls
                )
                assert False, msg
        self._initialize_structures()

    def module_name(self):
        return self._module_name

    def is_cls_found(self, cls):
        if cls in self._classes:
            return True
        else:
            return False

    def _get_structures(
        self, t
    ):
        cls_type = type(t)
        if cls_type in (
            BooleanType,
            SignedIntegerType, UnsignedIntegerType,
            CustomIntegerType, FloatType, DoubleType,
            BytesType, TextType, CustomTextType
        ):
            pass
        elif cls_type in (
            OptionalType, StaticArrayType,
            VectorType, SetType
        ):
            self._get_structures(
                t.element_type()
            )
        elif cls_type is TupleType:
            for x in t.element_types():
                self._get_structures(
                    x
                )
        elif cls_type is MapType:
            self._get_structures(
                t.key_type()
            )
            self._get_structures(
                t.value_type()
            )
        elif cls_type is EnumType:
            self._structures.add(t)
        elif cls_type is RecordType:
            self._structures.add(t)
            for field in t.fields():
                self._get_structures(
                    field.type()
                )
        elif cls_type is VariantType:
            self._structures.add(t)
            for option in t.options():
                self._get_structures(
                    option
                )
        else:
            msg = "invalid type: %s" % (cls_type,)
            assert False, msg


    def _initialize_structures(self):
        for t in self._classes:
            self._get_structures(t)

    def structures(self):
        return self._structures
