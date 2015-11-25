$(function() {
	$("#country-add").hide();
	initialize();
});
$(".btn-country-add").click(function(){
	$("#country-add").show();
	$("#country-view").hide();
	$("#country-name").val('');
  	$("#country-id").val('');
  	$(".error-message").html('');
});
$(".btn-country-cancel").click(function(){
	$("#country-add").hide();
	$("#country-view").show();
});
function initialize(){
	function success(status, data){
		loadCountriesList(data);
	}
	function failure(status, data){
	}
	mirror.getCountryList("getCountryList", success, failure);
}

function loadCountriesList(countriesList){
 	$(".tbody-countries-list").find("tr").remove();
  	var sno=0;
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
			var tableRow=$('#templates .table-countries-list .table-row');
			var clone=tableRow.clone();
			sno = sno + 1;
			$('.sno', clone).text(sno);
			$('.country-name', clone).text(countryName);
			$('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="country_edit('+countryId+',\''+countryName+'\')"/>');
			$('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="country_active('+countryId+', '+statusVal+')"/>');
			$('.tbody-countries-list').append(clone);
		}
	}
}

$("#submit").click(function(){
	var countryIdValue = $("#country-id").val();
	var countryNameValue = $("#country-name").val();
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
	$("#country-name").val(countryName);
  	$("#country-id").val(countryId);
}
function country_active(countryId, isActive){
  	$("#country-id").val(countryId);
  	function success(status, data){
	  initialize();
  	}
  	function failure(status, data){
  	}
  	mirror.changeCountryStatus("ChangeCountryStatus",  parseInt(countryId), isActive, success, failure);
}


$("#search-country-name").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".country-name").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});
