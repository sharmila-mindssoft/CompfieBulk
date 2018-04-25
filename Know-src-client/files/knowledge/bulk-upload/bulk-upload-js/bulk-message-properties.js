
console.log(message.DisabledUser)

var bulkMessage = {
  "knowledge_executive_name_required": "KE Required",
  "download_files" : "File Downloaded Successfully !",
  "password_authentication_success":"Authentication Success",
  "record_deleted":"Record Removed Successfully",
  "upload_csv": "File Required",
  "upload_success": "CSV file uploaded successfully",
  "approve_success": "CSV file approved successfully",
  "reject_success": "CSV file rejected successfully",
  "invalid_file": "Invalid file ",
  'client_group_required': 'Client Group Required',
  'client_group_50': 'More than 50 characters are not allowed for Client Group Name',
  'secondary_legislation_required': 'Please select any one of the Secondary Legislation',
  'statutory_provision_required': 'Please select any one of the Statutory Provision',
  'un_saved_compliance': 'All compliance should be selected before submit',
  'compliance_task_required': 'Please select any one of the Compliance Task',
  'compliance_description_required': 'Please select any one of the Compliance Description',
  'sys_rejected_confirm': 'compliance declined, Do you want to continue ?',
  'manuval_rejected_confirm': 'Some manual rejections are inside, Do you want to continue?',
  'un_saved_compliance': 'All compliance should be selected before submit',
  'clientgroup_required': 'Client Group Name Required',
  "no_compliance_assign_statutory": "No Compliance Available for Assign Statutory",
  "upload_limit": "CSV Rejected files limit exceeded",
  "csv_max_lines_exceeded": "CSV file exceeded max \"MAX_LINES\" lines",
  "document_upload_success": "Document uploaded successfully",

  "client_unit_upload_success": "Client Units uploaded successfully",
  "client_unit_upload_failed": "Client Units not uploaded successfully",
  "upload_failed": "CSV file upload failed",
  "confirm_success": "Action taken successfully",
  "client_unit_file_max": "Rejected CSV File Reached the Max Limit for uploading CSV File",
  "cg_required": "Client Group Required",
  "csv_file_blank": "CSV File Cannot be Blank",
  "csv_file_lines_max": "CSV File Lines Reached the Max Limit",
  "invalid_csv_file": "Invalid Csv File",
  "rejection_max_count_reached": "Already reached the maximum count of rejected files",
  "reason_invalid":"Reason should accept only 0-9, A-Z, a-z, dot, comma, hyphen.",
  "units_not_assigned_to_user": "Some Units not assigned to you",
  "document_required": "Document Required"
}

$.extend(message, bulkMessage);