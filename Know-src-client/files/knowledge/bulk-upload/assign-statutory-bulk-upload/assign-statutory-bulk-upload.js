var GROUPS = null;
var LEGAL_ENTITIES = null;
var UNITS = null;
var DOMAINS = null;

var GroupName = $('#group_name');
var GroupId = $("#group_id");
var ACGroup = $("#ac-group");

var LegalEntityName = $("#legal_entity_name");
var LegalEntityId = $("#legal_entity_id");
var ACLegalEntity = $("#ac-entity");


var MultiSelect_Domain = $('#domains');



function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    var current_id = id_element[0].id;
    if (current_id == 'group_id') {
        LegalEntityName.val('');
        LegalEntityId.val('');
    } else if (current_id == 'legal_entity_id') {
        
    }
}

function fetchCountryMultiselect() {
    var str = '';
    if (DOMAINS.length > 0) {
        for (var i in DOMAINS) {
            d = DOMAINS[i];
            if (d.is_active == true) {
                var selected = '';
                //if ($.inArray(d.country_id, d_page._country_ids) >= 0)
                if (d_page._country_ids.indexOf(d.country_id) >= 0){
                    selected = ' selected ';
                    disabled = ' disabled ';
                }
                else{
                    selected = '';
                    disabled = '';
                }
                str += '<option value="'+ d.country_id +'" '+ selected +' '+ disabled +'>'+ d.country_name +'</option>';
            }
           }
        MultiSelect_Domain.html(str).multiselect('rebuild');
    }
}

function fetchData(){
	displayLoader();
	
	bu.getClientInfo(function(error, data) {
        if (error == null) {
            GroupName.focus();
            GROUPS = data.grps;
            LEGAL_ENTITIES = data.lety;
            DOMAINS = data.dms;
            hideLoader();


            fetchCountryMultiselect()
    		MultiSelect_Domain.multiselect('rebuild');
        } else {
            displayMessage(error);
            hideLoader();
        }
    });
}

function pageControls() {
    
    GroupName.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACGroup, GroupId, text_val,
            GROUPS, "group_name", "client_id",
            function(val) {
                onAutoCompleteSuccess(GroupName, GroupId, val);
            });
    });

    LegalEntityName.keyup(function(e) {
        if (GroupId.val() != '') {
            var condition_fields = ["client_id"];
            var condition_values = [GroupId.val()];
            
            var text_val = $(this).val();
            commonAutoComplete(
                e, ACLegalEntity, LegalEntityId, text_val,
                LEGAL_ENTITIES, "legal_entity_name", "legal_entity_id",
                function(val) {
                    onAutoCompleteSuccess(LegalEntityName, LegalEntityId, val);
                }, condition_fields, condition_values);
        }
    });
}

function initialize() {
	fetchData();
    pageControls();
    
}

$(function() {
    initialize();
});