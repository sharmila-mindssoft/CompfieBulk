var usersList;
var domainsList;
var userGroupsList;
var countriesList;
var domainIds = [];
var countryIds = [];


$(".btn-user-cancel").click(function(){
  $("#user-add").hide();
  $("#user-view").show();
});

$(".btn-user-add").click(function(){
$("#user-view").hide();
$("#user-add").show();
$(".fieldvalue").val('');
$("#view_emailid").hide();
$("#emailid").show();
$("#userid").val('');
domainIds = [];
countryIds = []
displayMessage('');
});

function displayEdit (userId) {
	displayMessage("");
	$("#user-view").hide();
	$("#user-add").show();
	$("#userid").val(userId);
	for(var entity in usersList) {
		if(usersList[entity]["user_id"] == userId){
			var userId = usersList[entity]["user_id"];
			var employeeName = usersList[entity]["employee_name"];
			var employeeId = usersList[entity]["employee_code"];
			var address = usersList[entity]["address"];
			var mergeContactNo = usersList[entity]["contact_no"].split("-");
			var countryCode = mergeContactNo[0];
			var areaCode = mergeContactNo[1];
			var contactNo = mergeContactNo[2];
			var userGroup = usersList[entity]["user_group_id"];
			var userGroupval;
			var designation = usersList[entity]["designation"];
			domainIds = usersList[entity]["domain_ids"]; 
			countryIds = usersList[entity]["country_ids"];
			var emailId = usersList[entity]["email_id"];
			for(var k in userGroupsList){
				if(userGroupsList[k]["user_group_id"] == userGroup){
					userGroupval = userGroupsList[k]["user_group_name"];
					break;
				}
			}
			$("#employeename").val(employeeName);
		    $("#employeeid").val(employeeId);
		  	$("#address").val(address);
		 	$("#countrycode").val(countryCode);
			$("#areacode").val(areaCode);
			$("#contactno").val(contactNo);
			$("#usergroupval").val(userGroupval);
			$("#usergroup").val(userGroup);
			$("#designation").val(designation);
			$("#domainselected").val(domainIds.length+" Selected");
			$("#countryselected").val(countryIds.length+" Selected");
			$("#emailid").hide();
			$("#emailid").val(emailId);
			$("#view_emailid").show();
			$("#view_emailid").text(emailId);
			break;
		}
	}
}

function changeStatus (userId,isActive) {
	var msgstatus='deactivate';
    if(isActive){
      msgstatus='activate';
    }
    var answer = confirm('Are you sure want to '+msgstatus+ '?');
    if (answer)
    {
		function onSuccess(response){
			getUsers();
		}
		function onFailure(error){
			displayMessage(error);
		}
		mirror.changeAdminUserStatus(userId, isActive,
			function (error, response) {
	            if (error == null){
	              onSuccess(response);
	            }
	            else {
	              onFailure(error);
	            }
	        }
	    );
	}
}


function loadUserList(usersList) {
	var j = 1;
	var imgName = '';
  	var passStatus = '';
  	var userId = 0;
  	var employeeName = '';
  	var employeeId = '';
  	var isActive = false;
  	var designation = '';
  	var userList;

  	$(".tbody-user-list").find("tr").remove();
  	for(var entity in usersList) {
  		userId = usersList[entity]["user_id"];
    	employeeName = usersList[entity]["employee_name"];
    	employeeId = usersList[entity]["employee_code"];
    	isActive = usersList[entity]["is_active"];
    	designation = usersList[entity]["designation"];
    	if (designation == "None" || designation == null){
    		designation = "-"
    	}
    	for(var k in userGroupsList){
    		if(userGroupsList[k]["user_group_id"] == usersList[entity]["user_group_id"]){
    			usergroup = userGroupsList[k]["user_group_name"];
    		break;
    	}
    }
    if(isActive == true) {
    	passStatus=false;
    	imgName="icon-active.png"
    }
    else {
    	passStatus=true;
   	 	imgName="icon-inactive.png"
   	 }
   	var tableRow=$('#templates .table-user-master .table-row');
    var clone=tableRow.clone();
    $('.sno', clone).text(j);
    $('.employee-name', clone).html(employeeId + ' - ' + employeeName);
    $('.user-group', clone).text(usergroup);
    $('.designation', clone).text(designation);
    $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+userId+',\''+employeeName+'\')"/>');
    $('.status', clone).html('<img src=\'/images/'+imgName+'\' onclick="changeStatus('+userId+','+passStatus+')"/>');
    $('.tbody-user-list').append(clone);
    j = j + 1;
  }
}

function getUsers(){
	function onSuccess(data){
		usersList = data["users"];
		domainsList = data["domains"];
		userGroupsList = data["user_groups"];
		countriesList = data["countries"];
		loadUserList(usersList);
	}
	function onFailure(error){
	}
	mirror.getAdminUserList(
		function (error, response) {
          if (error == null){
            onSuccess(response);
          }
          else {
            onFailure(error);
          }
      }
  );
}

function validate(){
	var employeeName = $("#employeename").val().trim();
	var employeeId = $("#employeeid").val().trim();
	var contactNo = $("#contactno").val().trim();
	var userGroup = '';
	if($("#usergroup").val()!='')
		userGroup = parseInt($("#usergroup").val());

	var emailId = $("#emailid").val().trim();
	var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

	if(employeeName.length == 0) {
		displayMessage(getMessage('employeename-required'));
		$("#employeename").focus();
	} else if(employeeId.length == 0) {
		displayMessage(getMessage('employeeid-required'));
		$("#employeeid").focus();
	} else if(emailId.length == 0) {
		displayMessage(getMessage('emailid-required'));
		$("#emailid").focus();
	} else if(userGroup.length == 0) {
		displayMessage(getMessage('usergroup-required'));
		$("#usergroupval").focus();
	} else if(reg.test(emailId) == false) {
		displayMessage(getMessage('invalid-emailid'));
		$("#emailid").focus();
	} else if(countryIds.length == 0) {
		displayMessage(getMessage('country-required'));
		$("#countryselected").focus().click();
	} else if(domainIds.length == 0) {
		displayMessage(getMessage('domain-required'));
		$("#domainselected").focus().click();
  	}else{
    	displayMessage('');
    	return true
  }
}

$("#submit").click(function(){
	var userId = parseInt($("#userid").val());
	var employeeName = $("#employeename").val().trim();
	var employeeId = $("#employeeid").val().trim();
	var address = $("#address").val();
	var countryCode = $("#countrycode").val();
	var areaCode = $("#areacode").val();
	var contactNo = $("#contactno").val();
	var userGroup = parseInt($("#usergroup").val());
	var designation = $("#designation").val();
	var emailId = $("#emailid").val().trim();
	if(validate()){
		if($("#userid").val() == '') {
			function onSuccess(response) {
					getUsers();
					$("#user-view").show();
   				$("#user-add").hide();
			}
			function onFailure(error){
				if(error == "EmailIDAlreadyExists"){
            	displayMessage(getMessage('emailid-exists'));
        }
        if(error == "ContactNumberAlreadyExists"){
            displayMessage(getMessage('contactno-exists'));
        }
        if(error == "EmployeeCodeAlreadyExists"){
            displayMessage(getMessage('employeeid-exists'));
        }
			}
			userDetail = [emailId,userGroup,employeeName,employeeId,countryCode+'-'+areaCode+'-'+contactNo,address, designation,countryIds,domainIds];
			userDetailDict = mirror.getSaveAdminUserDict(userDetail);
			mirror.saveAdminUser(userDetailDict,
				function (error, response) {
        if (error == null){
          onSuccess(response);
        }
        else {
          onFailure(error);
        }
      });
		} else {
			function onSuccess(response) {
				getUsers();
				$("#user-add").hide();
				$("#user-view").show();
 			}
			function failure(data) {
				if(error == "EmailIDAlreadyExists"){
            	displayMessage(getMessage('emailid-exists'));
        }
        if(error == "ContactNumberAlreadyExists"){
            displayMessage(getMessage('contactno-exists'));
        }
        if(error == "EmployeeCodeAlreadyExists"){
            displayMessage(getMessage('employeeid-exists'));
        }
        if(error == "InvalidUserId"){
            displayMessage(getMessage('invalid-userid'));
        }
			}
			console.log("address:"+address);
			userDetail = [userId,userGroup,employeeName,employeeId,countryCode+'-'+areaCode+'-'+contactNo,address, designation,countryIds,domainIds];
			userDetailDict = mirror.getUpdateAdminUserDict(userDetail);
			console.log(userDetailDict)
			mirror.updateAdminUser(userDetailDict,
				function (error, response) {
        if (error == null){
          onSuccess(response);
        }
        else {
          onFailure(error);
        }
      });
		}
	}
});

//filter process
$(".filter-text-box").keyup(function() { 
	var employeenamefilter = $("#search-employee-name").val().toLowerCase();
	var usergroupfilter = $("#search-usergroup").val().toLowerCase();
	var designationfilter = $("#search-designation").val().toLowerCase();
	var filteredList=[];
	var concatName = '';
	for(var entity in usersList) {
			employeeName = usersList[entity]["employee_name"];
			designation = usersList[entity]["designation"];
			if(designation == null || designation == 'None'){
				designation = '-';
			}
			employeeId = usersList[entity]["employee_code"];
			concatName = employeeId + ' - ' + employeeName;

			var userGroup='';
			for(var k in userGroupsList){
				if(userGroupsList[k]["user_group_id"] == usersList[entity]["user_group_id"]){
					userGroup = userGroupsList[k]["user_group_name"];
					break;
				}
			}
			if (~concatName.toLowerCase().indexOf(employeenamefilter) && ~designation.toLowerCase().indexOf(designationfilter) && ~userGroup.toLowerCase().indexOf(usergroupfilter)) 
			{
				filteredList.push(usersList[entity]);
			}		
	}
	loadUserList(filteredList);
});

//Autocomplete Script Starts
//Hide list items after select
$(".hidemenu").click(function(){
  $("#autocompleteview").hide(); 
});
$(".hideselect").mouseleave(function(){
  $("#selectboxview").hide(); 
  $("#selectboxview-country").hide(); 
});

//load domain list in multi select box
$("#domainselected").click(function(){
	$("#selectboxview").show();
	var domains = domainsList;
	$('#ulist').empty();
	var str='';
	for(var i in domains){
		if(domains[i]["is_active"] == true){
  		if($.inArray(domains[i]["domain_id"], domainIds) >= 0){
  			str += '<li id="'+domains[i]["domain_id"]+'" class="active_selectbox" onclick="activate(this)" >'+domains[i]["domain_name"]+'</li> ';
  		}else{
 			str += '<li id="'+domains[i]["domain_id"]+'" onclick="activate(this)" >'+domains[i]["domain_name"]+'</li> ';
 		}
		}
	}
  $('#ulist').append(str);
});
//check & uncheck process
function activate(element){
	var chkstatus = $(element).attr('class');
	if(chkstatus == 'active_selectbox'){
		$(element).removeClass("active_selectbox");
		remove = domainIds.indexOf(parseInt(element.id));
    	domainIds.splice(remove,1);
	}else{
		$(element).addClass("active_selectbox");
		domainIds.push(parseInt(element.id));
	}  
	$("#domainselected").val(domainIds.length+" Selected");
 }

//load country list in multi select box
$("#countryselected").click(function(){
	$("#selectboxview-country").show();
	
	var countries = countriesList;
	$('#ulist-country').empty();
	var str='';
	for(var i in countries){
		if(countries[i]["is_active"] == true){
		if($.inArray(countries[i]["country_id"], countryIds) >= 0){
			str += '<li id="'+countries[i]["country_id"]+'" class="active_selectbox_country" onclick="activatecountry(this)" >'+countries[i]["country_name"]+'</li> ';
		}else{
			str += '<li id="'+countries[i]["country_id"]+'" onclick="activatecountry(this)" >'+countries[i]["country_name"]+'</li> ';
		}
	 	}
	}
  $('#ulist-country').append(str);
});
//check & uncheck process
function activatecountry(element){
   var chkstatus = $(element).attr('class');
   if(chkstatus == 'active_selectbox_country'){
   	$(element).removeClass("active_selectbox_country");
   	remove = countryIds.indexOf(parseInt(element.id));
    countryIds.splice(remove,1);
   }else{
    $(element).addClass("active_selectbox_country");
     countryIds.push(parseInt(element.id))
   }  
   
   $("#countryselected").val(countryIds.length+" Selected");
  }

//load usergroup list in autocomplete text box  
$("#usergroupval").keyup(function(){
  var textval = $(this).val();
  $("#autocompleteview").show();
  var usergroups = userGroupsList;
  var suggestions = [];
  $('#ulist_text').empty();
  if(textval.length>0){
    for(var i in usergroups){
      if (~usergroups[i]["user_group_name"].toLowerCase().indexOf(textval.toLowerCase()) && usergroups[i]["is_active"] == true) suggestions.push([usergroups[i]["user_group_id"],usergroups[i]["user_group_name"]]); 
    }
    var str='';
    for(var i in suggestions){
              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
    }
    $('#ulist_text').append(str);
    $("#usergroup").val('');
    }else{
      $("#usergroup").val('');
      $("#autocompleteview").hide();
    }
});
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#usergroupval").val(checkname);
  $("#usergroup").val(checkval);
}

$(document).ready(function(){
	getUsers();
	$("#employeename").focus();
  $('#contactno').keyup('input', function (event) {
      this.value = this.value.replace(/[^0-9]/g, '');
  });

  $('#areacode').keyup('input', function (event) {
      this.value = this.value.replace(/[^0-9]/g, '');
  });

  $('#countrycode').keyup('input', function (event) {
      this.value = this.value.replace(/[^0-9^+]/g, '');
  });
});
