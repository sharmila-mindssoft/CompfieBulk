$(document).ready(function(){
	function success(status,data){
		alert("success");
	}
	function failure(data){
	}
		 /*var None =null;
	     var mappingdata ={
                "country_id": 1,
                "domain_id": 1,
                "industry_ids": [1,2],
                "statutory_nature_id": 1,
                "statutory_ids": [1,2],
                "compliances":[
                                        { 
                        "statutory_provision": "Rule 10, Section 1, Sub-Sec 1A",
                        "compliance_task": "Notice of Opening",
                        "description": "Within 30 days of opening a branch", 
                        "document": "Form I", 
                        "format_file_name": "", 
                        "penal_consequences": "Imprisonment With Fine", 
                        "compliance_frequency": "OneTime", 
                        "statutory_dates": [
                            {
                                "statutory_date": 9,
                                "statutory_month": 7,
                                "trigger_before_days": 30
                            },
                        ],
                        "repeats_type": None, 
                        "repeats_every": None, 
                        "duration_type": None,
                        "duration": None,
                        "is_active": 1
                    },
                    { 
                        "statutory_provision": "Rule 3, Section 1, Sub-Sec 1A",
                        "compliance_task": "Dealer Registration",
                        "description": "Within 30 days of opening a branch", 
                        "document": "Form I", 
                        "format_file_name": "", 
                        "penal_consequences": "Imprisonment With Fine", 
                        "compliance_frequency": "Periodical", 
                        "statutory_dates": [
                            {
                                "statutory_date": 9,
                                "statutory_month": 7,
                                "trigger_before_days": 30
                            },
                        ],
                        "repeats_type": "Year", 
                        "repeats_every": 1, 
                        "duration_type": None,
                        "duration": None,
                        "is_active": 1
                    },
                    { 
                        "statutory_provision": "Rule 11, Section 12, Sub-Sec 1A",
                        "compliance_task": "Dealer Registration",
                        "description": "Within 30 days of opening a branch", 
                        "document": "Form I", 
                        "format_file_name": "", 
                        "penal_consequences": "Imprisonment With Fine", 
                        "compliance_frequency": "OnOccurrence", 
                        "statutory_dates": [
                            {
                                "statutory_date": 9,
                                "statutory_month": 7,
                                "trigger_before_days": 30
                            },
                        ],
                        "repeats_type": None, 
                        "repeats_every": None, 
                        "duration_type": "Day",
                        "duration": 30,
                        "is_active": 1
                    }
                    
                ],
                "geography_ids":[2]
            }

	mirror.saveStatutoryMapping(mappingdata, success, failure);*/

	 {
                "statutory_level_id": 2,
                "statutory_name": "Tamil Nadu Gratuity Act, 1972",
                "parent_ids": [1]
            }
            mirror.saveStatutory(1,"Tamil Nadu Gratuity Act, 1972",[0], success, failure);
});

function GetStatutories(){
	function success(status,data){
		/*tempUsersList = data["users"];
		usersList = data["users"];
		domainsList = data["domains"];
		userGroupsList = data["user_groups"];
		countriesList = data["countries"];
		loadUserList(usersList);*/
	}
	function failure(data){
	}
	mirror.getStatutoryMappings(success, failure);
}
function loadUserList(usersList) {
	/*var j = 1;
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
      	}*/
      }

      function displayAdd () {
	    $("#error").text('');
	    $("#listview").hide();
	    $("#addview").show();
	}

	function changeStatus (userId,isActive) {
		/*mirror.changeAdminUserStatus("AdminAPI", userId, isActive, success, failure);
		function success(status,data){
			GetUsers();
			$("#error").text("Status Changed Successfully");
		}
		function failure(data){
		}*/
	}

	/*//filter process
	function filter (){
		var employeenamefilter = $("#employeenamefilter").val().toLowerCase();
		var usergroupfilter = $("#usergroupfilter").val().toLowerCase();
		var designationfilter = $("#designationfilter").val().toLowerCase();
		var filteredList=[];
		for(var entity in tempUsersList) {
				employeeName = tempUsersList[entity]["employee_name"];
				designation = tempUsersList[entity]["designation"];
				var userGroup='';
				for(var k in userGroupsList){
					if(userGroupsList[k]["user_group_id"] == tempUsersList[entity]["user_group_id"]){
						userGroup = userGroupsList[k]["user_group_name"];
						break;
					}
				}
				if (~employeeName.toLowerCase().indexOf(employeenamefilter) && ~designation.toLowerCase().indexOf(designationfilter) && ~userGroup.toLowerCase().indexOf(usergroupfilter)) 
				{
					filteredList.push(tempUsersList[entity]);
				}		
		}
		loadUserList(filteredList);
	}*/

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
		  		if(domains[i]["is_active"] == 1){
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
		  		if(countries[i]["is_active"] == 1){
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
		      if (~usergroups[i]["user_group_name"].toLowerCase().indexOf(textval.toLowerCase()) && usergroups[i]["is_active"] == 1) suggestions.push([usergroups[i]["user_group_id"],usergroups[i]["user_group_name"]]); 
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