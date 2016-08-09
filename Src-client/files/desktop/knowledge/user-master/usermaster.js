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
$("#employeename").focus();
});

// Edit process
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
			var address = '';
			if(usersList[entity]["address"] != null && usersList[entity]["address"] != 'None') address = usersList[entity]["address"];

			var mergeContactNo = usersList[entity]["contact_no"].split("-");
			var countryCode = mergeContactNo[0];
			var areaCode = mergeContactNo[1];
			var contactNo = mergeContactNo[2];
			var userGroup = usersList[entity]["user_group_id"];
			var userGroupval;
			var designation = '';
			if(usersList[entity]["designation"] != null && usersList[entity]["designation"] != 'None') designation = usersList[entity]["designation"];

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

// activate/deactivate process
function changeStatus (userId,isActive) {

	var msgstatus = message.deactive_message;
	if(isActive){
	    msgstatus = message.active_message;
	}
	$( ".warning-confirm" ).dialog({
	    title: message.title_status_change,
	    buttons: {
	        Ok: function() {
	            $( this ).dialog( "close" );

	            function onSuccess(response){
					getUsers();
					$(".filter-text-box").val('');
				}
				function onFailure(error){
					custom_alert(error)
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
	        },
	        Cancel: function() {
	            $( this ).dialog( "close" );
	        }
	    },
	    open: function ()  {
	        $(".warning-message").html(msgstatus);
	    }
	});
}

// display user list in view page
function loadUserList(usersList) {
	var j = 1;

  	$(".tbody-user-list").find("tr").remove();
  	$.each(usersList, function(key, value) {
  		var userId = value["user_id"];
    	var employeeName = value["employee_name"];
    	var employeeId = value["employee_code"];
    	var isActive = value["is_active"];
    	var designation = value["designation"];
    	if (designation == "None" || designation == null){
    		designation = "-"
    	}
    	for(var k in userGroupsList){
    		if(userGroupsList[k]["user_group_id"] == value["user_group_id"]){
    			usergroup = userGroupsList[k]["user_group_name"];
    		break;
	    	}
	    }
    
	    var passStatus = null;
	    var classValue = null;

	    if(isActive == true) {
	      passStatus = false;
	      classValue = "active-icon";
	    }
	    else {
	      passStatus=true;
	      classValue = "inactive-icon";
	    }

	   	var tableRow=$('#templates .table-user-master .table-row');
	    var clone=tableRow.clone();
	    $('.sno', clone).text(j);
	    $('.employee-name', clone).html(employeeId + ' - ' + employeeName);
	    $('.user-group', clone).text(usergroup);
	    $('.designation', clone).text(designation);

	    $('.edit-icon').attr('title', 'Edit');
	    $(".edit-icon", clone).on("click", function() {
	        displayEdit(userId);
	    });

	    $(".status", clone).addClass(classValue);
	    $('.active-icon').attr('title', 'Deactivate');
	    $('.inactive-icon').attr('title', 'Activate');
	    $(".status", clone).on("click", function() {
	        changeStatus(userId, passStatus);
	    });

	    $('.tbody-user-list').append(clone);
	    j = j + 1;
	});
}

// get users list from api
function getUsers(){
	function onSuccess(data){
		usersList = data["users"];
		domainsList = data["domains"];
		userGroupsList = data["user_groups"];
		countriesList = data["countries"];
		loadUserList(usersList);
	}
	function onFailure(error){
		custom_alert(error);
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

//validation
function validate(){
	var checkLength = userValidate();
  	if(checkLength){
  		var employeeName = $("#employeename").val().trim();
		var employeeId = $("#employeeid").val().trim();
		var contactNo = $("#contactno").val().trim();
		var userGroup = '';
		if($("#usergroup").val()!='')
			userGroup = parseInt($("#usergroup").val());
		var emailId = $("#emailid").val().trim();
		var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;

		if(employeeName.length == 0) {
			displayMessage(message.employeename_required);
			$("#employeename").focus();
		} else if(employeeId.length == 0) {
			displayMessage(message.employeeid_required);
			$("#employeeid").focus();
		} else if(emailId.length == 0) {
			displayMessage(message.emailid_required);
			$("#emailid").focus();
		} else if(userGroup.length == 0) {
			displayMessage(message.usergroup_required);
			$("#usergroupval").focus();
		} else if(reg.test(emailId) == false) {
			displayMessage(message.invalid_emailid);
			$("#emailid").focus();
		} else if(countryIds.length == 0) {
			displayMessage(message.country_required);
			$("#countryselected").focus().click();
		} else if(domainIds.length == 0) {
			displayMessage(message.domain_required);
			$("#domainselected").focus().click();
	  	}else{
	    	displayMessage('');
	    	return true
	  	}
  	}
}

// save or update user details
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
   				$(".filter-text-box").val('');
			}
			function onFailure(error){
				if(error == "EmailIDAlreadyExists"){
		           displayMessage(message.emailid_exists);
		        }
		        else if(error == "ContactNumberAlreadyExists"){
		            displayMessage(message.contactno_exists);
		        }
		        else if(error == "EmployeeCodeAlreadyExists"){
		            displayMessage(message.employeeid_exists);
		        }else{
		        	displayMessage(error);
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
				$(".filter-text-box").val('');
 			}
			function failure(data) {
				if(error == "EmailIDAlreadyExists"){
            	displayMessage(message.emailid_exists);
        }
        if(error == "ContactNumberAlreadyExists"){
            displayMessage(message.contactno_exists);
        }
        if(error == "EmployeeCodeAlreadyExists"){
            displayMessage(message.employeeid_exists);
        }
        if(error == "InvalidUserId"){
            displayMessage(message.invalid_userid);
        }
			}
			userDetail = [userId,userGroup,employeeName,employeeId,countryCode+'-'+areaCode+'-'+contactNo,address, designation,countryIds,domainIds];
			userDetailDict = mirror.getUpdateAdminUserDict(userDetail);
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

function onArrowKeyUser(e, ac_item){
  if (e.keyCode != 40 && e.keyCode != 38 && e.keyCode != 13) {
    chosen_user = "";
  }

  if (e.keyCode == 40) {
      if(chosen_user === "") {
          chosen_user = 0;
      } else if((chosen_user+1) < $('#' + ac_item + ' li').length) {
          chosen_user++;
      }
      $('#' + ac_item + ' li').removeClass('auto-selected');
      $('#' + ac_item + ' li:eq('+chosen_user+')').addClass('auto-selected');

      return false;
  }
  if (e.keyCode == 38) {
      if(chosen_user === "") {
          chosen_user = 0;
      } else if(chosen_user > 0) {
          chosen_user--;
      }
      $('#' + ac_item + ' li').removeClass('auto-selected');
      $('#' + ac_item + ' li:eq('+chosen_user+')').addClass('auto-selected');
      return false;
  }
  if (e.keyCode == 13) {
  	var ms_id = $('#' + ac_item + ' li:eq('+chosen_user+')').attr('id');
  	var chkstatus = $('#' + ac_item + ' li:eq('+chosen_user+')').attr('class');

  	if(ac_item == 'ulist'){
  		$('#' + ac_item + ' li:eq('+chosen_user+')').removeClass('auto-selected');
		if(chkstatus == 'active_selectbox'){
			$('#' + ac_item + ' li:eq('+chosen_user+')').removeClass("active_selectbox");
			var remove = domainIds.indexOf(parseInt(ms_id));
	    	domainIds.splice(remove,1);
		}else{
			$('#' + ac_item + ' li:eq('+chosen_user+')').addClass("active_selectbox");
			domainIds.push(parseInt(ms_id));
		}
		$("#domainselected").val(domainIds.length+" Selected");
  	}else{
  		$('#' + ac_item + ' li:eq('+chosen_user+')').removeClass('auto-selected');
		if(chkstatus == 'active_selectbox_country'){
			$('#' + ac_item + ' li:eq('+chosen_user+')').removeClass("active_selectbox_country");
			var remove = countryIds.indexOf(parseInt(ms_id));
	    	countryIds.splice(remove,1);
		}else{
			$('#' + ac_item + ' li:eq('+chosen_user+')').addClass("active_selectbox_country");
			countryIds.push(parseInt(ms_id));
		}
		$("#countryselected").val(countryIds.length+" Selected");
  	}
    return false;
  }
}

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

var chosen_user = '';
$("#domainselected").keyup(function(e){
	onArrowKeyUser(e, 'ulist')
});

$("#countryselected").keyup(function(e){
	onArrowKeyUser(e, 'ulist-country')
});

//check & uncheck process
function activate(element){
	var chkstatus = $(element).attr('class');
	if(chkstatus == 'active_selectbox'){
		$(element).removeClass("active_selectbox");
		var remove = domainIds.indexOf(parseInt(element.id));
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
   	var remove = countryIds.indexOf(parseInt(element.id));
    countryIds.splice(remove,1);
   }else{
    $(element).addClass("active_selectbox_country");
     countryIds.push(parseInt(element.id))
   }
   $("#countryselected").val(countryIds.length+" Selected");
  }


//retrive usergroup autocomplete value
function onUserGroupSuccess(val){
  $("#usergroupval").val(val[1]);
  $("#usergroup").val(val[0]);
  $("#usergroupval").focus();
}

//load usergroup list in autocomplete text box
$("#usergroupval").keyup(function(e){
  var textval = $(this).val();
  getUserGroupAutocomplete(e, textval, userGroupsList, function(val){
    onUserGroupSuccess(val)
  })
});

//initialize
$(document).ready(function(){
	getUsers();
	$("#employeename").focus();
});

$('#employeename').on('input', function (e) {
    this.value = isCommon_Name($(this));
});
$('#employeeid').on('input', function (e) {
    this.value = isCommon($(this));
});
$('#address').on('input', function (e) {
    this.value = isCommon_Address($(this));
});
$('#designation').on('input', function (e) {
    this.value = isCommon($(this));
});
$('#contactno').on('input', function (e) {
    this.value = isNumbers($(this));
});
$('#areacode').on('input', function (e) {
    this.value = isNumbers($(this));
});
$('#countrycode').on('input', function (e) {
    this.value = isNumbers_Countrycode($(this));
});