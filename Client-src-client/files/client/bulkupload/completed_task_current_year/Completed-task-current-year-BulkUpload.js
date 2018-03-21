var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();

var CANCELBUTTON = $("#cancelButton");
var ADDSCREEN = $("#add-screen");
var VIEWSCREEN = $("#list-screen");
var ADDBUTTON = $("#btn-add");
var DOWNLOADBUTTON = $("#btnDownloadFile");
var DIVUPLOAD = $('#divUploadFile')
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

var unitList = [];
var domainList = [{ "d_name": "Commercial Law", "d_id": 1 }, { "d_name": "Labour Law", "d_id": 2 }];

txtdomain.keyup(function(e) {
    // var text_val = domain.val().trim();
    // var domainList = REPORT._domains;
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
    //     DIVUPLOAD.show();
    // }
    else {
        $('#downloadFormatFile').
        attr("href", "/files/client/bulkupload/Completed_Task_Current_Year-Past_Data.csv");
        $('#downloadFormatFile').
        attr("download", "/files/client/bulkupload/Completed_Task_Current_Year-Past_Data.csv");
        DIVUPLOAD.show();

    }
}

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
        DIVUPLOAD.hide();
    });

    //Add Button Click Event
    DOWNLOADBUTTON.click(function() {
        downloadData();
    });
}

//initialization & master list filter
$(document).ready(function() {
    pageControls();
});