var countriesList;
var geographyLevelsList;

$(".btn-geographylevel-cancel").click(function(){
	$(".fieldvalue").val("");
    $(".hiddenvalue").val("");
    $("#countryval").val("");
    $("#country").val("");
    $("#insertvalue").val("");
    $("#view-insert-level").hide();
  	$("#add").show();
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
	function onSuccess(data){
		geographyLevelsList = data["geography_levels"];
		countriesList = data["countries"];
	}
	function onFailure(error){
		displayMessage(error);
	}
	mirror.getGeographyLevels(
    function (error, response) {
        if (error == null){
          onSuccess(response);
        }
        else {
          onFailure(error);
        }
    }
);
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
      if (~countries[i]["country_name"].toLowerCase().indexOf(textval.toLowerCase()) && countries[i]["is_active"] == true) suggestions.push([countries[i]["country_id"],countries[i]["country_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_text').append(str);
    $("#country").val('');
    }else{
    	$("#country").val('');
    	$("#autocompleteview").hide();
    }
});
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#countryval").val(checkname);
  $("#country").val(checkval);
  $("#view-insert-level").hide();
  $("#add").show();
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
		   var levelPosition = levellist[entity]["l_position"];
		   var levelName = levellist[entity]["l_name"];
		   var levelId = levellist[entity]["l_id"];
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
    if($("#country").val().trim().length==0){
      displayMessage(message.country_required);
    }else if($("#level1").val().trim().length==0){
      displayMessage(message.levelone_title_required);
    }
    else {
      displayMessage('');
      return true
    }
}

$("#submit").click(function(){  
	var country = $("#country").val();
	if(validate()){
		for(var k=1; k<=10; k++) {
			if($("#level"+k).val().trim().length > 0){
				var maxlevel = k;
			}
		}
	    var result=true;
	    for(var k=1; k<=maxlevel; k++) {
	    	if($("#level"+k).val().trim().length==0){
			result = false;
			}
		}

	  if(result) {
	   	var passlevellist = [];
	   	var isAdd = true;
		for(var k=1; k<=10; k++) {
			if($("#levelid"+k).val() != '' && $("#level"+k).val().trim() == ''){
				displayMessage("Geography Level "+ k + " Should not be Empty")
				return false;
			}else if($("#level"+k).val().trim() != ''){
				if($("#levelid"+k).val() != ''){
					passlevellist.push({"l_position" : k, "l_name" : $("#level"+k).val().trim(), "l_id" : parseInt($("#levelid"+k).val())});
					isAdd = false;
				}else{
					passlevellist.push({"l_position" : k, "l_name" : $("#level"+k).val().trim(), "l_id" : null });
				}
			}
	   }
		function onSuccess(response) {
			if(isAdd){
				displayMessage(message.record_added);
			}else{
				displayMessage(message.record_updated);
			}
			
			jQuery('.btn-geographylevel-cancel').focus().click();
			GetGeographyLevels();			
		}
		function onFailure(error){             
          if(error == "DuplicateGeographyLevelsExists"){
            displayMessage(message.geographylevel_exists);
          }
        }
		mirror.saveAndUpdateGeographyLevels(parseInt(country), passlevellist, 
			function (error, response) {
            if (error == null){
              onSuccess(response);
            }
            else {
              onFailure(error);
            }
          });
	   }else{
	   		displayMessage(message.intermediatelevel_required);
	   }
		}
});

$("#insert-record").click(function(){
	var insertlevel = parseInt($("#insertlevel").val());
	var insertvalue = $("#insertvalue").val().trim();
	var inserlevelstatus = true;
	if(insertvalue.length > 0){
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
	   	$("#insertlevel").val("2");
		$("#insertvalue").val("");
		$("#view-insert-level").hide();
	  	$("#add").show();
	  	displayMessage("");
	}else{
		displayMessage(message.title_required);
		$("#add").hide();
		inserlevelstatus = false;
	}

	for(var i=1; i <= 10; i++){
   		if( $("#level"+i).val() == ''){
   			$("#add").show();
   		}else{
   			$("#add").hide();
   		}
	}

	if(inserlevelstatus == false) $("#add").hide();
});

$(document).ready(function(){
	GetGeographyLevels()
	$("#countryval").focus();
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