var userList;
var logintraceList;
var sno = 0;
var userid = null;
var fromdate = null;
var todate = null;
function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
function clearMessage() {
  $('.error-message').hide();
  $('.error-message').text('');
}
function displayMessage(message) {
  $('.error-message').text(message);
  $('.error-message').show();
}
function datetonumber(datetime) {
  var date = datetime.substring(0, 11);
  var timeval = datetime.substring(12, 18);
  var date1 = date.split('-');
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
    if (date1[1] == months[j]) {
      date1[1] = months.indexOf(months[j]) + 1;
    }
  }
  if (date1[1] < 10) {
    date1[1] = '0' + date1[1];
  }
  var formattedDate = date1[2] + '/' + date1[1] + '/' + date1[0];
  var newdate = new Date(formattedDate + ' ' + timeval);
  return Date.parse(newdate);
}
function initialize() {
  var m_names = new Array('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec');
  var d = new Date();
  var curr_date = d.getDate();
  var curr_month = d.getMonth();
  var curr_year = d.getFullYear();
  if (curr_date < 10) {
    curr_date = '0' + curr_date;
  }
  var todaydate = curr_date + '-' + m_names[curr_month] + '-' + curr_year;
  var currentDate = new Date(new Date().getTime() - 24 * 60 * 60 * 1000 * 7);
  var day = currentDate.getDate();
  var month = currentDate.getMonth();
  var year = currentDate.getFullYear();
  if (day < 10) {
    day = '0' + day;
  }
  var lastdate = day + '-' + m_names[month] + '-' + year;
  $('#to-date').val(todaydate);
  $('#from-date').val(lastdate);
  $('#userval').focus();
  fromdate = todaydate;
  todate = lastdate;
  if ($('#userid').val() == '') {
    var userid = null;
  } else {
    var userid = $('userid').val();
  }
  $('.grid-table').show();
  $('.tbody-login-trace-list tr').remove();
  $('#pagination').show();
  apipass(sno, userid, lastdate, todaydate);
}
//pagination process
$('#pagination').click(function () {
  displayLoader();
  s_endCount = sno;
  clearMessage();
  function onSuccess(data) {
    if (data.login_trace == '') {
      $('#pagination').hide();
    }
    loadrecords(data.login_trace);
    hideLoader();
  }
  function onFailure(error) {
    displayMessage(error);
    hideLoader();
  }
  client_mirror.getLoginTrace(sno, parseInt(userid), fromdate, todate, function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
});
function showrecord() {
  userid = $('#userid').val();
  fromdate = $('#from-date').val();
  todate = $('#to-date').val();
  if (userid == '') {
    userid = null;
  }
  if (fromdate == '') {
    displayMessage(message.fromdate_required);
  } else if (todate == '') {
    displayMessage(message.todate_required);
  } else {
    $('.grid-table').show();
    $('.tbody-login-trace-list tr').remove();
    //loadrecords(logintraceList); 
    sno = 0;
    $('#pagination').show();
    apipass(sno, userid, fromdate, todate);
  }
}
function apipass(sno, userid, lastdate, todaydate) {
  function onSuccess(data) {
    if (data.login_trace != '') {
      userList = data.users;
      logintraceList = data.login_trace;
      loadrecords(logintraceList);
      $('.total-records').html('Total : ' + sno + ' records');
    } else {
      $('#pagination').hide();
      console.log(sno);
      if (sno == 0) {
        $('.tbody-login-trace-list').html('<tr><td colspan=\'4\' align=\'center\'>No record found.</td></tr>');
      }
    }
  }
  function onFailure(error) {
    displayMessage(error);
  }
  client_mirror.getLoginTrace(sno, parseInt(userid), lastdate, todaydate, function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
function loadrecords(logintraceList) {
  if (logintraceList == '') {
    $('#pagination').hide();
  }
  $.each(logintraceList, function (key, value) {
    var formname;
    if (value.action.substring(0, 6) == 'Log In') {
      formname = 'Login';
    } else {
      formname = 'Logout';
    }
    var tableRow = $('#templates .table-logintrace-list .table-row');
    var clone = tableRow.clone();
    $('.date-time', clone).text(value.created_on);
    $('.form-name', clone).text(formname);
    $('.info-text', clone).text(value.action);
    $('.tbody-login-trace-list').append(clone);
    sno++;
  });
}
//retrive user autocomplete value
function onUserSuccess(val) {
  $('#userval').val(val[1]);
  $('#userid').val(val[0]);
}
//load user list in autocomplete text box  
$('#userval').keyup(function (e) {
  var textval = $(this).val();
  getUserAutocomplete(e, textval, userList, function (val) {
    onUserSuccess(val);
  });
});
$(function () {
  initialize();
});