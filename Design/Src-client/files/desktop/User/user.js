var usersList;
var domainsList;
var userGroupsList;
var tempUsersList;
var countriesList;

$(document).ready(function(){
	GetUsers()
});

function GetUsers(){
	function success(status,data){
		tempUsersList = data["users"];
		usersList = data["users"];
		domainsList = data["domains"];
		userGroupsList = data["user_groups"];
		countriesList = data["countries"];
		loadUserList(usersList);
	}
	function failure(data){
	}
	mirror.getAdminUserList("AdminAPI", success, failure);
}
function loadUserList(usersList) {
	var j = 1;
	var imgName = '';
    var passStatus = '';
    var userId = 0;
    var employeeName = '';
    var isActive = 0;
    var designation = '';
    var userList;

   $(".tbody-user-list").find("tr").remove();
    for(var entity in usersList) {
    	userId = usersList[entity]["user_id"];
        employeeName = usersList[entity]["employee_name"];
        isActive = usersList[entity]["is_active"];
        designation = usersList[entity]["designation"];
        for(var k in userGroupsList){
        	if(userGroupsList[k]["user_group_id"] == usersList[entity]["user_group_id"]){
        		usergroup = userGroupsList[k]["user_group_name"];
        		break;
        	}
        }
        if(isActive == 1) {
        	passStatus="0";
        	imgName="icon-active.png"
        }
        else {
        	passStatus="1";
       	 	imgName="icon-inactive.png"
       	 }
       	  var tableRow=$('#templates .table-user-master .table-row');
	      var clone=tableRow.clone();
	      $('.sno', clone).text(j);
	      $('.employee-name', clone).text(employeeName);
	      $('.user-group', clone).text(usergroup);
	      $('.designation', clone).text(designation);
	      $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+userId+',\''+employeeName+'\')"/>');
	      $('.status', clone).html('<img src=\'/images/'+imgName+'\' onclick="changeStatus('+userId+','+passStatus+')"/>');
	      $('.tbody-user-list').append(clone);
	      j = j + 1;
      	}
      }

      function displayAdd () {
      	$("#listview").hide();
	    $("#addview").show();
	    $("#userid").val('');
		$("#employeename").val('');
	    $("#employeeid").val('');
	    $("#address").val('');
	    $("#countrycode").val('');
	    $("#areacode").val('');
	    $("#contactno").val('');
	    $("#usergroup").val('');
	    $("#designation").val('');
	    $("#domain").val('');
	    $("#domainselected").val('');
	    $("#country").val('');
	    $("#countryselected").val('');
	    $("#emailid").val('');
	    $("#error").text('');
	}

	function changeStatus (userId,isActive) {
		mirror.changeAdminUserStatus("AdminAPI", userId, isActive, success, failure);
		function success(status,data){
			GetUsers();
			$("#error").text("Status Changed Successfully");
		}
		function failure(data){
		}
	}
	function saveRecord () {
		$("#error").text("");
		var userId = parseInt($("#userid").val());
		var employeeName = $("#employeename").val();
		var employeeId = $("#employeeid").val();
		var address = $("#address").val();
		var countryCode = $("#countrycode").val();
		var areaCode = $("#areacode").val();
		var contactNo = $("#contactno").val();
		var userGroup = parseInt($("#usergroup").val());
		var designation = $("#designation").val();
		var domain = $("#domain").val();
		var country = $("#country").val();
		var emailId = $("#emailid").val();

		if(employeeName == '') {
			$("#error").text("Employee Name Required");
		} else if(employeeId == '') {
			$("#error").text("Employee Id Required");
		} else if(contactNo == '') {
			$("#error").text("Contact Number Required");
		} else if(userGroup == '') {
			$("#error").text("User Group Required");
		} else if(domain == '') {
			$("#error").text("Domain Required");
		} else if(emailId == '') {
			$("#error").text("Email Id Required");
		} else if(country == '') {
			$("#error").text("Country Required");
		} else {
			if($("#userid").val() == '') {
				saveUserDetail = [emailId,userGroup,employeeName,employeeId,countryCode+'-'+areaCode+'-'+contactNo,address, designation,country,domain];
				function success(status,data) {
					if(status == 'SaveUserSuccess') {
						GetUsers();
						$("#listview").show();
     					$("#addview").hide();
						$("#error").text("Record Added Successfully");
					} else {
						$("#error").text(status);
					}
				}
				function failure(data){
				}
				mirror.saveAdminUser("AdminAPI", saveUserDetail, success, failure);
			} else {
				updateUserDetail = [userId,userGroup,employeeName,employeeId,countryCode+'-'+areaCode+'-'+contactNo,address, designation,country,domain];
				function success(status,data){
					if(status == 'UpdateUserSuccess') {
						GetUsers();
						$("#listview").show();
      					$("#addview").hide();
						$("#error").text("Record Updated Successfully");
					} else {
						$("#error").text(status);
					}
				}
				function failure(data) {
				}
				mirror.updateAdminUser("AdminAPI", updateUserDetail, success, failure);
			}
		}
	}
	function displayEdit (userId) {
		$("#error").text("");
		$("#listview").hide();
  		$("#addview").show();
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
				var domain = usersList[entity]["domain_ids"]; 
				var country = usersList[entity]["country_ids"];
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
				$("#domain").val(domain);
				var editdomainval = domain.split(",");
				$("#domainselected").val(editdomainval.length+" Selected");
				$("#country").val(country);
				var editcountryval = domain.split(",");
				$("#countryselected").val(editcountryval.length+" Selected");
				$("#emailid").val(emailId);
				break;
			}
		}
	}

	//filter process
	function filter (term, cellNr){
		var filterkey = term.value.toLowerCase();
		var filteredList=[];
		if(cellNr == '1'){
			for(var entity in tempUsersList) {
				employeeName = tempUsersList[entity]["employee_name"];
				if (~employeeName.toLowerCase().indexOf(filterkey)) filteredList.push(tempUsersList[entity]);
			}
		} else if(cellNr == '2') {
			for(var entity in tempUsersList) {
				var userGroup='';
				for(var k in userGroupsList){
					if(userGroupsList[k]["user_group_id"] == tempUsersList[entity]["user_group_id"]){
						userGroup = userGroupsList[k]["user_group_name"];
						break;
					}
				}
				if (~userGroup.toLowerCase().indexOf(filterkey)) filteredList.push(tempUsersList[entity]);
			}
		} else {
			for(var entity in tempUsersList) {
				designation = tempUsersList[entity]["designation"];
				if (~designation.toLowerCase().indexOf(filterkey)) filteredList.push(tempUsersList[entity]);
			}
		}
		loadUserList(filteredList);
	}

	//Autocomplete Script Starts
	//Hide list items after select
	function hidemenu() {
		document.getElementById('selectboxview').style.display = 'none';
		document.getElementById('selectboxview-country').style.display = 'none';
		document.getElementById('autocompleteview').style.display = 'none';
	}
	//load domain list in multi select box
	function loadauto () {
		document.getElementById('selectboxview').style.display = 'block';
		var editdomainval=[];
		if($("#domain").val() != ''){
			editdomainval = $("#domain").val().split(",");
		}
		//if($("#domainselected").val() == ''){
		  	var domains = domainsList;
		  	$('#ulist').empty();
		  	var str='';
		  	for(var i in domains){
		  		var selectdomainstatus='';
		  		for(var j=0; j<editdomainval.length; j++){
		  			if(editdomainval[j]==domains[i]["domain_id"]){
		  				selectdomainstatus='checked';
		  			}
		  		}
		  		if(selectdomainstatus == 'checked'){
		  			str += '<li id="'+domains[i]["domain_id"]+'" class="active_selectbox" onclick="activate(this)" >'+domains[i]["domain_name"]+'</li> ';
		  		}else{
		 			str += '<li id="'+domains[i]["domain_id"]+'" onclick="activate(this)" >'+domains[i]["domain_name"]+'</li> ';
		 		}
		  	}
		    $('#ulist').append(str);
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


		  //load country list in multi select box
		function loadautocountry () {
		document.getElementById('selectboxview-country').style.display = 'block';
		var editcountryval=[];
		if($("#country").val() != ''){
			editcountryval = $("#country").val().split(",");
		}
		  	var countries = countriesList;
		  	$('#ulist-country').empty();
		  	var str='';
		  	for(var i in countries){
		  		var selectcountrystatus='';
		  		for(var j=0; j<editcountryval.length; j++){
		  			if(editcountryval[j]==countries[i]["country_id"]){
		  				selectcountrystatus='checked';
		  			}
		  		}
		  		if(selectcountrystatus == 'checked'){
		  			str += '<li id="'+countries[i]["country_id"]+'" class="active_selectbox_country" onclick="activatecountry(this)" >'+countries[i]["country_name"]+'</li> ';
		  		}else{
		 			str += '<li id="'+countries[i]["country_id"]+'" onclick="activatecountry(this)" >'+countries[i]["country_name"]+'</li> ';
		 		}
		  	}
		    $('#ulist-country').append(str);
		    $("#countryselected").val(editcountryval.length+" Selected")
		}
		//check & uncheck process
		function activatecountry(element){
		   var chkstatus = $(element).attr('class');
		   if(chkstatus == 'active_selectbox_country'){
		   	$(element).removeClass("active_selectbox_country");
		   }else{
		    $(element).addClass("active_selectbox_country");
		   }  
		   var selids='';
		   var totalcount =  $(".active_selectbox_country").length;
		   $(".active_selectbox_country").each( function( index, el ) {
		   	if (index === totalcount - 1) {
		   		selids = selids+el.id;
		   	}else{
		   		selids = selids+el.id+",";
		   	}    
		    });
		   $("#countryselected").val(totalcount+" Selected");
		   $("#country").val(selids);
		  }


		//load usergroup list in autocomplete text box  
		function loadauto_text (textval) {
		  document.getElementById('autocompleteview').style.display = 'block';
		  var usergroups = userGroupsList;
		  var suggestions = [];
		  $('#ulist_text').empty();
		  if(textval.length>0){
		    for(var i in usergroups){
		      if (~usergroups[i]["user_group_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([usergroups[i]["user_group_id"],usergroups[i]["user_group_name"]]); 
		    }
		    var str='';
		    for(var i in suggestions){
		              str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
		    }
		    $('#ulist_text').append(str);
		    $("#usergroup").val('');
		    }
		}
		//set selected autocomplte value to textbox
		function activate_text (element,checkval,checkname) {
		  $("#usergroupval").val(checkname);
		  $("#usergroup").val(checkval);
		}