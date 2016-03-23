var unitWiseComplianceList;
var countriesList;
var domainsList;
var actList;
var compliancesList;
var unitsList;
var usersList;

function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

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

function convert_date (data){
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
}

function loadresult(filterList){
  $(".grid-table-rpt").show();
  var country = $("#country").find('option:selected').text();
  var domain = $("#domainval").val();
  var act = $("#actval").val();
  var status = $("#status").val();

  $(".tbody-unit").find("tbody").remove();

  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth();
  var yyyy = today.getFullYear();
  if(dd<10){
      dd='0'+dd
  } 
  if(mm<10){
      mm='0'+mm
  } 
  var currentDate = new Date(yyyy, mm, dd);

  var compliance_count=0;
  var tableRow=$('#unit-list-templates .table-unit-list .table-row-unit-list');
  var clone=tableRow.clone();
  $('.tbl_country', clone).text(country);
  $('.tbl_domain', clone).text(domain);
  $('.tbl_act', clone).text(act);
  $('.tbody-unit').append(clone);

  var tableRow1=$('#unit-head-templates .table-unit-head .table-row-unit-head');
  var clone1=tableRow1.clone();
  $('.tbody-unit').append(clone1);

  for(var entity in filterList){
    var unitName = filterList[entity]["unit_name"];
    var compliancelists = filterList[entity]["compliances"];
    var unitdisplay = true;

    for(var compliancelist in compliancelists){
        if(unitdisplay){
          var tableRow2=$('#unit-name-templates .table-unit-name .table-row-unit-name');
          var clone2=tableRow2.clone();
          $('.tbl_unitheading', clone2).html('<div class="heading" style="margin-top:5px;width:auto;">' + unitName + '</div>');
          $('.tbody-unit').append(clone2);
          unitdisplay = false;
        }

        var vDate = '';
        if(compliancelists[compliancelist]["validity_date"] != null) vDate = compliancelists[compliancelist]["validity_date"];
        
        var dueDate = compliancelists[compliancelist]["due_date"];
        
        var completionDate = '';
        if(compliancelists[compliancelist]["completion_date"] != null) completionDate = compliancelists[compliancelist]["completion_date"];
        
        var cDueDate = convert_date(compliancelists[compliancelist]["due_date"]);
        var cDate = currentDate;
        if(completionDate != ''){
          cDate = convert_date(completionDate);
        }
        var dateDifference = daydiff(cDueDate, cDate);
        
        var remark = '';
        var compStatus = '';

        if(completionDate != '' && dateDifference <=0){
          remark = 'On Time';
          compStatus = 'Complied';
        } 
        else if (completionDate != '' && dateDifference > 0) {
          remark = 'Over due by '+ dateDifference +' Days';
          compStatus = 'Complied';
        }
        else if (completionDate == '' && dateDifference > 0) {
          remark = 'Delayed by '+ dateDifference +' Days';
          compStatus = 'DelayedCompliance';
        }
        else if (completionDate == '' && dateDifference <= 0) {
          remark =  dateDifference +' Days left';
          compStatus = 'Inprogress';
        }

        if(status == '' || status == compStatus){
          var tableRow3=$('#unit-content-templates .table-unit-content .table-row-unit-content');
          var clone3=tableRow3.clone();
          $('.tbl_sno', clone3).text(compliance_count+1);
          $('.tbl_compliance', clone3).html(compliancelists[compliancelist]["compliance_name"]);
          $('.tbl_assignee', clone3).text(compliancelists[compliancelist]["assignee"]);
          $('.tbl_duedate', clone3).text(dueDate);
          $('.tbl_completiondate', clone3).text(completionDate);
          $('.tbl_validitydate', clone3).text(vDate);
          $('.tbl_remarks', clone3).text(remark);
          if(compliancelists[compliancelist]["documents"] != null){
            var documentsList = compliancelists[compliancelist]["documents"];
            var url = '';
            for(var i=0; i<documentsList.length; i++){
              url = url + '<a href="'+documentsList[i]+'" target="_new"> Download '+ (i+1) +' </a> ';
            }
            $('.tbl_document', clone3).html(url);
          }
          $('.tbody-unit').append(clone3);
          compliance_count++;
        }
    }   

    /*if(compliancelists.length == 0){
        var tableRow4=$('#unit-content-templates .table-unit-content .table-row-unit-content');
        var clone4=tableRow4.clone();
        $('.tbl_duedate', clone4).text("No Compliance Found");
        $('.tbody-unit').append(clone4);
      }*/
  }  
  $('.compliance_count').text("Total : "+ (compliance_count) +" records");
}

function loadCompliance(reportType){
  var country = $("#country").val();
  var domain = $("#domain").val();
  var act = $("#act").val().trim();
  var unit = null;
  var compliances = null;
  var user = null;
  var fromdate = null;
  var todate = null;
  var status = null;

  if($("#compliancetask").val() != '') compliances = $("#compliancetask").val();
  if($("#unit").val() != '') unit = $("#unit").val();
  if($("#assignee").val() != '') user = $("#assignee").val();
  if($("#fromdate").val() != '') fromdate = $("#fromdate").val();
  if($("#todate").val() != '') todate = $("#todate").val();
  if($("#status").val() != '') status = $("#status").val();

  if(country.length == 0){
    displayMessage("Country Required");
  }
  else if(domain.length == 0){
    displayMessage("Domain Required");  
  }
  else if(act.length == 0){
    displayMessage("Act Required");  
  }
  else{
      loadresult(unitWiseComplianceList);
      function onSuccess(data){
        unitWiseComplianceList = data["unit_wise_compliancess"];
        if(reportType == "show"){
          loadresult(unitWiseComplianceList);
        }else{
          loadresult(unitWiseComplianceList);
          client_mirror.exportToCSV(data, 
            function (error, response) {
              if (error == null){
                var download_url = response["link"];
                window.open(download_url, '_blank');
              }
              else {
                displayMessage(error);
              }
            });
        }
      }
      function onFailure(error){
        onFailure(error);
      }
      client_mirror.getComplianceDetailsReport( parseInt(country), parseInt(domain), act, parseInt(unit), parseInt(compliances), parseInt(assignee), fromdate, todate, status, 
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
//Hide list items after select
$(".hidemenu").click(function(){
  $("#autocomplete_domain").hide();
  $("#autocomplete_act").hide();
  $("#autocomplete_unit").hide();
  $("#autocomplete_assignee").hide();
  $("#autocomplete_compliancetask").hide();
});

//load country list
function loadCountries(countriesList){
  $('#country').append($('<option value=""> Select </option>'));
  $.each(countriesList, function(key, values){
    var countryId = countriesList[key]['country_id'];
    var countryName = countriesList[key]['country_name'];
    $('#country').append($('<option value="'+countryId+'">'+countryName+'</option>'));
  });
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

//acts-------------------------------------
$("#actval").keyup(function(){
  var textval = $(this).val();
  $("#autocomplete_act").show();

  var acts = actList;
  var suggestions = [];
  $('#ulist_act').empty();
  if(textval.length>0){
    for(var i in acts){
      if (~acts[i].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([acts[i],acts[i]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_acts(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_act').append(str);
    $("#act").val('');
    }else{
      $("#act").val('');
      $("#autocomplete_act").hide();
    }
});
function activate_acts (element,checkval,checkname) {
  $("#actval").val(checkname);
  $("#act").val(checkval);
}

//Units-------------------------------------------------------------------------------------------
$("#unitval").keyup(function(){

  var textval = $(this).val();
  $("#autocomplete_unit").show();
  var units = unitsList;
  var suggestions = [];
 $('#ulist_unit').empty();
  if(textval.length>0){
    for(var i in units){
      if (~units[i]["unit_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([units[i]["unit_id"],units[i]["unit_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_units(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_unit').append(str);
    $("#unit").val('');
    }else{
      $("#unit").val('');
      $("#autocomplete_unit").hide();
    }
});
//set selected autocomplte value to textbox
function activate_units (element,checkval,checkname) {
  $("#unitval").val(checkname);
  $("#unit").val(checkval);
}

//compliancetask Entity---------------------------------------------------
$("#compliancetaskval").keyup(function(){

  var textval = $(this).val();
  $("#autocomplete_compliancetask").show();
  
  var compliancetasks = compliancesList;
  var suggestions = [];
 $('#ulist_compliancetask').empty();
  if(textval.length>0){
    for(var i in compliancetasks){
      if (~compliancetasks[i]["compliance_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([compliancetasks[i]["compliance_id"],compliancetasks[i]["compliance_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_compliancetask(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_compliancetask').append(str);
    $("#compliancetask").val('');
    }else{
      $("#compliancetask").val('');
      $("#autocomplete_compliancetask").hide();
    }
});
//set selected autocomplte value to textbox
function activate_compliancetask (element,checkval,checkname) {
  $("#compliancetaskval").val(checkname);
  $("#compliancetask").val(checkval);
}


//Assignee---------------------------------------------------
$("#assigneeval").keyup(function(){

  var textval = $(this).val();
  $("#autocomplete_assignee").show();
  
  var assignees = usersList;
  var suggestions = [];
 $('#ulist_assignee').empty();
  if(textval.length>0){
    for(var i in assignees){
      if (~assignees[i]["employee_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([assignees[i]["employee_id"],assignees[i]["employee_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_assignee(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
              
    }
    $('#ulist_assignee').append(str);
    $("#assignee").val('');
    }else{
      $("#assignee").val('');
      $("#autocomplete_assignee").hide();
    }
});
//set selected autocomplte value to textbox
function activate_assignee (element,checkval,checkname) {
  $("#assigneeval").val(checkname);
  $("#assignee").val(checkval);
}
//Autocomplete Script ends

$(function() {
  $(".grid-table-rpt").hide();
  getComplianceDetailsReportFilters();
});