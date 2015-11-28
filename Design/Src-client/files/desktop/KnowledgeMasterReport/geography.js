var countriesList;
var geographiesList;

$(function() {
	initialize();
});
function initialize(){
	function success(status, data){
		console.log(data);
		//loadGeographyList(data);
		alert("success");
	}
	function failure(status, data){
	}
	mirror.getGeographyReport("GeographyReport", success, failure);
}

function loadGeographyList(domainList){
  	/*var sno=0;
	var title;	
	for(var i in domainList){
		var domains=domainList[i];
		for(var j in domains){
			var isActive=domains[j]["is_active"];
			if(isActive==1){ title="Active"; }
			else { title="Inacive"; }
			var tableRow=$('#templates .table-domain-report .table-row');
			var clone=tableRow.clone();
			sno = sno + 1;
			$('.sno', clone).text(sno);
			$('.domain-name', clone).text(domains[j]["domain_name"]);
			$('.is-active', clone).text(title);
			$('.tbody-geography-list').append(clone);			
		}
	
	}
	$("#total-records").html('Total : '+sno+' records');*/
}
$("#search-geography-name").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $("table").find("tr:not(:first):not(:last)").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".geography-name").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
    count = $('tr:visible').length-3;
    $("#total-records").html('Total : '+count+' records');
});


//Autocomplete Script Starts
//Hide list items after select
function hidemenu() {
  document.getElementById('autocompleteview').style.display = 'none';
}

//load country list in autocomplete text box  
function loadauto_text (textval) {
  document.getElementById('autocompleteview').style.display = 'block';
  var countries = countriesList;
  var suggestions = [];
  $('#ulist_text').empty();
  if(textval.length>0){
    for(var i in countries){
      if (~countries[i]["country_name"].toLowerCase().indexOf(textval.toLowerCase()) && countries[i]["is_active"] == 1) suggestions.push([countries[i]["country_id"],countries[i]["country_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_text').append(str);
    $("#country").val('');
    }
}
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#countryval").val(checkname);
  $("#country").val(checkval);
  
  loadGeographyFirstLevels(checkval);
}
//Autocomplete Script ends
