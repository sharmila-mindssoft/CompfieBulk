$(function() {
	$("#country-add").hide();
	initialize();
});
$(".btn-country-add").click(function(){
	$("#country-add").show();
	$("#country-view").hide();
	$("#countryName").val('');
  	$("#countryId").val('');
  	$(".error-message").html('');
});
$(".btn-country-cancel").click(function(){
	$("#country-add").hide();
	$("#country-view").show();
});
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
function initialize(){
	function success(status, data){
		loadData(data);
	}
	function failure(status, data){
	}
	mirror.getCountryList("getCountryList", success, failure);
}

function loadData(countriesList){
 	$('#tableRow').show();
  	$("#tableCountriesList").find("tr:gt(0)").remove();
  	var sno=1;
	var imageName, title;	
	for(var i in countriesList){
		var countries=countriesList[i];
		for(var j in countries){
			var countryId=countries[j]["country_id"];
			var countryName=countries[j]["country_name"];
			var isActive=countries[j]["is_active"];
					
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
			var tableName = document.getElementById("tableCountriesList");
			var tableRow=document.getElementById('tableRow');
			var clone=tableRow.cloneNode(true);
			clone.id = sno; 

			clone.cells[0].innerHTML =sno;
			clone.cells[1].innerHTML=countryName;
			clone.cells[2].innerHTML='<img src="/images/icon-edit.png" id="editid" onclick="country_edit('+countryId+',\''+countryName+'\')"/>';
			clone.cells[3].innerHTML='<img src="/images/'+imageName+'" title="'+title+'" onclick="country_active('+countryId+', '+statusVal+')"/>';
			tableName.appendChild(clone);
			sno = sno + 1;
		}
		$('#tableRow').hide();
	}
}

$("#submit").click(function(){
	var countryIdValue = $("#countryId").val();
	var countryNameValue = $("#countryName").val();
	if(countryNameValue=='' || countryNameValue==null){
		$(".error-message").html('Country Name Required');
	}
	else if(countryIdValue==''){		
		function success(status, data){
			if(status == 'success') {
		    	$("#country-add").hide();
	  			$("#country-view").show();
	  			initialize();
	  		}
	  		 else {
      			$(".error-message").html(status);
      		}	
	    }
		function failure(status, data){
			$(".error-message").html(status);
		}
		mirror.saveCountry("SaveCountry", countryNameValue, success, failure);
	}
	else{		
		function success(status, data){
			if(status == 'success') {
				$("#country-add").hide();
	  			$("#country-view").show();
	  			initialize();
  			}
  			if(status == 'CountryNameAlreadyExists') {
  				$(".error-message").html(status);
  			}	
		}
		function failure(status, data){
		}
		mirror.updateCountry("updateCountry", parseInt(countryIdValue), countryNameValue, success, failure);
	}
});
function country_edit(countryId, countryName){
	$("#country-add").show();
	$("#country-view").hide();
	$("#countryName").val(countryName);
  	$("#countryId").val(countryId);
}
function country_active(countryId, isActive){
	$("#countryName").val(countryName);
  	$("#countryId").val(countryId);
  	function success(status, data){
	  initialize();
  	}
  	function failure(status, data){
  	}
  	mirror.changeCountryStatus("ChangeCountryStatus",  parseInt(countryId), isActive, success, failure);
}

function filter (term, cellNr){
	var suche = term.value.toLowerCase();
	var table = document.getElementById("tableCountriesList");
	var ele;

	for (var r = 0; r < table.rows.length; r++){
		ele = table.rows[r].cells[cellNr].innerHTML.replace(/<[^>]+>/g,"");
		if (ele.toLowerCase().indexOf(suche)>=0 )
			table.rows[r].style.display = '';
		else table.rows[r].style.display = 'none';
	}
}
