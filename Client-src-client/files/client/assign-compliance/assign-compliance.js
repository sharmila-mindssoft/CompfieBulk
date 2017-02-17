var CURRENT_TAB = 1;
var LEGAL_ENTITIES = null;
var DOMAINS = null;
var DIVISIONS = null;
var CATEGORIES = null;
var UNITS = null;
var FREQUENCY = null;
var USERS = null;
var ASSIGNEE_SU = {};
var APPROVER_SU = {};
var two_level_approve;

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
var SUBMIT_API = 'submit_api';

var ACTIVE_UNITS = [];
var ACTIVE_FREQUENCY = [];
 
var ComplianceList = null;
var ActList = null;
var LastAct = '';
var SCOUNT = 1;
var ACOUNT = 1;

function convert_month(data) {
  var months = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec'
  ];
  var rmonth;
  for (var j = 0; j < months.length; j++) {
    if (data == months[j]) {
      rmonth = months.indexOf(months[j]) + 1;
    }
  }
  return rmonth;
}
function convert_date(data) {
  var date = data.split('-');
  var months = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec'
  ];
  for (var j = 0; j < months.length; j++) {
    if (date[1] == months[j]) {
      date[1] = months.indexOf(months[j]) + 1;
    }
  }
  if (date[1] < 10) {
    date[1] = '0' + date[1];
  }
  return new Date(date[2], date[1] - 1, date[0]);
}
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
    else if (api_type == SUBMIT_API) { 
        displayLoader();
        var le_id = LEList.find("li.active").attr("id");
        var d_id = DomainList.find("li.active").attr("id");

		var assignComplianceAssigneeId = null;
		var assignComplianceConcurrenceId = null;
		var assignComplianceApprovalId = null;
		var assignComplianceAssigneeName = null;
		var assignComplianceConcurrenceName = null;
		var assignComplianceApprovalName = null;


		var d = new Date();
		var month = d.getMonth() + 1;
		var day = d.getDate();
		var output = d.getFullYear() + '/' + month + '/' + day;
		var currentDate = new Date(output);


		if ($('.assigneelist.active').attr('id') != undefined) {
		    assignComplianceAssigneeId = parseInt($('.assigneelist.active').attr('id'));
		    assignComplianceAssigneeName = $('.assigneelist.active').text().trim();
		}
		if ($('.concurrencelist.active').attr('id') != undefined) {
		    assignComplianceConcurrenceId = parseInt($('.concurrencelist.active').attr('id'));
		    assignComplianceConcurrenceName = $('.concurrencelist.active').text().trim();
		}
		if ($('.approvallist.active').attr('id') != undefined) {
		    assignComplianceApprovalId = parseInt($('.approvallist.active').attr('id'));
		    assignComplianceApprovalName = $('.approvallist.active').text().trim();
		}
		  

		assignCompliance = [];
		var totalCompliance = 1;
		var selectedStatus = false;
		var applicableUnitsArray = [];
		for (var i = 1; i <= ACOUNT - 1; i++) {
		    var actComplianceCount = $('.a-' + i).length;
		    for (var j = 1; j <= actComplianceCount; j++) {
		      	var complianceApplicable = false;
		      	if ($('#c-' + totalCompliance).is(':checked')) {
		        	complianceApplicable = true;
		        	selectedStatus = true;
		      	}

		     	if (complianceApplicable) {
			        var combineidVal = $('#combineid' + totalCompliance).val().split('#');
			        var compliance_id = parseInt(combineidVal[0]);
			        var compliance_name = combineidVal[1];
			        var due_date = parseInt(combineidVal[3]);
			        var frequency = combineidVal[2];
			        /*var repeats_type = combineidVal[4];
			        var repeats_every = combineidVal[5];*/
			        var appl_units = $('#appl_unit' + totalCompliance).val();
			        if (appl_units != '')
			          appl_units = appl_units.replace(/,\s*$/, '').split(',');
			        var applicable_units = [];
			        for (var u = 0; u < appl_units.length; u++) {
			          applicable_units.push(parseInt(appl_units[u]));
			        }
			        for (var k = 0; k < applicable_units.length; k++) {
			          if ($.inArray(applicable_units[k], applicableUnitsArray) == -1) {
			            applicableUnitsArray.push(parseInt(applicable_units[k]));
			          }
			        }
			        var statutory_dates = [];
			        var current_due_date = '';
			        var current_trigger_day = '';
			        var current_due_dates = [];
			        var validitydate = null;
			        var cvaliditydate = null;
			        var minvaliditydate = false;
			        var maxvaliditydate = false;
			        if ($('#validitydate' + totalCompliance).val() != undefined && $('#validitydate' + totalCompliance).val() != '') {
			          validitydate = $('#validitydate' + totalCompliance).val();
			          cvaliditydate = convert_date(validitydate);
			        }
			        if (frequency != 'On Occurrence') {
			          	var dDate = null;
			          	var tDay = null;
			          	if (due_date > 1) {
				            for (var k = 0; k < due_date; k++) {
				              	dDate = $('#duedate' + totalCompliance + '-' + k).val();
					            if (dDate != '') {
					                tDay = $('#triggerdate' + totalCompliance + '-' + k).val();
					                current_due_dates.push([
					                  dDate,
					                  tDay
					                ]);
					            } else {
					                displayMessage(message.compliance_duedate_required);
					                hideLoader();
					                return false;
					            }
				            }
				        } else {
				            dDate = $('#duedate' + totalCompliance).val();
				            if (dDate != '') {
				              tDay = $('#triggerdate' + totalCompliance).val();
				              current_due_dates.push([
				                dDate,
				                tDay
				              ]);
				            } else {
				              displayMessage(message.compliance_duedate_required);
				              hideLoader();
				              return false;
				            }
				        }

				        if (dDate != undefined && dDate != '') {
				            var convertDueDate = convert_date(dDate);
				            if (convertDueDate < currentDate) {
				              displayMessage(message.duedatelessthantoday_compliance + compliance_name);
				              hideLoader();
				              return false;
				            }
				        }
				        var sort_elements = current_due_dates;
				        if (current_due_dates.length > 1) {
				            sort_elements.sort(function (a, b) {
				              a1 = convert_date(a[0]);
				              b1 = convert_date(b[0]);
				              return a1 - b1;
				            });
				            current_due_date = sort_elements[0][0];
				            current_trigger_day = parseInt(sort_elements[0][1]);
				        } else {
				            current_due_date = current_due_dates[0][0];
				            current_trigger_day = parseInt(sort_elements[0][1]);
				        }
				        for (var dDates = 0; dDates < sort_elements.length; dDates++) {
				            var statutory_day = null;
				            var statutory_month = null;
				            var trigger_before_days = null;
				            if (sort_elements[dDates][0] != '' && sort_elements[dDates][0] != undefined) {
					            var splitDueDates = sort_elements[dDates][0].split('-');
					            var strMonth = splitDueDates[1];
					            statutory_day = parseInt(splitDueDates[0]);
					            statutory_month = convert_month(strMonth);
					            trigger_before_days = sort_elements[dDates][1];
					            if (trigger_before_days != '') {
					                var max_triggerbefore = 0;
					                /*if (repeats_type != null) {
					                  if (repeats_type == 1) {
					                    max_triggerbefore = repeats_every;
					                  } else if (repeats_type == 2) {
					                    max_triggerbefore = repeats_every * 30;
					                  } else {
					                    max_triggerbefore = repeats_every * 365;
					                  }
					                }*/
					                trigger_before_days = parseInt(trigger_before_days);
					                if (trigger_before_days > 100) {
					                  	displayMessage(message.triggerbefore_exceed);
					                  	hideLoader();
					                  	return false;
					                }
					                if (trigger_before_days == 0) {
					                  	displayMessage(message.triggerbefore_iszero);
					                  	hideLoader();
					                  	return false;
					                }
					               /* if (max_triggerbefore > 0 && trigger_before_days > max_triggerbefore) {
					                  displayMessage(message.triggerdays_exceeding_repeatsevery);
					                  hideLoader();
					                  return false;
					                }*/
					                if (validitydate != null) {
					                  	var convertDue = convert_date(sort_elements[dDates][0]);
					                  	if (cvaliditydate >= convertDue)
					                    	minvaliditydate = true;
					                  	if (daydiff(convertDue, cvaliditydate) <= 90)
					                    	maxvaliditydate = true;
					                  	if (minvaliditydate == false || maxvaliditydate == false) {
					                    	displayMessage(message.invalid_validitydate);
					                    	hideLoader();
					                    	return false;
					                  	}
					                }
					            } else {
					                displayMessage(message.compliance_triggerdate_required);
					                hideLoader();
					                return false;
					            }
				            }
				            statutoryDateList = client_mirror.statutoryDates(statutory_day, statutory_month, trigger_before_days, null);
				            statutory_dates.push(statutoryDateList);
				        }
			        } else {
			          	var statutory_dates = null;
			          	var current_due_date = null;
			          	var current_trigger_day = null;
			        }
			        assignComplianceData = client_mirror.assignCompliances(compliance_id, compliance_name, statutory_dates, current_due_date, validitydate, current_trigger_day, applicable_units);
			        assignCompliance.push(assignComplianceData);
			    }
			    totalCompliance++;
			}
		}
		
		if (selectedStatus) {
		    var unit_names = '';
		    for (var unit in UNITS) {
		      if ($.inArray(UNITS[unit].unit_id, ACTIVE_UNITS) >= 0) {
		        if (unit_names == '') {
		          unit_names += UNITS[unit].unit_name;
		        } else {
		          unit_names += ', ' + UNITS[unit].unit_name;
		        }
		      }
		    }

		    function onSuccess(data) {
		        displayMessage(message.save_success);
		    }
		    function onFailure(error, response) {
		        displayMessage(error);
		        err_message = message.error;
		        if (err_message == 'undefined')
		          displayMessage(error);
		        else if (error == 'InvalidDueDate') {
		          task = response.compliance_task;
		          displayMessage(message.invalid_duedate + task);
		        } else
		        displayMessage(err_message);
		        hideLoader();
		    }
		    client_mirror.saveAssignedComplianceFormData(assignComplianceAssigneeId, assignComplianceAssigneeName, assignComplianceConcurrenceId, assignComplianceConcurrenceName, 
		    	assignComplianceApprovalId, assignComplianceApprovalName, assignCompliance, parseInt(le_id), parseInt(d_id),  function (error, response) {
		        if (error == null) {
		          onSuccess(response);
		        } else {
		          onFailure(error, response);
		        }
		    });
			    
		} else {
			hideLoader();
			displayMessage(message.nocompliance_selected_forassign);
		}
    }
}

function validateFirstTab() {
    if (ACTIVE_FREQUENCY.length <= 0) {
        displayMessage(message.atleast_one_unit_required)
        return false;
    } else {
        /*$(".total_count_view").hide();
        LastAct = '';
        LastSubAct = '';
        SCOUNT = 1;
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

function validateSecondTab() {
    /*if (ACTIVE_FREQUENCY.length <= 0) {
        displayMessage(message.atleast_one_unit_required)
        return false;
    } else {
        $(".total_count_view").hide();
        LastAct = '';
        LastSubAct = '';
        SCOUNT = 1;
        actCount = 1;
        count = 1;
        sno = 1;
        totalRecord = 0;
        AssignStatutoryList.empty();
        SingleAssignStatutoryList.empty();
        SELECTED_COMPLIANCE = {};
        ACT_MAP = {};
        return true;
    }*/
    return true;
};

function loadCompliances(){
if (SCOUNT <= 1) {
    $('.tbody-accordion-list').empty();
}

for (var l = 0; l < ActList.length; l++) {

    if(LastAct != ActList[l]){         
        var countrytableRow = $('#act-templates .p-head');
        var clone = countrytableRow.clone();
        $('.acc-title', clone).attr('id', 'heading'+ACOUNT);
        $('.panel-title a span', clone).text(ActList[l]);
        $('.panel-title a', clone).attr('href', '#collapse'+ACOUNT);
        $('.panel-title a', clone).attr('aria-controls', 'collapse'+ACOUNT);
        $('.coll-title', clone).attr('id', 'collapse'+ACOUNT);
        $('.coll-title', clone).attr('aria-labelledb', 'heading'+ACOUNT);
        $('.tbody-accordion-list').append(clone);
        LastAct = ActList[l];
        ACOUNT++;

        var C_LIST = ComplianceList[ActList[l]];
        $.each(C_LIST, function(key, value) {
		    var compliance_id = value.comp_id;
		    var compliance_name = value.comp_name
		    var compliance_description = value.descp;
		    var applicable_units = value.applicable_units;
		    var frequency = value.freq;
		    var statutory_date = value.statu_dates;
		    var due_date = value.due_date_list;
		    var summary = value.summary;
		    var triggerdate = '';
		    var statutorydate = '';
		    var elementTriggerdate = '';
		    var elementDuedate = '';
		    var due_date_length = 0;
		    var disp_appl_unit = applicable_units.length + '/' + ACTIVE_UNITS.length;

		    //var repeats_type = value.repeats_by;
		    //var repeats_every = value.repeats_every;

		    if (due_date != '' || due_date != null) {
		        if (due_date.length > 1) {
		          for (var k = 0; k < due_date.length; k++) {
		            elementDuedate += '<input type="text" id="duedate' + SCOUNT + '-' + k + '" readonly="readonly" class="input-box" value="' + due_date[k] + '"/>';
		          }
		        } else {
		          elementDuedate += '<input type="text" id="duedate' + SCOUNT + '" readonly="readonly" class="input-box" value="' + due_date[0] + '" style="width:50px;"/>';
		        }
		        due_date_length = due_date.length;
		    }
		    for (j = 0; j < statutory_date.length; j++) {
		        var sDay = '';
		        if (statutory_date[j].statutory_date != null)
		          sDay = statutory_date[j].statutory_date;
		        var sMonth = '';
		        if (statutory_date[j].statutory_month != null)
		          sMonth = statutory_date[j].statutory_month;
		        var tDays = '';
		        if (statutory_date[j].trigger_before_days != null)
		          tDays = statutory_date[j].trigger_before_days;
		        if (sMonth != '')
		          sMonth = getMonth_IntegertoString(sMonth);
		        if (tDays != '') {
		          triggerdate += tDays + ' Day(s) ';
		        }
		        statutorydate += sMonth + ' ' + sDay + ' ';
		        if (statutory_date.length > 1) {
		          elementTriggerdate += '<input type="text" id="triggerdate' + SCOUNT + '-' + j + '" placeholder="Days" class="input-box trigger" value="' + tDays + '" maxlength="3" style="width:50px; float:left;" />';
		        } else {
		          elementTriggerdate += '<input type="text" id="triggerdate' + SCOUNT + '" placeholder="Days" class="input-box trigger" value="' + tDays + '" maxlength="3" style="width:50px; float:left;" />';
		        }
		    }


		    var combineId = compliance_id + '#' + compliance_name + '#' + frequency + '#' + due_date_length;
		    var COMPRow = $('#compliances .table-compliances .row-compliances');
		    var clone2 = COMPRow.clone();
		    $('.comp-checkbox', clone2).attr('id', 'c-' + SCOUNT);
        	$('.comp-checkbox', clone2).val(compliance_id);
        	$('.comp-checkbox', clone2).addClass('a-' + (ACOUNT-1));

        	$('.combineid-class', clone2).attr('id', 'combineid' + SCOUNT);
      		$('.combineid-class', clone2).val(combineId);

		    $('.compliancetask', clone2).text(compliance_name);
		    $('.desc', clone2).attr('title', compliance_description);
		    $('.applicableunits', clone2).text(disp_appl_unit);
		    $('.frequency', clone2).text(frequency);

		    var dispUnit = '';
		    for (var i = 0; i < applicable_units.length; i++) {
		        dispUnit = dispUnit + applicable_units[i] + ',';
		    }
		    $('.appl_unit', clone2).attr('id', 'appl_unit' + SCOUNT);
		    $('.appl_unit', clone2).val(dispUnit);

		    if (summary != null) {
		        if (statutorydate.trim() != '') {
		          statutorydate = summary + ' ( ' + statutorydate + ' )';
		        } else {
		          statutorydate = summary;
		        }
		    }

		    //$('.summary', clone2).text(statutorydate);
		    $('.summary', clone2).text(summary);

		    if (frequency != 'On Occurrence') {
		        if (triggerdate == '') {
		          $('.trigger', clone2).html(' <input type="text" value="" class="input-box trigger" placeholder="Days" id="triggerdate' + SCOUNT + '" maxlength="3"/>');
		          $('.duedate', clone2).html('<input type="text" value="" class="input-box" readonly="readonly" id="duedate' + SCOUNT + '"/>');
		        } else {
		          $('.trigger', clone2).html('<span style="float:right;padding-right:30px;" class="edittrigger' + SCOUNT + '" value="' + SCOUNT + '"><img src="/images/icon-edit.png" width="12"></span> <span style="float:right;display: none;padding-right:30px;" class="closetrigger' + SCOUNT + '" value="' + SCOUNT + '"><img src="/images/delete.png" width="12"></span>' + triggerdate + '<div class="edittriggertextbox' + SCOUNT + '" style="display:none;padding-top:10px;">' + elementTriggerdate + '</div>');
		          $('.duedate', clone2).html('<div>' + elementDuedate + '</div>');
		        }
		    }
		    if (frequency == 'Periodical' || frequency == 'Review' || frequency == 'Flexi Review') {
		        $('.vdate', clone2).attr('id', 'validitydate' + SCOUNT);
		      } else {
		        $('.validitydate', clone2).html('');
		    }


		    $('#collapse' + (ACOUNT-1) + ' .tbody-compliance-list').append(clone2);

		        var duename = SCOUNT;
			    if (due_date.length > 1) {
			        for (var k = 0; k < due_date.length; k++) {
			          duename = SCOUNT + '-' + k;
			          $('#duedate' + duename).datepicker({
			            changeMonth: true,
			            changeYear: true,
			            numberOfMonths: 1,
			            dateFormat: 'dd-M-yy',
			            monthNames: [
			              'Jan',
			              'Feb',
			              'Mar',
			              'Apr',
			              'May',
			              'Jun',
			              'Jul',
			              'Aug',
			              'Sep',
			              'Oct',
			              'Nov',
			              'Dec'
			            ]
			          });
			        }
			    } else {
			        $('#duedate' + duename).datepicker({
			          changeMonth: true,
			          changeYear: true,
			          numberOfMonths: 1,
			          dateFormat: 'dd-M-yy',
			          monthNames: [
			            'Jan',
			            'Feb',
			            'Mar',
			            'Apr',
			            'May',
			            'Jun',
			            'Jul',
			            'Aug',
			            'Sep',
			            'Oct',
			            'Nov',
			            'Dec'
			          ]
			        });
			    }
			    $('#validitydate' + SCOUNT).datepicker({
			        changeMonth: true,
			        changeYear: true,
			        numberOfMonths: 1,
			        dateFormat: 'dd-M-yy',
			        monthNames: [
			          'Jan',
			          'Feb',
			          'Mar',
			          'Apr',
			          'May',
			          'Jun',
			          'Jul',
			          'Aug',
			          'Sep',
			          'Oct',
			          'Nov',
			          'Dec'
			        ]
			    });

		    $('.edittrigger' + SCOUNT).click(function () {
		        var text = $(this).attr('class');
		        var clickvalue = text.substring(text.lastIndexOf('r') + 1);
		        $('.edittriggertextbox' + clickvalue).show();
		        $('.closetrigger' + clickvalue).show();
		        $('.edittrigger' + clickvalue).hide();
		    });
		    $('.closetrigger' + SCOUNT).click(function () {
		        var text = $(this).attr('class');
		        var clickvalue = text.substring(text.lastIndexOf('r') + 1);
		        $('.edittriggertextbox' + clickvalue).hide();
		        $('.edittrigger' + clickvalue).show();
		        $('.closetrigger' + clickvalue).hide();
		    });
		    $('.trigger').on('input', function (e) {
		        this.value = isNumbers($(this));
		    });

		    SCOUNT++;
		});

    }


}


}

//load available user in third wizard
function loadUser(userType) {
  var selectedUnit = null;
  var userClass;
  var temp_assignee = null;
  var temp_concurrence = null;
  var temp_approval = null;
  var sId = 0;
  //var temp_id = null;
  if (userType == 'assignee') {
    selectedUnit = $('#assignee_unit').val();
    userClass = 'assigneelist';  /*if($('.assigneelist.active').attr('id') != undefined)
      temp_id = parseInt($('.assigneelist.active').attr('id'));*/
  } else if (userType == 'concurrence') {
    selectedUnit = $('#concurrence_unit').val();
    userClass = 'concurrencelist';  /*if($('.concurrencelist.active').attr('id') != undefined)
      temp_id = parseInt($('.concurrencelist.active').attr('id'));*/
  } else {
    selectedUnit = $('#approval_unit').val();
    userClass = 'approvallist';  /*if($('.approvallist.active').attr('id') != undefined)
      temp_id = parseInt($('.approvallist.active').attr('id'));*/
  }
  $('#' + userType).empty();
  var assigneeUserId = null;

  if ($('.assigneelist.active').attr('id') != undefined) {
    var cIds = $('.assigneelist.active').attr('id').split('-');
    assigneeUserId = parseInt(cIds[0]);
    if (parseInt(cIds[1]) != 0)
      sId = cIds[1];
  }
  var concurrenceUserId = null;
  if ($('.concurrencelist.active').attr('id') != undefined) {
    var cIds = $('.concurrencelist.active').attr('id').split('-');
    concurrenceUserId = parseInt(cIds[0]);
    if (parseInt(cIds[1]) != 0)
      sId = cIds[1];
  }
  var approvalUserId = null;
  if ($('.approvallist.active').attr('id') != undefined) {
    var cIds = $('.approvallist.active').attr('id').split('-');
    approvalUserId = parseInt(cIds[0]);
    if (parseInt(cIds[1]) != 0)
      sId = cIds[1];
  }
  var conditionResult = true;
  var conditionResult1 = true;
  /*var userLevel = null;
  var userLevel1 = null;
  if (userType == 'assignee' && (concurrenceUserId != null || approvalUserId != null)) {
    if (concurrenceUserId != null) {
      userLevel = getUserLevel(concurrenceUserId);
    } else {
      userLevel = getUserLevel(approvalUserId);
    }
  } else if (userType == 'concurrence' && (assigneeUserId != null || approvalUserId != null)) {
    if (assigneeUserId != null) {
      userLevel = getUserLevel(assigneeUserId);
    }
    if (approvalUserId != null) {
      userLevel1 = getUserLevel(approvalUserId);
    }
  } else if (userType == 'approval' && (concurrenceUserId != null || assigneeUserId != null)) {
    if (concurrenceUserId != null) {
      userLevel = getUserLevel(concurrenceUserId);
    } else {
      userLevel = getUserLevel(assigneeUserId);
    }
  }*/
  var str = '';
  var str1 = '';
  /*if (userType = 'approval' && selectedUnit != '') {
    str1 = '<li id="' + client_admin + '-0' + '" class="' + userClass + '" > Client Admin </li>'; 
  }*/

  for (var user in USERS) {
    var serviceProviderId = 0;
    if (USERS[user].sp_id != null) {
      serviceProviderId = USERS[user].sp_id;
    }
    if (selectedUnit == 'all' || parseInt(selectedUnit) == USERS[user].s_u_id || (serviceProviderId > 0 && selectedUnit != '')) {
      var userId = USERS[user].usr_id;
      var userName = USERS[user].emp_name;
      /*if (userId == client_admin) {
        userName = userName + ' (Client Admin)';
        str1 = '';
      }*/
      var combine = userId + '-' + serviceProviderId;
      var isAssignee = USERS[user].is_assignee;
      var isConcurrence = USERS[user].is_approver;
      var isApprover = USERS[user].is_approver;
      var userPermission;
      if (userType == 'assignee') {
        userPermission = isAssignee;
      } else if (userType == 'concurrence') {
        userPermission = isConcurrence;
      } else if (userType == 'approval') {
        userPermission = isApprover;
      }

      var concurrenceStatus = true;
      if(userType == 'concurrence' && USERS[user].usr_cat_id == 1){
      	concurrenceStatus = false;
      }
      if (userPermission && (assigneeUserId == null || assigneeUserId != userId) && (approvalUserId == null || approvalUserId != userId) && (concurrenceUserId == null || concurrenceUserId != userId) && (serviceProviderId == 0 || sId == serviceProviderId || sId == 0) && concurrenceStatus) {
        str += '<li id="' + combine + '" class="' + userClass + '" >' + userName + ' <i></i> </li>';
      }
    }
  }
  $('#' + userType).append(str1 + str);
}

$('#assignee_unit').change(function () {
  loadUser('assignee');
});

$('#concurrence_unit').change(function () {
  var assigneeSelectedId = '';
  if ($('.assigneelist.active').attr('id') != undefined) {
    assigneeSelectedId = $('.assigneelist.active').attr('id').split('-')[0];
  }
  loadUser('concurrence');
  
});
$('#approval_unit').change(function () {
  var assigneeSelectedId = '';
  if ($('.assigneelist.active').attr('id') != undefined) {
    assigneeSelectedId = $('.assigneelist.active').attr('id').split('-')[0];
  }
  loadUser('approval');
});


$('#assignee').click(function (event) {
  var chkstatus = $(event.target).attr('class');
  if (chkstatus != undefined) {
    if (chkstatus == 'assigneelist active') {
      $(event.target).removeClass('active');
      $(event.target).find('i').removeClass('fa fa-check pull-right');
    } else {
      $('.assigneelist').each(function (index, el) {
        $(el).removeClass('active');
        $(el).find('i').removeClass('fa fa-check pull-right');
      });
      $(event.target).addClass('active');
      $(event.target).find('i').addClass('fa fa-check pull-right');
    }
  }
});
$('#concurrence').click(function (event) {
  var chkstatus = $(event.target).attr('class');
  if (chkstatus != undefined) {
    if (chkstatus == 'concurrencelist active') {
      $(event.target).removeClass('active');
      $(event.target).find('i').removeClass('fa fa-check pull-right');
    } else {
      $('.concurrencelist').each(function (index, el) {
        $(el).removeClass('active');
        $(el).find('i').removeClass('fa fa-check pull-right');
      });
      $(event.target).addClass('active');
      $(event.target).find('i').addClass('fa fa-check pull-right');
    }
 
    loadUser('approval');
  }
});
$('#approval').click(function (event) {
  var chkstatus = $(event.target).attr('class');
  if (chkstatus != undefined) {
    if (chkstatus == 'approvallist active') {
      $(event.target).removeClass('active');
      $(event.target).find('i').removeClass('fa fa-check pull-right');
    } else {
      $('.approvallist').each(function (index, el) {
        $(el).removeClass('active');
        $(el).find('i').removeClass('fa fa-check pull-right');
      });
      $(event.target).addClass('active');
      $(event.target).find('i').addClass('fa fa-check pull-right');
    }  
  }
});

function loadSeatingUnits(){
  $('#assignee_unit').empty();
  $('#assignee_unit').append('<option value=""> Select </option>');
  $('#assignee_unit').append('<option value="all"> All </option>');
  $.each(ASSIGNEE_SU, function (key, value) {
    var option = $('<option></option>');
    option.val(key);
    option.text(value);
    $('#assignee_unit').append(option);
  });
  $('#concurrence_unit').empty();
  $('#concurrence_unit').append('<option value=""> Select </option>');
  $('#concurrence_unit').append('<option value="all"> All </option>');
  $.each(APPROVER_SU, function (key, value) {
    var option = $('<option></option>');
    option.val(key);
    option.text(value);
    $('#concurrence_unit').append(option);
  });
  $('#approval_unit').empty();
  $('#approval_unit').append('<option value=""> Select </option>');
  $('#approval_unit').append('<option value="all"> All </option>');
  $.each(APPROVER_SU, function (key, value) {
    var option = $('<option></option>');
    option.val(key);
    option.text(value);
    $('#approval_unit').append(option);
  });

  /*if (two_level_approve) {
    $('.c-view').show();
  } else {
    $('.c-view').hide();
  }*/
}

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
                parseInt(le_id), ACTIVE_UNITS, parseInt(d_id), 0, ACTIVE_FREQUENCY, 
                function(error, data) {
                    if (error == null) {
                    	ComplianceList = data.assign_statutory;
                    	ActList = data.level_one_name;
                    	loadCompliances();
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
    } else if (CURRENT_TAB == 3) {
        if (validateSecondTab() == false) {
            CURRENT_TAB -= 1;
            return false;
        } else {
            displayLoader();
            var le_id = LEList.find("li.active").attr("id");
        	var d_id = DomainList.find("li.active").attr("id");

            client_mirror.getUserToAssignCompliance(
                parseInt(d_id), ACTIVE_UNITS,  parseInt(le_id), 
                function(error, data) {
                    if (error == null) {
                    	two_level_approve = data.t_l_approve;
                    	USERS = data.assign_users;
                    	$.each(USERS, function(key, value) {
					        id = value.s_u_id;
					        text = value.s_u_name;
					        assignee_flag = value.is_assignee;
					        approver_flag = value.is_approver;
					        if (id != null && assignee_flag) ASSIGNEE_SU[id] = text;

					        if (id != null && approver_flag) APPROVER_SU[id] = text;
					    });
					    loadSeatingUnits();

             			//ComplianceList = data.assign_statutory;
                    	//ActList = data.level_one_name;
                    	//loadCompliances();
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