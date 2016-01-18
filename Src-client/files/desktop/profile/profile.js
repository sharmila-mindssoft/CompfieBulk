function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}
function initialize(){
	var userprofile = mirror.getUserProfile();
	var contactNo = (userprofile['contact_no']).split('-');
	$('.employee-name').text(userprofile['employee_name']);
	$('.designation').text(userprofile['designation']);
	$('.email-id').text(userprofile['email_id']);
	$('.countrycode').val(contactNo[0]);
	$('.areacode').val(contactNo[1]);
	$('.mobile').val(contactNo[2]);
	$('.employee-id').text(userprofile['employee_code']);
	$('.usergroup').text(userprofile['user_group']);
	$('textarea.address').text(userprofile['address']);	
	$('.userid').val(userprofile['user_id']);
}
$(function() {
	initialize();
});

