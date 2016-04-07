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

var finalList;
var pageSize = 500;
var startCount = 0;
var endCount;
var sno = 0;
var fullArrayList = [];
var acc_count = 1;

function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}

function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}

function displayLoader() {
    $(".loading-indicator-spin").show();
}

function hideLoader() {
    $(".loading-indicator-spin").hide();
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
    loadcomplianceactivityreport("show");
});
$("#export-button").click(function(){ 
    loadcomplianceactivityreport("export");
});
function loadcomplianceactivityreport(buttontype){
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
            fullArrayList = [];
            hideLoader();
            clearMessage();
            startCount = 0;
            endCount = 0;

            if(buttontype == "show"){
                loadComplianceActivityReportList(data['activities']);     
            }
            if(buttontype == "export"){
                if (error == null){
                    var download_url = data["link"];
                    window.open(download_url, '_blank');
                }
                else {
                    displayMessage(error);
                }
            }
        }
        function onFailure(error){
            hideLoader();
            console.log(error);
        }
        var csv = false
        if(buttontype == "export"){
            csv = true
        }
        displayLoader();
        client_mirror.getComplianceActivityReportData(
           usertype, userid,  parseInt(countries), parseInt(domain), 
           level1id, unitid, complianceid, fromdate, todate, csv,
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
function compactivityfilterList(data){
    var tableRowHeading = $('#templates .table-compliance-activity-list-temp .filter-heading-list');
    var cloneHeading = tableRowHeading.clone();
    $('.country-filter-name', cloneHeading).text(countriesNameVal);
    $('.domain-filter-name', cloneHeading).text(domainNameVal);
    $('.usertype-filter-name', cloneHeading).text(usertype);
    $('.user-filter-name', cloneHeading).text(userval);
    $('.fromdate-filter-name', cloneHeading).text(fromdate);
    $('.todate-filter-name', cloneHeading).text(todate);

    $('.table-compliance-activity-list').append(cloneHeading);

    var tableRowHeadingth = $('#templates .table-compliance-activity-list-temp .table-heading-th');
    var cloneHeadingth = tableRowHeadingth.clone();
    $('.table-compliance-activity-list').append(cloneHeadingth);
}

function compactivityunitList(data){
    var tableRowUnit = $('#templates .table-compliance-activity-list-temp .table-unit-heading');
    var cloneUnit = tableRowUnit.clone();
    $('.unit-heading', cloneUnit).text(data['unit_name']+" - "+data['address']);
    $('.table-compliance-activity-list').append(cloneUnit);
}

function compactivitylevel1list(data){
    var tableRow = $('#templates .table-compliance-activity-list-temp .table-level1-heading');
    var clone = tableRow.clone();
    $('.level1-heading', clone).text(data['level1_name']);
    $('.table-compliance-activity-list').append(clone);
}

function compactivitycompliancetasklist(data, acc_count){
    var tableRowvalues = $('#templates .table-compliance-activity-list-temp .tbody-activity-list');
    var cloneval = tableRowvalues.clone();
    sno = sno + 1;
    $('.sno', cloneval).text(sno);
    $.each(data, function(k, val){
        $('.compliance-task', cloneval).html(k);
        var clist = data[k];
        var count = 0;
        
        $.each(clist, function(k1, val1){
            if(count == 0){
                $('.compliance-date', cloneval).html(clist[k1]['activity_date']);
                $('.activity-status', cloneval).html(clist[k1]['activity_status']);
                $('.compliance-task-status', cloneval).html(clist[k1]['compliance_status']);
                $('.remarks', cloneval).html(clist[k1]['remarks']);                    
                $('.compliance-activity-list .table-compliance-activity-list').append(cloneval);                        
                $('.table-compliance-activity-list').append('<tbody class="accordion-content accordion-content'+acc_count+'"></tbody>');
                if(acc_count == 1){
                    $('.accordion-content'+acc_count).addClass("default");    
                }
                
            }
            else{
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
    });
    
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

           if(Object.keys(list[y])[0] == "unit_name"){
               compactivityunitList(list[y]);
            }    
            else if(Object.keys(list[y])[0] == "level1_name"){
               compactivitylevel1list(list[y]);
            }    
            else{
               compactivitycompliancetasklist(list[y], acc_count);
               acc_count++;
            }
        }        
    }
    //textchangeloadinghide();
}

function loadresult(finalList) {   
    endCount = pageSize;
    $.each(finalList, function(i, val){
        var list = finalList[i];
        var list_statu_wise = val["statutory_wise_compliances"]
        delete list["statutory_wise_compliances"];         
        fullArrayList.push(list);

        $.each(list_statu_wise, function(i1, val1){
            var level1_Object = new Object();
            level1_Object.level1_name = i1;
            var list_act = val1;
            fullArrayList.push(level1_Object);
            
            $.each(list_statu_wise[i1], function(i2, val2){    
                var olddata  = {};            
                var newdata = {};
                newdata[i2] = val1[i2];
                $.extend(true, olddata, newdata);

                fullArrayList.push(olddata);
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
    compactivityfilterList();
    for(var y = 0;  y < pageSize; y++){
        if(sub_keys_list[y] !=  undefined){
            if(Object.keys(sub_keys_list[y])[0] == "unit_name"){
               compactivityunitList(sub_keys_list[y]);
            }    
            else if(Object.keys(sub_keys_list[y])[0] == "level1_name"){
               compactivitylevel1list(sub_keys_list[y]);
            }    
            else{
               compactivitycompliancetasklist(sub_keys_list[y], acc_count);
               acc_count++;
            }
        } 
    }
    $('#accordion').find('.accordion-toggle').click(function(){
        $(this).next().slideToggle('fast');
        $(".accordion-content").not($(this).next()).slideUp('fast');
    });
}


function loadComplianceActivityReportList(data){
    
    $(".grid-table-rpt").show();
    $('.table-compliance-activity-list').empty();
    var sno = 0;
    
    $.each(data, function(key, value) {     
        var level1list = data[key]['statutory_wise_compliances'];        
        $.each(level1list, function(ke, valu) { 
            var list = level1list[ke];
            $.each(list, function(k, val){               
                sno = sno + 1;                
            });               
        });       
    });
    loadresult(data);
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
