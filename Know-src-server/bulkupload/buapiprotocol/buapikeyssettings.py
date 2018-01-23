from protocol.api_key_validation import *
__all__ = [
    'bu_api_params'
]
statutory_mapping = "bulkupload.buapiprotocol.bustatutorymappingprotocol"
bu_api_params = {
    'c_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'c_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet_withdot, 'is_optional': False},
    'd_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'd_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet_withdot, 'is_optional': False},
    'csv_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'csv_name': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet_withdot, 'is_optional': False},
    'no_of_records': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'no_of_documents': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'uploaded_documents': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'csv_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': statutory_mapping, "class_name": "CsvList"},
    'upload_more': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
}
