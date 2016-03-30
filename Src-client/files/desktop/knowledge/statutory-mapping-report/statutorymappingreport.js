var statutoryMappingDataList;
var geographiesList;
var countriesList;
var domainsList;
var industriesList;
var statutoryNaturesList;
var statutoriesList;
var complianceFrequencyList;
var temp_act = null;

var finalList;
var pageSize;
var startCount;
var endCount;

var count=1;
var compliance_count=0;
var lastActName = '';
var lastOccuranceid = 0;

function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
}

function getStatutoryMappings(){
  function onSuccess(data){
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
  function onFailure(error){
    displayMessage(error);
  }
  mirror.getStatutoryMappingsReportFilter(
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

function loadCountwiseResult(filterList){

  if(startCount <= 0){
    $(".grid-table-rpt").show();
    var country = $("#countryval").val();
    var domain = $("#domainval").val();
    var compliance_frequency = $("#compliance_frequency").val();
    $(".country").text(country);
    $(".domain").text(domain);
    $(".tbody-compliance").find("tbody").remove();
    count=1;
    compliance_count=0;
    lastActName = '';
    lastOccuranceid = 0;
  }

  for(var entity in filterList){
    var actname = filterList[entity]["act_name"];
    var frequency_id = filterList[entity]["frequency_id"];
    var industry_names = filterList[entity]["industry_names"];
    var statutory_nature_name = filterList[entity]["statutory_nature_name"];
    var statutory_provision = filterList[entity]["statutory_provision"];
    var compliance_name = filterList[entity]["compliance_task"];
    var download_url = filterList[entity]["url"];
    console.log(frequency_id)

    if(actname != lastActName){
      var tableRow=$('#act-templates .table-act-list .table-row-act-list');
      var clone=tableRow.clone();
      $('.actname', clone).html(actname +'<span><img src="/images/chevron_black_down.png"></span>');
      $('.tbody-compliance').append(clone);
      $('.tbody-compliance').append('<tbody class="accordion-content accordion-content'+count+' default"></tbody>');
      /*if(count==1){
        $('.accordion-content'+count).addClass("default");
      }*/
      lastOccuranceid = 0;
      count++;
    }

    var occurance = '';
    var occuranceid;
    if(frequency_id != lastOccuranceid){
      $.each(complianceFrequencyList, function(index, value) {
      if (value.frequency_id == frequency_id) {
        occurance = value.frequency;
        occuranceid = value.frequency_id;
      }
      });
      var tableRow2=$('#head-templates .table-compliance-frequency-list .table-row-com-frequency');
      var clone2=tableRow2.clone();
      $('.tbl_heading', clone2).html('<div class="heading" style="margin-top:5px;width:150px;">'+occurance+'</div>');
      $('.accordion-content'+(count-1)).append(clone2);
    }

    var tableRow1=$('#compliance-templates .table-compliances-list .table-row');
    var clone1=tableRow1.clone();
    $('.tbody-compliance').append(clone1);
    $('.tbl_sno', clone1).text(compliance_count+1);
    $('.tbl_industrytype', clone1).text(industry_names);
    $('.tbl_statutorynature',   clone1).text(statutory_nature_name);
    $('.tbl_statutoryprovision', clone1).text(statutory_provision);
    if(download_url == null){
      $('.tbl_compliancetask', clone1).html(compliance_name);
    }else{
      $('.tbl_compliancetask', clone1).html('<a href= "'+ download_url +'" target="_new">'+compliance_name+'</a>');
    }

    var sdateDesc = '';
    var duration = filterList[entity]["duration"];
    var duration_type_id = filterList[entity]["duration_type_id"];
    var repeats_every = filterList[entity]["repeats_every"];
    var repeats_type_id = filterList[entity]["repeats_type_id"];
    var statutory_date =  filterList[entity]["statutory_dates"];
    var statutorydate = '';
    var duration_type = '';
    var repeats_type = '';
    if(frequency_id == 4){
      if(duration_type_id == 1){
        duration_type = 'Day(s)';
      }else{
        duration_type = 'Hour(s)';
      }
      sdateDesc = 'To complete with in ' +duration + ' ' + duration_type;
    }
    else if(frequency_id == 1){
      sdateDesc = '';
    }
    else{
      if(repeats_type_id == 1){
        repeats_type = 'Day(s)';
      }else if(repeats_type_id == 2){
        repeats_type = 'Month(s)';
      }else{
        repeats_type = 'Year(s)';
      }
      sdateDesc = 'Every ' + repeats_every + ' ' + repeats_type;
    }

    if(frequency_id != 4){
      for(z = 0; z < statutory_date.length; z++){
      var sDay = '';
      if(statutory_date[z]["statutory_date"] != null) sDay = statutory_date[z]["statutory_date"];

      var sMonth = '';
      if(statutory_date[z]["statutory_month"] != null) sMonth = statutory_date[z]["statutory_month"];

      if(sMonth == 1) sMonth = "January"
      else if(sMonth == 2) sMonth = "February"
      else if(sMonth == 3) sMonth = "March"
      else if(sMonth == 4) sMonth = "April"
      else if(sMonth == 5) sMonth = "May"
      else if(sMonth == 6) sMonth = "June"
      else if(sMonth == 7) sMonth = "July"
      else if(sMonth == 8) sMonth = "Auguest"
      else if(sMonth == 9) sMonth = "September"
      else if(sMonth == 10) sMonth = "October"
      else if(sMonth == 11) sMonth = "November"
      else if(sMonth == 12) sMonth = "December"
      statutorydate +=  sMonth +' '+ sDay +' ';
      if(statutorydate.trim() != '') statutorydate += ', ';

      }
      if(statutorydate.trim() != ''){
        statutorydate = statutorydate.replace(/,\s*$/, "");
        if(sdateDesc == ''){
          statutorydate = statutorydate;
        }else{
          statutorydate = sdateDesc + ' ( '+statutorydate+' )';
        } 
      }
    }else{
      statutorydate = sdateDesc;
    }
    $('.tbl_description', clone1).text(filterList[entity]["description"]);
    $('.tbl_penalconsequences', clone1).text(filterList[entity]["penal_consequences"]);
    $('.tbl_occurance', clone1).text(statutorydate);
    $('.tbl_applicablelocation', clone1).text(filterList[entity]["geography_mappings"]);
    $('.accordion-content'+(count-1)).append(clone1);

    compliance_count = compliance_count + 1;
    lastActName = actname;
    lastOccuranceid = frequency_id;
  }

  if(count > 1){
    if(endCount > finalList.length) endCount = finalList.length
    $('.compliance_count').text("Showing " + 1 + " to " + endCount + " of " + Object.keys(finalList).length);
  }
  if(endCount >= finalList.length){
    $(document).ready(function($) {
    $('#accordion').find('.accordion-toggle').click(function(){
      //Expand or collapse this panel
      $(this).next().slideToggle('fast');
      //Hide the other panels
      $(".accordion-content").not($(this).next()).slideUp('fast');
    });
  });
  }

  if(count == 1){
    var tableRow1=$('#nocompliance-templates .table-nocompliances-list .table-row');
    var clone1=tableRow1.clone();
    $('.tbody-compliance').append(clone1);
    $('.tbl_norecords', clone1).text("No Records");
    $('.accordion-content'+count).append(clone1);
  }
}

function get_sub_array(object, start, end){
    if(!end){ end=-1;}
    return object.slice(start, end);
}

$('#pagination').click(function(e){
  startCount = endCount;
  endCount = startCount + pageSize;
  var sub_act_list =  finalList;
  var sub_keys_list = get_sub_array(sub_act_list, startCount, endCount);
  if(sub_keys_list.length < pageSize){
    $('#pagination').hide();
  }
  //alert(startCount + '-' + endCount + '-' +sub_keys_list.length)
  e.preventDefault();
  loadCountwiseResult(sub_keys_list);
  
});

function loadresult() {
  pageSize = 500;
  startCount = 0;
  endCount = pageSize;

  var c_frequency = $("#compliance_frequency").val();
  if(c_frequency == 'All'){
    finalList = statutoryMappingDataList;
  }else{
    var filteredList=[];
    for(var entity in statutoryMappingDataList) {
      var filter_frequency = statutoryMappingDataList[entity]["frequency_id"];
      if (c_frequency == filter_frequency) filteredList.push(statutoryMappingDataList[entity]);
    }
    finalList = filteredList;
  }

  if(finalList.length > pageSize){
    $('#pagination').show();
  }else{
    $('#pagination').hide();
  }

  var sub_act_list =  finalList;
  var sub_keys_list = get_sub_array(sub_act_list, startCount, endCount);
  loadCountwiseResult(sub_keys_list);
}


$("#submit").click(function(){
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
  if($("#statutory").val() != '') act = $("#statutory").val();

  if(country.length == 0){
    displayMessage("Country Required");
  }
  else if(domain.length == 0){
    displayMessage("Domain Required");
  }
  else{
    displayLoader();
      var filterdata={};
      filterdata["country_id"]=parseInt(country);
      filterdata["domain_id"]=parseInt(domain);
      filterdata["industry_id"]=parseInt(industry);
      filterdata["statutory_nature_id"]=parseInt(statutorynature);
      filterdata["geography_id"]=parseInt(geography);
      filterdata["level_1_statutory_id"]=parseInt(act);

      function onSuccess(data){
        statutoryMappingDataList = data["statutory_mappings"];
        /*var currentTime = new Date();
        hour = currentTime.getHours();
        min  = currentTime.getMinutes();
        sec  = currentTime.getSeconds();
        ms = currentTime.getMilliseconds();
        console.log("API Response: "+ hour + ":" + min + ":" + sec + ":" + ms  );*/
        loadresult();
        hideLoader();
      }
      function onFailure(error){
        onFailure(error);
        hideLoader();
      }

      mirror.getStatutoryMappingsReportData(filterdata,
        function (error, response) {
          if (error == null){
            onSuccess(response);
          }
          else {
            onFailure(error);
          }
        });
    temp_act = act;
  }
});

//Autocomplete Script Starts
//Hide list items after select
$(".hidemenu").click(function(){
  $("#autocompleteview").hide();
  $("#autocomplete_domain").hide();
  $("#autocomplete_industry").hide();
  $("#autocomplete_statutorynature").hide();
  $("#autocomplete_geography").hide();
  $("#autocomplete_statutory").hide();
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
}

//load domain list in autocomplete text box
$("#domainval").keyup(function(){
  var textval = $(this).val();
  $("#autocomplete_domain").show();
  var domains = domainsList;
  var suggestions = [];
  $('#ulist_domain').empty();
  if(textval.length>0){
    for(var i in domains){
      if (~domains[i]["domain_name"].toLowerCase().indexOf(textval.toLowerCase()) && domains[i]["is_active"] == true) suggestions.push([domains[i]["domain_id"],domains[i]["domain_name"]]);
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_domain(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_domain').append(str);
    $("#domain").val('');
    }else{
      $("#domain").val('');
      $("#autocomplete_domain").hide();
    }
});
//set selected autocomplte value to textbox
function activate_domain (element,checkval,checkname) {
  $("#domainval").val(checkname);
  $("#domain").val(checkval);
}

//load domain list in autocomplete text box
$("#industryval").keyup(function(){
  var textval = $(this).val();
  $("#autocomplete_industry").show();
  var industries = industriesList;
  var suggestions = [];
  $('#ulist_industry').empty();
  if(textval.length>0){
    for(var i in industries){
      if (~industries[i]["industry_name"].toLowerCase().indexOf(textval.toLowerCase()) && industries[i]["is_active"] == true) suggestions.push([industries[i]["industry_id"],industries[i]["industry_name"]]);
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_industry(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_industry').append(str);
    $("#industry").val('');
    }else{
      $("#industry").val('');
      $("#autocomplete_industry").hide();
    }
});
//set selected autocomplte value to textbox
function activate_industry (element,checkval,checkname) {
  $("#industryval").val(checkname);
  $("#industry").val(checkval);
}


//load statutorynature list in autocomplete text box
$("#statutorynatureval").keyup(function(){
  var textval = $(this).val();
  $("#autocomplete_statutorynature").show();
  var statutorynatures = statutoryNaturesList;
  var suggestions = [];
  $('#ulist_statutorynature').empty();
  if(textval.length>0){
    for(var i in statutorynatures){
      if (~statutorynatures[i]["statutory_nature_name"].toLowerCase().indexOf(textval.toLowerCase()) && statutorynatures[i]["is_active"] == true) suggestions.push([statutorynatures[i]["statutory_nature_id"],statutorynatures[i]["statutory_nature_name"]]);
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_statutorynature(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_statutorynature').append(str);
    $("#statutorynature").val('');
    }else{
      $("#statutorynature").val('');
      $("#autocomplete_statutorynature").hide();
    }
});
//set selected autocomplte value to textbox
function activate_statutorynature (element,checkval,checkname) {
  $("#statutorynatureval").val(checkname);
  $("#statutorynature").val(checkval);
}

//load statutorynature list in autocomplete text box
$("#geographyval").keyup(function(){
  var textval = $(this).val();
  $("#autocomplete_geography").show();
  var geographies = geographiesList[$("#country").val()];
  var suggestions = [];
  $('#ulist_geography').empty();
  if(textval.length>0){
    for(var i in geographies){
      if (~geographies[i]["geography_name"].toLowerCase().indexOf(textval.toLowerCase()) && geographies[i]["is_active"] == true) suggestions.push([geographies[i]["geography_id"],geographies[i]["geography_name"]]);
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_geography(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_geography').append(str);
    $("#geography").val('');
    }else{
      $("#geography").val('');
       $("#autocomplete_geography").hide();
    }
});
//set selected autocomplte value to textbox
function activate_geography (element,checkval,checkname) {
  $("#geographyval").val(checkname);
  $("#geography").val(checkval);
}

//load statutorynature list in autocomplete text box
$("#statutoryval").keyup(function(){
  var textval = $(this).val();
  $("#autocomplete_statutory").show();
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
    }else{
      $("#statutory").val('');
      $("#autocomplete_statutory").hide();
    }
});
//set selected autocomplte value to textbox
function activate_statutory (element,checkval,checkname) {
  $("#statutoryval").val(checkname);
  $("#statutory").val(checkval);
}
//Autocomplete Script ends

$(function() {
  $(".grid-table-rpt").hide();
  getStatutoryMappings();
});

