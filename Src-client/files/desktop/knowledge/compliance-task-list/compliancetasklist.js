var statutoryMappingDataList;
var geographiesList;
var countriesList;
var domainsList;
var industriesList;
var statutoryNaturesList;
var statutoriesList;
var complianceFrequencyList;
var finalList;

var count=1;
var compliance_count=0;
var lastActName = '';
var lastOccuranceid = 0;
var lastIndustryName = '';
var s_endCount = 0;
var totalRecord;
var filterdata={};


function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
}

//get compliance list report filters
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
  mirror.getComplianceTaskFilter(
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

//display compliance list report data
function loadCountwiseResult(filterList){
  if(compliance_count <= 0){
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
    lastIndustryName = '';
  }

  for(var entity in filterList){
    var actname = filterList[entity]["act_name"];
    var frequency_id = filterList[entity]["frequency_id"];
    var industry_names = filterList[entity]["industry_names"];
    var statutory_nature_name = filterList[entity]["statutory_nature_name"];
    var statutory_provision = filterList[entity]["statutory_provision"];
    var compliance_name = filterList[entity]["compliance_task"];
    var download_url = filterList[entity]["url"];

    if(actname != lastActName){
      var tableRow=$('#act-templates .table-act-list .table-row-act-list');
      var clone=tableRow.clone();
      $('.actname', clone).html(actname +'<span><img src="/images/chevron_black_down.png"></span>');
      $('.tbody-compliance').append(clone);
      $('.tbody-compliance').append('<tbody class="accordion-content accordion-content'+count+' default"></tbody>');
      lastOccuranceid = 0;
      lastIndustryName = '';
      count++;

      $(clone, '.actname').click(function(){
          //Expand or collapse this panel
          $(this).next().slideToggle('fast');
          //Hide the other panels
          $(".accordion-content").not($(this).next()).slideUp('fast');
      });

    }

    if(industry_names != lastIndustryName){
      var tableRow3=$('#industry-head-templates .table-industry-list .table-row-industry');
      var clone3=tableRow3.clone();
      $('.tbl_industry_heading', clone3).html("Industry : " +industry_names);
      $('.accordion-content'+(count-1)).append(clone3);
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
    $('.tbl_compliancefrequency', clone1).text(occurance);
    $('.tbl_statutorynature',   clone1).text(statutory_nature_name);
    $('.tbl_statutoryprovision', clone1).text(statutory_provision);
    if(download_url == null){
      $('.tbl_compliancetask', clone1).html(compliance_name);
    }else{
      $('.tbl_compliancetask', clone1).html('<a href= "'+ download_url +'" target="_new" download>'+compliance_name+'</a>');
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

      if(sMonth != '') sMonth = getMonth_IntegettoString(sMonth);

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
      }else{
        statutorydate = sdateDesc;
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
    lastIndustryName = industry_names;
  }

  if(compliance_count > 0){
    $('.compliance_count').text("Showing " + 1 + " to " + compliance_count + " of " + totalRecord);
  }else{
    $('.compliance_count').text('');
  }

  if(compliance_count >= totalRecord){
    $('#pagination').hide();
  }

  if(count == 1){
    var tableRow1=$('#nocompliance-templates .table-nocompliances-list .table-row');
    var clone1=tableRow1.clone();
    $('.tbody-compliance').append(clone1);
    $('.tbl_norecords', clone1).text("No Records");
    $('.accordion-content'+count).append(clone1);
    $('#pagination').hide();
  }
}

function loadresult() {
 /* var c_frequency = $("#compliance_frequency").val();
  if(c_frequency == 'All'){
    finalList = statutoryMappingDataList;
  }else{
    var filteredList=[];
    for(var entity in statutoryMappingDataList) {
      var filter_frequency = statutoryMappingDataList[entity]["frequency_id"];
      if (c_frequency == filter_frequency) filteredList.push(statutoryMappingDataList[entity]);
    }
    finalList = filteredList;
  }*/
  loadCountwiseResult(statutoryMappingDataList);
}

$('#pagination').click(function(){
  s_endCount = compliance_count;
  filterdata["record_count"]=parseInt(s_endCount);
  displayLoader();
  function onSuccess(data){
    statutoryMappingDataList = data["statutory_mappings"];
    totalRecord = data["total_count"];
    loadresult();
    hideLoader();
  }
  function onFailure(error){
    displayMessage(error);
    hideLoader();
  }
  mirror.getComplianceTaskReport(filterdata,
    function (error, response) {
      if (error == null){
        onSuccess(response);
      }
      else {
        onFailure(error);
      }
    });
});

//get compliance list report data based on filter selection from api
$("#submit").click(function(){
  var country = $("#country").val();
  var domain = $("#domain").val();
  var industry = null;
  var statutorynature = null;
  var geography = null;
  var act = null;
  var c_frequency = null;

  if($("#industry").val() != '') industry = $("#industry").val();
  if($("#statutorynature").val() != '') statutorynature = $("#statutorynature").val();
  if($("#geography").val() != '') geography = $("#geography").val();
  if($("#statutory").val() != '') act = $("#statutory").val();
  if($("#compliance_frequency").val() != '') c_frequency = $("#compliance_frequency").val();


  if(country.length == 0){
    displayMessage(message.country_required);
  }
  else if(domain.length == 0){
    displayMessage(message.domain_required);
  }
  else{
    count=1;
    compliance_count=0;
    lastActName = '';
    lastOccuranceid = 0;
    lastIndustryName = '';
    displayLoader();
    displayMessage("");
    s_endCount = 0;
    filterdata={};
    filterdata["country_id"]=parseInt(country);
    filterdata["domain_id"]=parseInt(domain);
    filterdata["industry_id"]=parseInt(industry);
    filterdata["statutory_nature_id"]=parseInt(statutorynature);
    filterdata["geography_id"]=parseInt(geography);
    filterdata["level_1_statutory_id"]=parseInt(act);
    filterdata["frequency_id"]=parseInt(c_frequency);
    filterdata["record_count"]=parseInt(s_endCount);

    function onSuccess(data){
      statutoryMappingDataList = data["statutory_mappings"];
      totalRecord = data["total_count"];
      loadresult();
      hideLoader();
    }
    function onFailure(error){
      displayMessage(error);
      hideLoader();
    }
    mirror.getComplianceTaskReport(filterdata,
      function (error, response) {
        if (error == null){
          onSuccess(response);
        }
        else {
          onFailure(error);
        }
      });
    }
});

//Autocomplete Script Starts
//retrive country autocomplete value
function onCountrySuccess(val){
  $("#countryval").val(val[1]);
  $("#country").val(val[0]);
}

//load country list in autocomplete text box  
$("#countryval").keyup(function(){
  var textval = $(this).val();
  getCountryAutocomplete(textval, countriesList, function(val){
    onCountrySuccess(val)
  })
});

//retrive domain autocomplete value
function onDomainSuccess(val){
  $("#domainval").val(val[1]);
  $("#domain").val(val[0]);
}
//load domain list in autocomplete textbox  
$("#domainval").keyup(function(){
  var textval = $(this).val();
  getDomainAutocomplete(textval, domainsList, function(val){
    onDomainSuccess(val)
  })
});

//retrive industry autocomplete value
function onIndustrySuccess(val){
  $("#industryval").val(val[1]);
  $("#industry").val(val[0]);
}
//load industry list in autocomplete textbox  
$("#industryval").keyup(function(){
  var textval = $(this).val();
  getIndustryAutocomplete(textval, industriesList, function(val){
    onIndustrySuccess(val)
  })
});

//retrive statutorynature autocomplete value
function onStatutoryNatureSuccess(val){
  $("#statutorynatureval").val(val[1]);
  $("#statutorynature").val(val[0]);
}
//load statutorynature list in autocomplete textbox  
$("#statutorynatureval").keyup(function(){
  var textval = $(this).val();
  getStatutoryNatureAutocomplete(textval, statutoryNaturesList, function(val){
    onStatutoryNatureSuccess(val)
  })
});

//retrive geography autocomplete value
function onGeogaphySuccess(val){
  $("#geographyval").val(val[1]);
  $("#geography").val(val[0]);
}
//load geography list in autocomplete textbox  
$("#geographyval").keyup(function(){
  var textval = $(this).val();
  getGeographyAutocomplete(textval, geographiesList[$("#country").val()], function(val){
    onGeogaphySuccess(val)
  })
});

//retrive statutory autocomplete value
function onStatutorySuccess(val){
  $("#statutoryval").val(val[1]);
  $("#statutory").val(val[0]);
}
//load statutory list in autocomplete textbox  
$("#statutoryval").keyup(function(){
  var textval = $(this).val();
  getStatutoryAutocomplete(textval, statutoriesList[$("#country").val()][$("#domain").val()], function(val){
    onStatutorySuccess(val)
  })
});
//Autocomplete Script ends

//initialization
$(function() {
  $(".grid-table-rpt").hide();
  getStatutoryMappings();
});