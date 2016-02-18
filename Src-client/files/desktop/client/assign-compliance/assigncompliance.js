var countriesList;
var businessgroupsList;
var legalentitiesList;
var divisionsList;
var unitsList;
var usersList;
var assignStatutoryUnitIds = [];
var assignStatutoryUnitValues = [];
var statutoriesList;


function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
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
}

function actstatus(element){
  /*var remarkbox = '.remark'+$(element).val();
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
  }*/
}


function load_secondwizard(){
  var count=1;
  var statutoriesCount= 1;
  var actCount = 1;
  $(".tbody-assignstatutory").find("tbody").remove();
  for(var statutory in statutoriesList){
    var actname = statutory;
    
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
   
    /*$('.tbody-assignstatutory').append('<tbody class="accordion-content accordion-content'+count+'"></tbody>');
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
    }*/

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

function validate_firsttab(){
  if($('.countrylist.active').text() == ''){
    displayMessage("Country Required");
    return false;
  /*}else if ($('.legalentitylist.active').text() == ''){
    displayMessage("Legal Entity Required");
    return false;
  }else if (assignStatutoryUnitIds.length == 0){
    displayMessage("Unit Required");
    return false;*/
  }else{

    function onSuccess(data){
      statutoriesList = data["statutories"];
      load_secondwizard();
    }
    function onFailure(error){
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

    displayMessage("");
    return true;
  }    
}

function validate_secondtab(){
  return true;
}

function validate_thirdtab(){
  return true;
}

function saveorsubmit(submissionType){/*
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
  }*/
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
  //savestatutorymapping();
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

function load_firstwizard(){
  var str='';
  $('#country').empty();
    for(var country in countriesList){
      if(countriesList[country]["is_active"] == true){
      str += '<li id="'+countriesList[country]["country_id"]+'" class="countrylist">'+countriesList[country]["country_name"]+'</li>';
    }
  }
  $('#country').append(str);
}


function getAssignCompliances () {
  function onSuccess(data){
    countriesList = data["countries"];
    businessgroupsList = data["business_groups"];
    legalentitiesList = data["legal_entities"];
    divisionsList = data["divisions"];
    unitsList = data["units"];
    usersList = data["users"];
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

});