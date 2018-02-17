
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

var u_names = [];
var u_ids = [];
var d_names = [];
var d_ids = [];


function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    var current_id = id_element[0].id;
    if (current_id == 'group_id') {
        LegalEntityName.val('');
        LegalEntityId.val('');
        u_names = [];
        u_ids = [];
        d_names = [];
        d_ids = [];
        fetchDomainMultiselect()
        MultiSelect_Domain.multiselect('rebuild');
        fetchUnitMultiselect()
        MultiSelect_Unit.multiselect('rebuild');
    } else if (current_id == 'legal_entity_id') {
        u_names = [];
        u_ids = [];
        d_names = [];
        d_ids = [];
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
            if(UNITS[i].le_id == LegalEntityId.val()){
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
        cl_id = GroupId.val();
        le_id = LegalEntityId.val();
        cl_name = GroupName.val();
        le_name = LegalEntityName.val();
        
    
        if (cl_id.trim().length <= 0) {
            displayMessage(message.client_required);
            return false;
        } else if (le_id.trim().length <= 0) {
            displayMessage(message.legalentity_required);
            return false;
        } else if (MultiSelect_Domain.val() == null) {
            displayMessage(message.domain_required);
            return false;
        } else {
            d_ids = MultiSelect_Domain.val().map(Number);
            d_names = [];
            $("#domains option:selected").each(function () {
               var $this = $(this);
               if ($this.length) {
                d_names.push($this.text());
               }
            });

            u_names = [];
            u_ids = [];
            if(MultiSelect_Unit.val() == null){
                for (var i in UNITS) {
                    u_names.push(UNITS[i].u_name.split('-').pop());
                    u_ids.push(UNITS[i].u_id)
                }
            }else{
                $("#units option:selected").each(function () {
                   var $this = $(this);
                   if ($this.length) {
                    var selText = $this.text().split('-').pop();
                    u_names.push(selText);
                   }
                });
                u_ids = MultiSelect_Unit.val().map(Number);
            }

            displayLoader();
            bu.getDownloadAssignStatutory(parseInt(cl_id), parseInt(le_id), d_ids, u_ids, cl_name, le_name, d_names, u_names, function(error, data) {
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
        }
    });

    MultiSelect_Domain.change(function(e) {
        u_names = [];
        u_ids = [];
        fetchUnitMultiselect()
        MultiSelect_Unit.multiselect('rebuild');
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