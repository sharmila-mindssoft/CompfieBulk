var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();

var cancelButton = $("#cancelButton");
var addScreen = $("#add-screen");
var viewScreen = $("#list-screen");
var addButton = $("#btn-add");
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
    console.log(domainList);
    commonAutoComplete(e, divDomain, hdnDomain, text_val, domainList, "d_name", "d_id", function(val) {
        onAutoCompleteSuccess(txtdomain, hdnDomain, val);
    }, condition_fields, condition_values);
});

//Unit Auto Complete
txtUnit.keyup(function(e) {
    var condition_fields = [];
    var condition_values = [];
    var text_val = $(this).val();
    console.log(unitList);
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

$(function() {
    loadEntityDetails();
});

function pageControls() {
    // Cancel Button Click Event
    cancelButton.click(function() {
        viewScreen.show();
        addScreen.hide();
    });

    //Add Button Click Event
    addButton.click(function() {
        viewScreen.hide();
        addScreen.show();
    });
}

//initialization & master list filter
$(document).ready(function() {
    pageControls();
});