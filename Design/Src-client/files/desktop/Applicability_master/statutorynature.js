$(function() {
	$("#statutoryNatureAdd").hide();
	initialize();
});
$("#btnStatutoryNatureAdd").click(function(){
	$("#statutoryNatureAdd").show();
	$("#statutoryNatureView").hide();
	$("#statutoryNatureName").val('');
 	$("#statutoryNatureId").val('');
  	$(".error-message").html('');
});
$("#btnStatutoryNatureCancel").click(function(){
	$("#statutoryNatureAdd").hide();
	$("#statutoryNatureView").show();
});
function initialize(){
	function success(status, data){
		loadStatNatureData(data);
	}
	function failure(status, data){
	}
	mirror.getStatutoryNatureList("GetStatutoryNatures", success, failure);
}
function loadStatNatureData(statNatureList){
	$('#tableRow').show();
  	$("#tableStatutoryNatureList").find("tr:gt(0)").remove();
	var sno=1;
	for(var i in statNatureList){
		var statNature=statNatureList[i];
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
			var tableName=document.getElementById("tableStatutoryNatureList");
			var tableRow=document.getElementById("tableRow");
			var clone=tableRow.cloneNode(true);

			clone.cells[0].innerHTML=sno;
			clone.cells[1].innerHTML=statNatureName;
			clone.cells[2].innerHTML='<img src="/images/icon-edit.png" id="editid" onclick="statNature_edit('+statNatureId+',\''+statNatureName+'\')"/>';
			clone.cells[3].innerHTML='<img src="/images/'+imageName+'" title="'+title+'" onclick="statNature_active('+statNatureId+', '+statusVal+')"/>';
			tableName.appendChild(clone);
      		sno = sno + 1;
		}
		$('#tableRow').hide();
	}
}

$("#btnStatutoryNatureSubmit").click(function(){
	var statutoryNatureIdVal = $("#statutoryNatureId").val();
	var statutoryNatureNameVal = $("#statutoryNatureName").val();
	if(statutoryNatureNameVal=='' || statutoryNatureNameVal==null){
		$(".error-message").html('Statutory Nature Name Required');
	}
	else if(statutoryNatureIdVal==''){

		function success(status, data){
			if(status == 'success') {
		    	$("#statutoryNatureAdd").hide();
  				$("#statutoryNatureView").show();
  				initialize();
	  		}
	  		else {
      			$(".error-message").html(status);
      		}	
	    }
		function failure(status, data){
			$(".error-message").html(status);
		}
		mirror.saveStatutoryNature("SaveStatutoryNature", statutoryNatureNameVal, success, failure);
		
	}
	else{
		function success(status, data){
			if(status == 'success') {
				$("#statutoryNatureAdd").hide();
  				$("#statutoryNatureView").show();
  				initialize();
  			}
  			if(status == 'StatutoryNatureNameAlreadyExists') {
  				$(".error-message").html(status);
  			}	
		}
		function failure(status, data){
		}
		mirror.updateStatutoryNature("UpdateStatutoryNature", parseInt(statutoryNatureIdVal), statutoryNatureNameVal, success, failure);
	
	}
});
function statNature_edit(statNatureId, statNatureName){
	$("#statutoryNatureAdd").show();
	$("#statutoryNatureView").hide();
	$("#statutoryNatureName").val(statNatureName);
  	$("#statutoryNatureId").val(statNatureId);
}
function statNature_active(statNatureId, isActive){
	function success(status, data){
	  initialize();
  	}
  	function failure(status, data){
  	}
  	mirror.changeCountryStatus("ChangeStatutoryNatureStatus",  parseInt(statNatureId), isActive, success, failure);

}
function ajaxCall (url, options, callback) {
	$.support.cors = true;
	$.ajax({
		crossDomain: true,
		url: url,
		dataType: 'json',
		type: 'POST',
		data: options,
		success: function(data) {
			console.log(data);
			callback(data);					
		},
		error: function(xhr, status, err) {
			console.error(url, status, err.toString());
			callback(null);
		}
	});
}


function filter (term, cellNr){
	var suche = term.value.toLowerCase();
	var table = document.getElementById("tableStatutoryNatureList");
	var ele;
	for (var r = 0; r < table.rows.length; r++){
		ele = table.rows[r].cells[cellNr].innerHTML.replace(/<[^>]+>/g,"");
		if (ele.toLowerCase().indexOf(suche)>=0 )
			table.rows[r].style.display = '';
		else table.rows[r].style.display = 'none';
	}
}