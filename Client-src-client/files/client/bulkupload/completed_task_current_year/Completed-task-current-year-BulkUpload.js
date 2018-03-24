var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();

var CANCELBUTTON = $("#cancelButton");
var ADDSCREEN = $("#add-screen");
var VIEWSCREEN = $("#list-screen");
var ADDBUTTON = $("#btn-add");
var DOWNLOADBUTTON = $("#btnDownloadFile");
var DIVUPLOAD = $('#divUploadFile');
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
        unitsList = data["in_units"];

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
    var legalEntityName = LegalEntityName.val();
    var domainName = txtdomain.val();    
    var unitName = txtUnit.val();
    //Todo Get Unit Code 
    var unitCode = "unitCode";
    var leId = LegalEntityId.val();
    var domainId = hdnDomain.val();
    var unitId = hdnUnit.val();
    var frequency = "Periodical";
    var startCount = 0;

    buClient.getDownloadData(
        parseInt(leId), parseInt(domainId), parseInt(unitId), frequency, startCount,
        legalEntityName, domainName, unitName, unitCode,
        function(error, data) {
            if (error == null) {
                    var download_url = data.link;
                    if (download_url != null){
                        window.open(download_url, '_blank');
                        hideLoader();
                    }
                    else{
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