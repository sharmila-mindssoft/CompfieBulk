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

var finalList;
var pageSize = 500;
var startCount = 0;
var endCount;
var sno = 0;
var unitcountid = null;
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
        level1List = data['users'];
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
    loadStatutoryNotificationsListreport("show");
});
$("#export-button").click(function(){ 
    loadStatutoryNotificationsListreport("export");
});
function loadStatutoryNotificationsListreport(buttontype){

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
        displayMessage(message.country_required);
    }
    else if(domain == ""){
        displayMessage(message.domain_required);
    }
    else if(fromdate != '' && todate ==''){
        displayMessage(message.todate_required);
    }
    else if(fromdate == '' && todate !=''){
        displayMessage(message.fromdate_required);
    }
    else{
        function onSuccess(data){
            $(".grid-table-rpt").show();
            
            if(buttontype == "export"){
                var download_url = data["link"];
                window.open(download_url, '_blank');      
            }
            else{
                loadStatutoryNotificationsList(data['statutory_wise_notifications']);    
            }
        }
        function onFailure(error){
            console.log(error);
        }
        csv = false
        if(buttontype == "export"){
            csv = true   
        } 
        client_mirror.getStatutoryNotificationsListReport(
            countriesNameVal, domainNameVal, businessgroupid, legalentityid, divisionid, 
            unitid, level1id, fromdate, todate, csv,
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
    
    //e.preventDefault();
    for(var y = 0;  y < pageSize; y++){
        if(list[y] !=  undefined){
            if(Object.keys(sub_keys_list[y])[0] == "division_name"){
               filterlist(sub_keys_list[y]);
            }    
            else if(Object.keys(sub_keys_list[y])[0] == "notification_text"){
               statutorylist(sub_keys_list[y]);
            }    
            else {
               level1list(sub_keys_list[y]);
            }        
        }        
    }
    //textchangeloadinghide();
}
function loadresult(finalList) {   
    endCount = pageSize;
    $.each(finalList, function(i, val){
        var list = finalList[i];
        var list_level1 = val;
        delete list["level_1_statutory_wise_notifications"];         
        fullArrayList.push(list);

        $.each(list_level1, function(i1, val1){
            var list_val = i1;
            var list_text = val1;
            delete val1;  
            fullArrayList.push(list_val);
       
            $.each(list_text, function(i2, val2){
                var list_c = list_text[i2]; 
                fullArrayList.push(list_c);
            }); 
        });
    });
    var totallist = fullArrayList.length;

    if(totallist > pageSize){
        $('#pagination').show();
    }
    else{
        $('#pagination').hide();
    }
    var sub_keys_list = get_sub_array(fullArrayList, startCount, endCount);
    
    for(var y = 0;  y < pageSize; y++){
        if(sub_keys_list[y] !=  undefined){
            if(Object.keys(sub_keys_list[y])[0] == "division_name"){
               filterlist(sub_keys_list[y]);
            }    
            else if(Object.keys(sub_keys_list[y])[0] == "notification_text"){
               statutorylist(sub_keys_list[y]);
            }    
            else {
               level1list(sub_keys_list[y]);
            }
        } 
    }
}

function filterlist(data){
    var tableRowHeading = $('#templates .table-statutory-notifications-list .filter-heading-list');
    var cloneHeading = tableRowHeading.clone();
    $('.heading-country-name', cloneHeading).text(countriesNameVal);
    $('.heading-domain-name', cloneHeading).text(domainNameVal);
    $('.heading-business-group-name', cloneHeading).text(data['business_group_name']);
    $('.heading-legal-entity-name', cloneHeading).text(data['legal_entity_name']);
    $('.heading-division-name', cloneHeading).text(data['division_name']);
    $('.statutory-notifications-list .tbody-statutory-notifications-list').append(cloneHeading);

    var tableRowHeadingth = $('#templates .table-statutory-notifications-list .heading-th');
    var cloneHeadingth = tableRowHeadingth.clone();
    $('.statutory-notifications-list .tbody-statutory-notifications-list').append(cloneHeadingth);
}

function level1list(data){
    var tableRow = $('#templates .table-statutory-notifications-list .table-row-heading ');
    var clone = tableRow.clone();
    $('.level1-heading', clone).text(data);
    $('.statutory-notifications-list .tbody-statutory-notifications-list').append(clone);
}

function statutorylist(data){
    var tableRowvalues = $('#templates .table-statutory-notifications-list .table-row-values');
    var cloneval = tableRowvalues.clone();
    sno = sno + 1;
    $('.sno', cloneval).text(sno);
    $('.statutory-provision', cloneval).html(data['statutory_provision']);
    $('.unit-name', cloneval).html(data['unit_name']);
    $('.statutory-notificaions', cloneval).html(data['notification_text']);
    $('.date-time', cloneval).html(data['date_and_time']);
    $('.statutory-notifications-list .tbody-statutory-notifications-list').append(cloneval);
}

function loadStatutoryNotificationsList(data){
    $('.tbody-statutory-notifications-list tr').remove();
    var totalrecords = 0;
    $.each(data, function(key, value) {
        var level1list = data[key]['level_1_statutory_wise_notifications'];
        $.each(level1list, function(ke, valu) {           
            var list = level1list[ke];
            $.each(list, function(k, val){
                var reccount = list.length;
                totalrecords = totalrecords + reccount;  
            });
        });
    });
    loadresult(data);
    $(".total-records").html( sno+" records")
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
