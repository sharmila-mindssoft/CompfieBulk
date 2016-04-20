var countriesList;
var domainsList;
var businessgroupsList;
var legalEntityList;
var divisionsList;
var unitList;
var level1List;
var applicableStatusList;
var countriesText;
var domainText;
var businessGroupText;
var legalentityText;
var divisionText;

var pageSize = 500;
var startCount = 0;
var endCount;
var sno = 0;
var fullArrayList = [];


function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}

function initialize(){
    function onSuccess(data){
        countriesList = data['countries'];
        domainsList = data['domains'];
        businessgroupsList = data['business_groups'];
        legalEntityList = data['legal_entities'];
        divisionsList = data['divisions'];
        unitList = data['units'];
        level1List = data['level_1_statutories'];
        applicableStatusList = data['applicable_status'];
        loadApplicableStatus(applicableStatusList);
    }
    function onFailure(error){
        console.log(error);
    }
    client_mirror.getTaskApplicabilityReportFilters(
        function (error, response){
            if(error == null){
                onSuccess(response);
            }
            else{
                onFailure(error);
            }
        }
    );
}
$("#show-button").click(function(){ 
    loadcompliancetaskapplicabilityreport("show");
});
$("#export-button").click(function(){ 
    loadcompliancetaskapplicabilityreport("export");
});
function loadcompliancetaskapplicabilityreport(buttontype){
    var countries = $("#country").val();
    countriesText = $("#countryval").val();
    //Domain    
    var domain = $("#domain").val();
    domainText = $("#domainval").val();
    //business_groups
    businessgroupText = $("#businessgroupsval").val();
    var businessgroupid = $("#businessgroupid").val();
    if(businessgroupid == ''){
        businessgroupid = null;
    }
    else{
        businessgroupid = parseInt(businessgroupid);
    }
    //Legal Entity
    legalentityText = $("#legalentityval").val();
    var legalentityid = $("#legalentityid").val();
    if(legalentityid == ''){
        legalentityid = null;
    }
    else{
        legalentityid = parseInt(legalentityid);
    }
    //Divisions
    divisionText = $("#divisionval").val();
    var divisionid = $("#divisionid").val();
    if(divisionid == ''){
        divisionid = null;
    }
    else{
        divisionid = parseInt(divisionid);
    }
    //Unit
    var unitid = $("#unitid").val();
    if(unitid == ''){
        unitid = null;
    }
    else{
        unitid = parseInt(unitid);
    }
    //Level 1 Statutories
    var level1id = $("#level1id").val();
    if(level1id == ''){
        level1id = null;
    }
    else{
        level1id = parseInt(level1id);
    }
    var appstatus = $("#applicable-status").val();
    if(countries == ""){
        displayMessage(message.country_required);
    }
    else if(domain == ""){
        displayMessage(message.domain_required);  
    }
    else{
        function onSuccess(data){
            $(".grid-table-rpt").show();
                 
            if(buttontype == "export"){
                var download_url = data["link"];
                window.open(download_url, '_blank');     
            }else{
                loadTaskApplicabilityStatusList(data);
            }
        }
        function onFailure(error){
            console.log(error);
        }
        csv = false
        if(buttontype == "export"){
            csv = true
        }

        client_mirror.getTaskApplicabilityReportData(
            parseInt(countries), parseInt(domain), businessgroupid,
            legalentityid, divisionid, unitid, level1id, appstatus, csv,
            function (error, response){
                if(error == null){
                    onSuccess(response);
                }
                else{
                    onFailure(error);
                }
            }
        );
    }
}
function get_sub_array(object, start, end){
    if(!end){ end = -1;}
    return object.slice(start, end);
}

$(function() {
    $('#pagination').click(function(e){
        $(".loading-indicator-spin").show();
        if($('.loading-indicator-spin').css('display') != 'none')
        {
            setTimeout(function(){  
                showloadrecord();
            }, 500);
            
        }
        setTimeout(function(){  
            $(".loading-indicator-spin").hide();
        }, 500);
        
    });
});

function showloadrecord() {

    startCount = endCount;
    endCount = startCount + pageSize;
      
    var list = get_sub_array(fullArrayList, startCount, endCount);
    if(list.length < pageSize){
        $('#pagination').hide();
    }
    for(var y = 0;  y < pageSize; y++){
        if(list[y] !=  undefined){
            if(Object.keys(list[y])[0] == "compliance_frequency"){
               compliancelist(list[y]);
            }    
            else if(list[y] == "applicable" ||  list[y] == "not_applicable" || list[y] == "not_opted" ){
               applicablestatus(list[y]);
            }    
            else{
               level1heading(list[y]);
            }                
        }        
    }
}

function loadresult(finalList) {   
    endCount = pageSize;
    $.each(finalList, function(i, val){        
        var list = i;
        var list_act = val;

        if(Object.keys(val).length != 0){
            delete val;  
            fullArrayList.push(list);
            $.each(list_act, function (i_act, val_act){
                var actval = i_act;
                var list_unit = val_act;
                delete val_act;  
                fullArrayList.push(actval);
                $.each(list_unit, function(i_unit, val_unit){
                    var list_comp = val_unit['compliances'];
                    $.each(list_comp, function(i_com, val_com){  
                        jQuery.extend(val_com, {'unit_name': val_unit['unit_name'], 'address': val_unit['address']});
                        fullArrayList.push(val_com);
                    });
                });
            });    
        }

    });
    
    var totallist = fullArrayList.length;

    if(totallist > pageSize){
        $('#pagination').show();
    }
    else{
        $('#pagination').hide();
    }
    var sub_keys_list = get_sub_array(fullArrayList, startCount, endCount);
    filterheading();
    for(var y = 0;  y < pageSize; y++){
        if(sub_keys_list[y] !=  undefined){
            if(Object.keys(sub_keys_list[y])[0] == "compliance_frequency"){
               compliancelist(sub_keys_list[y]);
            }    
            else if(sub_keys_list[y] == "applicable" ||  sub_keys_list[y] == "not_applicable" || sub_keys_list[y] == "not_opted" ){
               applicablestatus(sub_keys_list[y]);
            }    
            else{
               level1heading(sub_keys_list[y]);
            }
        } 
    }
}
function filterheading(){
    var tableFilterHeading = $('#templates .table-task-applicability-list .filter-task-applicability-list');
    var clonefilterHeading = tableFilterHeading.clone();
    $('.filter-country', clonefilterHeading).text(countriesText);
    $('.filter-domain', clonefilterHeading).text(domainText);
    $('.filter-businessgroup', clonefilterHeading).text(businessgroupText);
    $('.filter-legalentity', clonefilterHeading).text(legalentityText);
    $('.filter-division', clonefilterHeading).text(divisionText);
    $('.tbody-task-applicability-list').append(clonefilterHeading);
}
function applicablestatus(key){
    count = 0;
    var tableRowHeading = $('#templates .table-task-applicability-list .applicable-status-list');
    var cloneHeading = tableRowHeading.clone();
    if(key == "applicable"){
        keyvalue = "Applicable"
    }
    if(key == "not_opted"){
        keyvalue = "Not Opted"
    }
    if(key == "not_applicable"){
        keyvalue = "Not Applicable"
    }
    $('.applicable-status-heading', cloneHeading).text(keyvalue);

    $('.tbody-task-applicability-list').append(cloneHeading);    
}
function level1heading(ke){
    var arr = [];
    var tableRowLevel1 = $('#templates .table-task-applicability-list .level1-list');
    var cloneLevel1 = tableRowLevel1.clone();
    $('.level1-heading', cloneLevel1).text(ke);
    $('.tbody-task-applicability-list').append(cloneLevel1);
    var tableRowList = $('#templates .table-task-applicability-list .list-heading');
    var cloneList = tableRowList.clone();
    $('.tbody-task-applicability-list').append(cloneList);   
}
function compliancelist(data){
    var valcomp = data;
    var tableRow = $('#templates .table-task-applicability-list .task-list');
    var clone = tableRow.clone();
    sno = sno + 1;
    $('.sno', clone).text(sno);
    $('.statutory-provision', clone).html(valcomp['statutory_provision']);
    $('.unit span', clone).html(valcomp["unit_name"]);
    $('.unit abbr', clone).attr("title", valcomp["address"]);
    $('.compliance-task a', clone).html(valcomp['compliance_name'][0]);
    $('.compliance-task a', clone).attr("href",valcomp['compliance_name'][1]);
    $('.compliance-description', clone).html(valcomp['description']);
    $('.penal-consequences', clone).html(valcomp['penal_consequences']);
    $('.compliance-frequency', clone).html(valcomp['compliance_frequency']);
    $('.repeats', clone).html(valcomp['repeats']);
    $('.tbody-task-applicability-list').append(clone);
}

function loadTaskApplicabilityStatusList(data){
    $("#pagination").hide();
    var totalrecords = 0;
    $('.tbody-task-applicability-list tr').remove();

    $.each(data, function(key, value) {   
        var actwiselist = data[key];
        $.each(actwiselist, function(ke, valu) {                      
            var list = actwiselist[ke];
            $.each(list, function(i, val) { 
                var listval = list[i]["compliances"];                                               
                var reccount = listval.length;
                totalrecords = totalrecords + reccount;                   
            });
        });
    });
    loadresult(data);    
    $(".total-records").html("Total : "+totalrecords+" records");
}


//Country----------------------------------------------------------------------------------------------------------------------
function hidecountrylist(){
    document.getElementById('selectboxview-country').style.display = 'none';
}
function loadauto_country (textval) {
  document.getElementById('selectboxview-country').style.display = 'block';
  var countries = countriesList;
  var suggestions = [];
  $('#selectboxview-country ul').empty();
  if(textval.length>0){
    for(var i in countries){
      if (~countries[i]['country_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([countries[i]["country_id"],countries[i]["country_name"]]); 
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#selectboxview-country ul').append(str);
    $("#country").val('');
    }
}
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#countryval").val(checkname);
  $("#country").val(checkval);  
}

//Domains---------------------------------------------------------------------------------------------------------------
function hidedomainslist(){
    document.getElementById('selectboxview-domains').style.display = 'none';
}
function loadauto_domains (textval) {
  document.getElementById('selectboxview-domains').style.display = 'block';
  var domains = domainsList;
  var suggestions = [];
  $('#selectboxview-domains ul').empty();
  if(textval.length>0){
    for(var i in domains){
        if (~domains[i]['domain_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([domains[i]["domain_id"],domains[i]["domain_name"]]);     
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_domains(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#selectboxview-domains ul').append(str);
    $("#domain").val('');
    }
}
function activate_domains (element,checkval,checkname) {
  $("#domainval").val(checkname);
  $("#domain").val(checkval);
}


//businessgroups---------------------------------------------------------------------------------------------------------------
function hidebgroupslist(){
    document.getElementById('autocompleteview-bgroups').style.display = 'none';
}
function loadauto_businessgroups (textval) {
    if($("#businessgroupsval").val() == ''){
        $("#businessgroupid").val('');
    }
    document.getElementById('autocompleteview-bgroups').style.display = 'block';
    var bgroups = businessgroupsList;
    var suggestions = [];
    $('#autocompleteview-bgroups ul').empty();
    if(textval.length>0){
        for(var i in bgroups){
            if (~bgroups[i]['business_group_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([bgroups[i]["business_group_id"],bgroups[i]["business_group_name"]]);     
        }
        var str='';
        for(var i in suggestions){
            str += '<li id="'+suggestions[i][0]+'" onclick="activate_businessgroups(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
        }
        $('#autocompleteview-bgroups ul').append(str);
        $("#businessgroupid").val('');
    }
}
function activate_businessgroups (element,checkval,checkname) {
  $("#businessgroupsval").val(checkname);
  $("#businessgroupid").val(checkval);
}
//Legal Entity---------------------------------------------------------------------------------------------------------------
function hidelentitylist(){
    document.getElementById('autocompleteview-lentity').style.display = 'none';
}
function loadauto_lentity (textval) {
    if($("#legalentityval").val() == ''){
        $("#legalentityid").val('');
    }
  document.getElementById('autocompleteview-lentity').style.display = 'block';
  var lentity = legalEntityList;
  var suggestions = [];
  $('#autocompleteview-lentity ul').empty();
  if(textval.length>0){
    for(var i in lentity){
        if($("#businessgroupid").val()!=''){
            if (~lentity[i]['legal_entity_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([lentity[i]["legal_entity_id"],lentity[i]["legal_entity_name"]]);   
        }        
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_lentity(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-lentity ul').append(str);
    $("#legalentityid").val('');
    }
}
//set selected autocomplte value to textbox
function activate_lentity (element,checkval,checkname) {
  $("#legalentityval").val(checkname);
  $("#legalentityid").val(checkval);
}
//Division---------------------------------------------------------------------------------------------------------------
function hidedivisionlist(){
    document.getElementById('autocompleteview-division').style.display = 'none';
}
function loadauto_division (textval) {
    if($("#divisionval").val() == ''){
        $("#divisionid").val('');
    }
  document.getElementById('autocompleteview-division').style.display = 'block';
  var division = divisionsList;
  var suggestions = [];
  $('#autocompleteview-division ul').empty();
  if(textval.length>0){
    for(var i in division){
        if (~division[i]['division_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([division[i]["division_id"],division[i]["division_name"]]);    
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_division(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-division ul').append(str);
    $("#divisionid").val('');
    }
}
function activate_division (element,checkval,checkname) {
  $("#divisionval").val(checkname);
  $("#divisionid").val(checkval);
}

//Units---------------------------------------------------------------------------------------------------------------
function hideunitlist(){
    document.getElementById('autocompleteview-unit').style.display = 'none';
}
function loadauto_unit (textval) {
    if($("#unitval").val() == ''){
        $("#unitid").val('');
    }
  document.getElementById('autocompleteview-unit').style.display = 'block';
  var unit = unitList;
  var suggestions = [];
  $('#autocompleteview-unit ul').empty();
  if(textval.length>0){
    for(var i in unit){
        var getunitidname = unit[i]['unit_code']+"-"+unit[i]['unit_name'];
        if (~getunitidname.toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([unit[i]["unit_id"],unit[i]["unit_name"],unit[i]["unit_code"]]);  
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_unit(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\', \''+suggestions[i][2]+'\')">'+suggestions[i][2]+'-'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-unit ul').append(str);
    $("#unitid").val('');
    }
}
function activate_unit (element,checkval,checkname, concatunit) {
  $("#unitval").val(concatunit+'-'+checkname);
  $("#unitid").val(checkval);
}

//Level 1 Statutory---------------------------------------------------------------------------------------------------------------
function hidelevel1list(){
    document.getElementById('autocompleteview-level1').style.display = 'none';
}
function loadauto_level1 (textval) {
    if($("#level1val").val() == ''){
        $("#level1id").val('');
    }
  document.getElementById('autocompleteview-level1').style.display = 'block';
  var countryId = $("#country").val();
  var domainId = $("#domain").val();
  var level1 = level1List;
  var suggestions = [];
  $('#autocompleteview-level1 ul').empty();
  if(textval.length>0){
    for(var j = 0; j<level1.length; j++){
      if (~level1[j].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([level1[j],level1[j]]);   
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_level1(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-level1 ul').append(str);
    $("#level1id").val('');
    }
}
function activate_level1 (element,checkval,checkname) {
  $("#level1val").val(checkname);
  $("#level1id").val(checkval);
}
//Countries---------------------------------------------------------------------------------------------------------------
function loadApplicableStatus(list){
  for(var k = 0; k < list.length; k++){
    $('#applicable-status').append($('<option value="'+list[k]+'">'+list[k]+'</option>'));
  }
}
$(function() {
    initialize();
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