var countriesList;
var businessgroupsList;
var divisionsList;
var domainsList;
var groupList;
var legalEntityList;
var unitList;
var countriesText;
var groupsval;
var businessgroupsval;
var legalentityval;
var divisionval;
var unitval;

function initialize(){
    function onSuccess(data){
        countriesList = data['countries'];
        businessgroupsList = data['business_groups'];
        divisionsList = data['divisions'];
        domainsList = data['domains'];
        groupList = data['group_companies'];
        legalEntityList = data['legal_entities'];
        unitList = data['units'];
        loadCountries(countriesList);
    }
    function onFailure(error){
        console.log(error);
    }
    mirror.getClientDetailsReportFilters(
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
    clearMessage();
    var countries = $("#countries").val();
    countriesText = $("#countries  option:selected").text();
    var groupid = $("#group-id").val();
    groupsval = $("#groupsval").val();
    var bgroups = $("#businessgroupid").val();
    if(bgroups != ''){ 
        var businessgroupid = parseInt(bgroups);
    }
    else{
        var businessgroupid = null;
    }
    businessgroupsval = $("#businessgroupsval").val();
    var legalentity = $("#legalentityid").val();
    if(legalentity != ''){
        var lentityid = parseInt(legalentity);
    }
    else{
        var lentityid = null;
    }
    legalentityval = $("#legalentityval").val();
    var division = $("#divisionid").val();
    if(division != ''){
        var divisionid = parseInt(division);
    }
    else{
        var divisionid = null;
    }
    divisionval = $("#divisionval").val();
    var units = $("#unitid").val();
    if(units != ''){
        var unitid = parseInt(units);
    }
    else{
        var unitid = null;
    }
    unitval = $("#unitval").val();
    var domain = $("#domain").val();
    if(domain != ''){
        var arrayDomainsVal = domain.split(",");
        var arrayDomains = [];
        for(var j = 0; j < arrayDomainsVal.length; j++){
            arrayDomains[j] = parseInt(arrayDomainsVal[j]);
        } 
        var domainsVal = arrayDomains;
    }
    if(domain == ''){
        var domainsVal = null;
    }   

    if(countries == ""){
        displayMessage(message.country_required);
    }
    else if(groupid == ""){
        displayMessage(message.group_required);  
    }
    else{
        function onSuccess(data){
            $(".grid-table-rpt").show();
            $(".countryval").text(countriesText);
            $(".groupsval").text(groupsval);
            $(".bgroupsval").text(businessgroupsval);
            $(".lentityval").text(legalentityval);
            $(".divisionval").text(divisionval);
            loadClientDetailsList(data['units']);       
        }
        function onFailure(error){
            console.log(error);
        }
        mirror.getClientDetailsReport(parseInt(countries), parseInt(groupid), businessgroupid,  
            lentityid, divisionid, unitid,  domainsVal,
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

function getBusinessGroupName(businessGroupId){
    var businessgroupName;
    if(businessGroupId != null){
        $.each(businessgroupsList, function(key, value){
            if(value['business_group_id'] == businessGroupId){
                businessgroupName = value['business_group_name'];
            }
        });
    }
   if(businessGroupId == null){
        businessgroupName = "Nil";
    }
    return businessgroupName;   
}
function getLegalEntityName(legalentityId){
    var legalEntityName;

    if(legalentityId != null){
        $.each(legalEntityList, function(key, value){
            if(value['legal_entity_id'] == legalentityId){
                legalEntityName = value['legal_entity_name'];
            }
        });    
    }
    if(legalentityId == null){
        legalEntityName = "Nil";
    }
    
    return legalEntityName; 
}
function getDivisionName(divisionId){
    var divisionName;
    if(divisionId != null){
        $.each(divisionsList, function(key, value){
            if(value['division_id'] == divisionId){
                divisionName = value['division_name'];
            }
        });
    }
    if(divisionId == null){
        divisionName = "Nil";
    }
    return divisionName;
}
function loadClientDetailsList(data){
    $('.table-clientdetails-list tbody').empty();
    var sno = 0;
    if(data.length != 0 ){
        $.each(data, function(key, value) {
            var tablefilter = $('#templates .tr-filter');
            var clonefilter = tablefilter.clone();
            $(".bgroupsval", clonefilter).text(getBusinessGroupName(value['business_group_id']));
            $(".lentityval", clonefilter).text(getLegalEntityName(value['legal_entity_id']));
            $(".divisionval", clonefilter).text(getDivisionName(value['division_id']));
            $('.tbody-clientdetails-list').append(clonefilter);

            var tableheading = $('#templates .tr-heading');
            var cloneheading = tableheading.clone();
            $('.tbody-clientdetails-list').append(cloneheading);

            var list = value['units'];
            $.each(list, function(k, val) { 
                var arr = [];
                var domainsNames = '';
                var tableRow = $('#templates .table-row');
                var clone = tableRow.clone();
                sno = sno + 1;
                $('.sno', clone).text(sno);
                $('.unit-name', clone).html(val['unit_code']+" - "+val['unit_name']);
                arr = val['domain_ids'];
                $.each(domainsList, function(key, value){
                    var domianid = value['domain_id'];
                    var domainname = value['domain_name']
                    if(jQuery.inArray(domianid, arr ) > -1){
                        domainsNames += domainname + ", ";
                    }
                });                 
                $('.domain-name', clone).html(domainsNames);
                $('.unit-address', clone).text(val['unit_address']+", "+val['geography_name']);
                $('.pincode', clone).html(val['postal_code']);
                $('.tbody-clientdetails-list').append(clone);
            });
        });
        $(".total-records").html("Total : "+sno+" records")
    }
    else{
        $(".tbody-clientdetails-list").html("<center style='padding:40px 0px; font-size:0.813em; '>No records found!</center>");
        $(".total-records").html("");
    }
    
}

//Countries---------------------------------------------------------------------------------------------------------------
function loadCountries(countriesList){
    $.each(countriesList, function(key, values){
        var countryId = countriesList[key]['country_id'];
        var countryName = countriesList[key]['country_name'];
        $('#countries').append($('<option value="'+countryId+'">'+countryName+'</option>'));
    });
}
//Groups----------------------------------------------------------------------------------------------------------------------
function hidegroupslist(){
    document.getElementById('autocompleteview').style.display = 'none';
}
function loadauto_text (textval) {
  document.getElementById('autocompleteview').style.display = 'block';
  var groups = groupList;
  var suggestions = [];
  $('#autocompleteview ul').empty();
  if(textval.length>0){
    for(var i in groups){
      if (~groups[i]['group_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([groups[i]["client_id"],groups[i]["group_name"]]); 
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_text(this)">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview ul').append(str);
    $("#group-id").val('');
    }else{
      $("#group-id").val('');
      $("#autocompleteview").hide();
    }
}
//set selected autocomplte value to textbox
function activate_text (element) {
  var checkname = $(element).text();
  var checkval = $(element).attr('id');
  $("#groupsval").val(checkname);
  $("#group-id").val(checkval);  
}

//businessgroups---------------------------------------------------------------------------------------------------------------
function hidebgroupslist(){
    document.getElementById('autocompleteview-bgroups').style.display = 'none';
}
function loadauto_businessgroups (textval) {
    document.getElementById('autocompleteview-bgroups').style.display = 'block';
    var bgroups = businessgroupsList;
    var suggestions = [];
    $('#autocompleteview-bgroups ul').empty();
    if(textval.length>0){
        for(var i in bgroups){
            if(bgroups[i]['client_id']==$("#group-id").val()){
                if (~bgroups[i]['business_group_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([bgroups[i]["business_group_id"],bgroups[i]["business_group_name"]]);     
            }      
        }
        var str='';
        for(var i in suggestions){
          str += '<li id="'+suggestions[i][0]+'" onclick="activate_businessgroups(this)">'+suggestions[i][1]+'</li>';
        }
        $('#autocompleteview-bgroups ul').append(str);
        $("#businessgroupid").val('');
    }
    else{
      $("#businessgroupid").val('');
      $("#autocompleteview-bgroups").hide();
    }
}
function activate_businessgroups (element) {
  var checkname = $(element).text();
  var checkval = $(element).attr('id');
  $("#businessgroupsval").val(checkname);
  $("#businessgroupid").val(checkval);
}
//Legal Entity---------------------------------------------------------------------------------------------------------------
function hidelentitylist(){
    document.getElementById('autocompleteview-lentity').style.display = 'none';
}
function loadauto_lentity (textval) {
  document.getElementById('autocompleteview-lentity').style.display = 'block';
  var lentity = legalEntityList;
  var suggestions = [];
  $('#autocompleteview-lentity ul').empty();
  if(textval.length>0){
    for(var i in lentity){
        if($("#businessgroupid").val()!=''){
            if(lentity[i]['business_group_id']==$("#businessgroupid").val()){
                if (~lentity[i]['legal_entity_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([lentity[i]["legal_entity_id"],lentity[i]["legal_entity_name"]]);   
            }      
        }
        else{
            if(lentity[i]['client_id']==$("#group-id").val()){
                if (~lentity[i]['legal_entity_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([lentity[i]["legal_entity_id"],lentity[i]["legal_entity_name"]]);   
            }     
        }
        
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_lentity(this)">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-lentity ul').append(str);
    $("#legalentityid").val('');
    }else{
      $("#legalentityid").val('');
      $("#autocompleteview-lentity").hide();
    }
}
//set selected autocomplte value to textbox
function activate_lentity (element) {
var checkname = $(element).text();
  var checkval = $(element).attr('id');
  $("#legalentityval").val(checkname);
  $("#legalentityid").val(checkval);
}
//Division---------------------------------------------------------------------------------------------------------------
function hidedivisionlist(){
    document.getElementById('autocompleteview-division').style.display = 'none';
}
function loadauto_division (textval) {
  document.getElementById('autocompleteview-division').style.display = 'block';
  var division = divisionsList;
  var suggestions = [];
  $('#autocompleteview-division ul').empty();
  if(textval.length>0){
    for(var i in division){
        if($("#legalentityid").val() != ''){
            if(division[i]['legal_entity_id']==$("#legalentityid").val()){
                if (~division[i]['division_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([division[i]["division_id"],division[i]["division_name"]]);    
            }
        }
        else{
            if(division[i]['client_id']==$("#group-id").val()){
               if (~division[i]['division_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([division[i]["division_id"],division[i]["division_name"]]);    
            }
        }   
               
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_division(this)">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-division ul').append(str);
    $("#divisionid").val('');
    }else{
      $("#divisionid").val('');
      $("#autocompleteview-division").hide();
    }
}
function activate_division (element) {
  var checkname = $(element).text();
  var checkval = $(element).attr('id');
  $("#divisionval").val(checkname);
  $("#divisionid").val(checkval);
}

//Units---------------------------------------------------------------------------------------------------------------
function hideunitlist(){
    document.getElementById('autocompleteview-unit').style.display = 'none';
}
function loadauto_unit (textval) {
    document.getElementById('autocompleteview-unit').style.display = 'block';
    var unit = unitList;
    var suggestions = [];
    $('#autocompleteview-unit ul').empty();
    if(textval.length>0){
        for(var i in unit){
            if($("#legalentityid").val() != ''){
                if(unit[i]['legal_entity_id'] == $("#legalentityid").val()){
                    if (~unit[i]['unit_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([unit[i]["unit_id"],unit[i]["unit_name"],unit[i]["unit_code"] ]);    
                }       
            }
            else if($("#divisionid").val() != ''){
                if(unit[i]['division_id']==$("#divisionid").val()){
                    if (~unit[i]['unit_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([unit[i]["unit_id"],unit[i]["unit_name"],unit[i]["unit_code"]]);    
                }       
            }
            else{
                if(unit[i]['client_id'] == $("#group-id").val()){
                    if (~unit[i]['unit_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([unit[i]["unit_id"],unit[i]["unit_name"],unit[i]["unit_code"]]);    
                } 
            }        
        }
        var str='';
        for(var i in suggestions){
            str += '<li id="'+suggestions[i][0]+'" onclick="activate_unit(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\', \''+suggestions[i][2]+'\')">'+suggestions[i][2]+'-'+suggestions[i][1]+'</li>';
        }
        $('#autocompleteview-unit ul').append(str);
        $("#unitid").val('');
    }
    else{
      $("#unitid").val('');
      $("#autocompleteview-unit").hide();
    }
}
function activate_unit (element,checkval,checkname, unitcode) {
  $("#unitval").val(unitcode+"-"+checkname);
  $("#unitid").val(checkval);
}
//Domains------------------------------------------------------------------------------------------------


function hidedomainmenu() {
    document.getElementById('selectboxview-domains').style.display = 'none';
}

function loadauto_domains() {
    document.getElementById('selectboxview-domains').style.display = 'block';
    var editdomainval=[];
    if($("#domain").val() != ''){
        editdomainval = $("#domain").val().split(",");
    }
    var domains = domainsList;
    $('#selectboxview-domains ul').empty();
    var str='';
    for(var i in domains){
        var selectdomainstatus='';
        for(var j=0; j<editdomainval.length; j++){
            if(editdomainval[j]==domains[i]["domain_id"]){
                selectdomainstatus='checked';
            }
        }
        var domainId=parseInt(domains[i]["domain_id"]);
        var domainName=domains[i]["domain_name"];
        if(selectdomainstatus == 'checked'){
            str += '<li id="'+domainId+'" class="active_selectbox" onclick="activate(this)" >'+domainName+'</li> ';
        }else{
            str += '<li id="'+domainId+'" onclick="activate(this)" >'+domainName+'</li> ';
        }
    }
  $('#selectboxview-domains ul').append(str);
  $("#domainselected").val(editdomainval.length+" Selected")
 // }
}
//check & uncheck process
function activate(element){
    var chkstatus = $(element).attr('class');
    if(chkstatus == 'active_selectbox'){
        $(element).removeClass("active_selectbox");
    }else{
        $(element).addClass("active_selectbox");
    }  
    var selids='';
    var totalcount =  $(".active_selectbox").length;
    $(".active_selectbox").each( function( index, el ) {
        if (index === totalcount - 1) {
            selids = selids+el.id;
        }else{
            selids = selids+el.id+",";          
        }    
    });
    $("#domainselected").val(totalcount+" Selected");
    $("#domain").val(selids);
    
}

$(function() {
    $(".grid-table-rpt").hide();
    initialize();
});