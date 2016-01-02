var countriesList;
var geographyLevelsList;

$(".btn-geographylevel-cancel").click(function(){
	$(".fieldvalue").val("");
    $(".hiddenvalue").val("");
    $("#countryval").val("");
    $("#country").val("");
    $("#insertvalue").val("");
});

$(".add-insert-level").click(function(){  
     $("#view-insert-level").show();
     $("#add").hide();
});

$(".insert-level-cancel").click(function(){ 
     $("#view-insert-level").hide();
      $("#add").show();
});


function GetGeographyLevels(){
	function success(status,data){
		geographyLevelsList = data["geography_levels"];
		countriesList = data["countries"];
	}
	function failure(data){
	}
	mirror.getGeographyLevels(success, failure);
}

//Autocomplete Script Starts
//Hide list items after select
$(".hidemenu").click(function(){
  $("#autocompleteview").hide(); 
});

//load country list in autocomplete text box  
$("#countryval").keyup(function(){
  var textval = $(this).val();
  $("#autocompleteview").show();
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
});
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#countryval").val(checkname);
  $("#country").val(checkval);
  loadGeographyLevelsList(checkval);
}
//Autocomplete Script ends

function loadGeographyLevelsList(countryval) {
	$(".error-message").html('');
	$(".fieldvalue").val("");
	$(".hiddenvalue").val("");
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
function validate(){
    if($("#country").val().length==0){
      $(".error-message").html("Country Required");
    }
    else {
      $(".error-message").html('');
      return true
    }
}

$("#submit").click(function(){  
	var country = $("#country").val();
	if(validate()){
		for(var k=1; k<=10; k++) {
			if($("#level"+k).val() != ''){
				var maxlevel = k;
			}
		}
	    var result=true;
	    for(var k=1; k<=maxlevel; k++) {
	    	if($("#level"+k).val() == ''){
			result = false;
			}
		}

	  if(result) {
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
				$(".error-message").html("Record Added Successfully");
				$("#insertvalue").val("");
				GetGeographyLevels();
			} else {
				$(".error-message").html(status);
			}
		}
		function failure(data){
		}
		mirror.saveAndUpdateGeographyLevels(parseInt(country), passlevellist, success, failure);
	   }else{
	   $(".error-message").html("Intermediate Level's should not be Empty");
	   }
		}
});

$("#insert-record").click(function(){
	var insertlevel = parseInt($("#insertlevel").val());
	var insertvalue = $("#insertvalue").val();
	if(insertvalue != ''){
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
	   	$("#insertlevel").val("");
		$("#insertvalue").val("");
		$("#view-insert-level").hide();
	  	$("#add").show();
	}else{
		$(".error-message").html("Title should not be Empty");
	}
	for(var i=1; i <= 10; i++){
   		if( $("#level"+i).val() == ''){
   			$("#add").show();
   		}else{
   			$("#add").hide();
   		}
	   	}
});

$(document).ready(function(){
	GetGeographyLevels()
});

$(".fieldvalue").keyup(function (evt) {
 var element = $(evt.target);
 var tabIndex = element.attr('tabIndex');
 if (evt.keyCode == 13){
  if(tabIndex == 10){
    if(validate()){
      jQuery('#submit').focus().click();
    }
  }else{
    var nextElement = $("input[tabIndex=" + (parseInt(tabIndex) + 1) + "]");
     if (nextElement) {
         nextElement.focus();
     }
  return false;
  }
 }
});