var assignedStatutoriesList;
var newCompliancesList;
var groupcompaniesList;
var businessgroupsList;
var legalentitiesList;
var divisionsList;
var geographyLevelsList;
var geographiesList;
var industriesList;
var domainsList;
var unitsList;
var statutoriesList;
var assignStatutoryUnitIds = [];
var assignStatutoryUnitValues = [];

function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}


function actstatus(element){
  var remarkbox = '.remark'+$(element).val();
  var changestatusStatutories = '.statutoryclass'+$(element).val();
  if ($(element).is(":checked"))
  {
    $(remarkbox).hide();
    $(changestatusStatutories).each(function() { 
      this.checked = true;           
    });
  }else{
    $(remarkbox).show();
    $(changestatusStatutories).each(function() {
      this.checked = false;                     
    });  
  }
}


function load_statutory(sList, dispBusinessGroup, dispLegalEntity, dispDivision, dispUnit){
  var count=1;
  var statutoriesCount= 1;
  var actCount = 1;

  $(".tbl_businessgroup").text(dispBusinessGroup);
  $(".tbl_legalentity").text(dispLegalEntity);
  $(".tbl_division").text(dispDivision);
  $(".tbl_unit").text(dispUnit);

  $(".tbody-statutorysettings").find("tbody").remove();

  $.each(sList, function(key, value){

  var tableRow3=$('#head-templates');
  var clone3=tableRow3.clone();
  $('.tbl_heading', clone3).html('<div class="heading" style="margin-top:20px;margin-bottom:5px;">'+key+'</div>');
  $('.tbody-statutorysettings').append(clone3);
    for(var statutory in value){
      var actname = value[statutory]["level_1_statutory_name"];
      var complianceslist = value[statutory]["compliances"];
      var level_1_statutory_id = value[statutory]["level_1_statutory_id"];
      var applicable_status = value[statutory]["applicable_status"];
      var not_applicable_remarks = value[statutory]["not_applicable_remarks"];
      if (not_applicable_remarks == null) not_applicable_remarks = '';
      var acttableRow=$('#act-templates .font1 .tbody-heading');
      var clone=acttableRow.clone();
      $('.actapplicable', clone).html('<input type="checkbox" checked="checked" id="act'+actCount+'" value="'+actCount+'" onclick="actstatus(this)" style="margin-top:100px;"> <label for="act'+actCount+'" style="margin-top:100px;"></label> ');
      $('.actname', clone).html('<div style="float:left;margin-top:5px;">'+actname+'</div> <div style="float:right; width:500px;" class="default-display-none remark'+actCount+'" ><div style="float:right;  width:250px;margin-top:-3px;"> <input type="text" maxlength="250" id="remarkvalue'+actCount+'" value="'+not_applicable_remarks+'" class="input-box" style="width:200px;" placeholder="Enter Remarks" ></div><div style="float:right; width:70px;margin-top:5px;"> Remarks</div></div>');
      $('.tbody-statutorysettings').append(clone);

      if(applicable_status == false){
        $('.remark'+actCount).show();
        $('#act'+actCount).each(function() { 
          this.checked = false;           
        });
      }

      $('.tbody-statutorysettings').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
      if(count==1){
        $('.accordion-content'+count).addClass("default");
      }
      var complianceHeadingtableRow=$('#statutory-templates .compliance-heading');
      var clone1=complianceHeadingtableRow.clone();
      $('.accordion-content'+count).append(clone1);
     
      for(var compliance in complianceslist){    
        var statutoryprovision = '';
        var compliance_id = complianceslist[compliance]["compliance_id"];
        var compliance_applicable_status = complianceslist[compliance]["compliance_applicable_status"];
        var complianceDetailtableRow=$('#statutory-values .table-statutory-values .compliance-details');
        var clone2=complianceDetailtableRow.clone();
        $('.sno', clone2).text(statutoriesCount);
        $('.statutoryprovision', clone2).text(complianceslist[compliance]["statutory_provision"]);
        $('.compliancetask', clone2).text(complianceslist[compliance]["compliance_name"]);
        $('.compliancedescription', clone2).text(complianceslist[compliance]["description"]);
        $('.complianceapplicable', clone2).html('<input type="checkbox" checked="checked" id="statutory'+statutoriesCount+'" class="statutoryclass'+actCount+'"><label for="statutory'+statutoriesCount+'"></label>');
        $('.accordion-content'+count).append(clone2);

        if(compliance_applicable_status == false){
          $('#statutory'+statutoriesCount).each(function() { 
          this.checked = false;           
        });
      }
        statutoriesCount = statutoriesCount + 1;
      }  
      actCount = actCount + 1;
      count++;
    }

    $(document).ready(function($) {
      $('#accordion').find('.accordion-toggle').click(function(){
        //Expand or collapse this panel
        $(this).next().slideToggle('fast');
        //Hide the other panels
        $(".accordion-content").not($(this).next()).slideUp('fast');
      });
    });
  });



}


$("#submit").click(function() {
    var assignStatutoryCountryId = 0;
    var assignStatutoryGroupId = 0;
    var assignStatutoryLocationId = 0;
    var assignStatutoryDomainId = 0;
    var clientStatutoryId = null;
    if($("#clientstatutoryid").val() == ''){
      assignStatutoryCountryId = parseInt($('.countrylist.active').attr('id'));
      assignStatutoryGroupId = parseInt($('.grouplist.active').attr('id'));
      assignStatutoryLocationId = parseInt($('.locationlist.active').attr('id'));
      assignStatutoryDomainId = parseInt($('.domainlist.active').attr('id'));
    }else{
      clientStatutoryId = parseInt($("#clientstatutoryid").val());
      assignStatutoryCountryId = parseInt($("#ascountry").val());
      assignStatutoryGroupId = parseInt($("#asgroup").val());
      assignStatutoryLocationId = parseInt($("#aslocation").val());
      assignStatutoryDomainId = parseInt($("#asdomain").val());
    }

    var assignedStatutories = [];
    var statutoriesCount= 1;
    var actCount = 1;
    for(var statutory in statutoriesList){
      var level1StatutoryId = statutoriesList[statutory]["level_1_statutory_id"];
      var applicableStatus = null;
      var notApplicableRemarks = null;
      
      if($('#act'+actCount).is(":checked")){
        applicableStatus = true;
      }
      else{
        applicableStatus = false;
        notApplicableRemarks = $('#remarkvalue'+actCount).val();
        if(notApplicableRemarks.length==0){
          displayMessage("Remarks required for not applicable act");
          return false;
        }
      }

    var complianceslist = statutoriesList[statutory]["compliances"];
    var compliances = { };
    for(var compliance in complianceslist){    
      var complianceId = complianceslist[compliance]["compliance_id"];
      var complianceApplicableStatus = false;
      if($('#statutory'+statutoriesCount).is(":checked"))
        complianceApplicableStatus = true;

      compliances[complianceId] = complianceApplicableStatus;
      statutoriesCount++;
    } 

    if($("#clientstatutoryid").val() != ''){
      var newCompliances = newCompliancesList[statutoriesList[statutory]["level_1_statutory_id"]];
      for(var newCompliance in newCompliances){
        var complianceId = newCompliances[newCompliance]["compliance_id"];
        var complianceApplicableStatus = false;
        if($('#statutory'+statutoriesCount).is(":checked"))
          complianceApplicableStatus = true;
          compliances[complianceId] = complianceApplicableStatus;
          statutoriesCount++;
      }
    }

    actCount++;
    assignedstatutoriesData = mirror.assignedStatutories(level1StatutoryId,compliances, applicableStatus, notApplicableRemarks);
    assignedStatutories.push(assignedstatutoriesData);
  }

  function onSuccess(data){
    getStatutorySettings ();
    $("#statutorysettings-add").hide();
    $("#statutorysettings-view").show();
    $('ul.setup-panel li:eq(0)').addClass('active');
    $('ul.setup-panel li:eq(1)').addClass('disabled');
    $('ul.setup-panel li a[href="#step-1"]').trigger('click');
    $(".tbody-statutorysettings").find("tbody").remove();
  }
  function onFailure(error){
    displayMessage(error)
  }
  mirror.saveOrSubmitAssignStatutory(assignStatutoryCountryId, assignStatutoryGroupId, assignStatutoryLocationId, assignStatutoryUnitIds, assignStatutoryDomainId, submissionType, clientStatutoryId, assignedStatutories, 
    function (error, response) {
    if (error == null){
      onSuccess(response);
    }
    else {
      onFailure(error);
    }
  }
  );
});

function displayEdit(unit_id){
  var sList;
  var dispBusinessGroup;
  var dispLegalEntity;
  var dispDivision;
  var dispUnit;

  $("#statutorysettings-view").hide();
  $("#statutorysettings-add").show();
  for(var entity in assignedStatutoriesList) {
      var check_unit_id = assignedStatutoriesList[entity]["unit_id"];
      if(unit_id == check_unit_id){
         sList = assignedStatutoriesList[entity]["statutories"];
         dispBusinessGroup = assignedStatutoriesList[entity]["business_group_name"];
         dispLegalEntity = assignedStatutoriesList[entity]["legal_entity_name"];
         dispDivision = assignedStatutoriesList[entity]["division_name"];
         dispUnit = assignedStatutoriesList[entity]["unit_name"];
        break;
      }
    }

  load_statutory(sList, dispBusinessGroup, dispLegalEntity, dispDivision, dispUnit);
}


function loadStatutorySettingsList(assignedStatutoriesList){
  var j = 1;
  var unit_id = 0;

  $(".tbody-statutorysettings-list").find("tr").remove();
    for(var entity in assignedStatutoriesList) {
      unit_id = assignedStatutoriesList[entity]["unit_id"];
      var tableRow=$('#templates .table-statutorysettings .table-row');
      var clone=tableRow.clone();
      $('.tbl_sno', clone).text(j);
      $('.tbl_country', clone).text(assignedStatutoriesList[entity]["country_name"]);
      $('.tbl_businessgroup', clone).text(assignedStatutoriesList[entity]["business_group_name"]);
      $('.tbl_legalentity', clone).text(assignedStatutoriesList[entity]["legal_entity_name"]);
      $('.tbl_division', clone).text(assignedStatutoriesList[entity]["division_name"]);
      $('.tbl_unit', clone).text(assignedStatutoriesList[entity]["unit_name"]);
      $('.tbl_domain', clone).text(assignedStatutoriesList[entity]["domain_names"]);
      $('.tbl_edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+unit_id+')"/>');
      $('.tbody-statutorysettings-list').append(clone);
      j = j + 1;
    }
}

function getStatutorySettings () {
  function onSuccess(data){
  assignedStatutoriesList = data["statutories"];
  loadStatutorySettingsList(assignedStatutoriesList);
  }
  function onFailure(error){
  }
  client_mirror.getStatutorySettings(
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

$(".listfilter").keyup(function() {
  var filter1 = $("#filter1").val().toLowerCase();
  var filter2 = $("#filter2").val().toLowerCase();
  var filter3 = $("#filter3").val().toLowerCase();
  var filter4 = $("#filter4").val().toLowerCase();
  var filter5 = $("#filter5").val().toLowerCase();
  var filter6 = $("#filter6").val().toLowerCase();
 
  var filteredList=[];
  for(var entity in assignedStatutoriesList) {
    var filter1val = assignedStatutoriesList[entity]["country_name"];
    var filter2val = assignedStatutoriesList[entity]["business_group_name"];
    var filter3val = assignedStatutoriesList[entity]["legal_entity_name"];
    var filter4val = assignedStatutoriesList[entity]["division_name"];
    var filter5val = assignedStatutoriesList[entity]["unit_name"];
    //var filter6val = assignedStatutoriesList[entity]["domain_name"];
    var filter6val = assignedStatutoriesList[entity]["unit_name"];
    
    if (~filter1val.toLowerCase().indexOf(filter1) && ~filter2val.toLowerCase().indexOf(filter2) && ~filter3val.toLowerCase().indexOf(filter3) && ~filter4val.toLowerCase().indexOf(filter4) && ~filter5val.toLowerCase().indexOf(filter5) && ~filter6val.toLowerCase().indexOf(filter6) ) 
    {
      filteredList.push(assignedStatutoriesList[entity]);
    }   
  }
  loadStatutorySettingsList(filteredList);
  });


$(document).ready(function () {
  getStatutorySettings ();
});