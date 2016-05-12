var countriesList;
var domainsList;
var businessgroupsList;
var legalEntityList;
var divisionsList;
var unitList;
var level1List;
var applicableStatusList;
var countriesText;
var domainText;
var businessGroupText;
var legalentityText;
var divisionText;

var pageSize = 500;
var startCount = 0;
var endCount;
var sno = 0;
var fullArrayList = [];
var totalrecords = 0;

var laststatus = '';
var lastcountry = '';
var lastdomain = '';
var lastbg = '';
var lastle = '';
var lastdivision = '';
var lastlevel1 = '';

var countries = null;
var domian = null;
var businessgroupid = null;
var legalentityid = null; 
var divisionid = null;
var unitid = null;
var level1id = null;
var appstatus = null;
var csv = false;

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
        businessgroupsList = data['business_groups'];
        legalEntityList = data['legal_entities'];
        divisionsList = data['divisions'];
        unitList = data['units'];
        level1List = data['level_1_statutories'];
        applicableStatusList = data['applicable_status'];
        loadApplicableStatus(applicableStatusList);
    }
    function onFailure(error){
        console.log(error);
    }
    client_mirror.getTaskApplicabilityReportFilters(
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
    loadcompliancetaskapplicabilityreport("show");
});
$("#export-button").click(function(){
    loadcompliancetaskapplicabilityreport("export");
});
function loadcompliancetaskapplicabilityreport(buttontype){
    console.log("load===="+buttontype);
    countries = $("#country").val();
    countriesText = $("#countryval").val();
    //Domain
    domain = $("#domain").val();
    domainText = $("#domainval").val();
    //business_groups
    businessgroupText = $("#businessgroupsval").val();
    businessgroupid = $("#businessgroupid").val();
    if(businessgroupid == ''){
        businessgroupid = null;
    }
    else{
        businessgroupid = parseInt(businessgroupid);
    }
    //Legal Entity
    legalentityText = $("#legalentityval").val();
    legalentityid = $("#legalentityid").val();
    if(legalentityid == ''){
        legalentityid = null;
    }
    else{
        legalentityid = parseInt(legalentityid);
    }
    //Divisions
    divisionText = $("#divisionval").val();
    divisionid = $("#divisionid").val();
    if(divisionid == ''){
        divisionid = null;
    }
    else{
        divisionid = parseInt(divisionid);
    }
    //Unit
    unitid = $("#unitid").val();
    if(unitid == ''){
        unitid = null;
    }
    else{
        unitid = parseInt(unitid);
    }
    //Level 1 Statutories
    level1id = $("#level1id").val();
    if(level1id == ''){
        level1id = null;
    }
    else{
        level1id = level1id;
    }
    appstatus = $("#applicable-status").val();
    if(countries == ""){
        displayMessage(message.country_required);
    }
    else if(domain == ""){
        displayMessage(message.domain_required);
    }
    else{
        console.log("else part");
        var csv = false;
        if(buttontype == "export"){
            csv = true;
        }
        function onSuccess(data){
            $(".grid-table-rpt").show();
            sno = 0;
            fullArrayList = [];
            $('.tbody-task-applicability-list tr').remove();
            if(buttontype == "export"){
                var download_url = data["link"];
                window.open(download_url, '_blank');
            }else{
                console.log("success");
                loadTaskApplicabilityStatusList(data);
            }
        }
        function onFailure(error){
            console.log(error);
        }

        client_mirror.getTaskApplicabilityReportData(
            parseInt(countries), parseInt(domain), businessgroupid,
            legalentityid, divisionid, unitid, level1id, appstatus, csv, sno,
            function (error, response){
                if(error == null){
                    console.log("response success")
                    onSuccess(response);
                }
                else{
                    onFailure(error);
                }
            }
        );
    }
}
function loadTaskApplicabilityStatusList(data1){
    //$("#pagination").hide();
    console.log("welcome");
    applicable = $("#applicable-status").val();
    var data = {}
    if (applicable == "Applicable")
        data["Applicable"] = data1["applicable"];
    else if (applicable == "Not Applicable")
        data["Not Applicable"] = data1["not_applicable"];
    else if (applicable == "Not Opted")
        data["Not Opted"] = data1["not_opted"];

    $.each(data, function(key, value) {
        var grouplist = data[key];
        for(var k=0; k<value.length; k++){
            var actwiselist = value[k]["actwise_units"];
            $.each(actwiselist, function(k1, v1) {
                $.each(v1, function(ke, valu) {
                    totalrecords += valu["compliances"].length;
                });
            });
        } 
    });
    loadresult(data);
    $(".total-records").html("Total : "+totalrecords+" records");
}



function get_sub_array(object, start, end){
    if(!end){ end = -1;}
    return object.slice(start, end);
}

$('#pagination').click(function(e){
    console.log("pagination");
    displayLoader();
    fullArrayList = [];
    clearMessage();

    function onSuccess(data){
        loadTaskApplicabilityStatusList(data);
        totalRecord = data["total_count"];
        hideLoader();
    }
    function onFailure(error){
        onFailure(error);
        hideLoader();
    }

    client_mirror.getTaskApplicabilityReportData(
        parseInt(countries), parseInt(domain), businessgroupid,
        legalentityid, divisionid, unitid, level1id, appstatus,  csv, sno,
        function (error, response){
            if(error == null){
                onSuccess(response);
            }
            else{
                onFailure(error);
            }
        }
    );
});


        // $(".loading-indicator-spin").show();
        // if($('.loading-indicator-spin').css('display') != 'none')
        // {
        //     setTimeout(function(){
        //         showloadrecord();
        //     }, 500);

        // }
        // setTimeout(function(){
        //     $(".loading-indicator-spin").hide();
        // }, 500);




// function showloadrecord() {
//     startCount = endCount;
//     endCount = startCount + pageSize;

//     var list = get_sub_array(fullArrayList, startCount, endCount);
//     if(list.length < pageSize){
//         $('#pagination').hide();
//     }
//     for(var y = 0;  y < pageSize; y++){
//         if(list[y] !=  undefined){
//             if(list[y] == "Applicable" ||  list[y] == "Not Applicable" || list[y] == "Not Opted" ){
//                applicablestatus(list[y]);
//             }
//             else if(Object.keys(list[y])[0] == "compliance_frequency"){
//                compliancelist(list[y]);
//             } 
//             else if(Object.keys(list[y])[0] == "division_name"){
//                filterheading(list[y]);
//             }
//             else{ 
//                level1heading(list[y]);
//             }
//         }
//     }
// }

function loadresult(finalList) {
    fullArrayList = [];
     $.each(finalList, function(i, val){
        fullArrayList.push(i);
        $.each(val, function(i1, val1){
            var grouplist = val1;
            var list_act = val1["actwise_units"];
            //delete grouplist["actwise_units"];
            fullArrayList.push(grouplist);
            $.each(list_act, function (i_act, val_act){
                var actval = i_act;
                var list_unit = val_act;
                delete val_act;
                fullArrayList.push(actval);
                $.each(list_unit, function(i_unit, val_unit){
                    var list_comp = val_unit['compliances'];
                    $.each(list_comp, function(i_com, val_com){
                        jQuery.extend(val_com, {'unit_name': val_unit['unit_name'], 'address': val_unit['address']});
                        fullArrayList.push(val_com);
                    });
                });
            });
        });
    });
     var totallist = fullArrayList.length;
     for (var k = 0 ; k < totallist; k++){
         splitwisedisplay(fullArrayList[k]);
     }

    // if(totallist > pageSize){
    //     $('#pagination').show();
    // }
    // else{
    //     $('#pagination').hide();
    // }
    //var sub_keys_list = get_sub_array(fullArrayList, startCount, endCount);

    
}
function splitwisedisplay(sub_keys_list){
    //console.log(sub_keys_list);
    if(sub_keys_list !=  undefined){
        if(sub_keys_list == "Applicable" ||  sub_keys_list == "Not Applicable" || sub_keys_list == "Not Opted" ){
           applicablestatus(sub_keys_list);
        }
        else if(Object.keys(sub_keys_list)[0] == "compliance_frequency"){
           compliancelist(sub_keys_list);
        } 
        else if(Object.keys(sub_keys_list)[0] == "division_name"){
           filterheading(sub_keys_list);
        }
        else{ 
           level1heading(sub_keys_list);
        }
    }

}

function filterheading(data){

    var bg = '-';
    if(data["business_group_name"] != null) bg = data["business_group_name"];
    var dv = '-';
    if( data["division_name"] != null) dv = data["division_name"];
    var le = data["legal_entity_name"];
    console.log(lastbg+"--"+bg);
    console.log(lastle+"--"+le);
    console.log(lastdivision+"--"+dv);

    if(lastbg !=  bg || lastle != le || lastdivision != dv){
        lastbg = bg;
        lastle = le;
        lastdivision =  dv;

        var tableFilterHeading = $('#templates .table-task-applicability-list .filter-task-applicability-list');
        var clonefilterHeading = tableFilterHeading.clone();
        $('.filter-country', clonefilterHeading).text(countriesText);
        $('.filter-domain', clonefilterHeading).text(domainText);

        $('.filter-businessgroup', clonefilterHeading).text(data["business_group_name"]);
        $('.filter-legalentity', clonefilterHeading).text(data["legal_entity_name"]);
        $('.filter-division', clonefilterHeading).text(data["division_name"]);
        $('.tbody-task-applicability-list').append(clonefilterHeading);

    }
}
function applicablestatus(key){
    //console.log(laststatus+"--"+key);
    if(laststatus != key){
        laststatus = key;
        count = 0;
        var tableRowHeading = $('#templates .table-task-applicability-list .applicable-status-list');
        var cloneHeading = tableRowHeading.clone();
        $('.applicable-status-heading', cloneHeading).text(key);
        $('.tbody-task-applicability-list').append(cloneHeading);    
    }    
}
function level1heading(ke){
    if(lastlevel1 != ke){
        lastlevel1 = ke;
        var arr = [];
        var tableRowLevel1 = $('#templates .table-task-applicability-list .level1-list');
        var cloneLevel1 = tableRowLevel1.clone();
        $('.level1-heading', cloneLevel1).text(ke);
        $('.tbody-task-applicability-list').append(cloneLevel1);
        var tableRowList = $('#templates .table-task-applicability-list .list-heading');
        var cloneList = tableRowList.clone();
        $('.tbody-task-applicability-list').append(cloneList);    
    }
    
}
function compliancelist(data){
    var valcomp = data;
    var tableRow = $('#templates .table-task-applicability-list .task-list');
    var clone = tableRow.clone();
    sno = sno + 1;
    $('.sno', clone).text(sno);
    $('.statutory-provision', clone).html(valcomp['statutory_provision']);
    $('.unit span', clone).html(valcomp["unit_name"]);
    $('.unit abbr', clone).attr("title", valcomp["address"]);
    if(valcomp['compliance_name'][1] != undefined){
        $('.compliance-task a', clone).html(valcomp['compliance_name'][0]);
        $('.compliance-task a', clone).attr("href",valcomp['compliance_name'][1]);
        $('.compliance-task a', clone).attr('target','_blank');
    }else{
        $('.compliance-task', clone).html(valcomp['compliance_name'][0]);
    }
    $('.compliance-description', clone).html(valcomp['description']);
    $('.penal-consequences', clone).html(valcomp['penal_consequences']);
    $('.compliance-frequency', clone).html(valcomp['compliance_frequency']);
    $('.repeats', clone).html(valcomp['repeats']);
    $('.tbody-task-applicability-list').append(clone);
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
  getUnitAutocomplete(textval, unitList, function(val){
    onUnitSuccess(val)
  })
});

//retrive statutory autocomplete value
function onStatutorySuccess(value){
  $("#level1val").val(value[1]);
  $("#level1id").val(value[0]);
}
//load statutory list in autocomplete textbox
$("#level1val").keyup(function(){
  var textval = $(this).val();
  getClientStatutoryAutocomplete(textval, level1List, function(val){
    onStatutorySuccess(val)
  })
});

function loadApplicableStatus(list){
  for(var k = 0; k < list.length; k++){
    $('#applicable-status').append($('<option value="'+list[k]+'">'+list[k]+'</option>'));
  }
}
$(function() {
    initialize();
});

$( document ).tooltip({
    position: {
        my: "center bottom-20",
        at: "center top",
        using: function( position, feedback ) {
            $( this ).css( position );
            $( "<div>" )
                .addClass( "arrow" )
                .addClass( feedback.vertical )
                .addClass( feedback.horizontal )
                .appendTo( this );
        }
    }
});