var countriesList;
var domainsList;
var unitList;
var level1List;
var compliancesList;
var userList;

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
        unitList = data['units'];
        level1List = data['level_1_statutories'];
        compliancesList = data['compliances'];
        userList = data['users'];
    }
    function onFailure(error){
        console.log(error);
    }
    client_mirror.GetReassignedHistoryReportFilters(
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
        var tableRowHeading = $('#templates .table-reassigned-list .table-level1-heading');
        var cloneHeading = tableRowHeading.clone();
        $('.level1-heading', cloneHeading).text(data[key]['domain_id']);
        $('.tbody-reassigned-notifications-list').append(cloneHeading);

        var list = data[key]['compliances'];
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



//compliances---------------------------------------------------------------------------------------------------------------
function hidecomplianceslist(){
    document.getElementById('selectboxview-compliances').style.display = 'none';
}
function loadauto_compliances (textval) {
  document.getElementById('selectboxview-compliances').style.display = 'block';
  var compliances = compliancesList;
  var suggestions = [];
  $('#autocompleteview-compliances ul').empty();
  if(textval.length>0){
    for(var i in compliances){
        if (~compliances[i]['compliances_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([compliances[i]["compliances_id"],domains[i]["domain_name"]]);     
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_compliances(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#selectboxview-compliances ul').append(str);
    $("#compliances").val('');
    }
}


//Users---------------------------------------------------------------------------------------------------------------
function hideuserlist(){
    document.getElementById('selectboxview-user').style.display = 'none';
}
function loadauto_domains (textval) {
  document.getElementById('selectboxview-user').style.display = 'block';
  var user = userList;
  var suggestions = [];
  $('#autocompleteview-user ul').empty();
  if(textval.length>0){
    for(var i in user){
        if (~user[i]['users'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([user[i]["users"],domains[i]["users"]]);     
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_users(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#selectboxview-user ul').append(str);
    $("#users").val('');
    }
}

function activate_users (element,checkval,checkname) {
  $("#usersval").val(checkname);
  $("#users").val(checkval);
}


$(function() {
    initialize();
});
