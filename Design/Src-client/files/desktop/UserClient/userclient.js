$(function() {
	$("#user-add").hide();
	initialize();
});
$(function() {
 	$('.service_provider').hide();
	$('#usertype').change(function () {
		if($("#usertype").val()=='Service Provider'){
		  $('.service_provider').show();
		  $('.star').hide();
		  $('.seatingunit').hide();      
		}
		else{
	  	$('.service_provider').hide();
	  	$('.seatingunit').show();   
	  	$('.star').show();  
		}
	});
});
$("#btn-user-add").click(function(){
	$("#user-add").show();
	$("#user-view").hide();
  $(".error-message").html('');  
  $("#user-privilege-id").val('');
  	
	function success(status, data){
		//loadUserGroupdata(data['user_groups']);
		//loadFormData(data['forms'])		
	}
	function failure(status, data){
		console.log(status);
	}
	mirror.getClientUsers("ClientAdminAPI", success, failure);
});
$("#btn-user-cancel").click(function(){
	$("#user-add").hide();
	$("#user-view").show();
});
function initialize(){
	function success(status, data){
		getCountryList(data['countries'], "select");
		
	}
	function failure(status, data){
		console.log(status);
	}
	mirror.getClientUsers("ClientAdminAPI", success, failure);
}
function loadUserGroupdata(list){

}
function getCountryList(countryList, formtype){
	$.each(countryList, function(key, value){
		if(formtype=="select"){
			return "<option>"+countryList[key]['country_name']+"</option>";
		}
		if(formtype=="ul"){
			return "<li>"+countryList[key]['country_name']+"</li>";
		}
	});
}