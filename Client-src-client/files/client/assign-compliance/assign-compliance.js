var LEGAL_ENTITIES = null;
var DOMAINS = null;
var DIVISIONS = null;
var CATEGORIES = null;

var LEList = $("#legalentity");
var DivisionList = $("#division");
var CategoryList = $("#category");
var DomainList = $("#domain");
var UnitList = $("#unit");
var FrequencyList = $("#frequency");

var ULRow = $("#templates .ul-row li");

var WIZARD_ONE_FILTER = 'wizard_ome_filter';


function callAPI(api_type) {
    if (api_type == WIZARD_ONE_FILTER) { 
        displayLoader();
        client_mirror.getAssignComplianceFormData(function(error, data) {
            if (error == null) {
                DOMAINS = data.domains;
                DIVISIONS = data.div_infos;
                CATEGORIES = data.cat_info;
                loadLegalEntity();
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    } 
    /*else if (api_type == API_Wizard1) {
        displayLoader();
        mirror.getAssignStatutoryWizardOneData(function(error, data) {
            if (error == null) {
                GroupName.focus();
                GROUPS = data.grps;
                BUSINESS_GROUPS = data.bgrps;
                LEGAL_ENTITIES = data.lety;
                DIVISIONS = data.divs;
                CATEGORIES = data.cates;
                DOMAINS = data.dms;
                hideLoader();
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    } else if (api_type == API_Wizard2) {
        COMPLIANCES_LIST = [];
        displayLoader();
        mirror.getAssignStatutoryWizardTwoData(
            int(val_domain_id), ACTIVE_UNITS, (sno - 1),
            function(error, data) {
                if (error == null) {
                    if (ACTIVE_UNITS.length == 1) {
                        COMPLIANCES_LIST = data.statutories_for_assigning;
                        loadSingleUnitCompliances();
                    } else {
                        COMPLIANCES_LIST = data.statutories_for_multiple;
                        loadMultipleUnitCompliances();
                    }
                } else {
                    displayMessage(error);
                    hideLoader();
                }
            }
        );
    } else if (api_type == SAVE_API || api_type == SUBMIT_API) {

        //check request is save or submit
        var submission_status;
        if (api_type == SAVE_API) {
            submission_status = 1;
        } else {
            submission_status = 2;
        }

        //check all compliance is selected before submit
        var checkSubmit = false;
        if($('.comp:checked').length == (statutoriesCount - 1)){
            checkSubmit = true;
        }

        //check remark validation
        for(var i=1; i<=(actCount-1); i++){
            var aStatus = parseInt($('#act'+i).attr("for"));
            var remark = null;
            if(aStatus == 2 || aStatus==3){
                remark = $('#remark'+i).val().trim();
                if(remark==''){
                    displayMessage(message.remarks_required);
                    hideLoader();
                    return false;
                }
            }
        }

        var selected_compliances_list = [];
        $.each(SELECTED_COMPLIANCE, function(key, value) {
            selected_compliances_list.push(
                value
            );
        });

        if (submission_status == 1 && selected_compliances_list.length == 0) {
            displayMessage(message.nocompliance_selected_forassign);
            hideLoader();
            return false;
        }
        else if (submission_status == 2 && checkSubmit == false) {
            displayMessage(message.assigncompliance_submit_failure);
            hideLoader();
            return false;
        } else {
            mirror.saveAssignedStatutory(selected_compliances_list, submission_status, int(val_group_id), int(val_legal_entity_id),
                int(val_domain_id), DomainName.val(), ACTIVE_UNITS,
                function(error, data) {
                    if (error == null) {
                        if (submission_status == 1) {
                            displaySuccessMessage(message.save_success);
                        } else {
                            displaySuccessMessage(message.submit_success);
                        }

                        CLIENT_STATUTORY_ID = null;
                        showList();
                        hideLoader();
                    } else {
                        displayMessage(error);
                        hideLoader();
                    }
                }
            );
        }

    }*/

}
function pageControls(){

}
//clear list values
function clearValues(levelvalue) {
  if (levelvalue == 'legalentity') {
    /*assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];*/
    DivisionList.empty();
    CategoryList.empty();
    DomainList.empty();
    UnitList.empty();
    FrequencyList.empty();
  }
  else if (levelvalue == 'division') {	
    CategoryList.empty();
    /*DomainList.empty();
    UnitList.empty();
    FrequencyList.empty();*/
  }
  else if (levelvalue == 'domain') {
    UnitList.empty();
    FrequencyList.empty();
  }else if (levelvalue == 'unit') {
    FrequencyList.empty();
  }
}

function loadChild(levelvalue) {
  if (levelvalue == 'legalentity') {
    loadDivision();
    loadCategory();
    loadDomain();
  }
  else if (levelvalue == 'division') {	
    loadCategory();
  }
  else if (levelvalue == 'domain') {
    loadUnit();
  }else if (levelvalue == 'unit') {
    loadFrequency();
  }
}

function activateList(element, levelvalue) {
	$('#' + levelvalue + ' li').each(function (index, el) {
      $(el).removeClass('active');
      $(el).find('i').removeClass('fa fa-check pull-right');
    });
    
    $(element).addClass('active');
    $(element).find('i').addClass('fa fa-check pull-right');
    clearValues(levelvalue);
    loadChild(levelvalue);
}

/*function activateMultiList(element, levelvalue) {
	clearValues(levelvalue);

    var chkstatus = $(element).attr('class');
    var chkid = $(element).attr('id');
    if (chkstatus == 'active') {
        $(element).removeClass('active');
        $(element).find('i').removeClass('fa fa-check pull-right');
    } else {
        $(element).addClass('active');
        $(element).find('i').addClass('fa fa-check pull-right');
    }
}*/

function loadLegalEntity(){
	$.each(LEGAL_ENTITIES, function(key, value) {
        id = value.le_id;
        text = value.le_name;
        var clone = ULRow.clone();
        clone.html(text + '<i></i>');
        clone.attr('id', id);
        LEList.append(clone);
        clone.click(function() {
            activateList(this, 'legalentity');
        });
    });
}

function loadDivision(){
	$.each(DIVISIONS, function(key, value) {
        id = value.div_id;
        text = value.div_name;

        var le_id = LEList.find("li.active").attr("id");
        if(le_id == value.le_id){
        	var clone = ULRow.clone();
	        clone.html(text + '<i></i>');
	        clone.attr('id', id);
	        DivisionList.append(clone);
	        clone.click(function() {
	            activateList(this, 'division');
	        });
        }
    });
}

function loadCategory(){
	$.each(CATEGORIES, function(key, value) {
        id = value.category_id;
        text = value.category_name;

        var le_id = LEList.find("li.active").attr("id");
        var div_id = '';
        if(DivisionList.find("li.active").attr("id") != undefined){
        	div_id = DivisionList.find("li.active").attr("id");
        }
        if(le_id == value.legal_entity_id && (div_id == '' || div_id == value.division_id)){
        	var clone = ULRow.clone();
	        clone.html(text + '<i></i>');
	        clone.attr('id', id);
	        CategoryList.append(clone);
	        clone.click(function() {
	            activateList(this, 'category');
	        });
        }
    });
}

function loadDomain(){
	$.each(DOMAINS, function(key, value) {
        id = value.d_id;
        text = value.d_name;

        var le_id = LEList.find("li.active").attr("id");
        
        if(le_id == value.le_id){
        	var clone = ULRow.clone();
	        clone.html(text + '<i></i>');
	        clone.attr('id', id);
	        DomainList.append(clone);
	        clone.click(function() {
	            activateList(this, 'domain');
	        });
        }
    });
}

function initialize() {
	LEList.empty();
	LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();
	callAPI(WIZARD_ONE_FILTER);
	

    //pageControls();
    
}

$(function() {
    initialize();
});