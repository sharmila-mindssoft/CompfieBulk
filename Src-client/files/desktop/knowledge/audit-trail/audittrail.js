var auditTrailList;
var formList;
var userList;
var finalList;
var pageSize;
var startCount;
var endCount;
var tempadlist;

var sno = 0;
var formid;
var userid;
var fromDateValue;
var toDateValue;
var userIdValue;
var formIdValue;

function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
}

function clearMessage() {
    $(".error-message").hide();
    $(".error-message").text("");
}
function displayMessage(message) {
    $(".error-message").text(message);
    $(".error-message").show();
}

function initialize(){
    var m_names = new Array("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec");
    var d = new Date();
    var curr_date = d.getDate();
    var curr_month = d.getMonth();
    var curr_year = d.getFullYear();
    if(curr_date < 10){ curr_date ='0'+curr_date; }
    var todaydate = curr_date + "-" + m_names[curr_month] + "-" + curr_year;
    var currentDate = new Date(new Date().getTime() - 24 * 60 * 60 * 1000 * 7);
    var day = currentDate.getDate()
    var month = currentDate.getMonth()
    var year = currentDate.getFullYear()
    if(day < 10){ day ='0'+day; }
    var lastdate = day + "-" + m_names[month] + "-" + year;

    $("#to-date").val(todaydate);
    $("#from-date").val(lastdate);

    var userid = null;
    var formid = null;

    fromDateValue = $("#from-date").val();
    toDateValue = $("#to-date").val();
    userIdValue = $("#userid").val();
    formIdValue = $("#formid").val();

    if($("#user").val().trim() == ''){
        userIdValue = '';
    }
    if($("#formname").val().trim() == ''){
        formIdValue = '';
    }
    
    if(fromDateValue == ''){
        displayMessage(message.fromdate_required);
    }
    else if(toDateValue == ''){
        displayMessage(message.todate_required);
    }
    else{
        $(".tbody-audittrail-list").find("tr").remove();
        $('.grid-table').show();
        sno = 0;    
        apipass(lastdate, todaydate, userid, formid, sno);   
    }
}
function apipass(lastdate, todaydate, userid, formid, sno){
    function onSuccess(data){
        if(data['audit_trail_details'] != ''){
            auditTrailList = data['audit_trail_details'];
            formList = data['forms'];
            userList = data['users'];      
            loadrecord(auditTrailList); 
        }
        else{
            $("#pagination").hide();
            if(sno == 0){
                $(".tbody-audittrail-list").html("<tr><td colspan='4' align='center'>No record found.</td></tr>");    
            }            
        }
    }
    function onFailure(error){
        displayMessage(error);
    }
    mirror.getAuditTrail(lastdate, todaydate, userid, formid, sno,
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

function getUserName(userId){
    var userName;
    if(userId != 0){
        $.each(userList, function(key){
            if(userList[key]['user_id'] == userId){
                userName = userList[key]['employee_name'];
            }
        });
        return userName;    
    }
    else{
        userName = "Admin";
        return userName;
    }    
}
function getFormName(formId){
    var formName;
    $.each(formList, function(key){
        if(formList[key]['form_id'] == formId){
            formName = formList[key]['form_name'];
        }
    });
    return formName;
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
 function showaudittrailclick(){
    $(".tbody-audittrail-list").find("tr").remove();
    $('.grid-table').show();
    sno = 0;
    $('#pagination').show();

    fromDateValue = $("#from-date").val();
    toDateValue = $("#to-date").val();
    userIdValue = $("#userid").val();
    formIdValue = $("#formid").val();

    if($("#user").val().trim() == ''){
        userid = null;
    }
    else{
        userid = parseInt(userIdValue);
    }
    if($("#formname").val().trim() == ''){
        formid = null;
    }
    else{
        formid = parseInt(formIdValue);
    }
    
    if(fromDateValue == ''){
        displayMessage(message.fromdate_required);
    }
    else if(toDateValue == ''){
        displayMessage(message.todate_required);
    }
    else{
       apipass(fromDateValue, toDateValue, userid, formid, sno);   
    }
   
 }

function loadrecord(auditTrailList){
    $.each(auditTrailList, function (key, value){
        loadaudittrail(value);
    });
    //$("#total-records").html('Total : '+sno+' records');
}


function loadaudittrail(tempadlist){    
    if(typeof tempadlist['action'] != "undefined"){
        sno++;
        var tableRow = $('#templates .table-audittrail-list .tableRow');
        var clone = tableRow.clone();
        $('.username', clone).text(getUserName(tempadlist['user_id']));
        $('.datetime', clone).text(tempadlist['date']);
        var dispFormname = 'Login';
        if(tempadlist['action'] != ''){
            if (tempadlist['action'].indexOf('password') >= 0){
                dispFormname = 'Change Password';
            }
        }        

        if(tempadlist['form_id'] != 0){
            dispFormname = getFormName(tempadlist['form_id']);
        }
        $('.formname', clone).text(dispFormname);
        $('.action', clone).text(tempadlist['action']);
        $('.tbody-audittrail-list').append(clone);    
    }
}
$('#pagination').click(function(){
    displayLoader();    
    clearMessage(); 

       
    if(userIdValue.trim() == ''){
        var userid = null;
    }
    else{
        var userid = parseInt(userIdValue);
    }
    if(formIdValue.trim() == ''){
        var formid = null;
    }
    else{
        var formid = parseInt(formIdValue);
    }
    

    function onSuccess(data){    
        if(data['audit_trail_details'] ==''){
            $('#pagination').hide();
        }
     
        loadrecord(data['audit_trail_details']);
        hideLoader();
    }
    function onFailure(error){
        displayMessage(error);
        hideLoader();
    }
    mirror.getAuditTrail(fromDateValue, toDateValue, userid, formid, sno, 
        function (error, response) {
            if (error == null){
                onSuccess(response);
            }
            else {
                onFailure(error);
            }
        });
});


//retrive user autocomplete value
function onUserSuccess(val){
    $("#user").val(val[1]);
    $("#userid").val(val[0]);
}

//load user list in autocomplete text box  
$("#user").keyup(function(){
    var textval = $(this).val();
    getUserAutocomplete(textval, userList, function(val){
        onUserSuccess(val);
    })
});

//retrive form autocomplete value
function onFormSuccess(val){
    $("#formname").val(val[1]);
    $("#formid").val(val[0]);
}

//load form list in autocomplete text box  
$("#formname").keyup(function(){
    var textval = $(this).val();
    getFormAutocomplete(textval, formList, function(val){
        onFormSuccess(val);
    });
});

$(function() {
    initialize();
});

