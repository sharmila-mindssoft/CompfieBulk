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

                $('.invaliddata').hide();
                $('.view-summary').hide();
                $('#divFileUpload').hide();
                $('#divSuccessFile').show();
                $('#divSuccessDocument').show();
                $('#divSuccessbutton').show();

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
                $('#divSuccessDocument').hide();
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
    var legalEntityName = LegalEntityName.val();
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

$(function() {
    loadEntityDetails();

});

BulkCompletedTaskCurrentYear.prototype.possibleFailures = function(error) {
    displayMessage(error);
};

function BulkCompletedTaskCurrentYear() {}

//initialization & master list filter
$(document).ready(function() {
    pageControls();
});