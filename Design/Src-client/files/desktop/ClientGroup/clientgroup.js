$(function() {
	$("#clientgroup-add").hide();
	initialize();
});
$(".btn-clientgroup-add").click(function(){
	$("#clientgroup-add").show();
	$("#clientgroup-view").hide();
	$("#clientgroup-name").val('');
  $("#clientgroup-id").val('');
  $(".error-message").html('');

});
$(".btn-clientgroup-cancel").click(function(){
	$("#clientgroup-add").hide();
	$("#clientgroup-view").show();
});
function initialize(){
	function success(status, data){
		console.log(data);
		loadClientGroupList(data);
	}
	function failure(status, data){
	}
	mirror.getClientGroup("GetClientGroup", success, failure);
}

function loadClientGroupList(clientGroupList){
  var sno=0;
	var imageName, title;	
	for(var i in clientGroupList){
		var clientGroups=clientGroupList[i];
		for(var j in clientGroups){
			var isActive=clientGroups[j]["is_active"];
			if(isActive==1){
				imageName="icon-active.png";
				title="Click here to deactivate"
				statusVal=0;
			}
			else{
				imageName="icon-inactive.png";	
				title="Click here to Activate"
				statusVal=1;
			}
			var tableRow=$('#templates .table-clientgroup-list .table-row');
			var clone=tableRow.clone();
			sno = sno + 1;
			$('.sno', clone).text(sno);
			$('.domain-name', clone).text(clientGroups[j]["domain_name"]);
			$('.is-active', clone).text(title);
			$('.tbody-domain-list').append(clone);			
		}
	
	}
	$("#total-records").html('Total : '+sno+' records');
}

$("#btn-clientgroup-submit").click(function(){
	var clientGroupIdVal = $("#clientgroup-id").val();
	var clientGroupNameVal = $("#clientgroup-name").val();
	var countriesVal = $("#countries").val();
	var domainsVal = $("#domains").val();
	var contractFromVal = $("#contract-from").val();
	var contractToVal = $("#contract-to").val();
	var usernameVal = $("#username").val();
	var uploadLogoVal = $("#upload-logo").val();
	var licenceVal = $("#no-of-user-licence").val();
	var fileSpaceVal = $("#file-space").val();
	var subscribeSmsVal = $("#subscribe-sms").val();
	var inchargePersonVal = $("#incharge-person").val();

	
	if(clientGroupNameVal==''){
		$(".error-message").html('Group Required');
	}
	else if(countriesVal==''){
		$(".error-message").html('Country Required');
	}
	else if(domainsVal==''){
		$(".error-message").html('Domain Required');
	}
	else if(contractFromVal==''){
		$(".error-message").html('Contract From Required');
	}
	else if(contractToVal==''){
		$(".error-message").html('Contract To Required');
	}
	else if(usernameVal==''){
		$(".error-message").html('Username Required');
	}
	else if(validateEmail(usernameVal)==''){
		$(".error-message").html('Username Invalid Format');
	}
	else if(uploadLogoVal==''){
		$(".error-message").html('Logo Required');
	}
	else if(licenceVal==''){
		$(".error-message").html('No. Of User Licence Required');
	}
	else if(validateDigit(licenceVal)){
		$(".error-message").html('Invalid No. Of User Licence');
	}
	else if(fileSpaceVal==''){
		$(".error-message").html('File Space Required');
	}
	else if(!$.isNumeric(fileSpaceVal)){
		$(".error-message").html('File Space Value Invalid');
	}
	else if(inchargePersonVal==''){
		$(".error-message").html('Incharge Person Required');
	}
	else if(countryIdValue==''){		
		function success(status, data){
			if(status == 'success') {
		    	$("#clientgroup-add").hide();
	  			$("#clientgroup-view").show();
	  			initialize();
	  		}
	  		 else {
      			$(".error-message").html(status);
      		}	
	    }
		function failure(status, data){
			$(".error-message").html(status);
		}
		clientGroupDetails
		mirror.saveClientGroup("TechnoAPI", clientGroupDetails, dateConfigurations,success, failure);
	}
});
function validateDigit($numb) {
  if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
    $(".error-message").html("Invaild Number");
    return false;
  }
}
function validateEmail($email) {
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  return emailReg.test( $email );
}
$("#search-clientgroup-name").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first):not(:last)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".clientgroup-name").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
   
});
