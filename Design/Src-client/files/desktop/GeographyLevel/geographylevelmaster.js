var countriesList;
var geographyLevelsList;

$(document).ready(function(){
	GetGeographyLevels()
});

function GetGeographyLevels(){
	function success(status,data){
		geographyLevelsList = data["geography_levels"];
		countriesList = data["countries"];
	}
	function failure(data){
	}
	mirror.getGeographyLevels("GetGeographyLevels", success, failure);
}
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
  loadGeographyLevelsList(checkval);
}
//Autocomplete Script ends
function loadGeographyLevelsList(countryval) {
	$("#level1").val("");
	$("#level2").val("");
	$("#level3").val("");
	$("#level4").val("");
	$("#level5").val("");
	$("#level6").val("");
	$("#level7").val("");
	$("#level8").val("");
	$("#level9").val("");
	$("#level10").val("");

	$("#levelid1").val("");
	$("#levelid2").val("");
	$("#levelid3").val("");
	$("#levelid4").val("");
	$("#levelid5").val("");
	$("#levelid6").val("");
	$("#levelid7").val("");
	$("#levelid8").val("");
	$("#levelid9").val("");
	$("#levelid10").val("");

	var levellist;

	if( geographyLevelsList[countryval] != undefined ){
	levellist = geographyLevelsList[countryval]
    for(var entity in levellist) {
       var levelPosition = levellist[entity]["level_position"];
       var levelName = levellist[entity]["level_name"];
       var levelId = levellist[entity]["level_id"];
       $("#level"+levelPosition).val(levelName);
       $("#levelid"+levelPosition).val(levelId);
   }
  
   if(levellist.length < 10)
   	$("#add").show();
   else
   	$("#add").hide();
}
}

function saveRecord () { 
		$("#error").text("");
		var country = $("#country").val();
		if(country == '') {
			$("#error").text("Country Required");
		} else {
			 for(var k=1; k<=10; k++) {
					if($("#level"+k).val() != ''){
						var maxlevel = k;
					}
			   }
			   var result="true";
			   for(var k=1; k<=maxlevel; k++) {
					if($("#level"+k).val() == ''){
						result = "false";
					}
			   }

			   if( result == "true") {
			   	var passlevellist = [];
				for(var k=1; k<=10; k++) {
					if($("#level"+k).val() != ''){
						if($("#levelid"+k).val() != ''){
							passlevellist.push({"level_position" : k, "level_name" : $("#level"+k).val(), "level_id" : parseInt($("#levelid"+k).val())});
						}else{
							passlevellist.push({"level_position" : k, "level_name" : $("#level"+k).val()});
						}
					}
			   }
				function success(status,data) {
					if(status == 'success') {
						$("#error").text("Record Added Successfully");
						GetGeographyLevels();
					} else {
						$("#error").text(status);
					}
				}
				function failure(data){
				}
				mirror.saveAndUpdateGeographyLevels("SaveGeographyLevel", parseInt(country), passlevellist, success, failure);
			   }else{
			   	$("#error").text("Intermediate Level's should not be Empty");
			   }
			}
	}

	function insertRecord () { 
		var insertlevel = parseInt($("#insertlevel").val());
		var insertvalue = $("#insertvalue").val();
		for(var x=10; x >= insertlevel; x--){
       		var s = x-1;
       		if( x == insertlevel){
       			$("#level"+x).val(insertvalue);
       			$("#levelid"+x).val('');
       		}else{
       			$("#level"+x).val($("#level"+s).val());
       			$("#levelid"+x).val($("#levelid"+s).val());
       		}
		}
	}