from aparajitha.model.types import *

__all__ = [
	"TinyInt",
	"SmallInt",
	"MediumInt",
	"Int",
	"BigInt",
	"Text20",
	"Text50",
	"Text100",
	"Text250",
	"Text500",
	"LongText",
	"validate_data"
]


TinyInt = IntegerType(1)
SmallInt = IntegerType(2)
MediumInt = IntegerType(3)
Int = IntegerType(4)
BigInt = IntegerType(8)

Text20 = TextType(20)
Text50 = TextType(50)
Text100 = TextType(100)
Text250 = TextType(250)
Text500 = TextType(500)
LongText = TextType()


#
# parser
#

def validate_integer(f, v):
	return f.validate(v)

def validate_float(f, v):
	return f.validate(v)

def validate_boolean(f, v):
	return f.validate(v)

def validate_text(f, v):
	return f.validate(v)

def validate_variant(f, v):
	result = f.validate(v)
	return validate(f.get(v[0]), v[1])

def validate_dict(f, v):
	result = f.validate(v)
	if not result :
		return False
	for _key, _type in f._items():
		if not validate(_type, v[_key]) :
			return False
	return True

def validate_list(f, v):
	result = f.validate(v)
	if not result :
		return False
	_type = f._field_type()
	for x in v :
		if not validate(_type, x) :
			return False
	return True

def validate_set(f, v):
	result = f.validate(v)
	if not result :
		return False
	_type = f._field_type()
	for x in v :
		if not validate(_type, x) :
			return False
	return True

def validate_enum(f, v) :
	result = f.validate(v)
	if not result :
		return False
	return True

def validate_optional(f, v):
	if v is None :
		return True
	result = f._field_type().validate(v)
	if not result :
		return False
	return True

validator_map = {
	IntegerType: validate_integer,
	UnsignedIntegerType: validate_integer,
	FloatType: validate_float,
	UnsignedFloatType: validate_float,
	BoolType: validate_boolean,
	TextType: validate_text,
	VariantType: validate_variant,
	DictType: validate_dict,
	ListType: validate_list,
	SetType: validate_set,
	EnumType: validate_enum,
	OptionalType: validate_optional,
}

def validate(f, v):
	format_type = type(f)
	return validator_map[format_type](f, v)

def validate_data(f, v) :
	return validate(f, v)

def validate_request(f, v) :
	return validate(f, v)