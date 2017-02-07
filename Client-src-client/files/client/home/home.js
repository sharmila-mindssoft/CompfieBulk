
$(document).ready(function () {
  if (!client_mirror.verifyLoggedIn())
    return;
  var user = client_mirror.getUserProfile();
  console.log(user)
  $('.page-title').text('Welcome ' + user.email_id + '!');
});
