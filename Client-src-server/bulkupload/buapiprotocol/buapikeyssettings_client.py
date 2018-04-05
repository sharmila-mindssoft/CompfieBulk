# from clientprotocol.api_key_validation import (
#     is_alphabet_withdot, is_file_name, is_alphabet, is_alpha_numeric,
#     is_alphabet_wtih_bracket, is_numeric, is_url, is_address,
#     is_alphabet_csv_delimeter
# )

__all__ = [
    'bu_api_params'
]

from clientprotocol.api_key_validation_client import *

completed_task = "bulkupload.buapiprotocol.bucompletedtaskcurrentyearprotocol"

def make_int_field(length=None, is_optional=False):
    return {'type': 'INT', 'length': length, 'is_optional': is_optional}

def make_string_field(length=100, is_optional=False, validfun=allow_specialchar):
    return {'type': 'STRING', 'length': length , 'validation_method': validfun, 'is_optional': is_optional}

def make_text_field(length=100, is_optional=False):
    return {'type': 'TEXT', 'length': length , 'is_optional': is_optional}

def make_vector_type_field(module, klass_name, is_optional=False):
    return {'type': 'VECTOR_TYPE', 'is_optional': is_optional, 'module_name': module, "class_name": klass_name}

def make_vector_type_int(length=None, is_optional=False):
    return {'type': 'VECTOR_TYPE_INT', 'length': length, 'is_optional': is_optional}

def make_vector_type_string(length=100, is_optional=False, validfun=allow_specialchar):
    return {'type': 'VECTOR_TYPE_STRING', 'length': length, 'is_optional': is_optional, 'validation_method': validfun}

def make_vector_type_text(length=None, is_optional=False, validfun=allow_specialchar):
    return {'type': 'VECTOR_TYPE_TEXT', 'length': length, 'is_optional': is_optional, 'validation_method': validfun}

def make_bool_field(is_optional=False):
    return {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': is_optional}

def make_enum_type(module, klass_name):
    return {'type': 'ENUM_TYPE', 'module_name': module, 'class_name': klass_name}

def make_map_type(module, klass_name, validfun=is_numeric, is_optional=False):
    return {'type': 'MAP_TYPE', 'validation_method': validfun, 'is_optional': is_optional, 'module_name': module, "class_name": klass_name}

def make_map_type_vector_type(module, klass_name, length=50, validfun=allow_specialchar):
    return {'type': 'MAP_TYPE_VECTOR_TYPE', 'length': length, 'validation_method': validfun, 'is_optional': False, 'module_name': module, "class_name": klass_name}

def make_map_type_vector_type_string(length=150, is_optional=False):
    return {'type': 'MAP_TYPE_VECTOR_TYPE_STRING', 'is_optional': is_optional, 'length': length}

def make_widget_type():
    # customized widget data from backend
    return {'type': 'WIDGET_TYPE'}

def make_record_type(module, klass_name):
    return {'type': 'RECORD_TYPE', 'module_name': module, 'class_name': klass_name}

bu_api_params = {
    'csv_name': make_text_field(length=250),
    'csv_data': make_text_field(length=None),
    'csv_size': make_int_field(),
    'mandatory_error': make_int_field(),
    'max_length_error': make_int_field(),
    'duplicate_error': make_int_field(),
    'invalid_char_error': make_int_field(),
    'invalid_data_error': make_int_field(),
    'inactive_error': make_int_field(),
    'invalid_file': make_text_field(length=250),
    'valid': make_int_field(),
    'invalid': make_int_field(),
    'new_csv_id': make_int_field(),
}