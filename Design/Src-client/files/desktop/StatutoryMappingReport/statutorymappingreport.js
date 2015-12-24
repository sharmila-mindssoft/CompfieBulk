var statutoryMappingsList;
var geographyLevelsList;
var geographiesList;
var countriesList;
var domainsList;
var industriesList;
var statutoryNaturesList;
var statutoryLevelsList;
var statutoriesList;

$(function() {
  $(".grid-table-rpt").hide();
	getStatutoryMappings();
});
function getStatutoryMappings(){
  function success(status,data){
    industriesList = data["industries"];
    statutoriesList = data["level_1_statutories"];
    countriesList = data["countries"];
    domainsList = data["domains"];
    statutoryNaturesList = data["statutory_natures"];
    geographiesList = data["geographies"];
    //loadStatutoryMappingList(statutoryMappingsList);
  }
  function failure(data){
  }
  mirror.getStatutoryMappingsReportFilter(success, failure);
}

function showResult(){ 
  var country = $("#country").val();
  var domain = $("#domain").val();
  var industry = null;
  var statutorynature = null;
  var geography = null;
  var act = null;
  var compliance_frequency = $("#compliance_frequency").val();

  if($("#industry").val() != '') industry = $("#industry").val();
  if($("#statutorynature").val() != '') statutorynature = $("#statutorynature").val();
  if($("#geography").val() != '') geography = $("#geography").val();
  if($("#act").val() != '') act = $("#act").val();

  if(country==""){
    $(".error-message").html("Country Required");
  }
  else if(domain==""){
    $(".error-message").html("Domain Required");  
  }
  else{
    var filterdata={};
    filterdata["country_id"]=parseInt(country);
    filterdata["domain_id"]=parseInt(domain);
    filterdata["industry_id"]=parseInt(industry);
    filterdata["statutory_nature_id"]=parseInt(statutorynature);
    filterdata["geography_id"]=parseInt(geography);
    filterdata["level_1_statutory_id"]=parseInt(act);

    function success(status, data){
     loadresult(data["statutory_mappings"]);
    }
    function failure(status, data){
    }
    mirror.getStatutoryMappingsReportData(filterdata, success, failure);
  }
}

//Autocomplete Script Starts
//Hide list items after select
function hidemenu() {
  document.getElementById('autocompleteview').style.display = 'none';
  document.getElementById('autocomplete_domain').style.display = 'none';
  document.getElementById('autocomplete_industry').style.display = 'none';
  document.getElementById('autocomplete_statutorynature').style.display = 'none';
  document.getElementById('autocomplete_geography').style.display = 'none';
  document.getElementById('autocomplete_statutory').style.display = 'none';
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
}

//load domain list in autocomplete text box  
function loadauto_domain (textval) {
  document.getElementById('autocomplete_domain').style.display = 'block';
  var domains = domainsList;
  var suggestions = [];
  $('#ulist_text').empty();
  if(textval.length>0){
    for(var i in domains){
      if (~domains[i]["domain_name"].toLowerCase().indexOf(textval.toLowerCase()) && domains[i]["is_active"] == 1) suggestions.push([domains[i]["domain_id"],domains[i]["domain_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_domain(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_domain').append(str);
    $("#domain").val('');
    }
}
//set selected autocomplte value to textbox
function activate_domain (element,checkval,checkname) {
  $("#domainval").val(checkname);
  $("#domain").val(checkval);
}

//load domain list in autocomplete text box  
function loadauto_industry (textval) {
  document.getElementById('autocomplete_industry').style.display = 'block';
  var industries = industriesList;
  var suggestions = [];
  $('#ulist_text').empty();
  if(textval.length>0){
    for(var i in industries){
      if (~industries[i]["industry_name"].toLowerCase().indexOf(textval.toLowerCase()) && industries[i]["is_active"] == 1) suggestions.push([industries[i]["industry_id"],industries[i]["industry_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_industry(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_industry').append(str);
    $("#industry").val('');
    }
}
//set selected autocomplte value to textbox
function activate_industry (element,checkval,checkname) {
  $("#industryval").val(checkname);
  $("#industry").val(checkval);
}


//load statutorynature list in autocomplete text box  
function loadauto_statutorynature (textval) {
  document.getElementById('autocomplete_statutorynature').style.display = 'block';
  var statutorynatures = statutoryNaturesList;
  var suggestions = [];
  $('#ulist_statutorynature').empty();
  if(textval.length>0){
    for(var i in statutorynatures){
      if (~statutorynatures[i]["statutory_nature_name"].toLowerCase().indexOf(textval.toLowerCase()) && statutorynatures[i]["is_active"] == 1) suggestions.push([statutorynatures[i]["statutory_nature_id"],statutorynatures[i]["statutory_nature_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_statutorynature(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_statutorynature').append(str);
    $("#statutorynature").val('');
    }
}
//set selected autocomplte value to textbox
function activate_statutorynature (element,checkval,checkname) {
  $("#statutorynatureval").val(checkname);
  $("#statutorynature").val(checkval);
}

//load statutorynature list in autocomplete text box  
function loadauto_geography (textval) {
  document.getElementById('autocomplete_geography').style.display = 'block';
  var geographies = geographiesList[$("#country").val()];
  var suggestions = [];
  $('#ulist_geography').empty();
  if(textval.length>0){
    for(var i in geographies){

      if (~geographies[i]["geography_name"].toLowerCase().indexOf(textval.toLowerCase()) && geographies[i]["is_active"] == 1) suggestions.push([geographies[i]["geography_id"],geographies[i]["geography_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_geography(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_geography').append(str);
    $("#geography").val('');
    }
}
//set selected autocomplte value to textbox
function activate_geography (element,checkval,checkname) {
  $("#geographyval").val(checkname);
  $("#geography").val(checkval);
}

//load statutorynature list in autocomplete text box  
function loadauto_statutory (textval) {
  document.getElementById('autocomplete_statutory').style.display = 'block';
  var statutories = statutoriesList[$("#country").val()][$("#domain").val()];
  var suggestions = [];
  $('#ulist_statutory').empty();
  if(textval.length>0){
    for(var i in statutories){
      if (~statutories[i]["statutory_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([statutories[i]["statutory_id"],statutories[i]["statutory_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_statutory(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_statutory').append(str);
    $("#statutory").val('');
    }
}
//set selected autocomplte value to textbox
function activate_statutory (element,checkval,checkname) {
  $("#statutoryval").val(checkname);
  $("#statutory").val(checkval);
}
//Autocomplete Script ends
function loadresult(filterList){
  $(".grid-table-rpt").show();
  var country = $("#countryval").val();
  var domain = $("#domainval").val();
  var industry = $("#industry").val();
  var statutorynature = $("#statutorynature").val();
  var geography = $("#geography").val();
  var act = $("#act").val();
  var statutorynature = $("#statutorynature").val();
  var compliance_frequency = $("#compliance_frequency").val();
  $(".country").text(country);
  $(".domain").text(domain);

  $(".tbody-act").find("tr").remove();

  for(var entity in filterList){
    var tableRow=$('#act-templates');
    var clone=tableRow.clone();
    $('.actname', clone).text(entity);
    
    var snature='';
    /*for(var i=0; i<filterList[entity].length; i++){
      statutoryMappings = statutoryMappings + filterList[entity]["statutory_mappings"][i] + " <br>";
    }*/

    var tableRow1=$('#compliance-templates');
    var clone1=tableRow1.clone();
    $('.tbl_industrytype', clone1).text("industrytype");
    //$('.tbody-compliance').append(clone1);
    
    $('.tbody-act').append(clone);

  }
      /*for(var entity in geographiesList) {
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
        for(var countryList in countriesList){
          if(countriesList[countryList]["country_id"] == entity){
            countryName = countriesList[countryList]["country_name"];
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
        $('.country', clone).text(countryName);
        $('.level', clone).text(level);
        $('.name', clone).text(geographyName);
        $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+geographyId+',\''+geographyName+'\',\''+countryName+'\','+entity+','+lposition+','+parentid+')"/>');
        $('.status', clone).html('<img src=\'/images/'+imgName+'\' onclick="changeStatus('+geographyId+','+passStatus+')"/>');
        $('.tbody-geography-list').append(clone);
        j = j + 1;
        }
        }*/

}