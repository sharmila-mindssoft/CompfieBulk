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
        var m_names = new Array("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec");
        var d = new Date();
        var curr_date = d.getDate();
        var curr_month = d.getMonth();
        var curr_year = d.getFullYear();
         if(curr_date < 10) {
            curr_date = "0"+curr_date;
        }
        var todaydate = curr_date + "-" + m_names[curr_month] + "-" + curr_year;
        var currentDate = new Date(new Date().getTime() - 24 * 60 * 60 * 1000 * 7);
        var day = currentDate.getDate()
        var month = currentDate.getMonth()
        var year = currentDate.getFullYear()
        if(day < 10) {
            day = "0"+day;
        }
        var lastdate = day + "-" + m_names[month] + "-" + year;

        $("#to-date").val(todaydate);
        $("#from-date").val(lastdate);
        $("#show-button").trigger("click");
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
function datetonumber(datetime){
    var date = datetime.substring(0,11);
    var timeval = datetime.substring(12,18);
    var date1 = date.split("-");
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    for(var j = 0; j < months.length; j++){
        if(date1[1] == months[j]){
             date1[1] = months.indexOf(months[j])+1;
         }                      
    } 
    if(date1[1] < 10){
        date1[1] = '0'+date1[1];
    }                        
    var formattedDate = date1[2]+"/"+date1[1]+"/"+date1[0];
    var newdate = new Date(formattedDate+" "+timeval);
    return Date.parse(newdate);
}
function showrecord(){
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
        fromdate = fromdate+" 00:00:00";
        todate = todate+" 23:59:59";
        $('.grid-table').show();
        $('.tbody-login-trace-list tr').remove();
        var sno = 0;
        $.each(logintraceList, function(key, value) {
            var formname;            
            if(logintraceList[key]['action'].substring(0, 6) == "Log In"){
                formname = "Login"
            }
            else{
                formname = "Logout"
            }
            
            if((datetonumber(fromdate) <= datetonumber(logintraceList[key]['created_on'])) && (datetonumber(todate) >= datetonumber(logintraceList[key]['created_on'])) && userid == ''){ 
                var tableRow = $('#templates .table-logintrace-list .table-row');
                var clone = tableRow.clone();
                $('.date-time', clone).text(logintraceList[key]['created_on']);
                $('.form-name', clone).text(formname);
                $('.info-text', clone).text(logintraceList[key]['action']);
                $('.tbody-login-trace-list').append(clone);
                sno++;
            }
            if((datetonumber(fromdate) <= datetonumber(logintraceList[key]['created_on'])) && (datetonumber(todate) >= datetonumber(logintraceList[key]['created_on'])) && userid == logintraceList[key]['user_id']){ 
                var tableRow= $('#templates .table-logintrace-list .table-row');
                var clone= tableRow.clone();
                $('.date-time', clone).text(logintraceList[key]['created_on']);
                $('.form-name', clone).text(formname);
                $('.info-text', clone).text(logintraceList[key]['action']);
                $('.tbody-login-trace-list').append(clone);
                sno++;
            }
        });
        $(".total-records").html("Total : "+sno+" records")
    }
}

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
        var getemployeeidname = user[i]['employee_code']+"-"+user[i]['employee_name'];
        if (~getemployeeidname.toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([user[i]["employee_code"],user[i]["employee_name"],user[i]["employee_code"]]);  
    }
    var str='';
    for(var i in suggestions){
      str += '<li id="'+suggestions[i][0]+'" onclick="activate_user(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\', \''+suggestions[i][2]+'\')">'+suggestions[i][2]+'-'+suggestions[i][1]+'</li>';
    }
    $('#autocompleteview-user ul').append(str);
    $("#userid").val('');
    }
}
function activate_user (element,checkval,checkname, concatunit) {
  $("#userval").val(concatunit+'-'+checkname);
  $("#userid").val(checkval);
}
$(function() {
    initialize();
});
