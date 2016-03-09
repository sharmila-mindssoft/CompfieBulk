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
$('.countrycode').on('input', function (event) {   
    this.value = this.value.replace(/[^0-9]/g, '');
});
$('.areacode').on('input', function (event) {
    this.value = this.value.replace(/[^0-9]/g, '');
});
$('.mobile').on('input', function (event) {
    this.value = this.value.replace(/[^0-9]/g, '');
});
$("#submit").click(function(){
	var countrycode = $(".countrycode").val().trim();
	var areacode = $(".areacode").val().trim();
	var mobile = $(".mobile").val().trim();
	var address = $(".address").val().trim();
	if(countrycode == ''){
		displayMessage("Enter country code");
	}
	else if(mobile == ''){
		displayMessage("Enter Contact Number");
	}
	else if(isNaN(mobile)){
		displayMessage("Contact Number Invalid");
	}
	else if(address == ''){
		displayMessage("Enter address")
	}
	else{
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
	}
});

$(function() {
	initialize();
});

