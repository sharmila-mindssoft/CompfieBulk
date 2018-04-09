var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();

var CANCELBUTTON = $("#cancelButton");
var ADDSCREEN = $("#add-screen");
var VIEWSCREEN = $("#list-screen");
var ADDBUTTON = $("#btn-add");
var DOWNLOADBUTTON = $("#btnDownloadFile");
var SUBMITBUTTON = $(".btn_submit");

var DIVUPLOAD = $('#divUploadFile');
var UploadFile = $("#fileInput");
var LegalEntityNameLabel = $(".legal-entity-name");
var LEGALENTITYNAMELABELUPLOAD = $(".legal-entity-name-upload");

var LegalEntityNameAC = $(".legal-entity-name-ac");
var LEGALENTITYNAMEACUPLOAD = $(".legal-entity-name-ac-upload");

var LegalEntityId = $("#legal_entity_id");
var LEGALENTITYIDUPLOAD = $("#legal_entity_id_upload");

var LegalEntityName = $("#legal_entity_name");
var LEGALENTITYNAMEUPLOAD = $("#legal_entity_name_upload");

var ACLegalEntity = $("#ac-entity");
var ACLEGALENTITYUPLOAD = $("#ac-entity-upload");

var txtdomain = $("#txtdomain");
var hdnDomain = $("#hdnDomain");
var divDomain = $("#divDomain");

var txtUnit = $('#txtUnit');
var hdnUnit = $('#hdnUnit');
var divUnit = $('#divUnit');

var BTNUPLOAD = $('#btnUpload');

var unitList = [];
var domainList = [];
var docNames = [];
var csvInfo = null;
var csvId = null;
var buCtPage = null;

//error description variable declaration
var TOTALRECORD = $('.totalRecords');
var VALIDRECORD = $('.validRecords');
var INVALIDRECORD = $('.invalidRecords');
var MANDATORYERROR = $('.mandatoryErrors');
var DUPLICATEERROR = $('.duplicateErrors');
var STATUSERROR = $('.statusErrors');
var LENGTHERROR = $('.lengthErrors');
var INVALIDERROR = $('.invalidErrors');
var INVALIDFILENAME = null;

var unit_list_map = {};


txtdomain.keyup(function(e) {
    var condition_fields = [];
    var condition_values = [];
    var text_val = $(this).val();
    commonAutoComplete(e, divDomain, hdnDomain, text_val, domainList,
        "d_name", "d_id",
        function(val) {
            onAutoCompleteSuccess(txtdomain, hdnDomain, val);
        }, condition_fields, condition_values);
});

//Unit Auto Complete
txtUnit.keyup(function(e) {
    var condition_fields = [];
    var condition_values = [];
    var text_val = $(this).val();
    commonAutoComplete(
        e, divUnit, hdnUnit, text_val,
        unitList, "unit_name", "unit_id",
        function(val) {
            onAutoCompleteSuccess(txtUnit, hdnUnit, val);
        }, condition_fields, condition_values);
});

function loadUnits(le_id, unit_id) {
    client_mirror.complianceFilters(le_id, function(error, response) {
        if (error == null) {
            unitList = response.user_units;
            $.each(unitList, function(key, u) {
                unit_list_map[parseInt(u["unit_id"])] = u["unit_code"]
            });
        }
    });
}
LegalEntityName.keyup(function(e) {
    var text_val = $(this).val();
    commonAutoComplete(
        e, ACLegalEntity, LegalEntityId, text_val,
        LEGAL_ENTITIES, "le_name", "le_id",
        function(val) {
            onAutoCompleteSuccess(LegalEntityName, LegalEntityId, val);
        });
});
LEGALENTITYNAMEUPLOAD.keyup(function(e) {
    var text_val = $(this).val();
    commonAutoComplete(
        e, ACLEGALENTITYUPLOAD, LEGALENTITYIDUPLOAD, text_val,
        LEGAL_ENTITIES, "le_name", "le_id",
        function(val) {
            onAutoCompleteSuccess(LEGALENTITYNAMEUPLOAD, LEGALENTITYIDUPLOAD, val);
        });
});




function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    if (id_element[0].id == 'legal_entity_id') {
        getPastRecords(parseInt(LegalEntityId.val()));
        loadUnits(parseInt(LegalEntityId.val()));
    }
}

function loadEntityDetails() {
    if (LEGAL_ENTITIES.length > 1) {
        LegalEntityNameLabel.hide();
        LEGALENTITYNAMELABELUPLOAD.hide();
        LegalEntityNameAC.show();
        LEGALENTITYNAMEACUPLOAD.show();
    } else {
        var LE_NAME = LEGAL_ENTITIES[0]["le_name"];
        var LE_ID = LEGAL_ENTITIES[0]["le_id"];

        LegalEntityNameLabel.show();
        LEGALENTITYNAMELABELUPLOAD.show();
        LegalEntityNameAC.hide();
        LEGALENTITYNAMEACUPLOAD.hide();

        LegalEntityNameLabel.text(LE_NAME);
        LEGALENTITYNAMELABELUPLOAD.text(LE_NAME);
        LegalEntityId.val(LE_ID);
        // LEGALENTITYIDUPLOAD

        loadUnits(parseInt(LegalEntityId.val()));
        // ShowButton.trigger("click");
        getPastRecords(parseInt(LegalEntityId.val()));
    }
}

function getPastRecords(legalEntity) {
    displayLoader();

    function onSuccess(data) {
        // unitsList = data["in_units"];
        domainList = data.domains;
        // loadUnit();
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
    if ($('#fileInput').val() == "") {
        displayMessage("Select file to upload");
        $('#myModal').modal('show');
        return false;
    } else {
        setTimeout(function() {
            // $('.invaliddata').show();
            // $('.view-summary').show();
            // $('#divSuccessFile').show();
            // $('#divSuccessDocument').show();
            // $('#divSuccessbutton').show();
        }, 1000);

        console.log("_ActionMode>>", buCtPage._ActionMode);
        if (buCtPage._ActionMode == "add") {

            var args = {
                "csv_name": csvInfo["file_name"],
                "csv_data": csvInfo["file_content"],
                "csv_size": csvInfo["file_size"],
                "legal_entity_id": parseInt(LegalEntityId.val())
            };

            buClient.UploadCompletedTaskCurrentYearCSV(args, function(error, data) {
                if (error == null) {
                    TOTALRECORD.text(data.total);
                    VALIDRECORD.text(parseInt(data.valid) -
                        parseInt(data.invalid));
                    INVALIDRECORD.text(data.invalid);
                    INVALIDFILENAME = null;
                    MANDATORYERROR.text("0");
                    DUPLICATEERROR.text("0");
                    STATUSERROR.text("0");
                    LENGTHERROR.text("0");
                    INVALIDERROR.text("0");
                    $('.view-summary').hide();
                    $('.dropbtn').hide();
                    $('#hdnCsvId').val(data.new_csv_id);
                    csvId = data.new_csv_id;
                    $('.successFileName').text(data.csv_name);
                    csv_path = "../../../../../uploaded_file/csv/" + data.csv_name;
                    $('.uploaded_data').attr("href", csv_path);
                    $('.uploaded_data').attr("download", csv_path);
                    // attr("href", "/files/client/bulkupload/Completed_Task_Current_Year-Past_Data.csv");

                    $('.invaliddata').hide();
                    $('.view-summary').hide();
                    $('#divFileUpload').hide();
                    $('#divSuccessFile').show();
                    $('.divSuccessDocument').show();
                    $('#divSuccessbutton').hide();
                    buCtPage._ActionMode = "upload";

                    displaySuccessMessage("Records uploaded successfully");
                    hideLoader();
                } else {
                    displayMessage(message.upload_failed);
                    INVALIDFILENAME = data.invalid_file.split('.');
                    TOTALRECORD.text(data.total);
                    var getValidCount = (parseInt(data.total) -
                        parseInt(data.invalid));
                    VALIDRECORD.text(getValidCount);
                    INVALIDRECORD.text(data.invalid);
                    MANDATORYERROR.text(data.mandatory_error);
                    DUPLICATEERROR.text(data.duplicate_error);
                    STATUSERROR.text(data.inactive_error);
                    LENGTHERROR.text(data.max_length_error);
                    getInvaliddataCount = parseInt(data.invalid_char_error) +
                        parseInt(data.invalid_data_error);
                    INVALIDERROR.text(getInvaliddataCount);
                    $('.dropbtn').show();
                    $('.view-summary').show();

                    $('.invaliddata').show();
                    $('.view-summary').show();
                    $('#divFileUpload').show();
                    $('#divSuccessFile').hide();
                    $('.divSuccessDocument').hide();
                    $('#divSuccessbutton').hide();

                    csv_path = "/invalid_file/csv/" + INVALIDFILENAME[0] +
                        '.csv';
                    xls_path = "/invalid_file/xlsx/" + INVALIDFILENAME[0] +
                        '.xlsx';
                    ods_path = "/invalid_file/ods/" + INVALIDFILENAME[0] +
                        '.ods';
                    txt_path = "/invalid_file/txt/" + INVALIDFILENAME[0] +
                        '.txt';
                    $('#csv').attr("href", csv_path);
                    $('#excel').attr("href", xls_path);
                    $('#ods').attr("href", ods_path);
                    $('#txt').attr("href", txt_path);

                    // InvalidFileName = data.invalid_file.split('.');;
                    // TotalRecordsCount.text(data.total);
                    // var getValidCount = (parseInt(data.total) - parseInt(data.invalid));
                    // ValidRecordsCount.text(getValidCount);
                    // InvalidRecordsCount.text(data.invalid);
                    // MandatoryErrorsCount.text(data.mandatory_error);
                    // DuplicateErrorsCount.text(data.duplicate_error);
                    // StatusErrorsCount.text(data.inactive_error);
                    // LengthErrorsCount.text(data.max_length_error);
                    // getInvaliddataCount = parseInt(data.invalid_char_error) + parseInt(data.invalid_data_error);
                    // InvalidErrorsCount.text(getInvaliddataCount);
                    // $('.invaliddata').show();
                    // $('.view-summary').show();

                    // csv_path = "/invalid_file/csv/" + InvalidFileName[0] + '.csv';
                    // xls_path = "/invalid_file/xlsx/" + InvalidFileName[0] + '.xlsx';
                    // ods_path = "/invalid_file/ods/" + InvalidFileName[0] + '.ods';
                    // txt_path = "/invalid_file/txt/" + InvalidFileName[0] + '.txt';
                    // $('#csv').attr("href", csv_path);
                    // $('#excel').attr("href", xls_path);
                    // $('#ods').attr("href", ods_path);
                    // $('#txt').attr("href", txt_path);
                    hideLoader();
                }
            });
        } else {
            myDropzone.processQueue();
        }
    }
}

UploadFile.change(function(e) {
    if ($(this).val() != '') {
        buClient.uploadCSVFile(e, function(status, response) {
            if (status == false) {
                displayMessage(response);
            } else {
                csvInfo = response;
            }
        });
    }
});

$(function() {
    loadEntityDetails();

});

function pageControls() {
    // Cancel Button Click Event
    CANCELBUTTON.click(function() {
        VIEWSCREEN.show();
        ADDSCREEN.hide();
    });

    //Add Button Click Event
    ADDBUTTON.click(function() {
        VIEWSCREEN.hide();
        ADDSCREEN.show();
        buCtPage._ActionMode = "add";
    });

    //Add Button Click Event
    DOWNLOADBUTTON.click(function() {
        downloadData();
    });

    //Upload Button Click Event
    BTNUPLOAD.click(function() {
        validateUpload();
    });

    SUBMITBUTTON.click(function() {
        submitUpload();
    });
}

BulkCompletedTaskCurrentYear.prototype.possibleFailures = function(error) {
    displayMessage(error);
};

function downloadData() {
    if (LegalEntityId.val().trim() == "") {
        displayMessage(message.legalentity_required);
        LegalEntityName.focus();
        return false;
    }
    if (txtdomain.val().trim() == "") {
        displayMessage(message.domain_required);
        txtdomain.focus();
        return false;
    }
    if (txtUnit.val().trim() == "") {
        displayMessage(message.unit_required);
        txtUnit.focus();
        return false;
    }
    var legalEntityName = LegalEntityNameLabel.text();
    var domainName = txtdomain.val();
    var unitName = txtUnit.val();
    var leId = LegalEntityId.val();
    var domainId = hdnDomain.val();
    var unitId = hdnUnit.val();
    var unitCode = unit_list_map[unitId];
    var frequency = "Periodical";
    var startCount = 0;

    buClient.getDownloadData(
        parseInt(leId), parseInt(domainId), parseInt(unitId), frequency, startCount,
        legalEntityName, domainName, unitName, unitCode,
        function(error, data) {
            if (error == null) {
                var download_url = data.link;
                if (download_url != null) {
                    window.open(download_url, '_blank');
                    hideLoader();
                } else {
                    displayMessage("message.empty_export");
                    hideLoader();
                }
            } else {
                displayMessage(error);
                hideLoader();
            }
        }
    );
}

function submitUpload() {

    var args = {
        "new_csv_id": parseInt($('#hdnCsvId').val()),
        "legal_entity_id": parseInt(LegalEntityId.val())
    };

    buClient.saveBulkRecords(args, function(error, data) {
        if (error == null) {
            VIEWSCREEN.show();
            ADDSCREEN.hide();
            displaySuccessMessage("Record Submitted successfully");
        } else {

        }
    });
}



$(function() {
    loadEntityDetails();

});

BulkCompletedTaskCurrentYear.prototype.possibleFailures = function(error) {
    displayMessage(error);
};

function file_upload_rul() {
    var session_id = client_mirror.getSessionToken();

    var file_base_url = "/temp/upload?session_id=" +
        session_id + "&csvid=" + csvId;
    console.log(file_base_url);
    return file_base_url;
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
            console.log("1>> " + file.name);
            console.log(">> " + jQuery.inArray(file.name, addedfiles));
            console.log("docNames>> " + jQuery.inArray(file.name, docNames));
            if (jQuery.inArray(file.name, addedfiles) > -1) {
                console.log("addedfiles part");
                myDropzone.removeFile(file);
            }
            if (jQuery.inArray(file.name, docNames) > -1) {
                console.log("docNames part");
                myDropzone.removeFile(file);
            } else {
                console.log("else part");
                addedfiles.push(file.name);
                queueCount += 1;
            }
        });
        this.on("removedfile", function(file) {
            console.log(file.name);
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
            }

            if (perQueueUploadSuccess == maxParallelCount) {
                perQueueUploadSuccess = 0;
                myDropzone.processQueue();
            }
            if (totalfileUploadSuccess == queueCount) {
                myDropzone.removeAllFiles(true);
                hideLoader();
                displaySuccessMessage(message.document_upload_success);
                // buSmPage.showList();
            }
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
}

buCtPage = new BulkCompletedTaskCurrentYear();

//initialization & master list filter
$(document).ready(function() {
    pageControls();
});