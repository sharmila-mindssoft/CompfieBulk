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
var tRecord = 0;


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
        displayMessage(error);
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
    tRecord = 0;
    $(".no-records").html("");
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
    }else{
        complianceid = parseInt(complianceid)
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
        displayMessage(message.country_required);
    }
    else if(domain == ""){
        displayMessage(message.domain_required);
    }
    else if(usertype  == null){
        displayMessage(message.usertype_required);
    }
    else if(fromdate != '' && todate ==''){
        displayMessage(message.todate_required);
    }
    else if(fromdate == '' && todate !=''){
        displayMessage(message.fromdate_required);
    }
    else{
        sno = 0;
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
                var download_url = data["link"];
                window.open(download_url, '_blank');
                // if (error == null){
                    
                // }
                // else {
                //     displayMessage(error);
                // }
            }
        }
        function onFailure(error){
            hideLoader();
            displayMessage(error);
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
    if (fromdate === null )
        fromdate = "Nil";
    $('.fromdate-filter-name', cloneHeading).text(fromdate);
    if (todate === null)
        todate = "Nil";
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
                $('.assigneee', cloneval).html(clist[k1]['assignee_name']);
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

    if(sno >= tRecord){
        $('#accordion').find('.accordion-toggle').click(function(){
            $(this).next().slideToggle('fast');
            $(".accordion-content").not($(this).next()).slideUp('fast');
        });
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

    if(totallist >= pageSize){
        $('#pagination').show();
    }
    else{
        $('#pagination').hide();
    }

}


function loadComplianceActivityReportList(data){

    $(".grid-table-rpt").show();
    $('.table-compliance-activity-list').empty();
    $(".total-records").html("");
    $(".no-records").html("");
    $("#pagination").hide();


    $.each(data, function(key, value) {
        var level1list = data[key]['statutory_wise_compliances'];
        $.each(level1list, function(ke, valu) {
            var list = level1list[ke];
            $.each(list, function(k, val){
                tRecord = tRecord + 1;
            });
        });
    });
    if(tRecord == 0){
        $(".no-records").html("No record Found");
    }
    else{
        loadresult(data);    
    }    
    $(".total-records").html("Total : "+tRecord+" records")
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

//retrive compliance task form autocomplete value
function onComplianceTaskSuccess(val){
  $("#complianceval").val(val[1]);
  $("#complianceid").val(val[0]);
}

//load compliancetask form list in autocomplete text box
$("#complianceval").keyup(function(){
  var textval = $(this).val();
  getComplianceTaskAutocomplete(textval, complianceList, function(val){
    onComplianceTaskSuccess(val)
  })
});

$(function() {
    initialize();
});
