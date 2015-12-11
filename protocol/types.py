__all__ = [
    "BooleanType",
    "IntegerType", "SignedIntegerType", "UnsignedIntegerType",
    "CustomIntegerType", "FloatType", "DoubleType",
    "BytesType", "TextType", "CustomTextType",
    "OptionalType",
    "StaticArrayType", "TupleType",
    "VectorType", "SetType", "MapType",
    "EnumType",
    "Field", "RecordType",
    "VariantType",

    "Bool",
    "Int8", "Int16", "Int32", "Int64",
    "UInt8", "UInt16", "UInt32", "UInt64",
    "Float", "Double",
    "Bytes", "Text",
]

class Type(object):
    def to_string(self):
        return NotImplementedError

    def __repr__(self):
        return self.to_string()

    def __str__(self):
        return self.to_string()

class PrimitiveType(Type):
    pass

class BooleanType(PrimitiveType):
    def to_string(self):
        return "Bool"

Bool = BooleanType()

#
# IntegerType
#

class IntegerType(PrimitiveType) :
    def __init__(self, bits, min_value, max_value) :
        self._bits = bits
        self._min_value = min_value
        self._max_value = max_value

    def bits(self) : return self._bits
    def min_value(self) : return self._min_value
    def max_value(self) : return self._max_value

class SignedIntegerType(IntegerType) :
    def __init__(self, bits) :
        v = 2 ** (bits - 1)
        min_value = -v
        max_value = v - 1
        super(SignedIntegerType, self).__init__(bits, min_value, max_value)

    def to_string(self) :
        return "Int%s" % (self.bits(),)

class UnsignedIntegerType(IntegerType) :
    def __init__(self, bits) :
        min_value = 0
        max_value = (2 ** bits) - 1
        super(UnsignedIntegerType, self).__init__(bits, min_value, max_value)

    def to_string(self) :
        return "UInt%s" % (self.bits(),)

Int8 = SignedIntegerType(8)
Int16 = SignedIntegerType(16)
Int32 = SignedIntegerType(32)
Int64 = SignedIntegerType(64)

UInt8 = UnsignedIntegerType(8)
UInt16 = UnsignedIntegerType(16)
UInt32 = UnsignedIntegerType(32)
UInt64 = UnsignedIntegerType(64)

class CustomIntegerType(IntegerType):
    def __init__(self, min_value, max_value) :
        assert(min_value <= max_value)
        super(CustomIntegerType, self).__init__(0, min_value, max_value)

    def to_string(self) :
        return "CustomInteger(%s, %s)" % (self.min_value(), self.max_value())


#
# FloatingPointType
#

class FloatingPointType(PrimitiveType) :
    pass

class FloatType(FloatingPointType) :
    def to_string(self) :
        return "Float"

class DoubleType(FloatingPointType) :
    def to_string(self) :
        return "Double"

Float = FloatType()
Double = DoubleType()


#
# BytesType, TextType
#

class BytesType(PrimitiveType) :
    def to_string(self) :
        return "Bytes"

class TextType(PrimitiveType) :
    def to_string(self) :
        return "Text"

Bytes = BytesType()
Text = TextType()

class CustomTextType(PrimitiveType) :
    def __init__(self, length):
        assert (length > 0)
        self._length = length

    def length(self): return self._length

    def to_string(self) :
        return "CustomText(%s)" % (self._length,)


#
# OptionalType
#

class OptionalType(Type) :
    def __init__(self, element_type) :
        self._element_type = element_type

    def element_type(self) : return self._element_type

    def to_string(self) :
        return "Optional(%s)" % (
            self._element_type.to_string(),
        )

#
# StaticArrayType, TupleType
#

class StaticArrayType(Type) :
    def __init__(self, element_type, size) :
        self._element_type = element_type
        self._size = size

    def element_type(self) : return self._element_type
    def size(self) : return self._size

    def to_string(self) :
        return "StaticArrayType(%s, %s)" % (
            self._element_type.to_string(),
            self._size
        )

class TupleType(Type) :
    def __init__(self, element_types) :
        self._element_types = element_types

    def element_types(self) : return self._element_types

    def to_string(self) :
        return "TupleType(%s)" % (
            ",".join([x.to_string() for x in self._element_types]),
        )


#
# VectorType, SetType, MapType
#

class VectorType(Type) :
    def __init__(self, element_type) :
        self._element_type = element_type

    def element_type(self) : return self._element_type

    def to_string(self) :
        return "VectorType(%s)" % (
            self._element_type.to_string(),
        )

class SetType(Type) :
    def __init__(self, element_type) :
        self._element_type = element_type

    def element_type(self) : return self._element_type

    def to_string(self) :
        return "SetType(%s)" % (
            self._element_type.to_string(),
        )

class MapType(Type) :
    def __init__(self, key_type, value_type) :
        self._key_type = key_type
        self._value_type = value_type

    def key_type(self) : return self._key_type
    def value_type(self) : return self._value_type

    def to_string(self) :
        return "MapType(%s, %s)" % (
            self._key_type.to_string(),
            self._value_type.to_string(),
        )


#
# NamedType
#

class NamedType(Type) :
    def __init__(self, name) :
        self._name = name

    def name(self) : return self._name


#
# EnumType
#

class EnumType(NamedType) :
    def __init__(self, name, value_names) :
        super(EnumType, self).__init__(name)
        self._value_names = value_names
        self._value_indices = {}
        for i, v in enumerate(self._value_names) :
            if not v[0].isupper() :
                msg = "enum values have to begin with an upper-case letter"
                assert False, msg
            self._value_indices[v] = i
            self.__dict__[v] = v

    def value_names(self) : return self._value_names
    def value_indices(self) : return self._value_indices

    def to_string(self) :
        return "Enum%s(%s)" % (
            self.name(),
            ",".join(self._value_names),
        )


#
# Field, RecordType
#

class Field(Type) :
    def __init__(self, name, type) :
        self._name = name
        self._type = type

    def name(self) : return self._name
    def type(self) : return self._type

    def to_string(self) :
        return "Field%s(%s)" % (
            self._name,
            self._type.to_string()
        )

class RecordType(NamedType) :
    def __init__(self, name, fields, base_class=None) :
        super(RecordType, self).__init__(name)
        self._fields = fields
        self._field_names = (x.name() for x in self._fields)
        self._base_class = base_class

    def fields(self) : return self._fields
    def field_names(self) : return self._field_names
    def base_class(self) : return self._base_class
    def set_base_class(self, base_class):
        self._base_class = base_class

    def to_string(self) :
        return "Record%s(%s)" % (
            self.name(),
            [x.to_string() for x in self._fields]
        )


#
# VariantType
#

class VariantType(NamedType) :
    def __init__(self, name, options) :
        super(VariantType, self).__init__(name)
        self._options = options
        for opt in options:
            opt.set_base_class(self)
        self._option_names = (x.name() for x in self._options)

    def options(self) : return self._options
    def option_names(self) : return self._option_names

    def to_string(self) :
        return "Variant%s(%s)" % (
            self.name(),
            ",".join([x.to_string() for x in self._options])
        )
