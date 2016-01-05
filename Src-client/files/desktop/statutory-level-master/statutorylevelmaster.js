var countriesList;
var domainsList;
var statutoryLevelsList;

$(document).ready(function(){
  GetStatutoryLevels();
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
function hidemenu() {
  document.getElementById('autocompleteview').style.display = 'none';
  document.getElementById('autocompleteview-domain').style.display = 'none';
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
  loadstatutoryLevelsList();
}

//load domain list in autocomplete text box  
function loadauto_text_domain (textval) {
  document.getElementById('autocompleteview-domain').style.display = 'block';
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
}
//set selected autocomplte value to textbox
function activate_text_domain (element,checkval,checkname) {
  $("#domainval").val(checkname);
  $("#domain").val(checkval);
  loadstatutoryLevelsList();
}
//Autocomplete Script ends

function loadstatutoryLevelsList() {
  $("#error").text("");
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

function saveRecord () { 
    $("#error").text("");
    var country = $("#country").val();
    var domain = $("#domain").val();
    if(country == '') {
      $("#error").text("Country Required");
    } else if(domain == '') {
      $("#error").text("Domain Required");
    }
    else {
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
            GetStatutoryLevels();
          } else {
            $("#error").text(status);
          }
        }
        function failure(data){
        }
        mirror.saveAndUpdateStatutoryLevels(parseInt(country), parseInt(domain), passlevellist, success, failure);
         }else{
          $("#error").text("Intermediate Level's should not be Empty");
         }
      }
  }