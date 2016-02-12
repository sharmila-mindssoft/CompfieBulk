var countriesList;
var domainsList;
var businessgroupsList;
var legalEntityList;
var divisionsList;
var unitList;
var level1List;
var countriesText;
var countriesNameVal;
var domainNameVal;

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
        unitList = data['units'];
        level1List = data['level_1_statutories'];
    }
    function onFailure(error){
        console.log(error);
    }
    client_mirror.getComplianceActivityReportFilters(
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
    countriesNameVal = $("#countryval").val();
    //Domain    
    var domain = $("#domain").val();
    domainNameVal = $("#domainval").val();
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
        level1id = level1id;
    }
    var fromdate = $("#from-date").val();
    if(fromdate == ''){
        fromdate = null;
    }
    var todate = $("#to-date").val();
    if(todate == ''){
        todate = null;
    }
    if(countries == ""){
        displayMessage("Please Enter Country");
    }
    else if(domain == ""){
        displayMessage("Please Enter Domain");  
    }
    else if(fromdate != '' && todate ==''){
        displayMessage("Please Select To Date");
    }
    else if(fromdate == '' && todate !=''){
        displayMessage("Please Select From Date");
    }
    else{
        function onSuccess(data){
            $(".grid-table-rpt").show();
            loadStatutoryNotificationsList(data['statutory_wise_notifications']);     
        }
        function onFailure(error){
            console.log(error);
        }

        client_mirror.getStatutoryNotificationsListReport(
            countriesNameVal, domainNameVal, businessgroupid, legalentityid, divisionid, unitid, level1id, fromdate, todate,
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
    
    $.each(data, function(key, value) {
        var tableRowHeading = $('#templates .table-statutory-notifications-list .filter-heading-list');
        var cloneHeading = tableRowHeading.clone();
        $('.heading-country-name', cloneHeading).text(countriesNameVal);
        $('.heading-domain-name', cloneHeading).text(domainNameVal);
        $('.heading-business-group-name', cloneHeading).text(data[key]['business_group_name']);
        $('.heading-legal-entity-name', cloneHeading).text(data[key]['legal_entity_name']);
        $('.heading-division-name', cloneHeading).text(data[key]['division_name']);
        $('.statutory-notifications-list .tbody-statutory-notifications-list').append(cloneHeading);

        var tableRowHeadingth = $('#templates .table-statutory-notifications-list .heading-th');
        var cloneHeadingth = tableRowHeadingth.clone();
        $('.statutory-notifications-list .tbody-statutory-notifications-list').append(cloneHeadingth);

        var level1list = data[key]['level_1_statutory_wise_notifications'];
        $.each(level1list, function(ke, valu) { 
            var tableRow = $('#templates .table-statutory-notifications-list .table-row-heading ');
            var clone = tableRow.clone();
            $('.level1-heading', clone).text(ke);
            $('.statutory-notifications-list .tbody-statutory-notifications-list').append(clone);

            var list = level1list[ke];
            $.each(list, function(k, val){
                var tableRowvalues = $('#templates .table-statutory-notifications-list .table-row-values');
                var cloneval = tableRowvalues.clone();
                sno = sno + 1;
                $('.sno', cloneval).text(sno);
                $('.statutory-provision', cloneval).html(list[k]['statutory_provision']);
                $('.unit-name', cloneval).html(list[k]['unit_name']);
                $('.statutory-notificaions', cloneval).html(list[k]['notification_text']);
                $('.date-time', cloneval).html(list[k]['date_and_time']);
                $('.statutory-notifications-list .tbody-statutory-notifications-list').append(cloneval);
            });            
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
//User---------------------------------------------------------------------------------------------------------------
function hideuserlist(){
    document.getElementById('autocompleteview-user').style.display = 'none';
}
function loadauto_user (textval) {
    if($("#userval").val() == ''){
        $("#userid").val('');
    }
    document.getElementById('autocompleteview-user').style.display = 'block';
    var user = userList;
    var suggestions = [];
    $('#autocompleteview-user ul').empty();
    if(textval.length>0){
        for(var i in user){
            if (~user[i]['employee_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([user[i]["employee_id"],user[i]["employee_name"]]);    
        }
        var str='';
        for(var i in suggestions){
          str += '<li id="'+suggestions[i][0]+'" onclick="activate_user(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
        }
        $('#autocompleteview-user ul').append(str);
        $("#userid").val('');
    }
}
function activate_user (element,checkval,checkname) {
  $("#userval").val(checkname);
  $("#userid").val(checkval);
}

$(function() {
    initialize();
});
