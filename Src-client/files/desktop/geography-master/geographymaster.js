var countriesList;
var geographyLevelsList;
var geographiesList;

function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

$(".btn-geography-add").click(function(){
$("#geography-view").hide();
$("#geography-add").show();
$("#country").val('');
$("#countryval").val('');
$(".error-message").html('');
$(".tbody-geography-level").find("div").remove();
});

function GetGeographies(){
  function onSuccess(data){
    geographyLevelsList = data["geography_levels"];
    geographiesList = data["geographies"];
    countriesList = data["countries"];
    loadGeographiesList(geographiesList);
  }
  function onFailure(error){
    displayMessage(error);
  }
  mirror.getGeographies(
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

function loadGeographiesList(geographiesList) {
  var j = 1;
  var imgName = '';
  var passStatus = '';
  var geographyId = 0;
  var countryName = '';
  var isActive = false;
  var geographyName = '';

  $(".tbody-geography-list").find("tr").remove();
  for(var entity in geographiesList) {
    var geographyList = geographiesList[entity];
    for(var countryList in countriesList){
        if(countriesList[countryList]["country_id"] == entity){
          countryName = countriesList[countryList]["country_name"];
          break;
        }
      }
    for(var list in geographyList) {
      geographyId = geographyList[list]["geography_id"];
      geographyName = geographyList[list]["geography_name"];
      isActive = geographyList[list]["is_active"];
      var level = '';
      var lposition=0;
      var parentid = geographyList[list]["parent_id"];
      var geographyLevelList = geographyLevelsList[entity];
      for(var i in geographyLevelList){
        if(geographyLevelList[i]["level_id"] == geographyList[list]["level_id"]){
          level = geographyLevelList[i]["level_name"];
          lposition = geographyLevelList[i]["level_position"];
          break;
        }
      }
      if(isActive == true) {
        passStatus=false;
        imgName="icon-active.png"
      }
      else {
        passStatus=true;
        imgName="icon-inactive.png"
       }
      var tableRow=$('#templates .table-geography-master .table-row');
      var clone=tableRow.clone();
      $('.sno', clone).text(j);
      $('.country', clone).text(countryName);
      $('.level', clone).text(level);
      $('.name', clone).text(geographyName);
      $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+geographyId+',\''+geographyName+'\',\''+countryName+'\','+entity+','+lposition+','+parentid+')"/>');
      $('.status', clone).html('<img src=\'/images/'+imgName+'\' onclick="changeStatus('+geographyId+','+passStatus+')"/>');
      $('.tbody-geography-list').append(clone);
      j = j + 1;
    }
  }
}

function changeStatus (geographyId,isActive) {
  function onSuccess(response){
    GetGeographies();
    displayMessage("Status Changed Successfully");
  }
  function onFailure(error){
  }
  mirror.changeGeographyStatus(geographyId, isActive,
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
    }
});
//set selected autocomplte value to textbox
function activate_text (element,saverecord,checkname) {
  $("#countryval").val(checkname);
  $("#country").val(saverecord);
  loadGeographyFirstLevels(saverecord);
}
//Autocomplete Script ends

function loadGeographyFirstLevels(saverecord){
  $(".tbody-geography-level").find("div").remove();
  var geographyLevelList = geographyLevelsList[saverecord];
  var levelposition;
  for(var j in geographyLevelList){
    levelposition = geographyLevelList[j]["level_position"];
    var tableRow=$('#geography-level-templates');
    var clone=tableRow.clone();
    $('.title', clone).text(geographyLevelList[j]["level_name"]);
    $('.levelvalue', clone).html('<ul id="ulist'+levelposition+'"></ul><div align="center" class="bottomfield"><input type="text" maxlength="50" class="input-box addleft" placeholder=""  style="width:80%;" id="datavalue'+levelposition+'" onkeypress="saverecord('+levelposition+',event)"/><span> <a href="#" id="update'+levelposition+'"><img src="/images/icon-plus.png" formtarget="_self" onclick="saverecord('+levelposition+',\'clickimage\')" /></a></span></div><input type="hidden" id="glmid'+levelposition+'" value="'+geographyLevelList[j]["level_id"]+'"/><input type="hidden" id="level'+levelposition+'" value="'+levelposition+'" />');
    $('.tbody-geography-level').append(clone);
  }    
  var setlevelstage= 1;
  $('#datavalue'+setlevelstage).val('');
  $('#ulist'+setlevelstage).empty();
  var firstlevelid= $('#glmid'+setlevelstage).val();
  var str='';
  var idval='';
  var clsval='.list'+setlevelstage;
  var clsval1='list'+setlevelstage;
  var geographyList = geographiesList[saverecord];
  for(var i in geographyList){
    var setgeographyid = geographyList[i]["geography_id"];
    if((geographyList[i]["level_id"] == firstlevelid) && (geographyList[i]["is_active"] == true)){
    str += '<a href="#"> <li id="'+setgeographyid+'" class="'+clsval1+'" onclick="activate(this,'+setgeographyid+',\''+clsval+'\','+saverecord+','+setlevelstage+')" >'+geographyList[i]["geography_name"]+'</li> </a>';
  }
  }
  $('#ulist'+setlevelstage).append(str); 
}

//check & uncheck list data
function activate(element, id, type,country, level){
  $(type).each( function( index, el ) {
    $(el).removeClass( "active" );
      });
   $(element).addClass("active");
     load(id,level,country);
}

//load geographymapping sub level data dynamically
function load(id,level,country){
  var levelstages= parseInt(level) + 1;
  for(var k=levelstages;k<=10;k++){
    var setlevelstage= k;
    if($('#geographyid').val()==''){
      $('#datavalue'+setlevelstage).val('');
    }
    $('#ulist'+setlevelstage).empty();
    var str='';
    var idval='';
    var clsval='.list'+setlevelstage;
    var clsval1='list'+setlevelstage;
    var geographyLevelList = geographyLevelsList[country];
    var levelid=$('#glmid'+setlevelstage).val();
    var geographyList = geographiesList[country];
    for(var i in geographyList){
      var setgeographyid = geographyList[i]["geography_id"];
      if( id == geographyList[i]["parent_id"] && geographyList[i]["level_id"] == levelid && geographyList[i]["is_active"] == true) {
      str += '<a href="#"> <li id="'+setgeographyid+'" class="'+clsval1+'" onclick="activate(this,'+setgeographyid+',\''+clsval+'\','+country+','+setlevelstage+')" >'+geographyList[i]["geography_name"]+'</li> </a>';
    }
    }
    $('#ulist'+setlevelstage).append(str); 
  }
}

//filter process
function filter (term, cellNr){
  var filterkey = term.value.toLowerCase();
  var table = document.getElementById("tableToModify");
  var ele;
  for (var r = 1; r < table.rows.length; r++){
    ele = table.rows[r].cells[cellNr].innerHTML.replace(/<[^>]+>/g,"");
    if (ele.toLowerCase().indexOf(filterkey)>=0 )
      table.rows[r].style.display = '';
    else table.rows[r].style.display = 'none';
  }
} 

//validate and insert records in geograpahymapping table
function saverecord(j,e){
  var data = e.keyCode;
  if(data==13 || data ==undefined){
    displayMessage("");
    var levelstage = $('#level'+j).val();
    var glm_id = $('#glmid'+j).val();
    var datavalue = $('#datavalue'+j).val().trim();
    var map_gm_id=[];
    var last_geography_id=0;
    var last_level = 0;
    for(k=1;k<j;k++){
      $(".list"+k+".active").each( function( index, el ) {
        map_gm_id.push(parseInt(el.id));
        last_geography_id = el.id;
        last_level = k;
        });
    }
    if(map_gm_id==0 && levelstage>1 ){
      displayMessage("Level Selection Should not be Empty");
    }else if(datavalue.length == 0){
     displayMessage("Level-"+levelstage+" Value Should not be Empty");
    }else{
      function onSuccess(response){
        displayMessage("Record Added Successfully");
        $('#datavalue'+j).val('');
        reload(last_geography_id,last_level,$('#country').val());
      }
      function onFailure(error){
        if(error == 'GeographyNameAlreadyExists'){
            displayMessage("Geography Name Already Exists");
        }
      }
      if(map_gm_id.length == 0){
        map_gm_id.push(0);
      }
      mirror.saveGeography(parseInt(glm_id), datavalue, map_gm_id,
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
  }
}

function reload(last_geography_id,last_level,cny){

  function onSuccess(data){
    geographiesList = data["geographies"];
    load(last_geography_id,last_level,cny)
  }
  function onFailure(error){
    displayMessage(error);
  }
  mirror.getGeographies(
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

function displayEdit (geographyId,geographyName,country,countryid,lposition,parentidval) {
  $(".error-message").html("");
  $("#geography-view").hide();
  $("#geography-add").show();
  $("#geographyid").val(geographyId);
  $("#countryval").val(country);
  $("#country").val(countryid);
  $(".tbody-geography-level").find("div").remove();
  var geographyLevelList = geographyLevelsList[countryid];
  var levelposition;
  for(var j in geographyLevelList){
    levelposition = geographyLevelList[j]["level_position"];
    var tableRow=$('#geography-level-templates');
    var clone=tableRow.clone();
    $('.title', clone).text(geographyLevelList[j]["level_name"]);
    if(levelposition == lposition){
      $('.levelvalue', clone).html('<ul id="ulist'+levelposition+'"></ul><div align="center" class="bottomfield"><input type="text" maxlength="50" class="input-box addleft" placeholder=""  style="width:80%;" name="datavalue'+levelposition+'" id="datavalue'+levelposition+'" onkeypress="updaterecord('+levelposition+',event)"/><span> <a href="#" id="update'+levelposition+'"><img src="/images/icon-plus.png" formtarget="_self" onclick="updaterecord('+levelposition+',\'clickimage\')" /></a></span></div><input type="hidden" id="glmid'+levelposition+'" value="'+geographyLevelList[j]["level_id"]+'"/> <input type="hidden" id="visible'+levelposition+'" value=""/> <input type="hidden" id="level'+levelposition+'" value="'+levelposition+'" />');
    }else{
      $('.levelvalue', clone).html('<ul id="ulist'+levelposition+'"></ul><div align="center" class="bottomfield"><input type="text" readonly="readonly" class="input-box addleft" placeholder=""  style="width:80%;" name="datavalue'+levelposition+'" id="datavalue'+levelposition+'" onkeypress="saverecord('+levelposition+',event)"/><span> <img src="/images/icon-plus.png" formtarget="_self"/></span></div><input type="hidden" name="glmid'+levelposition+'" id="glmid'+levelposition+'" value="'+geographyLevelList[j]["level_id"]+'"/> <input type="hidden" name="visible'+levelposition+'" id="visible'+levelposition+'" value=""/> <input type="hidden" name="level'+levelposition+'" id="level'+levelposition+'" value="'+levelposition+'" />');
    }
    $('.tbody-geography-level').append(clone);
  }
  $('#datavalue'+lposition).val(geographyName);
  var levelstages= lposition-1;
  var parentid=parentidval;
  var parentid1=parentidval;
  var dispparentid=1;
  for(var k=levelstages;k>=1;k--){
    var setlevelstage= k;
    $('#datavalue'+setlevelstage).val('');
    $('#ulist'+setlevelstage).empty();
    var str='';
    var idval='';
    var clsval='.list'+setlevelstage;
    var clsval1='list'+setlevelstage;

    var geographyLevelList = geographyLevelsList[countryid];
    var levelid=$('#glmid'+setlevelstage).val();
    var geographyList = geographiesList[countryid];
   
    for(var i in geographyList){
      var setgeographyid = geographyList[i]["geography_id"];
      if( geographyList[i]["level_id"] == levelid && geographyList[i]["is_active"] == true) {
        if(parentid1 == geographyList[i]["geography_id"]){
          parentid1 = geographyList[i]["parent_id"];
          $('#visible'+setlevelstage).val(parentid1)
        }
    }
    }

    for(var i in geographyList){
      var setgeographyid = geographyList[i]["geography_id"];
      if( $('#visible'+setlevelstage).val() == geographyList[i]["parent_id"] && geographyList[i]["level_id"] == levelid && geographyList[i]["is_active"] == true) {
        if(parentid == geographyList[i]["geography_id"]){
          str += '<a href="#"> <li id="'+setgeographyid+'" class="'+clsval1+' active" onclick="activateedit(this,'+setgeographyid+',\''+clsval+'\','+countryid+','+setlevelstage+','+levelstages+')" >'+geographyList[i]["geography_name"]+'</li> </a>';
          parentid = geographyList[i]["parent_id"];
        }else{
          str += '<a href="#"> <li id="'+setgeographyid+'" class="'+clsval1+'" onclick="activateedit(this,'+setgeographyid+',\''+clsval+'\','+countryid+','+setlevelstage+','+levelstages+')" >'+geographyList[i]["geography_name"]+'</li> </a>';
        }
    }
  }
  $('#ulist'+setlevelstage).append(str); 
  }
}

function updaterecord(j,e){
  var data = e.keyCode;
  if(data==13 || data ==undefined){
    $(".error-message").html("");
    var levelstage = $('#level'+j).val();
    var glm_id = $('#glmid'+j).val();
    var geographyid = $('#geographyid').val();
    var datavalue = $('#datavalue'+j).val().trim();
    var map_gm_id=[];
    var last_geography_id=0;
    var last_level = 0;
    for(k=1;k<j;k++){
      $(".list"+k+".active").each( function( index, el ) {
        map_gm_id.push(parseInt(el.id));
        last_geography_id = el.id;
        last_level = k;
        });
    }
    if(map_gm_id==0 && levelstage>1 ){
      displayMessage("Level Selection Should not be Empty");
    }else if(datavalue.length == 0){
      displayMessage("Level-"+levelstage+" Value Should not be Empty");
    }else{
     function onSuccess(response){
          displayMessage("Record Update Successfully");
          GetGeographies();
          $("#geography-view").show();
          $("#geography-add").hide();
      }
      function onFailure(error) {
        if(error == 'GeographyNameAlreadyExists'){
            displayMessage("Geography Name Already Exists");
        }
        if(error == 'InvalidGeographyId'){
            displayMessage("Invalid Geography Id");
        }

      }
      if(map_gm_id.length == 0){
        map_gm_id.push(0);
      }
      mirror.updateGeography(parseInt(geographyid), parseInt(glm_id), datavalue, map_gm_id,
        function (error, response) {
          if (error == null){
            onSuccess(response);
          }
          else {
            onFailure(error);
          }
      });
    }
  }
}

//check & uncheck list data
function activateedit(element, id, type,country, level,levelstage){
  $(type).each( function( index, el ) {
    $(el).removeClass( "active" );
      });
   $(element).addClass("active");
     loadedit(id,level,country,levelstage);
}

//load geographymapping sub level data dynamically
function loadedit(id,level,country,levelstagemax){
  var levelstages= parseInt(level) + 1;
  for(var k=levelstages;k<=levelstagemax;k++){
  var setlevelstage= k;
  if($('#geographyid').val()==''){
    $('#datavalue'+setlevelstage).val('');
  }
  $('#ulist'+setlevelstage).empty();
  var str='';
  var idval='';
  var clsval='.list'+setlevelstage;
  var clsval1='list'+setlevelstage;
  var geographyLevelList = geographyLevelsList[country];
  var levelid=$('#glmid'+setlevelstage).val();
  var geographyList = geographiesList[country];
  for(var i in geographyList){
    var setgeographyid = geographyList[i]["geography_id"];
    if( id == geographyList[i]["parent_id"] && geographyList[i]["level_id"] == levelid && geographyList[i]["is_active"] == true) {
    str += '<a href="#"> <li id="'+setgeographyid+'" class="'+clsval1+'" onclick="activateedit(this,'+setgeographyid+',\''+clsval+'\','+country+','+setlevelstage+','+levelstagemax+')" >'+geographyList[i]["geography_name"]+'</li> </a>';
  }
  }
  $('#ulist'+setlevelstage).append(str); 
  }
}

$(document).ready(function(){
  GetGeographies();
});
