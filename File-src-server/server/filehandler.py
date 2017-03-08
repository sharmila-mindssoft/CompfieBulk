
FILE_MAX_LIMIT = 1020 * 1024 * 50  # 50 MB
CLIENT_DOCS_BASE_PATH = os.path.join(ROOT_PATH, "clientdocuments")

def upload_file(request) :
    client_id = request.client_id
    legal_entity_id = request.legal_entity_id
    country_id = request.country_id
    domain_id = request.domain_id
    unit_id = request.unit_id
    start_date = request.start_date
    file_content = request.file_content
    file_name = request.file_name

    file_info = file_name.split('.')
    if len(file_info) == 1 or len(file_info) > 2 :
        raise ValueError("Invalid File")

    elif len(file_content) == 0:
        raise ValueError("File cannot be empty")

    elif len(file_content) > FILE_MAX_LIMIT :
        raise ValueError("Faile max limit exceeded")

    make_path = "%s/%s/%s/%s/%s/"
