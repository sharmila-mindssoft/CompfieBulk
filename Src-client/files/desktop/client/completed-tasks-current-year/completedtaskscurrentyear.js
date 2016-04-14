var countriesList;
var businessgroupsList;
var legalentitiesList;
var divisionsList;
var unitsList;
var statutoriesList;
var domainsList;
var frequencyList;
var actList;
var file_list = [];
var usersList;

function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
}
function clearValues(levelvalue) {
  if(levelvalue == 'country'){
    $('#businessgroup').empty();
    $('#legalentity').empty();
    $('#division').empty();
    $('#unit').empty();
  }

  if(levelvalue == 'businessgroup'){
    $('#legalentity').empty();
    $('#division').empty();
    $('#unit').empty();
  }

  if(levelvalue == 'legalentity'){
    $('#division').empty();
    $('#unit').empty();
  }

  if(levelvalue == 'division'){
    $('#unit').empty();
  }
}

function activate_assignee (element,checkval,checkname, clickvalue) {
  $("#assigneeval"+clickvalue).val(checkname);
  $("#assignee"+clickvalue).val(checkval);
}

function load_thirdwizard(){

  var arrowimage = " <img src=\'/images/right_arrow.png\'/> ";
    $(".breadcrumbs").html($('.countrylist.active').text() + arrowimage + 
      $('.legalentitylist.active').text() + arrowimage + $('.unitlist.active').text() +
      arrowimage + $('.domainlist.active').text());

    /*$(".breadcrumbs").html($('.countrylist.active').text() + arrowimage + $('.businessgrouplist.active').text() + arrowimage + 
      $('.legalentitylist.active').text() + arrowimage + $('.divisionlist.active').text() + arrowimage + $('.unitlist.active').text() +
      arrowimage + $('.domainlist.active').text());*/

  var count=1;
  var statutoriesCount= 1;
  var actCount = 1;
  $(".tbody-assignstatutory").find("tr").remove();

  for(var entity in statutoriesList){
    var actname = statutoriesList[entity]["level_1_statutory_name"];;
    var actCompliances = statutoriesList[entity]["compliences"];
      
      if(actCompliances.length > 0){
        var acttableRow=$('#act-templates .font1 .tableRow');
        var clone=acttableRow.clone();
        $('.actname', clone).html('<div class="heading" style="margin-top:5px;width:auto;">'+actname+'</div>');
        $('.tbody-assignstatutory').append(clone);
      }
      
      for(var ac in actCompliances){    
        var compliance_id = actCompliances[ac]["compliance_id"];
        var compliance_name = actCompliances[ac]["compliance_name"];
        var compliance_description = actCompliances[ac]["description"];
        var assignee_name =  actCompliances[ac]["assignee_name"];
        var assignee_id =  actCompliances[ac]["assignee_id"];
        var frequency =  actCompliances[ac]["frequency"];
        var statutory_date =  actCompliances[ac]["statutory_date"];
        var due_date =  actCompliances[ac]["due_date"];
        var statutorydate = actCompliances[ac]["statutory_date"];

      // if(frequency == 'Periodical' || frequency == 'Review') sdateDesc = 'Every';
      //   for(j = 0; j < statutory_date.length; j++){
      //     var sDay = '';
      //     if(statutory_date[j]["statutory_date"] != null) sDay = statutory_date[j]["statutory_date"];
          
      //     var sMonth = '';
      //     if(statutory_date[j]["statutory_month"] != null) sMonth = statutory_date[j]["statutory_month"];

      //     if(sMonth == 1) sMonth = "January"
      //     else if(sMonth == 2) sMonth = "February"
      //     else if(sMonth == 3) sMonth = "March"
      //     else if(sMonth == 4) sMonth = "April"  
      //     else if(sMonth == 5) sMonth = "May"
      //     else if(sMonth == 6) sMonth = "June"
      //     else if(sMonth == 7) sMonth = "July"
      //     else if(sMonth == 8) sMonth = "Auguest"
      //     else if(sMonth == 9) sMonth = "September"
      //     else if(sMonth == 10) sMonth = "October"
      //     else if(sMonth == 11) sMonth = "November"
      //     else if(sMonth == 12) sMonth = "December"
          
      //     statutorydate +=  sdateDesc + ' ' +sMonth +' '+ sDay;
      //   }

        var complianceDetailtableRow=$('#statutory-values .table-statutory-values .compliance-details');
        var clone2=complianceDetailtableRow.clone();
        
        $('.compliancetask', clone2).html('<abbr class="page-load" title="'+
          compliance_description+'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+compliance_name);
        $('.compliancefrequency', clone2).text(frequency);
        $('.statutorydate', clone2).text(statutorydate);
        $('.duedate', clone2).html('<input type="text" value="'+due_date+'" readonly="readonly" class="input-box" id="duedate'+statutoriesCount+'" />');
        $('.completiondate', clone2).html('<input type="text" value="" readonly="readonly" class="input-box" id="completiondate'+statutoriesCount+'" />');
        if(frequency == 'Periodical' || frequency == 'Review'){
          $('.validitydate', clone2).html('<input type="text" value="" class="input-box" readonly="readonly" id="validitydate'+statutoriesCount+'" />');
        }else{
          $('.validitydate', clone2).html("");
        }
        $('.documentupload', clone2).html('<input type="file" class="input-box" id="upload'+statutoriesCount+'" multiple />');
        $('.assignee', clone2).html('<input type="text" value="'+assignee_name+'" class="input-box icon-autocomplete" id="assigneeval'+statutoriesCount+'" style="width:100px;" /> <input type="hidden" id="assignee'+statutoriesCount+'" value="'+assignee_id+'"> <div id="autocomplete_assignee'+statutoriesCount+'" class="ac-textbox default-display-none"> <ul id="ulist_assignee'+statutoriesCount+'" style="width:115px;" class="hidemenu"></ul></div>');

        $('.completedstatus', clone2).html('<input type="checkbox" id="completedstatus'+statutoriesCount+'">');
        $('.tbody-assignstatutory').append(clone2);

        
        $("#upload"+statutoriesCount).on("change", function(e) {
        client_mirror.uploadFile(e, function result_data(data) {
          if(data != 'File max limit exceeded' || data != 'File content is empty'){
            uploadFile = data;
            file_list = data
          }
          else{
            file_list = [];
          }
         });
        });

        $("#duedate"+statutoriesCount).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        });

        $("#validitydate"+statutoriesCount ).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        });

        $("#completiondate"+statutoriesCount ).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        });

        $("#assigneeval"+statutoriesCount).keyup(function(){
        var textval = $(this).val();
        var text = $(this).attr('id');
        var clickvalue = text.substring(text.lastIndexOf('l') + 1);
        $("#autocomplete_assignee"+clickvalue).show();
        
        var assignees = usersList;
        var suggestions = [];
        $('#ulist_assignee'+clickvalue).empty();
        if(textval.length>0){
          for(var i in assignees){
            if (~assignees[i]["employee_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([assignees[i]["user_id"],assignees[i]["employee_name"]]); 
          }
          var str='';
          for(var i in suggestions){
                    str += '<li id="'+suggestions[i][0]+'"onclick="activate_assignee(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\','+clickvalue+')">'+suggestions[i][1]+'</li>';
                    
          }
          $('#ulist_assignee'+clickvalue).append(str);
          $("#assignee"+clickvalue).val('');
          }else{
            $("#assignee"+clickvalue).val('');
            $("#autocomplete_assignee"+clickvalue).hide();
          }
      });

        statutoriesCount = statutoriesCount + 1;
      }  
      actCount = actCount + 1;
      count++;
  }

  $(".hidemenu").click(function(){
    $(".ac-textbox").hide();
  });

  if(count <= 1){
    var tableRow4=$('#no-record-templates .table-no-content .table-row-no-content');
    var clone4=tableRow4.clone();
    $('.no_records', clone4).text('No Compliance Found');
    $('.tbody-assignstatutory').append(clone4);
    $('#activate-step-finish').hide();
  }
}


function validate_firsttab(){
  if($('.countrylist.active').text() == ''){
    displayMessage(message.country_required);
    return false;
  }else if ($('.legalentitylist.active').text() == ''){
    displayMessage(message.legalentity_required);
    return false;
  }else if ($('.unitlist.active').text() == ''){
    displayMessage(message.unit_required);
    return false;
  }else{
    displayMessage("");
    return true;
  }    
}

function validate_secondtab(){
  if($('.domainlist.active').text() == ''){
    displayMessage(message.domain_required);
    return false;
  }else{
    return true;
  }
}

function validate_thirdtab(){
  return true;
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

function submitcompliance(){
    displayLoader();
    var unit_id = parseInt($('.unitlist.active').attr('id'));;
    compliance_list = [];
    var statutoriesCount= 1;
    var actCount = 1;

    for(var entity in statutoriesList){
    var actCompliances = statutoriesList[entity]["compliences"];

      for(var ac in actCompliances){  
        var complianceApplicable = false;
        if($('#completedstatus'+statutoriesCount).is(":checked")){
          complianceApplicable = true;
        }
        if(complianceApplicable){
          var compliance_id = actCompliances[ac]["compliance_id"];
          var validity_date = $('#validitydate'+statutoriesCount).val();
          var due_date = $('#duedate'+statutoriesCount).val();
          var completion_date = $('#completiondate'+statutoriesCount).val();
          var completed_by = $('#assignee'+statutoriesCount).val();
          var frequency_ = actCompliances[ac]["frequency"];
          var compliance_name = actCompliances[ac]["compliance_name"];

          if(completed_by != '') completed_by = parseInt(completed_by);

          if(due_date == ''){
            displayMessage(message.duedate_required);
            hideLoader();
            return false;
          }
          else if(completion_date == ''){
            displayMessage(message.compliancedate_required);
            hideLoader();
            return false;
          }else if(validity_date == '' && frequency_ == 'Periodical'){
            displayMessage(message.validitydate_required);
            hideLoader();
            return false;
          }else if(completed_by == ''){
            displayMessage(message.assignee_required);
            hideLoader();
            return false;
          }else if(validity_date != '' && frequency_ == 'Periodical'){
            var convertDueDate = convert_date(due_date);
            var convertValidityDate = convert_date(validity_date);
            var dateDifference = daydiff(convertDueDate, convertValidityDate);
            if (convertDueDate > convertValidityDate) {
              displayMessage("Due date must be less than validity date for '" + compliance_name + "'");
              hideLoader();
              return false;
            }else if(dateDifference > 90){
              displayMessage("Invalid due date for '" + compliance_name + "'");
              hideLoader();
              return false;
            }else{
              displayMessage("");
            }
          }else{
            displayMessage("");
          }
          compliance = client_mirror.getPastRecordsComplianceDict(unit_id, compliance_id, due_date, completion_date, file_list, validity_date, completed_by);
          compliance_list.push(compliance);
        }
        statutoriesCount = statutoriesCount + 1;
      }  
      actCount = actCount + 1;
  }

  function onSuccess(data){
    $('ul.setup-panel li:eq(0)').addClass('active');
    $('ul.setup-panel li:eq(1)').addClass('disabled');
    $('ul.setup-panel li:eq(2)').addClass('disabled');
    $('ul.setup-panel li a[href="#step-1"]').trigger('click');
    $(".tbody-assignstatutory").find("tr").remove();
    load_firstwizard();
    hideLoader();
  }
  function onFailure(error){
    displayMessage(error[1]["error"]);
    hideLoader();
  }
  client_mirror.savePastRecords(compliance_list, 
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

var navListItems = $('ul.setup-panel li a'),
allWells = $('.setup-content');
allWells.hide();
navListItems.click(function(e)
{
e.preventDefault();
var $target = $($(this).attr('href')),
$item = $(this).closest('li');
if (!$item.hasClass('disabled')) {
navListItems.closest('li').removeClass('active');
$item.addClass('active');
allWells.hide();
$target.show();
}
});
$('ul.setup-panel li.active a').trigger('click');
$('#activate-step-2').on('click', function(e) {
if (validate_firsttab()){
$('ul.setup-panel li:eq(1)').removeClass('disabled');
$('ul.setup-panel li a[href="#step-2"]').trigger('click');
}
})

$('#activate-step-3').on('click', function(e) {
if (validate_secondtab()){
  getStatutories();
  $('#activate-step-finish').show();
  $('ul.setup-panel li:eq(2)').removeClass('disabled');
  $('ul.setup-panel li a[href="#step-3"]').trigger('click');
}
})

$('#backward-step-1').on('click', function(e) {
$('ul.setup-panel li:eq(1)').removeClass('disabled');
$('ul.setup-panel li a[href="#step-1"]').trigger('click');

})

$('#backward-step-2').on('click', function(e) {
  $('ul.setup-panel li:eq(2)').removeClass('disabled');
  $('ul.setup-panel li a[href="#step-2"]').trigger('click');

})

$('#activate-step-finish').on('click', function(e) {
  if (validate_thirdtab()){
  submitcompliance();
  }
})


function getStatutories(){
  displayLoader();
  var assignComplianceUnitId = null;
  var assignComplianceDomainId = null;
  var assignComplianceActId = null;
  var assignComplianceFrequencyId = null;
  var assignComplianceCountryId = null;

  if($('.countrylist.active').attr('id') != undefined) assignComplianceCountryId = parseInt($('.countrylist.active').attr('id'));
  if($('.unitlist.active').attr('id') != undefined) assignComplianceUnitId = parseInt($('.unitlist.active').attr('id'));
  if($('.domainlist.active').attr('id') != undefined) assignComplianceDomainId = parseInt($('.domainlist.active').attr('id'));
  if($('.actlist.active').attr('id') != undefined) assignComplianceActId = $('.actlist.active').attr('id');
  if($('.frequencylist.active').attr('id') != undefined) assignComplianceFrequencyId = $('.frequencylist.active').attr('id');
  
  if(assignComplianceUnitId != null && assignComplianceDomainId != null){
    function onSuccess(data){
    statutoriesList = data["statutory_wise_compliances"];
    usersList = data["users"];
    load_thirdwizard();
    hideLoader();
    }
    function onFailure(error){
      hideLoader();
    }
    client_mirror.getStatutoriesByUnit(assignComplianceUnitId, assignComplianceDomainId, assignComplianceActId, assignComplianceFrequencyId, assignComplianceCountryId,
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

function loadunit(){

  var assignStatutoryLegalEntityId = null;
  if($('.legalentitylist.active').attr('id') != undefined)
    assignStatutoryLegalEntityId = parseInt($('.legalentitylist.active').attr('id'));

  var assignStatutoryDivisionId = null;
  if($('.divisionlist.active').attr('id') != undefined)
    assignStatutoryDivisionId = parseInt($('.divisionlist.active').attr('id'));

  var assignStatutoryBusinessGroupId = null;
  if($('.businessgrouplist.active').attr('id') != undefined)
    assignStatutoryBusinessGroupId = parseInt($('.businessgrouplist.active').attr('id'));

  var assignStatutoryCountryId = parseInt($('.countrylist.active').attr('id'));

  if(assignStatutoryLegalEntityId != null){
      var str='';
      var splittext='';
      $('#unit').empty();
      for(var industryunit in unitsList){
        var iUnits = unitsList[industryunit]["units"];
        var iName = unitsList[industryunit]["industry_name"];
        splittext = '<h3 style="background-color:gray;padding:2px;font-size:13px;color:white;">'+iName+'</h3>';
        for(var unit in iUnits){
          if(iUnits[unit]["business_group_id"] == assignStatutoryBusinessGroupId && 
            iUnits[unit]["division_id"] == assignStatutoryDivisionId && 
            iUnits[unit]["legal_entity_id"] == assignStatutoryLegalEntityId && 
            iUnits[unit]["country_id"] == assignStatutoryCountryId){
            str += splittext + '<li id="'+iUnits[unit]["unit_id"]+'" class="unitlist" > <abbr class="page-load" title="'+
            iUnits[unit]["address"]+'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+ 
            iUnits[unit]["unit_name"]+'</li>';
            splittext = '';
        }
        }
      }
      $('#unit').append(str);
  }
}

$("#unit").click(function(event){
  if($(event.target).attr('class') == 'unitlist'){
    $('.'+$(event.target).attr('class')).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(event.target).addClass("active");
  }

  var assignStatutoryUnitId = parseInt($('.unitlist.active').attr('id'));
  var unitDomains = [];
  for(var industryunit in unitsList){
    var iUnits = unitsList[industryunit]["units"];
    for(var unit in iUnits){
      if(iUnits[unit]["unit_id"] == assignStatutoryUnitId){
        unitDomains = iUnits[unit]["domain_ids"];
    }
    }
  }

  var str='';
  $('#domain').empty();
  $('#act').empty();
  for(var domain in domainsList){
    if($.inArray(domainsList[domain]["domain_id"], unitDomains) >= 0){
      str += '<li id="'+domainsList[domain]["domain_id"]+'" class="domainlist" >'+domainsList[domain]["domain_name"]+'</li>';
    }
  }
  $('#domain').append(str);

  var str='';
  $('#frequency').empty();
  for(var frequency in frequencyList){
      str += '<li id="'+frequencyList[frequency]["frequency"]+'" class="frequencylist" >'+frequencyList[frequency]["frequency"]+'</li>';
    
  }
  $('#frequency').append(str);
  $('ul.setup-panel li:eq(2)').addClass('disabled');
});


$("#businessgroup").click(function(event){
  if($(event.target).attr('class') == 'businessgrouplist'){
    clearValues('businessgroup');
    $('.'+$(event.target).attr('class')).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(event.target).addClass("active");

    var str='';
    var assignStatutoryBusinessGroupId = parseInt(event.target.id);
    $('#legalentity').empty();
    for(var legalentity in legalentitiesList){
      if(legalentitiesList[legalentity]["business_group_id"] == assignStatutoryBusinessGroupId){
        str += '<li id="'+legalentitiesList[legalentity]["legal_entity_id"]+'" class="legalentitylist" >'+legalentitiesList[legalentity]["legal_entity_name"]+'</li>';
      }
    }
    $('#legalentity').append(str);
  }
});

$("#legalentity").click(function(event){
  if($(event.target).attr('class') == 'legalentitylist'){
    clearValues('legalentity');
    $('.'+$(event.target).attr('class')).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(event.target).addClass("active");
    var str='';
    var assignStatutoryLegalEntityId = parseInt(event.target.id);
    $('#division').empty();
    for(var division in divisionsList){
      if(divisionsList[division]["legal_entity_id"] == assignStatutoryLegalEntityId){
        str += '<li id="'+divisionsList[division]["division_id"]+'" class="divisionlist" >'+divisionsList[division]["division_name"]+'</li>';
      }
    }
    $('#division').append(str);
    loadunit();
  }
});

$("#division").click(function(event){
  if($(event.target).attr('class') == 'divisionlist'){
    clearValues('division');
    $('.'+$(event.target).attr('class')).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(event.target).addClass("active");
    loadunit();
  }
});

$("#country").click(function(event){
  if($(event.target).attr('class') == 'countrylist'){
      clearValues('country');
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");
  }

  var str='';
  $('#businessgroup').empty();
  for(var businessgroup in businessgroupsList){
      str += '<li id="'+businessgroupsList[businessgroup]["business_group_id"]+'" class="businessgrouplist" >'+businessgroupsList[businessgroup]["business_group_name"]+'</li>';
  }
  $('#businessgroup').append(str); 

  var str1='';
  $('#legalentity').empty();
  for(var legalentity in legalentitiesList){
    if(legalentitiesList[legalentity]["business_group_id"] == null){
      str1 += '<li id="'+legalentitiesList[legalentity]["legal_entity_id"]+'" class="legalentitylist" >'+legalentitiesList[legalentity]["legal_entity_name"]+'</li>';
    }
  }
  $('#legalentity').append(str1);
});


$("#domain").click(function(event){
  if($(event.target).attr('class') == 'domainlist'){
    $('.'+$(event.target).attr('class')).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(event.target).addClass("active");
  }

  var str='';
  var assignStatutoryDomainId = parseInt(event.target.id);
  $('#act').empty();
  for(act in actList){
    var domainAct = actList[act];
    if(act == assignStatutoryDomainId){
      for(var i=0; i < domainAct.length; i++){
        str += '<li id="'+domainAct[i]+'" class="actlist" >'+domainAct[i]+'</li>';
      }
    }
  }
  $('#act').append(str);
  $('ul.setup-panel li:eq(2)').addClass('disabled');
});

$("#act").click(function(event){
  if($(event.target).attr('class') == 'actlist'){
    $('.'+$(event.target).attr('class')).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(event.target).addClass("active");
  }
  $('ul.setup-panel li:eq(2)').addClass('disabled');
});

$("#frequency").click(function(event){
  if($(event.target).attr('class') == 'frequencylist'){
    $('.'+$(event.target).attr('class')).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(event.target).addClass("active");
  }
  $('ul.setup-panel li:eq(2)').addClass('disabled');
});

function load_firstwizard(){
  $('#businessgroup').empty();
  $('#legalentity').empty();
  $('#division').empty();
  $('#unit').empty();


  var str='';
  $('#country').empty();
    for(var country in countriesList){
      if(countriesList[country]["is_active"] == true){
      str += '<li id="'+countriesList[country]["country_id"]+'" class="countrylist">'+countriesList[country]["country_name"]+'</li>';
    }
  }
  $('#country').append(str);

  $('#assignee_unit').empty();
  $("#assignee_unit").append('<option value=""> Select </option>');
  $("#assignee_unit").append('<option value="all"> All </option>');
  for (var unitList in unitsList) {
    var option = $("<option></option>");
    option.val(unitsList[unitList]["unit_id"]);
    option.text(unitsList[unitList]["unit_name"]);
    $("#assignee_unit").append(option);
  }

  $('#concurrence_unit').empty();
  $("#concurrence_unit").append('<option value=""> Select </option>');
  $("#concurrence_unit").append('<option value="all"> All </option>');
  for (var unitList in unitsList) {
    var option = $("<option></option>");
    option.val(unitsList[unitList]["unit_id"]);
    option.text(unitsList[unitList]["unit_name"]);
    $("#concurrence_unit").append(option);
  }

  $('#approval_unit').empty();
  $("#approval_unit").append('<option value=""> Select </option>');
  $("#approval_unit").append('<option value="all"> All </option>');
  for (var unitList in unitsList) {
    var option = $("<option></option>");
    option.val(unitsList[unitList]["unit_id"]);
    option.text(unitsList[unitList]["unit_name"]);
    $("#approval_unit").append(option);
  }
}


function getPastRecords () {
  function onSuccess(data){
    countriesList = data["countries"];
    businessgroupsList = data["business_groups"];
    legalentitiesList = data["legal_entities"];
    divisionsList = data["divisions"];
    unitsList = data["industry_wise_units"];
    actList = data["level_1_statutories"];
    frequencyList = data["compliance_frequency"];
    domainsList = data["domains"];
    load_firstwizard();
  }
  function onFailure(error){
  }
  client_mirror.getPastRecordsFormData(
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

$(document).ready(function () {
  getPastRecords ();

  $("#filter_domain").keyup( function() {
    var filter = $("#filter_domain").val().toLowerCase();
    var lis = document.getElementsByClassName('domainlist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter)) 
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_act").keyup( function() {
    var filter = $("#filter_act").val().toLowerCase();
    var lis = document.getElementsByClassName('actlist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter)) 
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_frequency").keyup( function() {
    var filter = $("#filter_frequency").val().toLowerCase();
    var lis = document.getElementsByClassName('frequencylist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter)) 
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });


  $("#filter_country").keyup( function() {
    var filter = $("#filter_country").val().toLowerCase();
    var lis = document.getElementsByClassName('countrylist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter)) 
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_businessgroup").keyup( function() {
    var filter = $("#filter_businessgroup").val().toLowerCase();
    var lis = document.getElementsByClassName('businessgrouplist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter)) 
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_legalentity").keyup( function() {
    var filter = $("#filter_legalentity").val().toLowerCase();
    var lis = document.getElementsByClassName('legalentitylist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter)) 
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_division").keyup( function() {
    var filter = $("#filter_division").val().toLowerCase();
    var lis = document.getElementsByClassName('divisionlist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter)) 
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  
  $("#filter_unit").keyup( function() {
    var filter = $("#filter_unit").val().toLowerCase();
    var lis = document.getElementsByClassName('unitlist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter)) 
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

});

$( document ).tooltip({
    position: {
        my: "center bottom-20",
        at: "center top",
        using: function( position, feedback ) {
            $( this ).css( position );
            $( "<div>" )
                .addClass( "arrow" )
                .addClass( feedback.vertical )
                .addClass( feedback.horizontal )
                .appendTo( this );
        }
    }
});