$("#btn-statutory-nature-add").click(function(){
	$("#statutory-nature-view").hide();
	$("#statutory-nature-add").show();	
	$("#statutory-nature-name").val('');
 	$("#statutory-nature-id").val('');
	$(".error-message").html('');
});
$("#btn-statutory-nature-cancel").click(function(){
	$("#statutory-nature-add").hide();
	$("#statutory-nature-view").show();
});
function initialize(){
	function success(status, data){
		loadStatNatureData(data);
	}
	function failure(status, data){
	}
	mirror.getStatutoryNatureList(success, failure);
}
function loadStatNatureData(statNatureList){
  $(".tbody-statutory-nature-list").find("tr").remove();
	var sno=0;
	for(var i in statNatureList){
		var statNature=statNatureList[i];
		;
		for(var j in statNature){
			var statNatureName=statNature[j]['statutory_nature_name'];
			var statNatureId=statNature[j]['statutory_nature_id'];
			var statNatureActive=statNature[j]['is_active'];
			
			if(statNatureActive==1){	
				imageName="icon-active.png";
				title="Click here to deactivate";
				statusVal=0;
			}
			else{
				imageName="icon-inactive.png";	
				title="Click here to Activate";
				statusVal=1;
			}	
			var tableRow=$('#templates .table-statutory-nature-list .table-row');
			var clone=tableRow.clone();
			sno = sno + 1;
			$('.sno', clone).text(sno);
			$('.statutory-nature-name', clone).text(statNatureName);
			$('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="statNature_edit('+statNatureId+',\''+statNatureName+'\')"/>');
			$('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="statNature_active('+statNatureId+', '+statusVal+')"/>');
			$('.tbody-statutory-nature-list').append(clone);	
		}
	}
}
function validate(statutoryNatureNameVal){
	if(statutoryNatureNameVal.length==0){
		$(".error-message").html('Statutory Nature Name Required');
	}
}

$('#statutory-nature-name').keypress(function (e) {
	var statutoryNatureNameVal = $("#statutory-nature-name").val();
  if (e.which == 13) {
		if(statutoryNatureNameVal==''){
			$(".error-message").html('Statutory Nature Name Required');
		}
		else{
			jQuery('#btn-statutory-nature-submit').focus().click();
		}
  }
});
$("#btn-statutory-nature-submit").click(function(){
	var statutoryNatureIdVal = $("#statutory-nature-id").val();
	var statutoryNatureNameVal = $("#statutory-nature-name").val();
	validate(statutoryNatureNameVal);
	if(statutoryNatureIdVal==''){
		function success(status, data){
			if(status == 'success') {
		    	$("#statutory-nature-add").hide();
  				$("#statutory-nature-view").show();
  				initialize();
	  		}
	  		else {
      			$(".error-message").html(status);
      		}	
	    }
		function failure(status, data){
			$(".error-message").html(status);
		}
		mirror.saveStatutoryNature(statutoryNatureNameVal, success, failure);
	}
	else{
		function success(status, data){
			if(status == 'success') {
				$("#statutory-nature-add").hide();
  			$("#statutory-nature-view").show();
  			initialize();
  		}
  		if(status == 'StatutoryNatureNameAlreadyExists') {
  			$(".error-message").html(status);
  		}	
		}
		function failure(status, data){
		}
		mirror.updateStatutoryNature(parseInt(statutoryNatureIdVal), statutoryNatureNameVal, success, failure);
	}
});
function statNature_edit(statNatureId, statNatureName){
	$("#statutory-nature-add").show();
	$("#statutory-nature-view").hide();
	$("#statutory-nature-name").val(statNatureName);
  	$("#statutory-nature-id").val(statNatureId);
}
function statNature_active(statNatureId, isActive){
	function success(status, data){
	  initialize();
 	}
 	function failure(status, data){
 	}
 	mirror.changeStatutoryNatureStatus(parseInt(statNatureId), isActive, success, failure);
}
$("#search-statutory-nature-name").keyup(function() { 
	var count=0;
  var value = this.value.toLowerCase();
  $("table").find("tr:not(:first)").each(function(index) {
    if (index === 0) return;
      var id = $(this).find(".statutory-nature-name").text().toLowerCase();       
      $(this).toggle(id.indexOf(value) !== -1);;
  });
});
$(function() {
	initialize();
});