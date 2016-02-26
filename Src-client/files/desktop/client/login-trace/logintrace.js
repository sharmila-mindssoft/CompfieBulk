var userList;
var logintraceList;

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
        userList = data['users'];
        logintraceList = data['login_trace'];
    }
    function onFailure(error){
        console.log(error);
    }
    client_mirror.getLoginTrace(
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
    var userid = $("#userid").val();   
    var fromdate = $("#from-date").val();
    var todate = $("#to-date").val();
    if(fromdate == ''){
        displayMessage(" Select from Date");
    }
    else if(todate ==''){
        displayMessage(" Select to Date");
    }
    else{
        $('.grid-table').show();
        $('.tbody-login-trace-list tr').remove();
        var sno = 0;
        $.each(logintraceList, function(key, value) {
            if((fromdate <= logintraceList[key]['created_on']) && (todate >= logintraceList[key]['created_on']) && userid == ''){ 
                var tableRow = $('#templates .table-logintrace-list .table-row');
                var clone = tableRow.clone();
                $('.date-time', clone).text(logintraceList[key]['created_on']);
                $('.form-name', clone).text(logintraceList[key]['form_name']);
                $('.info-text', clone).text(logintraceList[key]['action']);
                $('.tbody-login-trace-list').append(clone);
                sno++;
            }
            if((fromdate <= logintraceList[key]['created_on']) && (todate >= logintraceList[key]['created_on']) && userid == logintraceList[key]['user_id']){ 
                var tableRow= $('#templates .table-logintrace-list .table-row');
                var clone= tableRow.clone();
                $('.date-time', clone).text(logintraceList[key]['created_on']);
                $('.form-name', clone).text(logintraceList[key]['form_name']);
                $('.info-text', clone).text(logintraceList[key]['action']);
                $('.tbody-login-trace-list').append(clone);
                sno++;
            }
        });
        $(".total-records").html("Total : "+sno+" records")
    }
});

//User---------------------------------------------------------------------------------------------------------------
function hideuserlist(){
    document.getElementById('autocompleteview-user').style.display = 'none';
}
function loadauto_user (textval) {
    if($("#userval").val() == ''){
        $("#userid").val('');
    }
    document.getElementById('autocompleteview-user').style.display = 'block';
    var user = userList;
    var suggestions = [];
    $('#autocompleteview-user ul').empty();
    if(textval.length>0){
        for(var i in user){
            if (~user[i]['employee_name'].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([user[i]["employee_id"],user[i]["employee_name"]]);    
        }
        var str='';
        for(var i in suggestions){
          str += '<li id="'+suggestions[i][0]+'" onclick="activate_user(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
        }
        $('#autocompleteview-user ul').append(str);
        $("#userid").val('');
    }
}
function activate_user (element,checkval,checkname) {
  $("#userval").val(checkname);
  $("#userid").val(checkval);
}

$(function() {
    initialize();
});
