var profiles;
var groupList;

function initialize(){
  $('#groupsval').val('');
	function success(status, data){
		groupList=data['group_companies'];
		profiles=data['profiles'];
	}
	function failure(status, data){
	}
	mirror.getClientProfile("TechnoAPI", success, failure);
}
function loadClientProfileList(groupId){
  $(".tbody-clientprofile-list").find("tr").remove();
 	var sno=0;
	var imageName, title;	
  var list=profiles[groupId];
  //var list=profiles[groupId];
  var contractFrom=list['contract_from'];
  var contractTo=list['contract_to'];
  var noLicence=list['no_of_user_licence'];
  var remaininglicence=list['remaining_licence'];
  var totaldiskspace=list["total_disk_space"];
  var useddiskspace=list["used_disk_space"];    
  $('.contract-start').html(contractFrom);
  $('.contract-expires').html(contractTo);    
  $('.space-summary').html(useddiskspace+" GB of "+totaldiskspace+" GB used");
  var calculate =((useddiskspace/totaldiskspace)*100).toFixed(2);
  var balance=100-calculate;
  $('.usedspace').css("width", calculate);
  $('.totalspace').css("width", balance);
  $('.totalspace').html(balance+"%");
  $('.usedspace').html(calculate+"%");
  $('.remaining-licence').html(remaininglicence);
  var lists=list['licence_holders'];
  $.each(lists, function(key, val) { 

    var tableRow=$('#templates .table-clientprofile-list .table-row');
    var clone=tableRow.clone();
    sno = sno + 1;
    $('.sno', clone).text(sno);
    $('.employee', clone).text(lists[key]['employee_name']);
    $('.email', clone).text(lists[key]['email_id']);
    if(lists[key]['contact_no']==null){
      $('.mobile-number', clone).text("-");  
    }
    else{
      $('.mobile-number', clone).text(lists[key]['contact_no']);
    }     
    $('.seating-unit', clone).text(lists[key]['unit_name']);
    $('.unit-address', clone).text(lists[key]['address']);      
    var userId=lists[key]['user_id'];
    var isAdmin=lists[key]["is_admin"];
    var isActive=lists[key]["is_active"];
    if(isActive==1){
      imageName="icon-active.png";
      title="Click here to deactivate"
      statusVal=0;
    }
    else{
      imageName="icon-inactive.png";  
      title="Click here to Activate"
      statusVal=1;
    }
    if(isAdmin==1){ adminstatus=0; imageadminName="promote-active.png"; admintitle="Click here to deactivate Promote Admin" }
    else{ adminstatus=1; imageadminName="promote-inactive.png"; admintitle="Click here to Promote Admin"}
    $('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="clientprofile_active('+userId+','+groupId+', '+statusVal+')"/>');
    $('.promote-admin', clone).html('<img src="/images/'+imageadminName+'" title="'+admintitle+'" onclick="clientprofile_isadmin('+userId+', '+adminstatus+')" />');
    
    $('.tbody-clientprofile-list').append(clone);
  });  
    
}
function clientprofile_active(userId, clientId, status){
  function success(status, data){
    initialize();
  }
  function failure(status, data){
  }
  mirror.changeClientUserStatus("ClientAdminAPI", userId, status, success, failure);
}
function clientprofile_isadmin(userId, isAdmin){
  function success(status, data){
    initialize();
  }
  function failure(status, data){
  }
  mirror.changeAdminStatus("ClientAdminAPI", userId, isAdmin, success, failure);
}
function hidelist(){
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
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview ul').append(str);
    $("#group-id").val('');
    }
}
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#groupsval").val(checkname);
  $("#group-id").val(checkval);
  $('.list-container').show();
  loadClientProfileList(checkval);
}


$("#search-employee").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $(".tbody-clientprofile-list").find("tr").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".employee").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});

$("#search-email").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $(".tbody-clientprofile-list").find("tr").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".email").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});

$("#search-mobile-number").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $(".tbody-clientprofile-list").find("tr").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".mobile-number").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});

$("#search-seating-unit").keyup(function() { 
	var count=0;
    var value = this.value.toLowerCase();
    $(".tbody-clientprofile-list").find("tr").each(function(index) {
        if (index === 0) return;
        var id = $(this).find(".seating-unit").text().toLowerCase();       
        $(this).toggle(id.indexOf(value) !== -1);;
    });
});

$(function() {
  initialize();
});