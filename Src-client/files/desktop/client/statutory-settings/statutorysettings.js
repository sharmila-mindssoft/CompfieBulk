var assignedStatutoriesList;
var statutoriesList;
var sList;
var assignedStatutories = [];
var accordionstatus = true;
var finalList;
var pageSize = 100;
var startCount;
var endCount;
var totalRecord;
var lastActName = '';
var lastDomainName = '';

var count = 1;
var statutoriesCount = 1;
var actCount = 1;
var s_endCount = 0;

function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
}

//view/hide act remark textbox based on act applicable selection
function actstatus(element){
  var remarkbox = '.remark'+$(element).val();
  var changestatusStatutories = '.statutoryclass'+$(element).val();

  if ($(element).is(":checked"))
  {
    $(remarkbox).hide();
    $(changestatusStatutories).each(function() {
      var cremark = $('.cremarkview'+this.value).text();
      this.checked = true;
      if($('#applicable'+this.value).val() == "false"){
        if(cremark != ''){
          $('.cremarkview'+this.value).show();
        }else{
          $('.cremarkadd'+this.value).show();
        }
      }
    });
  }else{
    $(remarkbox).show();
    $(changestatusStatutories).each(function() {
      this.checked = false;
      $('.cremarkadd'+this.value).hide();
    });
  }
  accordionstatus = false;
}

//view/hide compliance remark textbox based on compliance opted selection
function compliancestatus(element, viewremarks){
  var remarkadd = '.cremarkadd'+$(element).val();
  var remarkview = '.cremarkview'+$(element).val();
  var applicable = '#applicable'+$(element).val();
  var sClass = $(element).attr('class').split(' ')[1];

  $('#cremarkvalue'+$(element).val()).val('');
  var optedval = $(element).is(":checked");
  var applicableval = $(applicable).val();

  var addStatus = false;
  if(applicableval == 'true'){
    if(optedval){
      addStatus = true;
    }
  }else{
    if(optedval == false){
      addStatus = true;
    }
  }

  if(addStatus){
    $(remarkadd).hide();
    if(viewremarks) $(remarkview).show();
  }else{
    $(remarkadd).show();
    $(remarkview).hide();
  }

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

    $('.'+sClass).each(function() {
    var aStatus = $('#applicable'+this.value).val();
    var oStatus = "false";
    var cremark = $('.cremarkview'+this.value).text();
    if($(this).is(":checked")){
      oStatus = "true";
    }
    if(aStatus == oStatus){
      $('.cremarkadd'+this.value).hide();
    }
    else{
      if(cremark != ''){
        $('.cremarkview'+this.value).show();
      }else{
        $('.cremarkadd'+this.value).show();
        $('.cremarkview'+this.value).hide();
      }
    }
  });

  }else{
    $('#act'+actSelect).prop("checked",false);
    $('.remark'+actSelect).show();

    $('.'+sClass).each(function() {
      $('.cremarkadd'+this.value).hide();
    });
  }
}

function part_compliance (remark) {
    if (remark.length > 15) {
        return (remark.substring(0, 15) + "...");
    }
    else {
        return remark;
    }
}

//load compliance list
function load_statutory(sList){
  if(statutoriesCount <= 1){
    $(".tbody-statutorysettings").find("tbody").remove();
  }
  for(var statutory in sList){
    var domainName = sList[statutory]["domain_name"];
    if(domainName != lastDomainName){
      var tableRow3 = $('#head-templates .tbl_heading');
      var clone3 = tableRow3.clone();
      $('.heading', clone3).html(domainName);
      $('.tbody-statutorysettings').append(clone3);
    }
    var actname = sList[statutory]["level_1_statutory_name"];
    var applicable_status = sList[statutory]["opted_status"];
    var not_applicable_remarks = sList[statutory]["not_applicable_remarks"];
    if (not_applicable_remarks == null) not_applicable_remarks = '';

    if(actname != lastActName){
      var acttableRow=$('#act-templates .font1 .tbody-heading');
      var clone=acttableRow.clone();

      $('.act-ck-box', clone).attr('id', 'act'+actCount);
      $('.act-ck-box', clone).val(actCount);
      //$('.act-label', clone).text(actname);
      $('.act-label', clone).attr('for', 'act'+actCount);

	    $('.act-remark', clone).addClass('remark'+actCount);
      $('.remark-text', clone).attr('id', 'remarkvalue'+actCount);
      $('.remark-text', clone).val(not_applicable_remarks);
      $('.actname', clone).text(actname);

      $('.tbody-statutorysettings').append(clone);
      $('.tbody-statutorysettings').append('<tbody class="accordion-content accordion-content'+count+' default"></tbody>');

      var complianceHeadingtableRow=$('#statutory-templates .compliance-heading');
      var clone1=complianceHeadingtableRow.clone();
      $('.accordion-content'+count).append(clone1);

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

    if(applicable_status == false){
      $('.remark'+(actCount-1)).show();
      $('#act'+(actCount-1)).each(function() {
        this.checked = false;
      });
    }

    var statutoryprovision = '';
    var compliance_id = sList[statutory]["compliance_id"];
    var client_compliance_id = sList[statutory]["client_compliance_id"];
    var client_statutory_id = sList[statutory]["client_statutory_id"];
    var compliance_applicable_status = sList[statutory]["compliance_applicable_status"];
    var compliance_opted_status = sList[statutory]["compliance_opted_status"];
    var compliance_remarks = sList[statutory]["compliance_remarks"];
    var compliance_remarks_part = '';
    var viewremarks = true;
    if (compliance_remarks == null) {
      compliance_remarks = '';
      viewremarks = false;
    }else{
      compliance_remarks_part = part_compliance(compliance_remarks)
    }
    var isNew = sList[statutory]["is_new"];
    var openTag = '';
    var closeTag = ''
    if(isNew){
      openTag = '<font color="#0404B4">';
      closeTag = '</font>'
    }

    var optedTitle = 'Not Opted';
    if(compliance_opted_status){
      optedTitle = 'Opted';
    }
    var combineId = compliance_id + '-' + client_statutory_id + '-' + client_compliance_id;

    var complianceDetailtableRow=$('#statutory-values .table-statutory-values .compliance-details');
    var clone2=complianceDetailtableRow.clone();
    $('.sno', clone2).html(openTag + statutoriesCount + closeTag);
    $('.combineid-class', clone2).attr('id', 'combineid'+statutoriesCount);
    $('.combineid-class', clone2).val(combineId);
    $('.oldremark-class', clone2).attr('id', 'oldremark'+statutoriesCount);
    $('.oldremark-class', clone2).val(compliance_remarks);

    $('.statutoryprovision', clone2).html(openTag + sList[statutory]["statutory_provision"] + closeTag);
    $('.compliancetask', clone2).html( openTag + sList[statutory]["compliance_name"] + closeTag);
    $('.compliancedescription', clone2).html( openTag + sList[statutory]["description"] + closeTag);

    $('.compliance-ck-box', clone2).attr('id', 'statutory'+statutoriesCount);
  	$('.compliance-ck-box', clone2).val(statutoriesCount);
  	$('.compliance-ck-box', clone2).addClass('statutoryclass'+(actCount-1));
  	$('.compliance-label', clone2).attr('for', 'statutory'+statutoriesCount);
  	$(".compliance-ck-box", clone2).on("click", function() {
      compliancestatus(this, viewremarks);
    });

  	$('.cremarkadd', clone2).addClass('cremarkadd'+statutoriesCount);
  	$('.cremarkvalue', clone2).attr('id', 'cremarkvalue'+statutoriesCount);
  	$('.remark-text', clone2).val(not_applicable_remarks);

  	$('.cremarkview', clone2).addClass('cremarkview'+statutoriesCount);
  	$('.tipso_style', clone2).attr('title', compliance_remarks);
  	$('.crval', clone2).html(compliance_remarks_part);
	
    if(compliance_applicable_status){
      $('.applicable', clone2).html('<img src=\'/images/tick1bold.png\' title="Applicable"/> <input type="hidden" id="applicable'+statutoriesCount+
        '" value="'+compliance_applicable_status+'"> </input> ');
    }
    else{
      $('.applicable', clone2).html('<img src=\'/images/deletebold.png\' title="Not Applicable"/> <input type="hidden" id="applicable'+statutoriesCount+
        '" value="'+compliance_applicable_status+'"> </input>');
    }
    $('.accordion-content'+(count-1)).append(clone2);

    if(compliance_remarks == ''){
      $('.cremarkview'+statutoriesCount).hide();
    }

    if(compliance_opted_status == false){
      $('#statutory'+statutoriesCount).each(function() {
        this.checked = false;
      });
    }
    statutoriesCount = statutoriesCount + 1;
    lastDomainName = domainName;
    lastActName = actname;

    $('.remark-text').on('input', function (e) {
      this.value = isCommon($(this));
    });

    $('.cremarkvalue').on('input', function (e) {
      this.value = isCommon($(this));
    });
    
  }

  if(statutoriesCount > 1){
    $('.compliance_count').text("Showing " + 1 + " to " + (statutoriesCount-1) + " of " + totalRecord);
  }else{
    $('.compliance_count').text('');
  }

  if(totalRecord <= statutoriesCount){
    $('#pagination').hide();
    $('#submit').show();
    $('#cancel').show();
    /*$(document).ready(function($) {
      $(".act-label").on("click", function(event){
        accordionstatus = false;
      });
      $("#accordion").find(".accordion-toggle").click(function(){
        if(accordionstatus){
          //Expand or collapse this panel
          $(this).next('tbody').slideToggle('fast');
          //Hide the other panels
          $(".accordion-content").not($(this).next()).slideUp('fast');
        }else{
          accordionstatus = true;
        }
      });
    });*/
  }
  if($("#is_closed").val() == 'true'){
    $('#submit').hide();
  }
}

//pagination process
$('#pagination').click(function(){
  unit_id =  parseInt($("#unit").val());
  s_endCount = statutoriesCount - 1;
  displayLoader();
  client_mirror.getStatutorySettingsCompliance(unit_id, s_endCount,
    function (error, response) {
        if (error == null){
          sList = response["statutories"];
          totalRecord = response["total_count"];
          if(parseInt(totalRecord) > s_endCount){
            $('#pagination').show();
            $('#submit').hide();
            $('#cancel').hide();
          }else{
            $('#pagination').hide();
            $('#submit').show();
            $('#cancel').show();
          }
          load_statutory(sList);
          hideLoader();
        }
        else {
          displayMessage(error);
          hideLoader();
        }
    })
});

//update statutory setting
function submit_statutory(){
  var password = $('#password').val();
  if(password == ''){
    $('.popup-error-msg').html(message.enter_password);
    $('#password').focus();
  }else{
    displayLoader();
    var uId = $("#unit").val();
    var uVal = $("#unitval").val();
    function onSuccess(data){
      $('.overlay').css("visibility","hidden");
      $('.overlay').css("opacity","0");
      $('#password').val("");
      getStatutorySettings ();
      $("#statutorysettings-add").hide();
      $("#statutorysettings-view").show();
      $(".listfilter").val('');
      hideLoader();
    }
    function onFailure(error){
      if(error == 'InvalidPassword'){
        $('.popup-error-msg').html(message.enter_correct_password);
        $('#password').focus();
        $('#password').val("");
      }else{
         $('.popup-error-msg').html(error);
      }
      hideLoader();
    }
    client_mirror.updateStatutorySettings(password, uVal, parseInt(uId), assignedStatutories,
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

$('.close').click(function(){
  //$('#unitidval').val("");
  $('#password').val("");
  $('.overlay').css("visibility","hidden");
  $('.overlay').css("opacity","0");
});


//save assigned statutories data in assignedStatutories variable
$("#submit").click(function() {
  $('#password').focus();
  displayLoader();
  displayMessage("");
  assignedStatutories = [];

  var saveflag = true;
  var totalCompliance = 1;

  for(var i=1; i<=(actCount-1); i++){
    var applicableStatus = null;
    var notApplicableRemarks = null;
    if($('#act'+i).is(":checked")){
      applicableStatus = true;
    }
    else{
      applicableStatus = false;
      notApplicableRemarks = $('#remarkvalue'+i).val().trim();
      if(notApplicableRemarks.length==0){
        displayMessage(message.act_remarks_opted_required);
        saveflag = false;
        hideLoader();
        return false;
      }
      else if(notApplicableRemarks.length > 500){
        displayMessage("Act Remarks" + message.should_not_exceed + " 500 characters");
        saveflag = false;
        hideLoader();
        return false;
      }
    }
    var actComplianceCount = $('.statutoryclass'+i).length;
    for(var j=1; j<=actComplianceCount; j++){
      var combineidVal = $('#combineid'+totalCompliance).val().split('-');
      var client_statutory_id = parseInt(combineidVal[1]);
      var complianceId = parseInt(combineidVal[0]);
      var clientComplianceId = parseInt(combineidVal[2]);
      var compliance_remarks = $('#oldremark'+totalCompliance).val();
      var complianceApplicableStatus = false;
      var compliancenotApplicableRemarks = null;

      var optedval = $('#statutory'+totalCompliance).is(":checked");
      var applicableval = $('#applicable'+totalCompliance).val();
      var addStatus = true;
      if(applicableval == 'true'){
        if(optedval){
          addStatus = false;
        }
      }else{
        if(optedval == false){
          addStatus = false;
        }
      }
      if($('#statutory'+totalCompliance).is(":checked")){
        complianceApplicableStatus = true;
      }

      if(addStatus){
        $('#cremarkvalue'+totalCompliance).show();
        if($('#cremarkvalue'+totalCompliance).val().trim() != ''){
          compliancenotApplicableRemarks = $('#cremarkvalue'+totalCompliance).val().trim();
        }else{
          compliancenotApplicableRemarks = compliance_remarks;
        }
        if(compliancenotApplicableRemarks == '' && compliance_remarks == '' && applicableStatus == true){
          displayMessage(message.compliance_remarks_opted_required);
          saveflag = false;
          hideLoader();
          return false;
        }
        else if(compliancenotApplicableRemarks.length > 500 && applicableStatus == true){
          displayMessage("Compliance Remarks" + message.should_not_exceed + " 500 characters");
          saveflag = false;
          hideLoader();
          return false;
        }
      }
      assignedstatutoriesData = client_mirror.updateStatutory(client_statutory_id, clientComplianceId, applicableStatus, notApplicableRemarks, complianceId, complianceApplicableStatus, compliancenotApplicableRemarks);
      assignedStatutories.push(assignedstatutoriesData);
      totalCompliance++;
    }
  }
  if(saveflag){
    $('.overlay').css("visibility","visible");
    $('.overlay').css("opacity","1");
    $('.popup-error-msg').html("");
    $('#password').val("");
    $('#password').focus();
    window.scrollTo(0, 0);
    hideLoader();
  }
});

$("#cancel").click(function() {
  $("#statutorysettings-add").hide();
  $("#statutorysettings-view").show();
});

//edit statutiry settings for already assigned unit
function displayEdit(unit_id, dispBusinessGroup, dispLegalEntity, dispDivision, dispUnit, isClosed){
  displayLoader();
  s_endCount = 0;
  client_mirror.getStatutorySettingsCompliance(unit_id, parseInt(s_endCount),
    function (error, response) {
      if (error == null){
        sList = response["statutories"];
        totalRecord = response["total_count"];
        $(".tbl_businessgroup_disp").text(dispBusinessGroup);
        $(".tbl_legalentity_disp").text(dispLegalEntity);
        $(".tbl_division_disp").text(dispDivision);
        $(".tbl_unit_disp").text(dispUnit);
        $("#unit").val(unit_id);
        $("#unitval").val(dispUnit);
        $("#is_closed").val(isClosed);

        count=1;
        statutoriesCount= 1;
        actCount = 1;
        lastActName = '';
        lastDomainName = '';
        displayMessage("");
        $("#statutorysettings-view").hide();
        $("#statutorysettings-add").show();

        if(parseInt(totalRecord) > s_endCount){
          $('#pagination').show();
          $('#submit').hide();
          $('#cancel').hide();
        }else{
          $('#pagination').hide();
          $('#submit').show();
          $('#cancel').show();
        }
        load_statutory(sList);
        hideLoader();
      }
      else {
        displayMessage(error);
        hideLoader();
      }
    }
  )
}

//diaplay statutory settings details in view page
function loadCountwiseStatutorySettings(assignedStatutoriesList){
  var j = startCount + 1;
  var unit_id = 0;
  $(".tbody-statutorysettings-list").find("tr").remove();
  if(endCount>finalList.length) endCount = finalList.length
  if(finalList.length > 0) $('.view-count-message').text("Showing " + (startCount+1) + " to " + endCount + " of " + finalList.length);

    for(var entity in assignedStatutoriesList) {

      var isNew = assignedStatutoriesList[entity]["is_new"];
      var openTag = '';
      var closeTag = ''
      if(isNew){
        openTag = '<font color="#0404B4">';
        closeTag = '</font>'
      }

      unit_id = assignedStatutoriesList[entity]["unit_id"];
      var bGroup = assignedStatutoriesList[entity]["business_group_name"];
      if(bGroup == null){
        bGroup = '-';
      }
      var dName = assignedStatutoriesList[entity]["division_name"];
      if(dName == null){
        dName = '-';
      }
      var lEntity = assignedStatutoriesList[entity]["legal_entity_name"];
      var uName = assignedStatutoriesList[entity]["unit_name"];
      var isClosed = assignedStatutoriesList[entity]["is_closed"];

      var tableRow=$('#templates .table-statutorysettings .table-row');
      var clone=tableRow.clone();
      $('.tbl_sno', clone).html(openTag + j + closeTag);
      $('.tbl_country', clone).html(openTag + assignedStatutoriesList[entity]["country_name"] + closeTag);
      $('.tbl_businessgroup', clone).html(openTag + bGroup + closeTag);
      $('.tbl_legalentity', clone).html(openTag + lEntity + closeTag);
      $('.tbl_division', clone).html(openTag + dName + closeTag);
      $('.tbl_unit', clone).html(openTag + uName + closeTag);
      $('.tbl_domain', clone).html(openTag + assignedStatutoriesList[entity]["domain_names"] + closeTag);
      $('.tbl_edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+unit_id+',\''+
        bGroup+'\',\''+lEntity+'\',\''+dName+'\',\''+uName+'\','+isClosed+')"/>');

      $('.tbody-statutorysettings-list').append(clone);
      j = j + 1;
    }
}

function get_sub_array(object, start, end){
    if(!end){ end=-1;}
    return object.slice(start, end);
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
  loadCountwiseStatutorySettings(sub_list);
});

//create pagination according to statutory setting list size
function loadStatutorySettingsList(assignedStatutoriesList) {
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

  loadCountwiseStatutorySettings(sub_list);
}

//get statutory setting from api
function getStatutorySettings () {
  displayLoader();
  function onSuccess(data){
    assignedStatutoriesList = data["statutories"];
    loadStatutorySettingsList(assignedStatutoriesList);
    hideLoader();
  }
  function onFailure(error){
    custom_alert(error);
    hideLoader();
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

//filter process
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

     var filter2val = '-';
    if(assignedStatutoriesList[entity]["business_group_name"] != null) filter2val = assignedStatutoriesList[entity]["business_group_name"];

    var filter3val = assignedStatutoriesList[entity]["legal_entity_name"];

    var filter4val = '-';
    if(assignedStatutoriesList[entity]["division_name"] != null) filter4val = assignedStatutoriesList[entity]["division_name"];

    var filter5val = assignedStatutoriesList[entity]["unit_name"];
    var domainList = assignedStatutoriesList[entity]["domain_names"];
    var domains = '';
    for(var i=0; i<domainList.length; i++){
      domains += domainList[i];
    }
    var filter6val = domains;

    if (~filter1val.toLowerCase().indexOf(filter1) && ~filter2val.toLowerCase().indexOf(filter2) && ~filter3val.toLowerCase().indexOf(filter3) && ~filter4val.toLowerCase().indexOf(filter4) && ~filter5val.toLowerCase().indexOf(filter5) && ~filter6val.toLowerCase().indexOf(filter6) )
    {
      filteredList.push(assignedStatutoriesList[entity]);
    }
  }
  loadStatutorySettingsList(filteredList);
  });

//initialization
$(document).ready(function () {
  getStatutorySettings ();
});