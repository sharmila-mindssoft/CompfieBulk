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
	mirror.getCountryList("getCountryList", success, failure);
	function success(status, data){
		loadData(data[1]);
	}
	function failure(status, data){

	}
	// var countries_url = "http://192.168.1.9:8080/GetCountries";
	// var countries_data = {
	// 	"session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
	// 	"request" : [
	// 		"GetCountries",
	// 		{}
	// 	]
	// };
	// var options = JSON.stringify(countries_data);	
	// ajaxCall(countries_url, options, function (data) {
	// 	loadData(data[1]);
	// });
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
		mirror.SaveCountry("SaveCountry", success, failure);
		function success(status, data){
		    $("#country-add").hide();
	  		$("#country-view").show();
	  		initialize();
	    }
		function failure(status, data){
			$(".error-message").html(data[0]);
		}
	}
	else{
		var countries_url = "http://192.168.1.9:8080/UpdateCountry";
 		var countries_data = {
 			"session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
           	"request" : [
	            "UpdateCountry",
	            {
	                "country_id": parseInt(countryIdValue),
	                "country_name": countryNameValue,
	            }
       		]
    	};
    	var options = JSON.stringify(countries_data);
  		ajaxCall(countries_url, options, function (data) {  		
  			$("#country-add").hide();
  			$("#country-view").show();
  			initialize();
		});	
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

  	var countries_url = "http://192.168.1.9:8080/ChangeDomainStatus";
  	var countries_data = {
          "session_token" : "b4c59894336c4ee3b598f5e4bd2b276b",
          "request" : [
              "ChangeCountryStatus",
            {
                "country_id": countryId,
                "is_active": isActive
            }
          ]
      };
  	var options = JSON.stringify(countries_data);

	ajaxCall(countries_url, options, function (data) {
	  console.log(data)
	  initialize();
	});
}

function filter (term, cellNr){
	var suche = term.value.toLowerCase();
	var table = document.getElementById("tableCountriesList");
	var ele;
	for (var r = 1; r < table.rows.length; r++){
		ele = table.rows[r].cells[cellNr].innerHTML.replace(/<[^>]+>/g,"");
		if (ele.toLowerCase().indexOf(suche)>=0 )
			table.rows[r].style.display = '';
		else table.rows[r].style.display = 'none';
	}
}
