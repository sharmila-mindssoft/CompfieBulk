$(function() {
	$("#clientunit-add").hide();
	initialize();
});
$(".btn-clientunit-add").click(function(){
	$("#clientunit-add").show();
	$("#clientunit-view").hide();
 	//$("#clientunit-id").val('');
  	$(".error-message").html('');
});
$(".btn-clientunit-cancel").click(function(){
	$("#clientunit-add").hide();
	$("#clientunit-view").show();
});
function initialize(){
	function success(status, data){
		loadClientsList(data);
	}
	function failure(status, data){
		$(".error-message").html(status);
	}
	mirror.getClients("TechnoAPI", success, failure);
}
function loadClientsList(clientunitsList){
 	$(".tbody-clientunit-list").find("tr").remove();
  	var sno=0;
	var imageName, title;	
	for(var i in clientunitList){
		var clientunits=clientunitsList[i];
		for(var j in clientunits){
			var clientunitId=clientunits[j]["clientunit_id"];
			var clientunitName=clientunits[j]["clientunit_name"];
			var isActive=clientunits[j]["is_active"];
					
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
			var tableRow=$('#templates .table-clientunits-list .table-row');
			var clone=tableRow.clone();
			sno = sno + 1;
			$('.sno', clone).text(sno);
			$('.clientunit-name', clone).text(clientunitName);
			$('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="clientunit_edit('+clientunitId+',\''+clientunitName+'\')"/>');
			$('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="clientunit_active('+clientunitId+', '+statusVal+')"/>');
			$('.tbody-clientunits-list').append(clone);
		}
	}
}

$("#btn-clientunit-submit").click(function(){
	var clientunitIdValue = $("#clientunit-id").val();
	var clientunitNameValue = $("#clientunit-name").val();
	if(clientunitNameValue=='' || clientunitNameValue==null){
		$(".error-message").html('clientunit Name Required');
	}
	else if(clientunitIdValue==''){		
		function success(status, data){
			if(status == 'success') {
		    	$("#clientunit-add").hide();
	  			$("#clientunit-view").show();
	  			initialize();
	  		}
	  		 else {
      			$(".error-message").html(status);
      		}	
	    }
		function failure(status, data){
			$(".error-message").html(status);
		}
		mirror.saveclientunit("Saveclientunit", clientunitNameValue, success, failure);
	}
	else{		
		function success(status, data){
			if(status == 'success') {
				$("#clientunit-add").hide();
	  			$("#clientunit-view").show();
	  			initialize();
  			}
  			if(status == 'clientunitNameAlreadyExists') {
  				$(".error-message").html(status);
  			}	
		}
		function failure(status, data){
		}
		mirror.updateclientunit("updateclientunit", parseInt(clientunitIdValue), clientunitNameValue, success, failure);
	}
});
function clientunit_edit(clientunitId, clientunitName){
	$("#clientunit-add").show();
	$("#clientunit-view").hide();
	$("#clientunit-name").val(clientunitName);
  	$("#clientunit-id").val(clientunitId);
}
function clientunit_active(clientunitId, isActive){
  	$("#clientunit-id").val(clientunitId);
  	function success(status, data){
	  initialize();
  	}
  	function failure(status, data){
  	}
  	mirror.changeclientunitStatus("ChangeclientunitStatus",  parseInt(clientunitId), isActive, success, failure);
}


$("#search-clientunit-name").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".clientunit-name").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});
