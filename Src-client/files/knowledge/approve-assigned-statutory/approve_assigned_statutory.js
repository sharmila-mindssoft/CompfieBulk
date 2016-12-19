/* Elements */
var CancelButton = $('#btn-user-cancel');
var AssignStatutoryView = $("#assignstatutory-view");
var AssignStatutoryAdd = $("#assignstatutory-add");
var SubmitButton = $("#btn-submit");

var AssignStatutoryList = $(".tbody-assignstatutory");
var StatutoryProvision = ".statutoryprovision";
var ComplianceTask = ".compliancetask";
var ComplianceDescription = ".compliancedescription";

var AssignedStatutoryList = $(".tbody-approved-assigned-statutories-list");
var AssignedStatutoryRow = $("#templates .table-approved-assigned-statutories .table-row");

var TblSno = ".tbl_sno";
var TblCountry = ".tbl_country";
var TblGroup = ".tbl_group";
var TblBG = ".tbl_businessgroup";
var TblLE = ".tbl_legalentity";
var TblDiv = ".tbl_division";
var TblCat = ".tbl_category";
var TblUnit = ".tbl_unit";
var TblDomain = ".tbl_domain";
var TblStatus = ".tbl_status";
var TblView = ".view-icon";

/* Data */

var COMPLIANCES_LIST = null;
var ASSIGNED_STATUTORIES = null;

/* Values */

var DOMAIN_ID = null;
var UNIT_ID = null;
var REJ_COMP = [];
var CLIENT_STATUTORY_ID = null;

var LastAct='';
var LastSubAct='';
var statutoriesCount;
var actCount;


function loadCompliances() {
    var ccount = 1;
    var count = 1;
    statutoriesCount = 1;
    actCount = 1;
    AssignStatutoryList.empty();
    var sno = 0;
    $.each(COMPLIANCES_LIST, function(key, value) {
        if(LastAct != value.level_1_s_name){
            var acttableRow = $('#act-templates .p-head');
            var clone = acttableRow.clone();

            $('.acc-title', clone).attr('id', 'heading'+actCount);
            $('.panel-title a span', clone).text(value.level_1_s_name);
            $('.panel-title a', clone).attr('href', '#collapse'+actCount);
            $('.panel-title a', clone).attr('aria-controls', 'collapse'+actCount);

            $('.coll-title', clone).attr('id', 'collapse'+actCount);
            $('.coll-title', clone).attr('aria-labelledb', 'heading'+actCount);
            
           	if(value.a_status == 2){
                $('.act-status', clone).html('<img src="images/deletebold.png">');
                $('.remarks', clone).val(value.remarks);
                $('.remarks', clone).show();
            }else if(value.a_status == 3){
            	$('.act-status', clone).html('<img src="images/iconminusactive.png">');
                $('.remarks', clone).val(value.remarks);
                $('.remarks', clone).show();
            }else{
                $('.act-status', clone).html('<img src="images/tick1bold.png">');
            }
            $('.tbody-assignstatutory').append(clone);

	        ccount = actCount;
	        LastAct = value.level_1_s_name;
	        LastSubAct = value.level_1_s_name;
	        actCount = actCount + 1;
        }
        ++sno;

        if(LastSubAct != value.map_text){
            var subTitleRow = $('#statutory-value .table-statutory-values .sub-title-row');
            var clone3 = subTitleRow.clone();
            $('.sub-title', clone3).text(value.map_text);
            $(' #collapse'+ccount+' .tbody-compliance-list').append(clone3);
            LastSubAct = value.map_text;
        }
        
        var complianceDetailtableRow = $('#statutory-value .table-statutory-values .compliance-details');
        var clone2 = complianceDetailtableRow.clone();

        $('.sno', clone2).text(statutoriesCount);
        $('.statutoryprovision', clone2).text(value.s_provision);
        $('.compliancetask', clone2).text(value.comp_name);
        $('.org-name', clone2).attr('title', 'Organizations: ' + value.org_names);
        $('.compliancedescription', clone2).text(value.descrip);
        $('.rejected', clone2).on('click', function (event) {
      
        	if($(event.target).hasClass("text-muted") || 
        		$(event.target).find('i').hasClass("text-muted")){
        		$(this).html('<i class="fa fa-square text-warning c-pointer"></i>');
        		REJ_COMP.push(value.comp_id);
        	}else{
        		$(this).html('<i class="fa fa-square text-muted c-pointer"></i>');
        		index = REJ_COMP.indexOf(value.comp_id);
            	REJ_COMP.splice(index, 1);
        	}
        });

        if(value.comp_status == 1){
            $('.tick', clone2).html('<img src="images/tick1bold.png">');
        }else if(value.comp_status == 2){
            $('.untick', clone2).html('<img src="images/deletebold.png">');
        }else{
            $('.minus', clone2).html('<img src="images/iconminusactive.png">');
        }
       
        $(' #collapse'+ccount+' .tbody-compliance-list').append(clone2);
        statutoriesCount++;
        count++;
    });

}

function ifNullReturnHyphen(value){
    if(value){
        return value;
    }else{
        return "-";
    }
}
function EditAssignedStatutory(u_id, d_id){
    AssignStatutoryView.hide();
    AssignStatutoryAdd.show();
    mirror.getAssignedStatutoriesById(u_id, d_id, function(error, data) {
        if (error == null) {
            COMPLIANCES_LIST = data.statutories_for_assigning;
            loadCompliances();
        } else {
            custom_alert(error);
        }
    });
}

function loadAssignedStatutories(){
    var sno = 0;
    REJ_COMP = [];

    AssignedStatutoryList.empty();
    $.each(ASSIGNED_STATUTORIES, function(key, value){
        ++ sno;
        var clone = AssignedStatutoryRow.clone();
        $(TblSno, clone).text(sno);
        $(TblCountry, clone).text(value.c_name);
        $(TblGroup, clone).text(value.grp_name);
        $(TblBG, clone).text(value.b_grp_name);
        $(TblLE, clone).text(value.l_e_name);
        $(TblDiv, clone).text(ifNullReturnHyphen(value.div_name));
        $(TblCat, clone).text(ifNullReturnHyphen(value.cat_name));
        $(TblUnit, clone).text(value.u_name);
        $(TblDomain, clone).text(value.d_name);
        
        $('.view-icon', clone).on('click', function () {
            DOMAIN_ID = value.d_id;
            UNIT_ID = value.u_id;
            CLIENT_STATUTORY_ID = value.client_statutory_id;
            EditAssignedStatutory(value.u_id, value.d_id);
        });
        AssignedStatutoryList.append(clone);       
    });
}


SubmitButton.click(function(){
    var approval_status = $('#approval-status').val();
    var reason = $('#reason').val().trim();

     if (approval_status.length <= 0) {
        displayMessage(message.action_required);
        return false;
    } else if (reason.trim().length <= 0) {
        displayMessage(message.reason_required);
        return false;
    } else if (approval_status == 2 && REJ_COMP.length == 0) {
        displayMessage(message.no_compliance_to_reject);
        return false;
    } else {
    	mirror.approveAssignedStatutory(UNIT_ID, DOMAIN_ID, CLIENT_STATUTORY_ID, REJ_COMP,
	    parseInt(approval_status), reason,
	        function(error, data) {
	            if (error == null) {
	                displaySuccessMessage(message.action_success);
	                initialize();
	            } else {
	                custom_alert(error);
	            }
	        }
	    );
    }
});

CancelButton.click(function() {
    AssignStatutoryView.show();
    AssignStatutoryAdd.hide();
});

function initialize() {
    AssignStatutoryView.show();
    AssignStatutoryAdd.hide();
    mirror.getAssignedStatutoriesForApprove(function(error, data) {
        if (error == null) {
            ASSIGNED_STATUTORIES = data.assigned_statutories;
            loadAssignedStatutories();
        } else {
            custom_alert(error);
        }
    });
}

$(function() {
    initialize();
    $(document).find('.js-filtertable').each(function(){
        $(this).filtertable().addFilter('.js-filter');
    });
});