var assignedStatutoriesList;
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

var assignStatutoryCountryId = 0;
var assignStatutoryCountryValue = null;
var assignStatutoryGroupId = 0;
var assignStatutoryGroupValue = null;
var assignStatutoryBusinessGroupId = 0;
var assignStatutoryBusinessGroupValue = null;
var assignStatutoryLegalEntityId = 0;
var assignStatutoryLegalEntityValue = null;
var assignStatutoryDivisionId = 0;
var assignStatutoryDivisionValue = null;
var assignStatutoryGeographyLevelId = 0;
var assignStatutoryGeographyLevelValue = null;
var assignStatutoryLocationId = 0;
var assignStatutoryLocationValue = null;
var assignStatutoryIndustryId = 0;
var assignStatutoryIndustryValue = null;
var assignStatutoryUnitIds = [];
var assignStatutoryUnitValues = [];
var assignStatutoryDomainId = 0;
var assignStatutoryDomainValue = null;


function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

function clearValues(levelvalue) {

  if(levelvalue == 'all'){
    assignStatutoryCountryId = 0;
    assignStatutoryCountryValue = null;
    assignStatutoryGroupId = 0;
    assignStatutoryGroupValue = null;
    assignStatutoryBusinessGroupId = 0;
    assignStatutoryBusinessGroupValue = null;
    assignStatutoryLegalEntityId = 0;
    assignStatutoryLegalEntityValue = null;
    assignStatutoryDivisionId = 0;
    assignStatutoryDivisionValue = null;
    assignStatutoryGeographyLevelId = 0;
    assignStatutoryGeographyLevelValue = null;
    assignStatutoryLocationId = 0;
    assignStatutoryLocationValue = null;
    assignStatutoryIndustryId = 0;
    assignStatutoryIndustryValue = null;
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    assignStatutoryDomainId = 0;
    assignStatutoryDomainValue = null;

    $('#group').empty();
    $('#businessgroup').empty();
    $('#legalentity').empty();
    $('#division').empty();
    $('#geographylevel').empty();
    $('#location').empty();
    $('#industry').empty();
    $('#unit').empty();
    $('#domain').empty();
  }

  if(levelvalue == 'country'){
    assignStatutoryGroupId = 0;
    assignStatutoryGroupValue = null;
    assignStatutoryBusinessGroupId = 0;
    assignStatutoryBusinessGroupValue = null;
    assignStatutoryLegalEntityId = 0;
    assignStatutoryLegalEntityValue = null;
    assignStatutoryDivisionId = 0;
    assignStatutoryDivisionValue = null;
    assignStatutoryGeographyLevelId = 0;
    assignStatutoryGeographyLevelValue = null;
    assignStatutoryLocationId = 0;
    assignStatutoryLocationValue = null;
    assignStatutoryIndustryId = 0;
    assignStatutoryIndustryValue = null;
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    assignStatutoryDomainId = 0;
    assignStatutoryDomainValue = null;

    $('#group').empty();
    $('#businessgroup').empty();
    $('#legalentity').empty();
    $('#division').empty();
    $('#geographylevel').empty();
    $('#location').empty();
    $('#industry').empty();
    $('#unit').empty();
    $('#domain').empty();
  }

  if(levelvalue == 'group'){
    assignStatutoryBusinessGroupId = 0;
    assignStatutoryBusinessGroupValue = null;
    assignStatutoryLegalEntityId = 0;
    assignStatutoryLegalEntityValue = null;
    assignStatutoryDivisionId = 0;
    assignStatutoryDivisionValue = null;
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    assignStatutoryDomainId = 0;
    assignStatutoryDomainValue = null;

    $('#businessgroup').empty();
    $('#legalentity').empty();
    $('#division').empty();
    $('#unit').empty();
    $('#domain').empty();
  }

  if(levelvalue == 'businessgroup'){
    assignStatutoryLegalEntityId = 0;
    assignStatutoryLegalEntityValue = null;
    assignStatutoryDivisionId = 0;
    assignStatutoryDivisionValue = null;
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    assignStatutoryDomainId = 0;
    assignStatutoryDomainValue = null;

    $('#legalentity').empty();
    $('#division').empty();
    $('#unit').empty();
    $('#domain').empty();
  }

  if(levelvalue == 'legalentity'){
    assignStatutoryDivisionId = 0;
    assignStatutoryDivisionValue = null;
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    assignStatutoryDomainId = 0;
    assignStatutoryDomainValue = null;

    $('#division').empty();
    $('#unit').empty();
    $('#domain').empty();

  }

  if(levelvalue == 'division'){
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    assignStatutoryDomainId = 0;
    assignStatutoryDomainValue = null;

    $('#unit').empty();
    $('#domain').empty();

  }

  if(levelvalue == 'geographylevel'){
    assignStatutoryLocationId = 0;
    assignStatutoryLocationValue = null;
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    assignStatutoryDomainId = 0;
    assignStatutoryDomainValue = null;

    $('#location').empty();
    $('#unit').empty();
    $('#domain').empty();
  }

  if(levelvalue == 'location'){
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    assignStatutoryDomainId = 0;
    assignStatutoryDomainValue = null;

    $('#unit').empty();
    $('#domain').empty();
  }

  if(levelvalue == 'industry'){
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    assignStatutoryDomainId = 0;
    assignStatutoryDomainValue = null;
    
    $('#unit').empty();
    $('#domain').empty();
  }

  if(levelvalue == 'unit'){
    assignStatutoryDomainId = 0;
    assignStatutoryDomainValue = null;
    
    $('#domain').empty();
  }
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

function make_breadcrumbs(){
    var arrowimage = " <img src=\'/images/chevron_black_right.png\'/> ";
    $(".breadcrumbs").html(assignStatutoryCountryValue + arrowimage + assignStatutoryGroupValue + arrowimage + assignStatutoryBusinessGroupValue + arrowimage + assignStatutoryLegalEntityValue + arrowimage + assignStatutoryDivisionValue + arrowimage + assignStatutoryGeographyLevelValue + arrowimage + assignStatutoryLocationValue + arrowimage + assignStatutoryIndustryValue + arrowimage + assignStatutoryUnitValues + arrowimage + assignStatutoryDomainValue);
}

function load_secondwizard(){
  var count=1;
  var statutoriesCount= 1;
  var actCount = 1;
  $(".tbody-assignstatutory").find("tr").remove();
  for(var statutory in statutoriesList){
    var actname = statutoriesList[statutory]["level_1_statutory_name"];
    var complianceslist = statutoriesList[statutory]["compliances"];
    var level_1_statutory_id = statutoriesList[statutory]["level_1_statutory_id"];

    var acttableRow=$('#act-templates .font1 .tbody-heading');
    var clone=acttableRow.clone();
    $('.actapplicable', clone).html('<input type="checkbox" checked="checked" id="act'+actCount+'" value="'+actCount+'" onclick="actstatus(this)" style="margin-top:100px;"> <label for="act'+actCount+'" style="margin-top:100px;"></label> ');
    $('.actname', clone).html('<div style="float:left;margin-top:5px;">'+actname+'</div> <div style="float:right; width:500px;" class="default-display-none remark'+actCount+'" ><div style="float:right;  width:250px;margin-top:-3px;"> <input type="text" id="remarkvalue'+actCount+'" class="input-box" style="width:200px;" placeholder="Enter Remarks" ></div><div style="float:right; width:70px;margin-top:5px;"> Remarks</div></div>');
    $('.tbody-assignstatutory').append(clone);

    $('.tbody-assignstatutory').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
    if(count==1){
      $('.accordion-content'+count).addClass("default");
    }
    var complianceHeadingtableRow=$('#statutory-templates .compliance-heading');
    var clone1=complianceHeadingtableRow.clone();
    $('.accordion-content'+count).append(clone1);
   
    for(var compliance in complianceslist){    
      var statutoryprovision = '';
      var compliance_id = complianceslist[compliance]["compliance_id"];
      var complianceDetailtableRow=$('#statutory-values .table-statutory-values .compliance-details');
      var clone2=complianceDetailtableRow.clone();
      $('.sno', clone2).text(statutoriesCount);
      $('.statutoryprovision', clone2).text(complianceslist[compliance]["statutory_provision"]);
      $('.compliancetask', clone2).text(complianceslist[compliance]["compliance_name"]);
      $('.compliancedescription', clone2).text(complianceslist[compliance]["description"]);
      $('.complianceapplicable', clone2).html('<input type="checkbox" checked="checked" id="statutory'+statutoriesCount+'" class="statutoryclass'+actCount+'"><label for="statutory'+statutoriesCount+'"></label>');
      $('.accordion-content'+count).append(clone2);
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
}

function loadunit(){
  if(assignStatutoryLegalEntityId != 0 && assignStatutoryIndustryId != 0 && assignStatutoryLocationId != 0){
    if(assignStatutoryDivisionId == 0){
    var str='';
    $('#unit').empty();
    for(var unit in unitsList){
      if(unitsList[unit]["division_id"] == null && unitsList[unit]["legal_entity_id"] == assignStatutoryLegalEntityId && unitsList[unit]["client_id"] == assignStatutoryGroupId && unitsList[unit]["industry_id"] == assignStatutoryIndustryId && $.inArray(assignStatutoryLocationId, unitsList[unit]["geography_ids"]) >= 0){
        str += '<li id="'+unitsList[unit]["unit_id"]+'" class="unitlist" >'+unitsList[unit]["unit_name"]+'</li>';
      }
    }
    $('#unit').append(str);
    }else{
      var str='';
      $('#unit').empty();
      for(var unit in unitsList){
        if(unitsList[unit]["division_id"] == assignStatutoryDivisionId && unitsList[unit]["legal_entity_id"] == assignStatutoryLegalEntityId && unitsList[unit]["client_id"] == assignStatutoryGroupId && unitsList[unit]["industry_id"] == assignStatutoryIndustryId && $.inArray(assignStatutoryLocationId, unitsList[unit]["geography_ids"]) >= 0){
          str += '<li id="'+unitsList[unit]["unit_id"]+'" class="unitlist" >'+unitsList[unit]["unit_name"]+'</li>';
        }
      }
      $('#unit').append(str);
    }
  }
}

$("#geographylevel").click(function(event){
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");

  var str='';
  assignStatutoryGeographyLevelId = parseInt(event.target.id);
  assignStatutoryGeographyLevelValue = $(event.target).text();
  $('#location').empty();
  for(var geography in geographiesList[assignStatutoryCountryId]){
    if(geographiesList[assignStatutoryCountryId][geography]["is_active"] == true && geographiesList[assignStatutoryCountryId][geography]["level_id"] == assignStatutoryGeographyLevelId){
      str += '<li id="'+geographiesList[assignStatutoryCountryId][geography]["geography_id"]+'" class="locationlist">'+geographiesList[assignStatutoryCountryId][geography]["geography_name"]+'</li>';
    }
  }
  $('#location').append(str);
});

$("#group").click(function(event){
  clearValues('group');
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");

  var str='';
  assignStatutoryGroupId = parseInt(event.target.id);
  assignStatutoryGroupValue = $(event.target).text();
  $('#businessgroup').empty();
  for(var businessgroup in businessgroupsList){
    if(businessgroupsList[businessgroup]["client_id"] == assignStatutoryGroupId){
      str += '<li id="'+businessgroupsList[businessgroup]["business_group_id"]+'" class="businessgrouplist" >'+businessgroupsList[businessgroup]["business_group_name"]+'</li>';
    }
  }
  $('#businessgroup').append(str); 

  var str1='';
  $('#legalentity').empty();
  for(var legalentity in legalentitiesList){
    if(legalentitiesList[legalentity]["client_id"] == assignStatutoryGroupId && legalentitiesList[legalentity]["business_group_id"] == null){
      str1 += '<li id="'+legalentitiesList[legalentity]["legal_entity_id"]+'" class="legalentitylist" >'+legalentitiesList[legalentity]["legal_entity_name"]+'</li>';
    }
  }
  $('#legalentity').append(str1);

});


$("#businessgroup").click(function(event){
  clearValues('businessgroup');
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");

  var str='';
  assignStatutoryBusinessGroupId = parseInt(event.target.id);
  assignStatutoryBusinessGroupValue = $(event.target).text();
  $('#legalentity').empty();
  for(var legalentity in legalentitiesList){
    if(legalentitiesList[legalentity]["client_id"] == assignStatutoryGroupId && legalentitiesList[legalentity]["business_group_id"] == assignStatutoryBusinessGroupId){
      str += '<li id="'+legalentitiesList[legalentity]["legal_entity_id"]+'" class="legalentitylist" >'+legalentitiesList[legalentity]["legal_entity_name"]+'</li>';
    }
  }
  $('#legalentity').append(str);
});

$("#legalentity").click(function(event){
  clearValues('legalentity');
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");

  var str='';
  assignStatutoryLegalEntityId = parseInt(event.target.id);
  assignStatutoryLegalEntityValue = $(event.target).text();
  $('#division').empty();
  for(var division in divisionsList){
    if(divisionsList[division]["client_id"] == assignStatutoryGroupId && divisionsList[division]["legal_entity_id"] == assignStatutoryLegalEntityId){
      str += '<li id="'+divisionsList[division]["division_id"]+'" class="divisionlist" >'+divisionsList[division]["division_name"]+'</li>';
    }
  }
  $('#division').append(str);

  loadunit();
});

$("#division").click(function(event){
  clearValues('division');
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");
  assignStatutoryDivisionId = parseInt(event.target.id);
  assignStatutoryDivisionValue = $(event.target).text();

  loadunit();
});

$("#location").click(function(event){
  clearValues('location');
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");
  assignStatutoryLocationId = parseInt(event.target.id);
  assignStatutoryLocationValue = $(event.target).text();

  loadunit();
});

$("#industry").click(function(event){
  clearValues('industry');
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");
  assignStatutoryIndustryId = parseInt(event.target.id);
  assignStatutoryIndustryValue = $(event.target).text();
  loadunit();
});


$("#unit").click(function(event){
  clearValues('unit');
  var chkstatus = $(event.target).attr('class');
  if(chkstatus == 'unitlist active'){
    $(event.target).removeClass("active");
    var removeid = assignStatutoryUnitIds.indexOf(event.target.id);
    assignStatutoryUnitIds.splice(removeid,1);
    var removename = assignStatutoryUnitValues.indexOf($(event.target).text());
    assignStatutoryUnitValues.splice(removename,1);
  }else{
    $(event.target).addClass("active");
    assignStatutoryUnitIds.push(parseInt(event.target.id));
    assignStatutoryUnitValues.push($(event.target).text());
  }
  
  var domainArray = [];
  for(var unit in unitsList){
    if($.inArray(unitsList[unit]["unit_id"], assignStatutoryUnitIds) >= 0){
      domainArray.push(unitsList[unit]["domain_ids"]);
    }
  }
  
  if(domainArray.length > 0){
    var applicableDomains = domainArray.shift().filter(function(v) {
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
});

$("#domain").click(function(event){
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");
  assignStatutoryDomainId = parseInt(event.target.id);
  assignStatutoryDomainValue = $(event.target).text();

  make_breadcrumbs();
});

function load_firstwizard(){

  var str='';
  $('#group').empty();
  for(var group in groupcompaniesList){
    if(groupcompaniesList[group]["is_active"] == true && $.inArray(assignStatutoryCountryId, groupcompaniesList[group]["country_ids"]) >= 0){
      str += '<li id="'+groupcompaniesList[group]["client_id"]+'" class="grouplist">'+groupcompaniesList[group]["group_name"]+'</li>';
    }
  }
  $('#group').append(str);
   
  var str1='';
  $('#geographylevel').empty();
  for(var geographylevel in geographyLevelsList[assignStatutoryCountryId]){
    str1 += '<li id="'+geographyLevelsList[assignStatutoryCountryId][geographylevel]["level_id"]+'" class="geographylevellist">'+geographyLevelsList[assignStatutoryCountryId][geographylevel]["level_name"]+'</li>';
  }
  $('#geographylevel').append(str1);

  var str2='';
  $('#industry').empty();
  for(var industry in industriesList){
    if(industriesList[industry]["is_active"] == true){
      str2 += '<li id="'+industriesList[industry]["industry_id"]+'" class="industrylist">'+industriesList[industry]["industry_name"]+'</li>';
    }
  }
  $('#industry').append(str2);
}

$("#country").click(function(event){
  clearValues('country');
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");
  assignStatutoryCountryId = parseInt(event.target.id);
  assignStatutoryCountryValue = $(event.target).text();

  function onSuccess(data){
  //countriesList = data["countries"];
  groupcompaniesList = data["group_companies"];
  businessgroupsList = data["business_groups"];
  legalentitiesList = data["legal_entities"];
  divisionsList = data["divisions"];
  geographyLevelsList = data["geography_levels"];
  geographiesList = data["geographies"];
  industriesList = data["industries"];
  domainsList = data["domains"];
  unitsList = data["units"];
  load_firstwizard();
}
function onFailure(error){
}
mirror.getAssignStatutoryWizardOne(assignStatutoryCountryId,
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

function loadCountriesList(data){
  var countriesList = data["countries"];
  var str='';
  $('#country').empty();
    for(var country in countriesList){
      if(countriesList[country]["is_active"] == true){
      str += '<li id="'+countriesList[country]["country_id"]+'" class="countrylist">'+countriesList[country]["country_name"]+'</li>';
    }
  }
  $('#country').append(str);
}

$(".btn-assignstatutory-add").click(function(){
$("#assignstatutory-view").hide();
$("#assignstatutory-add").show();
$("#edit_assignstatutory_id").val('');
displayMessage('');
clearValues("all");
$(".breadcrumbs").html('');

function onSuccess(data){
  loadCountriesList(data);
}
function onFailure(error){
  displayMessage(error);
}
mirror.getCountryList(
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

function validate_firsttab(){
  if(assignStatutoryCountryId == 0){
    displayMessage("Country Required");
    return false;
  }else if (assignStatutoryGroupId == 0){
    displayMessage("Group Required");
    return false;
  }else if (assignStatutoryBusinessGroupId == 0){
    displayMessage("Business Group Required");
    return false;
  }else if (assignStatutoryLegalEntityId == 0){
    displayMessage("Legal Entity Required");
    return false;
  }else if (assignStatutoryDivisionId == 0){
    displayMessage("Division Required");
    return false;
  }else if (assignStatutoryGeographyLevelId == 0){
    displayMessage("Geography Level Required");
    return false;
  }else if (assignStatutoryLocationId == 0){
    displayMessage("Location Required");
    return false;
  }else if (assignStatutoryIndustryId == 0){
    displayMessage("Industry Required");
    return false;
  }else if (assignStatutoryUnitIds.length == 0){
    displayMessage("Unit Required");
    return false;
  }else if (assignStatutoryDomainId == ''){
    displayMessage("Domain Required");
    return false;
  }else{
    var checkDupliacteAssignStauttory = true;
    for(var entity in assignedStatutoriesList) {
      if(assignStatutoryLocationValue == assignedStatutoriesList[entity]["geography_name"] && assignStatutoryIndustryValue == assignedStatutoriesList[entity]["industry_name"] && assignStatutoryDomainValue == assignedStatutoriesList[entity]["domain_name"]){
        for(var j=0;j<assignStatutoryUnitValues.length;j++){
          if(assignStatutoryUnitValues[j] == assignedStatutoriesList[entity]["unit_name"]){
            displayMessage("Already Statutory Assigned for this "+assignStatutoryUnitValues[j]);
            checkDupliacteAssignStauttory = false;
            break;
            return false;
          }
        }
      }
    }

    if(checkDupliacteAssignStauttory){
      function onSuccess(data){
        statutoriesList = data["statutories"];
        load_secondwizard();
      }
      function onFailure(error){
      }
      mirror.getAssignStatutoryWizardTwo(assignStatutoryCountryId, assignStatutoryDomainId, assignStatutoryIndustryId, assignStatutoryLocationId,
        function (error, response) {
              if (error == null){
                onSuccess(response);
              }
              else {
                onFailure(error);
              }
          }
    );

      displayMessage("");
      return true;
    }    
  }
}

function validate_secondtab(){
  /*if (sm_geographyids.length == 0){
    displayMessage("Atleast one Location should be selected");
  }else{
    displayMessage("");
    return true;
  }*/

  return true;
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
$('#backward-step-1').on('click', function(e) {
$('ul.setup-panel li:eq(1)').removeClass('disabled');
$('ul.setup-panel li a[href="#step-1"]').trigger('click');

})
$('#activate-step-finish').on('click', function(e) {

if (validate_secondtab()){

  //siva
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
      notApplicableRemarks = $('#remarkvalue1').val();
      if(notApplicableRemarks.length==0){
        displayMessage("Remarks required for not applicable Act");
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
    actCount++;
    assignedstatutoriesData = mirror.assignedStatutories(level1StatutoryId,compliances, applicableStatus, notApplicableRemarks);
    assignedStatutories.push(assignedstatutoriesData);
  }

  function onSuccess(data){
    getAssignedStatutories ();
    $("#assignstatutory-add").hide();
    $("#assignstatutory-view").show();
    $('ul.setup-panel li:eq(0)').addClass('active');
    $('ul.setup-panel li:eq(1)').addClass('disabled');
    $('ul.setup-panel li a[href="#step-1"]').trigger('click');
    $(".tbody-assignstatutory").find("tbody").remove();
  }
  function onFailure(error){
    displayMessage(error)
  }
  mirror.saveOrSubmitAssignStatutory(assignStatutoryCountryId, assignStatutoryGroupId, assignStatutoryLocationId, assignStatutoryUnitIds, assignStatutoryDomainId, "Save", null, assignedStatutories, 
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
})
function loadAssignedStatutoriesList(assignedStatutoriesList){
  var j = 1;
  var client_saved_statutory_id = 0;
  var client_assigned_statutory_id = 0;
  $(".tbody-assignstatutory-list").find("tr").remove();
    for(var entity in assignedStatutoriesList) {
      client_saved_statutory_id = assignedStatutoriesList[entity]["client_saved_statutory_id"];
      client_assigned_statutory_id = assignedStatutoriesList[entity]["client_assigned_statutory_id"];
      
      var tableRow=$('#templates .table-assignstatutory .table-row');
      var clone=tableRow.clone();
      $('.tbl_sno', clone).text(j);
      $('.tbl_country', clone).text(assignedStatutoriesList[entity]["country_name"]);
      $('.tbl_group', clone).text(assignedStatutoriesList[entity]["group_name"]);
      $('.tbl_businessgroup', clone).text(assignedStatutoriesList[entity]["business_group_name"]);
      $('.tbl_legalentity', clone).text(assignedStatutoriesList[entity]["legal_entity_name"]);
      $('.tbl_division', clone).text(assignedStatutoriesList[entity]["division_name"]);
      $('.tbl_location', clone).text(assignedStatutoriesList[entity]["geography_name"]);
      $('.tbl_industry', clone).text(assignedStatutoriesList[entity]["industry_name"]);
      $('.tbl_unit', clone).text(assignedStatutoriesList[entity]["unit_name"]);
      $('.tbl_domain', clone).text(assignedStatutoriesList[entity]["domain_name"]);
      if(assignedStatutoriesList[entity]["submission_status"] == 2){
        $('.tbl_status', clone).text('Submitted');
      }
      else{
        $('.tbl_status', clone).text("Pending");
        $('.tbl_edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+client_saved_statutory_id+')"/>');
      $('.tbl_view', clone).html('<img src=\'/images/icon-viewsubmit.png\' onclick="changeStatus('+client_saved_statutory_id+')"/>');
      }
      $('.tbody-assignstatutory-list').append(clone);
      j = j + 1;
    }
}

function getAssignedStatutories () {

  function onSuccess(data){
  assignedStatutoriesList = data["assigned_statutories"];
  loadAssignedStatutoriesList(assignedStatutoriesList);
  }
  function onFailure(error){
  }
  mirror.getAssignedStatutoriesList(
    function (error, response) {
          if (error == null){
            onSuccess(response);
          }
          else {
            onFailure(error);
          }
      }
  );
  loadAssignedStatutoriesList(assignedStatutoriesList);
}


$(".listfilter").keyup(function() {
  var filter1 = $("#filter1").val().toLowerCase();
  var filter2 = $("#filter2").val().toLowerCase();
  var filter3 = $("#filter3").val().toLowerCase();
  var filter4 = $("#filter4").val().toLowerCase();
  var filter5 = $("#filter5").val().toLowerCase();
  var filter6 = $("#filter6").val().toLowerCase();
  var filter7 = $("#filter7").val().toLowerCase();
  var filter8 = $("#filter8").val().toLowerCase();
  var filter9 = $("#filter9").val().toLowerCase();
  var filter10 = $("#filter10").val().toLowerCase();
 
  var filteredList=[];
  for(var entity in assignedStatutoriesList) {
    var filter1val = assignedStatutoriesList[entity]["country_name"];
    var filter2val = assignedStatutoriesList[entity]["group_name"];
    var filter3val = assignedStatutoriesList[entity]["business_group_name"];
    var filter4val = assignedStatutoriesList[entity]["legal_entity_name"];
    var filter5val = assignedStatutoriesList[entity]["division_name"];
    var filter6val = assignedStatutoriesList[entity]["geography_name"];
    var filter7val = assignedStatutoriesList[entity]["industry_name"];
    var filter8val = assignedStatutoriesList[entity]["unit_name"];
    var filter9val = assignedStatutoriesList[entity]["domain_name"];
    var filter10val = null;
    if(assignedStatutoriesList[entity]["submission_status"] == 2)
        filter10val = 'Submitted';
      else
        filter10val = "Pending";
    
    if (~filter1val.toLowerCase().indexOf(filter1) && ~filter2val.toLowerCase().indexOf(filter2) && ~filter3val.toLowerCase().indexOf(filter3) && ~filter4val.toLowerCase().indexOf(filter4) && ~filter5val.toLowerCase().indexOf(filter5) && ~filter6val.toLowerCase().indexOf(filter6) && ~filter7val.toLowerCase().indexOf(filter7) && ~filter8val.toLowerCase().indexOf(filter8) && ~filter9val.toLowerCase().indexOf(filter9) && ~filter10val.toLowerCase().indexOf(filter10)) 
    {
      filteredList.push(assignedStatutoriesList[entity]);
    }   
  }
  loadAssignedStatutoriesList(filteredList);
  });

$(document).ready(function () {
  getAssignedStatutories ();

  $("#filter_country").keyup( function() {
    var filter = $("#filter_country").val().toLowerCase();
    var lis = document.getElementsByClassName('countrylist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (name.toLowerCase().indexOf(filter) == 0) 
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_group").keyup( function() {
    var filter = $("#filter_group").val().toLowerCase();
    var lis = document.getElementsByClassName('grouplist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (name.toLowerCase().indexOf(filter) == 0) 
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
      if (name.toLowerCase().indexOf(filter) == 0) 
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
      if (name.toLowerCase().indexOf(filter) == 0) 
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
      if (name.toLowerCase().indexOf(filter) == 0) 
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_geographylevel").keyup( function() {
    var filter = $("#filter_geographylevel").val().toLowerCase();
    var lis = document.getElementsByClassName('geographylevellist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (name.toLowerCase().indexOf(filter) == 0) 
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_location").keyup( function() {
    var filter = $("#filter_location").val().toLowerCase();
    var lis = document.getElementsByClassName('locationlist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (name.toLowerCase().indexOf(filter) == 0) 
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_industry").keyup( function() {
    var filter = $("#filter_industry").val().toLowerCase();
    var lis = document.getElementsByClassName('industrylist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (name.toLowerCase().indexOf(filter) == 0) 
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
      if (name.toLowerCase().indexOf(filter) == 0) 
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
      if (name.toLowerCase().indexOf(filter) == 0) 
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });
});