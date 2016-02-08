var countriesList;
var domainsList;
var businessgroupsList;
var legalEntityList;
var divisionsList;
var unitList;
var level1List;
var countriesText;
var domainval;

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
        console.log(data);
        countriesList = data['countries'];
        domainsList = data['domains'];
        businessgroupsList = data['business_groups'];
        legalEntityList = data['legal_entities'];
        divisionsList = data['divisions'];
        unitList = data['units'];
        level1List = data['level_1_statutories'];
    }
    function onFailure(error){
        console.log(error);
    }
    client_mirror.getStatutoryNotificationsListFilters(
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
    var countries = $("#country").val();
    var countriesNameVal = $("#countryval").val();
    //Domain    
    var domain = $("#domain").val();
    var domainNameVal = $("#domainval").val();
    //business_groups
    var businessgroupid = $("#businessgroupid").val();
    if(businessgroupid == ''){
        businessgroupid = null;
    }
    else{
        businessgroupid = parseInt(businessgroupid);
    }
    //Legal Entity
    var legalentityid = $("#legalentityid").val();
    if(legalentityid == ''){
        legalentityid = null;
    }
    else{
        legalentityid = parseInt(legalentityid);
    }
    //Divisions
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
   
    if(countries == ""){
        displayMessage("Please Enter Country");
    }
    else if(domain == ""){
        displayMessage("Please Enter Domain");  
    }
    else{
        function onSuccess(data){
            console.log(data);
            $(".grid-table-rpt").show();
            loadStatutoryNotificationsList(data['notifications']);     
        }
        function onFailure(error){
            console.log(error);
        }

        client_mirror.getStatutoryNotificationsListReport(
            countriesNameVal, domainNameVal, businessgroupid, legalentityid, divisionid, unitid, level1id,
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
});


function loadStatutoryNotificationsList(data){
    $('.tbody-statutory-notifications-list tr').remove();
    var sno = 0;
    console.log(data);
    $.each(data, function(key, value) {
        var tableRowHeading = $('#templates .table-statutory-notifications-list .table-row-heading');
        var cloneHeading = tableRowHeading.clone();
        var domainId = data[key]['domain_id'];
        $('.heading', cloneHeading).text(getDomainName(domainId));
        $('.tbody-statutory-notifications-list').append(cloneHeading);
        var list = data[key]['notifications'];
        $.each(list, function(k, val) { 
            var arr = [];
            var tableRow = $('#templates .table-statutory-notifications-list .table-row-values');
            var clone = tableRow.clone();
            sno = sno + 1;
            $('.sno', clone).text(sno);
            $('.statutory-provision', clone).html(list[k]['statutory_provision']);
            $('.unit-name', clone).html(list[k]['statutory_provision']);
            $('.statutory-notificaions', clone).html(list[k]['notification_text']);
            $('.date-time', clone).html(list[k]['date_and_time']);
            $('.tbody-statutory-notifications-list').append(clone);
        });
    });
    $(".total-records").html("Total : "+sno+" records")
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
  $('#autocompleteview-domains ul').empty();
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
//Level1 Statutory---------------------------------------------------------------------------------------------------------------
function hidedomainslist(){
    document.getElementById('selectboxview-domains').style.display = 'none';
}
function loadauto_domains (textval) {
  document.getElementById('selectboxview-domains').style.display = 'block';
  var domains = domainsList;
  var suggestions = [];
  $('#autocompleteview-domains ul').empty();
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
    $.each(level1, function(i, value){    
        if (~level1[i]['statutory'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([level1[i]["statutory"],level1[i]["statutory"]]);   
    });
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_level1(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-level1 ul').append(str);
    $("#legalentityid").val('');
    }
}
function activate_level1 (element,checkval,checkname) {
  $("#level1val").val(checkname);
  $("#level1id").val(checkval);
}
$(function() {
    initialize();
});
