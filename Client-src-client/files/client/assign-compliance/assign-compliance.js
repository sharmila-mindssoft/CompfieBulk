var CURRENT_TAB = 1;
var LEGAL_ENTITIES = null;
var DOMAINS = null;
var DIVISIONS = null;
var CATEGORIES = null;
var UNITS = null;
var FREQUENCY = null;
var USERS = null;
var VALIDITY_DAYS = 0;
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
var GET_COMPLIANCE = 'get_compliance';
var SUBMIT_API = 'submit_api';

var ACTIVE_UNITS = [];
var ACTIVE_FREQUENCY = [];

var ComplianceList = null;
var ActList = null;
var LastAct = '';
var SCOUNT = 1;
var ACOUNT = 1;
var totalRecord = 0;
var mUnit = 20;
var mCompliances = 500;

var isPrevious = false;

var Filter_List = $('.filter-list');
var assignCompliance = [];
var currentDate = null;

function convert_month(data) {
    var months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ];
    var rmonth;
    for (var j = 0; j < months.length; j++) {
        if (data == months[j]) {
            rmonth = months.indexOf(months[j]) + 1;
        }
    }
    return rmonth;
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
                hideLoader();
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    } else if (api_type == WIZARD_ONE_UNIT_FILTER) {
        displayLoader();
        var le_id = LEList.find("li.active").attr("id");
        var d_id = DomainList.find("li.active").attr("id");
        var c_id = getCountryId(le_id);

        client_mirror.getAssignComplianceUnits(parseInt(le_id), parseInt(d_id), c_id, function(error, data) {
            if (error == null) {
                UNITS = data.assign_units;
                FREQUENCY = data.unit_comp_frequency;
                VALIDITY_DAYS = data.validity_days;
                two_level_approve = data.t_l_approve;
                loadUnit();
                hideLoader();
            } else {
                displayMessage(error);
                hideLoader();
            }
        });
    } else if (api_type == GET_COMPLIANCE) {
        displayLoader();
        var le_id = LEList.find("li.active").attr("id");
        var d_id = DomainList.find("li.active").attr("id");
        client_mirror.getAssignComplianceForUnits(
            parseInt(le_id), ACTIVE_UNITS, parseInt(d_id), (SCOUNT - 1), ACTIVE_FREQUENCY,
            function(error, data) {
                if (error == null) {
                    ComplianceList = data.assign_statutory;
                    ActList = data.level_one_name;
                    loadCompliances();
                } else {
                    displayMessage(error);
                    hideLoader();
                }
            });
    } else if (api_type == SUBMIT_API) {
        displayLoader();
        var le_id = LEList.find("li.active").attr("id");
        var d_id = DomainList.find("li.active").attr("id");

        var ass_Id = null;
        var con_Id = null;
        var app_Id = null;
        var ass_Name = null;
        var con_Name = null;
        var app_Name = null;

        if ($('.assigneelist.active').attr('id') != undefined) {
            ass_Id = parseInt($('.assigneelist.active').attr('id'));
            ass_Name = $('.assigneelist.active').text().trim();
        }
        if ($('.concurrencelist.active').attr('id') != undefined) {
            con_Id = parseInt($('.concurrencelist.active').attr('id'));
            con_Name = $('.concurrencelist.active').text().trim();
        }
        if ($('.approvallist.active').attr('id') != undefined) {
            app_Id = parseInt($('.approvallist.active').attr('id'));
            app_Name = $('.approvallist.active').text().trim();
        }

        /*var unit_names = '';
        for (var unit in UNITS) {
          if ($.inArray(UNITS[unit].unit_id, ACTIVE_UNITS) >= 0) {
            if (unit_names == '') {
              unit_names += UNITS[unit].unit_name;
            } else {
              unit_names += ', ' + UNITS[unit].unit_name;
            }
          }
        }*/

        function onSuccess(data) {
            displaySuccessMessage(message.compliance_assign_success);
            CURRENT_TAB = 1;
            initialize();
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
        client_mirror.saveAssignedComplianceFormData(ass_Id, ass_Name, con_Id, con_Name,
            app_Id, app_Name, assignCompliance, parseInt(le_id), parseInt(d_id), ACTIVE_UNITS,
            function(error, response) {
                if (error == null) {
                    onSuccess(response);
                } else {
                    onFailure(error, response);
                }
            });
    }
}

function validateFirstTab() {
    var le_id = LEList.find("li.active").attr("id");
    var d_id = DomainList.find("li.active").attr("id");

    if (le_id == undefined) {
        displayMessage(message.legalentity_required)
        return false;
    } else if (d_id == undefined) {
        displayMessage(message.domain_required)
        return false;
    } else if (ACTIVE_UNITS.length == 0) {
        displayMessage(message.unit_required)
        return false;
    } else if (ACTIVE_FREQUENCY.length == 0) {
        displayMessage(message.compliancefrequency_required)
        return false;
    } else {
        LastAct = '';
        SCOUNT = 1;
        ACOUNT = 1;
        return true;
    }
};

function validateSecondTab() {
    if ($('.comp-checkbox:checked').length <= 0) {
        displayMessage(message.nocompliance_selected_forassign)
        return false;
    } else {
        displayLoader();
        assignCompliance = [];
        var totalCompliance = 1;
        var applicableUnitsArray = [];
        for (var i = 1; i <= ACOUNT - 1; i++) {
            var actComplianceCount = $('.a-' + i).length;
            for (var j = 1; j <= actComplianceCount; j++) {
                var complianceApplicable = false;
                if ($('#c-' + totalCompliance).is(':checked')) {
                    complianceApplicable = true;
                }

                if (complianceApplicable) {
                    var combineidVal = $('#combineid' + totalCompliance).val().split('#');
                    var compliance_id = parseInt(combineidVal[0]);
                    var compliance_name = combineidVal[1];
                    var due_date = parseInt(combineidVal[3]);
                    var frequency = combineidVal[2];
                    var repeats_type = combineidVal[4];
                    var repeats_every = combineidVal[5];

                    if (repeats_type != null) {
                        repeats_type = parseInt(repeats_type);
                    }
                    if (repeats_every != null) {
                        repeats_every = parseInt(repeats_every);
                    }

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
                            var convertCDate = convert_date(currentDate);
                            if (convertDueDate < convertCDate) {
                                displayMessage(message.duedatelessthantoday_compliance + compliance_name);
                                hideLoader();
                                return false;
                            }
                        }
                        var sort_elements = current_due_dates;
                        if (current_due_dates.length > 1) {
                            sort_elements.sort(function(a, b) {
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
                                    if (repeats_type != null) {
                                        if (repeats_type == 1) {
                                            max_triggerbefore = repeats_every;
                                        } else if (repeats_type == 2) {
                                            max_triggerbefore = repeats_every * 30;
                                        } else {
                                            max_triggerbefore = repeats_every * 365;
                                        }
                                    }
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
                                    if (max_triggerbefore > 0 && trigger_before_days > max_triggerbefore) {
                                        displayMessage(message.triggerdays_exceeding_repeatsevery);
                                        hideLoader();
                                        return false;
                                    }
                                    if (validitydate != null && VALIDITY_DAYS != 0) {
                                        var convertDue = convert_date(sort_elements[dDates][0]);
                                        /*if (cvaliditydate >= convertDue)
					                    	minvaliditydate = true;*/
                                        if (Math.abs(daydiff(convertDue, cvaliditydate)) <= VALIDITY_DAYS)
                                            maxvaliditydate = true;
                                        /*if (minvaliditydate == false) {
					                    	displayMessage(message.validity_gt_duedate);
					                    	hideLoader();
					                    	return false;
					                  	}*/
                                        if (maxvaliditydate == false) {
                                            displayMessage(message.validity_date_before_after.replace('V_DAYS', VALIDITY_DAYS).replace('COMPLIANCE', compliance_name));
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
                    assignComplianceData = client_mirror.assignCompliances(compliance_id, compliance_name, statutory_dates, current_due_date, validitydate, current_trigger_day, applicable_units, repeats_type, repeats_every, frequency);
                    assignCompliance.push(assignComplianceData);
                }
                totalCompliance++;
            }
        }

        if (assignCompliance.length > 0) {
            hideLoader();
            return true;
        } else {
            hideLoader();
            displayMessage(message.nocompliance_selected_forassign);
            return false;
        }
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
    }
};

function actstatus(element) {
    var id = $(element).attr("id");
    var cstatus = $(element).prop("checked");
    $('.a-' + id).each(function() {
        if (cstatus) {
            if ($('.comp-checkbox:checked').length > mCompliances) {
                $(this).prop("checked", false);
                displayMessage(message.maximum_compliance_selection_reached_select_all);
                return false;
            } else {
                $(this).prop("checked", true);
            }
        } else {
            $(this).prop("checked", cstatus);
        }
    });
    $('.selected_count').text('Selected Compliance: ' + $('.comp-checkbox:checked').length);
}

function get_selected_count(element) {
    if ($('.comp-checkbox:checked').length > mCompliances) {
        $(element).prop("checked", false);
        displayMessage(message.maximum_compliance_selection_reached_select_all);
    }
    $('.selected_count').text('Selected Compliance: ' + $('.comp-checkbox:checked').length);
}

function displayPopup(units_string) {
    $('.popup-list').find('tr').remove();
    var units = units_string.split(',');
    for (var i = 0; i < units.length - 1; i++) {
        var dispUnit = '';
        $.each(UNITS, function(index, value) {
            if (value.u_id == parseInt(units[i])) {
                dispUnit = value.u_name + ', ' + value.address;
            }
        });
        var tableRow = $('#templates .table-popup-list .table-row');
        var clone = tableRow.clone();
        $('.popup_unitname', clone).text(dispUnit);
        $('.popup-list').append(clone);
    }

    Custombox.open({
        target: '#custom-modal',
        effect: 'contentscale',
    });
}

function loadCompliances() {
    if (SCOUNT <= 1) {
        $('.tbody-accordion-list').empty();
    }
    for (var l = 0; l < ActList.length; l++) {
        if (LastAct != ActList[l]) {
            var countrytableRow = $('#act-templates .p-head');
            var clone = countrytableRow.clone();

            $('.act-checkbox', clone).attr('id', ACOUNT);
            $('.act-checkbox', clone).on('click', function() {
                actstatus(this);
            });

            $('.acc-title', clone).attr('id', 'heading' + ACOUNT);
            $('.panel-title a span', clone).text(ActList[l]);
            $('.panel-title a', clone).attr('href', '#collapse' + ACOUNT);
            $('.panel-title a', clone).attr('aria-controls', 'collapse' + ACOUNT);
            $('.coll-title', clone).attr('id', 'collapse' + ACOUNT);
            $('.coll-title', clone).attr('aria-labelledb', 'heading' + ACOUNT);
            $('.tbody-accordion-list').append(clone);

            $('#' + ACOUNT).click(function() {
                actStatus(this);
            });

            LastAct = ActList[l];
            ACOUNT++;
        }
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
            var repeats_type = value.repeat_by;
            var repeats_every = value.r_every;

            if (due_date != '' || due_date != null) {
                if (due_date.length > 1) {
                    for (var k = 0; k < due_date.length; k++) {
                        elementDuedate += '<input type="text" id="duedate' + SCOUNT + '-' + k + '" readonly="readonly" class="form-control input-sm" value="' + due_date[k] + '"/>';
                    }
                } else {
                    elementDuedate += '<input type="text" id="duedate' + SCOUNT + '" readonly="readonly" class="form-control input-sm" value="' + due_date[0] + '"/>';
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
                    triggerdate += tDays + ' Day(s), ';
                }
                statutorydate += sMonth + ' ' + sDay + ', ';
                if (statutory_date.length > 1) {
                    elementTriggerdate += '<input type="text" id="triggerdate' + SCOUNT + '-' + j + '" placeholder="Days" class="form-control input-sm trigger" value="' + tDays + '" maxlength="3" style="width:50px; float:left;" />';
                } else {
                    elementTriggerdate += '<input type="text" id="triggerdate' + SCOUNT + '" placeholder="Days" class="form-control input-sm trigger" value="' + tDays + '" maxlength="3" style="width:50px; float:left;" />';
                }
            }

            var combineId = compliance_id + '#' + compliance_name + '#' + frequency + '#' + due_date_length + '#' + repeats_type + '#' + repeats_every;
            var COMPRow = $('#compliances .table-compliances .row-compliances');
            var clone2 = COMPRow.clone();
            $('.comp-checkbox', clone2).attr('id', 'c-' + SCOUNT);
            $('.comp-checkbox', clone2).val(compliance_id);
            $('.comp-checkbox', clone2).addClass('a-' + (ACOUNT - 1));

            $('.comp-checkbox', clone2).on('click', function() {
                get_selected_count(this);
            });

            $('.combineid-class', clone2).attr('id', 'combineid' + SCOUNT);
            $('.combineid-class', clone2).val(combineId);

            $('.compliancetask', clone2).text(compliance_name);
            $('.desc', clone2).attr('title', compliance_description);

            var dispUnit = '';
            for (var i = 0; i < applicable_units.length; i++) {
                dispUnit = dispUnit + applicable_units[i] + ',';
            }
            $('.appl_unit', clone2).attr('id', 'appl_unit' + SCOUNT);
            $('.appl_unit', clone2).val(dispUnit);

            $('.applicableunits', clone2).find('a').text(disp_appl_unit);
            $('.applicableunits', clone2).find('a').on('click', function(e) {
                displayPopup(dispUnit);
            });

            $('.frequency', clone2).text(frequency);

            statutorydate = statutorydate.replace(/,\s*$/, "");

            if (summary != null) {
                if (statutorydate.trim() != '' && frequency != 'One Time') {
                    statutorydate = summary + ' ( ' + statutorydate + ' )';
                } else {
                    statutorydate = summary;
                }
            }
            $('.summary', clone2).text(statutorydate);
            //$('.summary', clone2).text(summary);

            if (frequency != 'On Occurrence') {
                triggerdate = triggerdate.replace(/,\s*$/, "");
                if (triggerdate == '') {
                    $('.trigger', clone2).html(' <input type="text" value="" class="form-control input-sm trigger" placeholder="Days" id="triggerdate' + SCOUNT + '" maxlength="3"/>');
                    $('.duedate', clone2).html('<input type="text" value="" class="form-control input-sm" readonly="readonly" id="duedate' + SCOUNT + '"/>');
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

            $('#collapse' + (ACOUNT - 1) + ' .tbody-compliance-list').append(clone2);

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
                            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
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
                        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                    ]
                });
            }
            $('#validitydate' + SCOUNT).datepicker({
                changeMonth: true,
                changeYear: true,
                numberOfMonths: 1,
                dateFormat: 'dd-M-yy',
                monthNames: [
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                ]
            });

            $('.edittrigger' + SCOUNT).click(function() {
                var text = $(this).attr('class');
                var clickvalue = text.substring(text.lastIndexOf('r') + 1);
                $('.edittriggertextbox' + clickvalue).show();
                $('.closetrigger' + clickvalue).show();
                $('.edittrigger' + clickvalue).hide();
            });
            $('.closetrigger' + SCOUNT).click(function() {
                var text = $(this).attr('class');
                var clickvalue = text.substring(text.lastIndexOf('r') + 1);
                var isClosed = true;
                $('.edittriggertextbox' + clickvalue + " input").each(function() {

                    if ($(this).val().trim() == '') {
                        isClosed = false;
                        displayMessage(message.compliance_triggerdate_required)
                        return false;
                    }

                    if ($(this).val().trim() > 100) {
                        isClosed = false;
                        displayMessage(message.triggerbefore_exceed);
                        return false;
                    }
                    if ($(this).val().trim() == 0) {
                        isClosed = false;
                        displayMessage(message.triggerbefore_iszero);
                        return false;
                    }
                });
                if (isClosed) {
                    $('.edittriggertextbox' + clickvalue).hide();
                    $('.edittrigger' + clickvalue).show();
                    $('.closetrigger' + clickvalue).hide();
                }
            });
            $('.trigger').on('input', function(e) {
                this.value = isNumbers($(this));
            });
            SCOUNT++;
        });
    }

    if (SCOUNT == 1) {
        NextButton.hide();
        $(".total_count_view").hide();
        var no_record_row = $("#templates .table-no-record tr");
        var noclone = no_record_row.clone();
        $('.tbody-accordion-list').append(noclone);
    } else {
        if (totalRecord == (SCOUNT - 1)) {
            ShowMore.hide();
        } else {
            ShowMore.show();
        }
        $(".total_count").text('Showing 1 to ' + (SCOUNT - 1) + ' of ' + totalRecord + ' entries');
        $(".total_count_view").show();
    }
    hideLoader();
}

function getUserLevel(selectedUserId) {
  var getuserLevel = null;
  for (var user in USERS) {
    var userId = USERS[user].usr_id;
    if (userId == selectedUserId) {
      getuserLevel = USERS[user].usr_cat_id;
    }
  }
  return getuserLevel;
}

//load available user in third wizard
function loadUser(userType) {
    var selectedUnit = null;
    var userClass;
    var sId = 0;
    if (userType == 'assignee') {
        selectedUnit = $('#assignee_unit').val();
        userClass = 'assigneelist';
    } else if (userType == 'concurrence') {
        selectedUnit = $('#concurrence_unit').val();
        userClass = 'concurrencelist';
    } else {
        selectedUnit = $('#approval_unit').val();
        userClass = 'approvallist';
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
    var userLevel = null;
    if (userType == 'concurrence' && approvalUserId != null) {
          userLevel = getUserLevel(approvalUserId);
    } else if (userType == 'approval' && concurrenceUserId != null ) {
          userLevel = getUserLevel(concurrenceUserId);
    }

    var str = '';
    for (var user in USERS) {
        var serviceProviderId = 0;
        if (USERS[user].sp_id != null) {
            serviceProviderId = USERS[user].sp_id;
        }
        //if (selectedUnit == 'all' || parseInt(selectedUnit) == USERS[user].s_u_id || (serviceProviderId > 0 && selectedUnit != '')) {
        if (selectedUnit == 'all' || parseInt(selectedUnit) == USERS[user].s_u_id) {
            var userId = USERS[user].usr_id;
            var userCategoryId = USERS[user].usr_cat_id;
            var empCode = USERS[user].emp_code;
            var userName = '';
            if (empCode != null && empCode != '') {
                userName = USERS[user].emp_code + ' - ' + USERS[user].emp_name;
            } else {
                userName = USERS[user].emp_name;
            }

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
            if (userType == 'concurrence' && USERS[user].usr_cat_id == 1) {
                concurrenceStatus = false;
            }

            if (userLevel != null) {
                if (userType == 'concurrence') {
                  conditionResult = userCategoryId >= userLevel;
                } else if (userType == 'approval') {
                  conditionResult = userCategoryId <= userLevel;
                }
            }

            //if (userPermission && conditionResult && (assigneeUserId == null || assigneeUserId != userId) && (approvalUserId == null || approvalUserId != userId) && (concurrenceUserId == null || concurrenceUserId != userId) && (serviceProviderId == 0 || sId == serviceProviderId || sId == 0) && concurrenceStatus) {
            if (userPermission && conditionResult && (assigneeUserId == null || assigneeUserId != userId) && (approvalUserId == null || approvalUserId != userId) && (concurrenceUserId == null || concurrenceUserId != userId) && concurrenceStatus) {
                str += '<li id="' + combine + '" class="' + userClass + '" >' + userName + ' <i></i> </li>';
            }
        }
    }
    $('#' + userType).append(str);
}

$('#assignee_unit').change(function() {
    loadUser('assignee');
});

$('#concurrence_unit').change(function() {
    var assigneeSelectedId = '';
    if ($('.assigneelist.active').attr('id') != undefined) {
        assigneeSelectedId = $('.assigneelist.active').attr('id').split('-')[0];
    }
    loadUser('concurrence');
});

$('#approval_unit').change(function() {
    var assigneeSelectedId = '';
    if ($('.assigneelist.active').attr('id') != undefined) {
        assigneeSelectedId = $('.assigneelist.active').attr('id').split('-')[0];
    }
    loadUser('approval');
});

$('#assignee').click(function(event) {
    var chkstatus = $(event.target).attr('class');
    if (chkstatus != undefined && chkstatus != 'list-unstyled') {
        if (chkstatus == 'assigneelist active') {
            $(event.target).removeClass('active');
            $(event.target).find('i').removeClass('fa fa-check pull-right');
        } else {
            $('.assigneelist').each(function(index, el) {
                $(el).removeClass('active');
                $(el).find('i').removeClass('fa fa-check pull-right');
            });
            $(event.target).addClass('active');
            $(event.target).find('i').addClass('fa fa-check pull-right');
        }
    }
});

$('#concurrence').click(function(event) {
    var chkstatus = $(event.target).attr('class');
    if (chkstatus != undefined && chkstatus != 'list-unstyled') {
        if (chkstatus == 'concurrencelist active') {
            $(event.target).removeClass('active');
            $(event.target).find('i').removeClass('fa fa-check pull-right');
        } else {
            $('.concurrencelist').each(function(index, el) {
                $(el).removeClass('active');
                $(el).find('i').removeClass('fa fa-check pull-right');
            });
            $(event.target).addClass('active');
            $(event.target).find('i').addClass('fa fa-check pull-right');
        }
        loadUser('approval');
    }
});

$('#approval').click(function(event) {
    var chkstatus = $(event.target).attr('class');
    if (chkstatus != undefined && chkstatus != 'list-unstyled') {
        if (chkstatus == 'approvallist active') {
            $(event.target).removeClass('active');
            $(event.target).find('i').removeClass('fa fa-check pull-right');
        } else {
            $('.approvallist').each(function(index, el) {
                $(el).removeClass('active');
                $(el).find('i').removeClass('fa fa-check pull-right');
            });
            $(event.target).addClass('active');
            $(event.target).find('i').addClass('fa fa-check pull-right');
        }
        //loadUser('concurrence');
    }
});

function loadSeatingUnits() {
    $('#assignee').empty();
    $('#concurrence').empty();
    $('#approval').empty();

    $('#assignee_unit').empty();
    $('#assignee_unit').append('<option value=""> Select </option>');
    $('#assignee_unit').append('<option value="all"> All </option>');
    $.each(ASSIGNEE_SU, function(key, value) {
        var option = $('<option></option>');
        option.val(key);
        option.text(value);
        $('#assignee_unit').append(option);
    });
    $('#concurrence_unit').empty();
    $('#concurrence_unit').append('<option value=""> Select </option>');
    $('#concurrence_unit').append('<option value="all"> All </option>');
    $.each(APPROVER_SU, function(key, value) {
        var option = $('<option></option>');
        option.val(key);
        option.text(value);
        $('#concurrence_unit').append(option);
    });
    $('#approval_unit').empty();
    $('#approval_unit').append('<option value=""> Select </option>');
    $('#approval_unit').append('<option value="all"> All </option>');
    $.each(APPROVER_SU, function(key, value) {
        var option = $('<option></option>');
        option.val(key);
        option.text(value);
        $('#approval_unit').append(option);
    });

    if (two_level_approve) {
        $('.c-view').show();
      } else {
        $('.c-view').hide();
    }
}

function showTab() {
    hideall = function() {
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
        if (isPrevious) {
            $(".total_count_view").show();
            hideall();
            enabletabevent(2);
            $('.tab-step-2').addClass('active')
            $('#tab2').addClass('active in');
            $('#tab2').show();
            PreviousButton.show();
            NextButton.show();
            isPrevious = false;
        } else {
            if (validateFirstTab() == false) {
                CURRENT_TAB -= 1;
                return false;
            } else {
                displayLoader();
                var le_id = LEList.find("li.active").attr("id");
                var d_id = DomainList.find("li.active").attr("id");
                $('.selected_count').text('Selected Compliance: 0');
                client_mirror.getComplianceTotalToAssign(
                    parseInt(le_id), ACTIVE_UNITS, parseInt(d_id), ACTIVE_FREQUENCY,
                    function(error, data) {
                        if (error == null) {
                            totalRecord = data.r_count;
                            callAPI(GET_COMPLIANCE);
                            hideall();
                            enabletabevent(2);
                            $('.tab-step-2').addClass('active')
                            $('#tab2').addClass('active in');
                            $('#tab2').show();
                            PreviousButton.show();
                            NextButton.show();
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

    } else if (CURRENT_TAB == 3) {
        if (validateSecondTab() == false) {
            CURRENT_TAB -= 1;
            return false;
        } else {

            displayLoader();
            var le_id = LEList.find("li.active").attr("id");
            var d_id = DomainList.find("li.active").attr("id");
            client_mirror.getUserToAssignCompliance(
                parseInt(d_id), ACTIVE_UNITS, parseInt(le_id),
                function(error, data) {
                    if (error == null) {
                        USERS = data.assign_users;
                        $.each(USERS, function(key, value) {
                            id = value.s_u_id;
                            text = value.s_u_name;
                            assignee_flag = value.is_assignee;
                            approver_flag = value.is_approver;
                            if (id != null && assignee_flag && text != '' && text != null) ASSIGNEE_SU[id] = text;

                            if (id != null && approver_flag && text != '' && text != null) APPROVER_SU[id] = text;
                        });
                        loadSeatingUnits();
                        hideall();
                        enabletabevent(3);
                        $('.tab-step-3').addClass('active')
                        $('#tab3').addClass('active in');
                        $('#tab3').show();
                        PreviousButton.show();
                        NextButton.hide();
                        SubmitButton.show();
                        hideLoader();
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
        UNITS = null;
    } else if (levelvalue == 'division') {
        CategoryList.empty();
        UnitList.empty();
    } else if (levelvalue == 'category') {
        UnitList.empty();
    } else if (levelvalue == 'domain') {
        ACTIVE_UNITS = [];
        ACTIVE_FREQUENCY = [];
        UnitList.empty();
        FrequencyList.empty();
    } else if (levelvalue == 'unit') {
        ACTIVE_FREQUENCY = [];
        FrequencyList.empty();
    }
}

function loadChild(levelvalue) {
    if (levelvalue == 'legalentity') {
        loadDivision();
        loadCategory();
        loadDomain();
    } else if (levelvalue == 'division') {
        loadCategory();
        if(UNITS != null){
            loadUnit();
        }
        
    } else if (levelvalue == 'category') {
        if(UNITS != null){
            loadUnit();
        }
    } else if (levelvalue == 'domain') {
        callAPI(WIZARD_ONE_UNIT_FILTER);
    } else if (levelvalue == 'unit') {
        loadFrequency();
    }
}

function activateList(element, levelvalue) {
    $('#' + levelvalue + ' li').each(function(index, el) {
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
        if (levelvalue == 'unit') {
            index = ACTIVE_UNITS.indexOf(parseInt(chkid));
            ACTIVE_UNITS.splice(index, 1);
        } else {
            index = ACTIVE_FREQUENCY.indexOf(parseInt(chkid));
            ACTIVE_FREQUENCY.splice(index, 1);
        }

    } else {
        $(element).addClass('active');
        $(element).find('i').addClass('fa fa-check pull-right');

        if (ACTIVE_UNITS.length >= mUnit) {
            displayMessage(message.maximum_units);
            return false;
        } else {
            $(element).addClass('active');
            $(element).find('i').addClass('fa fa-check pull-right');
            if (levelvalue == 'unit') {
                ACTIVE_UNITS.push(parseInt(chkid));
            } else {
                ACTIVE_FREQUENCY.push(parseInt(chkid));
            }
        }
    }
    clearValues(levelvalue);
    loadChild(levelvalue);
}

function loadLegalEntity() {
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

function loadDivision() {
    $.each(DIVISIONS, function(key, value) {
        id = value.div_id;
        text = value.div_name;

        var le_id = LEList.find("li.active").attr("id");
        if (le_id == value.le_id) {
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

function loadCategory() {
    $.each(CATEGORIES, function(key, value) {
        id = value.cat_id;
        text = value.cat_name;

        var le_id = LEList.find("li.active").attr("id");
        var div_id = '';
        if (DivisionList.find("li.active").attr("id") != undefined) {
            div_id = DivisionList.find("li.active").attr("id");
        }
        if (le_id == value.le_id && (div_id == '' || div_id == value.div_id)) {
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

function loadDomain() {
    $.each(DOMAINS, function(key, value) {
        id = value.d_id;
        text = value.d_name;

        var le_id = LEList.find("li.active").attr("id");

        if (le_id == value.le_id) {
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

function loadUnit() {
    $.each(UNITS, function(key, value) {
        id = value.u_id;
        text = value.u_name;
        var cat_id = CategoryList.find("li.active").attr("id");
        var div_id = DivisionList.find("li.active").attr("id");

        if((cat_id == undefined || cat_id == value.category_id) && (div_id == undefined || div_id == value.division_id)){
            var clone = ULRow.clone();
            clone.html(text + '<i></i>');
            clone.attr('id', id);
            UnitList.append(clone);
            clone.click(function() {
                activateMultiList(this, 'unit');
            });
        }
    });
}

function containsAll(arr1, arr2) {
    for (var i = 0, len = arr1.length; i < len; i++) {
        if ($.inArray(arr1[i], arr2) == -1) return false;
    }
    return true;
}

function loadFrequency() {
    $.each(FREQUENCY, function(key, value) {
        id = value.frequency_id;
        text = value.frequency;
        FREQUENCY_UNITS = value.u_ids;
        if (ACTIVE_UNITS.length == 1 || (id != 3 && id != 4)) {
            if(ACTIVE_UNITS.length > 0 && containsAll(ACTIVE_UNITS, FREQUENCY_UNITS)){
                var clone = ULRow.clone();
                clone.html(text + '<i></i>');
                clone.attr('id', id);
                FrequencyList.append(clone);
                clone.click(function() {
                    activateMultiList(this, 'frequency');
                });
            }            
        }
    });
}

//validation on third wizard
function validate_thirdtab() {
    if ($('.assigneelist.active').text() == '') {
        displayMessage(message.assignee_required);
        return false;
    } else if ($('.concurrencelist.active').text() == '' && two_level_approve) {
        displayMessage(message.concurrence_required);
        return false;
    } else if ($('.approvallist.active').text() == '') {
        displayMessage(message.approval_required);
        return false;
    } else {
        return true;
    }
}

function pageControls() {
    NextButton.click(function() {
        //$('.tbody-compliance-list').empty();
        CURRENT_TAB += 1;
        showTab();
    });
    PreviousButton.click(function() {
        $(".total_count_view").hide();
        CURRENT_TAB = CURRENT_TAB - 1;

        if (CURRENT_TAB == 2) {
            isPrevious = true;
        } else {
            isPrevious = false;
        }

        showTab();
    });
    ShowMore.click(function() {
        callAPI(GET_COMPLIANCE);
    });
    SubmitButton.click(function() {
        if (validate_thirdtab()) {
            displayLoader();
            setTimeout(function() {
                callAPI(SUBMIT_API)
            }, 500);
        }
    });

    Filter_List.keyup(function() {
        var currentFilter = '#' + $(this).attr("class").split(' ').pop() + ' > li';
        var searchText = $(this).val().toLowerCase();
        $(currentFilter).each(function() {
            var currentLiText = $(this).text().toLowerCase();
            showCurrentLi = currentLiText.indexOf(searchText) !== -1;
            $(this).toggle(showCurrentLi);
        });
    });

}

function getCountryId(LE_ID) {
    var C_ID = 0;
    $.each(LEGAL_ENTITIES, function(key, value) {
        if (value.le_id == LE_ID) {
            C_ID = value.c_id;
        }
    });
    return C_ID;
}

function initialize() {
    Filter_List.val('');
    LEList.empty();
    showTab();
    clearValues('legalentity')
    LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();
    callAPI(WIZARD_ONE_FILTER);
    hideLoader();
}

$(function() {
    current_date(function (c_date){
        currentDate = c_date;
        initialize();
        pageControls();
    });
});