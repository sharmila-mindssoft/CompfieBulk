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

var sno = 0;
var totalRecord;
var lastBG = '';
var lastLE = '';
var lastDV = '';

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
            lentityid, divisionid, unitid,  domainsVal, 0, 
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

//load unit wwith condition form list in autocomplete text box  
$("#unitval").keyup(function(){
  var textval = $(this).val();
  getUnitConditionAutocomplete(textval, unitList, function(val){
    onUnitSuccess(val)
  })
});


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