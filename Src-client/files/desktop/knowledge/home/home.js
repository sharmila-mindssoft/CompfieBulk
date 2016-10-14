function initialize() {
  function onSuccess(data) {
    loadNotificationList(data.notifications);
  }
  function onFailure(error) {
    displayMessage(error);
  }
  $('.notification-container').hide();
  if (mirror.getUserId() > 0) {
    mirror.getNotifications('Notification', function (error, response) {
      if (error == null) {
        onSuccess(response);
      } else {
        onFailure(error);
      }
    });
  }
}
function loadNotificationList(list) {
  $('.notification-container').show();
  $('.notification-ul').find('li').remove();
  var notificationtext;
  var notificationtime;
  if (list.length == 0) {
    $('.notification-container').hide();
  } else {
    $.each(list, function (k, value) {
      notificationtext = list[k].notification_text;
      notificationtime = list[k].date_and_time;
      var tableRow = $('#templates .list');
      var clone = tableRow.clone();
      $('.notification-text', clone).text(notificationtext);
      $('.notification-time', clone).text(notificationtime);
      $('.notification-container .notification-ul').append(clone);
    });
  }
}
$(function () {
  // initialize();
  $('.notification-container').hide();
});
function initializeUI() {
  var windowHeight = $(window).height();
  var boxHeight = $('.welcome-msg').outerHeight();
  var getEmptySpace = windowHeight - boxHeight;
  var contentAreaTop = parseInt($('.content-area').css('padding-top'));
  var navBarHeight = $('.header-section').outerHeight();
  var marginTop = getEmptySpace / 2 - navBarHeight - contentAreaTop;
  $('.welcome-msg').css('margin-top', marginTop);
}
$(document).ready(function () {
  if (!mirror.verifyLoggedIn())
    return;
  var user = mirror.getUserProfile();
  $('.welcome-msg').text('Welcome ' + user.employee_name + '!');
  initializeUI();
});
$(window).resize(initializeUI);