from protocol.api_key_validation import *
__all__ = [
    'bu_api_params'
]
statutory_mapping = "bulkupload.buapiprotocol.bustatutorymappingprotocol"
client_units = "bulkupload.buapiprotocol.buclientunitsprotocol"
bu_api_params = {
    'c_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'c_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet_withdot, 'is_optional': False},
    'd_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'd_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet_withdot, 'is_optional': False},
    'csv_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'csv_name': {'type': 'STRING', 'length': 100, 'validation_method': is_file_name, 'is_optional': False},
    'no_of_records': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'no_of_documents': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'uploaded_documents': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'csv_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': statutory_mapping, "class_name": "CsvList"},
    'upload_more': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},

    'doc_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'doc_names': {'type': 'VECTOR_TYPE_STRING', 'length': 1000, 'validation_method': is_file_name, 'is_optional': True},
    'total': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'valid': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'invalid': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'csv_data': {'type': 'TEXT', 'length': None , 'validation_method': None, 'is_optional': False},
    'csv_size': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'uploadby_name': {'type': 'TEXT', 'length': None , 'validation_method': None, 'is_optional': False},
    'mandatory_error': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'max_length_error': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'invalid_char_error': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'not_found_error': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'inactive_error': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'duplicate_error': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'invalid_data_error': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},

    'mandatory_failed': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'maxlength_failed': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'duplication_failed': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'specialchar_failed': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'invaliddata_failed': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'status_failed': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'invalid_file': {'type': 'STRING', 'length': 500, 'validation_method': is_file_name, 'is_optional': False},
    'rej_by': {'type': 'STRING', 'length': 100, 'validation_method': None, 'is_optional': False},
    'rej_on': {'type': 'STRING', 'length': 100, 'validation_method': None, 'is_optional': False},
    'rej_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'rej_file': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': False},
    'rej_reason': {'type': 'STRING', 'length': 500, 'validation_method': None, 'is_optional': False},
    'remove': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    'rejected_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': statutory_mapping, "class_name": "RejectedList"},
    'pwd': {'type': 'STRING', 'length': 100, 'validation_method': None, 'is_optional': False},
    'uploaded_by': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'uploaded_on': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': False},
    'action_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'approve_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},

    'download_file': {'type': 'STRING', 'length': 500, 'validation_method': is_file_name, 'is_optional': False},

    'pending_csv_list': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': statutory_mapping, "class_name": "PendingCsvList"},


    'orga_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': True},
    's_nature': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'geo_location': {'type': 'TEXT', 'length': None, 'validation_method': None, 'is_optional': True},
    'c_task_name': {'type': 'STRING', 'length': 100, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'c_desc': {'type': 'STRING', 'length': 500, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'c_doc': {'type': 'STRING', 'length': 100, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'sm_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'refer': {'type': 'STRING', 'length': 500, 'validation_method': is_url, 'is_optional': True},
    'statu_date': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': True},
    'statu_month': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': True},
    'trigger_before': {'type': 'TEXT', 'length': 100, 'validation_method': None, 'is_optional': True},

    'r_type': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet_wtih_bracket, 'is_optional': True},
    'r_by': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'dur': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'dur_type': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet_wtih_bracket, 'is_optional': True},
    'multiple_input': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'format_file': {'type': 'STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'bu_remarks': {'type': 'STRING', 'length': 500, 'validation_method': is_alphabet, 'is_optional': True},
    'bu_action': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},

    'mapping_data': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': statutory_mapping, "class_name": "MappingData"},

    'c_ids': {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'd_ids': {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'child_ids': {'type': 'VECTOR_TYPE_INT', 'length': None, 'validation_method': None, 'is_optional': False},

    'from_date': {'type': 'TEXT', 'length': 20, 'validation_method': None, 'is_optional': True},
    'to_date': {'type': 'TEXT', 'length': 20, 'validation_method': None, 'is_optional': True},
    'export': {'type': 'BOOL', 'length': None, 'validation_method': None, 'is_optional': False},
    'r_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'p_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},

    'reportdata': {'type': 'VECTOR_TYPE', 'length': None, 'validation_method': None, 'is_optional': False, 'module_name': statutory_mapping, "class_name": "ReportData"},
    'country_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'domain_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},

    'uploaded_on': {'type': 'TEXT', 'length': 20, 'validation_method': None, 'is_optional': True},


    'total_records': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'total_rejected_records': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'approved_by': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'rejected_by': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},

    'approved_on': {'type': 'TEXT', 'length': 20, 'validation_method': None, 'is_optional': True},
    'rejected_on': {'type': 'TEXT', 'length': 20, 'validation_method': None, 'is_optional': True},
    'is_fully_rejected': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'rejected_by': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'approve_status': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},

    'bu_client_id': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': True},
    'bu_group_name': {'type': 'STRING', 'length': 50, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'csv_size': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},

    'orga_names': {'type': 'VECTOR_TYPE_STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': True},
    's_natures': {'type': 'VECTOR_TYPE_STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'geo_locations': {'type': 'VECTOR_TYPE_STRING', 'length': 1000, 'validation_method': is_alphabet, 'is_optional': True},
    'c_tasks': {'type': 'VECTOR_TYPE_STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'c_descs': {'type': 'VECTOR_TYPE_STRING', 'length': 500, 'validation_method': is_alphabet, 'is_optional': True},
    'c_docs': {'type': 'VECTOR_TYPE_STRING', 'length': 100, 'validation_method': is_alphabet, 'is_optional': True},
    'bu_statutories': {'type': 'VECTOR_TYPE_STRING', 'length': 500, 'validation_method': is_alpha_numeric, 'is_optional': True},
    'frequencies': {'type': 'VECTOR_TYPE_STRING', 'length': 50, 'validation_method': is_alphabet, 'is_optional': True},

    'f_count': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},
    'r_range': {'type': 'INT', 'length': None, 'validation_method': None, 'is_optional': False},

    'task_id': {'type': 'STRING', 'length': 25, 'validation_method': is_alpha_numeric, 'is_optional': False},
    'task_type': {'type': 'STRING', 'length': 25, 'validation_method': is_alphabet, 'is_optional': False},
}
