var approvalList;
var file_list = [];
var action;
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
        closeicon();
        approvalList = data['approval_list'];
        currentDate = data['current_date'];
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
            $('.compliance-task abbr', clonelist).attr("title", val['description']);
            //$('.compliance-task', clonelist).attr("title", val['description']);
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
                //$(".table-row-list", clonelist).addClass("active1");
                // tableRowvalues.addClass("active1");
                clearMessage(); 
                $(".table-row-list").removeClass("active1");
                $(clonelist, ".table-row-list").addClass("active1");
                showSideBar(compliance_history_id, val);
            });
            $('.full-width-list .tbody-compliance-approval-list').append(clonelist);   
            sno = sno + 1;
        });      
    });    
}

function showSideBar(idval, data){
    var fileslist = [];
    var documentslist = [];
    $(".half-width-task-details").empty();
    $(".half-width-task-details").show();
    $(".full-width-list").attr("width", "60%");
    $(".half-width-task-details").attr("width", "40%");

    //SideView append ---------------------------------------------------------------------
    var tableRowSide = $('#templates .sideview-div');
    var cloneValSide = tableRowSide.clone();
    var complianceFrequency = data['compliance_frequency'];
    $(".validityAndDueDate", cloneValSide).hide();  
    $('.sidebar-unit span', cloneValSide).html(data['unit_name']);
   // $('.sidebar-unit abbr', cloneValSide).attr("title", data['address']);
    $('.sidebar-compliance-task span', cloneValSide).html(data['compliance_name']);
    $('.sidebar-compliance-task abbr', cloneValSide).attr("title", data['description']);
    $('.sidebar-compliance-frequency', cloneValSide).html(complianceFrequency);
    fileslist = data['file_names'];
    documentslist = data['documents'];
    if( fileslist != null){
        for (var i = 0; i < fileslist.length; i++){
            if(fileslist[i] != ""){
                $('.sidebar-uploaded-documents', cloneValSide).append("<span><abbr class='sidebardocview'>"+fileslist[i]+"</abbr><a href='' download='"+documentslist[i]+"' class='download-file' ><img src='/images/download.png' style='width:16px;height:16px' title='Download' /></a><a href='"+ documentslist[i] +"' target='_new' class='view-file'> <img src='/images/view.png' style='width:16px;height:16px;' title='View' /></a></span>");        
            }     
        }    
    }
    // $(".view-file", cloneValSide).on("click", function(e){
    //     $(".view-file", cloneValSide).attr("target", "_new");
    //     $(".view-file", cloneValSide).attr("href", documentslist[i]);
    // }); 
    // $(".download-file", cloneValSide).on("click", function(e){        
    //     $(".download-file", cloneValSide).attr("target", "_new");
    //     $(".download-file", cloneValSide).attr("href", documentslist[i]);
    // }); 
    $('.sidebar-uploaded-date', cloneValSide).html(data['upload_date']);
    $('.sidebar-completion-date', cloneValSide).html(data['completion_date']);
    if(complianceFrequency != 'One Time'){       
        $(".validitydate1_textbox", cloneValSide).hide();
        $(".validitydate1_label", cloneValSide).show();
        $(".duedate1_textbox", cloneValSide).hide();
        $(".duedate1_label", cloneValSide).show();

        $(".validityAndDueDate", cloneValSide).show();        
        $(".validitydate1_label", cloneValSide).html(data['validity_date']);
        $(".duedate1_label abbr ", cloneValSide).html(data['next_due_date']); 
        $(".validity1-textbox-input", cloneValSide).val(data['validity_date']);
        $(".duedate1-textbox-input", cloneValSide).val(data['next_due_date']); 
        $(".duedate1_icon", cloneValSide).on("click", function(e, data){  
            showTextbox();
        });        
    }
    else if(complianceFrequency == "On Occurrence"){
        $(".validityAndDueDate", cloneValSide).hide();
    }

    
    if(data['delayedby'] != null){
        $(".sidebar-status", cloneValSide).html("Not Complied");    
    }
    if(data['delayedby'] == null){
        $(".sidebar-status", cloneValSide).html("InProgress");    
    }
    if(data["remarks"] != "None"){
        $(".sidebar-remarks span", cloneValSide).html(data["remarks"]);    
    }
    
    action = data["action"];
    if(action == "Approve"){
        $(".action-tr", cloneValSide).show();
        
        $(".concurr-action", cloneValSide).hide();
        $(".approval-action", cloneValSide).show();
        if(data['concurrenced_by'] != null){
             $(".concurrance-tab", cloneValSide).show();
             $(".sidebar-concurrence span", cloneValSide).html(data['concurrenced_by']);
        }
        $(".approval-action", cloneValSide).on("change", function(e, data){ 
            if($(".approval-action", cloneValSide).val() == 'Reject'){
                $(".sidebar-remarks-textarea", cloneValSide).val();
            }
            else if($(".approval-action", cloneValSide).val() == "Reject Approval"){
                $(".sidebar-remarks-textarea", cloneValSide).show();
            }
            else{
                $(".sidebar-remarks-textarea", cloneValSide).hide();
            }
        }); 
    }
    if(action == "Concur"){
        //$(".concurrance-tab", cloneValSide).show();
    
        $(".concurr-action", cloneValSide).show();
        $(".approval-action", cloneValSide).hide();
        
        //$(".sidebar-concurrence span", cloneValSide).html(data['concurrenced_by']);               
        $(".action-tr", cloneValSide).show();
        $(".concurr-action", cloneValSide).on("change", function(e, data){ 
            if($(".concurr-action option:selected", cloneValSide).val() == 'Reject Concurrence'){
                $(".sidebar-remarks-textarea", cloneValSide).show();
            }
            else{
                $(".sidebar-remarks-textarea", cloneValSide).hide();
            }
        });  
    }
    if(action == "Reject Concurrence"){
        $(".concurrance-tab", cloneValSide).show();
        $(".sidebar-concurrance", cloneValSide).html(data['remarks']);
        $(".action-tr", cloneValSide).show();

        $(".concurr-action", cloneValSide).show();
        $(".approval-action", cloneValSide).hide();
        
        $(".sidebar-remarks-textarea", cloneValSide).show();
        $(".concurr-action", cloneValSide).on("change", function(e, data){ 
            if($(".concurr-action option:selected", cloneValSide).val() == 'Reject Concurrence'){
                $(".sidebar-remarks-textarea", cloneValSide).show();
            }
            else{
                $(".sidebar-remarks-textarea", cloneValSide).hide();
            }
        });    
    }
    if(action == "Reject Approval"){

        $(".action-tr", cloneValSide).show();   

        $(".concurr-action", cloneValSide).hide();
        $(".approval-action", cloneValSide).show();

        $(".sidebar-remarks-textarea", cloneValSide).show(); 
        $(".approval-action", cloneValSide).on("change", function(e, data){ 
            if($(".approval-action option:selected", cloneValSide).val() == 'Reject'){
                $(".sidebar-remarks-textarea", cloneValSide).show();
            }
            else{
                $(".sidebar-remarks-textarea", cloneValSide).hide();
            }
        });   
    }
    $(function() {
        // $(".datepick" ).datepicker({
        //     changeMonth: true,
        //     changeYear: true,
        //     numberOfMonths: 1,
        //     dateFormat: "dd-M-yy",
        //     monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        //     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],  
        // });
        $(".validity1-textbox-input", cloneValSide).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],  
        });
        $(".duedate1-textbox-input", cloneValSide).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],  
        });
    });
    function parseMyDate(s) {
        return new Date(s.replace(/^(\d+)\W+(\w+)\W+/, '$2 $1 '));
    }
               
    $('.btn-submit', cloneValSide).on("click", function(e){
        var compliance_history_id;
        var approval_status;
        var remarks = '';
        var next_due_date;
        var validity_date;
        compliance_history_id = data['compliance_history_id'];
        if(action  ==  "Approve"){
            approval_status = $(".approval-action option:selected").val();        
        }
        if(action  ==  "Concur"){
            approval_status = $(".concurr-action option:selected").val();        
        }
        if(action  ==  "Reject Concurrence"){
            approval_status = $(".concurr-action option:selected").val();        
        }
        if(action  ==  "Reject Approval"){
            approval_status = $(".approval-action option:selected").val();        
        }
        console.log(approval_status);
        
        if(approval_status == ''){
            displayMessage("Select Any Action");
            return false;
        }
        else if(approval_status == "Reject"){
            remarks = $(".remarks-textarea", cloneValSide).val();
        }
        else if(approval_status == "Reject Approval"){
            remarks = $(".remarks-textarea").val();
        }

        validity_date = $('.validitydate1_label', cloneValSide).html();
        
        if(validity_date == ''){
            validity_date = $('.validity1-textbox-input', cloneValSide).val();
            if(validity_date == ''){
                validity_date = null;
            }
        }
        next_due_date = $('.duedate1_label abbr', cloneValSide).val();
        if(next_due_date == ''){
            next_due_date = $('.duedate1-textbox-input', cloneValSide).val();
            if(next_due_date == ''){
                next_due_date = null;
            }
        }
       

        if(remarks == ''){
            remarks = null;
        }
        else if(typeof remarks == 'undefined'){
            remarks = null;
        }      
        else if(validity_date == ''){
            displayMessage("Select Validity Date");
            return;
        }
        else if(next_due_date == ''){
            displayMessage("Select Next Due Date");
            return;
        }
        if(validity_date != null  && next_due_date != null){
            if(parseMyDate(validity_date) > parseMyDate(next_due_date)){
                displayMessage("Validity Date is Greater than or equal to Due Date");
                return;
            }
        }
        // if(currentDate != null && validity_date != null){
        //     if(parseMyDate(currentDate) > parseMyDate(next_due_date)){
        //         displayMessage("Validity Date is Greater than Current Date");
        //         return;
        //     }
        // }
        function onSuccess(data){
            clearMessage();
            if(approval_status == "Reject Concurrence"){
                displayMessage("Compliance Concurrence Rejected");    
            }
            else if(approval_status == "Reject Approval"){
                displayMessage("Compliance Approval Rejected");    
            }
            else if(approval_status == "Approve"){
                displayMessage("Compliance Approved");    
            }
            else if(approval_status == "Concur"){
                displayMessage("Compliance Concurred");    
            }            
            initialize();
        }
        function onFailure(error){
            displayMessage(error);
        }
        client_mirror.approveCompliance(compliance_history_id, approval_status,
            remarks, validity_date, next_due_date,                
            function (error, response){
                if(error == null){
                    onSuccess(response);
                }
                else{
                    onFailure(error);
                }
            }    
        );   
       
    });

    $('.half-width-task-details').append(cloneValSide);   
   
}

function showTextbox(){
    $(".validitydate1_textbox").show();
    $(".validitydate1_label").hide();
    $(".duedate1_textbox").show();
    $(".duedate1_label").hide();
}
function hideTextbox(){
    $(".validitydate1_textbox").hide();
    $(".validitydate1_label").show();
    $(".duedate1_textbox").hide();
    $(".duedate1_label").show();
}
function closeicon(){
    $(".half-width-task-details").hide();
    $(".full-width-list").attr("width", "100%");
    $(".half-width-task-details").attr("width", "0%");
}

function uploadedfile(e){

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