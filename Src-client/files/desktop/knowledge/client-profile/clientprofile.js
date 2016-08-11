var profiles;
var groupList;
var currentAdminId = null;
var newAdmin = null;
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
    $("#groupsval").focus();
	function onSuccess(data){
		groupList = data['group_companies'];
		profiles = data['profiles'];
	}
	function onFailure(error){
        displayMessage(error);
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
            var list = profiles[key]['profile_detail'];
            var contractFrom = list['contract_from'];
            var contractTo = list['contract_to'];
            var noLicence = list['no_of_user_licence'];
            var remaininglicence = list['remaining_licence'];
            var totaldiskspace = list["total_disk_space"];
            var useddiskspace = list["used_disk_space"];
            var free_space = (totaldiskspace - useddiskspace).toFixed(2);
            $('.contract-start').html(contractFrom);
            $('.contract-expires').html(contractTo);
            $('.space-summary').html(free_space+" GB free of "+totaldiskspace+" GB");
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
                employeeName = lists[key]['user_name'];
                $('.sno', clone).text(sno);
                $('.employee', clone).text(employeeName);
                $('.email', clone).text(lists[key]['email_id']);
                if(lists[key]['contact_no'] == null){
                  $('.mobile-number', clone).text("-");
                }
                else{
                  $('.mobile-number', clone).text(lists[key]['contact_no']);
                }
                if(lists[key]["is_service_provider"] == false && lists[key]['seating_unit_name'] != '-'){
                    $('.seating-unit span', clone).html(lists[key]['seating_unit_name']);
                    $('.seating-unit abbr', clone).attr("title", lists[key]['address']);
                }
                else{
                    $('.seating-unit', clone).html("-");
                }
                var userId = lists[key]['user_id'];
                var isAdmin = lists[key]["is_admin"];
                var isActive = lists[key]["is_active"];
                var isServiceProvider = lists[key]["is_service_provider"];
                /*if(isActive == true){
                    imageName = "icon-active.png";
                    title = "Click here to deactivate"
                    statusVal = false;
                }
                else{
                  imageName = "icon-inactive.png";
                  title = "Click here to Activate"
                  statusVal = true;
                }*/
                if(isAdmin == true){
                    currentAdminId = userId;
                    // adminstatus = false;
                    imageadminName = "promote-active.png";
                    admintitle = "Click here to deactivate Promote Admin";
                    // if(isActive == false){
                    //     imageadminName = "icon-inactive.png";
                    // }
                }
                else{
                    // adminstatus = true;
                    imageadminName = "promote-inactive.png";
                    admintitle = "Click here to Promote Admin";
                    if(isActive == false){
                        imageadminName = "icon-inactive.png";
                    }
                }
                // $('.is-active', clone).html('<img src="/images/'+imageName+'" title="'+title+'" onclick="clientprofile_active('+userId+','+groupId+', '+statusVal+')"/>');
                if(isActive == true){
                    $('.is-active', clone).html("Active");
                }else{
                    $('.is-active', clone).html("Inactive");
                }

                if(isServiceProvider == false){
                    if(isAdmin == true){
                        $('.promote-admin', clone).html('<img src="/knowledge/images/'+imageadminName+'" title="'+admintitle+'" onclick="alertUserToPromoteAnotherAdmin('+isActive+')" />');
                    }else{
                        $('.promote-admin', clone).html('<img src="/knowledge/images/'+imageadminName+'" title="'+admintitle+'" onclick="clientprofile_isadmin('+userId+','+groupId+',\''+employeeName+'\')" />');
                    }

                }
                $('.tbody-clientprofile-list').append(clone);
            });
        }

    });
}

function dismissPopup(){
    $('.overlay').css("visibility","hidden");
    $('.overlay').css("opacity","0");
}

function clientprofile_active(userId, clientId, status){

    var msgstatus = message.deactive_message;
    if(status){
        msgstatus = message.active_message;
    }
    $( ".warning-confirm" ).dialog({
        title: message.title_status_change,
        buttons: {
            Ok: function() {
                $( this ).dialog( "close" );

                function onSuccess(data){
                    initialize();
                }
                function onFailure(error){
                    if(error == "ReassignFirst"){
                        custom_alert("Cannot Promote this user as Client admin. \nSince the old admin has compliances under him. \n Inform client to reassign those compliances to another user.");
                    }else{
                        displayMessage(error)
                    }
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

function alertUserToPromoteAnotherAdmin(isActive){
    if (isActive == true){
        custom_alert("Try Promote another person as Client admin. \nCurrent admin will be deactivated automatically");
    }else{
        custom_alert("Cannot Change status of inactive administrator");
    }
}

function clientprofile_isadmin(userId, clientId, userName){
    function onSuccess(data){
        // initialize();
        //$('#groupsval').val('');
        function onSuccess(data){
            groupList = data['group_companies'];
            profiles = data['profiles'];
            $("#group-id").val(clientId);
            loadClientProfileList(clientId)
        }
        function onFailure(error){
            displayMessage(error);
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
    function failure(error){
        if(error == "ReassignFirst"){
            custom_alert("Cannot Promote this user as Client admin. \nSince the old admin has compliances under him. \nFirst inform admin to reassign those compliances to another user.");
        }
    }
    mirror.createNewAdmin(userId, clientId, currentAdminId, userName,
        function(error, response){
            if(error == null){
                onSuccess(response);
            }
            else{
                failure(error);
            }
        }
    );
}

//retrive form autocomplete value
function onGroupSuccess(val){
  $("#groupsval").val(val[1]);
  $("#group-id").val(val[0]);
  $('.list-container').show();
  loadClientProfileList(val[0]);
}

//load form list in autocomplete text box
$("#groupsval").keyup(function(e){
  var textval = $(this).val();
  getGroupAutocomplete(e, textval, groupList, function(val){
    onGroupSuccess(val)
  })
});

$(function() {
  initialize();
});

$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});

$( document ).tooltip({
    position: {
        my: "center bottom-20",
        at: "center top",
        using: function( position, feedback ) {
            $( this ).css( position );
            $( "<div>" )
                .addClass( "arrow" )
                .addClass( feedback.vertical )
                .addClass( feedback.horizontal )
                .appendTo( this );
        }
    }
});