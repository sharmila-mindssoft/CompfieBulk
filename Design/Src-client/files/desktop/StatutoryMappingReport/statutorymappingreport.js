var statutoryMappingsList;
var geographyLevelsList;
var geographiesList;
var countriesList;
var domainsList;
var industriesList;
var statutoryNaturesList;
var statutoryLevelsList;
var statutoriesList;
var complianceFrequencyList;

$(function() {
  $(".grid-table-rpt").hide();
  getStatutoryMappings();


  //  Accordion Panels
    $(".accordion div").show();
    setTimeout("$('.accordion div').slideToggle('slow');", 10000);
    $(".accordion h3").click(function () {
        $(this).next(".pane").slideToggle("slow").siblings(".pane:visible").slideUp("slow");
        $(this).toggleClass("current");
        $(this).siblings("h3").removeClass("current");
    });

});
function getStatutoryMappings(){
  function success(status,data){
    industriesList = data["industries"];
    statutoriesList = data["level_1_statutories"];
    countriesList = data["countries"];
    domainsList = data["domains"];
    statutoryNaturesList = data["statutory_natures"];
    geographiesList = data["geographies"];
    complianceFrequencyList = data["compliance_frequency"];

    //load compliance frequency selectbox
    for (var compliancefrequency in complianceFrequencyList) {
    var option = $("<option></option>");
    option.val(complianceFrequencyList[compliancefrequency]["frequency_id"]);
    option.text(complianceFrequencyList[compliancefrequency]["frequency"]);
    $("#compliance_frequency").append(option);
    }
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
  var compliance_frequency = $("#compliance_frequency").val();
  $(".country").text(country);
  $(".domain").text(domain);

  $(".tbody-compliance").find("div").remove();
  var compliance_count=0;
  for(var entity in filterList){
    var actname = '';
    var display_occurance1=true;
    var display_occurance2=true;
    var display_occurance3=true;
    var display_occurance4=true;

    $.each(statutoriesList[$("#country").val()][$("#domain").val()], function(index, value) {
    if (value.statutory_id == entity) {
        actname = value.statutory_name;
    }
    });

    var tableRow=$('#act-templates');
    var clone=tableRow.clone();
    $('.actname', clone).html(actname);
    $('.tbody-compliance').append(clone);

    for(var j=0; j<complianceFrequencyList.length; j++){

      
    for(var i=0; i<filterList[entity].length; i++){
      for(var k=0; k<filterList[entity][i]["compliances"].length; k++){

      if((compliance_frequency == 'All' || compliance_frequency == filterList[entity][i]["compliances"][k]["frequency_id"]) ){
        var occurance = '';
        var occuranceid;
        $.each(complianceFrequencyList, function(index, value) {
        if (value.frequency_id == filterList[entity][i]["compliances"][k]["frequency_id"]) {
            occurance = value.frequency;
            occuranceid = value.frequency_id;
        }
        });
        if(occuranceid == 1 && (j+1)==1){

          if(display_occurance1){
            var tableRow2=$('#head-templates');
            var clone2=tableRow2.clone();
            $('.tbl_heading', clone2).html('<div class="heading" style="margin-top:5px;">'+occurance+'</div>');
            $('.tbody-compliance').append(clone2);
            display_occurance1 = false;}
        }
        if(occuranceid == 2 && (j+1)==2){

          if(display_occurance2){
            var tableRow2=$('#head-templates');
            var clone2=tableRow2.clone();
            $('.tbl_heading', clone2).html('<div class="heading" style="margin-top:5px;">'+occurance+'</div>');
            $('.tbody-compliance').append(clone2);
            display_occurance2 = false;}
        }
        if(occuranceid == 3 && (j+1)==3){

          if(display_occurance3){
            var tableRow2=$('#head-templates');
            var clone2=tableRow2.clone();
            $('.tbl_heading', clone2).html('<div class="heading" style="margin-top:5px;">'+occurance+'</div>');
            $('.tbody-compliance').append(clone2);
            display_occurance3 = false;}
        }
        if(occuranceid == 4 && (j+1)==4){

          if(display_occurance4){
            var tableRow2=$('#head-templates');
            var clone2=tableRow2.clone();
            $('.tbl_heading', clone2).html('<div class="heading" style="margin-top:5px;">'+occurance+'</div>');
            $('.tbody-compliance').append(clone2);
            display_occurance4 = false;}
        }

        if(occuranceid == 1 && (j+1)==1 || occuranceid == 2 && (j+1)==2 || occuranceid == 3 && (j+1)==3 || occuranceid == 4 && (j+1)==4){

          var tableRow1=$('#compliance-templates');
          var clone1=tableRow1.clone();
          $('.tbody-compliance').append(clone1);
          $('.tbl_sno', clone1).text(compliance_count+1);
          $('.tbl_industrytype', clone1).text(filterList[entity][i]["industry_names"]);
          $('.tbl_statutorynature',   clone1).text(filterList[entity][i]["statutory_nature_name"]);
          $('.tbl_statutoryprovision', clone1).text(filterList[entity][i]["compliances"][k]["statutory_provision"]);
          $('.tbl_compliancetask', clone1).text(filterList[entity][i]["compliance_names"][k]);
          $('.tbl_description', clone1).text(filterList[entity][i]["compliances"][k]["description"]);
          $('.tbl_penalconsequences', clone1).text(filterList[entity][i]["compliances"][k]["penal_consequences"]);
          $('.tbl_occurance', clone1).text(occurance);
          $('.tbl_applicablelocation', clone1).text(filterList[entity][i]["geography_mappings"]);
          $('.tbody-compliance').append(clone1);
          compliance_count = compliance_count + 1;
        } 
      }
      }
    }
    }
  }  
  $('.compliance_count').text("Total : "+ (compliance_count) +" records");
}