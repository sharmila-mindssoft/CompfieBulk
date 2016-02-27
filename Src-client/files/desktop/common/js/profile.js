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
	clearMessage();
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
$("#submit").click(function(){
	var countrycode = $(".countrycode").val();
	var areacode = $(".areacode").val();
	var mobile = $(".mobile").val();
	var address = $(".address").val();
	if(countrycode == ''){
		displayMessage("Enter country code");
	}
	if(mobile == ''){
		displayMessage("Enter Contact Number");
	}
	if(isNaN(mobile)){
		displayMessage("Contact Number Invalid");
	}
	if(address == ''){
		displayMessage("Enter address")
	}
	function onSuccess(data){
		initialize();
		displayMessage("Updated Successfully");
	}
	function onFailure(error){
		console.log(error);
	}
	mirror.updateUserProfile( countrycode+"-"+areacode+"-"+mobile, address,
	    	function(error, response){
	            if(error == null){
	                onSuccess(response);
	            }
	            else{
	                onFailure(error);
	            }
	        }
	    );
});

$(function() {
	initialize();
});

