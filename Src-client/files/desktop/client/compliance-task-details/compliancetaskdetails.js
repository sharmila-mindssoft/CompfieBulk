var currentCompliances;
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
        currentCompliances = data['compliance_detail']['current_compliances'];
        loadComplianceTaskDetails(currentCompliances);
        loadUpcomingCompliancesDetails(data['compliance_detail']['upcoming_compliances'])
    }
    function onFailure(error){
        console.log(error);
    }
    client_mirror.getComplianceDetail(
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
function loadComplianceTaskDetails(data){
    $('.tbody-compliances-task-list tr').remove();
    var sno = 0;
    var countOverdue = 0;
    var countInprogress = 0;
    $.each(data, function(k, value) {
        if(data[k]['compliance_status'] == "Not Complied" && countOverdue == 0){
            var tableRowHeading = $('#templates .table-compliances-task-list .headingRow');
            var clone = tableRowHeading.clone();
            $('.compliance-types', clone).html("Over due Compliances");      
            $('.tbody-compliances-task-list').append(clone);
            countOverdue++;
        }
        if(data[k]['compliance_status'] == "Inprogress" && countInprogress == 0){
            var tableRowHeading = $('#templates .table-compliances-task-list .headingRow');
            var clone = tableRowHeading.clone();
            $('.compliance-types', clone).html("Inprogress Compliances");      
            $('.tbody-compliances-task-list').append(clone);
            countInprogress++;
        }

        var tableRowvalues = $('#templates .table-compliances-task-list .table-row-list');
        var cloneval = tableRowvalues.clone();
        sno = sno + 1;
        $('.sno', cloneval).text(sno);
        $('.compliance-task span', cloneval).html(data[k]['compliance_name']);
        $('.compliance-task', cloneval).attr("title", data[k]['compliance_description']);
        $('.domain', cloneval).html(data[k]['domain_name']);
        $('.startdate', cloneval).html(data[k]['start_date']);
        $('.duedate', cloneval).html(data[k]['due_date']);
        $('.days-text', cloneval).html(data[k]['ageing']);
        if(data[k]['compliance_status'] == "Not Complied"){
            $('.days-text', cloneval).attr("style", "color:#f00;");
        }
        $('.status', cloneval).html(data[k]['compliance_status']);
        $('.format-file', cloneval).attr("href", data[k]['format_file_name']);
        $('.table-row-list', cloneval).attr("id", "id-"+data[k]['compliance_history_id'])
        $('.tbody-compliances-task-list').append(cloneval);
    });    
}
function loadUpcomingCompliancesDetails(data){
    $('.tbody-upcoming-compliances-list tr').remove();
    var sno = 0;
    $.each(data, function(k, value) {
        var tableRowvalues = $('#templates .table-upcoming-compliances-list .table-row-list');
        var cloneval = tableRowvalues.clone();
        sno = sno + 1;
        $('.uc-sno', cloneval).text(sno);
        $('.uc-compliance-task span', cloneval).html(data[k]['compliance_name']);
        $('.uc-compliance-task', cloneval).attr("title", data[k]['compliance_description']);
        $('.uc-domain', cloneval).html(data[k]['domain_name']);
        $('.uc-startdate', cloneval).html(data[k]['start_date']);
        $('.uc-duedate', cloneval).html(data[k]['due_date']);
        $('.format-file', cloneval).attr("href", data[k]['format_file_name']);
        $('.tbody-upcoming-compliances-list').append(cloneval);
    }); 

}
$(".table-row-list").click(function(){
    var getIdValue = this.id;
    var idValue = getIdValue.split("-");
    console.log(idValue[1]);
});

$(function() {
    initialize();
});
