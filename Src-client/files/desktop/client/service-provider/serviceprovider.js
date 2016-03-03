var splist;
function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}
$("#btn-service-provider-add").click(function(){
	$("#service-provider-view").hide();
	$("#service-provider-add").show();	
	$("#service-provider-id").val('');
	clearMessage();
  	var x = document.getElementsByTagName("input");
 	for(i = 0; i <= x.length-1; i++){
  		if(x.item(i).type != "submit" ){ x.item(i).value = ""; }
  	}
  	$("#address").val('');
});
$("#btn-service-provider-cancel").click(function(){
	$("#service-provider-add").hide();
	$("#service-provider-view").show();
});
function initialize(){
	function onSuccess(data){
		splist = data;
		loadServiceProviderList(data);
	}
	function onFailure(error){
		console.log(error);
	}
	client_mirror.getServiceProviders(
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
function loadServiceProviderList(serviceProviderList){
 	$(".tbody-service-provider-list").find("tr").remove();
	var sno = 0;
	var imageName, title;	
	for(var i in serviceProviderList){
		var serviceProvider = serviceProviderList[i];
		for(var j in serviceProvider){
			var serviceProviderId = serviceProvider[j]["service_provider_id"];
			var serviceProviderName = serviceProvider[j]["service_provider_name"];
			var contactPerson = serviceProvider[j]["contact_person"];
			var contactNo = serviceProvider[j]["contact_no"];			
			var isActive = serviceProvider[j]["is_active"];
					
			if(isActive == true){
				imageName = "icon-active.png";
				title = "Click here to deactivate"
				statusVal = false;
			}
			else{
				imageName = "icon-inactive.png";	
				title = "Click here to Activate"
				statusVal = true;
			}
			var tableRow = $('#templates .table-service-provider-list .table-row');
			var clone = tableRow.clone();
			sno = sno + 1;
			$('.sno', clone).text(sno);
			$('.service-provider-name', clone).text(serviceProviderName);
			$('.contact-person', clone).text(contactPerson);
			$('.contact-number', clone).text(contactNo.replace(/-/g," "));
			$('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="serviceprovider_edit('+serviceProviderId+')"/>');
			$('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="serviceprovider_active('+serviceProviderId+', '+statusVal+')"/>');
			$('.tbody-service-provider-list').append(clone);
		}
	}
}
$('#country-code').on('input', function (event) {
    this.value = this.value.replace(/[^0-9]/g, '');
});
$('#area-code').on('input', function (event) {
    this.value = this.value.replace(/[^0-9]/g, '');
});
$('#mobile-number').on('input', function (event) {
    this.value = this.value.replace(/[^0-9]/g, '');
});

$("#submit").click(function(){
	var serviceProviderIdValue = $("#service-provider-id").val();
	var serviceProviderNameValue = $("#service-provider-name").val();
	var contactPersonValue = $("#contact-person").val();
	var countryCodeValue = $("#country-code").val();
	var areaCodeValue = $("#area-code").val();
	var mobileNumberValue = $("#mobile-number").val();
	var addressValue = $("#address").val();
	var contractFromValue = $("#contract-from").val();
	var contractToValue = $("#contract-to").val();
	if(serviceProviderNameValue == ''){
		displayMessage('Enter Service Provider Name ');
	}
	else if(serviceProviderNameValue.length > 50){
		displayMessage('Service Provider Name is maximum 50 characters Allowed');
	}
	else if(contactPersonValue == ''){
		displayMessage('Enter Contact Person Name ');
	}
	else if(contactPersonValue.length > 50){
		displayMessage('Contact Person Name is maximum 50 characters Allowed');
	}
	else if(countryCodeValue == ''){
		displayMessage('Enter Contact No. Country Code');
	}
	else if(countryCodeValue.length > 4){
		displayMessage('Contact No. Country Code is maximum 4 characters Allowed');
	}
	else if(areaCodeValue > 4){
		displayMessage('Contact No. Area Code is maximum 4 characters');
	}
	else if(mobileNumberValue == ''){
		displayMessage('Enter Contact No.');
	}
	else if(mobileNumberValue.length > 12){
		displayMessage('Contact No. is maximum 12 characters Allowed');
	}
	else if(addressValue.length > 500){
		displayMessage('Address is maximum 500 characters Allowed');
	}
	else if(contractFromValue == ''){
		displayMessage('Enter Contract From ');
	}
	else if(contractToValue == ''){
		displayMessage('Enter Contract To');
	}
	else if(serviceProviderIdValue == ''){		
		function onSuccess(data){
		    $("#service-provider-add").hide();
	  		$("#service-provider-view").show();
	  		initialize();
	    }
		function onFailure(error){
			if(error == 'ServiceProviderNameAlreadyExists') {
  				displayMessage('Service Provider Name Already Exists');
  			}	
  			if(error == 'ContactNumberAlreadyExists') {
	  			displayMessage('Contact Number Already Exists');
  			}	
	 
		}
		var serviceProviderDetail;
		var contactNo = countryCodeValue+'-'+areaCodeValue+'-'+mobileNumberValue;
        serviceProviderDetail = [serviceProviderNameValue, addressValue, contractFromValue, 
        contractToValue, contactPersonValue, contactNo];
        serviceProviderDetail = client_mirror.getSaveServiceProviderDict(serviceProviderDetail);

		client_mirror.saveServiceProvider( serviceProviderDetail, 
			function (error, response){
				if(error == null){
					onSuccess(response);
				}
				else{
					onFailure(error);
				}
			}
		);
	}
	else{		
		function onSuccess(data){	
			$("#service-provider-add").hide();
	  		$("#service-provider-view").show();
	  		initialize();
  		}
  			
		function onFailure(error){
			if(error == 'ServiceProviderNameAlreadyExists') {
  				displayMessage('Service Provider Name Already Exists');
  			}	
  			if(error == 'ContactNumberAlreadyExists') {
  				displayMessage('Contact Number Already Exists');
  			}
		}
		var serviceProviderDetail;
		var contactNo = countryCodeValue+'-'+areaCodeValue+'-'+mobileNumberValue;

        serviceProviderDetail = [parseInt(serviceProviderIdValue), serviceProviderNameValue, addressValue, 
        contractFromValue, contractToValue, contactPersonValue, contactNo]
        serviceProviderDetail = client_mirror.getUpdateServiceProviderDict(serviceProviderDetail)

		client_mirror.updateServiceProvider(serviceProviderDetail, 
			function (error, response){
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
function serviceprovider_edit(serviceProviderId){
	$("#service-provider-view").hide();
	$("#service-provider-add").show();
	clearMessage();
	$("#service-provider-id").val(serviceProviderId);
	for(var i in splist){
		var lists = splist[i];
		for(var j in lists){
			if(lists[j]['service_provider_id'] == serviceProviderId){
				$('#service-provider-name').val(lists[j]['service_provider_name']);
				$('#contact-person').val(lists[j]['contact_person']);
				$('#address').val(lists[j]['address']);
				$('#contract-from').val(lists[j]['contract_from']);
				$('#contract-to').val(lists[j]['contract_to']);
				var mobileno = (lists[j]['contact_no']).split("-");
				$('#country-code').val(mobileno[0]);
				$('#area-code').val(mobileno[1]);
				$('#mobile-number').val(mobileno[2]);
			}	
		}
	}
}
function serviceprovider_active(serviceProviderId, isActive){
  	function onSuccess(data){
		initialize();
  	}
  	function onFailure(error){
  		console.log(error);
  	}
  	client_mirror.changeServiceProviderStatus(parseInt(serviceProviderId), isActive, 
  		function (error, response){
			if(error == null){
				onSuccess(response);
			}
			else{
				onFailure(error);
			}
		}
	);
}


$("#search-service-provider").keyup(function() { 
  var value = this.value.toLowerCase();
  $("table").find("tr:not(:first)").each(function(index) {
    if (index === 0) return;
    var id = $(this).find(".service-provider-name").text().toLowerCase();       
    $(this).toggle(id.indexOf(value) !== -1);
  });
});
$("#search-contact-person").keyup(function() { 
  var value = this.value.toLowerCase();
  $("table").find("tr:not(:first)").each(function(index) {
    if (index === 0) return;
    var id = $(this).find(".contact-person").text().toLowerCase();       
    $(this).toggle(id.indexOf(value) !== -1);;
  });
});

$("#search-contact-no").keyup(function() { 
  var value = this.value.toLowerCase();
  $("table").find("tr:not(:first)").each(function(index) {
    if (index === 0) return;
    var id = $(this).find(".contact-number").text().toLowerCase();       
    $(this).toggle(id.indexOf(value) !== -1);;
  });
});
$(function() {
	initialize();
});

