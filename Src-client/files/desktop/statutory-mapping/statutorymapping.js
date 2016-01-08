var statutoryMappingsList;
var geographyLevelsList;
var geographiesList;
var countriesList;
var domainsList;
var industriesList;
var statutoryNaturesList;
var statutoryLevelsList;
var statutoriesList;
var complianceFrequencyList;
var complianceDurationTypeList;
var complianceRepeatTypeList;
var complianceApprovalStatusList;
var sm_countryid='';
var sm_domainid='';
var sm_statutorynatureid='';
var sm_industryids=[];
var sm_countryval='';
var sm_domainval='';
var sm_industryvals = [];
var sm_statutorynatureval='';
var sm_statutoryids = [];
var disp_statutories = [];
var statutory_dates = [];
var sm_geographyids = [];
var compliances = [];

function clearMessage() {
  $(".error-message").hide();
  $(".error-message").text("");
}
function displayMessage(message) {
  $(".error-message").text(message);
  $(".error-message").show();
}

function load_selectdomain_master(){
    //load country details
    var clsval='.countrylist';
    var clsval1='countrylist';
    var str='';
    $('#country').empty();
      for(var country in countriesList){
        var countryid = countriesList[country]["country_id"];
        var dispcountryname = countriesList[country]["country_name"];
        if(countriesList[country]["is_active"] == true){
        str += '<li id="'+countryid+'" class="'+clsval1+'" onclick="activate(this,'+countryid+',\''+dispcountryname+'\',\''+clsval+'\')" ><span class="filter1_name">'+dispcountryname+'</span></li>';
      }
    }
    $('#country').append(str); 

    //load domain details
    var clsval='.domainlist';
    var clsval1='domainlist';
    var str='';
    $('#domain').empty();
    for(var domain in domainsList){
      var domainid = domainsList[domain]["domain_id"];
      var dispdomainname = domainsList[domain]["domain_name"];
      if(domainsList[domain]["is_active"] == true){
      str += '<li id="'+domainid+'" class="'+clsval1+'" onclick="activate(this,'+domainid+',\''+dispdomainname+'\',\''+clsval+'\')" ><span class="filter2_name">'+dispdomainname+'</span></li>';
    }
    }
    $('#domain').append(str);

    //load industry details
    var clsval='.industrylist';
    var clsval1='industrylist';
    var str='';
    $('#industry').empty();
    for(var industry in industriesList){
      var industryid = industriesList[industry]["industry_id"];
      var dispindustryname = industriesList[industry]["industry_name"];
      if(industriesList[industry]["is_active"] == true){
      str += '<li id="'+industryid+'" class="'+clsval1+'" onclick="multiactivate(this,'+industryid+',\''+dispindustryname+'\',\''+clsval+'\')" ><span class="filter3_name">'+dispindustryname+'</span></li>';
    }
    }
    $('#industry').append(str);

    //load statutorynature details
    var clsval='.statutorynaturelist';
    var clsval1='statutorynaturelist';
    var str='';
    $('#statutorynature').empty();
    for(var statutorynature in statutoryNaturesList){
      var statutorynatureid = statutoryNaturesList[statutorynature]["statutory_nature_id"];
          var dispstatutoryname = statutoryNaturesList[statutorynature]["statutory_nature_name"];
      if(statutoryNaturesList[statutorynature]["is_active"] == true){
      str += '<li id="'+statutorynatureid+'" class="'+clsval1+'" onclick="activate(this,'+statutorynatureid+',\''+dispstatutoryname+'\',\''+clsval+'\')" ><span class="filter4_name">'+dispstatutoryname+'</span></li>';
    }
    }
    $('#statutorynature').append(str);

    //load compliance frequency selectbox
    for (var compliancefrequency in complianceFrequencyList) {
    var option = $("<option></option>");
    option.val(complianceFrequencyList[compliancefrequency]["frequency_id"]);
    option.text(complianceFrequencyList[compliancefrequency]["frequency"]);
    $("#compliance_frequency").append(option);
    }

    //load compliance duration type selectbox
    for (var compliancedurationtype in complianceDurationTypeList) {
    var option = $("<option></option>");
    option.val(complianceDurationTypeList[compliancedurationtype]["duration_type_id"]);
    option.text(complianceDurationTypeList[compliancedurationtype]["duration_type"]);
    $("#duration_type").append(option);
    }

    //load compliance repeat type selectbox
    for (var compliancerepeattype in complianceRepeatTypeList) {
    var option = $("<option></option>");
    option.val(complianceRepeatTypeList[compliancerepeattype]["repeat_type_id"]);
    option.text(complianceRepeatTypeList[compliancerepeattype]["repeat_type"]);
    $("#repeats_type").append(option);
    }
  }
  
$(".btn-statutorymapping-add").click(function(){
$("#statutorymapping-view").hide();
$("#statutorymapping-add").show();
$("#edit_sm_id").val('');
displayMessage('');
sm_countryid='';
sm_domainid='';
sm_statutorynatureid='';
sm_countryval='';
sm_domainval='';
sm_statutorynatureval='';
sm_statutoryids=[];
sm_industryids=[];
compliances = [];
load_selectdomain_master();
$(".tbody-statutory-list").find("tr").remove();
$(".tbody-compliance-list").find("tr").remove();
$(".tbody-statutory-level").find("div").remove();
$(".tbody-geography-level").find("div").remove();
});

function getStatutoryMappings(){
  function onSuccess(data){
    industriesList = data["industries"];
    statutoryLevelsList = data["statutory_levels"];
    statutoriesList = data["statutories"];
    countriesList = data["countries"];
    domainsList = data["domains"];
    geographyLevelsList = data["geography_levels"];
    statutoryNaturesList = data["statutory_natures"];
    geographiesList = data["geographies"];
    statutoryMappingsList = data["statutory_mappings"];
    complianceFrequencyList = data["compliance_frequency"];
    complianceDurationTypeList = data["compliance_duration_type"];
    complianceRepeatTypeList = data["compliance_repeat_type"];
    complianceApprovalStatusList = data["compliance_approval_status"];
    
    loadStatutoryMappingList(statutoryMappingsList);
  }
  function onFailure(error){
  }
  mirror.getStatutoryMappings(
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
function loadStatutoryMappingList(statutoryMappingsList) {
  var j = 1;
  var imgName = '';
  var passStatus = '';
  var statutorymappingId = 0;
  var isActive = false;
  var industryName = '';
  var statutoryNatureName = '';
  var countryName = '';
  var domainName = '';
  var approvalStatus = '';

  $(".tbody-statutorymapping-list").find("tr").remove();
  for(var entity in statutoryMappingsList) {
    statutorymappingId = entity;
    industryName = statutoryMappingsList[entity]["industry_names"];
    statutoryNatureName = statutoryMappingsList[entity]["statutory_nature_name"];        
    var statutoryMappings='';
    for(var i=0; i<statutoryMappingsList[entity]["statutory_mappings"].length; i++){
      statutoryMappings = statutoryMappings + statutoryMappingsList[entity]["statutory_mappings"][i] + " <br>";
    }
    var complianceNames='';
    for(var i=0; i<statutoryMappingsList[entity]["compliance_names"].length; i++){
      complianceNames = complianceNames + statutoryMappingsList[entity]["compliance_names"][i] + " <br>";
    }

    for(approvalstatuslist in complianceApprovalStatusList){
      if(statutoryMappingsList[entity]["approval_status"] == complianceApprovalStatusList[approvalstatuslist]["approval_status_id"]){
        approvalStatus = complianceApprovalStatusList[approvalstatuslist]["approval_status"];
      }
    }

    statutoryMappings = statutoryMappings.replace(/>>/gi,' <img src=\'/images/right_arrow.png\'/> ');
    countryName = statutoryMappingsList[entity]["country_name"];
    domainName = statutoryMappingsList[entity]["domain_name"];
    isActive = statutoryMappingsList[entity]["is_active"];
    if(isActive == true) {
      passStatus= false;
      imgName="icon-active.png"
    }
    else {
      passStatus=true;
      imgName="icon-inactive.png"
     }
     if(approvalStatus == '0'){
      approvalStatus = "Pending";
     }
    var tableRow=$('#templates .table-statutorymapping .table-row');
    var clone=tableRow.clone();
    $('.sno', clone).text(j);
    $('.country', clone).text(countryName);
    $('.domain', clone).text(domainName);
    $('.industry', clone).text(industryName);
    $('.statutorynature', clone).text(statutoryNatureName);
    $('.statutory', clone).html(statutoryMappings);
    $('.compliancetask', clone).html(complianceNames);
    $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+statutorymappingId+')"/>');
    $('.status', clone).html('<img src=\'/images/'+imgName+'\' onclick="changeStatus('+statutorymappingId+','+passStatus+')"/>');
    $('.approvalstatus', clone).text(approvalStatus);
    $('.tbody-statutorymapping-list').append(clone);
    j = j + 1;
    }
  }

  function changeStatus (statutorymappingId,isActive) {
    function onSuccess(data){
      getStatutoryMappings();
      displayMessage("Status Changed Successfully");
    }
    function onFailure(error){
    }
    mirror.changeStatutoryMappingStatus(statutorymappingId, isActive,
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
    for(var entity in statutoryMappingsList) {
      var filter1val = statutoryMappingsList[entity]["country_name"];
      var filter2val = statutoryMappingsList[entity]["domain_name"];
      var filter3val = statutoryMappingsList[entity]["industry_names"];
      var filter4val = statutoryMappingsList[entity]["statutory_nature_name"];

      var filter5val='';
      for(var i=0; i<statutoryMappingsList[entity]["statutory_mappings"].length; i++){
        filter5val = filter5val + statutoryMappingsList[entity]["statutory_mappings"][i] + " <br>";
      }
      var filter6val='';
      for(var i=0; i<statutoryMappingsList[entity]["compliance_names"].length; i++){
        filter6val = filter6val + statutoryMappingsList[entity]["compliance_names"][i] + " <br>";
      }

      if (~filter1val.toLowerCase().indexOf(filter1) && ~filter2val.toLowerCase().indexOf(filter2) && ~filter3val.toLowerCase().indexOf(filter3) && ~filter4val.toLowerCase().indexOf(filter4) && ~filter5val.toLowerCase().indexOf(filter5) && ~filter6val.toLowerCase().indexOf(filter6)) 
      {
        filteredList.push(statutoryMappingsList[entity]);
      }   
    }
    loadStatutoryMappingList(filteredList);
  });

  

  
  //check & uncheck list data for single selection
  function activate(element, id, dispname, type){
    $(type).each( function( index, el ) {
      $(el).removeClass( "active" );
    });
    $(element).addClass("active");

      var checkbox_status = $(element).attr('class');
      if(checkbox_status == 'countrylist active'){
        sm_countryid = id;
        sm_countryval = dispname;
      }

      if(checkbox_status == 'domainlist active'){
        sm_domainid = id;
        sm_domainval = dispname;
      }

      if(checkbox_status == 'statutorynaturelist active'){
        sm_statutorynatureid = id;
        sm_statutorynatureval = dispname;
      }

      if(sm_countryid != '' && sm_domainid !=''){
        loadStatutoryLevels(sm_countryid,sm_domainid);
      }
      if(sm_countryid != ''){
        loadGeographyLevels(sm_countryid);
      }
      make_breadcrumbs();
  }

  //check & uncheck list data for multi selection
  function multiactivate(element, id, dispname, type){
  var chkstatus = $(element).attr('class');
  if(chkstatus == 'industrylist active'){
    $(element).removeClass("active");
        var removeid = sm_industryids.indexOf(id);
        sm_industryids.splice(removeid,1);
        var removename = sm_industryvals.indexOf(dispname);
        sm_industryvals.splice(removename,1);
  }else{
    $(element).addClass("active");
        sm_industryids.push(id);
        sm_industryvals.push(dispname);
  }
    make_breadcrumbs();
}

function make_breadcrumbs(){
    var arrowimage = " <img src=\'/images/right_arrow.png\'/> ";
    $(".breadcrumbs_1").html(sm_countryval + arrowimage + sm_domainval + arrowimage + sm_industryvals + arrowimage + sm_statutorynatureval);
}
//load statutory levels
function loadStatutoryLevels(countryval,domainval){
  $(".tbody-statutory-level").find("div").remove();
  var statutoryLevelList = statutoryLevelsList[countryval][domainval];
  var levelposition;
    for(var j in statutoryLevelList){
      levelposition = statutoryLevelList[j]["level_position"];
      var tableRow=$('#statutory-level-templates');
      var clone=tableRow.clone();
      $('.statutory_title', clone).text(statutoryLevelList[j]["level_name"]);
      $('.statutory_levelvalue', clone).html('<input type="text" class="filter-text-box" id="statutoryfilter'+levelposition+'" onkeyup="filter_statutory('+levelposition+')"> <ul id="statutorylist'+levelposition+'"></ul><div class="bottomfield"><input type="text" class="input-box addleft" placeholder="" id="datavalue'+levelposition+'" onkeypress="saverecord('+levelposition+',event)"/><span> <a href="#" class="addleftbutton" id="update'+levelposition+'"><img src="/images/icon-plus.png" formtarget="_self" onclick="saverecord('+levelposition+',\'clickimage\')" /></a></span></div><input type="hidden" id="statutorylevelid'+levelposition+'" value="'+statutoryLevelList[j]["level_id"]+'"/><input type="hidden" id="level'+levelposition+'" value="'+levelposition+'" />');
      $('.tbody-statutory-level').append(clone);
    }   

    var setlevelstage= 1;
    $('#datavalue'+setlevelstage).val('');
    $('#statutorylist'+setlevelstage).empty();
    var firstlevelid= $('#statutorylevelid'+setlevelstage).val();

    var str='';
    var idval='';
    var clsval='.slist'+setlevelstage;
    var clsval1='slist'+setlevelstage;

    var statutoryList = statutoriesList[countryval][domainval];
    for(var i in statutoryList){
      var setstatutoryid = statutoryList[i]["statutory_id"];
      if(statutoryList[i]["level_id"] == firstlevelid){
      str += '<span class="eslist-filter'+setlevelstage+'" style="float:left;margin-right:5px;margin-left:5px;margin-top:3px;cursor:pointer;" onclick="editstaturoty('+setstatutoryid+',\''+statutoryList[i]["statutory_name"]+'\','+setlevelstage+')"><img src="/images/icon-edit.png" style="width:11px;height:11px"/> </span> <li id="'+setstatutoryid+'" class="'+clsval1+'" onclick="activate_statutorylist(this,'+setstatutoryid+',\''+clsval+'\','+countryval+','+domainval+','+setlevelstage+')" >'+statutoryList[i]["statutory_name"]+'</li> ';
    }
    }
    $('#statutorylist'+setlevelstage).append(str);
}

//check & uncheck list data
function activate_statutorylist(element,id,type,country,domain,level){
  $(type).each( function( index, el ) {
    $(el).removeClass( "active" );
      });
   $(element).addClass("active");
     load(id,level,country,domain);
  }

//load statutory sub level data dynamically
function load(id,level,country,domain){
  var levelstages= parseInt(level) + 1;
  for(var k=levelstages;k<=10;k++){
  var setlevelstage= k;
  if($('#statutoryid').val()==''){
  $('#datavalue'+setlevelstage).val('');
   }
  $('#statutorylist'+setlevelstage).empty();
  var str='';
  var idval='';
  var clsval='.slist'+setlevelstage;
  var clsval1='slist'+setlevelstage;
  var levelid=$('#statutorylevelid'+setlevelstage).val();
  var statutoryList = statutoriesList[country][domain];
  for(var i in statutoryList){
    var setstatutoryid = statutoryList[i]["statutory_id"];
    if( id == statutoryList[i]["parent_id"] && statutoryList[i]["level_id"] == levelid) {
      str += '<span class="eslist-filter'+setlevelstage+'" style="float:left;margin-right:5px;margin-left:5px;margin-top:3px;cursor:pointer;" onclick="editstaturoty('+setstatutoryid+',\''+statutoryList[i]["statutory_name"]+'\','+setlevelstage+')"><img src="/images/icon-edit.png" style="width:11px;height:11px"/></span> <li id="'+setstatutoryid+'" class="'+clsval1+'" onclick="activate_statutorylist(this,'+setstatutoryid+',\''+clsval+'\','+country+','+domain+','+setlevelstage+')" >'+statutoryList[i]["statutory_name"]+'</li> ';
    }
  }
  $('#statutorylist'+setlevelstage).append(str); 
  }
}

//validate and insert records in statutory table
function saverecord(j,e){
  var data = e.keyCode;
  if(data==13 || data ==undefined){
    displayMessage("");
    var levelstage = $('#level'+j).val();
    var statutorylevel_id = $('#statutorylevelid'+j).val();
    var datavalue = $('#datavalue'+j).val();
    var map_statutory_id=[];
    var last_statutory_id=0;
    var last_level = 0;
    for(k=1;k<j;k++){
      $(".slist"+k+".active").each( function( index, el ) {
        map_statutory_id.push(parseInt(el.id));
        last_statutory_id = el.id;
        last_level = k;
        });
    }
    if(map_statutory_id==0 && levelstage>1 ){
      displayMessage("Level Selection Should not be Empty");
    }else if(datavalue==""){
      displayMessage("Level-"+levelstage+" Value Should not be Empty");
    }else{
      if($("#statutoryid").val() == ''){
        function onSuccess(data){
          displayMessage("Record Added Successfully");
          reload(last_statutory_id,last_level,sm_countryid,sm_domainid);
        }
        function onFailure(error){
          displayMessage(error)
        }
        if(map_statutory_id.length == 0){
          map_statutory_id.push(0);
        }
        mirror.saveStatutory(parseInt(statutorylevel_id), datavalue, map_statutory_id, 
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
        function onSuccessUpdate(data){
          displayMessage("Record Updated Successfully");
          reload(last_statutory_id,last_level,sm_countryid,sm_domainid);
        }
        function onFailureUpdate(error){
          onFailure(error);
        }
        if(map_statutory_id.length == 0){
          map_statutory_id.push(0);
        }
        mirror.updateStatutory(parseInt($("#statutoryid").val()), parseInt(statutorylevel_id), datavalue, map_statutory_id,
        function (error, response) {
          if (error == null){
            onSuccessUpdate(response);
          }
          else {
            onFailureUpdate(error);
          }
        }
        );
        $("#statutoryid").val('');
        $('#datavalue'+j).val('');
      }    
    }
  }
}

function reload(last_statutory_id,last_level,country,domain){
  function success(status,data){
    statutoriesList = data["statutories"];
    load(last_statutory_id,last_level,country,domain)
  }
  function failure(data){
  }
  mirror.getStatutoryMappings(success, failure);
}

function filter_statutory(position){  
  var slist_filter = document.getElementsByClassName('slist'+position);
  var eslist_filter = document.getElementsByClassName('eslist-filter'+position);
  var filter = $('#statutoryfilter'+position).val().toLowerCase();
  for (var i = 0; i < slist_filter.length; i++) {
    name = slist_filter[i].innerHTML.trim();
    if (name.toLowerCase().indexOf(filter) == 0) {
        slist_filter[i].style.display = 'list-item';
        eslist_filter[i].style.display = 'list-item';
    } else {
        slist_filter[i].style.display = 'none';
        eslist_filter[i].style.display = 'none';
    }
  }
}

function editstaturoty(statu_id, statu_name, position){
  $("#statutoryid").val(statu_id);
  $('#datavalue'+position).val(statu_name)
}

function load_statories(){
  disp_statutories = [];
  $(".tbody-statutory-list").find("tr").remove();
  for(var i=0; i<sm_statutoryids.length; i++) {
    var dispstatutory = '';
    var statutoryList = statutoriesList[sm_countryid][sm_domainid];
    for(var statutory in statutoryList){
      if(statutoryList[statutory]["statutory_id"] == sm_statutoryids[i]){
          dispstatutory = statutoryList[statutory]["parent_mappings"];
          disp_statutories.push(dispstatutory);
      }
    }
    var tableRow=$('#statutory-templates .table-statutory .table-row');
    var clone=tableRow.clone();
    $('.sno', clone).text(i+1);
    $('.statutory', clone).html(dispstatutory.replace(/>>/gi,' <img src=\'/images/right_arrow.png\'/> '));
    $('.remove', clone).html('<img src=\'/images/icon-delete.png\' onclick="temp_removestatutories(\''+sm_statutoryids[i]+'\')"/>');
    $('.tbody-statutory-list').append(clone);
}
make_breadcrumbs2();
}

$("#temp_addstatutories").click(function() {
  var last_statutory_id=0;
  for(k=1;k<=10;k++){
    $(".slist"+k+".active").each( function( index, el ) {
      last_statutory_id = el.id;
      });
  }
  if(last_statutory_id==0){
    displayMessage("No Statutory is selected");
  }else if($.inArray(last_statutory_id, sm_statutoryids) >= 0){
    displayMessage("This Statutory already added");
  }else{
    sm_statutoryids.push(parseInt(last_statutory_id));
  }
  load_statories();    
});

function temp_removestatutories(remove_id){
  remove = sm_statutoryids.indexOf(remove_id)
  sm_statutoryids.splice(remove,1);
  load_statories();
}

$("#temp_addcompliance").click(function() {
  var comp_id=$('#complianceid').val();
  var statutory_provision = $('#statutory_provision').val().trim();
  var compliance_task = $('#compliance_task').val().trim();
  var description = $('#compliance_description').val().trim();
  var compliance_document = $('#compliance_document').val().trim();
  var file_format = null;
  //file_format = $('#upload_file').val()
  var penal_consequences = $('#penal_consequences').val().trim();
  var compliance_frequency = $('#compliance_frequency').val().trim();
  var repeats_type = null;
  var repeats_every = null;
  var duration = null;
  var duration_type= null;
  var statutory_date = null;
  var statutory_month = null;
  var trigger_before_days = null;
  var is_active = true;
  statutory_dates = [];

  if(statutory_provision.length == 0){
    displayMessage("Statutory Provision Required");
  }else if (compliance_task.length == 0){
    displayMessage("Compliance Task Required");
  }else if (description.length == 0){
    displayMessage("Compliance Description Required");
  }else if (compliance_frequency.length == 0){
    displayMessage("Compliance Frequency Required");
  }else if ((compliance_frequency == "2" || compliance_frequency == "3") && $('#repeats_type').val()==''){
     displayMessage("Repeats Type Required");
  }else if ((compliance_frequency == "2" || compliance_frequency == "3") && $('#repeats_every').val()==''){
     displayMessage("Repeats Every Required");
  }else{
    displayMessage("");
    if(compliance_frequency == "1"){
      if($('#statutory_date').val() != '' && $('#statutory_month').val() != ''){
        statutory_date = parseInt($('#statutory_date').val());
        statutory_month = parseInt($('#statutory_month').val());
      }
      
      if($('#triggerbefore').val().trim().length > 0)
        trigger_before_days = parseInt($('#triggerbefore').val());

      statutory_date = mirror.statutoryDates(statutory_date, statutory_month, trigger_before_days);
      statutory_dates.push(statutory_date);
      }else if (compliance_frequency == "2" || compliance_frequency == "3"){
        repeats_type = parseInt($('#repeats_type').val());
        repeats_every = parseInt($('#repeats_every').val());
        if(repeats_type == '2' && $('.multipleinput').prop("checked") == true){
          for(var i=1;i<=6;i++){
            if($('#multiple_statutory_month'+i).val() != ""){

            if($('#multiple_statutory_date'+i).val() != '' && $('#multiple_statutory_month'+i).val() != ''){
              statutory_date = parseInt($('#multiple_statutory_date'+i).val());
              statutory_month = parseInt($('#multiple_statutory_month'+i).val());
            }
            
            if($('#multiple_triggerbefore'+i).val().trim().length > 0)
            trigger_before_days = parseInt($('#multiple_triggerbefore'+i).val());

            statutory_date = mirror.statutoryDates(statutory_date, statutory_month, trigger_before_days);
            statutory_dates.push(statutory_date);
        }
      }
    }else{
      if($('#single_statutory_date').val() != '' && $('#single_statutory_month').val() != ''){
        statutory_date = parseInt($('#single_statutory_date').val());
        statutory_month = parseInt($('#single_statutory_month').val());
      }
      
      if($('#single_triggerbefore').val().trim().length > 0)
        trigger_before_days = parseInt($('#single_triggerbefore').val());

      statutory_date = mirror.statutoryDates(statutory_date, statutory_month, trigger_before_days);
      statutory_dates.push(statutory_date);
    }
  }else{
    duration = parseInt($('#duration').val());
    duration_type = parseInt($('#duration_type').val());
  }
  var check_duplicate_status= true;
  $.each(compliances, function(index, value) {
  if (((value.statutory_provision == statutory_provision) || (value.compliance_task == compliance_task) || (value.document_name == compliance_document)) &&  comp_id == '') {
      check_duplicate_status = false;
  }
  });

  if(check_duplicate_status){
  if(comp_id == ''){         
    compliance = mirror.complianceDetails(statutory_provision, compliance_task, description, compliance_document, file_format, penal_consequences, parseInt(compliance_frequency),
      statutory_dates, repeats_type, repeats_every, duration_type, duration, is_active, comp_id);
    compliances.push(compliance);
  }else{
    compliances[comp_id]["statutory_provision"] = statutory_provision;
    compliances[comp_id]["compliance_task"] = compliance_task;
    compliances[comp_id]["description"] = description;
    compliances[comp_id]["document_name"] = compliance_document;
    compliances[comp_id]["format_file_list"] = file_format;
    compliances[comp_id]["penal_consequences"] = penal_consequences;
    compliances[comp_id]["frequency_id"] = parseInt(compliance_frequency);
    compliances[comp_id]["statutory_dates"] = statutory_dates;
    compliances[comp_id]["repeats_type_id"] = repeats_type;
    compliances[comp_id]["repeats_every"] = repeats_every;
    compliances[comp_id]["duration_type_id"] = duration_type;
    compliances[comp_id]["duration"] = duration;
    compliances[comp_id]["is_active"] = true;
  }
  $('#statutory_provision').val('');
  $('#compliance_task').val('');
  $('#compliance_description').val('');
  $('#compliance_frequency').val('');
  $('#compliance_document').val('');
  $('#upload_file').val('');
  $('#penal_consequences').val('');
  $('#Recurring').hide();
  $('#Occasional').hide();
  $('#One_Time').hide();
  $('#repeats_every').val('');
  $('#repeats_type').val('');
  $('#duration').val('');
  $('#statutory_date').val('');
  $('#single_statutory_date').val('');
  $('#multiple_statutory_date1').val('');
  $('#multiple_statutory_date2').val('');
  $('#multiple_statutory_date3').val('');
  $('#multiple_statutory_date4').val('');
  $('#multiple_statutory_date5').val('');
  $('#multiple_statutory_date6').val('');
  $('#statutory_month').val('');
  $('#single_statutory_month').val('');
  $('#multiple_statutory_month1').val('');
  $('#multiple_statutory_month2').val('');
  $('#multiple_statutory_month3').val('');
  $('#multiple_statutory_month4').val('');
  $('#multiple_statutory_month5').val('');
  $('#multiple_statutory_month6').val('');
  $('#triggerbefore').val('');
  $('#single_triggerbefore').val('');
  $('#multiple_triggerbefore1').val('');
  $('#multiple_triggerbefore2').val('');
  $('#multiple_triggerbefore3').val('');
  $('#multiple_triggerbefore4').val('');
  $('#multiple_triggerbefore5').val('');
  $('#multiple_triggerbefore6').val('');
  //$('.multipleinput').prop("checked") == false;
  $('#complianceid').val('');
  load_compliance();
  }else{
    displayMessage("Duplicate Compliance");
  }
  }     
});

function load_compliance(){
  $(".tbody-compliance-list").find("tr").remove();
  complianceid = 0;
  for(var entity in compliances) {
    var display_repeats = 'Nil';
    var edit_compliance_id = compliances[entity]["compliance_id"];
    var passStatus = '';
    var isActive = compliances[entity]["is_active"];
    var display_image = '';
    var complianceFrequency=null;
    if(compliances[entity]["repeats_every"] != null && compliances[entity]["repeats_type"] != null){
      display_repeats = compliances[entity]["repeats_every"] + " " + compliances[entity]["repeats_type"];
    }

    for (var compliancefrequency in complianceFrequencyList) {
      if(complianceFrequencyList[compliancefrequency]["frequency_id"] == compliances[entity]["frequency_id"]){
        complianceFrequency = complianceFrequencyList[compliancefrequency]["frequency"];
      }
    }

    var tableRow=$('#compliance-templates .table-compliance .table-row');
    var clone=tableRow.clone();
    $('.sno', clone).text(complianceid+1);
    $('.statutory-provision', clone).text(compliances[entity]["statutory_provision"]);
    $('.task', clone).text(compliances[entity]["compliance_task"]);
    $('.description', clone).text(compliances[entity]["description"]);
    $('.frequency', clone).text(complianceFrequency);
    $('.repeats', clone).text(display_repeats);
    $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="temp_editcompliance(\''+complianceid+'\')"/>');
     
    if(edit_compliance_id != null){
      if(isActive == 1) {
        display_image="icon-active.png"
        passStatus = "0";
      }
      else {
        display_image="icon-inactive.png";
        passStatus = "1";
       }
      $('.status', clone).html('<img src=\'/images/'+display_image+'\' onclick="temp_change_status_compliance(\''+complianceid+'\','+passStatus+')"/>');
    }else{
      $('.status', clone).html('<img src=\'/images/icon-delete.png\' onclick="temp_removecompliance(\''+complianceid+'\')"/>');
    }
    
    $('.tbody-compliance-list').append(clone);

    complianceid = complianceid + 1;
}
make_breadcrumbs3();
}

function temp_editcompliance(edit_id){
  $('#statutory_provision').val(compliances[edit_id]["statutory_provision"]);
  $('#compliance_task').val(compliances[edit_id]["compliance_task"]);
  $('#compliance_description').val(compliances[edit_id]["description"]);
  $('#compliance_frequency').val(compliances[edit_id]["frequency_id"]);
  $('#compliance_document').val(compliances[edit_id]["document_name"]);
  $('#upload_file').val(compliances[edit_id]["format_file_list"]);
  $('#penal_consequences').val(compliances[edit_id]["penal_consequences"]);
  $('#duration_type').val(compliances[edit_id]["duration_type_id"]);
  $('#duration').val(compliances[edit_id]["duration"]);
  $('#repeats_type').val(compliances[edit_id]["repeats_type_id"]);
  $('#repeats_every').val(compliances[edit_id]["repeats_every"]);
  var compliance_frequency = compliances[edit_id]["frequency_id"];
  statutory_dates = compliances[edit_id]["statutory_dates"];
  if(compliance_frequency == "1"){
    $('#statutory_date').val(statutory_dates[0]["statutory_date"]);
    $('#statutory_month').val(statutory_dates[0]["statutory_month"]);
    $('#triggerbefore').val(statutory_dates[0]["trigger_before_days"]);
    $('#Recurring').hide();
    $('#Occasional').hide();
    $('#One_Time').show();
  }else if (compliance_frequency == "2" || compliance_frequency == "3"){
    $('#Recurring').show();
    $('#Occasional').hide();
    $('#One_Time').hide();
    if(statutory_dates.length > 1){
      $('.multipleinput').prop("checked") == true;
      $('.multipleselectnone').hide();
      $('.multipleselect').show();
      load_stautorydates();
      for(var i=1;i<=statutory_dates.length;i++){
      $('#multiple_statutory_date'+i).val(statutory_dates[i-1]["statutory_date"]);
      $('#multiple_statutory_month'+i).val(statutory_dates[i-1]["statutory_month"]);
      $('#multiple_triggerbefore'+i).val(statutory_dates[i-1]["trigger_before_days"]);
      }
      for(var i=statutory_dates+1;i<=6;i++){
      $('#multiple_statutory_date'+i).val('');
      $('#multiple_statutory_month'+i).val('');
      $('#multiple_triggerbefore'+i).val('');
      }
  }else{
    $('.multipleinput').prop("checked") == false;
    $('.multipleselectnone').show();
    $('.multipleselect').hide();
    if(statutory_dates.length > 0){
    $('#single_statutory_date').val(statutory_dates[0]["statutory_date"]);
    $('#single_statutory_month').val(statutory_dates[0]["statutory_month"]);
    $('#single_triggerbefore').val(statutory_dates[0]["trigger_before_days"]);
    }
  }
}else{
  $('#Recurring').hide();
  $('#Occasional').show();
  $('#One_Time').hide();
  }
  $('#complianceid').val(edit_id);
}

function temp_removecompliance(remove_id){
  compliances.splice(remove_id,1);
  load_compliance();
}

function temp_change_status_compliance(edit_id, passStatus){
   compliances[edit_id]["is_active"] = passStatus;
   load_compliance();
}
function make_breadcrumbs2(){
  var arrowimage = " <img src=\'/images/right_arrow.png\'/> ";
  var statutories_name = '';
  for(var i=0;i<disp_statutories.length;i++){
      statutories_name = statutories_name + disp_statutories[i].replace(/>>/gi,' <img src=\'/images/right_arrow.png\'/> ') + ',';
  }
  statutories_name = statutories_name.replace(/,\s*$/, "");
  $(".breadcrumbs_2").html(statutories_name);
}

function make_breadcrumbs3(){
    var compliance_name = '';
    for(var entity in compliances) {
        compliance_name = compliance_name + compliances[entity]["document"] +" - " + compliances[entity]["statutory_provision"] + ',';
    }
    compliance_name = compliance_name.replace(/,\s*$/, "");
    $(".breadcrumbs_3").html(compliance_name);
}

function loadGeographyLevels(sm_countryid){
  $(".tbody-geography-level").find("div").remove();
  var geographyLevelList = geographyLevelsList[sm_countryid];
  var levelposition;
  for(var j in geographyLevelList){
    levelposition = geographyLevelList[j]["level_position"];
    var tableRow=$('#geography-level-templates');
    var clone=tableRow.clone();
    $('.title', clone).text(geographyLevelList[j]["level_name"]);
    $('.levelvalue', clone).html('<input type="text" class="filter-text-box" id="filter_geography'+levelposition+'" onkeyup="filter_geography('+levelposition+')"> <ul id="ulist'+levelposition+'"></ul><input type="hidden" id="glmid'+levelposition+'" value="'+geographyLevelList[j]["level_id"]+'"/><input type="hidden" id="level'+levelposition+'" value="'+levelposition+'" />');
    $('.tbody-geography-level').append(clone);
  }    
  var setlevelstage= 1;
  $('#datavalue'+setlevelstage).val('');
  $('#ulist'+setlevelstage).empty();
  var firstlevelid= $('#glmid'+setlevelstage).val();
  var idval='';
  var clsval='.list'+setlevelstage;
  var clsval1='list'+setlevelstage;
  var str='<li id="select'+setlevelstage+'" class="'+clsval1+'" onclick="activate_geography_all(this,'+sm_countryid+','+setlevelstage+')" > Select All</li>';
  var geographyList = geographiesList[sm_countryid];
  for(var i in geographyList){
    var setgeographyid = geographyList[i]["geography_id"];
    var setparentid = geographyList[i]["parent_id"];
    var combineid = setgeographyid + "-" + setparentid;
    if((geographyList[i]["level_id"] == firstlevelid) && (geographyList[i]["is_active"] == true)){
    str += '<li id="'+combineid+'" value="'+setparentid+'" class="'+clsval1+'" onclick="activate_geography(this,'+sm_countryid+','+setlevelstage+',\''+combineid+'\')" >'+geographyList[i]["geography_name"]+'</li>';
  }
  }
  $('#ulist'+setlevelstage).append(str); 
}

//check & uncheck list data
function activate_geography(element,country,level,combineid){
  var chkstatus = $(element).attr('class');
  var displaytext = $(element).text();
  if(chkstatus == 'list'+level+' active'){
      $(element).removeClass("active");
      load_geography(level,country,combineid,"remove",displaytext);
  }else{
      $(element).addClass("active");
      load_geography(level,country,combineid,"add",displaytext);
  } 
}

//select all geography level data
function activate_geography_all(element,country,level){
  var chkstatus = $(element).attr('class');
  if(chkstatus == 'list'+level+' active'){
  $('.list'+level+".active").each( function( index, el ) {
  $(el).removeClass( "active" );
    });
  }else{
      $('.list'+level).each( function( index, el ) {
          $(el).addClass( "active" );
      });
  } 
  load_geography_all(level,country); 
}

//load geographymapping sub level data dynamically
function load_geography(level,country,combineids,status,displaytext){
  var geographyids=[];
  displayMessage("");
  var split_id = combineids.split('-');
  var previous_primary_id= split_id[1];
  geographyids.push([parseInt(split_id[0]),displaytext]);
  
  var levelstages= parseInt(level) + 1;
  for(var k=levelstages;k<=10;k++){
    var setlevelstage= k;
    $('#select'+setlevelstage).remove();
    if($('#geographyid').val()==''){
        $('#datavalue'+setlevelstage).val('');
    }
    var splittext = '';
    var idval='';
    var clsval='.list'+setlevelstage;
    var clsval1='list'+setlevelstage;
    var str='';
    var sel_all='<li id="select'+setlevelstage+'" class="'+clsval1+'" onclick="activate_geography_all(this,'+sm_countryid+','+setlevelstage+')" > Select All</li>';
    var levelid=$('#glmid'+setlevelstage).val();
    var geographyList = geographiesList[country];
    $("#ulist"+setlevelstage).children("li").each(function()
    {
      if($(this).val() == previous_primary_id){
        $(this).remove();
        $('.split'+previous_primary_id+setlevelstage).remove();
      }
    });

    for(var j=0;j<geographyids.length;j++){
      splittext = '';
      for(var i in geographyList){
        var setgeographyid = geographyList[i]["geography_id"];
        var setparentid = geographyList[i]["parent_id"];
        var combineid = setgeographyid + "-" + setparentid;
        if( geographyList[i]["parent_id"] == geographyids[j][0] && geographyList[i]["level_id"] == levelid && geographyList[i]["is_active"] == true) {
         if(status == 'add'){
          if(splittext != '') {
          str += '<li id="'+combineid+'" value="'+setparentid+'" class="'+clsval1+'" onclick="activate_geography(this,'+country+','+setlevelstage+',\''+combineid+'\')" > '+geographyList[i]["geography_name"]+'</li>';
          }else{
          splittext = '<h3 class="split'+setparentid+setlevelstage+'" style="background-color:gray;padding:2px;font-size:13px;color:white;">'+geographyids[j][1]+'</h3>';
          str += splittext + '<li id="'+combineid+'" value="'+setparentid+'" class="'+clsval1+'" onclick="activate_geography(this,'+country+','+setlevelstage+',\''+combineid+'\')" >'+geographyList[i]["geography_name"]+'</li>';
          }
        }
        else{
          if($('#'+combineid).attr('class') == 'list'+setlevelstage+' active'){
            displayMessage("Remove Child First");
            $('#'+combineids).addClass( "active" );
          }else{
            $('#'+combineid).remove();
            $('.split'+setparentid+setlevelstage).remove();
          }
        }
      }
    }
  } 
  $('#ulist'+setlevelstage).append(str);
  if($('#ulist'+setlevelstage+" li").length > 0){
    $('#ulist'+setlevelstage).prepend(sel_all);
  }
  }
}

//load geographymapping sub level data dynamically
function load_geography_all(level,country){
  var geographyids=[];
  $(".list"+level+".active").each( function( index, el ) {
      var split_id = el.id.split('-');
      geographyids.push([parseInt(split_id[0]),el.innerHTML]);
  });
  
  var levelstages= parseInt(level) + 1;
  for(var k=levelstages;k<=10;k++){
    var setlevelstage= k;
    if($('#geographyid').val()==''){
        $('#datavalue'+setlevelstage).val('');
    }
    $('#ulist'+setlevelstage).empty();
    var splittext = '';
    var idval='';
    var clsval='.list'+setlevelstage;
    var clsval1='list'+setlevelstage;
    var str='';
    var sel_all='<li id="selectall'+setlevelstage+'" class="'+clsval1+'" onclick="activate_geography_all(this,'+sm_countryid+','+setlevelstage+')" > Select All</li>';
    var levelid=$('#glmid'+setlevelstage).val();
    var geographyList = geographiesList[country];

    //working order is even for multiple selection
    for(var j=0;j<geographyids.length;j++){
      splittext = '';
      for(var i in geographyList){
        var setgeographyid = geographyList[i]["geography_id"];
        var setparentid = geographyList[i]["parent_id"];
        var combineid = setgeographyid + "-" + setparentid;

        if( geographyList[i]["parent_id"] == geographyids[j][0] && geographyList[i]["level_id"] == levelid && geographyList[i]["is_active"] == true) {
          str += sel_all;
         if(splittext != '') {
          str += '<li id="'+combineid+'" class="'+clsval1+'" onclick="activate_geography(this,'+country+','+setlevelstage+')" > '+geographyList[i]["geography_name"]+'</li>';
         }else{
          splittext = '<h3 style="background-color:gray;padding:2px;font-size:13px;color:white;">'+geographyids[j][1]+'</h3>';
          str += splittext + '<li id="'+combineid+'" class="'+clsval1+'" onclick="activate_geography(this,'+country+','+setlevelstage+')" >'+geographyList[i]["geography_name"]+'</li>';
         }
         sel_all = '';
      }
      }
   }
    //working but order is not even for multiple selection
    /*for(var i in geographyList){
      var setgeographyid = geographyList[i]["geography_id"];
      var checkstate = $.inArray(geographyList[i]["parent_id"], geographyids);
      if( checkstate >= 0 && geographyList[i]["level_id"] == levelid && geographyList[i]["is_active"] == 1) {
      str += '<a href="#"> <span class="glist-filter'+setlevelstage+'"> <li id="'+setgeographyid+'" class="'+clsval1+'" onclick="activate_geography(this,'+country+','+setlevelstage+')" > '+geographyList[i]["geography_name"]+'</li></span> </a>';
    }
    }*/
    $('#ulist'+setlevelstage).append(str); 
  }
}

function getGeographyResult(){
  sm_geographyids=[];
  for(k=1;k<=10;k++){
    $(".list"+k+".active").each( function( index, el ) {
      var split_id = el.id.split('-');
      var g_id = parseInt(split_id[0]);
      var p_id = parseInt(split_id[1]);
      sm_geographyids.push(g_id);
      if($.inArray(p_id, sm_geographyids) >= 0){
          var remove_geography = sm_geographyids.indexOf(p_id);
          sm_geographyids.splice(remove_geography,1);
      }
    });
  }   
}

function filter_geography(position){  
  var glist_filter = document.getElementsByClassName('list'+position);
  var filter = $('#filter_geography'+position).val().toLowerCase();
  for (var i = 0; i < glist_filter.length; i++) {
      name = glist_filter[i].innerHTML.trim();
      if (name.toLowerCase().indexOf(filter) == 0) {
          glist_filter[i].style.display = 'list-item';
      } else {
          glist_filter[i].style.display = 'none';
      }
  }
}

function savestatutorymapping(){
  function onSuccess(data){
      getStatutoryMappings();
      //displayMessage("Record Added Successfully");
      $("#statutorymapping-add").hide();
      $('ul.setup-panel li:eq(0)').addClass('active');
      $('ul.setup-panel li:eq(1)').addClass('disabled');
      $('ul.setup-panel li:eq(2)').addClass('disabled');
      $('ul.setup-panel li:eq(3)').addClass('disabled');
      $('ul.setup-panel li a[href="#step-1"]').trigger('click')
      $("#statutorymapping-view").show();
  }
  function onFailure(error){

  }
  var sm_id = null;
  if($("#edit_sm_id").val().length > 0){
    sm_id = parseInt($("#edit_sm_id").val());
  }
  
  if(sm_id == null){
    statutorymappingData = mirror.statutoryMapping(sm_countryid,sm_domainid,sm_industryids,sm_statutorynatureid,sm_statutoryids,compliances,sm_geographyids, sm_id);
    mirror.saveStatutoryMapping(statutorymappingData,
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
    statutorymappingData = mirror.UpdateStatutoryMappingData(sm_industryids,sm_statutorynatureid,sm_statutoryids,compliances,sm_geographyids, sm_id)
    mirror.updateStatutoryMapping(statutorymappingData, 
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

function validate_firsttab(){
  if(sm_countryid == ''){
    displayMessage("Country Required");
  }else if (sm_domainid == ''){
    displayMessage("Domain Required");
  }else if (sm_industryids.length == 0){
    displayMessage("Industry Required");
  }else if (sm_statutorynatureid == ''){
    displayMessage("Statutory Nature Required");
  }else{
    displayMessage("");
    return true;
  }
}
function validate_secondtab(){
  if (sm_statutoryids.length == 0){
    displayMessage("Atleast one Staturory should be selected");
  }else{
    displayMessage("");
    return true;
  }
}
function validate_thirdtab(){
  if (compliances.length == 0){
    displayMessage("Atleast one Compliance should be selected");
  }else{
    displayMessage("");
    return true;
  }
}
function validate_fourthtab(){
  if (sm_geographyids.length == 0){
    displayMessage("Atleast one Location should be selected");
  }else{
    displayMessage("");
    return true;
  }
}

function load_edit_selectdomain_master(sm_countryid,sm_domainid,sm_industryids,sm_statutorynatureid){
  //load country details
  var clsval='.countrylist';
  var clsval1='countrylist';
  var str='';
  $('#country').empty();
    for(var country in countriesList){
      var countryid = countriesList[country]["country_id"];
      var dispcountryname = countriesList[country]["country_name"];
      if(countriesList[country]["is_active"] == true){
        if(sm_countryid == countryid){
          str += '<li id="'+countryid+'" class="'+clsval1+' active"><span class="filter1_name">'+dispcountryname+'</span></li>';
        }else{
          str += '<li id="'+countryid+'" class="'+clsval1+'"><span class="filter1_name">'+dispcountryname+'</span></li>';
        }
      }
    }
    $('#country').append(str); 

    //load domain details
    var clsval='.domainlist';
    var clsval1='domainlist';
    var str='';
    $('#domain').empty();
    for(var domain in domainsList){
      var domainid = domainsList[domain]["domain_id"];
      var dispdomainname = domainsList[domain]["domain_name"];
      if(domainsList[domain]["is_active"] == true){
        if(sm_domainid == domainid){
            str += '<li id="'+domainid+'" class="'+clsval1+' active" ><span class="filter2_name">'+dispdomainname+'</span></li>';
          }else{
            str += '<li id="'+domainid+'" class="'+clsval1+'" ><span class="filter2_name">'+dispdomainname+'</span></li>';
          }
        }
      }
      $('#domain').append(str);
      //load industry details
      var clsval='.industrylist';
      var clsval1='industrylist';
      var str='';
      $('#industry').empty();
      for(var industry in industriesList){
        var industryid = industriesList[industry]["industry_id"];
        var dispindustryname = industriesList[industry]["industry_name"];
        if(industriesList[industry]["is_active"] == true){
          if($.inArray(industryid, sm_industryids) >= 0){
              str += '<li id="'+industryid+'" class="'+clsval1+' active" onclick="multiactivate(this,'+industryid+',\''+dispindustryname+'\',\''+clsval+'\')" ><span class="filter3_name">'+dispindustryname+'</span></li>';
            }else{
              str += '<li id="'+industryid+'" class="'+clsval1+'" onclick="multiactivate(this,'+industryid+',\''+dispindustryname+'\',\''+clsval+'\')" ><span class="filter3_name">'+dispindustryname+'</span></li>';
            }
          }
        }
        $('#industry').append(str);
        //load statutorynature details
        var clsval='.statutorynaturelist';
        var clsval1='statutorynaturelist';
        var str='';
        $('#statutorynature').empty();
        for(var statutorynature in statutoryNaturesList){
          var statutorynatureid = statutoryNaturesList[statutorynature]["statutory_nature_id"];
          var dispstatutoryname = statutoryNaturesList[statutorynature]["statutory_nature_name"];
          if(statutoryNaturesList[statutorynature]["is_active"] == true){
            if(statutorynatureid == sm_statutorynatureid){
                str += '<li id="'+statutorynatureid+'" class="'+clsval1+' active" onclick="activate(this,'+statutorynatureid+',\''+dispstatutoryname+'\',\''+clsval+'\')" ><span class="filter4_name">'+dispstatutoryname+'</span></li>';
              }else{
                str += '<li id="'+statutorynatureid+'" class="'+clsval1+'" onclick="activate(this,'+statutorynatureid+',\''+dispstatutoryname+'\',\''+clsval+'\')" ><span class="filter4_name">'+dispstatutoryname+'</span></li>';
              }
            }
          }
          $('#statutorynature').append(str);

        if(sm_countryid != '' && sm_domainid !=''){
            loadStatutoryLevels(sm_countryid,sm_domainid);
          }
        if(sm_countryid != ''){
          loadGeographyLevels(sm_countryid);
        }
        make_breadcrumbs();

    //load compliance frequency selectbox
    for (var compliancefrequency in complianceFrequencyList) {
    var option = $("<option></option>");
    option.val(complianceFrequencyList[compliancefrequency]["frequency_id"]);
    option.text(complianceFrequencyList[compliancefrequency]["frequency"]);
    $("#compliance_frequency").append(option);
    }

    //load compliance duration type selectbox
    for (var compliancedurationtype in complianceDurationTypeList) {
    var option = $("<option></option>");
    option.val(complianceDurationTypeList[compliancedurationtype]["duration_type_id"]);
    option.text(complianceDurationTypeList[compliancedurationtype]["duration_type"]);
    $("#duration_type").append(option);
    }

    //load compliance repeat type selectbox
    for (var compliancerepeattype in complianceRepeatTypeList) {
    var option = $("<option></option>");
    option.val(complianceRepeatTypeList[compliancerepeattype]["repeat_type_id"]);
    option.text(complianceRepeatTypeList[compliancerepeattype]["repeat_type"]);
    $("#repeats_type").append(option);
    }
  }
function displayEdit (sm_Id) {
  displayMessage("");
  $("#statutorymapping-view").hide();
  $("#statutorymapping-add").show();
  $("#edit_sm_id").val(sm_Id);
  sm_countryid = statutoryMappingsList[sm_Id]["country_id"];
  sm_countryval = statutoryMappingsList[sm_Id]["country_name"];
  sm_domainid = statutoryMappingsList[sm_Id]["domain_id"];
  sm_domainval = statutoryMappingsList[sm_Id]["domain_name"];
  sm_industryids = statutoryMappingsList[sm_Id]["industry_ids"]; 
  sm_industryvals = statutoryMappingsList[sm_Id]["industry_names"].split(","); 
  sm_statutorynatureid = statutoryMappingsList[sm_Id]["statutory_nature_id"];
  sm_statutorynatureval = statutoryMappingsList[sm_Id]["statutory_nature_name"];
  sm_statutoryids = statutoryMappingsList[sm_Id]["statutory_ids"];
  compliances = statutoryMappingsList[sm_Id]["compliances"];
  sm_geographyids = statutoryMappingsList[sm_Id]["geography_ids"];
  load_edit_selectdomain_master(sm_countryid,sm_domainid,sm_industryids,sm_statutorynatureid);
  load_statories();
  load_compliance();
  edit_geography(sm_countryid,sm_geographyids);
}

//edit geographymapping data dynamically
function edit_geography(country,geographyids_edit){
  var geographyids=geographyids_edit;
  for(var i=0; i<geographyids.length;i++){
    var geographyList = geographiesList[country];
    for(glist in geographyList){
      if(geographyids[i] == geographyList[glist]["geography_id"]){
        var parentids = geographyList[glist]["parent_ids"];
        var level = geographyList[glist]["level_position"];
      }
    }
    for(var j=0; j<parentids.length; j++){
      var geo_id = parentids[j];;
      var parent_id = 0;
      if(j!=0){
        parent_id = parentids[j-1];
      }
      for(glist in geographyList){
        if(geo_id == geographyList[glist]["geography_id"]){
        var level_id = geographyList[glist]["level_id"];
        var displaytext = geographyList[glist]["geography_name"];
      }
    }
    var combineid = geo_id + "-" + parent_id;
    var displaytext = displaytext;
    var geographyLevelList = geographyLevelsList[country];
    for(glevel in geographyLevelList){
      if(level_id == geographyLevelList[glevel]["level_id"]){
        var levelposition = geographyLevelList[glevel]["level_position"];
      }
    }
    $('#'+combineid).addClass( "active" );
    load_geography(levelposition,country,combineid,"add",displaytext);
  }
  var finalcombineid = geographyids[i]+"-"+geo_id;
  $('#'+finalcombineid).addClass( "active" );
  }
}

function load_stautorydates(){
  var rep_every = parseInt($('#repeats_every').val());
  if(rep_every == 1 || rep_every == 12){
    $('.input-row1').show();
    $('.input-row2').hide();
    $('.input-row3').hide();
    $('.input-row4').hide();
    $('.input-row5').hide();
    $('.input-row6').hide();
  }else if (rep_every == 2){
    $('.input-row1').show();
    $('.input-row2').show();
    $('.input-row3').show();
    $('.input-row4').show();
    $('.input-row5').show();
    $('.input-row6').show();
  }else if (rep_every == 3){
    $('.input-row1').show();
    $('.input-row2').show();
    $('.input-row3').show();
    $('.input-row4').show();
    $('.input-row5').hide();
    $('.input-row6').hide();
  }else if (rep_every == 4){
    $('.input-row1').show();
    $('.input-row2').show();
    $('.input-row3').show();
    $('.input-row4').hide();
    $('.input-row5').hide();
    $('.input-row6').hide();
  }else if (rep_every == 5){
    $('.input-row1').show();
    $('.input-row2').show();
    $('.input-row3').show();
    $('.input-row4').hide();
    $('.input-row5').hide();
    $('.input-row6').hide();
  }else{
    $('.input-row1').show();
    $('.input-row2').show();
    $('.input-row3').hide();
    $('.input-row4').hide();
    $('.input-row5').hide();
    $('.input-row6').hide();
  }
}

$(function()
{
  $('#compliance_description').keyup(function(e)
  {
  var maxLength = 500;
  var textlength = this.value.length;
  if (textlength >= maxLength)
  {
  $('#counter').html('You cannot write more then ' + maxLength + ' characters!');
  this.value = this.value.substring(0, maxLength);
  e.preventDefault();
  }
  else
  {
  $('#counter').html((maxLength - textlength) + ' characters left.');
  }
  });
  $('#duration').keyup(function()
  {
  $("#summary").html("To Complete within " + $('#duration').val() + " " + $('#duration_type option:selected').text() );
  });
  $('#duration_type').change(function()
  {
  $("#summary").html("To Complete within " + $('#duration').val() + " " + $('#duration_type option:selected').text() );
  });
  $('#repeats_every').change(function()
  {
  $(".summary_repeat").html("Every " + $('#repeats_every').val() + " " + $('#repeats_type option:selected').text());
  });
  $('#repeats_type').change(function()
  {
  $(".summary_repeat").html("Every " + $('#repeats_every').val() + " " + $('#repeats_type option:selected').text());
  });
});

$(document).ready(function(){ 
  getStatutoryMappings();
  //start -filter process in select domain tab
  $("#filter_country").keyup( function() {
    var filter = $("#filter_country").val().toLowerCase();
    var lis = document.getElementsByClassName('countrylist');
    for (var i = 0; i < lis.length; i++) {
        var name = lis[i].getElementsByClassName('filter1_name')[0].innerHTML;
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
        var name = lis[i].getElementsByClassName('filter2_name')[0].innerHTML;
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
        var name = lis[i].getElementsByClassName('filter3_name')[0].innerHTML;
        if (name.toLowerCase().indexOf(filter) == 0) 
            lis[i].style.display = 'list-item';
        else
            lis[i].style.display = 'none';
    }
    });

    $("#filter_statutorynature").keyup( function() {
    var filter = $("#filter_statutorynature").val().toLowerCase();
    var lis = document.getElementsByClassName('statutorynaturelist');
    for (var i = 0; i < lis.length; i++) {
        var name = lis[i].getElementsByClassName('filter4_name')[0].innerHTML;
        if (name.toLowerCase().indexOf(filter) == 0) 
            lis[i].style.display = 'list-item';
        else
            lis[i].style.display = 'none';
    }
    });
    //end -filter process in select domain tab

    $("#statutory_date").empty();
    var defaultoption = $("<option></option>");
    defaultoption.val("");
    defaultoption.text("")
    $("#statutory_date").append(defaultoption);
    for (var i=1; i<=31; i++) {
        var option = $("<option></option>");
        option.val(i);
        option.text(i)
        $("#statutory_date").append(option);
    }

    $("#single_statutory_date").empty();
    var defaultoption = $("<option></option>");
    defaultoption.val("");
    defaultoption.text("")
    $("#single_statutory_date").append(defaultoption);
    for (var i=1; i<=31; i++) {
        var option = $("<option></option>");
        option.val(i);
        option.text(i)
        $("#single_statutory_date").append(option);
    }

    for(var j=1; j<=6; j++){
    $("#multiple_statutory_date"+j).empty();
    var defaultoption = $("<option></option>");
    defaultoption.val("");
    defaultoption.text("")
     $("#multiple_statutory_date"+j).append(defaultoption);
    for (var i=1; i<=31; i++) {
        var option = $("<option></option>");
        option.val(i);
        option.text(i)
        $("#multiple_statutory_date"+j).append(option);
    }   
    }


     $("#duration").keypress(function (e) {
     if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        //$("#errmsg").html("Digits Only").show().fadeOut("slow");
        return false;
    }
    });

     $("#triggerbefore").keypress(function (e) {
     if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        //$("#errmsg").html("Digits Only").show().fadeOut("slow");
        return false;
    }
    });

     $("#single_triggerbefore").keypress(function (e) {
     if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        //$("#errmsg").html("Digits Only").show().fadeOut("slow");
        return false;
    }
    });

    for(var j=1; j<=6; j++){
    $("#multiple_triggerbefore"+j).keypress(function (e) {
     if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        //$("#errmsg").html("Digits Only").show().fadeOut("slow");
        return false;
    }
    });
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
  $('#activate-step-4').on('click', function(e) {
  if (validate_thirdtab()){
  $('ul.setup-panel li:eq(3)').removeClass('disabled');
  $('ul.setup-panel li a[href="#step-4"]').trigger('click');
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
  $('#backward-step-3').on('click', function(e) {
  $('ul.setup-panel li:eq(3)').removeClass('disabled');
  $('ul.setup-panel li a[href="#step-3"]').trigger('click');

  })
  $('#activate-step-finish').on('click', function(e) {
  getGeographyResult();
  if (validate_fourthtab()){
  savestatutorymapping();
  }
  })

  $('#days').hide();
  $('#hours').show();
  $("#trigger_every").show();
  })
  $(function() {
  $(".dayhour").change(function(){
  if($(this).val()=="1")
  {
  $('#days').show();
  $('#hours').hide();
  $("#trigger_every").show();
  }else if($(this).val()=="2"){
  $('#days').hide();
  $('#hours').show();
  $("#trigger_every").show();
  }
  });
  $('.tasktype').change(function(){
  if($(this).val()=="2" || $(this).val()=="3")
  {
  $('#Recurring').show();
  $('#Occasional').hide();
  $('#One_Time').hide();
  }

  else if($(this).val() == "4" )
  {
  $('#Recurring').hide();
  $('#Occasional').show();
  $('#One_Time').hide();
  }

  else if($(this).val() == "1")
  {
  $('#Recurring').hide();
  $('#Occasional').hide();
  $('#One_Time').show();
  }
  else
  {
  $('#Recurring').hide();
  $('#Occasional').hide();
  $('#One_Time').hide();
  }
  });
  $('.multipleinput').change(function() {
  if ($(this).is(':checked')) {
  if($('#repeats_type').val() == '2'){
  $('.multipleselectnone').hide();
  $('.multipleselect').show();
  load_stautorydates();
  }else{
  $('.multipleselect').hide();
  $('.multipleselectnone').show();
  }

  } else {
  $('.multipleselect').hide();
  $('.multipleselectnone').show();
  }
  });
  $('#repeats_type').change(function() {
  if($('#repeats_type').val() == '2' && $('.multipleinput').prop("checked") == true){
  $('.multipleselectnone').hide();
  $('.multipleselect').show();
  load_stautorydates();
  }else{
  $('.multipleselect').hide();
  $('.multipleselectnone').show();
  }
  });
  $('#repeats_every').change(function() {
  if($('#repeats_type').val() == '2' && $('.multipleinput').prop("checked") == true){
  $('.multipleselectnone').hide();
  $('.multipleselect').show();
  load_stautorydates();
  }else{
  $('.multipleselect').hide();
  $('.multipleselectnone').show();
  }
  });
  $('.repeatlabelday').click(function(){
  $('#single_statutory_date').show();
  $('#multiple_statutory_date1').show();
  $('#multiple_statutory_date2').show();
  $('#multiple_statutory_date3').show();
  $('#multiple_statutory_date4').show();
  $('#multiple_statutory_date5').show();
  $('#multiple_statutory_date6').show();
  $('#single_statutory_date').val('');
  $('#multiple_statutory_date1').val('');
  $('#multiple_statutory_date2').val('');
  $('#multiple_statutory_date3').val('');
  $('#multiple_statutory_date4').val('');
  $('#multiple_statutory_date5').val('');
  $('#multiple_statutory_date6').val('');
  });
  $('.repeatlabelendday').click(function(){
  $('#single_statutory_date').hide();
  $('#multiple_statutory_date1').hide();
  $('#multiple_statutory_date2').hide();
  $('#multiple_statutory_date3').hide();
  $('#multiple_statutory_date4').hide();
  $('#multiple_statutory_date5').hide();
  $('#multiple_statutory_date6').hide();
  $('#single_statutory_date').val('30');
  $('#multiple_statutory_date1').val('30');
  $('#multiple_statutory_date2').val('30');
  $('#multiple_statutory_date3').val('30');
  $('#multiple_statutory_date4').val('30');
  $('#multiple_statutory_date5').val('30');
  $('#multiple_statutory_date6').val('30');
  });
});