var countriesList;
var businessgroupsList;
var legalentitiesList;
var divisionsList;
var unitsList;
var usersList;
var assignStatutoryUnitIds = [];
var assignStatutoryUnitValues = [];
var statutoriesList;
var two_level_approve;
var client_admin;
var domainsList;
var accordionstatus = true;
var seatingunitsList = {};
var statutoriesNameList;
var totalRecord;
var lastActName = '';
var count = 1;
var statutoriesCount = 1;
var actCount = 1;
var s_endCount = 0;
var mUnit = 50;
var mCompliances = 500;
var msg = '';
function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
//clear list values
function clearValues(levelvalue) {
  if (levelvalue == 'country') {
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    $('#businessgroup').empty();
    $('#legalentity').empty();
    $('#division').empty();
    $('#unit').empty();
    $('#domain').empty();
  }
  if (levelvalue == 'businessgroup') {
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    $('#legalentity').empty();
    $('#division').empty();
    $('#unit').empty();
    $('#domain').empty();
  }
  if (levelvalue == 'legalentity') {
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    $('#division').empty();
    $('#unit').empty();
    $('#domain').empty();
  }
  if (levelvalue == 'division') {
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    $('#unit').empty();
    $('#domain').empty();
  }
  if (levelvalue == 'unit') {
    $('#domain').empty();
  }
}
function actstatus(element) {
  $('ul.setup-panel li:eq(2)').addClass('disabled');
  var changestatusStatutories = '.statutoryclass' + $(element).val();
  if ($(element).is(':checked')) {
    $(changestatusStatutories).each(function () {
      this.checked = true;
    });
  } else {
    $(changestatusStatutories).each(function () {
      this.checked = false;
    });
  }
  accordionstatus = false;
}
function compliancestatus(element) {
  $('ul.setup-panel li:eq(2)').addClass('disabled');
  var sClass = $(element).attr('class').split(' ')[1];
  var actSelect = sClass.substr(sClass.lastIndexOf('s') + 1);
  var cStatus = false;
  $('.' + sClass).each(function () {
    if (this.checked) {
      cStatus = true;
    }
  });
  if (cStatus) {
    $('#act' + actSelect).prop('checked', true);
  } else {
    $('#act' + actSelect).prop('checked', false);
  }
}
$('.close').click(function () {
  $('.overlay').css('visibility', 'hidden');
  $('.overlay').css('opacity', '0');
});
//display applicable unit details in popup
function disppopup(units_string) {
  $('.overlay').css('visibility', 'visible');
  $('.overlay').css('opacity', '1');
  $('.popup-list').find('tr').remove();
  var units = units_string.split(',');
  for (var i = 0; i < units.length - 1; i++) {
    var dispUnit = '';
    $.each(unitsList, function (index, value) {
      if (value.unit_id == parseInt(units[i])) {
        dispUnit = value.unit_name + ' - ' + value.address;
      }
    });
    var tableRow = $('#templates .table-popup-list .table-row');
    var clone = tableRow.clone();
    $('.popup_unitname', clone).text(dispUnit);
    $('.popup-list').append(clone);
  }
}
//load available compliance based on first wizard
function load_secondwizard() {
  if (statutoriesCount <= 1) {
    $('.tbody-assignstatutory').find('tbody').remove();
  }
  var selectedDomain = $('.domainlist.active').attr('id');
  var actname = '';
  for (var l = 0; l < statutoriesNameList.length; l++) {
    actname = statutoriesNameList[l];
    if (actname != lastActName) {
      var acttableRow = $('#act-templates .font1 .tbody-heading');
      var clone = acttableRow.clone();
      $('.actname-ckbox', clone).attr('id', 'act' + actCount);
      $('.actname-ckbox', clone).val(actCount);
      $('.actname-label', clone).attr('for', 'act' + actCount);
      $('.actname-label', clone).text(actname);
      $('.tbody-assignstatutory').append(clone);
      $('.tbody-assignstatutory').append('<tbody class="accordion-content accordion-content' + count + ' default"></tbody>');
      var complianceHeadingtableRow = $('#statutory-templates .compliance-heading');
      var clone1 = complianceHeadingtableRow.clone();
      $('.accordion-content' + count).append(clone1);
      actCount = actCount + 1;
      count++;
      lastActName = actname;
      $(clone, '.actname').click(function () {
        if (accordionstatus) {
          //Expand or collapse this panel
          $(this).next().slideToggle('fast');
          //Hide the other panels
          $('.accordion-content').not($(this).next()).slideUp('fast');
        } else {
          accordionstatus = true;
        }
      });
    }
    var actList = statutoriesList[actname];
    $.each(actList, function (key, value) {
      var statutoryprovision = '';
      var compliance_id = value.compliance_id;
      var compliance_name = value.compliance_name;
      var compliance_description = value.description;
      var applicable_units = value.applicable_units;
      var frequency = value.frequency;
      var statutory_date = value.statutory_date;
      var due_date = value.due_date;
      var summary = value.summary;
      var triggerdate = '';
      var statutorydate = '';
      var elementTriggerdate = '';
      var elementDuedate = '';
      var due_date_length = 0;
      var repeats_type = value.repeats_by;
      var repeats_every = value.repeats_every;
      if (due_date != '' || due_date != null) {
        if (due_date.length > 1) {
          for (var k = 0; k < due_date.length; k++) {
            elementDuedate += '<input type="text" id="duedate' + statutoriesCount + '-' + k + '" readonly="readonly" class="input-box" value="' + due_date[k] + '"/>';
          }
        } else {
          elementDuedate += '<input type="text" id="duedate' + statutoriesCount + '" readonly="readonly" class="input-box" value="' + due_date[0] + '"/>';
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
          sMonth = getMonth_IntegettoString(sMonth);
        if (tDays != '') {
          triggerdate += tDays + ' Day(s) ';
        }
        statutorydate += sMonth + ' ' + sDay + ' ';
        if (statutory_date.length > 1) {
          elementTriggerdate += '<input type="text" id="triggerdate' + statutoriesCount + '-' + j + '" placeholder="Days" class="input-box trigger" value="' + tDays + '" maxlength="3" style="width:50px; float:left;" />';
        } else {
          elementTriggerdate += '<input type="text" id="triggerdate' + statutoriesCount + '" placeholder="Days" class="input-box trigger" value="' + tDays + '" maxlength="3" style="width:50px; float:left;" />';
        }
      }
      var combineId = compliance_id + '#' + compliance_name + '#' + frequency + '#' + due_date_length + '#' + repeats_type + '#' + repeats_every;
      var complianceDetailtableRow = $('#statutory-values .table-statutory-values .compliance-details');
      var clone2 = complianceDetailtableRow.clone();
      $('.ckbox', clone2).attr('id', 'statutory' + statutoriesCount);
      $('.ckbox', clone2).addClass('statutoryclass' + (actCount - 1));
      $('.combineid-class', clone2).attr('id', 'combineid' + statutoriesCount);
      $('.combineid-class', clone2).val(combineId);
      $('.sno', clone2).text(statutoriesCount);
      $('.compliancetask span', clone2).html(compliance_name);
      $('.compliancetask abbr', clone2).attr('title', compliance_description);
      var dispApplicableUnits = applicable_units.length + '/' + assignStatutoryUnitIds.length;
      var dispUnit = '';
      for (var i = 0; i < applicable_units.length; i++) {
        dispUnit = dispUnit + applicable_units[i] + ',';
      }
      $('.appl_unit', clone2).attr('id', 'appl_unit' + statutoriesCount);
      $('.appl_unit', clone2).val(dispUnit);
      $('.popup-link', clone2).text(dispApplicableUnits);
      $('.popup-link', clone2).on('click', function () {
        disppopup(dispUnit);
      });
      $('.compliancefrequency', clone2).text(frequency);
      if (summary != null) {
        if (statutorydate.trim() != '') {
          statutorydate = summary + ' ( ' + statutorydate + ' )';
        } else {
          statutorydate = summary;
        }
      }
      $('.statutorydate', clone2).text(statutorydate);
      if (frequency != 'On Occurrence') {
        if (triggerdate == '') {
          $('.triggerbefore', clone2).html(' <input type="text" value="" class="input-box trigger" placeholder="Days" id="triggerdate' + statutoriesCount + '" maxlength="3"/>');
          $('.duedate', clone2).html('<input type="text" value="" class="input-box" readonly="readonly" id="duedate' + statutoriesCount + '" />');
        } else {
          $('.triggerbefore', clone2).html('<span style="float:right;padding-right:30px;" class="edittrigger' + statutoriesCount + '" value="' + statutoriesCount + '"><img src="/images/icon-edit.png" width="12"></span> <span style="float:right;display: none;padding-right:30px;" class="closetrigger' + statutoriesCount + '" value="' + statutoriesCount + '"><img src="/images/delete.png" width="12"></span>' + triggerdate + '<div class="edittriggertextbox' + statutoriesCount + '" style="display:none;padding-top:10px;">' + elementTriggerdate + '</div>');
          $('.duedate', clone2).html('<div>' + elementDuedate + '</div>');
        }
      }
      if (frequency == 'Periodical' || frequency == 'Review') {
        $('.vdate', clone2).attr('id', 'validitydate' + statutoriesCount);
      } else {
        $('.validitydate', clone2).html('');
      }
      $('.accordion-content' + (count - 1)).append(clone2);
      var duename = statutoriesCount;
      if (due_date.length > 1) {
        for (var k = 0; k < due_date.length; k++) {
          duename = statutoriesCount + '-' + k;
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
      $('#validitydate' + statutoriesCount).datepicker({
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
      $('.edittrigger' + statutoriesCount).click(function () {
        var text = $(this).attr('class');
        var clickvalue = text.substring(text.lastIndexOf('r') + 1);
        $('.edittriggertextbox' + clickvalue).show();
        $('.closetrigger' + clickvalue).show();
        $('.edittrigger' + clickvalue).hide();
      });
      $('.closetrigger' + statutoriesCount).click(function () {
        var text = $(this).attr('class');
        var clickvalue = text.substring(text.lastIndexOf('r') + 1);
        $('.edittriggertextbox' + clickvalue).hide();
        $('.edittrigger' + clickvalue).show();
        $('.closetrigger' + clickvalue).hide();
      });
      $('.trigger').on('input', function (e) {
        this.value = isNumbers($(this));
      });
      statutoriesCount = statutoriesCount + 1;
    });
  }
  if (statutoriesCount > 1) {
    $('.compliance_count').text('Showing ' + 1 + ' to ' + (statutoriesCount - 1) + ' of ' + totalRecord);
  } else {
    $('.compliance_count').text('');
  }
  if (totalRecord <= statutoriesCount - 1 && statutoriesCount > 1) {
    $('#pagination').hide();
    $('#activate-step-3').show();
  } else {
    $('#pagination').show();
    $('#activate-step-3').show();
  }
  if (count <= 1) {
    var norecordtableRow = $('#no-record-templates .font1');
    var noclone = norecordtableRow.clone();
    $('.tbody-assignstatutory').append(noclone);
    $('#activate-step-3').hide();
    $('#pagination').hide();
  }
}
//pagination process
$('#pagination').click(function () {
  var domainID = $('.domainlist.active').attr('id');
  unit_id = parseInt($('#unit').val());
  s_endCount = statutoriesCount - 1;
  displayLoader();
  client_mirror.getAssignComplianceForUnits(assignStatutoryUnitIds, parseInt(domainID), s_endCount, function (error, response) {
    if (error == null) {
      statutoriesList = response.statutories;
      statutoriesNameList = response.level_one_name;
      totalRecord = response.total_count;
      load_secondwizard();
      hideLoader();
    } else {
      displayMessage(error);
      hideLoader();
    }
  });
});
//find date difference between two dates
function daydiff(first, second) {
  return (second - first) / (1000 * 60 * 60 * 24);
}
//validation on first wizard
function validate_firsttab() {
  if ($('.countrylist.active').text() == '') {
    displayMessage(message.country_required);
    return false;
  } else if ($('.legalentitylist.active').text() == '') {
    displayMessage(message.legalentity_required);
    return false;
  } else if (assignStatutoryUnitIds.length == 0) {
    displayMessage(message.unit_required);
    return false;
  } else if ($('.domainlist.active').text() == '') {
    displayMessage(message.domain_required);
    return false;
  } else {
    s_endCount = 0;
    var domainID = $('.domainlist.active').attr('id');
    displayMessage('');
    count = 1;
    statutoriesCount = 1;
    actCount = 1;
    lastActName = '';
    displayMessage('');
    if (assignStatutoryUnitIds.length > 0) {
      displayLoader();
      function onSuccess(data) {
        statutoriesList = data.statutories;
        statutoriesNameList = data.level_one_name;
        totalRecord = data.total_count;
        load_secondwizard();
        hideLoader();
      }
      function onFailure(error) {
        hideLoader();
        displayMessage(error);
      }
      client_mirror.getAssignComplianceForUnits(assignStatutoryUnitIds, parseInt(domainID), s_endCount, function (error, response) {
        if (error == null) {
          onSuccess(response);
        } else {
          onFailure(error);
        }
      });
    }
    return true;
  }
}
function validate_secondtab() {
  var tCompliance = 1;
  var maxCompliance = 0;
  for (var i = 1; i <= actCount - 1; i++) {
    var actComplianceCount = $('.statutoryclass' + i).length;
    for (var j = 1; j <= actComplianceCount; j++) {
      if ($('#statutory' + tCompliance).is(':checked')) {
        maxCompliance++;
      }
      tCompliance++;
    }
  }
  if (maxCompliance == 0) {
    displayMessage(message.nocompliance_selected_forassign);
    return false;
  } else if (maxCompliance > mCompliances) {
    msg = 'Maximum(' + mCompliances + ') ';
    displayMessage(msg + message.maximum_compliances);
    return false;
  } else {
    displayMessage('');
    return true;
  }
}
//validation on third wizard
function validate_thirdtab() {
  if ($('.assigneelist.active').text() == '') {
    displayMessage(message.assignee_required);
    return false;
  } else if ($('.concurrencelist.active').text() == '' && two_level_approve && $('.assigneelist.active').attr('id').split('-')[0] != client_admin) {
    displayMessage(message.concurrence_required);
    return false;
  } else if ($('.approvallist.active').text() == '' && $('.assigneelist.active').attr('id').split('-')[0] != client_admin) {
    displayMessage(message.approval_required);
    return false;
  } else {
    displayMessage('');
    return true;
  }  //return true;
}
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
//save and assign compliances for selectd unit
function submitcompliance() {
  displayLoader();
  var newSettingsList = [];
  var newSetting = null;
  var assignComplianceCountryId = [];
  var acCountryId = null;
  var assignComplianceDomainId = null;
  var assignComplianceDomainVal = null;
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
  assignComplianceCountryId.push(parseInt($('.countrylist.active').attr('id')));
  acCountryId = parseInt($('.countrylist.active').attr('id'));
  assignComplianceDomainId = parseInt($('.domainlist.active').attr('id'));
  assignComplianceDomainVal = $('.domainlist.active').text();
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
  if (assignComplianceAssigneeId == client_admin) {
    assignComplianceApprovalId = assignComplianceAssigneeId;
    assignComplianceApprovalName = assignComplianceAssigneeName;
  }
  assignCompliance = [];
  var totalCompliance = 1;
  var selectedStatus = false;
  var applicableUnitsArray = [];
  for (var i = 1; i <= actCount - 1; i++) {
    var actComplianceCount = $('.statutoryclass' + i).length;
    for (var j = 1; j <= actComplianceCount; j++) {
      var complianceApplicable = false;
      if ($('#statutory' + totalCompliance).is(':checked')) {
        complianceApplicable = true;
        selectedStatus = true;
      }
      if (complianceApplicable) {
        var combineidVal = $('#combineid' + totalCompliance).val().split('#');
        var compliance_id = parseInt(combineidVal[0]);
        var compliance_name = combineidVal[1];
        var due_date = parseInt(combineidVal[3]);
        var frequency = combineidVal[2];
        var repeats_type = combineidVal[4];
        var repeats_every = combineidVal[5];
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
    var assigneeInserUnits = [];
    var assigneeInserUnitsVal = [];
    var assigneeInserDomain = [];
    if (assignComplianceAssigneeId != client_admin && assignComplianceAssigneeId != null) {
      var userUnits;
      var userDomains;
      for (var user in usersList) {
        if (usersList[user].user_id == assignComplianceAssigneeId) {
          userUnits = usersList[user].unit_ids;
          userDomains = usersList[user].domain_ids;
          if ($.inArray(assignComplianceDomainId, userDomains) == -1) {
            assigneeInserDomain.push(assignComplianceDomainId);
          }
        }
      }
      for (var k = 0; k < applicableUnitsArray.length; k++) {
        if ($.inArray(applicableUnitsArray[k], userUnits) == -1) {
          assigneeInserUnits.push(applicableUnitsArray[k]);
          for (var unit in unitsList) {
            if (unitsList[unit].unit_id == applicableUnitsArray[k]) {
              assigneeInserUnitsVal.push(unitsList[unit].unit_name);
            }
          }
        }
      }
    }
    var concurrenceInserUnits = [];
    var concurrenceInserUnitsVal = [];
    var concurrenceInserDomain = [];
    if (assignComplianceConcurrenceId != null) {
      var userUnits;
      var userDomains;
      for (var user in usersList) {
        if (usersList[user].user_id == assignComplianceConcurrenceId) {
          userUnits = usersList[user].unit_ids;
          userDomains = usersList[user].domain_ids;
          if ($.inArray(assignComplianceDomainId, userDomains) == -1) {
            concurrenceInserDomain.push(assignComplianceDomainId);
          }
        }
      }
      for (var k = 0; k < applicableUnitsArray.length; k++) {
        if ($.inArray(applicableUnitsArray[k], userUnits) == -1) {
          concurrenceInserUnits.push(applicableUnitsArray[k]);
          for (var unit in unitsList) {
            if (unitsList[unit].unit_id == applicableUnitsArray[k]) {
              concurrenceInserUnitsVal.push(unitsList[unit].unit_name);
            }
          }
        }
      }
    }
    var approvalInserUnits = [];
    var approvalInserUnitsVal = [];
    var approvalInserDomain = [];
    if (assignComplianceApprovalId != client_admin && assignComplianceApprovalId != null) {
      var userUnits;
      var userDomains;
      for (var user in usersList) {
        if (usersList[user].user_id == assignComplianceApprovalId) {
          userUnits = usersList[user].unit_ids;
          userDomains = usersList[user].domain_ids;
          if ($.inArray(assignComplianceDomainId, userDomains) == -1) {
            approvalInserDomain.push(assignComplianceDomainId);
          }
        }
      }
      for (var k = 0; k < applicableUnitsArray.length; k++) {
        if ($.inArray(applicableUnitsArray[k], userUnits) == -1) {
          approvalInserUnits.push(applicableUnitsArray[k]);
          for (var unit in unitsList) {
            if (unitsList[unit].unit_id == applicableUnitsArray[k]) {
              approvalInserUnitsVal.push(unitsList[unit].unit_name);
            }
          }
        }
      }
    }
    var unit_names = '';
    for (var unit in unitsList) {
      if ($.inArray(unitsList[unit].unit_id, assignStatutoryUnitIds) >= 0) {
        if (unit_names == '') {
          unit_names += unitsList[unit].unit_name;
        } else {
          unit_names += ', ' + unitsList[unit].unit_name;
        }
      }
    }
    if (assigneeInserUnits.length > 0 || concurrenceInserUnits.length > 0 || approvalInserUnits.length > 0 || assigneeInserDomain.length > 0 || concurrenceInserDomain.length > 0 || approvalInserDomain.length > 0) {
      var assigneeText = '';
      var concurrenceText = '';
      var approvalText = '';
      if (assigneeInserUnits.length > 0 || assigneeInserDomain.length > 0) {
        if (assigneeInserDomain.length > 0) {
          assigneeText = assignComplianceDomainVal + ' domain(s) ';
        } else {
          assigneeInserDomain = null;
        }
        if (assigneeInserUnits.length > 0) {
          assigneeText = assigneeText + assigneeInserUnitsVal + ' unit(s) ';
        } else {
          assigneeInserUnits = null;
        }
        assigneeText = assigneeText + 'not applicable for Assignee. ';
        newSetting = client_mirror.newUnitSettings(assignComplianceAssigneeId, assigneeInserUnits, assigneeInserDomain, assignComplianceCountryId);
        newSettingsList.push(newSetting);
      }
      if (concurrenceInserUnits.length > 0 || concurrenceInserDomain.length > 0) {
        if (concurrenceInserDomain.length > 0) {
          concurrenceText = assignComplianceDomainVal + ' domain ';
        } else {
          concurrenceInserDomain = null;
        }
        if (concurrenceInserUnits.length > 0) {
          concurrenceText = concurrenceText + concurrenceInserUnitsVal + ' unit(s) ';
        } else {
          concurrenceInserUnits = null;
        }
        concurrenceText = concurrenceText + 'not applicable for Concurrence. ';
        newSetting = client_mirror.newUnitSettings(assignComplianceConcurrenceId, concurrenceInserUnits, concurrenceInserDomain, assignComplianceCountryId);
        newSettingsList.push(newSetting);
      }
      if (approvalInserUnits.length > 0 || approvalInserDomain.length > 0) {
        if (approvalInserDomain.length > 0) {
          approvalText = assignComplianceDomainVal + ' domain ';
        } else {
          approvalInserDomain = null;
        }
        if (approvalInserUnits.length > 0) {
          approvalText = approvalText + approvalInserUnitsVal + ' unit(s) ';
        } else {
          approvalInserUnits = null;
        }
        approvalText = approvalText + 'not applicable for Approval. ';
        newSetting = client_mirror.newUnitSettings(assignComplianceApprovalId, approvalInserUnits, approvalInserDomain, assignComplianceCountryId);
        newSettingsList.push(newSetting);
      }
      var msgstatus = assigneeText + concurrenceText + approvalText + 'Do you want to add in settings ?';
      $('.warning-confirm').dialog({
        title: 'Add in Settings',
        buttons: {
          Ok: function () {
            $(this).dialog('close');
            function onSuccess(data) {
              //getAssignedStatutories ();
              message = 'The selected task items have been assigned to ' + assignComplianceAssigneeName;
              $('.warning-confirm').dialog({
                title: 'Success',
                buttons: {
                  Ok: function () {
                    $(this).dialog('close');
                    getAssignCompliances();
                    $('ul.setup-panel li:eq(0)').addClass('active');
                    $('ul.setup-panel li:eq(1)').addClass('disabled');
                    $('ul.setup-panel li:eq(2)').addClass('disabled');
                    $('ul.setup-panel li a[href="#step-1"]').trigger('click');
                    $('.tbody-assignstatutory').find('tbody').remove();
                    $('#assignee').empty();
                    $('#concurrence').empty();
                    $('#approval').empty();
                    load_firstwizard();
                    hideLoader();
                  }
                },
                open: function () {
                  $('.warning-message').html(message);
                }
              });
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
            client_mirror.saveAssignedComplianceFormData(acCountryId, assignComplianceAssigneeId, assignComplianceAssigneeName, assignComplianceConcurrenceId, assignComplianceConcurrenceName, assignComplianceApprovalId, assignComplianceApprovalName, assignCompliance, newSettingsList, function (error, response) {
              if (error == null) {
                onSuccess(response);
              } else {
                onFailure(error, response);
              }
            });
          },
          Cancel: function () {
            $(this).dialog('close');
            hideLoader();
          }
        },
        open: function () {
          $('.warning-message').html(msgstatus);
        }
      });
    } else {
      newSettingsList = null;
      function onSuccess(data) {
        message = 'The selected task items have been assigned to ' + assignComplianceAssigneeName;
        $('.warning-confirm').dialog({
          title: 'Success',
          buttons: {
            Ok: function () {
              $(this).dialog('close');
              getAssignCompliances();
              $('ul.setup-panel li:eq(0)').addClass('active');
              $('ul.setup-panel li:eq(1)').addClass('disabled');
              $('ul.setup-panel li:eq(2)').addClass('disabled');
              $('ul.setup-panel li a[href="#step-1"]').trigger('click');
              $('.tbody-assignstatutory').find('tbody').remove();
              $('#assignee').empty();
              $('#concurrence').empty();
              $('#approval').empty();
              load_firstwizard();
              hideLoader();
            }
          },
          open: function () {
            $('.warning-message').html(message);
          }
        });
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
      client_mirror.saveAssignedComplianceFormData(acCountryId, assignComplianceAssigneeId, assignComplianceAssigneeName, assignComplianceConcurrenceId, assignComplianceConcurrenceName, assignComplianceApprovalId, assignComplianceApprovalName, assignCompliance, newSettingsList, function (error, response) {
        if (error == null) {
          onSuccess(response);
        } else {
          onFailure(error, response);
        }
      });
    }
  } else {
    hideLoader();
    displayMessage(message.nocompliance_selected_forassign);
  }
}
//create wizard
var navListItems = $('ul.setup-panel li a'), allWells = $('.setup-content');
allWells.hide();
navListItems.click(function (e) {
  e.preventDefault();
  var $target = $($(this).attr('href')), $item = $(this).closest('li');
  if (!$item.hasClass('disabled')) {
    navListItems.closest('li').removeClass('active');
    $item.addClass('active');
    allWells.hide();
    $target.show();
  }
});
$('ul.setup-panel li.active a').trigger('click');
$('#activate-step-2').on('click', function (e) {
  if (validate_firsttab()) {
    $('ul.setup-panel li:eq(1)').removeClass('disabled');
    $('ul.setup-panel li a[href="#step-2"]').trigger('click');
  }
});
$('#activate-step-3').on('click', function (e) {
  if (validate_secondtab()) {
    $('ul.setup-panel li:eq(2)').removeClass('disabled');
    $('ul.setup-panel li a[href="#step-3"]').trigger('click');
  }
});
$('#backward-step-1').on('click', function (e) {
  $('ul.setup-panel li:eq(1)').removeClass('disabled');
  $('ul.setup-panel li a[href="#step-1"]').trigger('click');
});
$('#backward-step-2').on('click', function (e) {
  $('ul.setup-panel li:eq(2)').removeClass('disabled');
  $('ul.setup-panel li a[href="#step-2"]').trigger('click');
});
$('#activate-step-finish').on('click', function (e) {
  if (validate_thirdtab()) {
    submitcompliance();
  }
});
//load available units for selected filter
function loadunit() {
  var assignStatutoryLegalEntityId = null;
  if ($('.legalentitylist.active').attr('id') != undefined)
    assignStatutoryLegalEntityId = parseInt($('.legalentitylist.active').attr('id'));
  var assignStatutoryDivisionId = null;
  if ($('.divisionlist.active').attr('id') != undefined)
    assignStatutoryDivisionId = parseInt($('.divisionlist.active').attr('id'));
  var assignStatutoryBusinessGroupId = null;
  if ($('.businessgrouplist.active').attr('id') != undefined)
    assignStatutoryBusinessGroupId = parseInt($('.businessgrouplist.active').attr('id'));
  var assignStatutoryCountryId = parseInt($('.countrylist.active').attr('id'));
  if (assignStatutoryLegalEntityId != null) {
    /*var str='<li id="0" class="unitlist" > Select All</li>';*/
    var str = '';
    $('#unit').empty();
    for (var unit in unitsList) {
      if (unitsList[unit].business_group_id == assignStatutoryBusinessGroupId && unitsList[unit].division_id == assignStatutoryDivisionId && unitsList[unit].legal_entity_id == assignStatutoryLegalEntityId && unitsList[unit].country_id == assignStatutoryCountryId) {
        str += '<li id="' + unitsList[unit].unit_id + '" class="unitlist" > <abbr class="page-load" title="' + unitsList[unit].address + '"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>' + unitsList[unit].unit_name + '</li>';
      }
    }
    $('#unit').append(str);
  }
}
$('#unit').click(function (event) {
  var chkstatus = $(event.target).attr('class');
  $('#activate-step-3').show();
  /*if($(event.target).attr('id') == 0){
        assignStatutoryUnitIds = [];
        $("#unit li").each( function( index, el ) {
          if(assignStatutoryUnitIds.length < 300){
            $(el).addClass("active");
            if(parseInt(el.id) != 0){
              assignStatutoryUnitIds.push(parseInt(el.id));
            }
          }
            //assignStatutoryUnitValues.push($(event.target).text());
        });
    }*/
  if (chkstatus != undefined && chkstatus != 'active') {
    clearValues('unit');
    if (chkstatus == 'unitlist active') {
      $(event.target).removeClass('active');
      var removeid = assignStatutoryUnitIds.indexOf(parseInt(event.target.id));
      assignStatutoryUnitIds.splice(removeid, 1);
      var removename = assignStatutoryUnitValues.indexOf($(event.target).text());
      assignStatutoryUnitValues.splice(removename, 1);
      displayMessage('');
    } else {
      if (assignStatutoryUnitIds.length < mUnit) {
        displayMessage('');
        $(event.target).addClass('active');
        assignStatutoryUnitIds.push(parseInt(event.target.id));
        assignStatutoryUnitValues.push($(event.target).text());
      } else {
        msg = 'Maximum(' + mUnit + ') ';
        displayMessage(msg + message.maximum_units);
      }
    }
    var domainArray = [];
    var applicableDomains = [];
    for (var unit in unitsList) {
      if ($.inArray(unitsList[unit].unit_id, assignStatutoryUnitIds) >= 0) {
        domainArray.push(unitsList[unit].domain_ids);
      }
    }
    if (domainArray.length > 0) {
      applicableDomains = domainArray.shift().filter(function (v) {
        return domainArray.every(function (a) {
          return a.indexOf(v) !== -1;
        });
      });
      var str = '';
      $('#domain').empty();
      for (domain in domainsList) {
        if (domainsList[domain].is_active == true && $.inArray(domainsList[domain].domain_id, applicableDomains) >= 0) {
          str += '<li id="' + domainsList[domain].domain_id + '" class="domainlist" >' + domainsList[domain].domain_name + '</li>';
        }
      }
      $('#domain').append(str);
    } else {
      $('#domain').empty();
    }
    $('ul.setup-panel li:eq(1)').addClass('disabled');
    $('ul.setup-panel li:eq(2)').addClass('disabled');
  }
});
$('#domain').click(function (event) {
  $('#activate-step-3').show();
  if ($(event.target).attr('class') == 'domainlist') {
    $('.' + $(event.target).attr('class')).each(function (index, el) {
      $(el).removeClass('active');
    });
    $(event.target).addClass('active');
  }
});
$('#businessgroup').click(function (event) {
  if ($(event.target).attr('class') == 'businessgrouplist') {
    clearValues('businessgroup');
    $('.' + $(event.target).attr('class')).each(function (index, el) {
      $(el).removeClass('active');
    });
    $(event.target).addClass('active');
    var str = '';
    var assignStatutoryBusinessGroupId = parseInt(event.target.id);
    $('#legalentity').empty();
    for (var legalentity in legalentitiesList) {
      if (legalentitiesList[legalentity].business_group_id == assignStatutoryBusinessGroupId) {
        str += '<li id="' + legalentitiesList[legalentity].legal_entity_id + '" class="legalentitylist" >' + legalentitiesList[legalentity].legal_entity_name + '</li>';
      }
    }
    $('#legalentity').append(str);
  }
});
$('#legalentity').click(function (event) {
  if ($(event.target).attr('class') == 'legalentitylist') {
    clearValues('legalentity');
    $('.' + $(event.target).attr('class')).each(function (index, el) {
      $(el).removeClass('active');
    });
    $(event.target).addClass('active');
    var str = '';
    var assignStatutoryLegalEntityId = parseInt(event.target.id);
    $('#division').empty();
    for (var division in divisionsList) {
      if (divisionsList[division].legal_entity_id == assignStatutoryLegalEntityId) {
        str += '<li id="' + divisionsList[division].division_id + '" class="divisionlist" >' + divisionsList[division].division_name + '</li>';
      }
    }
    $('#division').append(str);
    loadunit();
  }
});
$('#division').click(function (event) {
  if ($(event.target).attr('class') == 'divisionlist') {
    clearValues('division');
    $('.' + $(event.target).attr('class')).each(function (index, el) {
      $(el).removeClass('active');
    });
    $(event.target).addClass('active');
    loadunit();
  }
});
$('#country').click(function (event) {
  if ($(event.target).attr('class') != undefined) {
    if ($(event.target).attr('class') == 'countrylist') {
      clearValues('country');
      $('.' + $(event.target).attr('class')).each(function (index, el) {
        $(el).removeClass('active');
      });
      $(event.target).addClass('active');
    }
    var str = '';
    $('#businessgroup').empty();
    for (var businessgroup in businessgroupsList) {
      str += '<li id="' + businessgroupsList[businessgroup].business_group_id + '" class="businessgrouplist" >' + businessgroupsList[businessgroup].business_group_name + '</li>';
    }
    $('#businessgroup').append(str);
    var str1 = '';
    $('#legalentity').empty();
    for (var legalentity in legalentitiesList) {
      if (legalentitiesList[legalentity].business_group_id == null) {
        str1 += '<li id="' + legalentitiesList[legalentity].legal_entity_id + '" class="legalentitylist" >' + legalentitiesList[legalentity].legal_entity_name + '</li>';
      }
    }
    $('#legalentity').append(str1);
  }
});
function getUserLevel(selectedUserId) {
  var getuserLevel = null;
  for (var user in usersList) {
    var userId = usersList[user].user_id;
    if (userId == selectedUserId) {
      getuserLevel = usersList[user].user_level;
    }
  }
  return getuserLevel;
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
  var userLevel = null;
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
  }
  var str = '';
  var str1 = '';
  if (userType != 'concurrence' && selectedUnit != '') {
    if ((assigneeUserId == null || assigneeUserId != client_admin) && (approvalUserId == null || approvalUserId != client_admin) && (concurrenceUserId == null || concurrenceUserId != client_admin)) {
      /*if(temp_id == client_admin){
        str='<li id="'+client_admin+'" class="'+userClass+' active" > Admin </li>';
      }else{
        str='<li id="'+client_admin+'" class="'+userClass+'" > Admin </li>';
      }*/
      str1 = '<li id="' + client_admin + '-0' + '" class="' + userClass + '" > Client Admin </li>';
    }
  }
  for (var user in usersList) {
    var userUnits = usersList[user].unit_ids;
    var serviceProviderId = 0;
    if (usersList[user].service_provider_id != null) {
      serviceProviderId = usersList[user].service_provider_id;
    }
    //if( selectedUnit == 'all' || $.inArray(parseInt(selectedUnit), userUnits) >= 0){
    if (selectedUnit == 'all' || parseInt(selectedUnit) == usersList[user].seating_unit_id || serviceProviderId > 0) {
      var userId = usersList[user].user_id;
      var uLevel = usersList[user].user_level;
      var userName = usersList[user].user_name + ' - Level ' + uLevel;
      if (userId == client_admin) {
        userName = userName + ' (Client Admin)';
        str1 = '';
      }
      var combine = userId + '-' + serviceProviderId;
      var isAssignee = usersList[user].is_assignee;
      var isConcurrence = usersList[user].is_concurrence;
      var isApprover = usersList[user].is_approver;
      var userPermission;
      var promotedAdminFlag = true;
      if (userType == 'assignee') {
        userPermission = isAssignee;
      } else if (userType == 'concurrence') {
        userPermission = isConcurrence;
        if (userId == client_admin) {
          promotedAdminFlag = false;
        }
      } else if (userType == 'approval') {
        userPermission = isApprover;
      }
      if (userLevel != null) {
        if (userType == 'assignee') {
          conditionResult = uLevel >= userLevel;
        } else if (userType == 'concurrence') {
          conditionResult = uLevel <= userLevel;
        } else if (userType == 'approval') {
          conditionResult = uLevel <= userLevel;
        }
      }
      if (userType == 'concurrence' && userLevel1 != null) {
        conditionResult1 = uLevel >= userLevel1;
      }
      if (userPermission && conditionResult && conditionResult1 && (assigneeUserId == null || assigneeUserId != userId) && (approvalUserId == null || approvalUserId != userId) && (concurrenceUserId == null || concurrenceUserId != userId) && (serviceProviderId == 0 || sId == serviceProviderId || sId == 0) && promotedAdminFlag) {
        str += '<li id="' + combine + '" class="' + userClass + '" >' + userName + '</li>';
      }
    }
  }
  $('#' + userType).append(str1 + str);
}
$('#assignee').click(function (event) {
  var chkstatus = $(event.target).attr('class');
  if (chkstatus != undefined) {
    if (chkstatus == 'assigneelist active') {
      $(event.target).removeClass('active');
    } else {
      $('.assigneelist').each(function (index, el) {
        $(el).removeClass('active');
      });
      $(event.target).addClass('active');
    }
    var assigneeText = '';
    if ($('.assigneelist.active').attr('id') != undefined) {
      assigneeText = $('.assigneelist.active').attr('id').split('-')[0];
    }
    if (assigneeText != client_admin) {
      loadUser('concurrence');
      loadUser('approval');
    } else {
      $('#concurrence').empty();
      $('#approval').empty();
    }
  }
});
$('#concurrence').click(function (event) {
  var chkstatus = $(event.target).attr('class');
  if (chkstatus != undefined) {
    if (chkstatus == 'concurrencelist active') {
      $(event.target).removeClass('active');
    } else {
      $('.concurrencelist').each(function (index, el) {
        $(el).removeClass('active');
      });
      $(event.target).addClass('active');
    }
    //loadUser('assignee');
    loadUser('approval');
  }
});
$('#approval').click(function (event) {
  var chkstatus = $(event.target).attr('class');
  if (chkstatus != undefined) {
    if (chkstatus == 'approvallist active') {
      $(event.target).removeClass('active');
    } else {
      $('.approvallist').each(function (index, el) {
        $(el).removeClass('active');
      });
      $(event.target).addClass('active');
    }  //loadUser('assignee');
       //loadUser('concurrence');
  }
});
$('#assignee_unit').change(function () {
  loadUser('assignee');
});
$('#concurrence_unit').change(function () {
  loadUser('concurrence');
});
$('#approval_unit').change(function () {
  loadUser('approval');
});
//load master data in first wizard
function load_firstwizard() {
  $('#businessgroup').empty();
  $('#legalentity').empty();
  $('#division').empty();
  $('#unit').empty();
  $('#domain').empty();
  var str = '';
  $('#country').empty();
  for (var country in countriesList) {
    if (countriesList[country].is_active == true) {
      str += '<li id="' + countriesList[country].country_id + '" class="countrylist">' + countriesList[country].country_name + '</li>';
    }
  }
  $('#country').append(str);
  for (var user in usersList) {
    var sId = usersList[user].seating_unit_id;
    var sName = usersList[user].seating_unit_name;
    if (sId != null)
      seatingunitsList[sId] = sName;
  }
  $('#assignee_unit').empty();
  $('#assignee_unit').append('<option value=""> Select </option>');
  $('#assignee_unit').append('<option value="all"> All </option>');
  $.each(seatingunitsList, function (key, value) {
    var option = $('<option></option>');
    option.val(key);
    option.text(value);
    $('#assignee_unit').append(option);
  });
  $('#concurrence_unit').empty();
  $('#concurrence_unit').append('<option value=""> Select </option>');
  $('#concurrence_unit').append('<option value="all"> All </option>');
  $.each(seatingunitsList, function (key, value) {
    var option = $('<option></option>');
    option.val(key);
    option.text(value);
    $('#concurrence_unit').append(option);
  });
  $('#approval_unit').empty();
  $('#approval_unit').append('<option value=""> Select </option>');
  $('#approval_unit').append('<option value="all"> All </option>');
  $.each(seatingunitsList, function (key, value) {
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
//get assign compliance master data from api
function getAssignCompliances() {
  function onSuccess(data) {
    countriesList = data.countries;
    businessgroupsList = data.business_groups;
    legalentitiesList = data.legal_entities;
    divisionsList = data.divisions;
    unitsList = data.units;
    usersList = data.users;
    two_level_approve = data.two_level_approve;
    client_admin = data.client_admin;
    domainsList = data.domains;
    load_firstwizard();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  client_mirror.getAssignComplianceFormData(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
//initialization and UL filter process
$(document).ready(function () {
  getAssignCompliances();
  $('#filter_assignee').keyup(function () {
    var filter = $('#filter_assignee').val().toLowerCase();
    var lis = document.getElementsByClassName('assigneelist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });
  $('#filter_concurrence').keyup(function () {
    var filter = $('#filter_concurrence').val().toLowerCase();
    var lis = document.getElementsByClassName('concurrencelist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });
  $('#filter_approval').keyup(function () {
    var filter = $('#filter_approval').val().toLowerCase();
    var lis = document.getElementsByClassName('approvallist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });
  $('.edittrigger').click(function () {
    $('.edittriggertextbox').show();
    $('.edittrigger').hide();
    $('.closetrigger').show();
  });
  $('.closetrigger').click(function () {
    $('.edittriggertextbox').hide();
    $('.edittrigger').show();
    $('.closetrigger').hide();
  });
  $('#filter_country').keyup(function () {
    var filter = $('#filter_country').val().toLowerCase();
    var lis = document.getElementsByClassName('countrylist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });
  $('#filter_businessgroup').keyup(function () {
    var filter = $('#filter_businessgroup').val().toLowerCase();
    var lis = document.getElementsByClassName('businessgrouplist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });
  $('#filter_legalentity').keyup(function () {
    var filter = $('#filter_legalentity').val().toLowerCase();
    var lis = document.getElementsByClassName('legalentitylist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });
  $('#filter_division').keyup(function () {
    var filter = $('#filter_division').val().toLowerCase();
    var lis = document.getElementsByClassName('divisionlist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });
  $('#filter_unit').keyup(function () {
    var filter = $('#filter_unit').val().toLowerCase();
    var lis = document.getElementsByClassName('unitlist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });
  $('#filter_domain').keyup(function () {
    var filter = $('#filter_domain').val().toLowerCase();
    var lis = document.getElementsByClassName('domainlist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });
});
$(document).tooltip({
  position: {
    my: 'center bottom-20',
    at: 'center top',
    using: function (position, feedback) {
      $(this).css(position);
      $('<div>').addClass('arrow').addClass(feedback.vertical).addClass(feedback.horizontal).appendTo(this);
    }
  }
});