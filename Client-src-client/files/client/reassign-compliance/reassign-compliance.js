var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();

var LegalEntityNameLabel = $(".legal-entity-name");
var LegalEntityNameAC = $(".legal-entity-name-ac");

var LegalEntityName = $("#legal_entity_name");
var LegalEntityId = $("#legal_entity_id");
var ACLegalEntity = $("#ac-entity");

var DomainName = $("#domain_name");
var DomainId = $("#domain_id");
var ACDomain = $("#ac-domain");

var UserName = $("#user_name");
var UserId = $("#user_id");
var ACUser = $("#ac-user");

var UnitName = $("#unit_name");
var UnitId = $("#unit_id");
var ACUnit = $("#ac-unit");

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    var current_id = id_element[0].id;
    if (current_id == 'legal_entity_id') {
        DomainName.val('');
        DomainId.val('');
        UserName.val('');
        UserId.val('');
        UnitName.val('');
        UnitId.val('');

        client_mirror.getReassignComplianceFilters(parseInt(val[0]),
            function(error, data) {
                if (error == null) {
                    //UNITS = data.statutories;
                } else {
                    displayMessage(error);
                }
        });


        
    } else if (current_id == 'domain_id') {
        UserName.val('');
        UserId.val('');
        UnitName.val('');
        UnitId.val('');
    } else if (current_id == 'user_id') {
        UnitName.val('');
        UnitId.val('');
    }
    /*UnitList.empty();
    ACTIVE_UNITS = [];*/
}

function pageControls(){
	LegalEntityName.keyup(function(e) {
        var condition_fields = [];
        var condition_values = [];
       
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACLegalEntity, LegalEntityId, text_val,
            LEGAL_ENTITIES, "le_name", "le_id",
            function(val) {
                onAutoCompleteSuccess(LegalEntityName, LegalEntityId, val);
            }, condition_fields, condition_values);
        
    });
}

function loadEntityDetails(){
    if(LEGAL_ENTITIES.length > 1){
        LegalEntityNameLabel.hide();
        LegalEntityNameAC.show();
        /*var no_record_row = $("#templates .table-no-record tr");
        var clone = no_record_row.clone();
        StatutorySettingsList.append(clone);
        SelectedUnitView.hide();
        EditButton.hide();*/
    }else{
        var LE_NAME = LEGAL_ENTITIES[0]["le_name"];
        var LE_ID = LEGAL_ENTITIES[0]["le_id"];
     
        LegalEntityNameLabel.show();
        LegalEntityNameAC.hide();
        LegalEntityNameLabel.text(LE_NAME);
        LegalEntityId.val(LE_ID);
        //Show.trigger( "click" );
    }
}

function initialize() {
    pageControls();
    //callAPI(API_FILTERS);
    loadEntityDetails();
    //showList();
}


$(function() {
    initialize();
});
