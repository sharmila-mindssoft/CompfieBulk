var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();
var DOMAINS = null;
var UNITS = null;
var USERS = null;
var REASSIGN_UNITS = null;

var NextButton = $('#btn-next');
var PreviousButton = $('#btn-previous');
var SubmitButton = $("#btn-submit");
var ShowMore = $(".btn-showmore");
var CancelButton = $('#btn-cancel');

var ReassignView = $("#reassigncompliance-view");
var ReassignAdd = $("#reassigncompliance-add");

var ShowButton = $(".btn-show");
var ReassignButton = $(".btn-reassign");

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

var UserType = $("#user_type");



var UnitList = $(".tbody-unit-list");
var UnitRow = $("#templates .table-unit .table-row");
var UserTypeRow = $("#templates .table-unit .table-type-row");

var SelectedUnitCount = $(".selected_checkbox_count");
var SelectedUnitView = $(".selected_checkbox");

var ACTIVE_UNITS = [];
var LastUserType = '';
var UTYPE = 0;

var REASSIGN_FILTER = "reassign_filter";
var GET_COMPLIANCE = "get_compliance";
function callAPI(api_type) {
    if (api_type == REASSIGN_FILTER) { 
        displayLoader();
        client_mirror.getReassignComplianceFilters(parseInt(LegalEntityId.val()),
            function(error, data) {
                if (error == null) {
                	DOMAINS = data.domains;
                    UNITS = data.units;
                    USERS = data.legal_entity_users;
                } else {
                    displayMessage(error);
                }
        });
    }

    else if (api_type == GET_COMPLIANCE) { 
        displayLoader();
        var val_legal_entity_id = LegalEntityId.val();
	    var val_domain_id = DomainId.val();
	    var val_user_id = UserId.val();
        client_mirror.getReAssignComplianceForUnits(int(val_legal_entity_id), 
            int(val_domain_id), int(val_user_id), UTYPE, ACTIVE_UNITS, 0,
        	function(error, data) {
            if (error == null) {
                //ComplianceList = data.assign_statutory;
                //ActList = data.level_one_name;
                //loadCompliances();
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    }

    /*else if (api_type == WIZARD_ONE_UNIT_FILTER) { 
        displayLoader();
        var le_id = LEList.find("li.active").attr("id");
        var d_id = DomainList.find("li.active").attr("id");
        client_mirror.getAssignComplianceUnits(parseInt(le_id), parseInt(d_id), function(error, data) {
            if (error == null) {
                UNITS = data.assign_units;
                FREQUENCY = data.comp_frequency;
                loadUnit();
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    } 
	*/
}

function getNoRecord(){
	SelectedUnitView.hide();
    var no_record_row = $("#templates .table-no-record tr");
    var clone = no_record_row.clone();
    UnitList.append(clone);
}

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

        callAPI(REASSIGN_FILTER);
    } else if (current_id == 'domain_id') {
        UserName.val('');
        UserId.val('');
        UnitName.val('');
        UnitId.val('');
    } else if (current_id == 'user_id') {
        UnitName.val('');
        UnitId.val('');
    }
    UnitList.empty();
    getNoRecord();
    ACTIVE_UNITS = [];
}

function int(val) {
    try {
        value = val.trim();
        value = parseInt(value);
        return value;
    } catch (e) {
        return null;
    }
}

function activateUnit(element) {
    var chkid = $(element).val();
    var cName = $(element).attr("class").split(' ').pop();
    if ($(element).prop("checked")) {
    	if(cName == 'type1'){
    		$('.type2').prop("checked", false);
    		$('.type3').prop("checked", false);
    	}
    	else if(cName == 'type2'){
    		$('.type1').prop("checked", false);
    		$('.type3').prop("checked", false);
    	}
    	else if(cName == 'type3'){
    		$('.type1').prop("checked", false);
    		$('.type2').prop("checked", false);
    	}
        $(this).prop("checked", true);
    }

    //alert($('.unit-checkbox:checked').length)
    SelectedUnitCount.text($('.unit-checkbox:checked').length);
}

function getCompliance(e, type){
	$('.unit-checkbox:checkbox:checked').each(function (index, el) {
        var id = $(this).val();
        ACTIVE_UNITS.push(parseInt(id));
    });

    if (ACTIVE_UNITS.length == 0) {
        displayMessage(message.atleast_one_unit_required)
        return false;
    } else {
    	/*ShowMore.hide();
        SubmitButton.hide();
        PreviousButton.hide();
        ReassignView.hide();
        ReassignAdd.show();*/
        UTYPE = type;
        callAPI(GET_COMPLIANCE);

        /*$(".total_count_view").hide();
        LastAct = '';
        LastSubAct = '';
        statutoriesCount = 1;
        actCount = 1;
        count = 1;
        sno = 1;
        totalRecord = 0;
        AssignStatutoryList.empty();
        SingleAssignStatutoryList.empty();
        SELECTED_COMPLIANCE = {};
        ACT_MAP = {};
        return true;*/
    }
}
function loadUnits() {
    //C_COUNT = 0;
    //UNIT_CS_ID = {};
    UnitList.empty();
    $.each(REASSIGN_UNITS, function(key, value) {
    	var rbutton = false;
    	if(LastUserType != value.user_type_id){
    		var u_type = '';
    		if(value.user_type_id == 1) {
    			u_type = 'Assignee';
    		}
    		else if(value.user_type_id == 2) {
    			u_type = 'Concurrence';
    		}
    		else if(value.user_type_id == 3) {
    			u_type = 'Approver';
    		}
    		var type_clone = UserTypeRow.clone();
	        $('.tbl_user_type', type_clone).text(u_type);
	       	UnitList.append(type_clone);

	       	LastUserType = value.user_type_id;
	       	rbutton = true;
    	}
        
        var clone = UnitRow.clone();
        $('.unit-checkbox', clone).attr('id', 'unit' + key);
        $('.unit-checkbox', clone).val(value.u_id);
        
        if(value.user_type_id == 1) {
			$('.unit-checkbox', clone).addClass('type1');
		}
		else if(value.user_type_id == 2) {
			$('.unit-checkbox', clone).addClass('type2');
		}
		else if(value.user_type_id == 3) {
			$('.unit-checkbox', clone).addClass('type3');
		}

        $('.tbl_unit', clone).text(value.u_name);
        $('.tbl_address', clone).attr('title', value.address + ', ' + value.postal_code);
        $('.tbl_no_of_compliance', clone).text(value.no_of_compliances);
        $('.unit-checkbox', clone).on('click', function(e) {
            activateUnit(this);
        });
        if(rbutton){
        	if(value.user_type_id == 1) {
        		$('.tbl_reassign', clone).on('click', function(e) {
		            getCompliance(this, 1);
		        });
			}
			else if(value.user_type_id == 2) {
				$('.tbl_reassign', clone).on('click', function(e) {
		            getCompliance(this, 2);
		        });
			}
			else if(value.user_type_id == 3) {
				$('.tbl_reassign', clone).on('click', function(e) {
		            getCompliance(this, 3);
		        });
			}
        }else{
        	$('.tbl_reassign', clone).hide();
        }
        //UNIT_CS_ID[value.u_id] = value.u_name;
        UnitList.append(clone);
    });

    if(REASSIGN_UNITS.length == 0){
        getNoRecord();
    }else{
        SelectedUnitView.show();
    }
   
}

function validateAndShow() {
    val_legal_entity_id = LegalEntityId.val();
    val_domain_id = DomainId.val();
    val_user_id = UserId.val();
    val_user_type = UserType.val();
    val_unit_id = UnitId.val();


    if (val_legal_entity_id.trim().length <= 0) {
        displayMessage(message.legalentity_required);
        return false;
    } else if (val_domain_id.trim().length <= 0) {
        displayMessage(message.domain_required);
        return false;
    } else if (val_user_id.trim().length <= 0) {
        displayMessage(message.user_required);
        return false;
    } else {
        displayLoader();
        client_mirror.getReAssignComplianceUnits(int(val_legal_entity_id), 
            int(val_domain_id), int(val_user_id), int(val_user_type), int(val_unit_id), 
            function(error, data) {
                if (error == null) {
                    REASSIGN_UNITS = data.reassign_units;
                    loadUnits();
                    hideLoader();
                } else {
                    displayMessage(error);
                    hideLoader();
                }
            });
    }
}

function pageControls(){
	ShowButton.click(function() {
		LastUserType = '';
        validateAndShow();
    });

    CancelButton.click(function() {
        ReassignView.show();
        ReassignAdd.hide();
    });

	LegalEntityName.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACLegalEntity, LegalEntityId, text_val,
            LEGAL_ENTITIES, "le_name", "le_id",
            function(val) {
                onAutoCompleteSuccess(LegalEntityName, LegalEntityId, val);
            });
    });

    DomainName.keyup(function(e) {
        var condition_fields = ['is_active'];
        var condition_values = [true];
   
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACDomain, DomainId, text_val,
            DOMAINS, "d_name", "d_id",
            function(val) {
                onAutoCompleteSuccess(DomainName, DomainId, val);
            }, condition_fields, condition_values);
          
    });

    UserName.keyup(function(e) {
        var condition_fields = ['is_active'];
        var condition_values = [true];
   
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACUser, UserId, text_val,
            USERS, "employee_name", "user_id",
            function(val) {
                onAutoCompleteSuccess(UserName, UserId, val);
            }, condition_fields, condition_values);
          
    });

    UnitName.keyup(function(e) {
        var condition_fields = ['is_closed'];
        var condition_values = [false];
   		
   		if(DomainId.val() != ''){
   			condition_fields.push("d_ids");
   			condition_values.push(DomainId.val())
   			var text_val = $(this).val();
	        commonAutoComplete(
	            e, ACUnit, UnitId, text_val,
	            UNITS, "unit_name", "unit_id",
	            function(val) {
	                onAutoCompleteSuccess(UnitName, UnitId, val);
	            }, condition_fields, condition_values);
   		}
        
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
        callAPI(REASSIGN_FILTER);
        //Show.trigger( "click" );
    }
    getNoRecord();
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
