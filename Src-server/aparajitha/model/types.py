
__all__ = [
	"IntegerType", "UnsignedIntegerType",
	"FloatType", "UnsignedFloatType",
	"BoolType",
	"TextType",
	"VariantType",
	"DictType", "ListType", "SetType",
	"EnumType", "OptionalType"
]


#
# IntegerType, UnsignedIntegerType
#

class IntegerType(object):
	def __init__(self, bytes):
		self.range = 2 ** (bytes * 8)
		self.max_value = self.range / 2
		self.min_value = -((self.range / 2) - 1)

	def validate(self, v):
		if not isinstance(v, int) :
			raise TypeError("expecting int but received %s" % (v,))
		if (v < self.min_value) or (v > self.max_value) :
			raise ValueError("value out of range")
		return True

class UnsignedIntegerType(object):
	def __init__(self, bytes):
		self.range = 2 ** (bytes * 8)
		self.max_value = self.range
		self.min_value = 0

	def validate(self, v):
		if not isinstance(v, int) :
			raise TypeError("expecting int but received %s" % (v,))
		if (v < self.min_value) or (v > self.max_value) :
			raise ValueError("value out of range")
		return True


#
# FloatType, UnsignedFloatType
#

class FloatType(object):
	def __init__(self, bytes):
		self.range = 2 ** (bytes * 8)
		self.max_value = self.range / 2
		self.min_value = -((self.range / 2) - 1)

	def validate(self, v):
		if not isinstance(v, int) and not isinstance(v, float) :
			raise TypeError("expecting float but received %s" % (v,))
		if (v < self.min_value) or (v > self.max_value) :
			raise ValueError("value out of range")
		return True

class UnsignedFloatType(object):
	def __init__(self, bytes):
		self.range = 2 ** (bytes * 8)
		self.max_value = self.range
		self.min_value = 0

	def validate(self, v):
		if not isinstance(v, int) and not isinstance(v, float) :
			raise TypeError("expecting float but received %s" % (v,))
		if (v < self.min_value) or (v > self.max_value) :
			raise ValueError("value out of range")
		return True


#
# BoolType
#

class BoolType(object):
	def __init__(self):
		pass

	def validate(self, v):
		if not isinstance(v, int) :
			raise ValueError("expecting boolean (0, 1) but received %s" % (v,))
		if not v in (0, 1):
			raise ValueError("expecting boolean (0, 1) but received %s" % (v,))
		return True


#
# TextType
#

class TextType(object):
	def __init__(self, length=None):
		self.length = length

	def validate(self, v):
		if not isinstance(v, str) and not isinstance(v, unicode):
			raise TypeError("expecting string but received %s" % (v,))
		if self.length is not None :
			if not len(v) <= self.length:
				raise ValueError("too long")
		return True


#
# VariantType
#

class VariantType(object):
	def __init__(self, name, fields):
		self.name = name
		self.fields = fields
		self.options = None
		self.set_options(fields)

	def set_options(self, fields):
		assert self.options is None
		self.options = []
		for k in fields._keys() :
			self.options.append(k)

	def validate(self, value):
		if not value[0] in self.options :
			raise ValueError("request: %s not found" % (value[0],))
		value2 = self.fields[value[0]]
		if not type(value2) in type_map[type(value[1])]:
			raise TypeError("expecting dictionary but received %s" % (value2,))
		return True

	def get_options(self) :
		return self.options

	def get(self, name) :
		return self.fields[name]


#
# DictType
#

class DictType(object):
	def __init__(self, fields):
		self.fields = fields

	def validate(self, value):
		def match_type(_type, _value) :
			if not type(_type) in type_map[type(_value)] :
				msg = "expecting type %s but received %s" % (_type, value[_key])
				raise TypeError(msg)
			return True

		if not isinstance(value, dict) :
			raise TypeError("%s not a dictionary" % (value,))

		for _key, _type in self.fields.items():
			if not _key in value.keys() :
				raise ValueError("key: %s not found" % (_key,))
			if type(_type) == OptionalType :
				if value[_key] is None :
					continue
				if match_type(_type._field_type(), value[_key]) :
					continue
			else :
				if match_type(_type, value[_key]) :
					continue
		return True

	def _keys(self):
		return self.fields.keys()

	def _items(self):
		return self.fields.items()

	def _display(self) :
		return self.fields

	def __getitem__(self, key):
		return self.fields[key]


#
# ListType
#

class ListType(object):
	def __init__(self, field_type):
		self.field_type = field_type

	def _field_type(self):
		return self.field_type

	def validate(self, v):
		if not isinstance(v, list) :
			raise TypeError("not a list")
		return True


#
# SetType
#

class SetType(object):
	def __init__(self, field_type):
		self.field_type = field_type

	def _field_type(self):
		return self.field_type

	def validate(self, v):
		if not isinstance(v, set) :
			raise TypeError("not a set")
		return True


#
# EnumType
#

class EnumType(object):
	def __init__(self, name, values):
		self.name = name
		self.values = values

	def validate(self, v) :
		if not isinstance(v, str) and not isinstance(v, unicode):
			raise TypeError("expecting string but received %s" % (v,))
		if not v in self.values :
			msg = "expecting one of %s" % (self.values)
			raise ValueError(msg)
		return True


#
# OptionalType
#

class OptionalType(object):
	def __init__(self, field_type):
		self.field_type = field_type

	def _field_type(self):
		return self.field_type


type_map = {
	list: (VariantType, ListType, SetType),
	str: (TextType, EnumType),
	unicode: (TextType, EnumType),
	int: (IntegerType, UnsignedIntegerType, BoolType),
	float: (FloatType, UnsignedFloatType),
	dict: (DictType,)
}

