var countriesList;
var geographyLevelsList;
var geographiesList;
var tempGeographiesList;

$(document).ready(function(){
	GetGeographies();
});

function GetGeographies(){
	function success(status,data){
		geographyLevelsList = data["geography_levels"];
		geographiesList = data["geographies"];
		tempGeographiesList = data["geographies"];
		countriesList = data["countries"];
		loadGeographiesList(geographiesList);
	}
	function failure(data){
	}
	mirror.getGeographies("GetGeographies", success, failure);
}
function loadGeographiesList(geographiesList) {
	var j = 1;
	var imgName = '';
  var passStatus = '';
  var geographyId = 0;
  var countryName = '';
  var isActive = 0;
  var geographyName = '';

   $(".tbody-geography-list").find("tr").remove();
    for(var entity in geographiesList) {
      var geographyList = geographiesList[entity];
      for(var list in geographyList) {
        geographyId = geographyList[list]["geography_id"];
        geographyName = geographyList[list]["geography_name"];
        isActive = geographyList[list]["is_active"];
        var level = '';
        var geographyLevelList = geographyLevelsList[entity];
        for(var i in geographyLevelList){
          if(geographyLevelList[i]["level_id"] == geographyList[list]["level_id"]){
            level = geographyLevelList[i]["level_name"];
            break;
          }
        }
        var country = '';        
        for(var countryList in countriesList){
          if(countriesList[countryList]["country_id"] == entity){
            country = countriesList[countryList]["country_name"];
            break;
          }
        }
        if(isActive == 1) {
          passStatus="0";
          imgName="icon-active.png"
        }
        else {
          passStatus="1";
          imgName="icon-inactive.png"
         }
        var tableRow=$('#templates .table-geography-master .table-row');
        var clone=tableRow.clone();
        $('.sno', clone).text(j);
        $('.country', clone).text(country);
        $('.level', clone).text(level);
        $('.name', clone).text(geographyName);
        $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+geographyId+',\''+geographyName+'\')"/>');
        $('.status', clone).html('<img src=\'/images/'+imgName+'\' onclick="changeStatus('+geographyId+','+passStatus+')"/>');
        $('.tbody-geography-list').append(clone);
        j = j + 1;
        }
      	}
      }

  function changeStatus (geographyId,isActive) {
    mirror.changeGeographyStatus("ChangeGeographyStatus", geographyId, isActive, success, failure);
    function success(status,data){
      GetGeographies();
      $("#error").text("Status Changed Successfully");
    }
    function failure(data){
    }
  }

function displayAdd () {
      $("#listview").hide();
      $("#addview").show();
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
      if (~countries[i]["country_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([countries[i]["country_id"],countries[i]["country_name"]]); 
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

function loadGeographyFirstLevels(checkval){
    $('#geography-level-templates').each(function (i) {
    $('[id="' + this.id + '"]:gt(0)').remove();
  });
  var geographyLevelList = geographyLevelsList[checkval];
   var levelposition;
   var firstlevelid=0;
    for(var j in geographyLevelList){
      levelposition = geographyLevelList[j]["level_position"];

      if(levelposition == 1){
        firstlevelid = geographyLevelList[j]["level_id"];
      }
      var tableRow=$('#geography-level-templates');
      var clone=tableRow.clone();
      $('.title', clone).text(geographyLevelList[j]["level_name"]);
      $('.levelvalue', clone).html('<ul id="ulist'+levelposition+'"></ul><div align="center" class="bottomfield"><input type="text" class="input-box addleft" placeholder=""  style="width:80%;" name="datavalue'+levelposition+'" id="datavalue'+levelposition+'" onkeypress="checkval('+levelposition+',event)"/><span> <a href="#" id="update'+levelposition+'"><img src="/images/icon-plus.png" formtarget="_self" onclick="checkval('+levelposition+',"\"clickimage\"")" /></a></span></div><input type="hidden" name="glmid'+levelposition+'" id="glmid'+levelposition+'" value="'+geographyLevelList[j]["level_id"]+'"/><input type="hidden" name="level'+levelposition+'" id="level'+levelposition+'" value="'+levelposition+'" />');
      $('.tbody-geography-level').append(clone);

    }
    //$('#geography-level-templates').eq(0).remove();
    
    var setlevelstage= 1;
    $('#datavalue'+setlevelstage).val('');
    $('#ulist'+setlevelstage).empty();

    var str='';
    var idval='';
    var clsval='.list'+setlevelstage;
    var clsval1='list'+setlevelstage;

    var geographyList = geographiesList[checkval];
    for(var i in geographyList){
      var setgeographyid = geographyList[i]["geography_id"];
      if(geographyList[i]["level_id"] == firstlevelid){
      str += '<a href="#"> <li id="'+setgeographyid+'" class="'+clsval1+'" onclick="activate(this,'+setgeographyid+',\''+clsval+'\','+checkval+','+setlevelstage+')" >'+geographyList[i]["geography_name"]+'</li> </a>';
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
     load(id,type,level,country);
  }

//load geographymapping sub level data dynamically
function load(id,type,level,country){
 /*   jQuery.ajax({
          url: "/geographymapping/load",
          type: "post",
          dataType: 'json',
          cache : false,
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify( {"data": {"id" : id }} ),
          success: function(msg) {
          var levelstages= parseInt(level) + 1;
          for(var k=levelstages;k<=10;k++){
          var setlevelstage= k;
          $('#datavalue'+setlevelstage).val('');
          $('#ulist'+setlevelstage).empty();
          var list = JSON.parse(msg);
          var str='';
          var idval='';
          var clsval='.list'+setlevelstage;
          var clsval1='list'+setlevelstage;
          for(var i in list){
            //idval=list[i].toString().split(',');
            if(list[i][1] == setlevelstage){
            str += '<a href="#"> <li id="'+i+'" class="'+clsval1+'" onclick="activate(this,'+i+',\''+clsval+'\','+setlevelstage+')" >'+list[i][0]+'</li> </a>';
          }
          }
          $('#ulist'+setlevelstage).append(str); 
        
          }
        }
      });*/
          var levelstages= parseInt(level) + 1;
          for(var k=levelstages;k<=10;k++){
          var setlevelstage= k;
          $('#datavalue'+setlevelstage).val('');
          $('#ulist'+setlevelstage).empty();
        
          var str='';
          var idval='';
          var clsval='.list'+setlevelstage;
          var clsval1='list'+setlevelstage;

          var geographyLevelList = geographyLevelsList[country];
          var levelid=0;
          for(var j in geographyLevelList){
            levelposition = geographyLevelList[j]["level_position"];
            if(levelposition == setlevelstage){
              levelid = geographyLevelList[j]["level_id"];
            }
          }

          var geographyList = geographiesList[country];
            for(var i in geographyList){
              var setgeographyid = geographyList[i]["geography_id"];
              if( (id in geographyList[i]["parent_ids"] || id == geographyList[i]["parent_ids"]) && geographyList[i]["level_id"] == levelid) {
              str += '<a href="#"> <li id="'+setgeographyid+'" class="'+clsval1+'" onclick="activate(this,'+setgeographyid+',\''+clsval+'\','+country+','+setlevelstage+')" >'+geographyList[i]["geography_name"]+'</li> </a>';
            }
            }
          $('#ulist'+setlevelstage).append(str); 
        
          }
    }

  //filter process
  function filter (){
    /*var countryfilter = $("#countryfilter").val().toLowerCase();
    var levelfilter = $("#levelfilter").val().toLowerCase();
    var namefilter = $("#namefilter").val().toLowerCase();
    var filteredList=[];
    for(var entity in tempGeographiesList) {
      var geographyList = tempGeographiesList[entity];
      for(var list in geographyList) {
        geographyName = geographyList[list]["geography_name"];
        geographyId = geographyList[list]["geography_id"];
        isActive = geographyList[list]["is_active"];
        var level = '';
        var levelId= '';
        var geographyLevelList = geographyLevelsList[entity];
        for(var i in geographyLevelList){
          if(geographyLevelList[i]["level_id"] == geographyList[list]["level_id"]){
            level = geographyLevelList[i]["level_name"];
            levelId = geographyLevelList[i]["level_id"];
            break;
          }
        }
        var countryName = '';        
        for(var countryList in countriesList){
          if(countriesList[countryList]["country_id"] == entity){
            countryName = countriesList[countryList]["country_name"];
            break;
          }
        }
         if (~geographyName.toLowerCase().indexOf(namefilter) && ~level.toLowerCase().indexOf(levelfilter) && ~countryName.toLowerCase().indexOf(countryfilter)) 
        {
          filteredList.push({entity : {"geography_id": geographyId,"level_id": levelId,"is_active": isActive,"geography_name": geographyName}});
        }  
        }
        }
        loadGeographiesList(filteredList);*/
  } 