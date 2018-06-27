var MY_MODAL = $("#myModal");
var STATUS = "DONE";
var TIMEOUT_MLS = 45000;
var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();

var CANCEL_BUTTON = $("#cancel_button");
var ADD_SCREEN = $("#add_screen");
var VIEW_SCREEN = $("#list_screen");
var ADD_BUTTON = $("#btn_add");
var DOWNLOAD_BUTTON = $("#btnDownloadFile");
var SUBMIT_BUTTON = $(".btn-submit");

var UPLOAD_FILE = $("#fileInput");

var LEGALENTITY_NAME = $("#txt_legal_entity_name");
var LEGALENTITY_ID = $("#hdn_legal_entity_id");
var LEGALENTITY_NAME_LABEL = $(".legal-entity-name");
var AC_LEGALENTITY = $("#ac_entity");
var LEGALENTITY_NAME_AC = $(".legal-entity-name-ac");

var LEGALENTITY_NAME_UPLOAD = $("#txt_legal_entity_name_upload");
var LEGALENTITY_ID_UPLOAD = $("#hdn_legal_entity_id_upload");
var LEGALENTITY_NAME_LABEL_UPLOAD = $(".legal-entity-name-upload");
var AC_LEGALENTITY_UPLOAD = $("#ac_entity_upload");
var LEGALENTITY_NAME_AC_UPLOAD = $(".legal-entity-name-ac-upload");

var LIST_CONTAINER = $(".tbody-ct-csv-list");
var LIST_ROW_TEMPLATE = $("#templates .table-ct-csv-info .table-row");

var TXT_DOMAIN = $("#txt_domain");
var HDN_DOMAIN = $("#hdn_domain");
var DIV_DOMAIN = $("#div_domain");

var TXT_UNIT = $("#txt_unit");
var HDN_UNIT = $("#hdn_unit");
var DIV_UNIT = $("#div_unit");

var BTN_UPLOAD = $("#btnUpload");
var BTN_UPLOADED_DATA = $(".uploaded-data");
var INVALID_FILE_NAME = null;

var UNIT_LIST = [];
var DOMAIN_LIST = [];
var DOC_NAMES = [];
var CSV_INFO = null;
var CSV_ID = null;
var BUCT_PAGE = null;
//Filters
var UPLOADED_ON_FILTER = $("#filter_uploaded_on");
var UPLOADED_FILE_FILTER = $("#filter_uploaded_file");

//error description variable declaration
var TOTAL_RECORD = $(".totalRecords");
var VALID_RECORD = $(".validRecords");
var INVALID_RECORD = $(".invalidRecords");
var INVALID_DATE = $(".invaliddate");
var DUPLICATE_ERROR = $(".duplicateErrors");
var MANDATORY_ERROR = $(".mandatoryfieldblank");
var LENGTH_ERROR = $(".lengthErrors");
var INACTIVE_ERROR = $(".masterdatainactive");
var INVALID_FILE_FORMAT_ERROR = $(".invalidfileformat");
var INVALID_DATA_VALIDATION = $(".invaliddatavaidation");
var INVALID_CHAR_VALIDATION = $(".invalidchar");

var UNIT_LISTMAP = {};
var LEGALENTITYUSR = [];

var TOTAL_DOCUMENTS = 0;
var UPLOADED_DOCUMENTS = 0;
var REMAINING_DOCUMENTS = 0;

BUCLIENT = buClient;

function displayLoader() {
  $(".loading-indicator-spin").show();
}
function hideLoader() {
  $(".loading-indicator-spin").hide();
}

TXT_DOMAIN.keyup(function(e) {
    var conditionFields = [];
    var conditionValues = [];
    var textVal = $(this).val();
    commonAutoComplete(e, DIV_DOMAIN, HDN_DOMAIN, textVal, DOMAIN_LIST,
        "d_name", "d_id",
        function(val) {
            displayLoader();
            loadUnits(parseInt(LEGALENTITY_ID.val()), parseInt(val), function(){
                onAutoCompleteSuccess(TXT_DOMAIN, HDN_DOMAIN, val);
            });
        }, conditionFields, conditionValues);
});

//Unit Auto Complete
TXT_UNIT.keyup(function(e) {
    var conditionFields = [];
    var conditionValues = [];
    var textVal = $(this).val();
    commonAutoComplete(
        e, DIV_UNIT, HDN_UNIT, textVal,
        UNIT_LIST, "unit_name", "unit_id",
        function(val) {
            onAutoCompleteSuccess(TXT_UNIT, HDN_UNIT, val);
        }, conditionFields, conditionValues);
});

//Uploaded on Filter
UPLOADED_ON_FILTER.keyup(function() {
    fList = key_search(BUCT_PAGE._ListDataForView);
    BUCT_PAGE.renderList(fList);
});

//Uploaded file Filter
UPLOADED_FILE_FILTER.keyup(function() {
    fList = key_search(BUCT_PAGE._ListDataForView);
    BUCT_PAGE.renderList(fList);
});

function loadUnits(leId, domainId, callback) {
    buClient.getUnits(leId, domainId, function(error, response) {
        if (error == null) {
            UNIT_LIST = response.user_units;
            $.each(UNIT_LIST, function(key, u) {
                UNIT_LISTMAP[parseInt(u["unit_id"])] = u["unit_code"];
                u["unit_name"] = u["unit_code"]+"-"+u["unit_name"];
            });
            hideLoader();
        }else{
            hideLoader();
        }
    });
    callback();
}
LEGALENTITY_NAME.keyup(function(e) {
    var textVal = $(this).val();
    commonAutoComplete(
        e, AC_LEGALENTITY, LEGALENTITY_ID, textVal,
        LEGAL_ENTITIES, "le_name", "le_id",
        function(val) {
            onAutoCompleteSuccess(LEGALENTITY_NAME, LEGALENTITY_ID, val);
        });
});
LEGALENTITY_NAME_UPLOAD.keyup(function(e) {
    var textVal = $(this).val();
    commonAutoComplete(
        e, AC_LEGALENTITY_UPLOAD, LEGALENTITY_ID_UPLOAD, textVal,
        LEGAL_ENTITIES, "le_name", "le_id",
        function(val) {
            onAutoCompleteSuccess(
                LEGALENTITY_NAME_UPLOAD, LEGALENTITY_ID_UPLOAD, val
            );
        });
});

function get_legal_entity_id(le_name){
     for (i = 0; i < LEGAL_ENTITIES.length; i++) {
        if (LEGAL_ENTITIES[i]["le_name"] == le_name){
            return LEGAL_ENTITIES[i]["le_id"]
        }
    }
}

function onAutoCompleteSuccess(valueElement, idElement, val) {
    valueElement.val(val[1]);
    idElement.val(val[0]);
    if (idElement[0].id == "hdn_legal_entity_id") {
        getPastRecords(parseInt(LEGALENTITY_ID.val()));
    }
}

function loadEntityDetails() {
    var leName = "";
    var leId = "";
    var i = 0;
    LEGALENTITYUSR = [];
    if (LEGAL_ENTITIES.length > 1) {
        LEGALENTITY_NAME_LABEL.hide();
        LEGALENTITY_NAME_LABEL_UPLOAD.hide();
        LEGALENTITY_NAME_AC.show();
        LEGALENTITY_NAME_AC_UPLOAD.show();

        for (i = 0; i < LEGAL_ENTITIES.length; i++) {
            LEGALENTITYUSR.push(LEGAL_ENTITIES[i]["le_id"]);
        }

    } else {
        leName = LEGAL_ENTITIES[0]["le_name"];
        leId = LEGAL_ENTITIES[0]["le_id"];
        LEGALENTITYUSR.push(leId);

        LEGALENTITY_NAME_LABEL.show();
        LEGALENTITY_NAME_LABEL_UPLOAD.show();
        LEGALENTITY_NAME_AC.hide();
        LEGALENTITY_NAME_AC_UPLOAD.hide();

        LEGALENTITY_NAME_LABEL.text(leName);
        LEGALENTITY_NAME_LABEL_UPLOAD.text(leName);
        LEGALENTITY_ID.val(leId);
        LEGALENTITY_ID_UPLOAD.val(leId);

        getPastRecords(parseInt(LEGALENTITY_ID.val()));
    }
}

function getPastRecords(legalEntity) {
    displayLoader();

    function onSuccess(data) {
        DOMAIN_LIST = data.domains;
        hideLoader();
    }

    function onFailure() {
        hideLoader();
    }
    client_mirror.getPastRecordsFormData(parseInt(legalEntity),
        function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure();
            }
        }
    );
}

function setDocumentCount(){
    $('#bu_doc_total').text(TOTAL_DOCUMENTS);
    if (UPLOADED_DOCUMENTS > TOTAL_DOCUMENTS) {
        UPLOADED_DOCUMENTS = TOTAL_DOCUMENTS;
        REMAINING_DOCUMENTS = TOTAL_DOCUMENTS - UPLOADED_DOCUMENTS;
    }
    $('#bu_upload_total').text(UPLOADED_DOCUMENTS);
    $('#bu_remain_total').text(REMAINING_DOCUMENTS);
}

function validateUpload() {
    var csvSplitName = null;
    var getValidCount = null;
    var args = null;
    if(
        $("#txt_legal_entity_name_upload").val() == "" &&
        LEGALENTITY_NAME_LABEL_UPLOAD.text() == ""
    ){
        displayMessage(message.legalentity_required);
        MY_MODAL.modal("hide");
        return false;
    }
    else if (
        UPLOAD_FILE.val() == "" && BUCT_PAGE._ActionMode == "add"
    ) {
        displayMessage(message.upload_csv);
        MY_MODAL.modal("hide");
        return false;
    }else if (
        addedfiles.length <=0 && BUCT_PAGE._ActionMode == "upload"
    ) {
        displayMessage(message.upload_docs);
        MY_MODAL.modal("hide");
        return false;
    }  else {
        MY_MODAL.modal("show");
        if (BUCT_PAGE._ActionMode == "add") {
            args = {
                "csv_name": CSV_INFO["file_name"],
                "csv_data": CSV_INFO["file_content"],
                "csv_size": CSV_INFO["file_size"],
                "legal_entity_id": parseInt(LEGALENTITY_ID_UPLOAD.val())
            };
            var csv_name = null;
            function apiCall(leg_id, csv_name, callback){
                console.log(new Date());
                console.log("calling get status: "+ new Date().getTime());
                buClient.GetStatus(leg_id, csv_name, callback);
            }
            function call_bck_fn(error, data){
                console.log(error);
                if (error == "Alive"){
                    setTimeout(apiCall, TIMEOUT_MLS, leg_id, csv_name, call_bck_fn);
                }else if (error == "InvalidCsvFile" ){
                    MY_MODAL.modal("hide");
                    UPLOAD_FILE.val("");
                    displayMessage(message.invalid_csv_file);
                }else if(error == "DataAlreadyExists"){
                    $('#myModal').modal('hide');
                    UPLOAD_FILE.val("");
                    displayMessage(message.data_already_exists);
                }else if(data == "Bad Request"){
                    displayMessage(message.upload_failed);
                    $('#myModal').modal('hide');
                    hideLoader();
                }
                else if (error == null) {
                    csvSplitName = data.csv_name.substring(
                        0, data.csv_name.lastIndexOf("_"));
                    $('#myModal').modal('hide');
                    TOTAL_RECORD.text(data.total);
                    VALID_RECORD.text(parseInt(data.valid) - parseInt(
                        data.invalid));
                    INVALID_RECORD.text(data.invalid);
                    INVALID_FILE_NAME = null;
                    INVALID_DATE.text("0");
                    DUPLICATE_ERROR.text("0");
                    MANDATORY_ERROR.text("0");
                    LENGTH_ERROR.text("0");
                    INACTIVE_ERROR.text("0");
                    INVALID_FILE_FORMAT_ERROR.text(0);
                    INVALID_DATA_VALIDATION.text("0");
                    INVALID_CHAR_VALIDATION.text("0");
                    $("#dom_id_hdn").val(data.domain_id);
                    $("#unit_id_hdn").val(data.unit_id);
                    $('.view-summary').hide();
                    $('.dropbtn').hide();
                    $('#hdn_csv_id').val(data.new_csv_id);
                    CSV_ID = data.new_csv_id;
                    $('.successFileName').text(csvSplitName);
                    csvPath = "../../../../../uploaded_file/csv/" +
                                    data.csv_name;
                    $("#success_file_download").attr("href", csvPath);
                    $('#success_file_download').attr("download", data.csv_name);
                    $('.uploaded-data').attr("id", CSV_ID);
                    $('.uploaded-data .text-primary').attr(
                        "id", data.legal_entity_id);
                    // $('.uploaded-data').attr("href", csvPath);
                    // $('.uploaded-data').attr("download", data.csv_name);

                    if (data.doc_count > 0) {
                        $('.divSuccessDocument').show();
                        $('#divSuccessbutton').hide();
                        BUCT_PAGE._ActionMode = "upload";
                        BTN_UPLOAD.show();
                        DOC_NAMES = data.doc_names;
                    } else {
                        $('.divSuccessDocument').hide();
                        $('#divSuccessbutton').show();
                        BTN_UPLOAD.hide();
                    }

                    $('.invaliddata').hide();
                    $('.view-summary').hide();
                    $('#divFileUpload').hide();
                    $('#divSuccessFile').show();
                    $(".bu-doc-summary").show();
                    TOTAL_DOCUMENTS = data.doc_count;
                    UPLOADED_DOCUMENTS = 0;
                    REMAINING_DOCUMENTS = data.doc_count;
                    setDocumentCount();
                    $('#up-doc-title').hide();
                    $('#remaining-doc-title').hide();
                    displaySuccessMessage(
                        "Csv file uploaded successfully");
                    hideLoader();
                } else {
                    MY_MODAL.modal('hide');
                    displayMessage(message.upload_failed);
                    INVALID_FILE_NAME = data.invalid_file.split('.');
                    TOTAL_RECORD.text(data.total);
                    getValidCount = (
                        parseInt(data.total) - parseInt(data.invalid));
                    VALID_RECORD.text(getValidCount);
                    INVALID_RECORD.text(data.invalid);
                    INVALID_DATE.text(data.invalid_date);
                    DUPLICATE_ERROR.text(data.duplicate_error);
                    MANDATORY_ERROR.text(data.mandatory_error);
                    LENGTH_ERROR.text(data.max_length_error);
                    getInvaliddataCount = parseInt(
                        data.invalid_char_error) +
                        parseInt(data.invalid_data_error);
                    INACTIVE_ERROR.text(data.inactive_error);
                    INVALID_FILE_FORMAT_ERROR.text(
                        data.invalid_file_format);
                    INVALID_DATA_VALIDATION.text(data.invalid_data_error);
                    INVALID_CHAR_VALIDATION.text(data.invalid_char_error);
                    $('.dropbtn').show();
                    $('.view-summary').show();
                    UPLOAD_FILE.val("");
                    $('.invaliddata').show();
                    $('.view-summary').show();
                    $('#divFileUpload').show();
                    $('#divSuccessFile').hide();
                    $('.divSuccessDocument').hide();
                    $('#divSuccessbutton').hide();
                    base_path = "../download/invalid";
                    csvPath = base_path + "/csv/" +
                                INVALID_FILE_NAME[0] + '.csv';
                    xls_path = base_path + "/xlsx/"
                                + INVALID_FILE_NAME[0] + '.xlsx';
                    ods_path = base_path + "/ods/"
                                + INVALID_FILE_NAME[0] + '.ods';
                    txt_path = base_path + "/txt/"
                                + INVALID_FILE_NAME[0] + '.txt';
                    $('#csv').attr("href", csvPath);
                    $('#excel').attr("href", xls_path);
                    $('#ods').attr("href", ods_path);
                    // $('#txt').attr("href", txt_path);
                    hideLoader();
                }
            }
            buClient.UploadCompletedTaskCurrentYearCSV(
                args, function(error, data){
                    if(error == "Done" || data == "Done"){
                        leg_id = parseInt(LEGALENTITY_ID_UPLOAD.val());
                        csv_name = data.csv_name;
                        apiCall(leg_id, csv_name, call_bck_fn);
                    }else if (error == "InvalidCsvFile" ){
                        MY_MODAL.modal("hide");
                        UPLOAD_FILE.val("");
                        displayMessage(message.invalid_csv_file);
                    }else if (error == "CsvFileExeededMaxLines"){
                        displayMessage(message.csv_max_lines_exceeded.replace(
                        "MAX_LINES", data.csv_max_lines));
                        UPLOAD_FILE.val("");
                        MY_MODAL.modal("hide");
                        hideLoader();
                    }else if(data == "Bad Request"){
                        displayMessage(message.upload_failed);
                        $('#myModal').modal('hide');
                        hideLoader();
                    }
                });
        } else {
            $('#myModal').modal('hide');
            displayLoader();
            $('#up-doc-title').show();
            $('#remaining-doc-title').show();
            setDocumentCount();
            myDropzone.processQueue();
        }
    }
}

document.getElementById("txt").addEventListener("click", function() {
    if (INVALID_FILE_NAME != null) {
        $.get(
            "../download/invalid/txt/" + INVALID_FILE_NAME[0] + ".txt",
            function(data) {
                download(
                    INVALID_FILE_NAME[0] + ".txt", "text/plain", data);
            },
            'text');
    }
});

function download(filename, mime_type, text) {
    var element = document.createElement('a');
    var href = 'data:' + mime_type + ';charset=utf-8,'
                + encodeURIComponent(text);
    element.setAttribute('href', href);
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

UPLOAD_FILE.change(function(e) {
    if ($(this).val() != '') {
        buClient.uploadCSVFile(e, function(status, response) {
            if (status == false) {
                UPLOAD_FILE.val("");
                displayMessage(response);
            } else {
                CSV_INFO = response;
            }
        });
    }
});

$(function() {
    loadEntityDetails();

});

function pageControls() {
    // Cancel Button Click Event
    CANCEL_BUTTON.click(function() {
        resetAdd();
        resetEdit();
        VIEW_SCREEN.show();
        ADD_SCREEN.hide();
        BUCT_PAGE.showList();
    });

    //Add Button Click Event
    ADD_BUTTON.click(function() {
        VIEW_SCREEN.hide();
        ADD_SCREEN.show();
        BUCT_PAGE._ActionMode = "add";
        resetAdd();
    });

    //Add Button Click Event
    DOWNLOAD_BUTTON.click(function() {
        downloadData();
    });

    //Upload Button Click Event
    BTN_UPLOAD.click(function() {
        this.disabled = true;
        validateUpload();
        this.disabled = false;
    });

    BTN_UPLOADED_DATA.click(function(){
        downloadUploadedData(
            parseInt($(".uploaded-data").attr("id"))
        );
    });

    SUBMIT_BUTTON.click(function() {
        submitUpload();
    });
}

BulkCompletedTaskCurrentYear.prototype.showList = function() {
    var tThis = this;
    var args = {
        "legal_entity_id": parseInt(LEGALENTITY_ID.val()),
        "legal_entity_list": LEGALENTITYUSR
    };

    displayLoader();
    buClient.GetCompletedTaskCsvUploadedList(args,
        function(error, data) {
            if (error == null) {
                tThis._ListDataForView = data.csv_list;
                tThis.renderList(tThis._ListDataForView);
                hideLoader();
            } else {
                hideLoader();
            }
        }
    );
};

BulkCompletedTaskCurrentYear.prototype.renderList = function(
    list_data) {
    var tThis = this;
    var j = 1;
    var tableRow4 = null;
    var clone4 = null;
    var balance = null;
    var cloneRow  = null;
    var cnameSplit = null;
    var cname = null;
    LIST_CONTAINER.find('tr').remove();
    if (list_data.length == 0) {
        LIST_CONTAINER.empty();
        tableRow4 = $(
            '#no_record_templates .table-no-content .table-row-no-content'
        );
        clone4 = tableRow4.clone();
        $('.no-records', clone4).text('No Records Found');
        LIST_CONTAINER.append(clone4);
    } else {
        $.each(list_data, function(idx, data) {
            balance = data.no_of_documents - data.bu_uploaded_documents;
            cloneRow = LIST_ROW_TEMPLATE.clone();
            cnameSplit = data.csv_name.split("_");
            cnameSplit.pop();
            cname = cnameSplit.join("_");
            var fileSubStats = data.file_submit_status;
            var dataSubStats = data.data_submit_status;
            var fileDownldStatus = data.file_download_status;

            $('.sno', cloneRow).text(j);
            $('.legal-entity', cloneRow).text(data.legal_entity_name);
            $('.csv-name', cloneRow).text(cname);
            $('.uploaded-on', cloneRow).text(data.uploaded_on);
            $('.tot-records', cloneRow).text(data.total_records);
            $('.req-docs', cloneRow).text(data.total_documents);
            $('.uploaded-docs', cloneRow).text(
                data.bu_uploaded_documents);
            $('.remaining-docs', cloneRow).text(
                data.remaining_documents);
            CSV_ID = data.csv_id;
            if(data.remaining_documents > 0){
                $('.upload i', cloneRow).show();
                $('.upload i', cloneRow).on('click', function() {
                    tThis.showEdit(data);
                });
                $('.queued-task i', cloneRow).hide();
            }else{
                $('.upload i', cloneRow).hide();
                if(jQuery.inArray(fileSubStats, [0,2]) != -1 ||
                   jQuery.inArray(dataSubStats, [0,2]) != -1 ){
                    $('.queued-task i', cloneRow).show();
                    $('.queued-task i', cloneRow).on('click', function() {
                        tThis.processQueuedTasks(data);
                    });
                }
                // else if(fileSubStats == 0 && fileDownldStatus == "completed"){
                //     console.log("Else")
                //     $('.queued-task i', cloneRow).hide();
                //     $('.queued-task', cloneRow).text("In Progress");
                // }
            }

            LIST_CONTAINER.append(cloneRow);
            j += 1;
        });
    }
    $('[data-toggle="tooltip"]').tooltip();
};

BulkCompletedTaskCurrentYear.prototype.showEdit = function(data) {
    var uploadedCsvName = data.csv_name;
    var legal_entity_name = data.legal_entity_name;
    resetEdit();
    LEGALENTITY_ID_UPLOAD.val(get_legal_entity_id(legal_entity_name));
    LEGALENTITY_NAME_LABEL.show();
    LEGALENTITY_NAME_LABEL_UPLOAD.show();
    LEGALENTITY_NAME_AC.hide();
    LEGALENTITY_NAME_AC_UPLOAD.hide();
    LEGALENTITY_NAME_LABEL_UPLOAD.text(legal_entity_name);

    DOC_NAMES = data.doc_names;
    TOTAL_DOCUMENTS = data.total_documents;
    UPLOADED_DOCUMENTS = data.bu_uploaded_documents;
    REMAINING_DOCUMENTS = data.remaining_documents;
    setDocumentCount();

    $("#dom_id_hdn").val(data.domain_id);
    $("#unit_id_hdn").val(data.unit_id);
    $("#start_date_hdn").val(data.start_date);

    csvPath = "../../../../../uploaded_file/csv/" +
                                    data.csv_name;
    $("#success_file_download").attr("href", csvPath);
    $('#success_file_download').attr("download", data.csv_name);

    $('#hdn_csv_id').val(data.csv_past_id);
    CSV_ID = data.csv_past_id;

    csvSplitName = uploadedCsvName.substring(
        0, uploadedCsvName.lastIndexOf("_"));
    $('.successFileName').text(csvSplitName);
    $('.uploaded-data .text-primary').attr("id", get_legal_entity_id(legal_entity_name));
    $('.uploaded-data').attr("id", CSV_ID);
};

BulkCompletedTaskCurrentYear.prototype.processQueuedTasks = function(data) {
    t_this = this;
    displayLoader();
    var fileSubStats = data.file_submit_status;
    var dataSubStats = data.data_submit_status;
    var csvPastId = data.csv_past_id;

    legId = get_legal_entity_id(data.legal_entity_name);
    countryId = getCountryId(legId);
    var args = {
        "file_submit_status": fileSubStats,
        "data_submit_status": dataSubStats,
        "new_csv_id": csvPastId,
        "country_id": parseInt(countryId),
        "legal_entity_id": parseInt(legId),
        "domain_id": parseInt(data.domain_id),
        "unit_id": parseInt(data.unit_id)
    };

    function apiCall(legId, csv_id, callback){
        buClient.GetStatus(legId, csv_id, callback);
    }
    function call_bck_fn(error, data){
        if (error == "Alive"){
            setTimeout(apiCall, TIMEOUT_MLS, legId, csv_id, call_bck_fn);
        }
        else if (error == null) {
            hideLoader();
            displaySuccessMessage(message.process_queued_task_success);
            VIEW_SCREEN.show();
            BUCT_PAGE.showList();
        } else if (error == "ProcessDocumentSubmitQueued"){
            displaySuccessMessage(message.process_queued_doc_success);
        }
        else{
            t_this.possibleFailures(error);
            hideLoader();
        }
    }


    buClient.processQueuedTasksRequest(args,
        function(error, data) {
            if(error == "Done" || data == "Done"){
                csv_id = data.csv_name;
                apiCall(legId, csv_id, call_bck_fn);
            }else if (error == "ProcessCompleted"){
                displaySuccessMessage(message.process_completed);
                hideLoader();
                VIEW_SCREEN.show();
                BUCT_PAGE.showList();
            }else{
                hideLoader();
            }
        });
}

BulkCompletedTaskCurrentYear.prototype.possibleFailures = function(
    error) {
    displayMessage(error);
};

function downloadUploadedData(CSV_ID){
    args = {
        "country_id": getCountryId(LEGALENTITY_ID_UPLOAD.val()),
        "legal_entity_id": parseInt(LEGALENTITY_ID_UPLOAD.val())
    };
    displayLoader();
    res = buClient.downloadUploadedData(
        parseInt(LEGALENTITY_ID_UPLOAD.val()), CSV_ID,
        function(error, data) {
            if (error == null) {
                downloadUrl = data.link;
                window.open(downloadUrl, '_blank');
                hideLoader();
            }else{
                hideLoader();
            }

            });
}

function downloadData() {
    displayLoader();
    var legalEntityName;
    var domainName = TXT_DOMAIN.val();
    var unitName = TXT_UNIT.val();
    var leId = LEGALENTITY_ID.val();
    var domainId = HDN_DOMAIN.val();
    var unitId = HDN_UNIT.val();
    var unitCode = UNIT_LISTMAP[unitId];
    var frequency = "Periodical";
    var startCount = 0;
    var downloadUrl  = null;

    if (LEGALENTITY_ID.val().trim() == "") {
        displayMessage(message.legalentity_required);
        LEGALENTITY_NAME.focus();
        hideLoader();
        return false;
    }
    if (HDN_DOMAIN.val().trim() == "") {
        displayMessage(message.domain_required);
        TXT_DOMAIN.focus();
        hideLoader();
        return false;
    }
    if (HDN_UNIT.val().trim() == "") {
        displayMessage(message.unit_required);
        TXT_UNIT.focus();
        hideLoader();
        return false;
    }
    if (LEGALENTITY_NAME_LABEL.text() == "") {
        legalEntityName = LEGALENTITY_NAME.val().trim();
    } else {
        legalEntityName = LEGALENTITY_NAME_LABEL.text();
    }

    buClient.getDownloadData(
        parseInt(leId), parseInt(domainId), parseInt(unitId),
        frequency, startCount,
        legalEntityName, domainName, unitName, unitCode,
        function(error, data) {
            if (error == null) {
                downloadUrl = data.link;
                if (downloadUrl != null) {
                    window.open(downloadUrl, '_blank');
                } else {
                    displayMessage(message.no_compliance_available);
                }
                hideLoader();
            } else {
                if (error == "ExportToCSVEmpty"){
                    displayMessage(message.no_compliance_available);
                }
                hideLoader();
            }
        }
    );
}


function getCountryId(le_id) {
    var cId = null;
    $.each(LEGAL_ENTITIES, function(k, v) {
        if (v.le_id == parseInt(le_id)) {
            cId = v.c_id;
        }
    });
    return cId;
}

function submitUpload() {
    var domId = $("#dom_id_hdn").val();
    var unitId = $("#unit_id_hdn").val();
    var leg_id = parseInt(LEGALENTITY_ID_UPLOAD.val())
    var csv_id = null;
    var args = {
        "new_csv_id": parseInt($('#hdn_csv_id').val()),
        "country_id": getCountryId(LEGALENTITY_ID_UPLOAD.val()),
        "legal_entity_id": leg_id,
        "domain_id": parseInt(domId),
        "unit_id": parseInt(unitId)
    };
    function apiCall(leg_id, csv_id, callback){
        buClient.GetStatus(leg_id, csv_id, callback);
    }
    function call_bck_fn(error, data){
        if (error == "Alive"){
            setTimeout(apiCall, TIMEOUT_MLS, leg_id, csv_id, call_bck_fn);
        }else if(error == 'DataAlreadyExists'){
            resetAdd();
            resetEdit();
            displayMessage(message.data_already_exists);
            $('#myModal').modal('hide');
            VIEW_SCREEN.show();
            BUCT_PAGE.showList();
            ADD_SCREEN.hide();
        }
        else if (error == null) {
            resetAdd();
            resetEdit();
            displaySuccessMessage("Compliance Submitted successfully");
            $('#myModal').modal('hide');
            VIEW_SCREEN.show();
            BUCT_PAGE.showList();
            ADD_SCREEN.hide();
        } else {
            $('#myModal').modal('hide');
        }
    }
    $('#myModal').modal('show');
    buClient.saveBulkRecords(args, function(error, data) {
        if(error == "Done" || data == "Done"){
            csv_id = data.csv_name;
            apiCall(leg_id, csv_id, call_bck_fn);
        }else{
            $('#myModal').modal('hide');
        }
    })
}


BulkCompletedTaskCurrentYear.prototype.possibleFailures = function(
    error) {
    displayMessage(error);
};

key_search = function(mainList) {
    key_one = UPLOADED_ON_FILTER.val().toLowerCase();
    key_two = UPLOADED_FILE_FILTER.val().toLowerCase();
    var fList = [];
    for (var entity in mainList) {
        uploaded_file = mainList[entity].csv_name;
        uploaded_on = mainList[entity].legal_entity_name;
        if (
            (~uploaded_on.toString().toLowerCase().indexOf(
                key_one)) &&
            (~uploaded_file.toString().toLowerCase().indexOf(
                key_two))
        ) {
            fList.push(mainList[entity]);

        }
    }
    return fList
};

function file_upload_rul() {
    var sessionId = client_mirror.getSessionToken();
    var fileBaseUrl = "/clienttemp/upload?session_id=" +
        sessionId + "&csvid=" + CSV_ID;
    return fileBaseUrl;
}

function resetAdd() {
    LEGALENTITY_NAME_LABEL.hide();
    LEGALENTITY_NAME_LABEL_UPLOAD.hide();
    LEGALENTITY_NAME_AC.show();
    LEGALENTITY_NAME_AC_UPLOAD.show();
    LEGALENTITY_NAME_LABEL_UPLOAD.text("");

    $('#divDownloadSection').show();
    $('#divUploadSection').show();

    $('.divSuccessDocument').hide();
    $('#divSuccessbutton').hide();
    $('.invaliddata').hide();
    $('.view-summary').hide();
    $('#divFileUpload').show();
    $('#divSuccessFile').hide();
    $('.bu-doc-summary').hide();
    BTN_UPLOAD.show();

    BUCT_PAGE._ActionMode = "add";
    UPLOAD_FILE.val("");
    LEGALENTITY_NAME.val("");
    TXT_DOMAIN.val("");
    TXT_UNIT.val("");
    LEGALENTITY_NAME_UPLOAD.val("");
    addedfiles = [];
    uploadedfiles = [];
    loadEntityDetails();
}

function resetEdit() {
    VIEW_SCREEN.hide();
    ADD_SCREEN.show();

    $('#divDownloadSection').hide();
    $('#divUploadSection').show();

    $('.divSuccessDocument').show();
    $('.bu-doc-summary').show();
    $('#divSuccessFile').show();

    $('.view-summary').hide();
    $('#divSuccessbutton').hide();
    $('.invaliddata').hide();
    $('#divFileUpload').hide();

    BUCT_PAGE._ActionMode = "upload";
    UPLOAD_FILE.val("");
    LEGALENTITY_NAME.val("");
    TXT_DOMAIN.val("");
    TXT_UNIT.val("");
    LEGALENTITY_NAME_UPLOAD.val("");
    myDropzone.removeAllFiles();
    BTN_UPLOAD.show();
    addedfiles = [];
    uploadedfiles = [];
    loadEntityDetails();
}

Dropzone.autoDiscover = false;
Dropzone.autoProcessQueue = false;
var addedfiles = [];
var uploadedfiles = [];
var totalfileUploadSuccess = 0;
var perQueueUploadSuccess = 0;
var queueCount = 0;
var maxParallelCount = 2;
var myDropzone = new Dropzone("div#myDrop", {
    addRemoveLinks: true,
    autoProcessQueue: false,
    parallelUploads: maxParallelCount,
    url: "#",
    transformFile: function transformFile(file, done) {
        var zip = new JSZip();
        zip.file(file.name, file);
        zip.generateAsync({
            type: "blob",
            compression: "DEFLATE"
        }).then(function(content) {
            done(content);
        });
    },
    init: function() {
        this.on("addedfile", function(file) {
            if (
                jQuery.inArray(file.name, addedfiles) > -1 ||
                jQuery.inArray(file.name, DOC_NAMES) == -1 ||
                jQuery.inArray(file.name, uploadedfiles) > -1 ||
                REMAINING_DOCUMENTS <= 0
            ){
                myDropzone.removeFile(file);
            }else {
                addedfiles.push(file.name);
                queueCount += 1;
            }
            if(REMAINING_DOCUMENTS <= 0){
                displayMessage("Required files were already added");
            }

        });
        this.on("removedfile", function(file) {
            if (jQuery.inArray(file.name, addedfiles) > -1) {
                addedfiles.pop(file.name);
                queueCount -= 1;
            }
        });

        this.on("processing", function(file) {
            this.options.url = file_upload_rul();
        });

        this.on("success", function(file, response) {
            addedfiles.pop(file.name);
            uploadedfiles.push(file.name);
            if (totalfileUploadSuccess < queueCount) {
                totalfileUploadSuccess += 1;
                perQueueUploadSuccess += 1;
                UPLOADED_DOCUMENTS += 1;
                REMAINING_DOCUMENTS = TOTAL_DOCUMENTS - UPLOADED_DOCUMENTS;
                setDocumentCount();
            }

            if (perQueueUploadSuccess == maxParallelCount) {
                perQueueUploadSuccess = 0;
                myDropzone.processQueue();
            }
            if (REMAINING_DOCUMENTS == 0) {
                displaySuccessMessage(message.document_upload_success);
                $('#divSuccessbutton').show();
                BTN_UPLOAD.hide();
                BUCT_PAGE.showList();
            }
            // myDropzone.removeAllFiles(true);
            hideLoader();
        });

        this.on("error", function(file, errorMessage) {
            displayMessage(errorMessage);
            addedfiles = [];
            myDropzone.removeAllFiles(true);
            hideLoader();
        });
    }
});

function BulkCompletedTaskCurrentYear() {
    this._ActionMode = null;
    this._ListDataForView = [];
}

function genericWorker(worker_url, data) {
    return new Promise(function (resolve, reject) {

        if (!data.callback || !Array.isArray(data.callback))
            return reject("Invalid data")

        var callback = data.callback.pop()
        var functions = data.callback
        var context = data.context

        if (!worker_url)
            return reject("Worker_url is undefined")

        if (!callback)
            return reject("A callback was expected")

        if (functions.length>0 && !context)
            return reject("context is undefined")

        callback = fn_string(callback) //Callback to be executed
        functions = functions.map((fn_name)=> { return fn_string( context[fn_name] ) })

        var worker = new Worker(worker_url)

        worker.postMessage({ callback: callback, functions: functions })

        worker.addEventListener('error', function(error){
            return reject(error.message)
        })

        worker.addEventListener('message', function(e) {
            resolve(e.data)
            worker.terminate()

        }, false)


        //From function to string, with its name, arguments and its body
        function fn_string (fn) {
            var name = fn.name
            fn = fn.toString()

            return {
                name: name,
                args: fn.substring(fn.indexOf("(") + 1, fn.indexOf(")")),
                body: fn.substring(fn.indexOf("{") + 1, fn.lastIndexOf("}"))
            }
        }

    })
}

BUCT_PAGE = new BulkCompletedTaskCurrentYear();

//initialization & master list filter
$(document).ready(function() {
    pageControls();
    BUCT_PAGE.showList();
});