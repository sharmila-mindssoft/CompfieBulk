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
var accordionstatus = true;
var finalList;
var pageSize = 100;
var startCount;
var endCount;
var mUnit = 3;
var msg = '';

function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
}

//clear old list values
function clearValues(levelvalue) {
  if(levelvalue == 'all'){
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];

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
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];

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
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];

    $('#businessgroup').empty();
    $('#legalentity').empty();
    $('#division').empty();
    $('#unit').empty();
    $('#domain').empty();
  }

  if(levelvalue == 'businessgroup'){
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];

    $('#legalentity').empty();
    $('#division').empty();
    $('#unit').empty();
    $('#domain').empty();
  }

  if(levelvalue == 'legalentity'){
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];

    $('#division').empty();
    $('#unit').empty();
    $('#domain').empty();

  }

  if(levelvalue == 'division'){
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    $('#unit').empty();
    $('#domain').empty();
  }

  if(levelvalue == 'geographylevel'){
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    $('#location').empty();
    $('#unit').empty();
    $('#domain').empty();
  }

  if(levelvalue == 'location'){
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    $('#unit').empty();
    $('#domain').empty();
  }

  if(levelvalue == 'industry'){
    assignStatutoryUnitIds = [];
    assignStatutoryUnitValues = [];
    $('#unit').empty();
    $('#domain').empty();
  }

  if(levelvalue == 'unit'){
    $('#domain').empty();
  }
}

//show/hide remark textbox based on act applicable selection
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
    $('.remark'+actSelect).hide();
  }else{
    $('#act'+actSelect).prop("checked",false);
    $('.remark'+actSelect).show();
  }
}

//display breadcrumbs
function make_breadcrumbs(){

  var bc_businessgroup = $('.businessgrouplist.active').text();
  var bc_divisionname = $('.divisionlist.active').text();
  var arrowimage = " <img src=\'/images/chevron_black_right.png\'/> ";

  if(bc_businessgroup != '') bc_businessgroup = arrowimage + bc_businessgroup;
  if(bc_divisionname != '') bc_divisionname = arrowimage + bc_divisionname;

  $(".breadcrumbs").html($('.countrylist.active').text() + arrowimage + $('.grouplist.active').text()
  + bc_businessgroup + arrowimage + $('.legalentitylist.active').text() + bc_divisionname + arrowimage + $('.locationlist.active').text()
    + arrowimage + $('.industrylist.active').text() + arrowimage + assignStatutoryUnitValues + arrowimage + $('.domainlist.active').text());
}

//load compliances in second wizard
function load_secondwizard(){
  displayMessage("");
  var count=1;
  var statutoriesCount= 1;
  var actCount = 1;
  $(".tbody-assignstatutory").find("tbody").remove();
  for(var statutory in statutoriesList){
    var actname = statutoriesList[statutory]["level_1_statutory_name"];
    var complianceslist = statutoriesList[statutory]["compliances"];
    var level_1_statutory_id = statutoriesList[statutory]["level_1_statutory_id"];
    var applicable_status = statutoriesList[statutory]["applicable_status"];
    var not_applicable_remarks = statutoriesList[statutory]["not_applicable_remarks"];
    if (not_applicable_remarks == null) not_applicable_remarks = '';
    var acttableRow=$('#act-templates .font1 .tbody-heading');
    var clone=acttableRow.clone();
    $('.actapplicable', clone).html('<input type="checkbox" checked="checked" id="act'+actCount+
      '" value="'+actCount+'" onclick="actstatus(this)" style="margin-top:100px;"> <label for="act'+actCount+
      '" style="margin-top:100px;" class="act-label"></label> ');

    $('.actname', clone).html('<div style="float:left;margin-top:5px;width:65%;">'+actname+
      '</div> <div style="float:right; width:35%;" class="default-display-none remark'+actCount+
      '" ><div style="float:right;  width:220px;margin-top:3px;"> <input type="text" maxlength="500" id="remarkvalue'+actCount+
      '" value="'+not_applicable_remarks+'" class="input-box" style="width:200px;" placeholder="Enter Remarks" ></div><div style="float:right; width:70px;margin-top:7px;"> Remarks</div></div>');
    $('.tbody-assignstatutory').append(clone);

    if(applicable_status == false){
      $('.remark'+actCount).show();
      $('#act'+actCount).each(function() {
        this.checked = false;
      });
    }

    $('.tbody-assignstatutory').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
    if(count==1){
      $('.accordion-content'+count).addClass("default");
    }
    var complianceHeadingtableRow=$('#statutory-templates .compliance-heading');
    var clone1=complianceHeadingtableRow.clone();
    $('.accordion-content'+count).append(clone1);



    for(var compliance in complianceslist){
      var cDescription = complianceslist[compliance]["description"];
      var partDescription = cDescription;
      if (cDescription != null && cDescription.length > 50){
        partDescription = cDescription.substring(0,49)+'...';
      }

      var statutoryprovision = '';
      var compliance_id = complianceslist[compliance]["compliance_id"];
      var compliance_applicable_status = complianceslist[compliance]["compliance_applicable_status"];
      var complianceDetailtableRow=$('#statutory-values .table-statutory-values .compliance-details');
      var clone2=complianceDetailtableRow.clone();
      $('.sno', clone2).text(statutoriesCount);
      $('.statutoryprovision', clone2).text(complianceslist[compliance]["statutory_provision"]);
      $('.compliancetask', clone2).text(complianceslist[compliance]["compliance_name"]);
      $('.compliancedescription', clone2).html('<abbr class="page-load" title="'+
          cDescription+'">'+partDescription+'</abbr>');
      $('.complianceapplicable', clone2).html('<input type="checkbox" checked="checked" id="statutory'+statutoriesCount+'" class="statutoryclass'+actCount+'" onclick="compliancestatus(this)"><label for="statutory'+statutoriesCount+'"></label>');
      $('.accordion-content'+count).append(clone2);

      if(compliance_applicable_status == false){
        $('#statutory'+statutoriesCount).each(function() {
        this.checked = false;
      });
    }
      statutoriesCount = statutoriesCount + 1;
    }

    if($("#clientstatutoryid").val() != ''){
      var newCompliances = newCompliancesList[level_1_statutory_id];
      for(var newCompliance in newCompliances){
        var statutoryprovision = '';
        var compliance_id = newCompliances[newCompliance]["compliance_id"];
        var compliance_applicable_status = newCompliances[newCompliance]["compliance_applicable_status"];
        var complianceDetailtableRow=$('#statutory-values .table-statutory-values .compliance-details');
        var clone2=complianceDetailtableRow.clone();
        $('.sno', clone2).html('<font color="#0404B4">'+statutoriesCount+'</font>');
        $('.statutoryprovision', clone2).html('<font color="#0404B4">'+newCompliances[newCompliance]["statutory_provision"]+'</font>');
        $('.compliancetask', clone2).html('<font color="#0404B4">'+newCompliances[newCompliance]["compliance_name"]+'</font>');
        $('.compliancedescription', clone2).html('<font color="#0404B4">'+newCompliances[newCompliance]["description"]+'</font>');
        $('.complianceapplicable', clone2).html('<input type="checkbox" checked="checked" id="statutory'+statutoriesCount+'" class="statutoryclass'+actCount+'"><label for="statutory'+statutoriesCount+'"></label>');
        $('.accordion-content'+count).append(clone2);

        if(compliance_applicable_status == false){
          $('#statutory'+statutoriesCount).each(function() {
          this.checked = false;
        });
      }
        statutoriesCount = statutoriesCount + 1;
      }
    }

    actCount = actCount + 1;
    count++;

    $(".act-label").on("click", function(event){
      accordionstatus = false;
    });
    
    $(clone, '.actname').click(function(){
      if(accordionstatus){
        //Expand or collapse this panel
        $(this).next().slideToggle('fast');
        //Hide the other panels
        $(".accordion-content").not($(this).next()).slideUp('fast');
      }else{
        accordionstatus = true;
      }
    });
      
  }

  if(count <= 1){
    var norecordtableRow=$('#no-record-templates .font1');
    var noclone=norecordtableRow.clone();
    $('.tbody-assignstatutory').append(noclone);
    $('#activate-step-finish').hide();
  }

  /*$(document).ready(function($) {
    $(".act-label").on("click", function(event){
      accordionstatus = false;
    });

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
  });*/
}

//load unit according to filter selection
function loadunit(){

  var assignStatutoryGroupId = null;
  if($('.grouplist.active').attr('id') != undefined)
    assignStatutoryGroupId = parseInt($('.grouplist.active').attr('id'));

  var assignStatutoryLegalEntityId = 0;
  if($('.legalentitylist.active').attr('id') != undefined)
    assignStatutoryLegalEntityId = parseInt($('.legalentitylist.active').attr('id'));

  var assignStatutoryIndustryId = 0;
  if($('.industrylist.active').attr('id') != undefined)
    assignStatutoryIndustryId = parseInt($('.industrylist.active').attr('id'));

  var assignStatutoryLocationId = 0;
  if($('.locationlist.active').attr('id') != undefined)
    assignStatutoryLocationId = parseInt($('.locationlist.active').attr('id'));

  var assignStatutoryDivisionId = null;
  if($('.divisionlist.active').attr('id') != undefined){
    assignStatutoryDivisionId = parseInt($('.divisionlist.active').attr('id'));
  }
  var assignStatutoryBusinessGroupId = null;
  if($('.businessgrouplist.active').attr('id') != undefined)
    assignStatutoryBusinessGroupId = parseInt($('.businessgrouplist.active').attr('id'));

  if(assignStatutoryLegalEntityId != 0 && assignStatutoryIndustryId != 0 && assignStatutoryLocationId != 0){
      var str='';
      $('#unit').empty();
      for(var unit in unitsList){
        if(unitsList[unit]["business_group_id"] == assignStatutoryBusinessGroupId && unitsList[unit]["division_id"] == assignStatutoryDivisionId && unitsList[unit]["legal_entity_id"] == assignStatutoryLegalEntityId && unitsList[unit]["client_id"] == assignStatutoryGroupId && unitsList[unit]["industry_id"] == assignStatutoryIndustryId && $.inArray(assignStatutoryLocationId, unitsList[unit]["geography_ids"]) >= 0){
          str += '<li id="'+unitsList[unit]["unit_id"]+'" class="unitlist" >'+unitsList[unit]["unit_name"]+'</li>';
        }
      }
      $('#unit').append(str);
  }
}

$("#geographylevel").click(function(event){
  if($(event.target).attr('class') == 'geographylevellist'){
    $('.'+$(event.target).attr('class')).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(event.target).addClass("active");

    var str='';
    var assignStatutoryGeographyLevelId = parseInt(event.target.id);
    var c_id = parseInt($('.countrylist.active').attr('id'));
    $('#location').empty();
    for(var geography in geographiesList[c_id]){
      if(geographiesList[c_id][geography]["is_active"] == true && geographiesList[c_id][geography]["level_id"] == assignStatutoryGeographyLevelId){
        str += '<li id="'+geographiesList[c_id][geography]["geography_id"]+'" class="locationlist">'+geographiesList[c_id][geography]["geography_name"]+'</li>';
      }
    }
    $('#location').append(str);
  }
});

$("#group").click(function(event){
  if($(event.target).attr('class') == 'grouplist'){
    clearValues('group');
    $('.'+$(event.target).attr('class')).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(event.target).addClass("active");

    var str='';
    var assignStatutoryGroupId = parseInt(event.target.id);
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
      if(legalentitiesList[legalentity]["client_id"] == $('.grouplist.active').attr('id') && legalentitiesList[legalentity]["business_group_id"] == assignStatutoryBusinessGroupId){
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
      if(divisionsList[division]["client_id"] == $('.grouplist.active').attr('id') && divisionsList[division]["legal_entity_id"] == assignStatutoryLegalEntityId){
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

$("#location").click(function(event){
  if($(event.target).attr('class') == 'locationlist'){
    clearValues('location');
    $('.'+$(event.target).attr('class')).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(event.target).addClass("active");
    loadunit();
  }
});

$("#industry").click(function(event){
  if($(event.target).attr('class') == 'industrylist'){
    clearValues('industry');
    $('.'+$(event.target).attr('class')).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(event.target).addClass("active");
    $("#asindustry").val(event.target.id);
    loadunit();
  }
});


$("#unit").click(function(event){
    var chkstatus = $(event.target).attr('class');
    if(chkstatus != undefined){
      clearValues('unit');
    if(chkstatus == 'unitlist active'){
      displayMessage("");
      $(event.target).removeClass("active");
      var removeid = assignStatutoryUnitIds.indexOf(parseInt(event.target.id));
      assignStatutoryUnitIds.splice(removeid,1);
      var removename = assignStatutoryUnitValues.indexOf($(event.target).text());
      assignStatutoryUnitValues.splice(removename,1);
    }else{
      if(assignStatutoryUnitIds.length < mUnit){
        displayMessage("");
        $(event.target).addClass("active");
        assignStatutoryUnitIds.push(parseInt(event.target.id));
        assignStatutoryUnitValues.push($(event.target).text());
      }else{
        msg = "Maximum("+ mUnit + ") ";
        displayMessage(msg + message.maximum_units);
      }
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
  }
});

$("#domain").click(function(event){
  $('#activate-step-finish').show();
  if($(event.target).attr('class') == 'domainlist'){
    $('.'+$(event.target).attr('class')).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(event.target).addClass("active");
    make_breadcrumbs();
  }
});

//load lists on first wizard
function load_firstwizard(){

  var c_id = parseInt($('.countrylist.active').attr('id'));
  var str='';
  $('#group').empty();
  for(var group in groupcompaniesList){
    if(groupcompaniesList[group]["is_active"] == true && $.inArray(c_id, groupcompaniesList[group]["country_ids"]) >= 0){
      str += '<li id="'+groupcompaniesList[group]["client_id"]+'" class="grouplist">'+groupcompaniesList[group]["group_name"]+'</li>';
    }
  }
  $('#group').append(str);

  var str1='';
  $('#geographylevel').empty();
  for(var geographylevel in geographyLevelsList[c_id]){
    str1 += '<li id="'+geographyLevelsList[c_id][geographylevel]["l_id"]+'" class="geographylevellist">'+geographyLevelsList[c_id][geographylevel]["l_name"]+'</li>';
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

//get master data based on country selection
$("#country").click(function(event){
  if($(event.target).attr('class') == 'countrylist'){
      clearValues('country');
  $('.'+$(event.target).attr('class')).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $(event.target).addClass("active");

  function onSuccess(data){
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
mirror.getAssignStatutoryWizardOne(parseInt($('.countrylist.active').attr('id')),
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
});

//load country list
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

$("#activate-step-finish-cancel").click(function(){
$("#assignstatutory-view").show();
$("#assignstatutory-add").hide();
displayMessage('');
clearValues('all');
$(".breadcrumbs").html('');
$("#activate-step-submit").hide();
});


$(".btn-assignstatutory-add").click(function(){
$("#assignstatutory-view").hide();
$("#assignstatutory-add").show();
$("#clientstatutoryid").val('');
displayMessage('');
clearValues('all');
$(".breadcrumbs").html('');
$("#activate-step-submit").hide();
$('#activate-step-finish').show();
$("#backward-step-1").show();

$('ul.setup-panel li:eq(0)').show();
$('ul.setup-panel li:eq(0)').removeClass('disabled');
$('ul.setup-panel li:eq(0)').addClass('active');
$('ul.setup-panel li:eq(1)').removeClass('active');
$('ul.setup-panel li:eq(1)').addClass('disabled');
$('ul.setup-panel li a[href="#step-1"]').trigger('click');

/*$("#step-1").show();
$("#step-2").show();
$('ul.setup-panel li:eq(1)').css({'width': '49.5%'});*/

$(".tbody-assignstatutory").find("tbody").remove();

function onSuccess(data){
  loadCountriesList(data);
}
function onFailure(error){
  displayMessage(error);
}
mirror.getCountriesForGroup(
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

//first wizard validation
function validate_firsttab(){
  if($('.countrylist.active').text() == ''){
    displayMessage(message.country_required);
    return false;
  }else if ($('.grouplist.active').text() == ''){
    displayMessage(message.group_required);
    return false;
  }else if ($('.legalentitylist.active').text() == ''){
    displayMessage(message.legalentity_required);
    return false;
  }else if ($('.geographylevellist.active').text() == ''){
    displayMessage(message.geographylevel_required);
    return false;
  }else if ($('.locationlist.active').text() == ''){
    displayMessage(message.location_required);
    return false;
  }else if ($('.industrylist.active').text() == ''){
    displayMessage(message.industry_required);
    return false;
  }else if (assignStatutoryUnitIds.length == 0){
    displayMessage(message.unit_required);
    return false;
  }else if ($('.domainlist.active').text() == ''){
    displayMessage(message.domain_required);
    return false;
  }else{
    var checkDuplicateAssignStauttory = true;
    var unitIdTab2 = null;
    for(var entity in assignedStatutoriesList) {
      if($('.industrylist.active').text() == assignedStatutoriesList[entity]["industry_name"] && $('.domainlist.active').attr('id') == assignedStatutoriesList[entity]["domain_id"]){
        for(var j=0;j<assignStatutoryUnitIds.length;j++){
          if(assignStatutoryUnitIds[j] == assignedStatutoriesList[entity]["unit_id"] && assignedStatutoriesList[entity]["submission_status"] == 0){
            displayMessage(message.statutory_already_assigned_unit + assignStatutoryUnitValues[j]);
            checkDuplicateAssignStauttory = false;
            break;
            return false;
          }
          if(assignStatutoryUnitIds[j] == assignedStatutoriesList[entity]["unit_id"] && assignedStatutoriesList[entity]["submission_status"] == 1 && assignStatutoryUnitIds.length > 1){
            displayMessage(message.statutory_already_submitted_unit + assignStatutoryUnitValues[j]);
            checkDuplicateAssignStauttory = false;
            break;
            return false;
          }
          if(assignStatutoryUnitIds[j] == assignedStatutoriesList[entity]["unit_id"] && assignedStatutoriesList[entity]["submission_status"] == 1 && assignStatutoryUnitIds.length == 1){
            unitIdTab2 = assignedStatutoriesList[entity]["unit_id"];
          }
        }
      }
    }

    //get compliances list for selected unit from api
    if(checkDuplicateAssignStauttory){
      displayLoader();
      function onSuccess(data){
        statutoriesList = data["statutories"];
        newCompliancesList = data["new_compliances"];
        load_secondwizard();
        displayMessage("");
        hideLoader();
        return true;
      }
      function onFailure(error){
        hideLoader();
      }
      mirror.getAssignStatutoryWizardTwo(parseInt($('.countrylist.active').attr('id')),
        parseInt($('.domainlist.active').attr('id')), parseInt($('.industrylist.active').attr('id')),
        parseInt($('.locationlist.active').attr('id')), unitIdTab2,
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
  return true;
}

//create wizard
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

//save or submit assign statutory
function saveorsubmit(submissionType){
  displayMessage("");
  if (validate_secondtab()){
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
    var isApplicableStatus = false;
    for(var statutory in statutoriesList){
      var level1StatutoryId = statutoriesList[statutory]["level_1_statutory_id"];
      var applicableStatus = null;
      var notApplicableRemarks = null;

      if($('#act'+actCount).is(":checked")){
        applicableStatus = true;
        isApplicableStatus = true;
      }
      else{
        applicableStatus = false;
        notApplicableRemarks = $('#remarkvalue'+actCount).val();
        if(notApplicableRemarks.length == 0){
          displayMessage(message.act_remarks_required);
          return false;
        }else if(notApplicableRemarks.length > 500){
          displayMessage("Remarks" + message.should_not_exceed + " 500 characters");
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

  if(isApplicableStatus) {
    displayLoader();
    function onSuccess(data){
      getAssignedStatutories ();
      hideLoader();
      $(".listfilter").val('');
      $(".filter-text-box").val('');
      $("#assignstatutory-add").hide();
      $("#assignstatutory-view").show();
      $('ul.setup-panel li:eq(0)').addClass('active');
      $('ul.setup-panel li:eq(1)').addClass('disabled');
      $('ul.setup-panel li a[href="#step-1"]').trigger('click');
      $(".tbody-assignstatutory").find("tbody").remove();
    }
    function onFailure(error){
      displayMessage(error);
      hideLoader();
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
  }else{
    displayMessage(message.statutory_selection_required);
  }
  }
}
$('#activate-step-finish').on('click', function(e) {
  saveorsubmit("Save")
})
$('#activate-step-submit').on('click', function(e) {
  saveorsubmit("Submit")
})

//edit assign statutory
function displayEdit(client_statutory_id, country_id, group_id, location_id, domain_id, unit_id, submit_type){
  displayLoader();
 function onSuccess(data){
    clearValues('all');
    $('ul.setup-panel li:eq(0)').removeClass('active');
    $('ul.setup-panel li:eq(0)').addClass('disabled');
    $('ul.setup-panel li:eq(1)').removeClass('disabled');
    $('ul.setup-panel li:eq(1)').addClass('active');
    $('ul.setup-panel li a[href="#step-2"]').trigger('click');
    $("#assignstatutory-view").hide();
    $("#assignstatutory-add").show();

    if(submit_type == 'edit'){
      $("#backward-step-1").hide();
      $("#activate-step-finish").show();
      $("#activate-step-submit").hide();
    }else{
      $("#backward-step-1").hide();
      $("#activate-step-finish").hide();
      $("#activate-step-submit").show();
    }

    var arrowimage = " <img src=\'/images/chevron_black_right.png\'/> ";
    var bc_businessgroup = '';
    var bc_divisionname = '';

    if(data["business_group_name"] != null) bc_businessgroup = arrowimage + data["business_group_name"];
    if(data["division_name"] != null) bc_divisionname = arrowimage + data["division_name"];

    $(".breadcrumbs").html(data["country_name"] + arrowimage + data["group_name"] + bc_businessgroup + arrowimage +
    data["legal_entity_name"] + bc_divisionname + arrowimage + data["geography_name"] + arrowimage + data["industry_name"]
    + arrowimage + data["unit_name"] +
    arrowimage + data["domain_name"]);

    statutoriesList = data["statutories"];
    newCompliancesList = data["new_compliances"];
    $("#ascountry").val(country_id);
    $("#asgroup").val(group_id);
    $("#aslocation").val(location_id);
    $("#asdomain").val(domain_id);
    assignStatutoryUnitIds = [];
    assignStatutoryUnitIds.push(unit_id);
    $("#clientstatutoryid").val(client_statutory_id);

    load_secondwizard();
    hideLoader();
    }
    function onFailure(error){
      displayMessage(error)
      hideLoader();
    }
    mirror.getAssignedStatutoryById(parseInt(client_statutory_id),
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

//display assigned statutories list in view page
function loadCountwiseAssignedStatutoriesList(assignedStatutoriesList){
  var j = startCount + 1;
  $(".tbody-assignstatutory-list").find("tr").remove();
  if(endCount>finalList.length) endCount = finalList.length
  if(finalList.length > 0) $('.view-count-message').text("Showing " + (startCount+1) + " to " + endCount + " of " + finalList.length );

  $.each(assignedStatutoriesList, function(key, value) {
    var client_statutory_id = value["client_statutory_id"];
    var country_id = value["country_id"];
    var group_id = value["client_id"];
    var location_id = value["geography_id"];
    var domain_id = value["domain_id"];
    var unit_id = value["unit_id"];

    var businessGroup = '-';
    if(value["business_group_name"] != null){
      businessGroup = value["business_group_name"];
    }

    var divisionName = '-';
    if(value["division_name"] != null){
      divisionName = value["division_name"];
    }

    var tableRow=$('#templates .table-assignstatutory .table-row');
    var clone=tableRow.clone();
    $('.tbl_sno', clone).text(j);
    $('.tbl_country', clone).text(value["country_name"]);
    $('.tbl_group', clone).text(value["group_name"]);
    $('.tbl_businessgroup', clone).text(businessGroup);
    $('.tbl_legalentity', clone).text(value["legal_entity_name"]);
    $('.tbl_division', clone).text(divisionName);
    $('.tbl_location', clone).text(value["geography_name"]);
    $('.tbl_industry', clone).text(value["industry_name"]);
    $('.tbl_unit', clone).text(value["unit_name"]);
    $('.tbl_domain', clone).text(value["domain_name"]);

    $('.edit-icon').attr('title', 'Edit');
    $('.view-icon').attr('title', 'View & Submit');

    if(value["submission_status"] == 1){
      $('.tbl_status', clone).text('Submitted');
      $(".edit-icon", clone).removeClass('edit-icon');
      $(".view-icon", clone).removeClass('view-icon');
    }
    else{
      $('.tbl_status', clone).text("Pending");
      $(".edit-icon", clone).on("click", function() {
          displayEdit(client_statutory_id, country_id, group_id, location_id, domain_id, unit_id, 'edit');
      });
      $(".view-icon", clone).on("click", function() {
          displayEdit(client_statutory_id, country_id, group_id, location_id, domain_id, unit_id, 'submit');
      });
    }
    $('.tbody-assignstatutory-list').append(clone);
    j = j + 1;
  });
}

function get_sub_array(object, start, end){
  if(!end){ end=-1;}
  return object.slice(start, end);
}

//create pagination based on total records
function loadAssignedStatutoriesList(assignedStatutoriesList){
  var listSize = Math.ceil(assignedStatutoriesList.length / pageSize);
  startCount = 0;
  endCount = pageSize;
  if(assignedStatutoriesList.length > 0){
    var str='<li id="pview1">«</li>';
    $('.pagination').empty();
    var j;
    for(j=1; j<=listSize; j++){
      if(j==1){
        str += '<li class="page active" id="pageview'+j+'">'+j+'</li>';
      }else{
        str += '<li class="page" id="pageview'+j+'">'+j+'</li>';
      }
    }
    str += '<li id="pview'+(j-1)+'">»</li>';
    $('.pagination').append(str);
  }else{
    $('.pagination').empty();
    $('.view-count-message').text('');
  }

  finalList = assignedStatutoriesList;
  var sub_list = get_sub_array(finalList, startCount, endCount);
  loadCountwiseAssignedStatutoriesList(sub_list);
}

//pagination process
$(".pagination").click(function(event){
  var text = $(event.target).attr('id');
  var pageId = text.substring(text.lastIndexOf('w') + 1);
  var type = '.page'

  $(type).each( function( index, el ) {
    $(el).removeClass( "active" );
  });
  $('#pageview'+pageId).addClass("active");

  startCount = pageSize * (pageId-1);
  endCount = pageSize * pageId;

  var sub_list = get_sub_array(finalList, startCount, endCount);
  loadCountwiseAssignedStatutoriesList(sub_list);
});

//get assigned statutories list from api
function getAssignedStatutories () {
  function onSuccess(data){
    assignedStatutoriesList = data["assigned_statutories"];
    loadAssignedStatutoriesList(assignedStatutoriesList);
  }
  function onFailure(error){
    displayMessage(error)
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
}

//filter process
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
    var filter3val = '-';
    if(assignedStatutoriesList[entity]["business_group_name"] != null) filter3val = assignedStatutoriesList[entity]["business_group_name"];

    var filter4val = assignedStatutoriesList[entity]["legal_entity_name"];

    var filter5val = '-';
    if(assignedStatutoriesList[entity]["division_name"] != null) filter5val = assignedStatutoriesList[entity]["division_name"];

    var filter6val = assignedStatutoriesList[entity]["geography_name"];
    var filter7val = assignedStatutoriesList[entity]["industry_name"];
    var filter8val = assignedStatutoriesList[entity]["unit_name"];
    var filter9val = assignedStatutoriesList[entity]["domain_name"];
    var filter10val = null;
    if(assignedStatutoriesList[entity]["submission_status"] == 1)
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

//initialization and UL filter process
$(document).ready(function () {
  hideLoader();
  getAssignedStatutories ();
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

  $("#filter_group").keyup( function() {
    var filter = $("#filter_group").val().toLowerCase();
    var lis = document.getElementsByClassName('grouplist');
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

  $("#filter_geographylevel").keyup( function() {
    var filter = $("#filter_geographylevel").val().toLowerCase();
    var lis = document.getElementsByClassName('geographylevellist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
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
      if (~name.toLowerCase().indexOf(filter))
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

//create tool tip
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