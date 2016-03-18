var currentCompliances;
var file_list = [];
var currentDate;

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
        clearMessage();
        closeicon();
        currentCompliances = data['compliance_detail']['current_compliances'];
        loadComplianceTaskDetails(currentCompliances);
        loadUpcomingCompliancesDetails(data['compliance_detail']['upcoming_compliances'])
        currentDate = data['compliance_detail']['current_date'];
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
    $('.tbody-compliances-task-list-overdue tr').remove();
    $('.tbody-compliances-task-list-inprogress tr').remove();
    clearMessage();
    $('.uploaded-filename').empty();
    var snoOverdue = 1;
    var snoInprogress = 1;
    var countOverdue = 0;
    var countInprogress = 0;
  
    $.each(data, function(k, value) {
        if(data[k]['compliance_status'] == "Not Complied" && countOverdue == 0){
            var tableRowHeading = $('#templates .table-compliances-task-list .headingRow');
            var clone = tableRowHeading.clone();
            $('.compliance-types', clone).html("Over due Compliances");      
            $('.tbody-compliances-task-list-overdue').append(clone);
            countOverdue++;
        }
        if(data[k]['compliance_status'] == "Inprogress" && countInprogress == 0){
            var tableRowHeading = $('#templates .table-compliances-task-list .headingRow');
            var clone = tableRowHeading.clone();
            $('.compliance-types', clone).html("Inprogress Compliances");      
            $('.tbody-compliances-task-list-inprogress').append(clone);
            countInprogress++;
        }

        var tableRowvalues = $('#templates .table-compliances-task-list .table-row-list');
        var cloneval = tableRowvalues.clone();
      
        //Full Width list append ---------------------------------------------------------------
       
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
        if(data[k]['format_file_name']  != null){
            $('.format-file', cloneval).attr("href", data[k]['format_file_name']);    
        }
        else{
            $('.format-file', cloneval).hide();   
        }
        var compliance_history_id = data[k]["compliance_history_id"];
        $(cloneval, ".expand-compliance").on("click", function() {
            showSideBar(compliance_history_id, data);
        });

        if(data[k]['compliance_status'] == "Not Complied"){
            $('.sno', cloneval).text(snoOverdue);
            $('.tbody-compliances-task-list-overdue').append(cloneval);
            snoOverdue = snoOverdue + 1
        }
        if(data[k]['compliance_status'] == "Inprogress" || data[k]['compliance_status'] == "Inprogress(Rejected)"){
            $('.sno', cloneval).text(snoInprogress);
            $('.tbody-compliances-task-list-inprogress').append(cloneval);   
            snoInprogress = snoInprogress + 1
        }      
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
function showSideBar(idval, data){
    $('.half-width-task-details').empty();
    var d = new Date().toLocaleDateString('en-GB', {  
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    }).split(' ').join('-');
    $('.half-width-task-details').show();
    $('.full-width-list').attr("width", "60%");
    $('.half-width-task-details').attr("width", "40%");

    //SideView append ---------------------------------------------------------------------
    $.each(data, function(k, value) {
        if(data[k]['compliance_history_id'] == idval){
            $('.validity1_label').show();
            $('.duedate1_label').show();
            $('.validity1_textbox').hide();
            $('.duedate1_textbox').hide();
            var tableRowSide = $('#templates .sideview-div');
            var cloneValSide = tableRowSide.clone();
            var complianceStatus = data[k]['compliance_status'];
            $('.sideview-compliance-unit span', cloneValSide).html(data[k]['unit_name']);
            $('.sideview-compliance-unit abbr', cloneValSide).attr("title", data[k]['address']);
            $('.sideview-compliance-task .ct', cloneValSide).html(data[k]['compliance_name']);
            $('.sideview-compliance-task abbr', cloneValSide).attr("title", data[k]['compliance_description']);
            $('.sideview-compliance-frequency', cloneValSide).html(data[k]['compliance_frequency']);
            $('.sideview-startdate', cloneValSide).val(data[k]['start_date']);
            $('.sideview-completion-date-td', cloneValSide).html("<input  type='text' class='input-box datepick sideview-completion-date' id='completion-date' readonly='readonly'>");
            $('.sideview-compliance-status', cloneValSide).html(complianceStatus);
            $('.sideview-upload-date', cloneValSide).html(d);
            $('.sideview-remarks-td', cloneValSide).html("<textarea class='input-box sideview-remarks' maxlength='500'></textarea>");
            $("#upload_file", cloneValSide).on("change", function(e) {
                if (e.originalEvent.defaultPrevented) return;
                uploadedfile(e);
            });
            if(data[k]['compliance_frequency'] == 'One Time') {
                $('.validityAndDueDate', cloneValSide).hide();
            }
            if(data[k]['compliance_frequency'] != 'One Time'){
                $('.validityAndDueDate').show();
                $('.validity1_icon', cloneValSide).on("click", function(e, complianceStatus){  
                    showTextbox(complianceStatus);
                }); 
                $('.validity1_label abbr', cloneValSide).html(data[k]['validity_date']);
                $('.duedate1_label abbr', cloneValSide).html(data[k]['next_due_date']); 
                $('.validity1-textbox-input', cloneValSide).val(data[k]['validity_date']);
                $('.duedate1-textbox-input', cloneValSide).val(data[k]['next_due_date']);  
            }
            $('.btn-submit', cloneValSide).on("click", function(e){
                var completion_date;
                var compliance_history_id;
                var documents;
                var validity_date;
                var next_due_date;
                var start_date;
                compliance_history_id = data[k]['compliance_history_id'];
                function parseMyDate(s) {
                    return new Date(s.replace(/^(\d+)\W+(\w+)\W+/, '$2 $1 '));
                }
               
                documents = file_list;
                if(documents.length == 0){
                    documents = null;
                }

                completion_date = $('.sideview-completion-date').val();
                validity_date = $('.validity1_label abbr').html();
                if(validity_date == ''){
                    validity_date = $('.validity1-textbox-input').val();
                    if(validity_date == ''){
                        validity_date = null;
                    }
                }
                next_due_date = $('.duedate1_label').val();
                if(next_due_date == ''){
                    next_due_date = $('.duedate1-textbox-input').val();
                    if(next_due_date == ''){
                        next_due_date = null;
                    }
                }
                remarks = $('.sideview-remarks').val();
                start_date = $('.sideview-startdate').val();

                if(remarks == ''){
                    remarks = null;
                }
                if(completion_date == ''){
                    displayMessage("Select Completion Date");
                    return;
                }
                if(validity_date == ''){
                    displayMessage("Select Validity Date");
                    return;
                }
                if(parseMyDate(start_date) > parseMyDate(completion_date)){
                    displayMessage("Completion Date is Greater than or equal to Start Date");
                    return;
                }
                if(validity_date != null){
                    if(parseMyDate(start_date) > parseMyDate(validity_date)){
                        displayMessage("Validity Date is Greater than or equal to Start Date");
                        return;
                    }
                }
                if(next_due_date != null){
                    if(parseMyDate(start_date) > parseMyDate(next_due_date)){
                        displayMessage("Due Date is Greater than or equal to Start Date");    
                        return;
                    }                    
                }
                if(currentDate != null && validity_date != null){
                    if(parseMyDate(currentDate) > parseMyDate(next_due_date)){
                        displayMessage("Validity Date is Greater than Current Date");
                        return;
                    }
                }
                if(validity_date != null  && next_due_date != null){
                    if(parseMyDate(next_due_date) > parseMyDate(validity_date)){
                        displayMessage("Validity Date is Greater than or equal to Due Date");
                        return;
                    }
                }
                else{
                    displayMessage("Welcome to api");
                    return;
                    function onSuccess(data){
                        initialize();
                    }
                    function onFailure(error){
                        console.log(error);
                    }
                    client_mirror.updateComplianceDetail(compliance_history_id, documents,
                        completion_date, validity_date, next_due_date, remarks,
                        
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
                 
            });
            $('.half-width-task-details').append(cloneValSide);    
        }        
    });
    $(".datepick").datepicker({
        changeMonth: true,
        changeYear: true,
        numberOfMonths: 1,
        dateFormat: "dd-M-yy",
        monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    });
    $(".duedate1-textbox-input").datepicker({
        changeMonth: true,
        changeYear: true,
        numberOfMonths: 1,
        dateFormat: "dd-M-yy",
        monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    });
    $(".validity1-textbox-input").datepicker({
        changeMonth: true,
        changeYear: true,
        numberOfMonths: 1,
        dateFormat: "dd-M-yy",
        monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    });    
}

function showTextbox(complianceStatus){
    $('.duedate1_textbox').show();
    $('.duedate1_label').hide();
    $('.validity1_textbox').show();
    $('.validity1_label').hide();
}
function closeicon(){
    $('.half-width-task-details').hide();
    $('.full-width-list').attr("width", "100%");
    $('.half-width-task-details').attr("width", "0%");
}

function uploadedfile(e){
    client_mirror.uploadFile(e, function result_data(data) {
        if(data == "File max limit exceeded"){
            displayMessage("File max limit exceeded");
            $(".uploaded_filename").html('');
        }
        if(data != 'File max limit exceeded' || data != 'File content is empty'){
            uploadFile = data;
            file_list = data
            var result = ""
            for(i = 0; i < data.length; i++){   
                var fileclassname;
                var filename = data[i]['file_name']   
                fileclassname = filename.replace(/[^\w\s]/gi,"");
                fileclassname = fileclassname.replace(/\s/g, "");
                result += "<span class='"+fileclassname+"'>" + filename + "<img src='/images/delete.png' class='removeicon' style='width:16px;height:16px;' onclick='remove_temp_file(\""+fileclassname+"\")' /></span>"; 
            }
            $(".uploaded-filename").html(result);
        }
        else{
          alert(data);
        }
    });
}
function remove_temp_file(classnameval){
    $('.'+classnameval).remove();
}
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
