var countriesList;
var domainsList;
var unitList;
var level1List;
var compliancesList;
var userList;
var countriesNameVal;
var domainNameVal;
var lastUnit = '';
var lastAct = '';
var totalRecord;
var sno = 0;
var acc_count = 1;
var s_endCount = 0;

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
        level1List = data['level_1_statutories'];
        compliancesList = data['compliances'];
        userList = data['users'];
    }
    function onFailure(error){
        displayMessage(error);
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

//pagination process
$('#pagination').click(function(){
  loadreassignedhistory("show", sno);
});


$("#show-button").click(function(){
    loadreassignedhistory("show", 0);
});
$("#export-button").click(function(){
    loadreassignedhistory("export", 0);
});
function loadreassignedhistory(buttontype, end_count){

    if(end_count == 0){
        acc_count = 1;
        lastAct = '';
        lastUnit = '';
        acc_count = 1;
        sno = 0;
        s_endCount = 0;
        $('.table-reassignedhistory-list').empty();
    }
    displayLoader();
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
        hideLoader();
    }
    else if(domainNameVal == ""){
        displayMessage(message.domain_required);
        hideLoader();
    }
    else{
        function onSuccess(data){

            if(buttontype == "export"){
                var download_url = data["link"];
                window.open(download_url, '_blank');
                hideLoader();
            }else{
                $('.grid-table-rpt').show();
                totalRecord = data["total"];
                loadReassignedHistoryList(data['statutory_wise_compliances']);
                hideLoader();
            }
        }
        function onFailure(error){
            displayMessage(error);
            hideLoader();
        }
        csv = false
        if(buttontype == "export"){
            csv = true
        }
        client_mirror.getReassignedHistoryReport(
            countries, domain, unitid, level1id,  compliancesid , userid, fromdate, todate, csv, s_endCount,
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

    $('.country-name').text(countriesNameVal);
    $('.domain-name').text(domainNameVal);
    $.each(data, function(key, value) {

        if(lastAct != data[key]['level_1_statutory_name']){
            var tableRowHeading = $('#templates .table-reassigned-list .level1-list');
            var cloneHeading = tableRowHeading.clone();
            $('.level1-heading', cloneHeading).text(data[key]['level_1_statutory_name']);
            $('.table-reassignedhistory-list').append(cloneHeading);

            var tableRow_tr = $('#templates .table-reassigned-list .heading-list');
            var clonetr = tableRow_tr.clone();
            $('.table-reassignedhistory-list').append(clonetr);
            lastUnit = '';
            lastAct = data[key]['level_1_statutory_name'];
        }


        var clist = data[key]['compliance'];
        $.each(clist, function(ke, val) {

            if(lastUnit != clist[ke]['unit_name']){
                var tableRowUnit = $('#templates .table-reassigned-list .unit-list');
                var cloneUnit = tableRowUnit.clone();
                $('.unit-heading', cloneUnit).html(clist[ke]['unit_name']);
                $('.table-reassignedhistory-list').append(cloneUnit);
            }
            var list = clist[ke]['reassign_compliances'];

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
                        s_endCount++;
                    }
                    else{
                        var tableRowvalues_ul = $('#templates .reassigned-inner-list');
                        var cloneval_ul = tableRowvalues_ul.clone();
                        $('.inner-assignee', cloneval_ul).html(rhistory[k1]['reassigned_to']);
                        $('.inner-reassigndate', cloneval_ul).html(rhistory[k1]['reassigned_date']);
                        $('.inner-reassigned-from', cloneval_ul).html(rhistory[k1]['reassigned_from']);
                        $('.inner-reason', cloneval_ul).html(rhistory[k1]['reassign_reason']);
                        $('.accordion-content'+acc_count).append(cloneval_ul);
                        s_endCount++;
                    }
                    count++;
                });
                acc_count++;
            });
        });
    });

    if(totalRecord == 0){
        var tableRow4=$('#no-record-templates .table-no-content .table-row-no-content');
        var clone4=tableRow4.clone();
        $('.no_records', clone4).text('No Compliance Found');
        $('.tbody-unit').append(clone4);
        $('#pagination').hide();
        $('.total-records').text('');
    }else{
        $('.total-records').text("Showing " + 1 + " to " + sno + " of " + totalRecord);
        if(sno >= totalRecord){
          $('#pagination').hide();
          $('#accordion').find('.accordion-toggle').click(function(){
            $(this).next().slideToggle('fast');
            $(".accordion-content").not($(this).next()).slideUp('fast');
        });
        }else{
          $('#pagination').show();
        }
    }
}


//retrive country autocomplete value
function onCountrySuccess(val){
  $("#countryval").val(val[1]);
  $("#country").val(val[0]);
}

//load country list in autocomplete text box
$("#countryval").keyup(function(e){
  function callback(val){
    onCountrySuccess(val)
  }
  var textval = $(this).val();
  getCountryAutocomplete(e, textval, countriesList, callback, flag=true)
});

//retrive domain autocomplete value
function onDomainSuccess(val){
  $("#domainval").val(val[1]);
  $("#domain").val(val[0]);
}
//load domain list in autocomplete textbox
$("#domainval").keyup(function(e){
  function callback(val){
    onDomainSuccess(val)
  }
  var textval = $(this).val();
  getDomainAutocomplete(e, textval, domainsList, callback, flag=true)
});

//retrive unit form autocomplete value
function onUnitSuccess(val){
  $("#unitval").val(val[1]);
  $("#unitid").val(val[0]);
}

//load unit  form list in autocomplete text box
$("#unitval").keyup(function(e){
  var textval = $(this).val();
  //getUnitConditionAutocomplete(textval, unitList, function(val){
  getUnitAutocomplete(e, textval, unitList, function(val){
    onUnitSuccess(val)
  })
});

//retrive statutory autocomplete value
function onStatutorySuccess(val){
  $("#level1val").val(val[1]);
  $("#level1id").val(val[0].replace(/##/gi,'"'));
}
//load statutory list in autocomplete textbox
$("#level1val").keyup(function(e){
  var textval = $(this).val();
  getClientStatutoryAutocomplete(e, textval, level1List, function(val){
    onStatutorySuccess(val)
  })
});

//retrive compliance task form autocomplete value
function onComplianceTaskSuccess(val){
  $("#compliancesval").val(val[1]);
  $("#compliancesid").val(val[0]);
}

//load compliancetask form list in autocomplete text box
$("#compliancesval").keyup(function(e){
  var textval = $(this).val();
  getComplianceTaskAutocomplete(e, textval, compliancesList, function(val){
    onComplianceTaskSuccess(val)
  })
});

//retrive user autocomplete value
function onUserSuccess(val){
  $("#userval").val(val[1]);
  $("#userid").val(val[0]);
}

//load user list in autocomplete text box
$("#userval").keyup(function(e){
  var textval = $(this).val();
  getUserAutocomplete(e, textval, userList, function(val){
    onUserSuccess(val)
  })
});



$(function() {
    initialize();
});
