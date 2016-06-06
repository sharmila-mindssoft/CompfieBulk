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
var level1val;
var applicableStatus;
var assignedStatutoryList;

var finalList;
var pageSize = 500;
var startCount = 0;
var endCount;
var sno = 0;
var unitcountid = null;
var fullArrayList = [];

function displayLoader() {
    $(".loading-indicator-spin").show();
}

function hideLoader() {
    $(".loading-indicator-spin").hide();
}

function initialize(){
    function onSuccess(data){
        countriesList = data['countries'];
        businessgroupsList = data['business_groups'];
        divisionsList = data['divisions'];
        domainsList = data['domains'];
        groupList = data['groups'];
        legalEntityList = data['legal_entities'];
        unitList = data['units'];
        level1List = data['level_1_statutories'];
        loadCountries(countriesList);
    }
    function onFailure(error){
        console.log(error);
    }
    mirror.getAssignedStatutoryReportFilters(
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
    var countries = $("#countries").val();
    countriesText = $("#countries  option:selected").text();
    //Domain

    var domain = $("#domain").val();
    if(domain != ''){
        var domainsVal = parseInt(domain);
    }
    else{
        var domainsVal = null;
    }
    var domainName = $("#domainval").val();
    //Groups
    var groups = $("#group-id").val();
    if(groups != ''){
        var groupid = parseInt(groups);
    }
    else{
        var groupid = null;
    }
    groupsval = $("#groupsval").val();

    //Business Groups
    var bgroups = $("#businessgroupid").val();
    businessgroupsval = $("#businessgroupsval").val().trim();
    if(bgroups != ''){
        if(businessgroupsval != ''){
            var businessgroupid = parseInt(bgroups);    
        }
        else{
            var businessgroupid = null;       
        }
        
    }
    else{
     var businessgroupid = null;
    }
    
    //Legal Entity
    var legalentity = $("#legalentityid").val();
     legalentityval = $("#legalentityval").val().trim();
    if(legalentity != ''){
        if( legalentityval != ''){
            var lentityid = parseInt(legalentity);
        }
        else{
            var lentityid = null;       
        }
    }
    else{
        var lentityid = null;
    }
   
    //division
    var division = $("#divisionid").val();
    divisionval = $("#divisionval").val().trim();
    if(division != ''){        
        if( divisionval != ''){
          var divisionid = parseInt(division);
        }
        else{
            var divisionid = null;       
        }
    }
    else{
        var divisionid = null;
    }
    
    //Units
    var units = $("#unitid").val();
    unitval = $("#unitval").val().trim();
    if(units != ''){
        if( unitval != ''){
            var unitid = parseInt(units);
        }
        else{
            var unitid = null;       
        }
    }
    else{
        var unitid = null;
    }
    
    //Level1Statutory
    var level1Statutory = $("#level1id").val();
    level1val = $("#level1val").val().trim();
    if(level1Statutory != ''){
        if( level1val != ''){
            var level1Statutoryid = parseInt(level1Statutory);
        }
        else{
            var level1Statutoryid = null;       
        }
    }
    else{
        var level1Statutoryid = null;
    }
   

    applicableStatus = $("#appliability-status option:selected").val();
    if(applicableStatus == "null"){
        applicableStatus = null;
    }
    if(applicableStatus == 1){
        applicableStatus = true;
    }
    if(applicableStatus == 0){
        applicableStatus = false;
    }
    if(countries == ""){
        displayMessage(message.country_required);
        $(".grid-table-rpt").hide();
    }
    else if(domain == ""){
        displayMessage(message.domain_required);
        $(".grid-table-rpt").hide();
    }
    else if(domainName == ""){
        displayMessage(message.domain_required);
        $(".grid-table-rpt").hide();
    }
    else{
        displayLoader();
        function onSuccess(data){
            fullArrayList = [];
            hideLoader();
            clearMessage();
            sno = 0;
            startCount = 0;
            endCount = 0;
            $(".grid-table-rpt").show();
            $(".countryval").text(countriesText);
            $(".groupsval").text(groupsval);
            $(".domainval").text(domainName);
            $(".bgroupsval").text(businessgroupsval);
            $(".lentityval").text(legalentityval);
            $(".divisionval").text(divisionval);
            loadAssignedStatutoryList(data['unit_wise_assigned_statutories']);

        }
        function onFailure(error){
            hideLoader();
            console.log(error);
        }
        //countryId, domainId,  clientId, businessGroupId, legalEntityId, divisionId, unitId, level1StatutoryId, applicableStatus,
        mirror.getAssignedStatutoryReport(parseInt(countries),  domainsVal,  groupid, businessgroupid,
            lentityid, divisionid, unitid,  level1Statutoryid, applicableStatus,
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
                loadAssignedStatutoriesheading(list[y]);
            }    
            else if(Object.keys(list[y])[0] == "level_1_statutory_id"){
               loadAssignedActdata(list[y]);
            }    
            else if(Object.keys(list[y])[0] == "compliance_applicable_status"){
               loadCompliancedata(list[y]);
            }                
        }        
    }
    //textchangeloadinghide();
}

function loadresult(finalList) {   
    endCount = pageSize;
    $.each(finalList, function(i, val){
        var list = finalList[i];
        var list_assigned = val["assigned_statutories"]
        delete list["assigned_statutories"];         
        fullArrayList.push(list);

        $.each(list_assigned, function(i1, val1){
            var list_ac = list_assigned[i1];
            var list_compliances = val1['compliances'];
            delete list_ac["compliances"];  
            fullArrayList.push(list_ac);
       
            $.each(list_compliances, function(i2, val2){
                var list_c = list_compliances[i2]; 
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
               loadAssignedStatutoriesheading(sub_keys_list[y]);
            }    
            else if(Object.keys(sub_keys_list[y])[0] == "level_1_statutory_id"){
               loadAssignedActdata(sub_keys_list[y]);
            }    
            else if(Object.keys(sub_keys_list[y])[0] == "compliance_applicable_status"){
               loadCompliancedata(sub_keys_list[y]);
            }
        } 
    }
}

function loadAssignedStatutoriesheading(data){
    var gname;
    var bgname;
    var lename;
    var dname;

    value = data;
    var tablefilter = $('#statutory-list .tr-filter');
    var clonefilter = tablefilter.clone();

    $('.groupsval', clonefilter).text(value["group_name"]);
    businessGroup = value["business_group_name"];
    if (businessGroup == null)
        businessGroup = "Nil";
    $('.bgroupsval', clonefilter).text(businessGroup);
    $('.lentityval', clonefilter).text(value["legal_entity_name"]);
    divisionName = value["division_name"];
    if (divisionName == null)
        divisionName = "Nil";
    $('.divisionval', clonefilter).text(divisionName);
    $('.tbody-assigned-statutory-list').append(clonefilter);

    var tableheading = $('#statutory-list .tr-heading');
    var cloneheading = tableheading.clone();
    $('.tbody-assigned-statutory-list').append(cloneheading);

    var tableRow = $('#unit-details-list .table-unit-details-list .tablerow');
    var clone = tableRow.clone();
    var unitNameAddress = value['unit_name']+", "+value['address'];
    $('.unit-name-address', clone).text(unitNameAddress);
    $('.tbody-assigned-statutory-list').append(clone);   

}
function loadCompliancedata(assignedRecord){
    var valu  = assignedRecord;    
    var appStatus = valu['compliance_applicable_status']
    if(appStatus == true){
        asImageName = "<img src='/images/tick1bold.png'>";
    }
    else{
        asImageName = "<img src='/images/deletebold.png'>";
    }
    var optedStatus = valu['compliance_opted_status']
    if(optedStatus == true){
        optedImageName = "<img src='/images/tick-orange.png'>";
    }
    else if(optedStatus == false){
        optedImageName = "<img src='/images/deletebold.png'>";
    }
    else{
        optedImageName = "Nil";
    }
    var remarks = valu['compliance_remarks'];
    if(remarks == null){
        remarks = "Nil";
    }
    sno++;
    var tableRowAssignedRecord = $('#statutory-list .table-statutory-list .tablerow');
    var cloneAssignedRecord = tableRowAssignedRecord.clone();
    $('.sno', cloneAssignedRecord).text(sno);
    $('.statutory-provision', cloneAssignedRecord).text(valu['statutory_provision']);
    $('.compliance-task', cloneAssignedRecord).text(valu['compliance_name']);
    $('.compliance-description', cloneAssignedRecord).text(valu['description']);
    $('.statutory-nature', cloneAssignedRecord).text(valu['statutory_nature']);
    $('.applicability-status', cloneAssignedRecord).html(asImageName);
    $('.opted', cloneAssignedRecord).html(optedImageName);
    $('.remarks', cloneAssignedRecord).text(remarks);
    $('.tbody-assigned-statutory-list').append(cloneAssignedRecord);
    
}
function loadAssignedActdata(assignedList){
    var val = assignedList;
    
    var asImageName;
    var optedImageName;
    var tableRowAssigned = $('#act-heading .table-act-heading-list .tablerow');
    var cloneAssigned = tableRowAssigned.clone();
    var appStatus = val['applicable_status']
    if(appStatus == true){
        asImageName = "<img src='/images/tick1bold.png'>";
    }
    else{
        asImageName = "<img src='/images/deletebold.png'>";
    }
    var optedStatuslevel1 = val['opted_status']

    if(optedStatuslevel1 == true){
        optedImageNamelevel1 = "<img src='/images/tick-orange.png'>";
    }
    else if(optedStatuslevel1 == false){
        optedImageNamelevel1 = "<img src='/images/deletebold.png'>";
    }
    else{
        optedImageNamelevel1 = "Nil";
    }
    var remarks = val['compliance_remarks'];
    if(remarks == null){
        remarks = "Nil";
    }
    $('.heading', cloneAssigned).text(val['level_1_statutory_name']);
    $('.act-applicable', cloneAssigned).html(asImageName);

    $('.act-opted', cloneAssigned).html(optedImageNamelevel1);
    $('.act-remarks', cloneAssigned).text(remarks);
    var assignedRecord = val['compliances'];
    $('.tbody-assigned-statutory-list').append(cloneAssigned);
}

function loadAssignedStatutoryList(data){
    $('.grid-table-rpt').show();
    $("#pagination").hide();
    var totalrecords = 0;
    $('.tbody-assigned-statutory-list tr').remove();
    $.each(data, function(i, val){
        var assignedstat = val['assigned_statutories'];
        $.each(assignedstat, function(i1, val1){
            var reccount = val1['compliances'].length;
            totalrecords = totalrecords + reccount;    
        });       
    });    
    loadresult(data);    
    $(".total-records").html("Total : "+totalrecords+" records");
}

//Countries---------------------------------------------------------------------------------------------------------------
function loadCountries(countriesList){
    $.each(countriesList, function(key, values){
        var countryId = values['country_id'];
        var countryName = values['country_name'];
        $('#countries').append($('<option value="'+countryId+'">'+countryName+'</option>'));
    });
}


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

//retrive group form autocomplete value
function onGroupSuccess(val){
  $("#groupsval").val(val[1]);
  $("#group-id").val(val[0]);
}

//load group form list in autocomplete text box  
$("#groupsval").keyup(function(){
  var textval = $(this).val();
  getGroupAutocomplete(textval, groupList, function(val){
    onGroupSuccess(val)
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
  getBusinessGroupAutocomplete(textval, businessgroupsList, function(val){
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
  getLegalEntityAutocomplete(textval, legalEntityList, function(val){
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
  getDivisionAutocomplete(textval, divisionsList, function(val){
    onDivisionSuccess(val)
  })
});

//retrive unit with condition form autocomplete value
function onUnitSuccess(val){
  $("#unitval").val(val[1]);
  $("#unitid").val(val[0]);
}

//load unit with conditionform list in autocomplete text box  
$("#unitval").keyup(function(){
  var textval = $(this).val();
  //getUnitConditionAutocomplete(textval, unitList, function(val){
  getUnitAutocomplete(textval, unitList, function(val){
    onUnitSuccess(val)
  })
});

//retrive statutory autocomplete value
function onStatutorySuccess(val){
  $("#level1val").val(val[1]);
  $("#level1id").val(val[0]);
}
//load statutory list in autocomplete textbox  
$("#level1val").keyup(function(){
  var textval = $(this).val();
  getStatutoryAutocomplete(textval, level1List[$("#countries").val()][$("#domain").val()], function(val){
    onStatutorySuccess(val)
  })
});

$(function() {
    // $( "#accordion" ).accordion({
    //  heightStyle: "content"
    // });
    initialize();
});

