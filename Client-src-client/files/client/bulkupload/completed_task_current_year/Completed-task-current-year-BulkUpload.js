var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();

var CANCELBUTTON = $("#cancelButton");
var ADDSCREEN = $("#add-screen");
var VIEWSCREEN = $("#list-screen");
var ADDBUTTON = $("#btn-add");
var DOWNLOADBUTTON = $("#btnDownloadFile");
var DIVUPLOAD = $('#divUploadFile');
var UploadFile = $("#fileInput");
var LegalEntityNameLabel = $(".legal-entity-name");
var LegalEntityNameAC = $(".legal-entity-name-ac");
var LegalEntityId = $("#legal_entity_id");
var LegalEntityName = $("#legal_entity_name");
var ACLegalEntity = $("#ac-entity");

var txtdomain = $("#txtdomain");
var hdnDomain = $("#hdnDomain");
var divDomain = $("#divDomain");

var txtUnit = $('#txtUnit');
var hdnUnit = $('#hdnUnit');
var divUnit = $('#divUnit');

var BTNUPLOAD = $('#btnUpload');

var unitList = [];
var domainList = [];
var csvInfo = null;

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

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    if (id_element[0].id == 'legal_entity_id') {
        // REPORT.fetchDomainList(countryId.val(), val[0]);
        getPastRecords(parseInt(LegalEntityId.val()));
        loadUnits(parseInt(LegalEntityId.val()));
    }
}

function loadEntityDetails() {
    if (LEGAL_ENTITIES.length > 1) {
        LegalEntityNameLabel.hide();
        LegalEntityNameAC.show();
    } else {
        var LE_NAME = LEGAL_ENTITIES[0]["le_name"];
        var LE_ID = LEGAL_ENTITIES[0]["le_id"];

        LegalEntityNameLabel.show();
        LegalEntityNameAC.hide();

        LegalEntityNameLabel.text(LE_NAME);
        LegalEntityId.val(LE_ID);

        loadUnits(parseInt(LegalEntityId.val()));
        // ShowButton.trigger("click");
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

function downloadData() {
    if (LegalEntityName.val().trim() == "") {
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

    // else if (txtUnit.val().trim() == "South Unit 15" && txtdomain.val().trim() == "Labour Law") {
    //     $('#downloadFormatFile').
    //     attr("href", "/files/client/bulkupload/Completed_Task_Current_Year-Past_Data.csv");
    //     $('#downloadFormatFile').
    //     attr("download", "/files/client/bulkupload/Completed_Task_Current_Year-Past_Data.csv");
    // }
    // else {
    //     $('#downloadFormatFile').
    //     attr("href", "/files/client/bulkupload/Completed_Task_Current_Year-Past_Data.csv");
    //     $('#downloadFormatFile').
    //     attr("download", "/files/client/bulkupload/Completed_Task_Current_Year-Past_Data.csv");
    // }

    // $('#fileInput').val()
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
            $('#divSuccessFile').show();
            $('#divSuccessDocument').show();
            $('#divSuccessbutton').show();
        }, 2000);

        var args = {
            "csv_name": csvInfo["file_name"],
            "csv_data": csvInfo["file_content"],
            "csv_size": csvInfo["file_size"],
            "legal_entity_id": parseInt(LegalEntityId.val())
                // "d_id": hdnDomain.val(),
                // "unit_id": hdnUnit.val()
        };

        buClient.UploadCompletedTaskCurrentYearCSV(args, function(error, data) {
            if (error == null) {
                // TotalRecordsCount.text(data.total);
                // ValidRecordsCount.text(parseInt(data.valid) - parseInt(data.invalid));
                // InvalidRecordsCount.text(data.invalid);
                // InvalidFileName = null;
                // MandatoryErrorsCount.text("0");
                // DuplicateErrorsCount.text("0");
                // StatusErrorsCount.text("0");
                // LengthErrorsCount.text("0");
                // InvalidErrorsCount.text("0");
                // $('.view-summary').show();
                // $('.invaliddata').hide();
                displaySuccessMessage("Records uploaded successfully for approval");
                hideLoader();
            } else {
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
        // DIVUPLOAD.hide();
    });

    //Add Button Click Event
    DOWNLOADBUTTON.click(function() {
        downloadData();
    });

    //Upload Button Click Event
    BTNUPLOAD.click(function() {
        validateUpload();
    });


}

BulkCompletedTaskCurrentYear.prototype.possibleFailures = function(error) {
    displayMessage(error);
};

function BulkCompletedTaskCurrentYear() {}

//initialization & master list filter
$(document).ready(function() {
    pageControls();
});