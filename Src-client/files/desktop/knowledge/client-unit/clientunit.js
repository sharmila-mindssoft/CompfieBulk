var groupList;
var countryList;
var domainList;
var businessGroupList;
var legalEntitiesList;
var divisionList;
var countryFulList;
var countc = 0;
var industryList;
var unitList;
var geographyList;
var geographyLevelList;
var unitcodecount = 1001;
var countryByCount = 1;
var lastClassval = 1;
var unitcodeautogenerateids = null;
var get2CharsofGroup = null;
var max = {};
var auto_generate_initial_value = null

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
        groupList = data['group_companies'];
        console.log("group list inside initialize"+groupList)
        console.log("client_id")
        businessGroupList = data['business_groups'];
        legalEntitiesList = data['legal_entities'];
        divisionList = data['divisions'];
        countryFulList = data['countries'];
        geographyLevelList = data['geography_levels'];      
        geographyList = data['geographies'];
        industryList = data['industries'];
        domainList = data['domains'];
        unitList = data['units'];
        loadClientsList(data);
    }
    function onFailure(error){
        displayMessage(error);
    }
    mirror.getClients(
        function(error, response){
            if(error == null){
                onSuccess(response);
            }
            else{
                onFailure(error);
            }
        }
    );
}
function getGroupName(groupId){
    var groupName;
    $.each(groupList, function(key, value){
        if(value['client_id'] == groupId){
            groupName = value['group_name'];
        }
    });
    return groupName;
}
function getBusinessGroupName(businessGroupId){
    var businessgroupName;
    $.each(businessGroupList, function(key, value){
        if(value['business_group_id'] == businessGroupId){
            businessgroupName = value['business_group_name'];
        }
    });
    return businessgroupName;   
}
function getLegalEntityName(legalentityId){
    var legalEntityName;
    $.each(legalEntitiesList, function(key, value){
        if(value['legal_entity_id'] == legalentityId){
            legalEntityName = value['legal_entity_name'];
        }
    });
    return legalEntityName; 
}
function getDivisionName(divisionId){
    var divisionName;
    $.each(divisionList, function(key, value){
        if(value['division_id'] == divisionId){
            divisionName = value['division_name'];
        }
    });
    return divisionName;
}
function getCountryName(countryId){
    var countryName;
    $.each(countryFulList, function(key, value){
        if(value['country_id'] == countryId){
            countryName = value['country_name'];
        }
    });
    return countryName;
}
function getIndustryName(industryId){
    var industryName;
    $.each(industryList, function(key, value){
        if(value['country_id'] == industryId){
            industryName = value['industry_name'];
        }
    });
    return industryName;
}
function getGeographyLevels(countryId, levelId){
    var geographyLevelName;
    var geoLevelListByCountry = geographyLevelList[countryId];
    $.each(geoLevelListByCountry, function(key, value){
        if(value['level_id'] ==  levelId){
            geographyLevelName = value['level_name'];
        }
    });
    return geographyLevelName;
}


//Load Get Client List -----------------------------------------------------------------------------------------
function loadClientsList(clientunitsList){
    $(".tbody-clientunit-list").find("tr").remove();
    var sno = 0;
    var imageName, title;
    var getAllArrayValues = [];
    for(var i=0; i<groupList.length; i++){
        max[groupList[i]["client_id"]] = groupList[i]["no_of_units"];
    }
    console.log(max);
    $.each(unitList, function (key, value){
        var isActive = unitList[key]['is_active'];  
        var unitId = unitList[key]['unit_id'];
        var unitVal = {};
        clientId = unitList[key]['client_id'];
        bgroupId = unitList[key]['business_group_id'];
        lentitiesId = unitList[key]['legal_entity_id'];
        divisionId = unitList[key]['division_id'];
        if(isActive == true){
            imageName = "icon-active.png";
            title = "Click here to deactivate"
            statusVal = false;
        }
        else{
            imageName = "icon-inactive.png";  
            title = "Click here to Activate"
            statusVal = true;
        }
        var tableRow = $('#templates .table-clientunit-list .table-row');
        var clone = tableRow.clone();
        sno = sno + 1;
        $('.sno', clone).text(sno);
        $('.group-name', clone).text(getGroupName(clientId));
        $('.business-group-name', clone).text(getBusinessGroupName(bgroupId));
        $('.legal-entity-name', clone).text(getLegalEntityName(lentitiesId)); 
        $('.division-name', clone).text(getDivisionName(divisionId));
        $('.edit', clone).html('<img src = "/images/icon-edit.png" id = "editid" onclick = "clientunit_edit('+clientId+','+bgroupId+','+lentitiesId+','+divisionId+')"/>');
        // $('.is-active', clone).html('<img src = "/images/'+imageName+'" title = "'+title+'" onclick = "clientunit_active('+clientId+','+lentitiesId+', '+divisionId+', '+statusVal+')"/>');
        $('.tbody-clientunit-list').append(clone);  
    });
}
//Add Button-------------------------------------------------------------------------------------------------
$("#btn-clientunit-add").click(function(){
    $("#clientunit-add").show();
    $("#clientunit-view").hide();
    $("#client-unit-id").val('');
    $(".unit-error-msg").val('');
    countryByCount = 1;
    countc = 0;
    clearMessage();
    var x = document.getElementsByTagName("input");
    for(i = 0; i <= x.length-1; i++){
        if(x.item(i).type!="submit" ){ x.item(i).value = ""; }
    }
    var y = document.getElementsByTagName("select");
    for(i = 0; i <= y.length-1; i++){
        y.item(i).value = ""; 
    }
    $('#group-select:gt(0)').empty();
    $('#businessgroup-select:gt(0)').empty();
    $('#entity-select:gt(0)').empty();
    $('#division-select:gt(0)').empty();
    $('.industry').empty();
    $('.add-country-unit-list').empty();
    divisionExistingChecking('Cancel');
    legalEntityExistingChecking('Cancel');
    businessGroupExistingChecking('Cancel');
    loadClientGroups(groupList);
    $(".no-of-units").val('');
});

//Cancel Button ----------------------------------------------------------------------------------------------
$("#btn-clientunit-cancel").click(function(){
    $("#clientunit-add").hide();
    $("#clientunit-view").show();
});

//Load All Groups---------------------------------------------------------------------------------------------
function loadClientGroups(groupsList){
    $('#group-select').find('option:gt(0)').remove();
    $.each(groupsList, function(key, value) {
        var groupId = value['client_id'];
        var groupName = value['group_name'];
        if(value['is_active'] == true){
            $('#group-select').append($('<option value = "'+groupId+'">'+groupName+'</option>'));   
        }       
    });
}

//Load Business Groups  ---------------------------------------------------------------------------------------------
function loadBusinessGroups() {
    var groupId = $("#group-select").val();
    $('#businessgroup-select').find('option:gt(0)').remove();
    for (var i in businessGroupList){
        if(businessGroupList[i]['client_id'] == groupId){
            var bgroupId = businessGroupList[i]['business_group_id'];
            var bgroupName = businessGroupList[i]['business_group_name'];
            $('#businessgroup-select').append($('<option value = "'+bgroupId+'">'+bgroupName+'</option>'));
        }
    }
    $('#entity-select').find('option:gt(0)').remove();  
    for (var i in legalEntitiesList){
        if(legalEntitiesList[i]['client_id'] == groupId){
            var lentityId = legalEntitiesList[i]['legal_entity_id'];
            var lentityName = legalEntitiesList[i]['legal_entity_name'];
            $('#entity-select').append($('<option value = "'+lentityId+'">'+lentityName+'</option>'));
        }
    }
}
//Load LegalEntities ---------------------------------------------------------------------------------------------
function loadLegalEntity() {
    var clientId = $("#group-select").val();
    var businessGroupId = $("#businessgroup-select").val();
    if(businessGroupId == ''){
        businessGroupId = null;
    }
    if(businessGroupId != null){
        $('#entity-select').find('option:gt(0)').remove();
        for (var i in legalEntitiesList){
            if(legalEntitiesList[i]['business_group_id'] == businessGroupId){
                var lentityId = legalEntitiesList[i]['legal_entity_id'];
                var lentityName = legalEntitiesList[i]['legal_entity_name'];
                $('#entity-select').append($('<option value = "'+lentityId+'">'+lentityName+'</option>'));
            }
        }   
    }
    if(businessGroupId == null){
        $('#entity-select').find('option:gt(0)').remove();
        for (var i in legalEntitiesList){
            if(legalEntitiesList[i]['client_id'] == clientId && legalEntitiesList[i]['business_group_id'] == null){
                var lentityId = legalEntitiesList[i]['legal_entity_id'];
                var lentityName = legalEntitiesList[i]['legal_entity_name'];
                $('#entity-select').append($('<option value = "'+lentityId+'">'+lentityName+'</option>'));
            }
        }   
    }   
}

//Load Divisions ---------------------------------------------------------------------------------------------
function loadDivision() {
    var lentityId = $("#entity-select").val();
    $('#division-select').find('option:gt(0)').remove();
    for (var i in divisionList){
        if(divisionList[i]['legal_entity_id'] == lentityId){
            var divisionId = divisionList[i]['division_id'];
            var divisionName = divisionList[i]['division_name'];
            $('#division-select').append($('<option value = "'+divisionId+'">'+divisionName+'</option>'));
        }
    }
}
function loadIndustry(className){
    $.each(industryList, function(key, value){
        $('.'+className).append(
            $('<option value="'+industryList[key]['industry_id']+'">'+industryList[key]['industry_name']+'</option>')
        );      
    })
}

function loadupdateunitlocation(cid, gid){
    var units = {};
    $.each(geographyList, function(key, val){
        if(key == cid){
            $.each(val, function(k, v){
                if(v['geography_id'] == gid){
                    units['gname'] = v['geography_name'];
                    units['mapping'] = v['mapping'];
                    units['level_id'] = v['level_id'];
                }
            });
        }
    });
    return units;
}


//Add Country Wise List ----------------------------------------------------------------------------------------
function addcountryrow(){
    var countryIds;
    var groupId = $("#group-select").val();
    if($("#entity-text").val().length == 0){
        var legalEntityValue = $("#entity-select").val();   
    }
    else{
        var legalEntityValue = $("#entity-text").val();     
    }   
    if(groupId == ''){
        displayMessage("Select Group");
    }
    else if(legalEntityValue == ''){
        displayMessage('Select Existing Legal Entity or Create New');
    }
    else{
        clearMessage();
        for (var i in groupList){
            if(groupList[i]['client_id'] == groupId){ countryIds = groupList[i]['country_ids'];
            }
        }
        var countryArray = [];      
        var countryCount = countryIds.length;       
        if(countryCount > countc){          
            var divCountryAddRow = $('#templates .grid-table');
            var clone = divCountryAddRow.clone();   
            $('.btable', clone).addClass('table-'+countryByCount);
            $('.countryval', clone).addClass('countryval-'+countryByCount);
            $('.country', clone).addClass('country-'+countryByCount);
            $('.autocompleteview', clone).addClass('autocompleteview-'+countryByCount);
            $('.ulist-text', clone).addClass('ulist-text-'+countryByCount);         
            $('.geography-levels', clone).addClass('glevel-'+countryByCount+'-'+1);
            $('.unit-location', clone).addClass('unitlocation-'+countryByCount+'-'+1);
            $('.unit-location-ids', clone).addClass('unitlocation-ids-'+countryByCount+'-'+1);
            $('.auto-complete-unit-location', clone).addClass('auto-complete-unit-location-'+countryByCount+'-'+1);
            $('.unitlocationlist-text', clone).addClass('unitlocationlist-text-'+countryByCount+'-'+1);
            $('.full-location-list', clone).addClass('full-location-list-'+countryByCount+'-'+1);
            //$('.unitcode-checkbox', clone).addClass('unitcode-checkbox-'+countryByCount);                        
            $('.unit-code', clone).addClass('unit-code-'+countryByCount);
            $('.unit-code', clone).addClass('unit-code-'+countryByCount+'-'+1);
            $('.unit-name', clone).addClass('unit-name-'+countryByCount+'-'+1);
            $('.industry', clone).addClass('industry-'+countryByCount+'-'+1);
            $('.unit-address', clone).addClass('unit-address-'+countryByCount+'-'+1);
            $('.postal-code', clone).addClass('postal-code-'+countryByCount+'-'+1);
            $('.domain-list', clone).addClass('domain-list-'+countryByCount+'-'+1);
            $('.domainselected', clone).addClass('domainselected-'+countryByCount+'-'+1);
            $('.domain', clone).addClass('domain-'+countryByCount+'-'+1);
            $('.domain-selectbox-view', clone).addClass('domain-selectbox-view-'+countryByCount+'-'+1);
            $('.ul-domain-list', clone).addClass('ul-domain-list-'+countryByCount+'-'+1);       
            $('.add-unit-row img', clone).addClass('table-addunit-'+countryByCount);
            $('.tbody-unit-list', clone).addClass('tbody-unit-'+countryByCount);
            $('.no-of-units', clone).addClass('no-of-units-'+countryByCount);
            $('.activedclass', clone).addClass('activedclass-'+countryByCount+'-'+1);
            
            $('#unitcount').val(1);
            $('.unit-error-msg', clone).addClass('unit-error-msg-'+countryByCount);
            $('.add-country-unit-list').append(clone);  
            $('.no-of-units-'+countryByCount).val(1);
            $('.activedclass-'+countryByCount+'-'+1).text("active");
            // if(countryByCount != 1){
            //     $('.unitcode-checkbox-'+countryByCount).hide();  
            // }  
            countc++;
            countryByCount++;
            $(".postal-code", clone).on('input', function (event) {
                this.value = this.value.replace(/[^0-9]/g, '');
            });
            
            // if($('.unitcode-checkbox').is(':checked')){
            //     $('.unit-code-'+countryByCount+'-'+1).val(get2CharsofGroup+unitcodeautogenerateids);
            //     unitcodeautogenerateids++;
            // }
        }
        if(countryCount <= countc){
            displayMessage("Exceeds Maximum Number of Countries");
        }

    }
}
//Add Unit for individual Rows---------------------------------------------------------------------------------
function addNewUnitRow(str){
    var tableclassname = $(str).parents('table').attr('class');
    var tableclass = tableclassname.split(" ");
    var countval = tableclass[1].split("-").pop();
    var tbodyclassname = $('.'+tableclass[1]).find('tbody:eq(1)').attr('class');
    var tbodyclasses = tbodyclassname.split(" ");
    var lastclassname = $('.'+tbodyclasses[1]).find('tr:last .geography-levels').attr('class');
    var lastClass = lastclassname.split(' ').pop();
    var lastClassval = parseInt(lastClass.split('-').pop());
    var divUnitAddRow = $('#templatesUnitRow .table-UnitRow-list .table-row');
    var clone1 = divUnitAddRow.clone(); 
    $('.geography-levels', clone1).addClass('glevel-'+countval+'-'+(lastClassval+1));
    $('.unit-location', clone1).addClass('unitlocation-'+countval+'-'+(lastClassval+1));
    $('.unit-location-ids', clone1).addClass('unitlocation-ids-'+countval+'-'+(lastClassval+1));
    $('.auto-complete-unit-location', clone1).addClass('auto-complete-unit-location-'+countval+'-'+(lastClassval+1));
    $('.unitlocationlist-text', clone1).addClass('unitlocationlist-text-'+countval+'-'+(lastClassval+1));
    $('.full-location-list', clone1).addClass('full-location-list-'+countval+'-'+(lastClassval+1));
    $('.unit-code', clone1).addClass('unit-code-'+countval);
    $('.unit-code', clone1).addClass('unit-code-'+countval+'-'+(lastClassval+1));
    $('.unit-name', clone1).addClass('unit-name-'+countval+'-'+(lastClassval+1));
    $('.industry', clone1).addClass('industry-'+countval+'-'+(lastClassval+1));
    $('.unit-address', clone1).addClass('unit-address-'+countval+'-'+(lastClassval+1));
    $('.postal-code', clone1).addClass('postal-code-'+countval+'-'+(lastClassval+1));
    $('.domain-list', clone1).addClass('domain-list-'+countval+'-'+(lastClassval+1));
    $('.domainselected', clone1).addClass('domainselected-'+countval+'-'+(lastClassval+1));
    $('.domain', clone1).addClass('domain-'+countval+'-'+(lastClassval+1));
    $('.domain-selectbox-view', clone1).addClass('domain-selectbox-view-'+countval+'-'+(lastClassval+1));
    $('.ul-domain-list', clone1).addClass('ul-domain-list-'+countval+'-'+(lastClassval+1));
    $('.no-of-units-'+countval).val(parseInt($('.no-of-units-'+countval).val())+1);
    $('.activedclass', clone1).addClass('activedclass-'+countval+'-'+(lastClassval+1));
    $('.'+tbodyclasses[1]).append(clone1);
    // if($('.unitcode-checkbox').is(':checked')){
    //     $('.unit-code-'+countval+'-'+(lastClassval+1)).val(get2CharsofGroup+unitcodeautogenerateids);
    //     unitcodeautogenerateids++;
    // }
    $('.activedclass-'+countval+'-'+(lastClassval+1)).text("active");
    $(".postal-code", clone1).on('input', function (event) {
        this.value = this.value.replace(/[^0-9]/g, '');
    });

}
function autoGenerateUnitCode(){
    client_id = $("#group-select").val()
    console.log(max[client_id])
    auto_generate_initial_value = max[client_id]
    unitcodeautogenerateids = (auto_generate_initial_value+1) + 10000; 
    var sno = [];
    if($('.unitcode-checkbox').is(':checked')){
        console.log("checked");
        var groupname = $.trim($("#group-select :Selected").text());   
        get2CharsofGroup = groupname.slice(0, 2);  
        //var numItems = $('.unit-code').length;
        var flag = 0;
        $(".unit-code").each(function(i){
            if ($(this).val() == "")
                flag++;
        });
        for (var i = 0; i < flag; i++){
            sno.push(get2CharsofGroup+unitcodeautogenerateids);
            unitcodeautogenerateids++;
        }   
        $(".unit-code").each(function(i){
            $(this).val(sno[i]);
            $(this).attr("readonly", "readonly");
        });
    }
    else{
        $('.unit-code').val('');
        $(".unit-code").removeAttr("readonly"); 
    }
}

// function autoGenerateUnitCode(classval){
//     var className = classval.split(' ');
//     var groupId = $("#group-select :selected").val();
//     var groupname = $.trim($("#group-select :Selected").text());    
//     var get3Chars = groupname.slice(0, 3);  
//     var getLastNumber = className[1].split('-').pop();
//     var countryname = $('.country-'+getLastNumber).val();
//     var totUnitcode = $('.unit-code-'+getLastNumber).length
//     if($('.'+className[1]).prop("checked") == true){
//         for(var i = 1;i <= totUnitcode; i++){
//             $('.unit-code-'+getLastNumber+'-'+i).val(get3Chars+unitcodecount);  
//             unitcodecount++;
//         }       
//     }
//     if($('.'+className[1]).prop("checked") == false){
//         $('.unit-code-'+getLastNumber).val('');
//     }

// }
function loadglevelsupdate(countryid, lastClass){
    if(countryid == ''){
        displayMessage('Enter Country');
    }    
    else{
        $('.'+lastClass).empty();
        for(var glevel in geographyLevelList[countryid]){
            var glevellist = geographyLevelList[countryid][glevel];
            $('.'+lastClass).append($('<option value = "'+glevellist['level_id']+'">'+glevellist['level_name']+'</option>'));
        }   
    }
}

//Load Geography Levels -------------------------------------------------------------------------------------------
function loadglevels(classval){
    var lastClass = classval.split(' ').pop();
    var checkval = lastClass.split('-');    
    var countryvalue = $('.countryval-'+checkval[1]).val();
    var countryid = $('.country-'+checkval[1]).val();
    
    if(countryvalue == ''){
        displayMessage('Enter Country');
    }
    
    else{
        $('.'+lastClass).empty();
        for(var glevel in geographyLevelList[countryid]){
            var glevellist = geographyLevelList[countryid][glevel];
            $('.'+lastClass).append($('<option value = "'+glevellist['level_id']+'">'+glevellist['level_name']+'</option>'));
        }   
    }
}

//load industry type--------------------------------------------------------------------------------------------------
function industrytype(classval){
    var lastClass = classval.split(' ').pop();
    var checkval = lastClass.split('-');
    $('.'+lastClass).empty();
    for(var industry in industryList){
        $('.'+lastClass).append(
            $('<option value = "'+industryList[industry]['industry_id']+'">'+industryList[industry]['industry_name']+'</option>')
        );
    }
}

//Edit client Unit -----------------------------------------------------------------------------------------------
function clientunit_edit(clientunitId, businessgroupId, legalentityId, divisionId){
    $("#clientunit-view").hide();   
    $("#clientunit-add").show();
    $("#businessgroup-text").hide();
    $("#businessgroup-select").show();
    $("#businessgroup-new").show();
    $("#businessgroup-existing").hide();
    $("#entity-text").hide();
    $("#entity-select").show();
    $("#entity-new").show();
    $("#entity-existing").hide();
    $("#division-text").hide();
    $("#division-select").show();
    $("#division-new").show();
    $("#division-existing").hide();
    $(".no-of-units").val('');

    var x = document.getElementsByTagName("input");
        for(i = 0; i <= x.length-1; i++){
        if(x.item(i).type != "submit" ){ x.item(i).value = ""; }
    }
    $('#group-select:gt(0)').empty();
    $('#businessgroup-select:gt(0)').empty();
    $('#entity-select:gt(0)').empty();
    $('#division-select:gt(0)').empty();
    $('.industry:gt(0)').empty();
    function onSuccess(data) {
        loadFormListUpdate(clientunitId, businessgroupId, legalentityId, divisionId);
    }
    function onFailure(error) {
        console.log(status);
    }
    mirror.getClients(
        function(error, response){
            if(error == null){
                onSuccess(response);
            }
            else{
                onFailure(error);
            }
        }
    );
}
//Update load form cal------------------------------------------------------------------------------------------
function loadFormListUpdate(clientunitId, businessgroupId, legalEntityId, divisionId){
    countryByCount = 1;
    $("#client-unit-id").val(clientunitId);
    $(".add-country-unit-list").empty();
    //group
    loadClientGroups(groupList);
    $('#group-select option[value = '+clientunitId+']').attr('selected','selected');
    //businessgroup
    if(businessgroupId != ''){
        loadBusinessGroups(clientunitId);
        $('#businessgroup-select option[value = '+businessgroupId+']').attr('selected','selected'); 
    }
    if(businessgroupId != null){
        $('#businessgroup-select').append($('<option value = "">select</option>'));
    }   
    //legalentity
    loadLegalEntity(clientunitId, businessgroupId);
    $('#entity-select option[value = '+legalEntityId+']').attr('selected','selected');
    //Division 
    if(divisionId != ''){
        loadDivision(legalEntityId);
        $('#division-select option[value = '+divisionId+']').attr('selected','selected');
    }
    if(divisionId != null){
        $('#division-select').append($('<option value = "">select</option>'));
    }
    //Load Countries
    $.each(unitList, function(unitkey,unitval){
        if( (unitval['client_id'] == clientunitId) && (unitval['business_group_id'] == businessgroupId) && (unitval['legal_entity_id'] == legalEntityId ) &&  (unitval['division_id'] == divisionId)){
            var unitValues = unitval['units'];
            $.each(unitValues, function(key, value){
                var unitListVal = unitValues[key];
                var units = [];
                var j = 0;
                $.each(unitListVal, function(k, val){
                    units[j++] = val['unit_id'];
                });

                addcountryrowupdate(clientunitId, businessgroupId, legalEntityId, divisionId, key, units, countryByCount, unitval['units']); //add country by Unit
                countryByCount++;
            });             
                
        }
    });

}
function addcountryrowupdate(clientunitId, businessgroupId, legalEntityId, divisionId, key, units, bycount, unitval){

    var countryByCount = bycount;
    var divCountryAddRow = $('#templates .grid-table');
    var clone = divCountryAddRow.clone();
    $('.btable', clone).addClass('table-'+countryByCount);
    $('.countryval', clone).addClass('countryval-'+countryByCount);
    $('.country', clone).addClass('country-'+countryByCount);
    $('.autocompleteview', clone).addClass('autocompleteview-'+countryByCount);
    $('.ulist-text', clone).addClass('ulist-text-'+countryByCount);         
    $('.geography-levels', clone).addClass('glevel-'+countryByCount+'-'+1);
    $('.unit-location', clone).addClass('unitlocation-'+countryByCount+'-'+1);
    $('.unit-location-ids', clone).addClass('unitlocation-ids-'+countryByCount+'-'+1);
    $('.auto-complete-unit-location', clone).addClass('auto-complete-unit-location-'+countryByCount+'-'+1);
    $('.unitlocationlist-text', clone).addClass('unitlocationlist-text-'+countryByCount+'-'+1);
    $('.full-location-list', clone).addClass('full-location-list-'+countryByCount+'-'+1);
    //$('.unitcode-checkbox', clone).addClass('unitcode-checkbox-'+countryByCount);
    $('.unit-id', clone).addClass('unit-id-'+countryByCount+'-'+1);
    $('.unit-code', clone).addClass('unit-code-'+countryByCount);
    $('.unit-code', clone).addClass('unit-code-'+countryByCount+'-'+1);
    $('.unit-name', clone).addClass('unit-name-'+countryByCount+'-'+1);
    $('.industry', clone).addClass('industry-'+countryByCount+'-'+1);
    $('.unit-address', clone).addClass('unit-address-'+countryByCount+'-'+1);
    $('.postal-code', clone).addClass('postal-code-'+countryByCount+'-'+1);
    $('.domain-list', clone).addClass('domain-list-'+countryByCount+'-'+1);
    $('.domainselected', clone).addClass('domainselected-'+countryByCount+'-'+1);
    $('.domain', clone).addClass('domain-'+countryByCount+'-'+1);
    $('.domain-selectbox-view', clone).addClass('domain-selectbox-view-'+countryByCount+'-'+1);
    $('.ul-domain-list', clone).addClass('ul-domain-list-'+countryByCount+'-'+1);       
    $('.add-unit-row img', clone).addClass('table-addunit-'+countryByCount);
    $('.tbody-unit-list', clone).addClass('tbody-unit-'+countryByCount);
    $('.no-of-units', clone).addClass('no-of-units-'+countryByCount);
    
    $('#unitcount').val(1);
    $('.unit-error-msg', clone).addClass('unit-error-msg-'+countryByCount);
    $('.activedclass', clone).addClass('activedclass-'+countryByCount+'-1');
    $('.add-country-unit-list').append(clone);          
    $('.no-of-units-'+countryByCount).val(1);
    // if(countryByCount != 1){
    //     $('.unitcode-checkbox-'+countryByCount).hide();  
    // }  
    $(".postal-code", clone).on('input', function (event) {
        this.value = this.value.replace(/[^0-9]/g, '');
    });

    var firstlist = unitval[key][0];
    $('.countryval-'+countryByCount).val(getCountryName(key));
    $('.country-'+countryByCount).val(key);    
    var gid = firstlist['geography_id'];
    var unitlts = loadupdateunitlocation(key, gid);
    loadglevelsupdate(key, "glevel-"+countryByCount+"-"+1);
    loadIndustry('industry-'+countryByCount+'-'+1);
    $('.glevel-'+countryByCount+'-'+1 +' option[value='+unitlts["level_id"]+']').attr("selected", "selected"); 
    $('.unitlocation-'+countryByCount+'-'+1).val(unitlts['gname']);
    $('.unitlocation-ids-'+countryByCount+'-'+1).val(gid);
    $('.full-location-list-'+countryByCount+'-'+1).text(unitlts['mapping']);
    $('.unit-id-'+countryByCount+'-1').val(firstlist['unit_id']);
    $('.unit-code-'+countryByCount+'-'+1).val(firstlist['unit_code']);
    $('.unit-name-'+countryByCount+'-1').val(firstlist['unit_name']);
    $('.industry-'+countryByCount+'-'+1+' option[value='+firstlist["industry_id"]+']').attr("selected", "selected");
    $('.unit-address-'+countryByCount+'-'+1).val(firstlist['unit_address']);
    $('.postal-code-'+countryByCount+'-'+1).val(firstlist['postal_code']);
    var domainsListArray = firstlist['domain_ids'];
    $('.domain-'+countryByCount+'-'+1).val(domainsListArray);
    $('.domainselected-'+countryByCount+'-'+1).val(domainsListArray.length+" Selected");
    $('.activedclass-'+countryByCount+'-'+1).text("active");

    unitcodeautogenerateids++;
    if(units != ''){
        var lastClassvalglobal = 2;
        var tbodyclassname = "tbody-unit-"+countryByCount;
        var unitids = (units.toString()).split(",");
        for( var icount = 1;  icount < unitids.length; icount++){
            addUnitRowUpdate(clientunitId, businessgroupId, legalEntityId, divisionId, unitids[icount], tbodyclassname, lastClassvalglobal, countryByCount, unitval[key][icount], key);
            lastClassvalglobal++;
        }
    }

}

function addUnitRowUpdate(clientunitId, businessgroupId, legalEntityId, divisionId, unitid, tbodyclassname, lastClassval, countval, unitlist, countryid){   
    var divUnitAddRow = $('#templatesUnitRow .table-UnitRow-list .table-row');
    var clone1 = divUnitAddRow.clone();
    $('.geography-levels', clone1).addClass('glevel-'+countval+'-'+(lastClassval));
    $('.unit-location', clone1).addClass('unitlocation-'+countval+'-'+(lastClassval));
    $('.unit-location-ids', clone1).addClass('unitlocation-ids-'+countval+'-'+(lastClassval));
    $('.auto-complete-unit-location', clone1).addClass('auto-complete-unit-location-'+countval+'-'+lastClassval);
    $('.unitlocationlist-text', clone1).addClass('unitlocationlist-text-'+countval+'-'+lastClassval);
    $('.full-location-list', clone1).addClass('full-location-list-'+countval+'-'+lastClassval);
    $('.unit-code', clone1).addClass('unit-code-'+countval);
    $('.unit-code', clone1).addClass('unit-code-'+countval+'-'+lastClassval);
    $('.unit-id', clone1).addClass('unit-id-'+countval+'-'+lastClassval);
    $('.unit-name', clone1).addClass('unit-name-'+countval+'-'+lastClassval);
    $('.industry', clone1).addClass('industry-'+countval+'-'+lastClassval);
    $('.unit-address', clone1).addClass('unit-address-'+countval+'-'+lastClassval);
    $('.postal-code', clone1).addClass('postal-code-'+countval+'-'+lastClassval);
    $('.domain-list', clone1).addClass('domain-list-'+countval+'-'+lastClassval);
    $('.domainselected', clone1).addClass('domainselected-'+countval+'-'+lastClassval);
    $('.domain', clone1).addClass('domain-'+countval+'-'+(lastClassval));
    $('.domain-selectbox-view', clone1).addClass('domain-selectbox-view-'+countval+'-'+lastClassval);
    $('.ul-domain-list', clone1).addClass('ul-domain-list-'+countval+'-'+lastClassval);
    $('.activedclass', clone1).addClass('activedclass-'+countval+'-'+lastClassval);   
    
    $('.'+tbodyclassname).append(clone1);
    unitcodeautogenerateids++;            
    $(".postal-code", clone1).on('input', function (event) {
        this.value = this.value.replace(/[^0-9]/g, '');
    });
    $('.no-of-units-'+countval).val(parseInt($('.no-of-units-'+countval).val())+1);
    loadglevelsupdate(countryid, "glevel-"+countval+"-"+lastClassval);
    var firstlist = unitlist;
    var gid = firstlist['geography_id'];    
    var unitlts = loadupdateunitlocation(countryid, gid);
    $('.glevel-'+countval+'-'+lastClassval+' option[value='+unitlts["level_id"]+']').attr("selected", "selected");    
    $('.unitlocation-'+countval+'-'+lastClassval).val(unitlts['gname']);
    $('.unitlocation-ids-'+countval+'-'+lastClassval).val(gid);
    $('.full-location-list-'+countval+'-'+lastClassval).text(unitlts['mapping']);
    $('.unit-id-'+countval+'-'+lastClassval).val(firstlist['unit_id']);
    $('.unit-code-'+countval+'-'+lastClassval).val(firstlist['unit_code']);
    $('.unit-name-'+countval+'-'+lastClassval).val(firstlist['unit_name']);
    loadIndustry('industry-'+countval+'-'+lastClassval);
    $('.industry-'+countval+'-'+lastClassval+' option[value='+firstlist["industry_id"]+']').attr("selected", "selected"); 
    $('.unit-address-'+countval+'-'+lastClassval).val(firstlist['unit_address']);
    $('.postal-code-'+countval+'-'+lastClassval).val(firstlist['postal_code']);
    var domainsListArray = firstlist['domain_ids'];
    $('.domain-'+countval+'-'+lastClassval).val(domainsListArray);
    $('.domainselected-'+countval+'-'+lastClassval).val(domainsListArray.length+" Selected");
    $('.activedclass-'+countval+'-'+lastClassval).text("active");
}


//Submit Record -----------------------------------------------------------------------------------------
$("#btn-clientunit-submit").click(function(){
    clearMessage();
    var clientunitIdValue = $("#client-unit-id").val();
    var groupNameValue = $("#group-select").val();
    var businessgrouptextValue = $("#businessgroup-text").val();        
    var businessgroupValue = $("#businessgroup-select").val();  
    var businessgroupName = $("#businessgroup-select :selected").text();        
    var legalEntityValue = $("#entity-select").val();
    var lentitytextValue = $("#entity-text").val();
    var legalEntityName = $("#entity-select :selected").text();
    var divisiontextValue = $("#division-text").val();      
    var divisionValue = $("#division-select").val();
    var divisionName = $("#division-select :selected").text();
    var unitCountValue = $("#unitcount").val();
    var countryVal = $(".country").val();
    if(groupNameValue.length == 0){
        displayMessage("Select Group");
        return false;
    }
    if(lentitytextValue.length == 0){
        if(legalEntityValue.length == 0){
            displayMessage("Select Existing Legal Entity or Create New");
            return false;
        }
    }
    if(unitCountValue.length == 0){
        displayMessage("Add atleast one unit in a Group");
        return false;
    }
    if(countryVal.length == 0){
        displayMessage("Enter Country");
        return false;
    }
    if(clientunitIdValue == ''){    
        function onSuccess(data) {
            $("#clientunit-add").hide();
            $("#clientunit-view").show();
            initialize();
        }
        function onFailure(error) {
            if(error == "UnitCodeAlreadyExists"){
                displayMessage("Unit Code Already Exists!");
            }
            else{
                displayMessage(error);    
            }
            
        }

        var businessGroup;
        var bgIdValue;
        var bgNameValue;
        if(businessgrouptextValue == ''){
            bgIdValue = parseInt(businessgroupValue);
            if(businessgroupValue != ''){
                bgNameValue = businessgroupName;    
            }
            else{
                bgNameValue = null; 
            }   
        }
        else{
            bgIdValue = null;
            bgNameValue = businessgrouptextValue;   
        }
     
        var legalEntity;
        var leIdValue;
        var leNameValue;
        if(lentitytextValue == ''){
            leIdValue = parseInt(legalEntityValue);
            if(legalEntityValue != ''){
                leNameValue = legalEntityName;  
            }
            else{
                leNameValue = null; 
            }   
        }
        else{
            leIdValue = null;
            leNameValue = lentitytextValue;   
        }
        var division;
        var divIdValue;
        var divNameValue;
        if(divisiontextValue == ''){
            divIdValue = parseInt(divisionValue);
            if(divisionValue!=''){
                divNameValue = divisionName;    
            }
            else{
                divNameValue = null;    
            }   
        }
        else{
            divIdValue = null;
            divNameValue = divisiontextValue;   
        }
        if(bgNameValue != null){
            businessGroup = mirror.getBusinessGroupDict(bgIdValue, bgNameValue);    
        }
        else{
            businessGroup = null;
        }
        legalEntity = mirror.getLegalEntityDict(leIdValue, leNameValue);
        if(divNameValue != null){
            division = mirror.getDivisionDict(divIdValue, divNameValue);
        }
        else{
            division = null;
        }
        

        var countryWiseUnits = [];
        var numItemsCountry = $('.country').length;
        for(var i = 1; i < numItemsCountry;i++){
            if($('.country-'+i).val() != ''){
                var unitarr = [];
                countryUnits = parseInt($('.country-'+i).val());
                var unitcount = $('.no-of-units-'+i).val();
                var units = [];
                for(var j = 1;j <= unitcount;j++){
                    
                    var unit;
                    unitId= null;
                    unitCode =  $('.unit-code-'+i+'-'+j).val();
                    unitName = $('.unit-name-'+i+'-'+j).val().trim();
                    unitAddress = $('.unit-address-'+i+'-'+j).val().trim();
                    unitPostalCode = $('.postal-code-'+i+'-'+j).val().trim();
                    unitGeographyId = $('.unitlocation-ids-'+i+'-'+j).val().trim();
                    unitLocation = $('.unitlocation-'+i+'-'+j).val().trim();
                    unitIndustryId = parseInt($('.industry-'+i+'-'+j).val());
                    unitIndustryName = $('.industry-'+i+'-'+j+' option:selected').text();
                    unitdomain = $('.domain-'+i+'-'+j).val();
                  
                    if(unitLocation == ''){
                        $(".unit-error-msg-"+i).html("Unit Location Required");
                        return;
                    }
                    else if(unitGeographyId == ''){
                        $(".unit-error-msg-"+i).html("Unit Location Name is Invalid");
                        return;   
                    }
                    else if(unitCode == ''){
                        $(".unit-error-msg-"+i).html("Unit Code Required");
                        return;
                    }
                    else if(unitName == ''){
                        $(".unit-error-msg-"+i).html("Unit Name Required");
                        return;
                    }
                    else if(unitIndustryName == ''){
                        $(".unit-error-msg-"+i).html("Select Industry");
                        return;
                    }
                    else if(unitAddress == ''){
                        $(".unit-error-msg-"+i).html("Unit Address Required");
                        return;
                    }
                    else if(unitPostalCode == ''){
                        $(".unit-error-msg-"+i).html("Unit Postal Code Required");
                        return;
                    }
                    else if(unitdomain == ''){
                        $(".unit-error-msg-"+i).html("Domain Required");
                        return;   
                    }
                    else{
                        unitarr.push(unitCode);
                        var hash = [];
                        for (var n=unitarr.length; n--; ){
                           if (typeof hash[unitarr[n]] === 'undefined') hash[unitarr[n]] = [];
                           hash[unitarr[n]].push(n);
                        }

                        var duplicates = [];
                        for (var key in hash){
                            if (hash.hasOwnProperty(key) && hash[key].length > 1){
                                duplicates.push(key);
                            }
                        }
                        if(duplicates == ""){
                            var arrayDomainsVal = unitdomain.split(",");
                            var arrayDomains = [];
                            for(var m = 0; m < arrayDomainsVal.length; m++){
                                arrayDomains[m] = parseInt(arrayDomainsVal[m]);
                            } 
                            var domainsVal = arrayDomains;

                            unit = mirror.getUnitDict(null, unitName, unitCode, unitAddress, parseInt(unitPostalCode), 
                                parseInt(unitGeographyId), unitLocation, unitIndustryId, unitIndustryName, domainsVal);
                            units.push(unit);    
                        }
                        else{
                            displayMessage(duplicates+" Unit Code Already Exits!!!");
                            return;
                        }

                        
                    }
                    
                }
                countryWiseUnits.push(mirror.mapUnitsToCountry(countryUnits, units))
            }
        } 
        mirror.saveClient( parseInt(groupNameValue), businessGroup, legalEntity, division, countryWiseUnits,
            function(error, response){
                if(error == null){
                    onSuccess(response);
                }
                else{
                    onFailure(error);
                }
            }
        );
    }
    else if(clientunitIdValue != ''){    
        clearMessage();   
        function onSuccess(data) {
            $("#clientunit-add").hide();
            $("#clientunit-view").show();
            initialize();
        }
        function onFailure(error) {
            displayMessage(error);
        }
        
        var businessGroup;
        var bgIdValue;
        var bgNameValue;
        if(businessgrouptextValue == ''){
            bgIdValue = parseInt(businessgroupValue);
            if(businessgroupValue != ''){
                bgNameValue = businessgroupName;    
            }
            else{
                bgNameValue = null; 
            }   
        }
        else{
            bgIdValue = null;
            bgNameValue = businessgrouptextValue;   
        }
     
        var legalEntity;
        var leIdValue;
        var leNameValue;
        if(lentitytextValue == ''){
            leIdValue = parseInt(legalEntityValue);
            if(legalEntityValue != ''){
                leNameValue = legalEntityName;  
            }
            else{
                leNameValue = null; 
            }   
        }
        else{
            leIdValue = null;
            leNameValue = lentitytextValue;   
        }
        var division;
        var divIdValue;
        var divNameValue;
        if(divisiontextValue == ''){
            divIdValue = parseInt(divisionValue);
            if(divisionValue!=''){
                divNameValue = divisionName;    
            }
            else{
                divNameValue = null;    
            }   
        }
        else{
            divIdValue = null;
            divNameValue = divisiontextValue;   
        }
        if(bgNameValue != null){
            businessGroup = mirror.getBusinessGroupDict(bgIdValue, bgNameValue);    
        }
        else{
            businessGroup = null;
        }
        legalEntity = mirror.getLegalEntityDict(leIdValue, leNameValue);
        if(divNameValue != null){
            division = mirror.getDivisionDict(divIdValue, divNameValue);
        }
        else{
            division = null;
        }
        

        var countryWiseUnits = [];

        var numItemsCountry = $('.country').length;
        for(var i = 1; i < numItemsCountry;i++){
            var countryUnits = {};
            var unitarr = [];
            if($('.country-'+i).val() != ''){
                countryUnits = parseInt($('.country-'+i).val());
                var unitcount = $('.no-of-units-'+i).val();
                console.log("unitcount value = "+$('.no-of-units-'+i).val());
                var units = [];
                for(var j = 1; j <= unitcount; j++){

                    var unit;
                    unitId= $('.unit-id-'+i+'-'+j).val();;
                    unitCode =  $('.unit-code-'+i+'-'+j).val();
                    unitName = $('.unit-name-'+i+'-'+j).val().trim();
                    unitAddress = $('.unit-address-'+i+'-'+j).val().trim();
                    unitPostalCode = $('.postal-code-'+i+'-'+j).val().trim();
                    unitGeographyId = $('.unitlocation-ids-'+i+'-'+j).val().trim();
                    unitLocation = $('.unitlocation-'+i+'-'+j).val().trim();
                    unitIndustryId = parseInt($('.industry-'+i+'-'+j).val());
                    unitIndustryName = $('.industry-'+i+'-'+j+' option:selected').text();
                    unitdomain = $('.domain-'+i+'-'+j).val();
                  
                    if(unitLocation == ''){
                        $(".unit-error-msg-"+i).html("Unit location Required");
                        return;
                    }
                    else if(unitGeographyId == ''){
                        $(".unit-error-msg-"+i).html("Unit location Name is Invalid");
                        return;   
                    }
                    else if(unitCode == ''){
                        $(".unit-error-msg-"+i).html("Unit Code Required");
                        return;
                    }
                    else if(unitName == ''){
                        $(".unit-error-msg-"+i).html("Unit Name Required");
                        return;
                    }
                    else if(unitIndustryName == ''){
                        $(".unit-error-msg-"+i).html("Select Industry");
                        return;
                    }
                    else if(unitAddress == ''){
                        $(".unit-error-msg-"+i).html("Unit Address Required");
                        return;
                    }
                    else if(unitPostalCode == ''){
                        $(".unit-error-msg-"+i).html("Unit Postal code Required");
                        return;
                    }
                    else if(unitdomain == ''){
                        $(".unit-error-msg-"+i).html("Domain Required");
                        return;   
                    } 
                    else{
                        unitarr.push(unitCode);
                        var hash = [];
                        for (var n=unitarr.length; n--; ){
                           if (typeof hash[unitarr[n]] === 'undefined') hash[unitarr[n]] = [];
                           hash[unitarr[n]].push(n);
                        }

                        var duplicates = [];
                        for (var key in hash){
                            if (hash.hasOwnProperty(key) && hash[key].length > 1){
                                duplicates.push(key);
                            }
                        }
                        if(duplicates == ""){
                            var arrayDomainsVal = unitdomain.split(",");
                            var arrayDomains = [];
                            for(var m = 0; m < arrayDomainsVal.length; m++){
                                arrayDomains[m] = parseInt(arrayDomainsVal[m]);
                            } 
                            var domainsVal = arrayDomains;

                            unit = mirror.getUnitDict(parseInt(unitId), unitName, unitCode, unitAddress, parseInt(unitPostalCode), 
                                parseInt(unitGeographyId), unitLocation, unitIndustryId, unitIndustryName, domainsVal);
                            units.push(unit);
                        }
                        else{
                            displayMessage(duplicates+" Unit Code Already Exists!!!");
                            return;
                        }
                    }
                    
                }
                countryWiseUnits.push(mirror.mapUnitsToCountry(countryUnits, units))
            }
        } 
        mirror.updateClient( parseInt(groupNameValue), businessGroup, legalEntity, division, countryWiseUnits,
            function(error, response){
                if(error == null){
                    onSuccess(response);
                }
                else{
                    onFailure(error);
                }
            }
        );
    }
    else{
        console.log("Fails All");
    }
});


//Active or inactive Client Unit List --------------------------------------------------------------------------
function clientunit_active(clientunitId, lentityId, divisionId, isActive){
    var msgstatus='deactivate';
    if(isActive){
        msgstatus='activate';
    }
    var answer = confirm('Are you sure want to '+msgstatus+ '?');
    if (answer)
    {
        function onSuccess(data) {
            initialize();   
        }
        function onFailure(error) {
            console.log(error); 
        }
        mirror.changeClientStatus( parseInt(clientunitId), parseInt(lentityId), divisionId, isActive, 
            function(error, response){
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

//Search Client name ----------------------------------------------------------------------------------------------
$("#search-clientunit-name").keyup(function() { 
    var count = 0;
  var value = this.value.toLowerCase();
  $("table").find("tr:not(:first)").each(function(index) {
      if (index === 0) return;
      var id = $(this).find(".clientunit-name").text().toLowerCase();       
      $(this).toggle(id.indexOf(value) !== -1);;
  });
});
function hidemenu(classname) {
    var lastClass = classname.split(' ').pop();
    var ccount = lastClass.split('-').pop();
    $('.autocompleteview-'+ccount).css("display", "none");
}

function loadauto_countrytext (textval, classval) {
    var lastClass = classval.split(' ').pop();
    var ccount = lastClass.split('-').pop();    
    $('.autocompleteview-'+ccount).css("display", "block");
    var groupId = $("#group-select").val();
    if(groupId == ''){
        displayMessage("Select Group First");
    }
    else{
        var arrayCountry = [];
        for (var i in groupList){
            if(groupList[i]['client_id'] == groupId){
                arrayCountry = groupList[i]['country_ids'];
            }
        }
    }

    var countries = countryFulList;
    var suggestions = [];
    $('.ulist-text-'+ccount).empty();
    if(textval.length>0){
        for(var i in countries){
            for(var j=0;j<arrayCountry.length;j++){
                if(arrayCountry[j] == countries[i]['country_id']){
                    //console.log(arrayCountry[j]+" == "+countries[i]['country_id']);
                    if (~countries[i]["country_name"].toLowerCase().indexOf(textval.toLowerCase()) && countries[i]["is_active"] == 1) suggestions.push([countries[i]["country_id"],countries[i]["country_name"]]);  
                }       
            }
        }
        var str='';
        for(var i in suggestions){
            str += '<li id="'+suggestions[i][0]+'" onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\', '+ccount+')">'+suggestions[i][1]+'</li>';
        }
        $('.ulist-text-'+ccount).append(str);
        $(".country-"+ccount).val('');
    }
}
//set selected autocomplte value to textbox and geographylevel list ---------------------------------------------------
function activate_text (element,checkval,checkname, ccount) {
    $(".countryval-"+ccount).val(checkname);
    $(".country-"+ccount).val(checkval);
    $('.glevel-'+checkval).empty();
}
function hideunitlocation(classname) {
    var lastClass = classname.split(' ').pop();
    $('.'+lastClass).css("display", "none");
}
//autocomplete location -----------------------------------------------------------------------------------------------
function loadlocation(textval, classval){
    var lastClass = classval.split(' ').pop();
    var ccount = lastClass.split('-');
    var countval = '-'+ccount[1]+'-'+ccount[2];
    var glevelval = $('.glevel'+countval).val();
    $('.auto-complete-unit-location'+countval).css("display", "block");
    var suggestions = [];
    $('.unitlocationlist-text'+countval).empty();
    
    if(textval.length>0){
        for(var geography in geographyList){
            var geolist = geographyList[geography];
            for(var glist in geolist){
                if(geolist[glist]['level_id'] == glevelval){
                    if (~geolist[glist]["geography_name"].toLowerCase().indexOf(textval.toLowerCase()) && geolist[glist]["is_active"] == 1) suggestions.push([geolist[glist]["geography_id"],geolist[glist]["geography_name"], geolist[glist]["mapping"]]);     
                }       
            }
        }
        var str='';
        for(var i in suggestions){
            str += '<li id="'+suggestions[i][0]+'" onclick="activate_unitlocaion(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\', \''+countval+'\', \''+suggestions[i][2]+'\')">'+suggestions[i][1]+'</li>';
        }
        $('.unitlocationlist-text'+countval).append(str);       
        $('.unitlocation-ids'+countval).val('');
    }
}
function activate_unitlocaion (element,checkval,checkname, ccount, mappingname) {
    $('.unitlocation'+ccount).val(checkname);
    $('.unitlocation-ids'+ccount).val(checkval);
    $('.full-location-list'+ccount).html(mappingname);
}
function hidedomain(classval){
    var lastClass = classval.split(' ').pop();
    var ccount=lastClass.split('-');
    var countval='-'+ccount[3]+'-'+ccount[4];
    $('.domain-selectbox-view'+countval).css("display", "none");    
}
//Load Domain  for Unit------------------------------------------------------------------------------------------------
function loaddomain(classval){
    var lastClass = classval.split(' ').pop();
    var ccount=lastClass.split('-');
    var countval='-'+ccount[1]+'-'+ccount[2];
    $('.domain-selectbox-view'+countval).css("display", "block");   
    var editdomainval=[];
    if($('.domain'+countval).val() != ''){
        editdomainval = $('.domain'+countval).val().split(",");
    }
    var domains=domainList;
    $('.ul-domain-list'+countval).empty();
    var str='';
    for(var i in domains){
        var selectdomainstatus='';
        for(var j=0; j<editdomainval.length; j++){
            if(editdomainval[j] == domains[i]["domain_id"]){
                selectdomainstatus='checked';
            }
        }
        var domainId=parseInt(domains[i]["domain_id"]);
        var domainName=domains[i]["domain_name"];
        if(selectdomainstatus == 'checked'){
            str += '<li id="'+domainId+'" class="active_selectbox'+countval+' active" onclick="activate(this,\''+countval+'\' )" >'+domainName+'</li> ';
        }else{
            str += '<li id="'+domainId+'" onclick="activate(this,\''+countval+'\')" >'+domainName+'</li> ';
        }
    }
    $('.ul-domain-list'+countval).append(str);
    $('.domainselected'+countval).val(editdomainval.length+" Selected")
}

//check & uncheck process
function activate(element, count){
    var chkstatus = $(element).attr('class');
    if(chkstatus == 'active_selectbox'+count+' active'){
        $(element).removeClass("active_selectbox"+count);
        $(element).removeClass("active");
        
    }else{
        $(element).addClass("active_selectbox"+count);
        $(element).addClass("active");
    }  
    var selids='';
    var selNames='';
    var totalcount =  $(".active_selectbox"+count).length;
    $(".active_selectbox"+count).each( function( index, el ) {
        if (index === totalcount - 1) {
            selids = selids+el.id;
        }else{
            selids = selids+el.id+",";
        }    
    });
    $(".domainselected"+count).val(totalcount+" Selected");
    $(".domain"+count).val(selids);
}
function divisionExistingChecking(str){
    if(str == "New"){
        $("#division-text").show();
        $("#division-select").hide();
        $("#division-new").hide();  
        $("#division-existing").show(); 
        $("#division-text").val("");
        $("#division-select").val("");
    }
    if(str == "Cancel"){
        $("#division-text").hide();
        $("#division-select").show();
        $("#division-new").show();
        $("#division-existing").hide();     
        $("#division-text").val("");
        $("#division-select").val("");
    }
}
function legalEntityExistingChecking(str){
    if(str == "New"){
        $("#entity-text").show();
        $("#entity-select").hide();
        $("#entity-new").hide();
        $("#entity-existing").show();
        $("#division-text").show();
        $("#division-select").hide();
        $("#division-new").hide();
        $("#division-existing").hide(); 
        $("#division-text").val("");
        $("#division-select").val("");
        $("#entity-text").val("");
        $("#entity-select").val("");
    }
    if(str == "Cancel"){
        $("#entity-text").hide();
        $("#entity-select").show();
        $("#entity-new").show();
        $("#entity-existing").hide();
        $("#division-text").hide();
        $("#division-select").show();
        $("#division-new").show();
        $("#division-existing").hide(); 
        $("#division-text").val("");
        $("#division-select").val("");
        $("#entity-text").val("");
        $("#entity-select").val("");
    }
}
function businessGroupExistingChecking(str){
    if(str == "New"){
        $("#businessgroup-text").show();
        $("#businessgroup-select").hide();
        $("#businessgroup-new").hide();
        $("#businessgroup-existing").show();
        $("#entity-text").show();
        $("#entity-select").hide();
        $("#entity-new").hide();
        $("#entity-existing").hide();
        $("#division-text").show();
        $("#division-select").hide();
        $("#division-new").hide();
        $("#division-existing").hide(); 
        $("#division-text").val("");
        $("#division-select").val("");
        $("#entity-text").val("");
        $("#entity-select").val("");
        $("#businessgroup-text").val("");
        $("#businessgroup-select").val("");
    }
    if(str == "Cancel"){
        $("#businessgroup-text").hide();
        $("#businessgroup-select").show();
        $("#businessgroup-new").show();
        $("#businessgroup-existing").hide();
        $("#entity-text").hide();
        $("#entity-select").show();
        $("#entity-new").show();
        $("#entity-existing").hide();
        $("#division-text").hide();
        $("#division-select").show();
        $("#division-new").show();
        $("#division-existing").hide();
        $("#division-text").val("");
        $("#division-select").val("");
        $("#entity-text").val("");
        $("#entity-select").val("");
        $("#businessgroup-text").val("");
        $("#businessgroup-select").val(""); 
    }
}
$(function() {
    initialize();
});
$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});
