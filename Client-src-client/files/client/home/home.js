
$(document).ready(function () {
  if (!client_mirror.verifyLoggedIn())
    return;
  var user = client_mirror.getUserInfo();
  console.log(user)
  $('.page-title').text('Welcome ' + user.emp_name + '!');
});
