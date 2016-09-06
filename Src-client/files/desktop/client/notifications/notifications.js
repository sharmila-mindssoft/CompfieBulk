var notificationsList;
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
function loadNotifications(notifications) {
  var str = '';
  $.each(notifications, function (key, value) {
    sno++;
    var readStatus = 'unread';
    var notificationId = notifications[key].notification_id;
    var notificationText = notifications[key].notification_text;
    var extraDetails = notifications[key].extra_details;
    var updatedon = notifications[key].updated_on;
    var act = notifications[key].level_1_statutory;
    var unit = notifications[key].unit_name;
    var unitaddress = notifications[key].unit_address;
    var compliance = notifications[key].compliance_name;
    var duedate = notifications[key].due_date;
    var delayedby = notifications[key].delayed_days;
    var assignee = notifications[key].assignee;
    var concurrence = notifications[key].concurrence_person;
    var approval = notifications[key].approval_person;
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
    if (notifications[key].read_status) {
      readStatus = '';
    }
    if (assignee != null) {
      str += '<li id="notification' + notificationId + '" class="' + readStatus + '" onclick="changeStatus(' + notificationId + ',' + notifications[key].read_status + ')"> ' + notificationText + '<p class="subtext"><span class="time">' + updatedon + '</span><span class="notification-cat">Category: ' + extraDetails + '</span></p> </li>';
    } else {
      str += '<li id="notification' + notificationId + '" class="' + readStatus + '" onclick="changeStatus(' + notificationId + ',' + notifications[key].read_status + ')"> ' + notificationText + '<p class="subtext"><span class="time">' + updatedon + '</span><span class="notification-cat">Category: ' + extraDetails + '</span></p> </li>';
    }
  });
  if (str == '' && sno == 0) {
    str += '<li style="text-align:center">' + 'No Notification Found' + '</li>';
  }
  $('#notificationsList').append(str);
  if (window.sessionStorage.CLIENT_NOTIFICATION_COUNT > sno) {
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
    var approvalName;
    var approvalDetails;
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
    client_mirror.updateNotificationStatus(parseInt(notification_id), true, function (error, response) {
      if (error == null) {
        get_notification_count();
      } else {
        displayMessage(error);
      }
    });
  }
}
function get_notifications(sno) {
  displayLoader();
  function onSuccess(data) {
    notificationsList = data.notifications;
    loadNotifications(notificationsList);
    hideLoader();
  }
  function onFailure(error) {
    displayMessage(error);
    hideLoader();
  }
  client_mirror.getNotifications('Notification', sno, function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
$('#pagination').click(function () {
  get_notifications(sno);
});
function initialize() {
  sno = 0;
  notificationDict = [];
  $('#notificationsList').empty();
  get_notifications(sno);  /*setInterval(function() {
        get_notifications(sno);
    }, 10000);*/
}
$(function () {
  get_notification_count();
  initialize();
});