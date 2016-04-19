var auditTrailList;
var formList;
var userList;
var finalList;
var pageSize;
var startCount;
var endCount;
var tempadlist;

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
        $("#show").trigger("click");

    }
    function onFailure(error){
        console.log(error);
    }
    client_mirror.getAuditTrail(
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

function get_sub_array(object, start, end){
    if(!end){ end=-1;}
    return object.slice(start, end);
}

$('#pagination').click(function(e){
    startCount = endCount;
    endCount = startCount + pageSize;
    var sub_act_list =  tempadlist;
    var sub_keys_list = get_sub_array(sub_act_list, startCount, endCount);
    if(sub_keys_list.length < pageSize){
        $('#pagination').hide();
    }
    //alert(startCount + '-' + endCount + '-' +sub_keys_list.length)
    loadaudittrail(sub_keys_list);
    e.preventDefault();
});

function loadresult(tempadlist) {
    pageSize = 50;
    startCount = 0;
    endCount = pageSize;

    if(tempadlist.length > pageSize){
        $('#pagination').show();
    }else{
        $('#pagination').hide();
    }

    var sub_keys_list = get_sub_array(tempadlist, startCount, endCount);
    loadaudittrail(sub_keys_list);
}
function loadaudittrail(tempadlist){
    var sno = 1;
    $.each(tempadlist, function (key, value){
        var tableRow = $('#templates .table-audittrail-list .tableRow');
        var clone = tableRow.clone();
        $('.sno', clone).text(sno++);
        $('.username', clone).text(getUserName(value['user_id']));
        $('.datetime', clone).text(value['date']);
        var dispFormname = 'Login';
        if(value['form_id'] != 0){
            dispFormname = getFormName(value['form_id']);
        }
        $('.formname', clone).text(dispFormname);
        $('.action', clone).text(value['action']);
        $('.tbody-audittrail-list').append(clone);
    });
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
$("#show").click(function(){
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

        $.each(auditTrailList, function (key, value){
            var fromDateVal = fromDateValue+" 00:00:00";
            var toDateVal = toDateValue+" 23:59:59";
            var auditDateVal = auditTrailList[key]['date'];

            var auditUser = value['user_id'];
            var auditFormId = value['form_id'];
            var formCheckval;
            var userCheckval;
            //userid empty, formid empty            
            if((datetonumber(fromDateVal) <= datetonumber(auditDateVal)) && (datetonumber(toDateVal) >= datetonumber(auditDateVal)) && userIdValue == '' && formIdValue == ''){ 
                sno++;
                tempadlist.push(auditTrailList[key]);
            }
            //userid empty
            else if((datetonumber(fromDateVal) <= datetonumber(auditDateVal)) && (datetonumber(toDateVal) >= datetonumber(auditDateVal)) && (userIdValue == '') && (formIdValue == auditFormId)){   
                sno++;
                tempadlist.push(auditTrailList[key]);
            }
            //formid empty
            else if((datetonumber(fromDateVal) <= datetonumber(auditDateVal)) && (datetonumber(toDateVal) >= datetonumber(auditDateVal)) && userIdValue == auditUser && formIdValue == ''){ 
                sno++;
                tempadlist.push(auditTrailList[key]);  
            }
            //all != empty
             else if((datetonumber(fromDateVal) <= datetonumber(auditDateVal)) && (datetonumber(toDateVal) >= datetonumber(auditDateVal)) && userIdValue == auditUser && formIdValue == auditFormId){   
                sno++;
                tempadlist.push(auditTrailList[key]);
            }
        });
        $("#total-records").html('Total : '+sno+' records');
        loadresult(tempadlist);
    }
});
function hidemenu(){
    $("#userListView").hide(); 
}

$("#user").keypress(function(){
    var textval = $(this).val();
    $("#userListView").show();
    var users = userList;
    var suggestions = [];
    $('#userListView ul').empty();
    if(textval.length>0){
        for(var i in users){
            if (~users[i]["employee_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([users[i]["user_id"],users[i]["employee_name"]]); 
        }
        var str='';
        for(var i in suggestions){
            str += '<li id="'+suggestions[i][0]+'"onclick="activate_text(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
        }
        $('#userListView ul').append(str);
        $("#userid").val('');
    }
});
//set selected autocomplte value to textbox
function activate_text (element,checkval,checkname) {
  $("#user").val(checkname);
  $("#userid").val(checkval);
}

function hideMenuFormList(){
    $("#formListView").hide(); 
}

$("#formname").keypress(function(){
    var textval = $(this).val();
    $("#formListView").show();
    var forms = formList;
    var suggestions = [];
    $('#formListView ul').empty();
    if(textval.length>0){
        for(var i in forms){
            if (~forms[i]["form_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([forms[i]["form_id"],forms[i]["form_name"]]); 
        }
        var str='<li id="0" onclick="activate_text1(this,\'0\',\'Login\')">Login</li>';
        for(var i in suggestions){
            str += '<li id="'+suggestions[i][0]+'"onclick="activate_text1(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\')">'+suggestions[i][1]+'</li>';
        }
        $('#formListView ul').append(str);
        $("#formid").val('');
    }
});
//selectedt selected autocomplte value to textbox
function activate_text1 (element,checkval,checkname) {
    $("#formname").val(checkname);
    $("#formid").val(checkval);
}

$(function() {
    initialize();
});

