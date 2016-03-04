var profiles;
var groupList;

function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}
function initialize(){
    $('#groupsval').val('');
	function onSuccess(data){
		groupList = data['group_companies'];
		profiles = data['profiles'];
	}
	function onFailure(error){
        console.log(error);
	}
	mirror.getClientProfile(
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
function loadClientProfileList(groupId){
    $(".tbody-clientprofile-list").find("tr").remove();
 	var sno = 0;
	var imageName, title;
    $.each(profiles, function(key, value){
        if(profiles[key]['client_id'] == groupId){
            var list=profiles[key]['profile_detail'];
            var contractFrom = list['contract_from'];
            var contractTo = list['contract_to'];
            var noLicence = list['no_of_user_licence'];
            var remaininglicence = list['remaining_licence'];
            var totaldiskspace = list["total_disk_space"];
            var useddiskspace = list["used_disk_space"];    
            $('.contract-start').html(contractFrom);
            $('.contract-expires').html(contractTo);    
            $('.space-summary').html(useddiskspace+" GB of "+totaldiskspace+" GB used");
            var calculate = ((useddiskspace/totaldiskspace)*100).toFixed(2);
            
            var balance = 100-calculate;
            if(calculate !='0.00'){
                $('.usedspace').css("width", calculate+"%");
                $('.totalspace').css("width", balance+"%");
                $('.totalspace').html(balance+"%");
                $('.usedspace').html(calculate+"%");
            }
            else{
                $('.usedspace').hide();
                $('.totalspace').css("width", balance+"%");
                $('.totalspace').html(balance+"%");
            }
            $('.remaining-licence').html(remaininglicence);

            var lists = list['licence_holders'];
            $.each(lists, function(key, val) { 
                var tableRow = $('#templates .table-clientprofile-list .table-row');
                var clone = tableRow.clone();
                sno = sno + 1;
                $('.sno', clone).text(sno);
                $('.employee', clone).text(lists[key]['employee_name']);
                $('.email', clone).text(lists[key]['email_id']);
                if(lists[key]['contact_no'] == null){
                  $('.mobile-number', clone).text("-");  
                }
                else{
                  $('.mobile-number', clone).text(lists[key]['contact_no']);
                }     
                $('.seating-unit', clone).text(lists[key]['unit_name']);
                $('.unit-address', clone).text(lists[key]['address']);      
                var userId = lists[key]['user_id'];
                var isAdmin = lists[key]["is_admin"];
                var isActive = lists[key]["is_active"];
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
                if(isAdmin == true){
                    adminstatus = false;
                    imageadminName = "promote-active.png";
                    admintitle = "Click here to deactivate Promote Admin";
                }
                else{
                    adminstatus = true; 
                    imageadminName = "promote-inactive.png";
                    admintitle = "Click here to Promote Admin";
                }
                $('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="clientprofile_active('+userId+','+groupId+', '+statusVal+')"/>');
                $('.promote-admin', clone).html('<img src="/images/'+imageadminName+'" title="'+admintitle+'" onclick="clientprofile_isadmin('+userId+', '+adminstatus+')" />');
                $('.tbody-clientprofile-list').append(clone);
            });
        }
         
    });	
      
    
}
function clientprofile_active(userId, clientId, status){
    function onSuccess(data){
        initialize();
    }
    function onFailure(error){
    }
    mirror.changeClientUserStatus(userId, status,
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
function clientprofile_isadmin(userId, isAdmin){
    function onSuccess(data){
        initialize();
    }
    function failure(error){
        console.log(error);
    }
    mirror.changeAdminStatus(userId, isAdmin,
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
        if(groups[i]['is_active'] == true){
            if (~groups[i]['group_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([groups[i]["client_id"],groups[i]["group_name"]]);       
        }      
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