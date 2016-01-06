var countriesList;
var domainsList;
var statutoryLevelsList;

$(".btn-statutorylevel-cancel").click(function(){
  $(".fieldvalue").val("");
  $(".hiddenvalue").val("");
  $("#countryval").val("");
  $("#country").val("");
  $("#domainval").val("");
  $("#domain").val("");
});

function GetStatutoryLevels(){
  function success(status,data){
    statutoryLevelsList = data["statutory_levels"];
    countriesList = data["countries"];
    domainsList = data["domains"];
  }
  function failure(data){
  }
  mirror.getStatutoryLevels(success, failure);
}

//Autocomplete Script Starts
//Hide list items after select
$(".hidemenu").click(function(){
  $("#autocompleteview").hide(); 
  $("#autocompleteview-domain").hide(); 
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
  loadstatutoryLevelsList();
}

//load domain list in autocomplete textbox  
$("#domainval").keyup(function(){
  var textval = $(this).val();
  $("#autocompleteview-domain").show(); 
  var domains = domainsList;
  var suggestions = [];
  $('#ulist_text_domain').empty();
  if(textval.length>0){
    for(var i in domains){
      if (~domains[i]["domain_name"].toLowerCase().indexOf(textval.toLowerCase()) && domains[i]["is_active"] == 1) suggestions.push([domains[i]["domain_id"],domains[i]["domain_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text_domain(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_text_domain').append(str);
    $("#domain").val('');
    }
});
//set selected autocomplte value to textbox
function activate_text_domain (element,checkval,checkname) {
  $("#domainval").val(checkname);
  $("#domain").val(checkval);
  loadstatutoryLevelsList();
}
//Autocomplete Script ends

function loadstatutoryLevelsList() {
  $(".error-message").html('');
  $(".fieldvalue").val("");
  $(".hiddenvalue").val("");
  var countryval = $("#country").val();
  var domainval = $("#domain").val();
  var levellist;
  if( statutoryLevelsList[countryval][domainval] != undefined ){
  levellist = statutoryLevelsList[countryval][domainval];
   for(var entity in levellist) {
       var levelPosition = levellist[entity]["level_position"];
       var levelName = levellist[entity]["level_name"];
       var levelId = levellist[entity]["level_id"];
       $("#level"+levelPosition).val(levelName);
       $("#levelid"+levelPosition).val(levelId);
   }
 }
}

function validate(){
    if($("#country").val().trim().length==0){
      $(".error-message").html("Country Required");
    } else if($("#domain").val().trim().length==0) {
      $(".error-message").text("Domain Required");
    }
    else {
      $(".error-message").html('');
      return true
    }
}

$("#submit").click(function(){ 
    $(".error-message").html('');
    var country = $("#country").val();
    var domain = $("#domain").val();
    if(validate()){
       for(var k=1; k<=10; k++) {
          if($("#level"+k).val().trim().length > 0){
            var maxlevel = k;
          }
         }
         var result="true";
         for(var k=1; k<=maxlevel; k++) {
          if($("#level"+k).val().trim().length==0){
            result = "false";
          }
         }

         if( result == "true") {
          var passlevellist = [];
         for(var k=1; k<=10; k++) {
          if($("#level"+k).val().trim().length > 0){
            if($("#levelid"+k).val().trim().length==0){
              passlevellist.push({"level_position" : k, "level_name" : $("#level"+k).val(), "level_id" : parseInt($("#levelid"+k).val())});
            }else{
              passlevellist.push({"level_position" : k, "level_name" : $("#level"+k).val()});
            }
          }
         }
        function success(status,data) {
          if(status == 'success') {
            $(".error-message").text("Record Added Successfully");
            GetStatutoryLevels();
          } else {
            $(".error-message").text(status);
          }
        }
        function failure(data){
          $(".error-message").text(status);
        }
        mirror.saveAndUpdateStatutoryLevels(parseInt(country), parseInt(domain), passlevellist, success, failure);
         }else{
          $(".error-message").text("Intermediate Level's should not be Empty");
         }
      }
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

$(document).ready(function(){
  GetStatutoryLevels();
});