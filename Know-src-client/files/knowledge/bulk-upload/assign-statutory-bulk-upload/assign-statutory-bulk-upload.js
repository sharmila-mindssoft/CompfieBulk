
var DownloaFileButton = $(".btn-download-file");

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
var MultiSelect_Unit = $('#units');



function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    var current_id = id_element[0].id;
    if (current_id == 'group_id') {
        LegalEntityName.val('');
        LegalEntityId.val('');
    } else if (current_id == 'legal_entity_id') {
        fetchDomainMultiselect()
        MultiSelect_Domain.multiselect('rebuild');

        fetchUnitMultiselect()
        MultiSelect_Unit.multiselect('rebuild');
    }
}

function fetchDomainMultiselect() {
    var str = '';
    if (LEGAL_ENTITIES.length > 0) {
        for (var i in LEGAL_ENTITIES) {
            if(LEGAL_ENTITIES[i].le_id == LegalEntityId.val()){
                DOMAINS = LEGAL_ENTITIES[i].domains;
                for (var j in DOMAINS) {
                    str += '<option value="'+ DOMAINS[j].d_id +'">'+ DOMAINS[j].d_name +'</option>';
                }
            }                
        }
        MultiSelect_Domain.html(str).multiselect('rebuild');
    }
}

function fetchUnitMultiselect() {
    var str = '';
    if (UNITS.length > 0) {
        for (var i in UNITS) {
            if(UNITS[i].le_id == LegalEntityId.val() >= 0){
                str += '<option value="'+ UNITS[i].u_id +'">'+ UNITS[i].u_name +'</option>';
            }
           }
        MultiSelect_Unit.html(str).multiselect('rebuild');
    }
}


function fetchData(){
	displayLoader();
	
	bu.getClientInfo(function(error, data) {
        if (error == null) {
            GroupName.focus();
            GROUPS = data.clients;
            LEGAL_ENTITIES = data.legalentites;
            UNITS = data.units;
            hideLoader();
        } else {
            displayMessage(error);
            hideLoader();
        }
    });
}

function pageControls() {
    
    DownloaFileButton.click(function() {
        cl_id = parseInt(GroupId.val());
        le_id = parseInt(LegalEntityId.val());
        d_ids = MultiSelect_Domain.val().map(Number);
        u_ids = MultiSelect_Unit.val().map(Number);

        bu.getDownloadAssignStatutory(cl_id, le_id, d_ids, u_ids, function(error, data) {
            if (error == null) {

                var download_url = data.link;
                if (download_url != null){
                    window.open(download_url, '_blank');
                }
                else{
                    displayMessage("message.empty_export");
                }
                
            } else {
                displayMessage(error);
                hideLoader();
            }
        });

        
    });

    GroupName.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACGroup, GroupId, text_val,
            GROUPS, "cl_name", "cl_id",
            function(val) {
                onAutoCompleteSuccess(GroupName, GroupId, val);
            });
    });

    LegalEntityName.keyup(function(e) {
        if (GroupId.val() != '') {
            var condition_fields = ["cl_id"];
            var condition_values = [GroupId.val()];
            
            var text_val = $(this).val();
            commonAutoComplete(
                e, ACLegalEntity, LegalEntityId, text_val,
                LEGAL_ENTITIES, "le_name", "le_id",
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
    MultiSelect_Domain.multiselect({
        buttonWidth: '100%'
    });
    MultiSelect_Unit.multiselect({
        buttonWidth: '100%'
    });
    initialize();
});