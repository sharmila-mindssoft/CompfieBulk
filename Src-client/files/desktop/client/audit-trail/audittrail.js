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
var fromdate;
var todate;

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
    function onSuccess(data){
        auditTrailList = data['audit_trail_details'];
        formList = data['forms'];
        userList = data['users'];

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
        showaudittrailclick();
    }
    function onFailure(error){
        console.log(error);
    }
    client_mirror.getAuditTrail(sno,
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

// function get_sub_array(object, start, end){
//     if(!end){ end=-1;}
//     return object.slice(start, end);
// }

// $('#pagination').click(function(e){
//     startCount = endCount;
//     endCount = startCount + pageSize;
//     var sub_act_list =  tempadlist;
//     var sub_keys_list = get_sub_array(sub_act_list, startCount, endCount);
//     if(sub_keys_list.length < pageSize){
//         $('#pagination').hide();
//     }
//     //alert(startCount + '-' + endCount + '-' +sub_keys_list.length)
//     loadaudittrail(sub_keys_list);
//     e.preventDefault();
// });

// function loadresult(tempadlist) {
//     pageSize = 50;
//     startCount = 0;
//     endCount = pageSize;

//     if(tempadlist.length > pageSize){
//         $('#pagination').show();
//     }else{
//         $('#pagination').hide();
//     }

//     var sub_keys_list = get_sub_array(tempadlist, startCount, endCount);
//     loadaudittrail(sub_keys_list);
// }
function loadaudittrail(tempadlist){    
    console.log(tempadlist['action']);
    var tableRow = $('#templates .table-audittrail-list .tableRow');
    var clone = tableRow.clone();
    $('.username', clone).text(sno+getUserName(tempadlist['user_id']));
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
$('#pagination').click(function(){
    displayLoader();    
    clearMessage();    

    function onSuccess(data){    
        if(data['audit_trail_details'] ==''){
            $('#pagination').hide();
        }
        loadrecord(data['audit_trail_details'], fromdate, todate, userid, formid);
        hideLoader();
    }
    function onFailure(error){
        console.log(error);
        hideLoader();
    }
    client_mirror.getAuditTrail(sno, 
    function (error, response) {
      if (error == null){
        onSuccess(response);
      }
      else {
        onFailure(error);
      }
    });
});

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
    var fromDateValue = $("#from-date").val();
    var toDateValue = $("#to-date").val();
    var userIdValue = $("#userid").val();
    var formIdValue = $("#formid").val();
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
        var sno = 0;
        tempadlist = [];
        loadrecord(auditTrailList, fromDateValue, toDateValue, userIdValue, formIdValue);      
        loadaudittrail(tempadlist);
    }
}

function loadrecord(auditTrailList, fromDateValue, toDateValue, userIdValue, formIdValue){

      $.each(auditTrailList, function (key, value){
            var fromDateVal = fromDateValue+" 00:00:00";
            var toDateVal = toDateValue+" 23:59:59";
            var auditDateVal = value['date'];

            var auditUser = value['user_id'];
            var auditFormId = value['form_id'];

            var formCheckval;
            var userCheckval;
            //userid empty, formid empty            
            if((datetonumber(fromDateVal) <= datetonumber(auditDateVal)) && (datetonumber(toDateVal) >= datetonumber(auditDateVal)) && userIdValue == '' && formIdValue == ''){ 
                sno++;
                loadaudittrail(value);
            }
            //userid empty
            else if((datetonumber(fromDateVal) <= datetonumber(auditDateVal)) && (datetonumber(toDateVal) >= datetonumber(auditDateVal)) && (userIdValue == '') && (formIdValue == auditFormId)){   
                sno++;
                loadaudittrail(value);
            }
            //formid empty
            else if((datetonumber(fromDateVal) <= datetonumber(auditDateVal)) && (datetonumber(toDateVal) >= datetonumber(auditDateVal)) && userIdValue == auditUser && formIdValue == ''){ 
                sno++;
                loadaudittrail(value);  
            }
            //all != empty
             else if((datetonumber(fromDateVal) <= datetonumber(auditDateVal)) && (datetonumber(toDateVal) >= datetonumber(auditDateVal)) && userIdValue == auditUser && formIdValue == auditFormId){   
                sno++;
                loadaudittrail(value);
            }
        });
        $("#total-records").html('Total : '+sno+' records');

}


//retrive user autocomplete value
function onUserSuccess(val){
  $("#user").val(val[1]);
  $("#userid").val(val[0]);
}

//load user list in autocomplete text box  
$("#user").keyup(function(){
  var textval = $(this).val();
  getUserAutocomplete(textval, userList, function(val){
    onUserSuccess(val)
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
    onFormSuccess(val)
  })
});

$(function() {
    initialize();
});

