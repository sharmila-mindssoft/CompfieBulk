var CURRENT_TAB = 1;
var LEGAL_ENTITIES = null;
var DOMAINS = null;
var DIVISIONS = null;
var CATEGORIES = null;
var UNITS = null;
var FREQUENCY = null;

var LEList = $("#legalentity");
var DivisionList = $("#division");
var CategoryList = $("#category");
var DomainList = $("#domain");
var UnitList = $("#unit");
var FrequencyList = $("#frequency");

var ULRow = $("#templates .ul-row li");

var NextButton = $('#btn-next');
var PreviousButton = $('#btn-previous');
var SubmitButton = $("#btn-submit");
var ShowMore = $(".btn-showmore");

var WIZARD_ONE_FILTER = 'wizard_one_filter';
var WIZARD_ONE_UNIT_FILTER = 'wizard_one_unit_filter';

var ACTIVE_UNITS = [];
var ACTIVE_FREQUENCY = [];

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
    else if (api_type == WIZARD_ONE_UNIT_FILTER) { 
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

function validateFirstTab() {
    if (ACTIVE_FREQUENCY.length <= 0) {
        displayMessage(message.atleast_one_unit_required)
        return false;
    } else {
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
        ACT_MAP = {};*/
        return true;
    }
};

function showTab() {
    hideall = function() {
        // $('.setup-panel li').addClass('disabled');
        $('.statutory_mapping_tab li').removeClass('active');
        $('.tab-pane').removeClass('active in');
        $('#tab1').hide();
        $('#tab2').hide();
        $('#tab3').hide();
        ShowMore.hide();
        SubmitButton.hide();
        NextButton.hide();
        PreviousButton.hide();
    }

    enabletabevent = function(tab) {
        if (tab == 1) {
            $('.tab-step-1 a').attr('href', '#tab1');
        } else if (tab == 2) {
            $('.tab-step-2 a').attr('href', '#tab2');
        } else if (tab == 3) {
            $('.tab-step-3 a').attr('href', '#tab3');
        }
    }
    disabletabevent = function() {
        $('.tab-step-1 a').removeAttr('href');
        $('.tab-step-2 a').removeAttr('href');
        $('.tab-step-3 a').removeAttr('href');
    }

    if (CURRENT_TAB == 1) {
        hideall();
        disabletabevent();
        enabletabevent(1);
        $('.tab-step-1').addClass('active')
        $('#tab1').addClass("active in");
        $('#tab1').show();
        NextButton.show();
    } else if (CURRENT_TAB == 2) {
        if (validateFirstTab() == false) {
            CURRENT_TAB -= 1;
            return false;
        } else {
            displayLoader();
            var le_id = LEList.find("li.active").attr("id");
        	var d_id = DomainList.find("li.active").attr("id");

            client_mirror.getAssignComplianceForUnits(
                parseInt(le_id), ACTIVE_UNITS, parseInt(d_id), 0, [1,2,3,4,5], 
                function(error, data) {
                    if (error == null) {
                    	alert('success')
                        /*totalRecord = data.total_records;
                        if (data.unit_total > 5000 && ACTIVE_UNITS.length > 1) {
                            displayMessage(message.maximum_compliance_selection_reached);
                            hideLoader();
                            CURRENT_TAB -= 1;
                            return false;
                        } else {
                            callAPI(API_Wizard2);
                            hideall();
                            enabletabevent(2);
                            $('.tab-step-2').addClass('active')
                            $('#tab2').addClass('active in');
                            $('#tab2').show();
                            SubmitButton.show();
                            PreviousButton.show();
                            SaveButton.show();
                            ShowMore.show();
                            showBreadCrumbText();
                        }*/
                    } else {
                        displayMessage(error);
                        hideLoader();
                        CURRENT_TAB -= 1;
                        return false;
                    }
                }
            );
        }
    }
};

function pageControls(){
	NextButton.click(function() {
        //$('.tbody-compliance-list').empty();
        CURRENT_TAB += 1;
        showTab();
    });
    PreviousButton.click(function() {
        $(".total_count_view").hide();
        CURRENT_TAB = CURRENT_TAB - 1;
        showTab();
    });
    ShowMore.click(function() {
        callAPI(API_Wizard2);
    });
    SubmitButton.click(function() {
        displayLoader();
        setTimeout(function() {
            callAPI(SUBMIT_API)
        }, 500);
    });

}
//clear list values
function clearValues(levelvalue) {
  if (levelvalue == 'legalentity') {
    ACTIVE_UNITS = [];
    ACTIVE_FREQUENCY = [];
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
  	ACTIVE_UNITS = [];
  	ACTIVE_FREQUENCY = [];
    UnitList.empty();
    FrequencyList.empty();
  }else if (levelvalue == 'unit') {
  	ACTIVE_FREQUENCY = [];
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
  	callAPI(WIZARD_ONE_UNIT_FILTER);
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

function activateMultiList(element, levelvalue) {
    var chkstatus = $(element).attr('class');
    var chkid = $(element).attr('id');
    if (chkstatus == 'active') {
        $(element).removeClass('active');
        $(element).find('i').removeClass('fa fa-check pull-right');
        if(levelvalue == 'unit'){
        	index = ACTIVE_UNITS.indexOf(parseInt(chkid));
        	ACTIVE_UNITS.splice(index, 1);
        }else{
        	index = ACTIVE_FREQUENCY.indexOf(parseInt(chkid));
        	ACTIVE_FREQUENCY.splice(index, 1);
        }
        
    } else {
        $(element).addClass('active');
        $(element).find('i').addClass('fa fa-check pull-right');

        if (ACTIVE_UNITS.length >= 20) {
            displayMessage(message.maximum_units);
            return false;
        }else{
            $(element).addClass('active');
            $(element).find('i').addClass('fa fa-check pull-right');
            if(levelvalue == 'unit'){
	        	ACTIVE_UNITS.push(parseInt(chkid));
	        }else{
	        	ACTIVE_FREQUENCY.push(parseInt(chkid));
	        }
        }
    }
    clearValues(levelvalue);
    loadChild(levelvalue);
}

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
        id = value.cat_id;
        text = value.cat_name;

        var le_id = LEList.find("li.active").attr("id");
        var div_id = '';
        if(DivisionList.find("li.active").attr("id") != undefined){
        	div_id = DivisionList.find("li.active").attr("id");
        }
        if(le_id == value.le_id && (div_id == '' || div_id == value.div_id)){
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

function loadUnit(){
	$.each(UNITS, function(key, value) {
        id = value.u_id;
        text = value.u_name;

    	var clone = ULRow.clone();
        clone.html(text + '<i></i>');
        clone.attr('id', id);
        UnitList.append(clone);
        clone.click(function() {
            activateMultiList(this, 'unit');
        });
    });
}

function loadFrequency(){
	$.each(FREQUENCY, function(key, value) {
        id = value.frequency_id;
        text = value.frequency;

    	var clone = ULRow.clone();
        clone.html(text + '<i></i>');
        clone.attr('id', id);
        FrequencyList.append(clone);
        clone.click(function() {
            activateMultiList(this, 'frequency');
        });
    });
}

function initialize() {
	LEList.empty();
	LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();
	callAPI(WIZARD_ONE_FILTER);
	

    pageControls();
    
}

$(function() {
    initialize();
});