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

    'total': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'valid': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'invalid': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'csv_data': {'type': 'TEXT', 'length': None , 'validation_method': None, 'is_optional': False},

    'mandatory_failed': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'maxlength_failed': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'duplication_failed': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'specialchar_failed': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'invaliddata_failed': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'status_failed': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'invalid_file': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': False},
    'rej_by': {'type': 'STRING', 'length': 100, 'validation_method': None, 'is_optional': False},
    'rej_on': {'type': 'STRING', 'length': 100, 'validation_method': None, 'is_optional': False},
    'rej_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'rej_file': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': False},
    'rej_reason': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': False},
    'remove': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    'rejected_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': statutory_mapping, "class_name": "RejectedList"},
    'pwd': {'type': 'STRING', 'length': 100, 'validation_method': None, 'is_optional': False},
    'uploaded_by': {'type': 'STRING', 'length': 100, 'validation_method': None, 'is_optional': False},
    'uploaded_on': {'type': 'STRING', 'length': 100, 'validation_method': None, 'is_optional': False},
    'action_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'download_file': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': False},

    'pending_csv_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': statutory_mapping, "class_name": "PendingCsvList"},

    'org': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    's_nature': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'geo_location': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'c_task_name': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'c_desc': {'type': 'STRING', 'length': 500, 'validation_method': is_alphabet, 'is_optional': True},
    'c_doc': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'sm_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'refer': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': True},
    'statu_date': {'type': 'STRING', 'length': 100, 'validation_method': None, 'is_optional': True},
    'statu_month': {'type': 'STRING', 'length': 100, 'validation_method': None, 'is_optional': True},
    'trigger_before': {'type': 'STRING', 'length': 100, 'validation_method': None, 'is_optional': True},

    'r_type': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'r_by': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'dur': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'dur_type': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'multiple_input': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'format_file': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'bu_remarks': {'type': 'STRING', 'length': 500, 'validation_method': is_alphabet, 'is_optional': True},
    'bu_action': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},

    'mapping_data': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': statutory_mapping, "class_name": "PendingCsvList"},

}
