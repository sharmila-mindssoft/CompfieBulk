var unitWiseComplianceList;
var countriesList;
var domainsList;
var actList;
var compliancesList;
var unitsList;
var usersList;

var sno = 0;
var fullArrayList = [];

var s_endCount = 0;
var totalRecord;
var lastUnit = '';

var country = null;
var domain = null;
var act = null;
var unit = null;
var compliances = null;
var userId = null;
var fromdate = null;
var todate = null;
var status = null;

function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
}

//get compliance details filter from api
function getComplianceDetailsReportFilters(){
  function onSuccess(data){
    countriesList = data["countries"];
    domainsList = data["domains"];
    actList = data["level_1_statutories"];
    unitsList = data["units"];
    usersList = data["users"];
    compliancesList = data["compliances"];
    loadCountries(countriesList);
  }
  function onFailure(error){
    displayMessage(error);
  }
  client_mirror.getComplianceDetailsReportFilters(
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

/*function convert_date (data){
  var date = data.split("-");
  var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  for(var j=0;j<months.length;j++){
      if(date[1]==months[j]){
           date[1]=months.indexOf(months[j])+1;
       }
  }
  if(date[1]<10){
      date[1]='0'+date[1];
  }
  return new Date(date[2], date[1]-1, date[0]);
}

function daydiff(first, second) {
    return (second-first)/(1000*60*60*24)
}*/


//clone & display unit heading
function filterList(data){
  var country = $("#country").find('option:selected').text();
  var domain = $("#domainval").val();
  var act = $("#actval").val();

  var tableRow=$('#unit-list-templates .table-unit-list .table-row-unit-list');
  var clone=tableRow.clone();
  $('.tbl_country', clone).text(country);
  $('.tbl_domain', clone).text(domain);
  $('.tbl_act', clone).text(act);
  $('.tbody-unit').append(clone);

  var tableRow1=$('#unit-head-templates .table-unit-head .table-row-unit-head');
  var clone1=tableRow1.clone();
  $('.tbody-unit').append(clone1);
}

//clone & display unit name
function unitList(data){
  if(lastUnit != data["unit_name"]){
    var tableRow2=$('#unit-name-templates .table-unit-name .table-row-unit-name');
    var clone2=tableRow2.clone();
    $('.tbl_unitheading', clone2).html('<div class="heading" style="margin-top:5px;width:auto;">' + data["unit_name"] + '</div>');
    $('.tbody-unit').append(clone2);
    lastUnit = data["unit_name"];
  }
}

//clone & display compliance details
function complianceListArray(data){
  var vDate = '-';
  if(data["validity_date"] != null) vDate = data["validity_date"];
  var dueDate = '-';
  if(data["due_date"] != null) dueDate = data["due_date"];

  var completionDate = '';
  if(data["completion_date"] != null) completionDate = data["completion_date"];

  var tableRow3=$('#unit-content-templates .table-unit-content .table-row-unit-content');
  var clone3=tableRow3.clone();
  $('.tbl_sno', clone3).text(sno+1);
  $('.tbl_compliance', clone3).html(data["compliance_name"]);
  $('.tbl_assignee', clone3).text(data["assignee"]);
  $('.tbl_duedate', clone3).text(dueDate);
  $('.tbl_completiondate', clone3).text(completionDate);
  $('.tbl_validitydate', clone3).text(vDate);
  $('.tbl_remarks', clone3).text(data["remarks"]);
  if(data["documents"] != null && data["documents"] != ''){
    var documentsList = data["documents"];
    var url = '';
    for(var i=0; i<documentsList.length; i++){
      url = url + '<a href="'+documentsList[i]+'" target="_new" download> Download '+ (i+1) +' </a> ';
    }
    $('.tbl_document', clone3).html(url);
  }
  $('.tbody-unit').append(clone3);
  sno++;
}






//create array for pagination and call display function
function loadArray(complianceList) {
  $.each(complianceList, function(i, val){
      var list = complianceList[i];
      var list_comp = val["compliances"]
      delete val["compliances"];
      fullArrayList.push(list);

      $.each(list_comp, function(i1, val1){
        var list_c = list_comp[i1];
        fullArrayList.push(list_c);
      });
  });
  
  var sub_keys_list = fullArrayList;
  for(var y = 0;  y < fullArrayList.length; y++){
    if(sub_keys_list[y] !=  undefined){
      if(Object.keys(sub_keys_list[y])[0] == "unit_name"){
        unitList(sub_keys_list[y]);
      }
      else if(Object.keys(sub_keys_list[y])[0] == "due_date"){
        complianceListArray(sub_keys_list[y]);
      }
    }
  }

  if(totalRecord == 0){
    var tableRow4=$('#no-record-templates .table-no-content .table-row-no-content');
    var clone4=tableRow4.clone();
    $('.no_records', clone4).text('No Compliance Found');
    $('.tbody-unit').append(clone4);
    $('#pagination').hide();
    $('.compliance_count').text('');
  }else{
    $('.compliance_count').text("Showing " + 1 + " to " + sno + " of " + totalRecord);
    if(sno >= totalRecord){
      $('#pagination').hide();
    }else{
      $('#pagination').show();
    }
  }
}

//pagination process
$('#pagination').click(function(){
  displayLoader();
  s_endCount = sno;
  fullArrayList = [];
  clearMessage();

  function onSuccess(data){
    unitWiseComplianceList = data["unit_wise_compliancess"];
    totalRecord = data["total_count"];
    loadArray(unitWiseComplianceList);
    hideLoader();
  }
  function onFailure(error){
    onFailure(error);
    hideLoader();
  }

  client_mirror.getComplianceDetailsReport(
      parseInt(country), parseInt(domain), act, parseInt(unit),
      parseInt(compliances), parseInt(userId), fromdate, todate,
      status, csv, s_endCount,
      function (error, response) {
      if (error == null){
        onSuccess(response);
      }
      else {
        onFailure(error);
      }
    });
});


//get compliance details report data from api
function loadCompliance(reportType){
  displayLoader();
  country = $("#country").val();
  domain = $("#domain").val();
  act = $("#act").val().trim();
  unit = null;
  compliances = null;
  userId = null;
  fromdate = null;
  todate = null;
  status = null;

  if($("#compliancetask").val() != '') compliances = $("#compliancetask").val();
  if($("#unit").val() != '') unit = $("#unit").val();
  if($("#assignee").val() != '') userId = $("#assignee").val();
  if($("#fromdate").val() != '') fromdate = $("#fromdate").val();
  if($("#todate").val() != '') todate = $("#todate").val();
  if($("#status").val() != '') status = $("#status").val();

  $(".tbody-unit").find("tbody").remove();
  $('.compliance_count').text('');
  lastUnit = '';
  sno = 0;
  s_endCount = 0;
  fullArrayList = [];
  clearMessage();

  if(country.length == 0){
    displayMessage(message.country_required);
    $(".grid-table-rpt").hide();
    hideLoader();
  }
  else if(domain.length == 0){
    displayMessage(message.domain_required);
    $(".grid-table-rpt").hide();
    hideLoader();
  }
  else if(act.length == 0){
    displayMessage(message.act_required);
    $(".grid-table-rpt").hide();
    hideLoader();
  }
  else{
    function onSuccess(data){
      unitWiseComplianceList = data["unit_wise_compliancess"];
      totalRecord = data["total_count"];
      filterList();
      $(".grid-table-rpt").show();

      if(reportType == "show"){
        loadArray(unitWiseComplianceList);
      }else{
        // loadTotalCount(unitWiseComplianceList);
        var download_url = data["link"];
        window.open(download_url, '_blank');
      }
      hideLoader();
    }
    function onFailure(error){
      onFailure(error);
      hideLoader();
    }
    csv = true
    if(reportType == "show"){
      csv = false
    }
    client_mirror.getComplianceDetailsReport(
      parseInt(country), parseInt(domain), act, parseInt(unit),
      parseInt(compliances), parseInt(userId), fromdate, todate,
      status, csv, s_endCount,
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

$("#submit").click(function(){
  loadCompliance("show")
});

$("#export").click(function(){
  loadCompliance("export")
});

//Autocomplete Script Starts


//load country list
function loadCountries(countriesList){
  $('#country').append($('<option value=""> Select </option>'));
  $.each(countriesList, function(key, values){
    var countryId = countriesList[key]['country_id'];
    var countryName = countriesList[key]['country_name'];
    $('#country').append($('<option value="'+countryId+'">'+countryName+'</option>'));
  });
}

//retrive domain autocomplete value
function onDomainSuccess(val){
  $("#domainval").val(val[1]);
  $("#domain").val(val[0]);
  $("#domainval").focus();
}
//load domain list in autocomplete textbox
$("#domainval").keyup(function(){
  var textval = $(this).val();
  getDomainAutocomplete(textval, domainsList, function(val){
    onDomainSuccess(val)
  })
});

//retrive statutory autocomplete value
function onStatutorySuccess(val){
  $("#actval").val(val[1]);
  $("#act").val(val[0].replace(/##/gi,'"'));
  $("#actval").focus();
}
//load statutory list in autocomplete textbox
$("#actval").keyup(function(){
  var textval = $(this).val();
  getClientStatutoryAutocomplete(textval, actList, function(val){
    onStatutorySuccess(val)
  })
});

//retrive unit form autocomplete value
function onUnitSuccess(val){
  $("#unitval").val(val[1]);
  $("#unit").val(val[0]);
  $("#unitval").focus();
}

//load unit  form list in autocomplete text box
$("#unitval").keyup(function(){
  var textval = $(this).val();
  //var cId = $("#country").val();
  //var dId = $("#domain").val();
  getUnitAutocomplete(textval, unitsList, function(val){
    onUnitSuccess(val)
  })
});

//retrive compliance task form autocomplete value
function onComplianceTaskSuccess(val){
  $("#compliancetaskval").val(val[1]);
  $("#compliancetask").val(val[0]);
  $("#compliancetaskval").focus();
}

//load compliancetask form list in autocomplete text box
$("#compliancetaskval").keyup(function(){
  var textval = $(this).val();
  getComplianceTaskAutocomplete(textval, compliancesList, function(val){
    onComplianceTaskSuccess(val)
  })
});

//retrive user autocomplete value
function onUserSuccess(val){
  $("#assigneeval").val(val[1]);
  $("#assignee").val(val[0]);
  $("#assigneeval").focus();
}

//load user list in autocomplete text box
$("#assigneeval").keyup(function(){
  var textval = $(this).val();
  getUserAutocomplete(textval, usersList, function(val){
    onUserSuccess(val)
  })
});
//Autocomplete Script ends

//initialization
$(function() {
  $(".grid-table-rpt").hide();
  getComplianceDetailsReportFilters();
  $("#country").focus();
});