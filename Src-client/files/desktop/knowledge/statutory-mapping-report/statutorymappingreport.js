var statutoryMappingDataList;
var geographiesList;
var countriesList;
var domainsList;
var industriesList;
var statutoryNaturesList;
var statutoriesList;
var complianceFrequencyList;
var temp_act = null;

function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
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

function loadresult(filterList){
  $(".grid-table-rpt").show();
  var country = $("#countryval").val();
  var domain = $("#domainval").val();
  var compliance_frequency = $("#compliance_frequency").val();
  $(".country").text(country);
  $(".domain").text(domain);

  $(".tbody-compliance").find("tbody").remove();
  var count=1;
  var compliance_count=0;
  for(var entity in filterList){
    var checkNoCompliance = true;
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

    var tableRow=$('#act-templates .table-act-list .table-row-act-list');
    var clone=tableRow.clone();
    $('.actname', clone).html(actname +'<span><img src="/images/chevron_black_down.png"></span>');
    $('.tbody-compliance').append(clone);
    $('.tbody-compliance').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
    if(count==1){
      $('.accordion-content'+count).addClass("default");
    }

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
                checkNoCompliance = false;
            }
            });
            if(occuranceid == 1 && (j+1)==1){
              if(display_occurance1){
                var tableRow2=$('#head-templates .table-compliance-frequency-list .table-row-com-frequency');
                var clone2=tableRow2.clone();
                $('.tbl_heading', clone2).html('<div class="heading" style="margin-top:5px;width:150px;">'+occurance+'</div>');
                $('.accordion-content'+count).append(clone2);
                display_occurance1 = false;}
            }
            if(occuranceid == 2 && (j+1)==2){
              if(display_occurance2){
                var tableRow2=$('#head-templates .table-compliance-frequency-list .table-row-com-frequency');
                var clone2=tableRow2.clone();
                $('.tbl_heading', clone2).html('<div class="heading" style="margin-top:5px;width:150px;">'+occurance+'</div>');
                $('.accordion-content'+count).append(clone2);
                display_occurance2 = false;}
            }
            if(occuranceid == 3 && (j+1)==3){
              if(display_occurance3){
                var tableRow2=$('#head-templates  .table-compliance-frequency-list .table-row-com-frequency');
                var clone2=tableRow2.clone();
                $('.tbl_heading', clone2).html('<div class="heading" style="margin-top:5px;width:150px;">'+occurance+'</div>');
                $('.accordion-content'+count).append(clone2);
                display_occurance3 = false;}
            }
            if(occuranceid == 4 && (j+1)==4){
              if(display_occurance4){
                var tableRow2=$('#head-templates  .table-compliance-frequency-list .table-row-com-frequency');
                var clone2=tableRow2.clone();
                $('.tbl_heading', clone2).html('<div class="heading" style="margin-top:5px;width:150px;">'+occurance+'</div>');
                $('.accordion-content'+count).append(clone2);
                display_occurance4 = false;}
            }

            if(occuranceid == 1 && (j+1)==1 || occuranceid == 2 && (j+1)==2 || occuranceid == 3 && (j+1)==3 || occuranceid == 4 && (j+1)==4){
              var tableRow1=$('#compliance-templates .table-compliances-list .table-row');
              var clone1=tableRow1.clone();
              $('.tbody-compliance').append(clone1);
              $('.tbl_sno', clone1).text(compliance_count+1);
              $('.tbl_industrytype', clone1).text(filterList[entity][i]["industry_names"]);
              $('.tbl_statutorynature',   clone1).text(filterList[entity][i]["statutory_nature_name"]);
              $('.tbl_statutoryprovision', clone1).text(filterList[entity][i]["compliances"][k]["statutory_provision"]);
              var compliance_name = filterList[entity][i]["compliance_names"][k]["compliance_name"]

              var download_url = filterList[entity][i]["compliance_names"][k]["url"];
              if(download_url == null){
                $('.tbl_compliancetask', clone1).html(compliance_name);
              }else{
                $('.tbl_compliancetask', clone1).html('<a href= "'+ download_url +'" target="_new">'+compliance_name+'</a>');
              }

              var sdateDesc = '';
              var duration = filterList[entity][i]["compliances"][k]["duration"];
              var duration_type_id = filterList[entity][i]["compliances"][k]["duration_type_id"];
              var repeats_every = filterList[entity][i]["compliances"][k]["repeats_every"];
              var repeats_type_id = filterList[entity][i]["compliances"][k]["repeats_type_id"];

              var statutory_date =  filterList[entity][i]["compliances"][k]["statutory_dates"];
              var statutorydate = '';

              var duration_type = '';
              var repeats_type = '';

              if(occurance == "On Occurrence"){
                if(duration_type_id == 1){
                  duration_type = 'Day(s)';
                }else{
                  duration_type = 'Hour(s)';
                }
                sdateDesc = duration + ' ' + duration_type;
              }
              else if(occurance == 'One Time'){
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

              if(occurance != "On Occurrence"){
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
                }
                if(sdateDesc != ''){
                  statutorydate = sdateDesc + ' ( '+statutorydate+' )';
                }
              }else{
                statutorydate = sdateDesc;
              }
              $('.tbl_description', clone1).text(filterList[entity][i]["compliances"][k]["description"]);
              $('.tbl_penalconsequences', clone1).text(filterList[entity][i]["compliances"][k]["penal_consequences"]);
              $('.tbl_occurance', clone1).text(statutorydate);
              $('.tbl_applicablelocation', clone1).text(filterList[entity][i]["geography_mappings"]);
              $('.accordion-content'+count).append(clone1);
              compliance_count = compliance_count + 1;
            }
          }
        }
      }
    }
    if(checkNoCompliance){
      var tableRow1=$('#nocompliance-templates .table-nocompliances-list .table-row');
      var clone1=tableRow1.clone();
      $('.tbody-compliance').append(clone1);
      $('.tbl_norecords', clone1).text("No Records");
      $('.accordion-content'+count).append(clone1);
    }
    count++;
  }
  $('.compliance_count').text("Total : "+ (compliance_count) +" records");
  $(document).ready(function($) {
    $('#accordion').find('.accordion-toggle').click(function(){
      //Expand or collapse this panel
      $(this).next().slideToggle('fast');
      //Hide the other panels
      $(".accordion-content").not($(this).next()).slideUp('fast');
    });
  });
  var currentTime = new Date();
  hour = currentTime.getHours();
  min  = currentTime.getMinutes();
  sec  = currentTime.getSeconds();
  ms = currentTime.getMilliseconds();
  console.log("End progress : "+ hour + ":" + min + ":" + sec + ":" + ms  );

}

$("#submit").click(function(){
  var currentTime = new Date();
  hour = currentTime.getHours();
  min  = currentTime.getMinutes();
  sec  = currentTime.getSeconds();
  ms = currentTime.getMilliseconds();
  console.log("Start Progress : "+ hour + ":" + min + ":" + sec + ":" + ms  );

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
    /*if((country == temp_country) && (domain == temp_domain) && (temp_industry == null || industry == temp_industry) && (temp_statutorynature == null || statutorynature == temp_statutorynature) &&
     (temp_geography == null || geography == temp_geography)){
      loadresult(statutoryMappingDataList);
    }else{*/
      var filterdata={};
      filterdata["country_id"]=parseInt(country);
      filterdata["domain_id"]=parseInt(domain);
      filterdata["industry_id"]=parseInt(industry);
      filterdata["statutory_nature_id"]=parseInt(statutorynature);
      filterdata["geography_id"]=parseInt(geography);
      filterdata["level_1_statutory_id"]=parseInt(act);

      function onSuccess(data){
        statutoryMappingDataList = data["statutory_mappings"];
        var currentTime = new Date();
        hour = currentTime.getHours();
        min  = currentTime.getMinutes();
        sec  = currentTime.getSeconds();
        ms = currentTime.getMilliseconds();
        console.log("API Response: "+ hour + ":" + min + ":" + sec + ":" + ms  );
        loadresult(statutoryMappingDataList);
      }
      function onFailure(error){
        onFailure(error);
      }

      var currentTime = new Date();
      hour = currentTime.getHours();
      min  = currentTime.getMinutes();
      sec  = currentTime.getSeconds();
      ms = currentTime.getMilliseconds();
      console.log("Call API : "+ hour + ":" + min + ":" + sec + ":" + ms  );

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

