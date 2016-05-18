function getMonth_IntegettoString(intMonth){
	var stringMonth = '';
	if(intMonth == 1) stringMonth = "Jan"
  	else if(intMonth == 2) stringMonth = "Feb"
  	else if(intMonth == 3) stringMonth = "Mar"
  	else if(intMonth == 4) stringMonth = "Apr"
  	else if(intMonth == 5) stringMonth = "May"
  	else if(intMonth == 6) stringMonth = "Jun"
  	else if(intMonth == 7) stringMonth = "Jul"
  	else if(intMonth == 8) stringMonth = "Aug"
  	else if(intMonth == 9) stringMonth = "Sep"
  	else if(intMonth == 10) stringMonth = "Oct"
  	else if(intMonth == 11) stringMonth = "Nov"
  	else if(intMonth == 12) stringMonth = "Dec"
  		
  	return stringMonth;
}

//country autocomplete function
function getCountryAutocomplete(textval, listval, callback){
  $("#ac-country").show(); 
  var countries = listval;
  var suggestions = [];
  $('#ac-country ul').empty();
  if(textval.length>0){
    for(var i in countries){
      if (~countries[i]["country_name"].toLowerCase().indexOf(textval.toLowerCase()) && countries[i]["is_active"] == true) suggestions.push([countries[i]["country_id"],countries[i]["country_name"]]); 
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-country ul').append(str);
    //$("#country").val('');
  }else{
    alert('ent')
    $("#country").val('');
    $(".ac-textbox").hide();
  }
}

//domain autocomplete function
function getDomainAutocomplete(textval, listval, callback){
  $("#ac-domain").show(); 
  var domains = listval;
  var suggestions = [];
  $('#ac-domain ul').empty();
  if(textval.length>0){
    for(var i in domains){
      if (~domains[i]["domain_name"].toLowerCase().indexOf(textval.toLowerCase()) && domains[i]["is_active"] == true) suggestions.push([domains[i]["domain_id"],domains[i]["domain_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-domain ul').append(str);
    //$("#domain").val('');
    }else{
      $("#domain").val('');
      $(".ac-textbox").hide();
    }
}

//usergroup autocomplete function
function getUserGroupAutocomplete(textval, listval, callback){
  $("#ac-usergroup").show(); 
  var usergroups = listval;
  var suggestions = [];
  $('#ac-usergroup ul').empty();
  if(textval.length>0){
    for(var i in usergroups){
      if (~usergroups[i]["user_group_name"].toLowerCase().indexOf(textval.toLowerCase()) && usergroups[i]["is_active"] == true) suggestions.push([usergroups[i]["user_group_id"],usergroups[i]["user_group_name"]]); 
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-usergroup ul').append(str);
    //$("#usergroup").val('');
  }else{
    $("#usergroup").val('');
    $(".ac-textbox").hide();
  }
}

//industry autocomplete function
function getIndustryAutocomplete(textval, listval, callback){
  $("#ac-industry").show();
  var industries = listval;
  var suggestions = [];
  $('#ac-industry ul').empty();
  if(textval.length>0){
    for(var i in industries){
      if (~industries[i]["industry_name"].toLowerCase().indexOf(textval.toLowerCase()) && industries[i]["is_active"] == 1) suggestions.push([industries[i]["industry_id"],industries[i]["industry_name"]]);
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-industry ul').append(str);
    //$("#industry").val('');
    }else{
      $("#industry").val('');
      $(".ac-textbox").hide();
    }
}

//statutorynature autocomplete function
function getStatutoryNatureAutocomplete(textval, listval, callback){
  $("#ac-statutorynature").show();
  var statutorynatures = statutoryNaturesList;
  var suggestions = [];
  $('#ac-statutorynature ul').empty();
  if(textval.length>0){
    for(var i in statutorynatures){
      if (~statutorynatures[i]["statutory_nature_name"].toLowerCase().indexOf(textval.toLowerCase()) && statutorynatures[i]["is_active"] == 1) suggestions.push([statutorynatures[i]["statutory_nature_id"],statutorynatures[i]["statutory_nature_name"]]);
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-statutorynature ul').append(str);
    //$("#statutorynature").val('');
    }else{
      $("#statutorynature").val('');
      $(".ac-textbox").hide();
    }
}

//geography autocomplete function
function getGeographyAutocomplete(textval, listval, callback){
  $("#ac-geography").show();
  var geographies = listval;
  var suggestions = [];
  $('#ac-geography ul').empty();
  if(textval.length>0){
    for(var i in geographies){
      if (~geographies[i]["geography_name"].toLowerCase().indexOf(textval.toLowerCase()) && geographies[i]["is_active"] == true) suggestions.push([geographies[i]["geography_id"],geographies[i]["geography_name"]]);
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-geography ul').append(str);
    //$("#geography").val('');
    }else{
      $("#geography").val('');
      $(".ac-textbox").hide();
    }
}

//statutory autocomplete function
function getStatutoryAutocomplete(textval, listval, callback){
  $("#ac-statutory").show();
  var statutories = listval;
  var suggestions = [];
  $('#ac-statutory ul').empty();
  if(textval.length>0){
    for(var i in statutories){
      if (~statutories[i]["statutory_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([statutories[i]["statutory_id"],statutories[i]["statutory_name"]]);
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-statutory ul').append(str);
    //$("#statutory").val('');
  }else{
    $("#statutory").val('');
    $(".ac-textbox").hide();
  }
}

//user autocomplete function
function getUserAutocomplete(textval, listval, callback){
  $("#ac-user").show();
  var users = listval;
  var suggestions = [];
  $('#ac-user ul').empty();
  if(textval.length>0){
      for(var i in users){
        var combineUserName = '';
        if(users[i]['employee_code'] != undefined){
          combineUserName = users[i]['employee_code']+"-"+users[i]['employee_name'];
        }else{
          combineUserName =users[i]['employee_name'];
        }
        
        var user_id;
        if(users[i]['user_id'] != undefined){
          user_id = users[i]['user_id'];
        }else{
          user_id =users[i]['employee_id'];
        }
        if (~users[i]["employee_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([user_id,combineUserName]); 
      }
      var str='';
      for(var i in suggestions){
        str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
      }
      $('#ac-user ul').append(str);
      
      //$("#userid").val('');
      //$("#assignee").val('');
  }else{
    $("#userid").val('');
    $("#assignee").val('');
    $(".ac-textbox").hide();
  }
}

//form autocomplete function
function getFormAutocomplete(textval, listval, callback){
  $("#ac-form").show();
  var forms = listval;
  var suggestions = [];
  $('#ac-form ul').empty();
  if(textval.length>0){
      for(var i in forms){
        if (~forms[i]["form_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([forms[i]["form_id"],forms[i]["form_name"]]); 
      }
      var str='<li id="0" onclick="activate_text(this,'+callback+')">Login</li>';
      for(var i in suggestions){
        str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
      }
      $('#ac-form ul').append(str);
      //$("#formid").val('');
  }else{
    $("#formid").val('');
    $(".ac-textbox").hide();
  }
}

//group autocomplete function
function getGroupAutocomplete(textval, listval, callback){
  $("#ac-group").show();
  var groups = listval;
  var suggestions = [];
  $('#ac-group ul').empty();
  if(textval.length>0){
    for(var i in groups){
        if(groups[i]['is_active'] == true){
            if (~groups[i]['group_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([groups[i]["client_id"],groups[i]["group_name"]]);
        }
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-group ul').append(str);
    //$("#group-id").val('');
  }else{
    $("#group-id").val('');
    $(".ac-textbox").hide();
  }
}

//businessgroup autocomplete function
function getBusinessGroupAutocomplete(textval, listval, callback){
  $("#ac-businessgroup").show();
  var bgroups = listval;
  var suggestions = [];
  $('#ac-businessgroup ul').empty();
  if(textval.length>0){
      for(var i in bgroups){
          if(bgroups[i]['client_id']==$("#group-id").val()){
              if (~bgroups[i]['business_group_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([bgroups[i]["business_group_id"],bgroups[i]["business_group_name"]]);     
          }      
      }
      var str='';
      for(var i in suggestions){
        str += '<li id="'+suggestions[i][0]+'" onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
      }
      $('#ac-businessgroup ul').append(str);
     // $("#businessgroupid").val('');
  }
  else{
    $("#businessgroupid").val('');
    $(".ac-textbox").hide();
  }
}

//legalentity autocomplete function
function getLegalEntityAutocomplete(textval, listval, callback){
  $("#ac-legalentity").show();
  var lentity = listval;
  var suggestions = [];
  $('#ac-legalentity ul').empty();
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
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-legalentity ul').append(str);
    //$("#legalentityid").val('');
    }else{
      $("#legalentityid").val('');
      $(".ac-textbox").hide();
    }
}

//division autocomplete function
function getDivisionAutocomplete(textval, listval, callback){
  $("#ac-division").show();
  var division = listval;
  var suggestions = [];
  $('#ac-division ul').empty();
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
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-division ul').append(str);
    //$("#divisionid").val('');
    }else{
      $("#divisionid").val('');
      $(".ac-textbox").hide();
    }
}

//unit condition autocomplete function
function getUnitConditionAutocomplete(textval, listval, callback){
  $("#ac-unit").show();
  var unit = listval;
    var suggestions = [];
    $('#ac-unit ul').empty();
    if(textval.length>0){
        for(var i in unit){
          var combineUnitName = unit[i]['unit_code']+"-"+unit[i]['unit_name'];
          if($("#legalentityid").val() != ''){
              if(unit[i]['legal_entity_id'] == $("#legalentityid").val()){
                  if (~unit[i]['unit_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([unit[i]["unit_id"],combineUnitName ]);    
              }       
          }
          else if($("#divisionid").val() != ''){
              if(unit[i]['division_id']==$("#divisionid").val()){
                  if (~unit[i]['unit_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([unit[i]["unit_id"],combineUnitName]);    
              }       
          }
          else{
              if(unit[i]['client_id'] == $("#group-id").val()){
                  if (~unit[i]['unit_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([unit[i]["unit_id"],combineUnitName]);    
              } 
          }        
        }
        var str='';
        for(var i in suggestions){
            str += '<li id="'+suggestions[i][0]+'" onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
        }
        $('#ac-unit ul').append(str);
        //$("#unitid").val('');
    }
    else{
      $("#unitid").val('');
      $(".ac-textbox").hide();
    }
}


//unit autocomplete function
function getUnitAutocomplete(textval, listval, callback){
  $("#ac-unit").show();
  var units = listval;
    var suggestions = [];
    $('#ac-unit ul').empty();
    if(textval.length>0){
        for(var i in units){
          var combineUnitName = '';
          if(units[i]['unit_code'] != undefined){
            combineUnitName = units[i]['unit_code']+"-"+units[i]['unit_name'];
          }else{
            combineUnitName =units[i]['unit_name'];
          }
          if (~combineUnitName.toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([units[i]["unit_id"],combineUnitName]);
        }
        var str='';
        for(var i in suggestions){
            str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
        }
        $('#ac-unit ul').append(str);
        //$("#seatingunit").val('');
        //$("#unit").val('');
        //$("#unitid").val('');
        
    }else{
      $("#seatingunit").val('');
      $("#unit").val('');
      $("#unitid").val('');
      $(".ac-textbox").hide();
    }
}

//reassignuser autocomplete function
function getReassignUserAutocomplete(textval, listval, callback){
  $("#ac-user").show();
  var sUnit = $("#seatingunit").val();
  var assignees = listval;

  var suggestions = [];
  $('#ac-user ul').empty();
  if(textval.length>0){
    for(var i in assignees){
    if(sUnit == '' || sUnit == assignees[i]["seating_unit_id"]){
      if (~assignees[i]["user_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([assignees[i]["user_id"],assignees[i]["user_name"]]);
    }
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';

    }
    $('#ac-user ul').append(str);
    //$("#user").val('');
    }else{
      $("#user").val('');
      $(".ac-textbox").hide();
    }
}

//client statutory autocomplete function
function getClientStatutoryAutocomplete(textval, listval, callback){
  $("#ac-statutory").show();
  var acts = listval;
  var suggestions = [];
  $('#ac-statutory ul').empty();
  if(textval.length>0){
    for(var i in acts){
      if (~acts[i].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([acts[i].replace(/"/gi,'##'),acts[i]]);
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-statutory ul').append(str);
    //$("#act").val('');
    //$("#level1id").val('');
  }else{
    $("#act").val('');
    $("#level1id").val('');
    $(".ac-textbox").hide();
  }
}

//client statutory autocomplete function
function getComplianceTaskAutocomplete(textval, listval, callback){
  $("#ac-compliancetask").show();
  var compliancetasks = listval;
  var suggestions = [];
 $('#ac-compliancetask ul').empty();
  if(textval.length>0){
    for(var i in compliancetasks){
      if (~compliancetasks[i]["compliance_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([compliancetasks[i]["compliance_id"],compliancetasks[i]["compliance_name"]]);
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-compliancetask ul').append(str);
    //$("#compliancetask").val('');
    //$("#complianceid").val('');
    //$("#compliancesid").val('');
  }else{
    $("#compliancetask").val('');
    $("#complianceid").val('');
    $("#compliancesid").val('');
    $(".ac-textbox").hide();
  }
}

//client businessgroup autocomplete function
function getClientBusinessGroupAutocomplete(textval, listval, callback){
  $("#ac-businessgroup").show();
  var bgroups = listval;
  var suggestions = [];
  $('#ac-businessgroup ul').empty();
  if(textval.length>0){
    for(var i in bgroups){
      if (~bgroups[i]["business_group_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([bgroups[i]["business_group_id"],bgroups[i]["business_group_name"]]);
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-businessgroup ul').append(str);
    //$("#businessgroup").val('');
    //$("#businessgroupid").val('');
  }else{
    $("#businessgroup").val('');
    $("#businessgroupid").val('');
    $(".ac-textbox").hide();
  }
}

//client legalentity autocomplete function
function getClientLegalEntityAutocomplete(textval, listval, callback){
  $("#ac-legalentity").show();
  var lentity = listval;
  var suggestions = [];
  $('#ac-legalentity ul').empty();

  if(textval.length>0){
    for(var i in lentity){
      if (~lentity[i]["legal_entity_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([lentity[i]["legal_entity_id"],lentity[i]["legal_entity_name"]]);
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-legalentity ul').append(str);
    //$("#legalentity").val('');
    //$("#legalentityid").val('');
  }else{
    $("#legalentity").val('');
    $("#legalentityid").val('');
    $(".ac-textbox").hide();
  }
}

//client division autocomplete function
function getClientDivisionAutocomplete(textval, listval, callback){
  $("#ac-division").show();
  var division = listval;
  var suggestions = [];
  $('#ac-division ul').empty();
  if(textval.length>0){
    for(var i in division){
      if (~division[i]["division_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([division[i]["division_id"],division[i]["division_name"]]);
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,'+callback+')">'+suggestions[i][1]+'</li>';
    }
    $('#ac-division ul').append(str);
    //$("#division").val('');
    //$("#divisionid").val('');
  }else{
    $("#division").val('');
    $("#divisionid").val('');
    $(".ac-textbox").hide();
  }
}
//autocomplete function callback
function activate_text (element,callback) {
  $(".ac-textbox").hide();
  var ac_id = $(element).attr('id');
  var ac_name = $(element).text();
  var ac_result = [ac_id,ac_name];
  callback(ac_result);
}