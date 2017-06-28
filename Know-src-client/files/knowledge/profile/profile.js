var EmployeeName = $('.employee-name');
var Designation = $('.designation');
var EmailId = $('.email-id');
var CountryCode = $('.countrycode');
var AreaCode = $('.areacode');
var ContactNo = $('.contactno');
var MCountryCode = $('.mcountrycode');
var MobileNo = $('.mobileno');
var EmployeeId = $('.employee-id');
var UserId = $('.user-id');
var UserGroup = $('.user-group');
var Address = $('.address');
var SubmitBtn = $('#submit');

function initialize() {
    displayLoader();
    var userprofile = mirror.getUserProfile();
    EmployeeName.text(userprofile.employee_name);
    
    if (userprofile.designation != null) {
        Designation.text(userprofile.designation);
    }

    EmailId.val(userprofile.email_id);

    if (userprofile.contact_no != null) {
        var cNo = userprofile.contact_no.split('-');
        CountryCode.val(cNo[0]);
        AreaCode.val(cNo[1]);
        ContactNo.val(cNo[2]);
    }

    if (userprofile.mobile_no != null) {
        var mNo = userprofile.mobile_no.split('-');
        MCountryCode.val(mNo[0]);
        MobileNo.val(mNo[1]);
    }

    EmployeeId.text(userprofile.employee_code);

    UserId.text(userprofile.user_name);

    UserGroup.text(userprofile.user_group);

    if (userprofile.address != null) {
        Address.val(userprofile.address);
    }
    hideLoader();
}


function pageControls() {

    Address.on('input', function(e) {
        this.value = isCommon_Address($(this));
    });
    ContactNo.on('input', function(e) {
        //this.value = isNumbers($(this));
        isNumbers(this);
    });
    AreaCode.on('input', function(e) {
        //this.value = isNumbers($(this));
        isNumbers(this);
    });
    CountryCode.on('input', function(e) {
        //this.value = isNumbers_Countrycode($(this));
        isNumbers_Countrycode(this);
    });
    MCountryCode.on('input', function(e) {
        //this.value = isNumbers_Countrycode($(this));
        isNumbers_Countrycode(this);
    });
    MobileNo.on('input', function(e) {
        //this.value = isNumbers($(this));
        isNumbers(this);
    });

    SubmitBtn.click(function() {
        if (EmailId.val().trim().length == 0) {
            displayMessage(message.emailid_required);
            EmailId.focus();
            return false;
        }
        else if (validateMaxLength("email_id", EmailId.val().trim(), "Email id") == false) {
            return false;
        }
        else if(!validateEmail(EmailId.val())){
            displayMessage(message.invalid_emailid);
            EmailId.focus();
            return false;
        }
        else if (validateMaxLength("countrycode", CountryCode.val().trim(), "Country code") == false) {
            return false;
        }
        else if (validateMaxLength("areacode", AreaCode.val().trim(), "Area code") == false) {
            return false;
        }
        else if (validateMaxLength("contactno", ContactNo.val().trim(), "Contact number") == false) {
            return false;
        }
        else if (MobileNo.val().trim().length == 0) {
            displayMessage(message.mobile_required);
            MobileNo.focus();
            return false;
        }
        else if (MobileNo.val().trim().length < 10) {
            displayMessage(message.mobile_length);
            MobileNo.focus();
            return false;
        }
        else if(validateMaxLength("countrycode", MCountryCode.val().trim(), "Mobile Country code") == false) {
            return false;
        }
        else if(validateMaxLength("mobileno", MobileNo.val().trim(), "Mobile number") == false) {
            return false;
        }
        else if (validateMaxLength("address", Address.val().trim(), "Address") == false) {
            return false;
        }else{
            displayLoader();
            var countrycode_ = CountryCode.val().trim();
            var areacode_ = AreaCode.val().trim();
            var contactno_ = ContactNo.val().trim();
            var address_ = Address.val().trim();

            var emailid_ = EmailId.val().trim();
            var mcountrycode_ = MCountryCode.val().trim();
            var mobileno_ = MobileNo.val().trim();

            path = window.location.pathname;
            if (path == '/knowledge/profile') {
                function onSuccess(data) {
                    initialize();
                    displaySuccessMessage(message.updated_success);
                }

                function onFailure(error) {
                    displayMessage(error);
                    hideLoader();
                }
                mirror.updateUserProfile(countrycode_ + '-' + areacode_ + '-' + contactno_, address_, mcountrycode_ + '-' + mobileno_, emailid_, function(error, response) {
                    if (error == null) {
                        onSuccess(response);
                    } else {
                        onFailure(error);
                    }
                });
            }
        }

    });

}

$(function() {
    initialize();
    pageControls();
});
