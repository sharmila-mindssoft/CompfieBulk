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

var LIST_CONTAINER = $('.tbody-ct-csv-list');
var LIST_ROW_TEMPLATE = $('#templates .table-ct-csv-info .table-row');

var TXT_DOMAIN = $("#txt_domain");
var HDN_DOMAIN = $("#hdn_domain");
var DIV_DOMAIN = $("#div_domain");

var TXT_UNIT = $('#txt_unit');
var HDN_UNIT = $('#hdn_unit');
var DIV_UNIT = $('#div_unit');

var BTN_UPLOAD = $('#btnUpload');
var BTN_UPLOADED_DATA = $('.uploaded-data');
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
var TOTAL_RECORD = $('.totalRecords');
var VALID_RECORD = $('.validRecords');
var INVALID_RECORD = $('.invalidRecords');
var INVALID_DATE = $('.invaliddate');
var DUPLICATE_ERROR = $('.duplicateErrors');
var MANDATORY_ERROR = $('.mandatoryfieldblank');
var LENGTH_ERROR = $('.lengthErrors');
var INACTIVE_ERROR = $('.masterdatainactive');
var INVALID_FILE_FORMAT_ERROR = $('.invalidfileformat');
var INVALID_DATA_VALIDATION = $('.invaliddatavaidation');
var INVALID_CHAR_VALIDATION = $('.invalidchar');

var UNIT_LISTMAP = {};
var LEGALENTITYUSR = [];

var TOTAL_DOCUMENTS = 0;
var UPLOADED_DOCUMENTS = 0;
var REMAINING_DOCUMENTS = 0;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

TXT_DOMAIN.keyup(function(e) {
    var conditionFields = [];
    var conditionValues = [];
    var textVal = $(this).val();
    commonAutoComplete(e, DIV_DOMAIN, HDN_DOMAIN, textVal, DOMAIN_LIST,
        "d_name", "d_id",
        function(val) {
            loadUnits(parseInt(LEGALENTITY_ID.val()), parseInt(val));
            onAutoCompleteSuccess(TXT_DOMAIN, HDN_DOMAIN, val);
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

function loadUnits(leId, domainId) {
    buClient.getUnits(leId, domainId, function(error, response) {
        if (error == null) {
            UNIT_LIST = response.user_units;
            $.each(UNIT_LIST, function(key, u) {
                UNIT_LISTMAP[parseInt(u["unit_id"])] = u["unit_code"];
                u["unit_name"] = u["unit_code"]+"-"+u["unit_name"];
            });
        }
    });
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
        console.log(LEGAL_ENTITIES[i]["le_name"])
        if (LEGAL_ENTITIES[i]["le_name"] == le_name){
            console.log("inside if")
            return LEGAL_ENTITIES[i]["le_id"]
        }
    }
}

function onAutoCompleteSuccess(valueElement, idElement, val) {
    valueElement.val(val[1]);
    idElement.val(val[0]);
    if (idElement[0].id == 'hdn_legal_entity_id') {
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

    function onFailure(error) {
        hideLoader();
    }
    client_mirror.getPastRecordsFormData(parseInt(legalEntity),
        function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        }
    );
}

function validateUpload() {
    var csvSplitName = null;
    var getValidCount = null;
    var args = null;
    $('#myModal').modal('show');
    if(
        $('#txt_legal_entity_name_upload').val() == "" && 
        LEGALENTITY_NAME_LABEL_UPLOAD.text() == ""
    ){
        displayMessage(message.legalentity_required);
        $('#myModal').modal('hide');
        return false;
    }
    else if (
        UPLOAD_FILE.val() == "" && BUCT_PAGE._ActionMode == "add"
    ) {
        displayMessage(message.upload_csv);
        $('#myModal').modal('hide');
        return false;
    }else if (
        addedfiles.length <=0 && BUCT_PAGE._ActionMode == 'upload'
    ) {
        displayMessage(message.upload_docs);
        $('#myModal').modal('hide');
        return false;
    }  else {
        $('#myModal').modal('show');
        if (BUCT_PAGE._ActionMode == "add") {
            args = {
                "csv_name": CSV_INFO["file_name"],
                "csv_data": CSV_INFO["file_content"],
                "csv_size": CSV_INFO["file_size"],
                "legal_entity_id": parseInt(LEGALENTITY_ID_UPLOAD.val())
            };

            buClient.UploadCompletedTaskCurrentYearCSV(
                args, function(error, data) {
                if (error == "CsvFileExeededMaxLines"){
                    displayMessage(message.csv_max_lines_exceeded.replace(
                    'MAX_LINES', data.csv_max_lines));
                    UPLOAD_FILE.val("");
                    $('#myModal').modal('hide');
                    hideLoader();
                }
                else if (error == "InvalidCsvFile" ){
                    $('#myModal').modal('hide');
                    UPLOAD_FILE.val("");
                    displayMessage(message.invalid_csv_file);
                }else if(error == 'DataAlreadyExists'){
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
                    // csvPath = "../../../../../uploaded_file/csv/" +
                    //                 data.csv_name;
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
                    $('#bu_doc_total').text(data.doc_count);
                    $('#up-doc-title').hide();
                    $('#remaining-doc-title').hide();
                    $('#bu_upload_total').text('0');
                    $('#bu_remain_total').text('0');
                    if (data.doc_count < 2){
                        myDropzone.parallelUploads = data.doc_count;    
                    }
                    displaySuccessMessage(
                        "Compliance uploaded successfully");
                    hideLoader();

                } else {
                    $('#myModal').modal('hide');
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
                    base_path = "../download/invalid"
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
            });
        } else {
            $('#myModal').modal('hide');
            displayLoader();
            $('#up-doc-title').show();
            $('#remaining-doc-title').show();
            $('#bu_upload_total').text(UPLOADED_DOCUMENTS);
            $('#bu_remain_total').text(
                TOTAL_DOCUMENTS - UPLOADED_DOCUMENTS
            );
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
        validateUpload();
    });

    BTN_UPLOADED_DATA.click(function(){
        downloadUploadedData(
            parseInt($(".uploaded-data .text-primary").attr("id")),
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
                // alert(data);
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
            DOC_NAMES = data.doc_names;
            $('.upload i', cloneRow).on('click', function() {
                tThis.showEdit(data);
            });
            LIST_CONTAINER.append(cloneRow);
            j += 1;
        });
    }
    $('[data-toggle="tooltip"]').tooltip();
};

BulkCompletedTaskCurrentYear.prototype.showEdit = function(data) {
    var uploadedCsvName = data.csv_name;
    var legal_entity_name = data.legal_entity_name;
    var csvSplitName = null;
    resetEdit();
    LEGALENTITY_ID_UPLOAD.val(get_legal_entity_id(legal_entity_name));
    LEGALENTITY_NAME_LABEL.show();
    LEGALENTITY_NAME_LABEL_UPLOAD.show();
    LEGALENTITY_NAME_AC.hide();
    LEGALENTITY_NAME_AC_UPLOAD.hide();
    LEGALENTITY_NAME_LABEL_UPLOAD.text(legal_entity_name);


    TOTAL_DOCUMENTS = data.total_documents;
    UPLOADED_DOCUMENTS = data.bu_uploaded_documents;
    REMAINING_DOCUMENTS = data.remaining_documents;

    $("#dom_id_hdn").val(data.domain_id);
    $("#unit_id_hdn").val(data.unit_id);
    $("#start_date_hdn").val(data.start_date);

    $('#hdn_csv_id').val(data.csv_past_id);
    CSV_ID = data.csv_past_id;

    csvSplitName = uploadedCsvName.substring(
        0, uploadedCsvName.lastIndexOf("_"));
    $('.successFileName').text(csvSplitName);
    $('.uploaded-data .text-primary').attr("id", get_legal_entity_id(legal_entity_name));
    $('.uploaded-data').attr("id", CSV_ID);

    $('#bu_doc_total').text(data.total_documents);
    $('#bu_upload_total').text(data.bu_uploaded_documents);
    $('#bu_remain_total').text(data.remaining_documents);

};


BulkCompletedTaskCurrentYear.prototype.possibleFailures = function(
    error) {
    displayMessage(error);
};

function downloadUploadedData(
    legal_entity_id, CSV_ID){
    res = buClient.downloadUploadedData(
        legal_entity_id, CSV_ID,
        function(error, data) {
            if (error == null) {
                    downloadUrl = data.link;
                    window.open(downloadUrl, '_blank');
                    hideLoader();
                }
            });
}

function downloadData() {
    $('#myModal').modal('show');
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
        $('#myModal').modal('hide');
        return false;
    }
    if (HDN_DOMAIN.val().trim() == "") {
        displayMessage(message.domain_required);
        TXT_DOMAIN.focus();
        $('#myModal').modal('hide');
        return false;
    }
    if (HDN_UNIT.val().trim() == "") {
        displayMessage(message.unit_required);
        TXT_UNIT.focus();
        $('#myModal').modal('hide');
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
                    $('#myModal').modal('hide');
                    hideLoader();
                } else {
                    displayMessage(message.no_compliance_available);
                    $('#myModal').modal('hide');
                    hideLoader();
                }
            } else {
                if (error == "ExportToCSVEmpty"){
                    displayMessage(message.no_compliance_available);
                }
                $('#myModal').modal('hide');
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
    var startDate = $("#start_date_hdn").val();
    var args = {
        "new_csv_id": parseInt($('#hdn_csv_id').val()),
        "country_id": getCountryId(LEGALENTITY_ID_UPLOAD.val()),
        "legal_entity_id": parseInt(LEGALENTITY_ID_UPLOAD.val()),
        "domain_id": parseInt(domId),
        "unit_id": parseInt(unitId)
    };
    $('#myModal').modal('show');
    buClient.saveBulkRecords(args, function(error, data) {
        if (error == null) {
            if (totalfileUploadSuccess > 0){
                buClient.updateDocumentCount(
                        parseInt(
                            $(".uploaded-data .text-primary").attr("id")
                        ), parseInt(
                        $(".uploaded-data").attr("id")), 
                        totalfileUploadSuccess, 
                    function(error, data){
                        resetAdd();
                        resetEdit();
                        displaySuccessMessage("Compliance Submitted successfully");
                        $('#myModal').modal('hide');
                        VIEW_SCREEN.show();
                        ADD_SCREEN.hide();
                    }
                )
            }else{
                resetAdd();
                resetEdit();
                displaySuccessMessage("Compliance Submitted successfully");
                $('#myModal').modal('hide');
                VIEW_SCREEN.show();
                ADD_SCREEN.hide();
            }           
        } else {
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
}

function file_upload_rul() {
    // console.log("inside file upload rul");
    var sessionId = client_mirror.getSessionToken();
    var fileBaseUrl = "/client/temp/upload?session_id=" +
        sessionId + "&csvid=" + CSV_ID;
    // var fileBaseUrl = "../api/bu/completed_task?session_id=" +
    //     sessionId + "&csvid=" + CSV_ID;
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
}

Dropzone.autoDiscover = false;
Dropzone.autoProcessQueue = false;
var addedfiles = [];
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
            if (jQuery.inArray(file.name, addedfiles) > -1) {
                myDropzone.removeFile(file);
            }
            if (jQuery.inArray(file.name, DOC_NAMES) == -1) {
                myDropzone.removeFile(file);
            }else if(REMAINING_DOCUMENTS == 0){
                myDropzone.removeFile(file);
                displayMessage("Required files were already added");
            } else {
                addedfiles.push(file.name);
                queueCount += 1;                
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
            if (totalfileUploadSuccess < queueCount) {
                totalfileUploadSuccess += 1;
                perQueueUploadSuccess += 1;
                UPLOADED_DOCUMENTS += 1;
                REMAINING_DOCUMENTS = TOTAL_DOCUMENTS - UPLOADED_DOCUMENTS;
            }

            if (perQueueUploadSuccess == maxParallelCount) {
                perQueueUploadSuccess = 0;
                myDropzone.processQueue();
            }
            if (totalfileUploadSuccess == DOC_NAMES.length || 
                REMAINING_DOCUMENTS == 0
            ) {
                displaySuccessMessage(message.document_upload_success);
                $('#divSuccessbutton').show();
                hideLoader();
                BTN_UPLOAD.hide();
                BUCT_PAGE.showList();
            }
            $('#bu_upload_total').text(UPLOADED_DOCUMENTS);
            $('#bu_remain_total').text(
                TOTAL_DOCUMENTS - UPLOADED_DOCUMENTS
            );
            myDropzone.removeAllFiles(true);
            hideLoader();
        });

        this.on("error", function(file, errorMessage) {
            displayMessage(errorMessage);
            addedfiles = [];
            myDropzone.removeAllFiles(true);
        });
    }
});

function BulkCompletedTaskCurrentYear() {
    this._ActionMode = null;
    this._ListDataForView = [];
}

BUCT_PAGE = new BulkCompletedTaskCurrentYear();

//initialization & master list filter
$(document).ready(function() {
    pageControls();
    BUCT_PAGE.showList();
});