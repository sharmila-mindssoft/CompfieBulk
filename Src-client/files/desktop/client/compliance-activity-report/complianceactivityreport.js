var countriesList;
var domainsList;
var unitList;
var userList;
var level1List;
var complianceList;
var countriesNameVal;
var domainNameVal;
var usertype;
var userval;
var fromdate;
var todate; 

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
        userList = data['users'];
        level1List = data['level_1_statutories'];
        complianceList = data['compliances'];
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
    //Usertype
    usertype = $("#user-type").val();
    if(usertype == ''){
        usertype = null;
    }
    //Unit
    var unitid = $("#unitid").val();
    if(unitid == ''){
        unitid = null;
    }
    else{
        unitid = parseInt(unitid);
    }
     //User
    userval = $("#userval").val();
    var userid = $("#userid").val();
    if(userid == ''){
        userid = null;
    }
    else{
        userid = parseInt(userid);
    }
    //Level 1 Statutories
    var level1id = $("#level1id").val();
    if(level1id == ''){
        level1id = null;
    }
    //compliance
    var complianceid = $("#complianceid").val();
    if(complianceid == ''){
        complianceid = null;
    }
    fromdate = $("#from-date").val();
    if(fromdate == ''){
        fromdate = null;
    }
    todate = $("#to-date").val();
    if(todate == ''){
        todate = null;
    }
    if(countries == ""){
        displayMessage("Enter Country");
    }
    else if(domain == ""){
        displayMessage("Enter Domain");  
    }
    else if(usertype  == null){
        displayMessage("Select Usertype");     
    }
    else if(fromdate != '' && todate ==''){
        displayMessage("Select To Date");
    }
    else if(fromdate == '' && todate !=''){
        displayMessage("Select From Date");
    }
    else{
        function onSuccess(data){
            loadComplianceActivityReportList(data['activities']);     
        }
        function onFailure(error){
            console.log(error);
        }

        client_mirror.getComplianceActivityReportData(
           usertype, userid,  parseInt(countries), parseInt(domain), level1id, unitid, complianceid, fromdate, todate,
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


function loadComplianceActivityReportList(data){
    $('.tbody-compliance-activity-list tr').remove();
    $(".grid-table-rpt").show();
    var sno = 0;
    
    $.each(data, function(key, value) {
        var tableRowHeading = $('#templates .table-compliance-activity-list .filter-heading-list');
        var cloneHeading = tableRowHeading.clone();
        $('.country-filter-name', cloneHeading).text(countriesNameVal);
        $('.domain-filter-name', cloneHeading).text(domainNameVal);
        $('.usertype-filter-name', cloneHeading).text(usertype);
        $('.user-filter-name', cloneHeading).text(userval);
        $('.fromdate-filter-name', cloneHeading).text(fromdate);
        $('.todate-filter-name', cloneHeading).text(todate);

        $('.compliance-activity-list .heading-list').append(cloneHeading);

        var tableRowHeadingth = $('#templates .table-compliance-activity-list .table-heading-th');
        var cloneHeadingth = tableRowHeadingth.clone();
        $('.compliance-activity-list .heading-list').append(cloneHeadingth);

        var tableRowUnit = $('#templates .table-compliance-activity-list .table-unit-heading');
        var cloneUnit = tableRowUnit.clone();
        $('.unit-heading', cloneUnit).text(data[key]['unit_name']);
        $('.compliance-activity-list .heading-list').append(cloneUnit);

        var level1list = data[key]['statutory_wise_compliances'];
        var acc_count = 1;
        $.each(level1list, function(ke, valu) { 
            var tableRow = $('#templates .table-compliance-activity-list .table-level1-heading');
            var clone = tableRow.clone();
            $('.level1-heading', clone).text(ke);
            $('.compliance-activity-list .heading-list').append(clone);

            var list = level1list[ke];
            $.each(list, function(k, val){
                var tableRowvalues = $('#templates .table-compliance-activity-list .tbody-activity-list');
                var cloneval = tableRowvalues.clone();
                sno = sno + 1;
                $('.sno', cloneval).text(sno);
                $('.compliance-task', cloneval).html(k);
                var clist = list[k];
                var count = 0;
                
                $.each(clist, function(k1, val1){
                    if(count == 0){
                        $('.compliance-date', cloneval).html(clist[k1]['activity_date']);
                        $('.activity-status', cloneval).html(clist[k1]['activity_status']);
                        $('.compliance-task-status', cloneval).html(clist[k1]['compliance_status']);
                        $('.remarks', cloneval).html(clist[k1]['remarks']);                    
                        $('.compliance-activity-list .table-compliance-activity-list').append(cloneval);                        
                        $('.table-compliance-activity-list').append('<tbody class="accordion-content accordion-content'+acc_count+'"></tbody>');
                        $('.accordion-content'+acc_count).addClass("default");
                    }
                    else{
                        console.log('accordion-content'+acc_count);
                        var tableRowvalues_ul = $('#templates .tree-tr');
                        var cloneval_ul = tableRowvalues_ul.clone();
                        $('.li-date', cloneval_ul).html(clist[k1]['activity_date']);
                        $('.li-activitystatus', cloneval_ul).html(clist[k1]['activity_status']);
                        $('.li-taskstatus', cloneval_ul).html(clist[k1]['compliance_status']);
                        $('.li-remarks', cloneval_ul).html(clist[k1]['remarks']);  
                        $('.accordion-content'+acc_count).append(cloneval_ul);   
                    }
                    count++;                    
                });

                acc_count++;
                
            });   
            
        }); 
        $('#accordion').find('.accordion-toggle').click(function(){
            //Expand or collapse this panel
            $(this).next().slideToggle('fast');
            //Hide the other panels
            $(".accordion-content").not($(this).next()).slideUp('fast');
        });       
    });
    $(".total-records").html("Total : "+sno+" records")
}

$("#accordion-bgwhite").find(".accordion-toggle-bgwhite").click(function(){
    $(this).next('tbody').slideToggle('fast');
    $(".accordion-content-bgwhite").not($(this).next()).slideUp('fast');
});



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
  
  var level1 = level1List;
  var suggestions = [];
  $('#autocompleteview-level1 ul').empty();
  if(textval.length>0){  
    for(var j = 0; j<level1.length; j++)
        if (~level1[j].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([level1[j],level1[j]]);   
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

//Compliances---------------------------------------------------------------------------------------------------------------
function hidecompliancelist(){
    document.getElementById('autocompleteview-compliance').style.display = 'none';
}
function loadauto_compliance (textval) {
    if($("#complianceval").val() == ''){
        $("#complianceid").val('');
    }
    document.getElementById('autocompleteview-compliance').style.display = 'block';
    var compliance = complianceList;
    var suggestions = [];
    $('#autocompleteview-compliance ul').empty();
    if(textval.length>0){
        for(var i in compliance){
            if (~compliance[i]['compliance_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([compliance[i]["compliance_id"],compliance[i]["compliance_name"]]);    
        }
        var str='';
        for(var i in suggestions){
          str += '<li id="'+suggestions[i][0]+'" onclick="activate_compliance(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
        }
        $('#autocompleteview-compliance ul').append(str);
        $("#complianceid").val('');
    }
}
function activate_compliance (element,checkval,checkname) {
  $("#complianceval").val(checkname);
  $("#complianceid").val(checkval);
}
$(function() {
    initialize();
});
