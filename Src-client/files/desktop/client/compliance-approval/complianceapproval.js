var approvalList;
var file_list = [];

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
        console.log(data);
        closeicon();
        approvalList = data['approval_list'];
        loadComplianceApprovalDetails(approvalList);     
    }
    function onFailure(error){
        console.log(error);
    }
    client_mirror.getComplianceApprovalList(
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

function loadComplianceApprovalDetails(data){
    $('.tbody-compliance-approval-list tr').remove();
    var sno = 1;
    $.each(data, function(key, value) {
        var tableRowHeading = $('#templates .table-compliance-approval-list .headingRow');
        var clone = tableRowHeading.clone();
        $('.heading', clone).html(value["assignee_name"]);      
        $('.tbody-compliance-approval-list').append(clone);
        complianceList = value['compliances'];
        //Full Width list append ---------------------------------------------------------------
        $.each(complianceList, function(k, val) {
            var tableRowvalues = $('#templates .table-compliance-approval-list .table-row-list');
            var clonelist = tableRowvalues.clone();
            $('.sno-ca', clonelist).html(sno);
            $('.compliance-task span', clonelist).html(val['compliance_name']);
            $('.compliance-task', clonelist).attr("title", val['description']);
            $('.domain', clonelist).html(val['domain_name']);
            $('.startdate', clonelist).html(val['start_date']);
            $('.duedate', clonelist).html(val['due_date']);
            if(val['delayedby'] == null){
                $('.delayedby', clonelist).html('');    
            }
            if(val['delayedby'] != null){
                $('.delayedby', clonelist).html(val['delayedby']+" days");    
            }
            var compliance_history_id = val['compliance_history_id'];  

            $(clonelist, ".expand-compliance").on("click", function() {
                showSideBar(compliance_history_id, val);
            });
            $('.full-width-list .tbody-compliance-approval-list').append(clonelist);   
            sno = sno + 1;
        });      
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
    $('.validity1_label').show();
    $('.duedate1_label').show();
    $('.validity1_textbox').hide();
    $('.duedate1_textbox').hide();
    var tableRowSide = $('#templates .sideview-div');
    var cloneValSide = tableRowSide.clone();
    var complianceFrequency = data['compliance_frequency'];
    $('.sideview-compliance-task span', cloneValSide).html(data['compliance_name']);
    $('.sideview-compliance-frequency', cloneValSide).html(complianceFrequency);
    $('.sidebar-uploaded-documents span', cloneValSide).html();
    $('.sidebar-uploaded-date', cloneValSide).html(data['upload_date']);
    $('.sidebar-completion-date', cloneValSide).html(data['completion_date']);
    if(complianceFrequency != 'One Time'){
        $('.validityAndDueDate').show();
        $(cloneValSide, '.duedate1_icon').on("click", function(e, data){  
            showTextbox();
        }); 
        $('.validity1_label abbr', cloneValSide).html(data[key]['validity_date']);
        $('.duedate1_label abbr', cloneValSide).html(data[key]['next_due_date']); 
        $('.validity1-textbox-input', cloneValSide).val(data[key]['validity_date']);
        $('.duedate1-textbox-input', cloneValSide).val(data[key]['next_due_date']); 
    }    
    if(data['delayedby'] != null){
        $('.sideview-status', cloneValSide).html("Not Complied");    
    }
    if(data['delayedby'] == null){
        $('.sideview-status', cloneValSide).html("InProgress");    
    }
    
    $('.sideview-remarks', cloneValSide).html(data['remarks']);
    var action = data['action'];
    if(action == "Approve"){
        $(".action-tr").show();
        //$(".sidebar-remarks-textarea").show();
    }
    if(action == "Concur"){
        $(".concurrance-tab").show();
        $(".sidebar-concurrance").html(data['remarks']);
        $(".action-tr").show();
        $('.sidebar-remarks-textarea').show();
    }
    if(action == "Reject Concurrence"){
        
    }
    if(action == "Reject Approval"){
        
    }

    // if(data[k]['compliance_frequency'] == 'One Time') {
    //     $('.validityAndDueDate', cloneValSide).hide();
    // }
    // if(data[k]['compliance_frequency'] != 'One Time'){
    //     $('.validityAndDueDate').show();
    //     $(cloneValSide, '.validity1_icon').on("click", function(e, complianceStatus){  
    //         showTextbox(complianceStatus);
    //     }); 
    //     $('.validity1_label abbr', cloneValSide).html(data[key]['validity_date']);
    //     $('.duedate1_label abbr', cloneValSide).html(data[key]['next_due_date']); 
    //     $('.validity1-textbox-input', cloneValSide).val(data[key]['validity_date']);
    //     $('.duedate1-textbox-input', cloneValSide).val(data[key]['next_due_date']);  
    // }
    // $('.btn-submit', cloneValSide).on("click", function(e){
    //     var completion_date;
    //     var compliance_history_id;
    //     var documents;
    //     var validity_date;
    //     var next_due_date;
    //     compliance_history_id = data[k]['compliance_history_id'];
       
    //     documents = file_list;
    //     if(documents.length == 0){
    //         documents = null;
    //     }

    //     completion_date = $('.sideview-completion-date').val();
    //     validity_date = $('.validity1_label abbr').html();
    //     if(validity_date == ''){
    //         validity_date = $('.validity1-textbox-input').val();
    //         if(validity_date == ''){
    //             validity_date = null;
    //         }
    //     }
    //     next_due_date = $('.duedate1_label').val();
    //     if(next_due_date == ''){
    //         next_due_date = $('.duedate1-textbox-input').val();
    //         if(next_due_date == ''){
    //             next_due_date = null;
    //         }
    //     }
    //     remarks = $('.sideview-remarks').val();

    //     if(remarks == ''){
    //         remarks = null;
    //     }
    //     if(completion_date == ''){
    //         displayMessage("Select Completion Date");
    //     }
    //     else if(validity_date == ''){
    //         displayMessage("Select Completion Date");
    //     }
    //     else{
    //         function onSuccess(data){
    //             initialize();
    //         }
    //         function onFailure(error){
    //             console.log(error);
    //         }
    //         client_mirror.updateComplianceDetail(compliance_history_id, documents,
    //             completion_date, validity_date, next_due_date, remarks,
                
    //             function (error, response){
    //                 if(error == null){
    //                     onSuccess(response);
    //                 }
    //                 else{
    //                     onFailure(error);
    //                 }
    //             }    
    //         );   
    //     }
         
    // });
    $('.full-width-list .half-width-task-details').append(cloneValSide);   
    $(".datepick" ).datepicker({
        changeMonth: true,
        changeYear: true,
        numberOfMonths: 1,
        dateFormat: "dd-M-yy",
        monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],  
    });
}

function showTextbox(){
    $('.validity1_textbox').show();
    $('.validity1_label').hide();
    $('.duedate1_textbox').show();
    $('.duedate1_label').hide();
}
function closeicon(){
    $('.half-width-task-details').hide();
    $('.full-width-list').attr("width", "100%");
    $('.half-width-task-details').attr("width", "0%");
}

function uploadedfile(e){
    client_mirror.uploadFile(e, function result_data(data) {
        if(data != 'File max limit exceeded' || data != 'File content is empty'){
            uploadFile = data;
            file_list = data
            var result = ""
            for(i = 0; i < data.length; i++){   
                var filename = data[i]['file_name']             
                result += "<span class='"+filename+"'>" + filename + "<img src='/images/delete.png' class='removeicon' style='width:16px;height:16px;' onclick='remove_temp_file(\""+filename+"\")' /></span>"; 
            }
            $(".uploaded-filename").html(result);

        }
        else{
          alert(data);
        }
    });
}
function remove_temp_file(classnameval){
    console.log(classnameval);
    $('.'+classnameval).remove();
}

 

$(function() {
    initialize();
});
