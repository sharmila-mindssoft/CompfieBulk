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
    $('.tbody-statutory-notifications-list tr').remove();
    sno = 0 ;    
    fullArrayList = [];
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
        $(".grid-table-rpt").hide();
    }
    else if(domain == ""){
        displayMessage(message.domain_required);
        $(".grid-table-rpt").hide();
    }
    else if(fromdate != '' && todate ==''){
        displayMessage(message.todate_required);
        $(".grid-table-rpt").hide();
    }
    else if(fromdate == '' && todate !=''){
        displayMessage(message.fromdate_required);
        $(".grid-table-rpt").hide();
    }
    else{
        clearMessage();
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
            if(Object.keys(list[y])[0] == "division_name"){
               filterlist(list[y]);
            }    
            else if(Object.keys(list[y])[0] == "notification_text"){
               statutorylist(list[y]);
            }    
            else {
               level1list(list[y]);
            }        
        }        
    }
    //textchangeloadinghide();
}
function loadresult(finalList) {   
    endCount = pageSize;
    $.each(finalList, function(i, val){
        var list = finalList[i];
        var list_level1 = list["level_1_statutory_wise_notifications"];
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

    var bg = '-';
    if(data["business_group_name"] != null) bg = data["business_group_name"];
    var dv = '-';
    if( data["division_name"] != null) dv = data["division_name"];
    var le = data["legal_entity_name"];

    var cloneHeading = tableRowHeading.clone();
    $('.heading-country-name', cloneHeading).text(countriesNameVal);
    $('.heading-domain-name', cloneHeading).text(domainNameVal);
    $('.heading-business-group-name', cloneHeading).text(bg);
    $('.heading-legal-entity-name', cloneHeading).text(le);
    $('.heading-division-name', cloneHeading).text(dv);
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
    var totalrecords = 0;
    $.each(data, function(key, value) {
        var level1list = data[key]['level_1_statutory_wise_notifications'];
        $.each(level1list, function(ke, valu) {           
            var list = level1list[ke];
            var reccount = list.length;
            totalrecords = totalrecords + reccount;  
        });
    });

    loadresult(data);
    $(".total-records").html( totalrecords +" records")
}

//retrive country autocomplete value
function onCountrySuccess(val){
  $("#countryval").val(val[1]);
  $("#country").val(val[0]);
}

//load country list in autocomplete text box  
$("#countryval").keyup(function(){
  var textval = $(this).val();
  getCountryAutocomplete(textval, countriesList, function(val){
    onCountrySuccess(val)
  })
});

//retrive domain autocomplete value
function onDomainSuccess(val){
  $("#domainval").val(val[1]);
  $("#domain").val(val[0]);
}
//load domain list in autocomplete textbox  
$("#domainval").keyup(function(){
  var textval = $(this).val();
  getDomainAutocomplete(textval, domainsList, function(val){
    onDomainSuccess(val)
  })
});

//retrive businessgroup form autocomplete value
function onBusinessGroupSuccess(val){
  $("#businessgroupsval").val(val[1]);
  $("#businessgroupid").val(val[0]);
}

//load businessgroup form list in autocomplete text box  
$("#businessgroupsval").keyup(function(){
  var textval = $(this).val();
  getClientBusinessGroupAutocomplete(textval, businessgroupsList, function(val){
    onBusinessGroupSuccess(val)
  })
});

//retrive legelentity form autocomplete value
function onLegalEntitySuccess(val){
  $("#legalentityval").val(val[1]);
  $("#legalentityid").val(val[0]);
}

//load legalentity form list in autocomplete text box  
$("#legalentityval").keyup(function(){
  var textval = $(this).val();
  getClientLegalEntityAutocomplete(textval, legalEntityList, function(val){
    onLegalEntitySuccess(val)
  })
});

//retrive division form autocomplete value
function onDivisionSuccess(val){
  $("#divisionval").val(val[1]);
  $("#divisionid").val(val[0]);
}

//load division form list in autocomplete text box  
$("#divisionval").keyup(function(){
  var textval = $(this).val();
  getClientDivisionAutocomplete(textval, divisionsList, function(val){
    onDivisionSuccess(val)
  })
});

//retrive unit form autocomplete value
function onUnitSuccess(val){
  $("#unitval").val(val[1]);
  $("#unitid").val(val[0]);
}

//load unit  form list in autocomplete text box  
$("#unitval").keyup(function(){
  var textval = $(this).val();
  //var cId = $("#country").val();
  //var dId = $("#domain").val();
  getUnitAutocomplete(textval, unitList, function(val){
    onUnitSuccess(val)
  })
});

//retrive statutory autocomplete value
function onStatutorySuccess(val){
  $("#level1val").val(val[1]);
  $("#level1id").val(val[0].replace(/##/gi,'"'));
}
//load statutory list in autocomplete textbox  
$("#level1val").keyup(function(){
  var textval = $(this).val();
  getClientStatutoryAutocomplete(textval, level1List, function(val){
    onStatutorySuccess(val)
  })
});

$(function() {
    initialize();
});
