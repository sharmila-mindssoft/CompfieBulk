var userDetails;

// Controls Initialized
var employeeName = $('.emp-name');
var shortName = $('.short-name');
var emailId = $('#user_email_id');

var c_intnlCode = $('#c_intl_code');
var c_localCode = $('#c_local_code');
var contactNo = $('#contact_no');

var m_intnlCode = $('#m_intl_code');
var mobileNo = $('#mobile_no');

var employeeCode = $('.emp-code');
var userName = $('.user-name');
var userGroup = $('.user-group');
var Address = $('.address');

var SubmitAction = $('#btn_submit');
var PasswordAction = $('#btn_chg_pwd');

var userId = null;

// Get User Details
function initialize(){
	function onSuccess(data) {
        userDetails = data.user_profile;
        loadUserDetails();
    }

    function onFailure(error) {
        displayMessage(error);
    }
    client_mirror.getUserProfile(function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

//bind the user details
function loadUserDetails(){
	if (userDetails.length > 0)
	{
		userId = userDetails[0].user_id;
		userName.text(userDetails[0].user_name);
		employeeCode.text(userDetails[0].emp_code);
		employeeName.text(userDetails[0].emp_name);
		shortName.text(userDetails[0].short_name);
		emailId.val(userDetails[0].email_id);
		c_no = userDetails[0].con_no;
		if (c_no.indexOf("-") >= 0){
			c_intnlCode.val(c_no.split("-")[0].trim());
			c_localCode.val(c_no.split("-")[1].trim());
			contactNo.val(c_no.split("-")[2].trim());
		}
		else{
			contactNo.val(c_no);
		}

		m_no = userDetails[0].mob_no;
		if (m_no.indexOf("-") >= 0){
			m_intnlCode.val(m_no.split("-")[0].trim());
			mobileNo.val(m_no.split("-")[1].trim());
		}

		userGroup.text(userDetails[0].u_g_name);
		Address.text(userDetails[0].address);
	}
}

//submit/update user details
SubmitAction.click(function() {
	if (ValidateRequest() == true){
		c_no = c_intnlCode.val().trim()+'-'+c_localCode.val().trim()+'-'+contactNo.val().trim();
		m_no = m_intnlCode.val().trim()+'-'+mobileNo.val().trim();
		function onSuccess(data) {
			displaySuccessMessage(message.update_success);
	    }

	    function onFailure(error) {
	        displayMessage(error);
	    }
	    client_mirror.updateUserProfile(userId, emailId.val(), c_no, m_no, Address.val().trim(), function(error, response) {
	        if (error == null) {
	            onSuccess(response);
	        } else {
	            onFailure(error);
	        }
	    });
	}
	else{
		displayMessage("Invalid Request");
	}
}

//Validation
function ValidateRequest(){
	var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
	if (userId != null){
		displayMessage(message.invalid_userid);
		return false;
	}
	else if (emailId.val() == "" || emailId.val().length == 0){
		displayMessage(message.emailid_required);
		emailId.focus();
		return false;
	}
	else if (emailId.val().length > 50){
		displayMessage(message.email_50);
		emailId.focus();
		return false;
	}
	else if (reg.test(emailId.val().trim()) == false){
        displayMessage(message.invalid_emailid);
        emailId.focus();
        return false;
	}
	else if (c_intnlCode.val() == ""){
		displayMessage("Contact No. International Code Required");
		c_intnlCode.focus();
		return false;
	}
	else if (c_intnlCode.val().length > 4){
		displayMessage(message.countrycode_max4);
		c_intnlCode.focus();
		return false;
	}
	else if (c_localCode.val() == ""){
		displayMessage("Contact No. Local Code Required");
		c_localCode.focus();
		return false;
	}
	else if (c_localCode.val().length > 4){
		displayMessage(message.areacode_max4);
		c_localCode.focus();
		return false;
	}
	else if (contactNo.val() == ""){
		displayMessage("Contact No. Required");
		contactNo.focus();
		return false;
	}
	else if (contactNo.val().length > 10){
		displayMessage(message.contactno_max10);
		contactNo.focus();
		return false;
	}
	else{
		return true;
	}
}

//initialize form
$(document).ready(function() {
    initialize();

    c_localCode.on('input', function(e) {
        this.value = isNumbers($(this));
    });
    c_intnlCode.on('input', function(e) {
        this.value = isNumbers_Countrycode($(this));
    });
    contactNo.on('input', function(e) {
        this.value = isNumbers($(this));
    });
    m_intnlCode.on('input', function(e) {
        this.value = isNumbers_Countrycode($(this));
    });
    mobileNo.on('input', function(e) {
        this.value = isNumbers($(this));
    });
    Address.on('input', function(e) {
        this.value = isCommon_Address($(this));
    });
});
