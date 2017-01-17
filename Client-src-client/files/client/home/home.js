
$(document).ready(function () {
  if (!client_mirror.verifyLoggedIn())
    return;
	console.log(client_mirror.getUserProfile())
  var user = client_mirror.getUserProfile();
  $('.page-title').text('Welcome ' + user.email_id + '!');
});
