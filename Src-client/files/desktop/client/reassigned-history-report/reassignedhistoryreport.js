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
        displayMessage(message.country_required);
    }
    else if(domainNameVal == ""){
        displayMessage(message.domain_required);  
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

//retrive unit form autocomplete value
function onUnitSuccess(val){
  $("#unitval").val(val[1]);
  $("#unitid").val(val[0]);
}

//load unit  form list in autocomplete text box  
$("#unitval").keyup(function(){
  var textval = $(this).val();
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

//retrive compliance task form autocomplete value
function onComplianceTaskSuccess(val){
  $("#compliancesval").val(val[1]);
  $("#compliancesid").val(val[0]);
}

//load compliancetask form list in autocomplete text box  
$("#compliancesval").keyup(function(){
  var textval = $(this).val();
  getComplianceTaskAutocomplete(textval, compliancesList, function(val){
    onComplianceTaskSuccess(val)
  })
});

//retrive user autocomplete value
function onUserSuccess(val){
  $("#userval").val(val[1]);
  $("#userid").val(val[0]);
}

//load user list in autocomplete text box  
$("#userval").keyup(function(){
  var textval = $(this).val();
  getUserAutocomplete(textval, userList, function(val){
    onUserSuccess(val)
  })
});



$(function() {
    initialize();
});
