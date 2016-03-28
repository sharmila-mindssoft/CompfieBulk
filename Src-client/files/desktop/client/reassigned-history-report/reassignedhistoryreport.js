var countriesList;
var domainsList;
var unitList;
var level1List;
var compliancesList;
var userList;
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
        compliancesList = data['compliances'];
        userList = data['users'];
    }
    function onFailure(error){
        console.log(error);
    }
    client_mirror.getReassignedHistoryReportFilters(  
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
    loadreassignedhistory("show");
});
$("#export-button").click(function(){ 
    loadreassignedhistory("export");
});
function loadreassignedhistory(buttontype){
    var countries = parseInt($("#country").val());
    countriesNameVal = $("#countryval").val();
    //Domain    
    var domain = parseInt($("#domain").val());
    domainNameVal = $("#domainval").val();
   
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
    var compliancesid = $("#compliancesid").val();
    if(compliancesid == ''){
        compliancesid = null;
    }
    else{
        compliancesid = parseInt(compliancesid);
    }
    var userid = $("#userid").val();
    if(userid == ''){
        userid = null;
    }
    else{
        userid = parseInt(userid);
    }
    var fromdate = $("#from-date").val();
    if(fromdate == ''){
        fromdate = null;
    }
    var todate = $("#to-date").val();
    if(todate == ''){
        todate = null;
    }
 
   
    if(countriesNameVal == ""){
        displayMessage("Enter Country");
    }
    else if(domainNameVal == ""){
        displayMessage("Enter Domain");  
    }
    else{
        function onSuccess(data){
            if(buttontype == "export"){
                var download_url = data["link"];
                window.open(download_url, '_blank');        
            }else{
                loadReassignedHistoryList(data['statutory_wise_compliances']);     
            }
        }
        function onFailure(error){
            console.log(error);
        }
        csv = false
        if(buttontype == "export"){
            csv = true
        }
        client_mirror.getReassignedHistoryReport(
            countries, domain, unitid, level1id,  compliancesid , userid, fromdate, todate, csv,
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


function loadReassignedHistoryList(data){
    $('.grid-table-rpt').show();
    $('.table-reassignedhistory-list').empty();
    var sno = 0;  
    $('.country-name').text(countriesNameVal);
    $('.domain-name').text(domainNameVal);
    $.each(data, function(key, value) {
        var tableRowHeading = $('#templates .table-reassigned-list .table-level1-heading');
        var cloneHeading = tableRowHeading.clone();
        $('.level1-heading', cloneHeading).text(data[key]['level_1_statutory_name']);
        $('.table-reassignedhistory-list').append(cloneHeading);

        var tableRow_tr = $('#templates .table-reassigned-list .heading-list');
        var clonetr = tableRow_tr.clone();
        $('.table-reassignedhistory-list').append(clonetr);

        var clist = data[key]['compliance'];
        $.each(clist, function(ke, val) {         
            var tableRowUnit = $('#templates .table-reassigned-list .unit-list');
            var cloneUnit = tableRowUnit.clone();
            $('.unit-heading', cloneUnit).html(clist[ke]['unit_name']);              
            $('.table-reassignedhistory-list').append(cloneUnit);
            var list = clist[ke]['reassign_compliances'];
            var acc_count = 1;

            $.each(list, function(k, val) {   
                var tableRow = $('#templates .table-reassigned-list .tbody-reassigned-list');
                var clone = tableRow.clone();      
                sno = sno + 1;
                $('.sno', clone).text(sno);
                $('.compliance-task', clone).html(list[k]['compliance_name']);
                $('.due-date', clone).html(list[k]['due_date']);
                var rhistory = list[k]['reassign_history'];
                var count = 0;
                $.each(rhistory, function(k1, val1) {                      
                    if(count == 0){
                        console.log("count=="+rhistory[k1]['reassigned_to']);
                        $('.assignee', clone).html(rhistory[k1]['reassigned_to']);
                        $('.reassign-date', clone).html(rhistory[k1]['reassigned_date']);
                        $('.reassigned-from', clone).html(rhistory[k1]['reassigned_from']);
                        $('.reason', clone).html(rhistory[k1]['reassign_reason']);
                        $('.table-reassignedhistory-list').append(clone);
                        $('.table-reassignedhistory-list').append('<tbody class="accordion-content accordion-content'+acc_count+'"></tbody>');
                        $('.accordion-content'+acc_count).addClass("default");
                        
                    }
                    else{
                        var tableRowvalues_ul = $('#templates .reassigned-inner-list');
                        var cloneval_ul = tableRowvalues_ul.clone();
                        $('.inner-assignee', cloneval_ul).html(rhistory[k1]['reassigned_to']);
                        $('.inner-reassigndate', cloneval_ul).html(rhistory[k1]['reassigned_date']);
                        $('.inner-reassigned-from', cloneval_ul).html(rhistory[k1]['reassigned_from']);
                        $('.inner-reason', cloneval_ul).html(rhistory[k1]['reassign_reason']);
                        $('.accordion-content'+acc_count).append(cloneval_ul);   
                    }
                    count++;
                });
                acc_count++;
            });

            $('#accordion').find('.accordion-toggle').click(function(){
                $(this).next().slideToggle('fast');
                $(".accordion-content").not($(this).next()).slideUp('fast');
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
    $("#level1id").val('');
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
  $('#selectboxview-compliances ul').empty();
  if(textval.length>0){
    for(var i in compliances){
        if (~compliances[i]['compliance_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([compliances[i]["compliance_id"],compliances[i]["compliance_name"]]);     
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_compliances(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#selectboxview-compliances ul').append(str);
    $("#compliancesid").val('');
    }
}
function activate_compliances (element,checkval,checkname) {
  $("#compliancesval").val(checkname);
  $("#compliancesid").val(checkval);
}

//Users---------------------------------------------------------------------------------------------------------------
function hideuserlist(){
    document.getElementById('autocompleteview-user').style.display = 'none';
}
function loadauto_users (textval) {
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
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_users(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-user ul').append(str);
    $("#userid").val('');
    }
}

function activate_users (element,checkval,checkname) {
  $("#usersval").val(checkname);
  $("#userid").val(checkval);
}


$(function() {
    initialize();
});
