
var max3 = 3;
var max4 = 4;
var max5 = 5;
var max10 = 10;
var max20 = 20;
var max30 = 30;
var max50 = 50;
var max100 = 100;
var max250 = 250;
var max500 = 500;

function countryValidate(){
	if($("#country-name").val().trim().length > max50){
		displayMessage("Country Name" + message.should_not_exceed + max50 + " characters");
		return false;
	}else{
		displayMessage();
		return true;
	}
}

function domainValidate(){
	if($("#domainname").val().trim().length > max50){
		displayMessage("Domain Name" + message.should_not_exceed + max50 + " characters");
		return false;
	}else{
		displayMessage();
		return true;
	}
}

function industryValidate(){
	if($("#industryname").val().trim().length > max50){
		displayMessage("Industry Name" + message.should_not_exceed + max50 + " characters");
		return false;
	}else{
		displayMessage();
		return true;
	}
}

function userGroupValidate(){
	if($("#groupName").val().trim().length > max50){
		displayMessage("Group Name" + message.should_not_exceed + max50 + " characters");
		return false;
	}else{
		displayMessage();
		return true;
	}
}

function userValidate(){
	if($("#employeename").val().trim().length > max50){
		displayMessage("Employee Name" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#employeeid").val().trim().length > max50){
		displayMessage("Employee Id" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#address").val().trim().length > max250){
		displayMessage("Address" + message.should_not_exceed + max250 + " characters");
		return false;
	}
	else if($("#emailid").val().trim().length > max100){
		displayMessage("Email Id" + message.should_not_exceed + max100 + " characters");
		return false;
	}
	else if($("#countrycode").val().trim().length > max3){
		displayMessage("Country Code" + message.should_not_exceed + max3 + " characters");
		return false;
	}
	else if($("#areacode").val().trim().length > max5){
		displayMessage("Area Code" + message.should_not_exceed + max5 + " characters");
		return false;
	}
	else if($("#contactno").val().trim().length > max10){
		displayMessage("Contact No" + message.should_not_exceed + max10 + " characters");
		return false;
	}
	else if($("#designation").val().trim().length > max50){
		displayMessage("Designation" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else{
		displayMessage();
		return true;
	}
}

function changePasswordValidate(){
	if($("#currentpassword").val().trim().length > max20){
		displayMessage("Current Password" + message.should_not_exceed + max20 + " characters");
		return false;
	}
	else if($("#newpassword").val().trim().length > max20){
		displayMessage("New Password" + message.should_not_exceed + max20 + " characters");
		return false;
	}
	else if($("#confirmpassword").val().trim().length > max20){
		displayMessage("Confirm Password" + message.should_not_exceed + max20 + " characters");
		return false;
	}
	else{
		displayMessage();
		return true;
	}
}

function resetPasswordValidate(){
	if($("#newpassword").val().trim().length > max20){
		displayMessage("New Password" + message.should_not_exceed + max20 + " characters");
		return false;
	}
	else if($("#confirmpassword").val().trim().length > max20){
		displayMessage("Confirm Password" + message.should_not_exceed + max20 + " characters");
		return false;
	}
	else{
		displayMessage();
		return true;
	}
}

function geographyLevelValidate(){
	if($("#insertvalue").val().trim().length > max30){
		displayMessage("Insert Level Value" + message.should_not_exceed + max20 + " characters");
		return false;
	}
	else if($("#level1").val().trim().length > max30){
		displayMessage("Level 1" + message.should_not_exceed + max30 + " characters");
		return false;
	}
	else if($("#level2").val().trim().length > max30){
		displayMessage("Level 2" + message.should_not_exceed + max30 + " characters");
		return false;
	}
	else if($("#level3").val().trim().length > max30){
		displayMessage("Level 3" + message.should_not_exceed + max30 + " characters");
		return false;
	}
	else if($("#level4").val().trim().length > max30){
		displayMessage("Level 4" + message.should_not_exceed + max30 + " characters");
		return false;
	}
	else if($("#level5").val().trim().length > max30){
		displayMessage("Level 5" + message.should_not_exceed + max30 + " characters");
		return false;
	}
	else if($("#level6").val().trim().length > max30){
		displayMessage("Level 6" + message.should_not_exceed + max30 + " characters");
		return false;
	}
	else if($("#level7").val().trim().length > max30){
		displayMessage("Level 7" + message.should_not_exceed + max30 + " characters");
		return false;
	}
	else if($("#level8").val().trim().length > max30){
		displayMessage("Level 8" + message.should_not_exceed + max30 + " characters");
		return false;
	}
	else if($("#level9").val().trim().length > max30){
		displayMessage("Level 9" + message.should_not_exceed + max30 + " characters");
		return false;
	}
	else if($("#level10").val().trim().length > max30){
		displayMessage("Level 10" + message.should_not_exceed + max30 + " characters");
		return false;
	}
	else{
		displayMessage();
		return true;
	}
}

function geographyValidate(dataValue){
	if(dataValue.length > max50){
		displayMessage("Level Value" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else{
		displayMessage();
		return true;
	}
}

function statutoryNatureValidate(){
	if($("#statutory-nature-name").val().trim().length > max50){
		displayMessage("Statutory Nature Name" + message.should_not_exceed + max50 + " characters");
		return false;
	}else{
		displayMessage();
		return true;
	}
}

function statutoryLevelValidate(){
	if($("#level1").val().trim().length > max50){
		displayMessage("Level 1" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#level2").val().trim().length > max50){
		displayMessage("Level 2" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#level3").val().trim().length > max50){
		displayMessage("Level 3" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#level4").val().trim().length > max50){
		displayMessage("Level 4" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#level5").val().trim().length > max50){
		displayMessage("Level 5" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#level6").val().trim().length > max50){
		displayMessage("Level 6" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#level7").val().trim().length > max50){
		displayMessage("Level 7" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#level8").val().trim().length > max50){
		displayMessage("Level 8" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#level9").val().trim().length > max50){
		displayMessage("Level 9" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#level10").val().trim().length > max50){
		displayMessage("Level 10" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else{
		displayMessage();
		return true;
	}
}

function statutoryValidate(dataValue){
	if(dataValue.length > max50){
		displayMessage("Level Value" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else{
		displayMessage();
		return true;
	}
}

function complianceValidate(){
	if($("#statutory_provision").val().trim().length > max500){
		displayMessage("Statutory Provision" + message.should_not_exceed + max500 + " characters");
		return false;
	}
	else if($("#compliance_task").val().trim().length > max100){
		displayMessage("Compliance Task" + message.should_not_exceed + max100 + " characters");
		return false;
	}
	else if($("#compliance_description").val().trim().length > max500){
		displayMessage("Compliance Description" + message.should_not_exceed + max500 + " characters");
		return false;
	}
	else if($("#compliance_document").val().trim().length > max50){
		displayMessage("Compliance Document" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#penal_consequences").val().trim().length > max500){
		displayMessage("Penal Consequences" + message.should_not_exceed + max500 + " characters");
		return false;
	}
	else if($("#triggerbefore").val().trim().length > max3){
		displayMessage("Trigger Before" + message.should_not_exceed + max3 + " characters");
		return false;
	}
	else if($("#duration").val().trim().length > max3){
		displayMessage("Duration" + message.should_not_exceed + max3 + " characters");
		return false;
	}
	else if($("#repeats_every").val().trim().length > max3){
		displayMessage("Repeats Every" + message.should_not_exceed + max3 + " characters");
		return false;
	}
	else{
		displayMessage();
		return true;
	}
}

function approveMappingValidate(dataValue){
	if(dataValue.length > max500){
		displayMessage("Reason Value" + message.should_not_exceed + max500 + " characters");
		return false;
	}
	else{
		displayMessage();
		return true;
	}
}


function profileValidate(){
	if($("#address").val().trim().length > max250){
		displayMessage("Address" + message.should_not_exceed + max250 + " characters");
		return false;
	}
	else if($("#countrycode").val().trim().length > max4){
		displayMessage("Country Code" + message.should_not_exceed + max4 + " characters");
		return false;
	}
	else if($("#areacode").val().trim().length > max4){
		displayMessage("Area Code" + message.should_not_exceed + max4 + " characters");
		return false;
	}
	else if($("#mobile").val().trim().length > max10){
		displayMessage("Contact No" + message.should_not_exceed + max10 + " characters");
		return false;
	}
	else{
		displayMessage();
		return true;
	}
}

function clientMasterValidate(){
	if($("#clientgroup-name").val().trim().length > max50){
		displayMessage("Group Name" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#username").val().trim().length > max100){
		displayMessage("Username" + message.should_not_exceed + max100 + " characters");
		return false;
	}
	else if($("#no-of-user-licence").val().trim().length > max3){
		displayMessage("No of User Licence" + message.should_not_exceed + max3 + " characters");
		return false;
	}
	else if($("#file-space").val().trim().length > max3){
		displayMessage("File Space" + message.should_not_exceed + max3 + " characters");
		return false;
	}
	else if($("#short-name").val().trim().length > max20){
		displayMessage("Short Name" + message.should_not_exceed + max20 + " characters");
		return false;
	}
	else{
		displayMessage();
		return true;
	}
}

function clientMasterValidate(){
	if($("#clientgroup-name").val().trim().length > max50){
		displayMessage("Group Name" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#username").val().trim().length > max100){
		displayMessage("Username" + message.should_not_exceed + max100 + " characters");
		return false;
	}
	else if($("#no-of-user-licence").val().trim().length > max3){
		displayMessage("No of User Licence" + message.should_not_exceed + max3 + " characters");
		return false;
	}
	else if($("#file-space").val().trim().length > max3){
		displayMessage("File Space" + message.should_not_exceed + max3 + " characters");
		return false;
	}
	else if($("#short-name").val().trim().length > max20){
		displayMessage("Short Name" + message.should_not_exceed + max20 + " characters");
		return false;
	}
	else{
		displayMessage();
		return true;
	}
}

function serviceProviderValidate(){
	if($("#service-provider-name").val().trim().length > max50){
		displayMessage("Service Provider" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#contact-person").val().trim().length > max50){
		displayMessage("Contact Person" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#country-code").val().trim().length > max4){
		displayMessage("Country Code" + message.should_not_exceed + max4 + " characters");
		return false;
	}
	else if($("#area-code").val().trim().length > max4){
		displayMessage("Area Code" + message.should_not_exceed + max4 + " characters");
		return false;
	}
	else if($("#mobile-number").val().trim().length > max10){
		displayMessage("Contact No" + message.should_not_exceed + max10 + " characters");
		return false;
	}
	else if($("#address").val().trim().length > max250){
		displayMessage("Address" + message.should_not_exceed + max250 + " characters");
		return false;
	}
	else{
		displayMessage();
		return true;
	}
}

function clientUserValidate(){
	if($("#employee-name").val().trim().length > max50){
		displayMessage("Employee Name" + message.should_not_exceed + max50 + " characters");
		return false;
	}
	else if($("#employee-id").val().trim().length > max100){
		displayMessage("Employee Id" + message.should_not_exceed + max100 + " characters");
		return false;
	}
	else if($("#country-code").val().trim().length > max4){
		displayMessage("Country Code" + message.should_not_exceed + max4 + " characters");
		return false;
	}
	else if($("#area-code").val().trim().length > max4){
		displayMessage("Area Code" + message.should_not_exceed + max4 + " characters");
		return false;
	}
	else if($("#mobile-number").val().trim().length > max10){
		displayMessage("Contact No" + message.should_not_exceed + max10 + " characters");
		return false;
	}
	else if($("#email-id").val().trim().length > max100){
		displayMessage("Email ID" + message.should_not_exceed + max100 + " characters");
		return false;
	}
	else{
		displayMessage();
		return true;
	}
}