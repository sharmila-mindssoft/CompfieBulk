var countriesList;
var businessgroupsList;
var legalentitiesList;
var divisionsList;
var unitsList;
var usersList;
var assignStatutoryUnitIds = [];
var assignStatutoryUnitValues = [];
var statutoriesList;
var two_level_approve;
var client_admin;
var domainsList;
var accordionstatus = true;

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

function clearValues(levelvalue) {
  if(levelvalue == 'country'){
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    $('#businessgroup').empty();
    $('#legalentity').empty();
    $('#division').empty();
    $('#unit').empty();
  }

  if(levelvalue == 'businessgroup'){
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    $('#legalentity').empty();
    $('#division').empty();
    $('#unit').empty();
  }

  if(levelvalue == 'legalentity'){
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    $('#division').empty();
    $('#unit').empty();
  }

  if(levelvalue == 'division'){
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    $('#unit').empty();
  }

  if(levelvalue == 'unit'){
    $('#domain').empty();
  }
}

function actstatus(element){
  var changestatusStatutories = '.statutoryclass'+$(element).val();
  if ($(element).is(":checked"))
  {
    $(changestatusStatutories).each(function() {
      this.checked = true;
    });
  }else{
    $(changestatusStatutories).each(function() {
      this.checked = false;
    });
  }
  accordionstatus = false;
}

function compliancestatus(element){
  var sClass = $(element).attr('class');
  var actSelect = sClass.substr(sClass.lastIndexOf("s") + 1);

  var cStatus = false;
  $('.'+sClass).each(function() {
    if(this.checked){
      cStatus = true;
    }
  });

  if(cStatus){
    $('#act'+actSelect).prop("checked",true);
  }else{
    $('#act'+actSelect).prop("checked",false);
  }
}

function disppopup(units){
  $("#popup1").show();
  $(".popup-list tr:gt(0)").remove();
  for(var i=0; i<units.length; i++){
    var dispUnit = '';
    $.each(unitsList, function(index, value) {
    if (value.unit_id == units[i]) {
        dispUnit = value.unit_name + ' - ' + value.address;
        var popuptableRow=$('#popup_table .popup_row');
        var clone=popuptableRow.clone();
        $(".popup_unitname",clone).text(dispUnit);
        $('#popup_table').append(clone);
    }
    });
  }
}

function load_secondwizard(){
  var count=1;
  var statutoriesCount= 1;
  var actCount = 1;
  $(".tbody-assignstatutory").find("tbody").remove();

  var selectedDomain = $('.domainlist.active').attr('id');

  if(selectedDomain in statutoriesList){

    var actname = '';
    var domainList = statutoriesList[selectedDomain];
    for(var domainentity in domainList){
      actname = domainentity;
      var acttableRow=$('#act-templates .font1 .tbody-heading');
      var clone=acttableRow.clone();
      $('.actname', clone).html('<input style="margin-top:5px" type="checkbox" checked="checked" id="act'+actCount+'" value="'+actCount+'" onclick="actstatus(this)"> <label for="act'+actCount+'">'+actname+'</label> <span><img src="/images/chevron_black_down.png"></span>');
      $('.tbody-assignstatutory').append(clone);

      $('.tbody-assignstatutory').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
      if(count==1){
        $('.accordion-content'+count).addClass("default");
      }

      var complianceHeadingtableRow=$('#statutory-templates .compliance-heading');
      var clone1=complianceHeadingtableRow.clone();
      $('.accordion-content'+count).append(clone1);

      var actList = domainList[domainentity];
      //$('.tbody-assignstatutory').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
      for(var actentity in actList){
        var statutoryprovision = '';
        var compliance_id = actList[actentity]["compliance_id"];
        var compliance_name = actList[actentity]["compliance_name"];
        var compliance_description = actList[actentity]["description"];
        var applicable_units =  actList[actentity]["applicable_units"];
        var frequency =  actList[actentity]["frequency"];
        var statutory_date =  actList[actentity]["statutory_date"];
        var due_date =  actList[actentity]["due_date"];
        var summary = actList[actentity]["summary"];
        var triggerdate = '';
        var statutorydate = '';
        var elementTriggerdate = '';
        var elementDuedate = '';

        if(due_date != ''){
          if(due_date.length > 1){
          for(var k = 0; k < due_date.length; k++){
            elementDuedate += '<input type="text" id="duedate'+statutoriesCount+'-'+k+'" readonly="readonly" class="input-box" value="' + due_date[k] + '"/>';
          }
          }else{
            elementDuedate += '<input type="text" id="duedate'+statutoriesCount+'" readonly="readonly" class="input-box" value="' + due_date[0] + '"/>'
          }
        }
        for(j = 0; j < statutory_date.length; j++){
          var sDay = '';
          if(statutory_date[j]["statutory_date"] != null) sDay = statutory_date[j]["statutory_date"];

          var sMonth = '';
          if(statutory_date[j]["statutory_month"] != null) sMonth = statutory_date[j]["statutory_month"];

          var tDays = '';
          if(statutory_date[j]["trigger_before_days"] != null) tDays = statutory_date[j]["trigger_before_days"];

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

          if(tDays != ''){
            triggerdate +=  tDays + " Day(s) ";
          }
          statutorydate +=  sMonth +' '+ sDay + ' ';

          if(statutory_date.length > 1){
            elementTriggerdate += '<input type="text" id="triggerdate'+statutoriesCount+'-'+j+'" class="input-box trigger" value="' + tDays + '" maxlength="3" style="width:50px; float:left;"/>';
          }else{
            elementTriggerdate += '<input type="text" id="triggerdate'+statutoriesCount+'" class="input-box trigger" value="' + tDays + '" maxlength="3" style="width:50px; float:left;"/>';
          }
        }

        var complianceDetailtableRow=$('#statutory-values .table-statutory-values .compliance-details');
        var clone2=complianceDetailtableRow.clone();
        $('.ckbox', clone2).html('<input type="checkbox" checked="checked" id="statutory'+statutoriesCount+'" class="statutoryclass'+actCount+'" onclick="compliancestatus(this)">');
        $('.compliancetask', clone2).html('<abbr class="page-load" title="'+
          compliance_description+'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+compliance_name);

        var dispApplicableUnits = applicable_units.length + '/' + assignStatutoryUnitIds.length;
        $('.applicableunit', clone2).html('<a href="#popup1" onclick="disppopup(\''+applicable_units+'\')">'+dispApplicableUnits+'</a>');
        $('.compliancefrequency', clone2).text(frequency);

        if(summary != null){
          if(statutorydate != ''){
            statutorydate = summary + ' ( '+statutorydate+' )';
          }else{
            statutorydate = summary;
          }
        }

        $('.statutorydate', clone2).text(statutorydate);

        if(frequency != 'On Occurrence'){
          if(triggerdate == ''){
          $('.triggerbefore', clone2).html('<input type="text" value="" class="input-box trigger" id="triggerdate'+statutoriesCount+'" />');
          $('.duedate', clone2).html('<input type="text" value="" class="input-box" id="duedate'+statutoriesCount+'" />');
          }
          else{
            $('.triggerbefore', clone2).html('<span style="float:right;padding-right:30px;" class="edittrigger'+statutoriesCount+'" value="'+statutoriesCount+'"><img src="/images/icon-edit.png" width="12"></span> <span style="float:right;display: none;padding-right:30px;" class="closetrigger'+statutoriesCount+'" value="'+statutoriesCount+'"><img src="/images/delete.png" width="12"></span>'+triggerdate +
              '<div class="edittriggertextbox'+statutoriesCount+'" style="display:none;padding-top:10px;">' + elementTriggerdate + '</div>');
            $('.duedate', clone2).html('<div>' + elementDuedate + '</div>');
          }
        }

        if(frequency == 'Periodical' || frequency == 'Review'){
          $('.validitydate', clone2).html('<input type="text" value="" class="input-box" readonly="readonly" id="validitydate'+statutoriesCount+'" />');
        }

        $('.accordion-content'+count).append(clone2);


        var duename = statutoriesCount;
        if(due_date.length > 1){
          for(var k = 0; k < due_date.length; k++){
            duename = statutoriesCount+'-'+k;
            $("#duedate"+duename).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
          });
          }
        }else{
          $("#duedate"+duename).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        });
        }
        $("#validitydate"+statutoriesCount ).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        });

        $('.edittrigger'+statutoriesCount).click(function(){
          var text = $(this).attr('class');
          var clickvalue = text.substring(text.lastIndexOf('r') + 1);
          $('.edittriggertextbox'+clickvalue).show();
          $('.closetrigger'+clickvalue).show();
          $('.edittrigger'+clickvalue).hide();
        });

        $('.closetrigger'+statutoriesCount).click(function(){
          var text = $(this).attr('class');
          var clickvalue = text.substring(text.lastIndexOf('r') + 1);
          $('.edittriggertextbox'+clickvalue).hide();
          $('.edittrigger'+clickvalue).show();
          $('.closetrigger'+clickvalue).hide();
        });

        $('.trigger').keyup('input', function (event) {
          this.value = this.value.replace(/[^0-9]/g, '');
        });

        statutoriesCount = statutoriesCount + 1;
      }
      actCount = actCount + 1;
      count++;
    }
  }
  if(count <= 1){
    var norecordtableRow=$('#no-record-templates .font1');
    var noclone=norecordtableRow.clone();
    $('.tbody-assignstatutory').append(noclone);
    $('#activate-step-3').hide();
  }

  $(document).ready(function($) {
    $('#accordion').find('.accordion-toggle').click(function(){
      if(accordionstatus){
        //Expand or collapse this panel
        $(this).next().slideToggle('fast');
        //Hide the other panels
        $(".accordion-content").not($(this).next()).slideUp('fast');
      }else{
        accordionstatus = true;
      }

    });
  });
}



function validate_firsttab(){
  if($('.countrylist.active').text() == ''){
    displayMessage("Country Required");
    return false;
  }else if ($('.legalentitylist.active').text() == ''){
    displayMessage("Legal Entity Required");
    return false;
  }else if (assignStatutoryUnitIds.length == 0){
    displayMessage("Unit Required");
    return false;
  }else if ($('.domainlist.active').text() == ''){
    displayMessage("Domain Required");
    return false;
  }else{
    displayMessage("");
    displayLoader();
    if(assignStatutoryUnitIds.length > 0){
      function onSuccess(data){
        statutoriesList = data["statutories"];
        load_secondwizard();
        hideLoader();
      }
      function onFailure(error){
        hideLoader();
      }
      client_mirror.getAssignComplianceForUnits(assignStatutoryUnitIds,
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
    return true;
  }
}

function validate_secondtab(){
  return true;
}

function validate_thirdtab(){
  if($('.assigneelist.active').text() == ''){
    displayMessage("Assignee Required");
    return false;
  }else if ($(".assigneelist.active").text().trim() == 'Client Admin'){
    displayMessage("");
    return true;
  }else if ($('.concurrencelist.active').text() == '' && two_level_approve){
    displayMessage("Concurrence Required");
    return false;
  }else if ($('.approvallist.active').text() == ''){
    displayMessage("Approval Required");
    return false;
  }else{
    displayMessage("");
    return true;
  }
  //return true;
}

function convert_month (data){
  var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var rmonth;
  for(var j=0;j<months.length;j++){
      if(data == months[j]){
           rmonth = months.indexOf(months[j])+1;
       }
  }
  return rmonth;
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


function submitcompliance(){

    displayLoader();
    var assignComplianceCountryId = null;
    var assignComplianceAssigneeId = null;
    var assignComplianceConcurrenceId = null;
    var assignComplianceApprovalId = null;
    var assignComplianceAssigneeName = null;
    var assignComplianceConcurrenceName = null;
    var assignComplianceApprovalName = null;
    var currentDate = new Date();

    assignComplianceCountryId = parseInt($('.countrylist.active').attr('id'));


    if($('.assigneelist.active').attr('id') != undefined){
      assignComplianceAssigneeId = parseInt($('.assigneelist.active').attr('id'));
      assignComplianceAssigneeName = $('.assigneelist.active').text().trim();
    }

    if($('.concurrencelist.active').attr('id') != undefined){
      assignComplianceConcurrenceId = parseInt($('.concurrencelist.active').attr('id'));
      assignComplianceConcurrenceName = $('.concurrencelist.active').text().trim();
    }

    if($('.approvallist.active').attr('id') != undefined){
      assignComplianceApprovalId = parseInt($('.approvallist.active').attr('id'));
      assignComplianceApprovalName = $('.approvallist.active').text().trim();
    }

    if(assignComplianceAssigneeName == 'Client Admin'){
      assignComplianceApprovalId = assignComplianceAssigneeId;
      assignComplianceApprovalName = assignComplianceAssigneeName;
    }

    assignCompliance = [];
    var statutoriesCount= 1;
    var actCount = 1;

    var applicableUnitsArray = [];

    for(var entity in statutoriesList){

      var domainList = statutoriesList[entity];
      for(var domainentity in domainList){
        var actList = domainList[domainentity];
        for(var actentity in actList){
          var complianceApplicable = false;
          if($('#statutory'+statutoriesCount).is(":checked")){
            complianceApplicable = true;
          }
          if(complianceApplicable){
            var compliance_id = actList[actentity]["compliance_id"];
            var compliance_name = actList[actentity]["compliance_name"];
            var applicable_units =  actList[actentity]["applicable_units"];
            var due_date =  actList[actentity]["due_date"];
            var frequency =  actList[actentity]["frequency"];

            for(var k=0; k<applicable_units.length; k++ ){
              if($.inArray(applicable_units[k], applicableUnitsArray) == -1){
                applicableUnitsArray.push(applicable_units[k]);
              }
            }

            var statutory_dates = [];
            var current_due_date = '';
            var current_trigger_day = '';
            var current_due_dates = [];


            var validitydate = null;
            if($('#validitydate'+statutoriesCount).val() != undefined && $('#validitydate'+statutoriesCount).val() != '') validitydate = $('#validitydate'+statutoriesCount).val();


            if(frequency != 'On Occurrence'){
              if(due_date.length > 1){
                for(var k = 0; k < due_date.length; k++){
                var dDate = null;
                var tDay = null;

                dDate = $('#duedate'+statutoriesCount+'-'+k).val();
                tDay = $('#triggerdate'+statutoriesCount+'-'+k).val();
                current_due_dates.push([dDate,tDay]);
                }
              }else{
                dDate = $('#duedate'+statutoriesCount).val();
                tDay = $('#triggerdate'+statutoriesCount).val();
                current_due_dates.push([dDate,tDay]);
              }
              var convertDueDate = convert_date(dDate);
              if (convertDueDate <= currentDate) {
                  displayMessage("Due date is less than today's date for compliance '" + compliance_name + "'");
                  hideLoader();
                  return false;
              }

              var sort_elements = current_due_dates;
                if(current_due_dates.length > 1){
                  sort_elements.sort(function(a, b) {
                    a1 = convert_date(a[0]);
                    b1 = convert_date(b[0]);
                  return a1 - b1;
                  });

                current_due_date = sort_elements[0][0];
                current_trigger_day = parseInt(sort_elements[0][1]);
            }else{
              current_due_date = current_due_dates[0][0];
              current_trigger_day = parseInt(sort_elements[0][1]);
            }


            for(var dDates = 0; dDates < sort_elements.length; dDates++){
              var statutory_day = null;
              var statutory_month = null;
              var trigger_before_days = null;
              if(sort_elements[dDates][0] != ''){
                var splitDueDates = sort_elements[dDates][0].split('-');
                var strMonth = splitDueDates[1];
                statutory_day = parseInt(splitDueDates[0]);
                statutory_month = convert_month(strMonth);
                trigger_before_days = sort_elements[dDates][1];

                if(trigger_before_days != '') {
                  trigger_before_days = parseInt(trigger_before_days);
                  if(trigger_before_days > 100){
                    displayMessage("Trigger days should not be exceed 100");
                    hideLoader();
                    return false;
                  }
                  if(trigger_before_days == 0){
                    displayMessage("Trigger days should be 1 to 100");
                    hideLoader();
                    return false;
                  }
                }else{
                  displayMessage("Trigger date Required in Select Compliance Task Wizard");
                  hideLoader();
                  return false;
                }
              }
              statutoryDateList = client_mirror.statutoryDates(statutory_day, statutory_month, trigger_before_days);
              statutory_dates.push(statutoryDateList);
            }
            }
            else{
              var statutory_dates = null;
              var current_due_date = null;
              var current_trigger_day = null;
            }
            assignComplianceData = client_mirror.assignCompliances(
            compliance_id, compliance_name, statutory_dates,
            current_due_date, validitydate, current_trigger_day, applicable_units
           );
            assignCompliance.push(assignComplianceData);
          }
          statutoriesCount = statutoriesCount + 1;
        }
        actCount = actCount + 1;
      }
    }

var assigneeInserUnits = [];
var assigneeInserUnitsVal = [];

if(assignComplianceAssigneeName != 'Client Admin' && assignComplianceAssigneeId != null){
  var userUnits;
  var userDomains;
  for(var user in usersList){
    if(usersList[user]["user_id"] == assignComplianceAssigneeId){
      userUnits = usersList[user]["unit_ids"];
      userDomains = usersList[user]["domain_ids"];
    }
  }

  for(var k=0; k<applicableUnitsArray.length; k++){
    if($.inArray(applicableUnitsArray[k], userUnits) == -1){
      assigneeInserUnits.push(applicableUnitsArray[k]);
      for(var unit in unitsList){
        if(unitsList[unit]["unit_id"] == applicableUnitsArray[k]){
          assigneeInserUnitsVal.push(unitsList[unit]["unit_name"])
        }
      }
    }
  }
}

var concurrenceInserUnits = [];
var concurrenceInserUnitsVal = [];

if(assignComplianceConcurrenceId != null){
  var userUnits;
  var userDomains;
  for(var user in usersList){
    if(usersList[user]["user_id"] == assignComplianceConcurrenceId){
      userUnits = usersList[user]["unit_ids"];
      userDomains = usersList[user]["domain_ids"];
    }
  }

  for(var k=0; k<applicableUnitsArray.length; k++){
    if($.inArray(applicableUnitsArray[k], userUnits) == -1){
      assigneeInserUnits.push(applicableUnitsArray[k]);
      for(var unit in unitsList){
        if(unitsList[unit]["unit_id"] == applicableUnitsArray[k]){
          concurrenceInserUnitsVal.push(unitsList[unit]["unit_name"])
        }
      }
    }
  }
}

var approvalInserUnits = [];
var approvalInserUnitsVal = [];


if(assignComplianceApprovalName != 'Client Admin' && assignComplianceApprovalId != null){
  var userUnits;
  var userDomains;
  for(var user in usersList){
    if(usersList[user]["user_id"] == assignComplianceApprovalId){
      userUnits = usersList[user]["unit_ids"];
      userDomains = usersList[user]["domain_ids"];
    }
  }

  for(var k=0; k<applicableUnitsArray.length; k++){
    if($.inArray(applicableUnitsArray[k], userUnits) == -1){
      assigneeInserUnits.push(applicableUnitsArray[k]);
      for(var unit in unitsList){
        if(unitsList[unit]["unit_id"] == applicableUnitsArray[k]){
          approvalInserUnitsVal.push(unitsList[unit]["unit_name"])
        }
      }
    }
  }
}

if(assigneeInserUnits.length > 0 || concurrenceInserUnits.length >0 || approvalInserUnits.length >0){
  var assigneeText = '';
  var concurrenceText = '';
  var approvalText = '';
  if(assigneeInserUnits.length > 0){
    assigneeText = assigneeInserUnitsVal + " unit(s) not applicable for Assignee. "
  }
  if(concurrenceInserUnits.length > 0){
    concurrenceText = concurrenceInserUnitsVal + " unit(s) not applicable for Concurrence. "
  }
  if(approvalInserUnits.length > 0){
    approvalText = approvalInserUnitsVal + " unit(s) not applicable for Approval. "
  }

  var answer = confirm(assigneeText + concurrenceInserUnits + approvalInserUnits + 'Do you want to add in settings ?');
  if (answer)
  {
    function onSuccess(data){
    //getAssignedStatutories ();
    $('ul.setup-panel li:eq(0)').addClass('active');
    $('ul.setup-panel li:eq(1)').addClass('disabled');
    $('ul.setup-panel li:eq(2)').addClass('disabled');
    $('ul.setup-panel li a[href="#step-1"]').trigger('click');
    $(".tbody-assignstatutory").find("tbody").remove();
    $('#assignee').empty();
    $('#concurrence').empty();
    $('#approval').empty();
    load_firstwizard();
    hideLoader();
  }
  function onFailure(error){
    displayMessage(error);
    hideLoader();
  }
  client_mirror.saveAssignedComplianceFormData(assignComplianceCountryId, assignComplianceAssigneeId,
    assignComplianceAssigneeName, assignComplianceConcurrenceId, assignComplianceConcurrenceName,
    assignComplianceApprovalId, assignComplianceApprovalName, assignCompliance,
    function (error, response) {
    if (error == null){
      onSuccess(response);
    }
    else {
      onFailure(error);
    }
  }
  );
  }else{
    hideLoader();
  }
}else{
  function onSuccess(data){
    //getAssignedStatutories ();
    $('ul.setup-panel li:eq(0)').addClass('active');
    $('ul.setup-panel li:eq(1)').addClass('disabled');
    $('ul.setup-panel li:eq(2)').addClass('disabled');
    $('ul.setup-panel li a[href="#step-1"]').trigger('click');
    $(".tbody-assignstatutory").find("tbody").remove();
    $('#assignee').empty();
    $('#concurrence').empty();
    $('#approval').empty();
    load_firstwizard();
    hideLoader();
  }
  function onFailure(error){
    displayMessage(error);
    hideLoader();
  }
  client_mirror.saveAssignedComplianceFormData(assignComplianceCountryId, assignComplianceAssigneeId,
    assignComplianceAssigneeName, assignComplianceConcurrenceId, assignComplianceConcurrenceName,
    assignComplianceApprovalId, assignComplianceApprovalName, assignCompliance,
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
      $('#unit').empty();
      for(var unit in unitsList){
        if(unitsList[unit]["business_group_id"] == assignStatutoryBusinessGroupId &&
          unitsList[unit]["division_id"] == assignStatutoryDivisionId &&
          unitsList[unit]["legal_entity_id"] == assignStatutoryLegalEntityId &&
          unitsList[unit]["country_id"] == assignStatutoryCountryId){
          str += '<li id="'+unitsList[unit]["unit_id"]+'" class="unitlist" > <abbr class="page-load" title="'+
          unitsList[unit]["address"]+'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+
          unitsList[unit]["unit_name"]+'</li>';
        }
      }
      $('#unit').append(str);
  }
}

$("#unit").click(function(event){
    var chkstatus = $(event.target).attr('class');
    $('#activate-step-3').show();
    if(chkstatus != undefined && chkstatus != 'active'){
      clearValues('unit');
      if(chkstatus == 'unitlist active'){
        $(event.target).removeClass("active");
        var removeid = assignStatutoryUnitIds.indexOf(parseInt(event.target.id));
        assignStatutoryUnitIds.splice(removeid,1);
        var removename = assignStatutoryUnitValues.indexOf($(event.target).text());
        assignStatutoryUnitValues.splice(removename,1);
      }else{
        $(event.target).addClass("active");
        assignStatutoryUnitIds.push(parseInt(event.target.id));
        assignStatutoryUnitValues.push($(event.target).text());
      }

      var domainArray = [];
      var applicableDomains = [];
      for(var unit in unitsList){
        if($.inArray(unitsList[unit]["unit_id"], assignStatutoryUnitIds) >= 0){
          domainArray.push(unitsList[unit]["domain_ids"]);
        }
      }

      if(domainArray.length > 0){
        applicableDomains = domainArray.shift().filter(function(v) {
        return domainArray.every(function(a) {
            return a.indexOf(v) !== -1;
        });
      });
      var str='';
      $('#domain').empty();
      for(var domain in domainsList){
        if(domainsList[domain]["is_active"] == true && $.inArray(domainsList[domain]["domain_id"], applicableDomains) >= 0){
          str += '<li id="'+domainsList[domain]["domain_id"]+'" class="domainlist" >'+domainsList[domain]["domain_name"]+'</li>';
        }
      }
      $('#domain').append(str);
      }else{
        $('#domain').empty();
      }
      $('ul.setup-panel li:eq(1)').addClass('disabled');
      $('ul.setup-panel li:eq(2)').addClass('disabled');
    }
});

$("#domain").click(function(event){
  if($(event.target).attr('class') == 'domainlist'){
    $('.'+$(event.target).attr('class')).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(event.target).addClass("active");
  }
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
  if($(event.target).attr('class') != undefined){
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
  }
});


function getUserLevel(selectedUserId){
  var getuserLevel = null;
  for(var user in usersList){
    var userId= usersList[user]["user_id"];
    if(userId == selectedUserId){
      getuserLevel = usersList[user]["user_level"];
    }
  }
  return getuserLevel;
}

function loadUser(userType){
  var selectedUnit = null;
  var userClass;
  var temp_assignee = null;
  var temp_concurrence = null;
  var temp_approval = null;
  //var temp_id = null;

  if(userType == 'assignee'){
    selectedUnit = $("#assignee_unit").val();
    userClass = 'assigneelist';
    /*if($('.assigneelist.active').attr('id') != undefined)
      temp_id = parseInt($('.assigneelist.active').attr('id'));*/
  }
  else if(userType == 'concurrence'){
    selectedUnit = $("#concurrence_unit").val();
    userClass = 'concurrencelist';
    /*if($('.concurrencelist.active').attr('id') != undefined)
      temp_id = parseInt($('.concurrencelist.active').attr('id'));*/
  }
  else{
    selectedUnit = $("#approval_unit").val();
    userClass = 'approvallist';
    /*if($('.approvallist.active').attr('id') != undefined)
      temp_id = parseInt($('.approvallist.active').attr('id'));*/
  }

  $('#'+userType).empty();

  var assigneeUserId = null;
  if($('.assigneelist.active').attr('id') != undefined)
    assigneeUserId = parseInt($('.assigneelist.active').attr('id'));

  var concurrenceUserId = null;
  if($('.concurrencelist.active').attr('id') != undefined)
    concurrenceUserId = parseInt($('.concurrencelist.active').attr('id'));

  var approvalUserId = null;
  if($('.approvallist.active').attr('id') != undefined)
    approvalUserId = parseInt($('.approvallist.active').attr('id'));


  var conditionResult = true;
  var conditionResult1 = true;
  var userLevel = null;
  var userLevel1 = null;

  if(userType == 'assignee' && (concurrenceUserId != null || approvalUserId != null)){
    if(concurrenceUserId != null){
      userLevel = getUserLevel(concurrenceUserId);
    }else{
      userLevel = getUserLevel(approvalUserId);
    }
  }else if(userType == 'concurrence' && (assigneeUserId != null || approvalUserId != null)){
    if(assigneeUserId != null){
      userLevel = getUserLevel(assigneeUserId);
    }
    if(approvalUserId != null){
      userLevel1 = getUserLevel(approvalUserId);
    }
  }else if(userType == 'approval' && (concurrenceUserId != null || assigneeUserId != null)){
    if(concurrenceUserId != null){
      userLevel = getUserLevel(concurrenceUserId);
    }else{
      userLevel = getUserLevel(assigneeUserId);
    }
  }

  var str='';
  if(userType != 'concurrence' && selectedUnit != ''){
    if((assigneeUserId == null || assigneeUserId != client_admin)
    && (approvalUserId == null || approvalUserId != client_admin)
    && (concurrenceUserId == null || concurrenceUserId != client_admin)){
      /*if(temp_id == client_admin){
        str='<li id="'+client_admin+'" class="'+userClass+' active" > Admin </li>';
      }else{
        str='<li id="'+client_admin+'" class="'+userClass+'" > Admin </li>';
      }*/
      str='<li id="'+client_admin+'" class="'+userClass+'" > Client Admin </li>';
    }
  }
  for(var user in usersList){
    var userUnits = usersList[user]["unit_ids"];
    if( selectedUnit == 'all' || $.inArray(parseInt(selectedUnit), userUnits) >= 0){
      var userId= usersList[user]["user_id"];
      var uLevel = usersList[user]["user_level"];
      var userName= usersList[user]["user_name"] + ' - Level ' + uLevel;

      if(userLevel != null){
        if(userType == 'assignee'){
          conditionResult = (uLevel >= userLevel);
        }
        else if(userType == 'concurrence'){
          conditionResult = (uLevel <= userLevel);
        }
        else if(userType == 'approval'){
          conditionResult = (uLevel <= userLevel);
        }
      }

      if(userType == 'concurrence' && userLevel1 != null){
          conditionResult1 = (uLevel >= userLevel1);
      }

      if(conditionResult && conditionResult1 && (assigneeUserId == null || assigneeUserId != userId)
        && (approvalUserId == null || approvalUserId != userId)
        && (concurrenceUserId == null || concurrenceUserId != userId)){
        /*if(temp_id == userId){
          str += '<li id="'+userId+'" class="'+userClass+ ' active'+'" >'+userName+'</li>';
        }else{
          str += '<li id="'+userId+'" class="'+userClass+'" >'+userName+'</li>';
        }*/
        str += '<li id="'+userId+'" class="'+userClass+'" >'+userName+'</li>';
      }
    }
  }
  $('#'+userType).append(str);
}

$("#assignee").click(function(event){
  var chkstatus = $(event.target).attr('class');
  if(chkstatus != undefined){
    if(chkstatus == 'assigneelist active'){
      $(event.target).removeClass("active");
    }else{
      $('.assigneelist').each( function( index, el ) {
        $(el).removeClass( "active" );
      });
      $(event.target).addClass("active");
    }
    var assigneeText = $(".assigneelist.active").text().trim();
    if(assigneeText != 'Client Admin'){
      loadUser('concurrence');
      loadUser('approval');
    }else{
      $('#concurrence').empty();
      $('#approval').empty();
    }
  }
});

$("#concurrence").click(function(event){
  var chkstatus = $(event.target).attr('class');
  if(chkstatus != undefined){
    if(chkstatus == 'concurrencelist active'){
      $(event.target).removeClass("active");
    }else{
      $('.concurrencelist').each( function( index, el ) {
        $(el).removeClass( "active" );
      });
      $(event.target).addClass("active");
    }
    //loadUser('assignee');
    loadUser('approval');
  }
});

$("#approval").click(function(event){
  var chkstatus = $(event.target).attr('class');
  if(chkstatus != undefined){
    if(chkstatus == 'approvallist active'){
      $(event.target).removeClass("active");
    }else{
      $('.approvallist').each( function( index, el ) {
        $(el).removeClass( "active" );
      });
      $(event.target).addClass("active");
    }

    //loadUser('assignee');
    //loadUser('concurrence');
  }
});

$('#assignee_unit').change(function() {
    loadUser('assignee');
});

$('#concurrence_unit').change(function() {
    loadUser('concurrence');
});

$('#approval_unit').change(function() {
    loadUser('approval');
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

  if(two_level_approve){
    $('.c-view').show();
  }else{
    $('.c-view').hide();
  }
}

function getAssignCompliances () {
  function onSuccess(data){
    countriesList = data["countries"];
    businessgroupsList = data["business_groups"];
    legalentitiesList = data["legal_entities"];
    divisionsList = data["divisions"];
    unitsList = data["units"];
    usersList = data["users"];
    two_level_approve = data["two_level_approve"];
    client_admin = data["client_admin"];
    domainsList = data["domains"];
    load_firstwizard();
  }
  function onFailure(error){
  }
  client_mirror.getAssignComplianceFormData(
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
  getAssignCompliances ();
  $("#filter_assignee").keyup( function() {
    var filter = $("#filter_assignee").val().toLowerCase();
    var lis = document.getElementsByClassName('assigneelist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_concurrence").keyup( function() {
    var filter = $("#filter_concurrence").val().toLowerCase();
    var lis = document.getElementsByClassName('concurrencelist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_approval").keyup( function() {
    var filter = $("#filter_approval").val().toLowerCase();
    var lis = document.getElementsByClassName('approvallist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

$('.edittrigger').click(function(){
      $('.edittriggertextbox').show();
      $('.edittrigger').hide();
      $('.closetrigger').show();
  });
  $('.closetrigger').click(function(){
      $('.edittriggertextbox').hide();
      $('.edittrigger').show();
      $('.closetrigger').hide();
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