var remindersList;
var sno = 0;
var notificationDict = [];
function clearMessage() {
  $('.error-message').hide();
  $('.error-message').text('');
}
function displayMessage(message) {
  $('.error-message').text(message);
  $('.error-message').show();
}
function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
function loadReminders(reminders) {
  var str = '';
  for (var reminder in reminders) {
    sno++;
    var readStatus = 'unread';
    var notificationId = reminders[reminder].notification_id;
    var notificationText = reminders[reminder].notification_text;
    var act = reminders[reminder].level_1_statutory;
    var unit = reminders[reminder].unit_name;
    var unitaddress = reminders[reminder].unit_address;
    var compliance = reminders[reminder].compliance_name;
    var duedate = reminders[reminder].due_date;
    var delayedby = reminders[reminder].delayed_days;
    var assignee = reminders[reminder].assignee;
    var concurrence = reminders[reminder].concurrence_person;
    var approval = reminders[reminder].approval_person;
    notificationDict[notificationId] = [
      act,
      unit,
      unitaddress,
      compliance,
      duedate,
      delayedby,
      assignee,
      concurrence,
      approval
    ];
    if (reminders[reminder].assignee != null) {
      var assignee1 = reminders[reminder].assignee;
      var assigneesplit = assignee1.split(',');
    }
    if (reminders[reminder].read_status) {
      readStatus = '';
    }
    if (assignee != null) {
      str += '<li class="' + readStatus + '" id="notification' + notificationId + '" onclick="changeStatus(' + notificationId + ',' + reminders[reminder].read_status + ')">' + notificationText + '<span style=\'font-weight:bold\'>' + assigneesplit[0] + '</span> </li>';
    } else {
      str += '<li class="' + readStatus + '" id="notification' + notificationId + '" onclick="changeStatus(' + notificationId + ',' + reminders[reminder].read_status + ')">' + notificationText;
    }
  }
  if (str == '' && sno == 0) {
    str += '<li style="text-align:center">' + 'No Reminders Found' + '</li>';
  }
  $('#reminderList').append(str);
  if (window.sessionStorage.CLIENT_REMINDER_COUNT > sno) {
    $('#pagination').show();
  } else {
    $('#pagination').hide();
  }
}
$('.close').click(function () {
  $('.overlay').css('visibility', 'hidden');
  $('.overlay').css('opacity', '0');
});
function changeStatus(notification_id, read_status) {
  $('.overlay').css('visibility', 'visible');
  $('.overlay').css('opacity', '1');
  $('#notification' + notification_id).removeClass('unread');
  if (notificationDict[notification_id][6] != null) {
    $('#popup1').show();
    var act = notificationDict[notification_id][0];
    var unit = notificationDict[notification_id][1];
    var unitaddress = notificationDict[notification_id][2];
    var compliance = notificationDict[notification_id][3];
    var duedate = notificationDict[notification_id][4];
    var delayedby = notificationDict[notification_id][5];
    var assignee = notificationDict[notification_id][6];
    var concurrence = notificationDict[notification_id][7];
    var approval = notificationDict[notification_id][8];
    var assigneeName;
    var assigneeDetails;
    var concurrenceName;
    var concurrenceDetails;
    var assigneeName;
    var assigneeDetails;
    if (assignee != '') {
      assigneeName = assignee.split(',')[0];
      assigneeDetails = assignee.substring(assignee.indexOf(',') + 1).trim().replace(/--, /gi, '');
    }
    if (concurrence != '' && concurrence != null) {
      concurrenceName = concurrence.split(',')[0];
      concurrenceDetails = concurrence.substring(concurrence.indexOf(',') + 1).trim().replace(/--, /gi, '');
    } else {
      concurrenceName = '-';
      concurrenceDetails = '-';
    }
    if (approval != '') {
      approvalName = approval.split(',')[0];
      approvalDetails = approval.substring(approval.indexOf(',') + 1).trim().replace(/--, /gi, '');
    }
    $('.popup_act').text(act);
    $('.popup_unit').html('<abbr class="page-load tipso_style" title="' + unitaddress + '"></abbr>' + unit);
    $('.popup_compliance').text(compliance);
    $('.popup_duedate').text(duedate);
    $('.popup_delayedby').text(delayedby);
    $('.popup_assignee').html(assigneeName + '<br>' + assigneeDetails);
    $('.popup_concurrence').html(concurrenceName + '<br>' + concurrenceDetails);
    $('.popup_approval').html(approvalName + '<br>' + approvalDetails);
  }
  if (read_status == false) {
    function onSuccess(response) {
      get_notification_count();
    }
    function onFailure(error) {
      displayMessage(error);
    }
    client_mirror.updateNotificationStatus(parseInt(notification_id), true, function (error, response) {
      if (error == null) {
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
  }
}
function get_reminders(sno) {
  displayLoader();
  function onSuccess(data) {
    remindersList = data.notifications;
    loadReminders(remindersList);
    hideLoader();
  }
  function onFailure(error) {
    displayMessage(error);
    hideLoader();
  }
  client_mirror.getNotifications('Reminder', sno, function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
$('#pagination').click(function () {
  get_reminders(sno);
});
function initialize() {
  sno = 0;
  notificationDict = [];
  $('#reminderList').empty();
  get_reminders(sno);  /*setInterval(function() {
      get_reminders();
  }, 10000);*/
}
$(function () {
  get_notification_count();
  initialize();
});