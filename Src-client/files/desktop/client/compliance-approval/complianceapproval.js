var approvalList;
var file_list = [];
var action;
var currentDate;
var sno = 0;
var totalRecord;
var lastAssignee;

function displayLoader() {
    $(".loading-indicator-spin").show();
}
function hideLoader() {
    $(".loading-indicator-spin").hide();
}

function initialize(){
    sno = 0;
    lastAssignee = '';
    displayLoader();
    function onSuccess(data){
        closeicon();
        $('.tbody-compliance-approval-list tr').remove();
        sno = 0;
        approvalList = data['approval_list'];
        currentDate = data['current_date'];
        totalRecord = data['total_count'];
        loadComplianceApprovalDetails(approvalList);
        hideLoader();
    }
    function onFailure(error){
        displayMessage(error);
        hideLoader();
    }
    client_mirror.getComplianceApprovalList(sno,
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

$('#pagination').click(function(){
    displayLoader();
    $('.js-filter').val('');
    function onSuccess(data){
        closeicon();
        approvalList = data['approval_list'];
        currentDate = data['current_date'];
        totalRecord = data['total_count'];
        loadComplianceApprovalDetails(approvalList);
        hideLoader();
    }
    function onFailure(error){
        displayMessage(error);
        hideLoader();
    }
    client_mirror.getComplianceApprovalList(sno,
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

function loadComplianceApprovalDetails(data){
    $.each(data, function(key, value) {
        if(lastAssignee != value["assignee_name"]){
            var tableRowHeading = $('#templates .table-compliance-approval-list .headingRow');
            var clone = tableRowHeading.clone();
            $('.heading', clone).html(value["assignee_name"]);
            $('.tbody-compliance-approval-list').append(clone);
            lastAssignee = value["assignee_name"];
        }

        complianceList = value['compliances'];
        //Full Width list append ---------------------------------------------------------------
        $.each(complianceList, function(k, val) {
            var tableRowvalues = $('#templates .table-compliance-approval-list .table-row-list');
            var clonelist = tableRowvalues.clone();
            sno = sno + 1;
            $('.sno-ca', clonelist).html(sno);
            $('.compliance-task span', clonelist).html(val['compliance_name']);
            $('.compliance-task abbr', clonelist).attr("title", val['description']);
            //$('.compliance-task', clonelist).attr("title", val['description']);
            $('.domain', clonelist).html(val['domain_name']);
            $('.startdate', clonelist).html(val['start_date']);
            $('.duedate', clonelist).html(val['due_date']);
            if(val['delayed_by'] == null){
                $('.delayedby', clonelist).html('');
            }
            if(val['delayed_by'] != null){
                $('.delayedby', clonelist).html(val['delayed_by']);
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
        });
    });

    if(totalRecord == 0){
        var norecordtableRow=$('#no-record-templates .table-no-content .table-row-no-content');
        var noclone=norecordtableRow.clone();
        $('.no_records', noclone).text('No Compliance Available');
        $('.tbody-compliance-approval-list').append(noclone);
        $('#pagination').hide();
        $('.compliance_count').text('');
    }else{
        $('.compliance_count').text("Total Compliances : " + totalRecord);
        if(sno >= totalRecord){
          $('#pagination').hide();
        }else{
          $('#pagination').show();
        }
    }
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
                $('.sidebar-uploaded-documents', cloneValSide).append("<span><abbr class='sidebardocview'>"+fileslist[i]+"</abbr><a href='"+documentslist[i]+"' download='"+documentslist[i]+"' class='download-file' ><img src='/images/download.png' style='width:16px;height:16px' title='Download' /></a><a href='"+ documentslist[i] +"' target='_new' class='view-file'> <img src='/images/view.png' style='width:16px;height:16px;' title='View' /></a></span>");
                $(".tr-sidebar-uploaded-date", cloneValSide).show();
            }
        }
    }
    if( fileslist == null){
        $('.sidebar-uploaded-documents', cloneValSide).val("-");
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
    if(complianceFrequency == "On Occurrence"){
        $(".validityAndDueDate", cloneValSide).hide();
    }


    if(data['delayed_by'] != null){
        $(".sidebar-status", cloneValSide).html("Not Complied");
    }
    if(data['delayed_by'] == null){
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
        //console.log(approval_status);

        if(approval_status == ''){
            displayMessage(message.action_required);
            return false;
        }
        else if(approval_status == "Reject Concurrence"){
            remarks = $(".remarks-textarea", cloneValSide).val();
        }
        else if(approval_status == "Reject Approval"){
            remarks = $(".remarks-textarea", cloneValSide).val();
        }
        else {
            remarks = data["remarks"];
        }

        validity_date = $('.validity1-textbox-input', cloneValSide).val();
        if(validity_date == ''){
            validity_date = $('.validitydate1_label', cloneValSide).html();
            if(validity_date == ''){
                validity_date = null;
            }
        }

        next_due_date = $('.duedate1-textbox-input', cloneValSide).val();
        if(next_due_date == ''){
            next_due_date = $('.duedate1_label abbr', cloneValSide).html();
            if(next_due_date == ''){
                next_due_date = null;
            }
        }

        if($(".remarks-textarea", cloneValSide).val().trim().length > 500){
            displayMessage("Remarks" + message.should_not_exceed  + " 500 characters");
            return false;
        }

        if(remarks == ''){
            remarks = null;
        }
        else if(typeof remarks == 'undefined'){
            remarks = null;
        }
        else if(validity_date == ''){
            displayMessage(message.validitydate_required);
            return;
        }
        else if(next_due_date == ''){
            displayMessage(message.nextduedate_required);
            return;
        }
        if(validity_date != null  && next_due_date != null){
            if(parseMyDate(next_due_date) >= parseMyDate(validity_date)){
                displayMessage(message.validitydate_gt_duedate);
                return;
            }
        }

        // if(currentDate != null && validity_date != null){
        //     if(parseMyDate(currentDate) > parseMyDate(next_due_date)){
        //         displayMessage("Validity Date is Greater than Current Date");
        //         return;
        //     }
        // }
        displayLoader();
        function onSuccess(data){
            clearMessage();
            if(approval_status == "Reject Concurrence"){
                displayMessage(message.compliance_concur_reject);
            }
            else if(approval_status == "Reject Approval"){
                displayMessage(message.compliance_app_reject);
            }
            else if(approval_status == "Approve"){
                displayMessage(message.compliance_approval);
            }
            else if(approval_status == "Concur"){
                displayMessage(message.compliance_concurred);
            }
            initialize();
            hideLoader();
        }
        function onFailure(error){
            displayMessage(error);
            hideLoader();
        }

        client_mirror.approveCompliance(compliance_history_id, approval_status,
            remarks, next_due_date, validity_date,
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
    $('.remarks-textarea').on('input', function (e) {
        this.value = isCommon($(this));
    });
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