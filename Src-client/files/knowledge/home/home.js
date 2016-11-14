
$(document).ready(function () {
  if (!mirror.verifyLoggedIn())
    return;
  var user = mirror.getUserProfile();
  $('.page-title').text('Welcome ' + user.employee_name + '!');
});
