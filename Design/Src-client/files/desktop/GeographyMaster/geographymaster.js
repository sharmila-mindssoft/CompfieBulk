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
        $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+geographyId+',\''+geographyName+'\',\''+country+'\','+entity+','+lposition+','+parentid+')"/>');
        $('.status', clone).html('<img src=\'/images/'+imgName+'\' onclick="changeStatus('+geographyId+','+passStatus+')"/>');
        $('.tbody-geography-list').append(clone);
        j = j + 1;
        }
      	}
      }

  function changeStatus (geographyId,isActive) {
    mirror.changeGeographyStatus("ChangeGeographyStatus", geographyId, isActive, success, failure);
    function success(status,data){
      if(status == "success"){
            GetGeographies();
            $("#error").text("Status Changed Successfully");
          }else{
            $("#error").text(status)
          }
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

function loadGeographyFirstLevels(checkval){
    $('#geography-level-templates').each(function (i) {
    $('[id="' + this.id + '"]:gt(0)').remove();
  });
  var geographyLevelList = geographyLevelsList[checkval];
  var levelposition;
    for(var j in geographyLevelList){
      levelposition = geographyLevelList[j]["level_position"];
      var tableRow=$('#geography-level-templates');
      var clone=tableRow.clone();
      $('.title', clone).text(geographyLevelList[j]["level_name"]);
      $('.levelvalue', clone).html('<ul id="ulist'+levelposition+'"></ul><div align="center" class="bottomfield"><input type="text" class="input-box addleft" placeholder=""  style="width:80%;" name="datavalue'+levelposition+'" id="datavalue'+levelposition+'" onkeypress="checkval('+levelposition+',event)"/><span> <a href="#" id="update'+levelposition+'"><img src="/images/icon-plus.png" formtarget="_self" onclick="checkval('+levelposition+',\'clickimage\')" /></a></span></div><input type="hidden" name="glmid'+levelposition+'" id="glmid'+levelposition+'" value="'+geographyLevelList[j]["level_id"]+'"/><input type="hidden" name="level'+levelposition+'" id="level'+levelposition+'" value="'+levelposition+'" />');
      $('.tbody-geography-level').append(clone);
    }
    //$('#geography-level-templates').eq(0).remove();
    
    var setlevelstage= 1;
    $('#datavalue'+setlevelstage).val('');
    $('#ulist'+setlevelstage).empty();
    var firstlevelid= $('#glmid'+setlevelstage).val();

    var str='';
    var idval='';
    var clsval='.list'+setlevelstage;
    var clsval1='list'+setlevelstage;

    var geographyList = geographiesList[checkval];
    for(var i in geographyList){
      var setgeographyid = geographyList[i]["geography_id"];
      if((geographyList[i]["level_id"] == firstlevelid) && (geographyList[i]["is_active"] == 1)){
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
              if( id == geographyList[i]["parent_id"] && geographyList[i]["level_id"] == levelid && geographyList[i]["is_active"] == 1) {
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
  function checkval(j,e){
      var data = e.keyCode;
      if(data==13 || data ==undefined){
      $("#error").text("");
      var levelstage = $('#level'+j).val();
      var glm_id = $('#glmid'+j).val();
      var datavalue = $('#datavalue'+j).val();
      var map_gm_id=[];
      var last_geography_id=0;
      var last_level = 0;
      for(k=1;k<j;k++){
        $(".list"+k+".active").each( function( index, el ) {
          map_gm_id.push(el.id);
          last_geography_id = el.id;
          last_level = k;
          });
      }
      if(map_gm_id==0 && levelstage>1 ){
        $("#error").text("Level Selection Should not be Empty");
      }else if(datavalue==""){
        $("#error").text("Level-"+levelstage+" Value Should not be Empty");
      }else{
        function success(status,data){
          if(status == "success"){
            $("#error").text("Record Added Successfully");
            GetGeographies();
            load(last_geography_id,"type",last_level,$('#country').val());
          }else{
            $("#error").text(status)
          }
        }
        function failure(data){
        }
        if(map_gm_id.length == 0){
          map_gm_id.push(0);
        }
        mirror.saveGeography("SaveGeography", parseInt(glm_id), datavalue, map_gm_id, success, failure);
}
}}

function displayEdit (geographyId,geographyName,country,countryid,lposition,parentidval) {
    $("#error").text("");
    $("#listview").hide();
    $("#addview").show();
    $("#geographyid").val(geographyId);
    $("#countryval").val(country);
    $("#country").val(countryid);
    $('#geography-level-templates').each(function (i) {
    $('[id="' + this.id + '"]:gt(0)').remove();
  });
  var geographyLevelList = geographyLevelsList[countryid];
  var levelposition;
    for(var j in geographyLevelList){
      levelposition = geographyLevelList[j]["level_position"];
      var tableRow=$('#geography-level-templates');
      var clone=tableRow.clone();
      $('.title', clone).text(geographyLevelList[j]["level_name"]);
      if(levelposition == lposition){
        $('.levelvalue', clone).html('<ul id="ulist'+levelposition+'"></ul><div align="center" class="bottomfield"><input type="text" class="input-box addleft" placeholder=""  style="width:80%;" name="datavalue'+levelposition+'" id="datavalue'+levelposition+'" onkeypress="editcheckval('+levelposition+',event)"/><span> <a href="#" id="update'+levelposition+'"><img src="/images/icon-plus.png" formtarget="_self" onclick="editcheckval('+levelposition+',\'clickimage\')" /></a></span></div><input type="hidden" name="glmid'+levelposition+'" id="glmid'+levelposition+'" value="'+geographyLevelList[j]["level_id"]+'"/> <input type="hidden" name="visible'+levelposition+'" id="visible'+levelposition+'" value=""/> <input type="hidden" name="level'+levelposition+'" id="level'+levelposition+'" value="'+levelposition+'" />');
      }else{
        $('.levelvalue', clone).html('<ul id="ulist'+levelposition+'"></ul><div align="center" class="bottomfield"><input type="text" readonly="readonly" class="input-box addleft" placeholder=""  style="width:80%;" name="datavalue'+levelposition+'" id="datavalue'+levelposition+'" onkeypress="checkval('+levelposition+',event)"/><span> <img src="/images/icon-plus.png" formtarget="_self"/></span></div><input type="hidden" name="glmid'+levelposition+'" id="glmid'+levelposition+'" value="'+geographyLevelList[j]["level_id"]+'"/> <input type="hidden" name="visible'+levelposition+'" id="visible'+levelposition+'" value=""/> <input type="hidden" name="level'+levelposition+'" id="level'+levelposition+'" value="'+levelposition+'" />');
      }
      $('.tbody-geography-level').append(clone);
    }
      //$('#geography-level-templates').eq(0).remove();
      $('#datavalue'+lposition).val(geographyName);
      var levelstages= lposition-1;
      var parentid=parentidval;
      var parentid1=parentidval;

      var dispparentid=1;
      for(var k=levelstages;k>=1;k--){
      var setlevelstage= k;
      //$('#datavalue'+setlevelstage).val('');
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
        if( geographyList[i]["level_id"] == levelid && geographyList[i]["is_active"] == 1) {
          if(parentid1 == geographyList[i]["geography_id"]){
            parentid1 = geographyList[i]["parent_id"];
            $('#visible'+setlevelstage).val(parentid1)
          }
      }
      }

      for(var i in geographyList){
        var setgeographyid = geographyList[i]["geography_id"];
        if( $('#visible'+setlevelstage).val() == geographyList[i]["parent_id"] && geographyList[i]["level_id"] == levelid && geographyList[i]["is_active"] == 1) {
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


  function editcheckval(j,e){
      var data = e.keyCode;
      if(data==13 || data ==undefined){
      $("#error").text("");
      var levelstage = $('#level'+j).val();
      var glm_id = $('#glmid'+j).val();
      var geographyid = $('#geographyid').val();
      var datavalue = $('#datavalue'+j).val();
      var map_gm_id=[];
      var last_geography_id=0;
      var last_level = 0;
      for(k=1;k<j;k++){
        $(".list"+k+".active").each( function( index, el ) {
          map_gm_id.push(el.id);
          last_geography_id = el.id;
          last_level = k;
          });
      }
      if(map_gm_id==0 && levelstage>1 ){
        $("#error").text("Level Selection Should not be Empty");
      }else if(datavalue==""){
        $("#error").text("Level-"+levelstage+" Value Should not be Empty");
      }else{
       function success(status,data){
          if(status == "success"){
            $("#error").text("Record Update Successfully");
            GetGeographies();
            $("#listview").show();
            $("#addview").hide();
          }else{
            $("#error").text(status)
          }
        }
        function failure(data){
        }
        if(map_gm_id.length == 0){
          map_gm_id.push(0);
        }
        mirror.updateGeography("UpdateGeography", parseInt(geographyid), parseInt(glm_id), datavalue, map_gm_id, success, failure);
}
}}

//check & uncheck list data
function activateedit(element, id, type,country, level,levelstage){
  $(type).each( function( index, el ) {
    $(el).removeClass( "active" );
      });
   $(element).addClass("active");
     loadedit(id,type,level,country,levelstage);
  }

//load geographymapping sub level data dynamically
function loadedit(id,type,level,country,levelstagemax){
  alert(levelstagemax);
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
              if( id == geographyList[i]["parent_id"] && geographyList[i]["level_id"] == levelid && geographyList[i]["is_active"] == 1) {
              str += '<a href="#"> <li id="'+setgeographyid+'" class="'+clsval1+'" onclick="activateedit(this,'+setgeographyid+',\''+clsval+'\','+country+','+setlevelstage+','+levelstagemax+')" >'+geographyList[i]["geography_name"]+'</li> </a>';
            }
            }
          $('#ulist'+setlevelstage).append(str); 
        
          }
    }