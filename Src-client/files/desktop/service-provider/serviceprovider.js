var splist;
$(function() {
	$("#service-provider-add").hide();
	initialize();
});
$("#btn-service-provider-add").click(function(){
	$("#service-provider-add").show();
	$("#service-provider-view").hide();
  $("#service-provider-id").val('');
  $(".error-message").html('');
  var x=document.getElementsByTagName("input");
 	for(i = 0; i<=x.length-1; i++){
  	if(x.item(i).type!="submit" ){ x.item(i).value = ""; }
  }
});
$("#btn-service-provider-cancel").click(function(){
	$("#service-provider-add").hide();
	$("#service-provider-view").show();
});
function initialize(){
	function success(status, data){
		splist=data;
		loadServiceProviderList(data);

	}
	function failure(status, data){
	}
	mirror.getServiceProviders("ClientAdminAPI", success, failure);
}
function loadServiceProviderList(serviceProviderList){
 	$(".tbody-service-provider-list").find("tr").remove();
  var sno=0;
	var imageName, title;	
	for(var i in serviceProviderList){
		var serviceProvider=serviceProviderList[i];
		for(var j in serviceProvider){
			var serviceProviderId=serviceProvider[j]["service_provider_id"];
			var serviceProviderName=serviceProvider[j]["service_provider_name"];
			var contactPerson=serviceProvider[j]["contact_person"];
			var contactNo=serviceProvider[j]["contact_no"];			
			var isActive=serviceProvider[j]["is_active"];
					
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
			var tableRow=$('#templates .table-service-provider-list .table-row');
			var clone=tableRow.clone();
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
	if(serviceProviderNameValue==''){
		$(".error-message").html('Please Enter Service Provider Name ');
	}
	else if(contactPersonValue==''){
		$(".error-message").html('Please Enter Contact Person Name ');
	}
	else if(countryCodeValue==''){
		$(".error-message").html('Please Enter Country Code');
	}
	else if(mobileNumberValue==''){
		$(".error-message").html('Please Enter Mobile Number');
	}
	else if(addressValue==''){
		$(".error-message").html('Please Enter Address ');
	}
	else if(contractFromValue==''){
		$(".error-message").html('Please Enter Contract From ');
	}
	else if(contractToValue==''){
		$(".error-message").html('Please Enter Contract To');
	}

	else if(serviceProviderIdValue==''){		
		function success(status, data){
			if(status == 'SaveServiceProviderSuccess') {
		    	$("#service-provider-add").hide();
	  			$("#service-provider-view").show();
	  			initialize();
	  		}
	  		if(status == 'ServiceProviderNameAlreadyExists') {
  				$(".error-message").html('Service Provider Name Already Exists');
  			}	
  			if(status == 'ContactNumberAlreadyExists') {
	  			$(".error-message").html('Contact Number Already Exists');
  			}	
	    }
		function failure(status, data){
			$(".error-message").html(status);
		}
		var serviceProviderDetail = {}
		serviceProviderDetail["service_provider_name"]=serviceProviderNameValue;
		serviceProviderDetail["address"]=addressValue;
		serviceProviderDetail["contract_from"]=contractFromValue;
		serviceProviderDetail["contract_to"]=contractToValue;
		serviceProviderDetail["contact_person"]=contactPersonValue;
		serviceProviderDetail["contact_no"]=countryCodeValue+'-'+areaCodeValue+'-'+mobileNumberValue;
		mirror.saveServiceProvider("ClientAdminAPI", serviceProviderDetail, success, failure);
	}
	else{		
		function success(status, data){
			if(status == 'UpdateServiceProviderSuccess') {
				$("#service-provider-add").hide();
	  			$("#service-provider-view").show();
	  			initialize();
  		}
  		if(status == 'ServiceProviderNameAlreadyExists') {
  			$(".error-message").html('Service Provider Name Already Exists');
  		}	
  		if(status == 'ContactNumberAlreadyExists') {
  			$(".error-message").html('Contact Number Already Exists');
  		}	
		}
		function failure(status, data){
		}
		var serviceProviderDetail = {}
		serviceProviderDetail["service_provider_id"]=parseInt(serviceProviderIdValue);
		serviceProviderDetail["service_provider_name"]=serviceProviderNameValue;
		serviceProviderDetail["address"]=addressValue;
		serviceProviderDetail["contract_from"]=contractFromValue;
		serviceProviderDetail["contract_to"]=contractToValue;
		serviceProviderDetail["contact_person"]=contactPersonValue;
		serviceProviderDetail["contact_no"]=countryCodeValue+'-'+areaCodeValue+'-'+mobileNumberValue;
		mirror.updateServiceProvider("ClientAdminAPI", serviceProviderDetail, success, failure);
	}
});
function serviceprovider_edit(serviceProviderId){
	$("#service-provider-add").show();
	$("#service-provider-view").hide();
	$("#service-provider-id").val(serviceProviderId);
	for(var i in splist){
		var lists=splist[i];
		for(var j in lists){
			if(lists[j]['service_provider_id']==serviceProviderId){
				$('#service-provider-name').val(lists[j]['service_provider_name']);
				$('#contact-person').val(lists[j]['contact_person']);
				$('#address').val(lists[j]['address']);
				$('#contract-from').val(lists[j]['contract_from']);
				$('#contract-to').val(lists[j]['contract_to']);
				var mobileno=(lists[j]['contact_no']).split("-");
				$('#country-code').val(mobileno[0]);
				$('#area-code').val(mobileno[1]);
				$('#mobile-number').val(mobileno[2]);
			}	
		}
	}
}
function serviceprovider_active(serviceProviderId, isActive){
  	function success(status, data){
	  initialize();
  	}
  	function failure(status, data){
  	}
  	mirror.changeServiceProviderStatus("ClientAdminAPI", parseInt(serviceProviderId), isActive, success, failure);
}


$("#search-service-provider").keyup(function() { 
  var value = this.value.toLowerCase();
  $("table").find("tr:not(:first)").each(function(index) {
    if (index === 0) return;
    var id = $(this).find(".service-provider-name").text().toLowerCase();       
    $(this).toggle(id.indexOf(value) !== -1);;
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


