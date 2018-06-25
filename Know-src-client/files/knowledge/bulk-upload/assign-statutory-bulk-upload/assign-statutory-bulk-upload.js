//button variable declaration
var DOWNLOADFILEBUTTON = $(".btn-download-file");
var UPLOADFILEBUTTON = $(".btn-upload-file");

//autocomplte variable declaration
var GROUPNAME = $('#group_name');
var GROUPID = $("#group_id");
var ACGROUP = $("#ac_group");
var LEGALENTITYNAME = $("#legal_entity_name");
var LEGALENTITYID = $("#legal_entity_id");
var ACLEGALENTITY = $("#ac_entity");
var MULTISELECTDOMAIN = $('#domains');
var MULTISELECTUNIT = $('#units');
var UPLOADFILE = $("#upload_file");

//error description variable declaration
var TOTALRECORD = $('.totalRecords');
var VALIDRECORD = $('.validRecords');
var INVALIDRECORD = $('.invalidRecords');
var MANDATORYERROR = $('.mandatoryErrors');
var DUPLICATEERROR = $('.duplicateErrors');
var STATUSERROR = $('.statusErrors');
var LENGTHERROR = $('.lengthErrors');
var INVALIDERROR = $('.invalidErrors');
var INVALIDFILENAME = null;

//api variable declaration
var GROUPS = null;
var LEGAL_ENTITIES = null;
var UNITS = null;
var DOMAINS = null;
var ASSIGNEDUNITS = null;

//other variable declaration
var UNITNAMES = [];
var UNITIDS = [];
var DOMAINNAMES = [];
var DOMAINIDS = [];
var CSVINFO = null;
var PREVIOUSVAL = [];


//Autocomplete success function
function onAutoCompleteSuccess(valueElement, idElement, val) {
    valueElement.val(val[1]);
    idElement.val(val[0]);
    var currentId = idElement[0].id;
    if (currentId == 'group_id') {
        LEGALENTITYNAME.val('');
        LEGALENTITYID.val('');
        UNITNAMES = [];
        UNITIDS = [];
        DOMAINNAMES = [];
        DOMAINIDS = [];
        fetchDomainMultiselect()
        MULTISELECTDOMAIN.multiselect('rebuild');
        fetchUnitMultiselect()
        // MULTISELECTUNIT.multiselect('rebuild');
    } else if (currentId == 'legal_entity_id') {
        UNITNAMES = [];
        UNITIDS = [];
        DOMAINNAMES = [];
        DOMAINIDS = [];
        fetchDomainMultiselect()
        MULTISELECTDOMAIN.multiselect('rebuild');
        fetchUnitMultiselect()
        // MULTISELECTUNIT.multiselect('rebuild');
    }
}

//load domains into multi select box
function fetchDomainMultiselect() {
    var str = '';
    if (LEGAL_ENTITIES.length > 0) {
        for (var i in LEGAL_ENTITIES) {
            if(LEGAL_ENTITIES[i].le_id == LEGALENTITYID.val()){
                DOMAINS = LEGAL_ENTITIES[i].bu_domains;
                for (var j in DOMAINS) {
                    str += '<option value="'+ DOMAINS[j].d_id +'">'+ 
                    DOMAINS[j].d_name +'</option>';
                }
            }                
        }
        MULTISELECTDOMAIN.html(str).multiselect('rebuild');
    }
}

//load units into multi select box
function fetchUnitMultiselect() {
    var str = '';
    var ISVALID = true;

    if(MULTISELECTDOMAIN.val() != null){
        checkDomain = MULTISELECTDOMAIN.val().map(Number);
        if (UNITS.length > 0 && checkDomain.length > 0) {
            for (var i in UNITS) {
                if(UNITS[i].le_id == LEGALENTITYID.val() &&
                    containsAll(checkDomain, UNITS[i].d_ids)
                    ){
                        ISVALID = true;
                        for(var j in ASSIGNEDUNITS){
                            if(
                                ASSIGNEDUNITS[j].u_id == UNITS[i].u_id &&
                                $.inArray(
                                    ASSIGNEDUNITS[j].d_id, UNITS[i].d_ids
                                ) == 0
                            ){
                                ISVALID = false;
                            }
                        }
                        if(ISVALID){
                            str += '<option value="'+ UNITS[i].u_id +'">'+ 
                            UNITS[i].u_name +'</option>';
                        }   
                }
            }
            MULTISELECTUNIT.html(str).multiselect('rebuild');
        }
    }else{
        MULTISELECTUNIT.html(str).multiselect('rebuild');
    }
    
}

//get information from api for filters 
function fetchData(){
	displayLoader();
	
	bu.getClientInfo(function(error, data) {
        if (error == null) {
            GROUPNAME.focus();
            GROUPS = data.bu_clients;
            LEGAL_ENTITIES = data.bu_legalentites;
            UNITS = data.bu_units;
            ASSIGNEDUNITS = data.bu_assigned_units;
            hideLoader();
        } else {
            displayMessage(error);
            hideLoader();
        }
    });
}

function pageControls() {
    
    //download file button process
    DOWNLOADFILEBUTTON.click(function() {
        var $this = null;
        var ISVALID = true;
        var selText = '';
        var downloadURL = null;

        clientId = GROUPID.val();
        legalentityId = LEGALENTITYID.val();
        clientName = GROUPNAME.val();
        legalentityName = LEGALENTITYNAME.val();
        
        if (clientId.trim().length <= 0) {
            displayMessage(message.client_group_required);
            return false;
        } else if (legalentityId.trim().length <= 0) {
            displayMessage(message.legalentity_required);
            return false;
        } else if (MULTISELECTDOMAIN.val() == null) {
            displayMessage(message.domain_required);
            return false;
        } else if (MULTISELECTUNIT.val() == null) {
            displayMessage(message.unit_required);
            return false;
        } else {
            DOMAINIDS = MULTISELECTDOMAIN.val().map(Number);
            DOMAINNAMES = [];
            $("#domains option:selected").each(function () {
               $this = $(this);
               if ($this.length) {
                DOMAINNAMES.push($this.text());
               }
            });

            UNITNAMES = [];
            UNITIDS = [];
            if(MULTISELECTUNIT.val() == null){
                for (var i in UNITS) {
                    if(UNITS[i].le_id == LEGALENTITYID.val() &&
                        containsAll(DOMAINIDS, UNITS[i].d_ids)){

                        ISVALID = true;
                        for(var j in ASSIGNEDUNITS){
                            if(
                                ASSIGNEDUNITS[j].u_id == UNITS[i].u_id &&
                                $.inArray(
                                    ASSIGNEDUNITS[j].d_id, UNITS[i].d_ids
                                ) == 0
                            ){
                                ISVALID = false;
                            }
                        }
                        if(ISVALID){
                            UNITNAMES.push(
                                UNITS[i].u_name.split('-').pop().trim()
                            );
                            UNITIDS.push(UNITS[i].u_id);
                        }   
                    }
                }
            }else{
                $("#units option:selected").each(function () {
                   $this = $(this);
                   if ($this.length) {
                    selText = $this.text().split('-').pop();
                    UNITNAMES.push(selText.trim());
                   }
                });
                UNITIDS = MULTISELECTUNIT.val().map(Number);
            }

            displayLoader();

            var csv_name = null;
            //var count = 0;
            function apiCallDownload(csv_name, callback){
                bu.getAssignStatutoryDownloadStatus(csv_name, callback);
            }
            function call_bck_fn(error, data){
                console.log("get status data: error"+ error + ", data:"+data)
                if (error == null) {
                    downloadURL = data.link;
                    if (downloadURL != null){
                        window.open(downloadURL, '_blank');
                        hideLoader();
                    }
                    else{
                        displayMessage(message.no_compliance_assign_statutory);
                        hideLoader();
                    }
                }
                else{
                    if (error == "Alive"){
                        console.log("inside if=====> going to get status again")
                        // count = count+1;
                        sleep(180000);
                        // apiCallDownload(csv_name, call_bck_fn);
                        //if(count <3){
                        apiCallDownload(csv_name, call_bck_fn);
                        //     count++;
                        // }
                        
                    }
                    hideLoader();
                    
                }
            }
            bu.getDownloadAssignStatutory(
                parseInt(clientId), parseInt(legalentityId), 
                DOMAINIDS, UNITIDS, clientName, 
                legalentityName, DOMAINNAMES, UNITNAMES, 
                function(error, response){
                if(error == "Done" || response == "Done"){
                    csv_name = response.csv_name;
                    apiCallDownload(csv_name, call_bck_fn);
                }else{
                    displayMessage(error);
                    hideLoader();
                }
            });

            // bu.getDownloadAssignStatutory(parseInt(clientId), 
            //     parseInt(legalentityId), 
            //     DOMAINIDS, UNITIDS, clientName, 
            //     legalentityName, DOMAINNAMES, UNITNAMES, 
            //     function(error, data) {
            //     if (error == null) {
            //         downloadURL = data.link;
            //         if (downloadURL != null){
            //             window.open(downloadURL, '_blank');
            //             hideLoader();
            //         }
            //         else{
            //             displayMessage(message.no_compliance_assign_statutory);
            //             hideLoader();
            //         }
            //     } else {
            //         displayMessage(error);
            //         hideLoader();
            //     }
            // });
        }
    });

    //domain multiselect box change process
    MULTISELECTDOMAIN.change(function(e) {
        displayLoader();
        setTimeout(function() {
            UNITNAMES = [];
            UNITIDS = [];
            fetchUnitMultiselect();
            hideLoader();
        }, 500);
        // MULTISELECTUNIT.multiselect('rebuild');
    });

    //unit multiselect box change process
    MULTISELECTUNIT.change(function(e) {
        if(
            MULTISELECTUNIT.val() != null && 
            MULTISELECTUNIT.val().length > maxUnitSelection
        ){
            PREVIOUSVAL = $(this).val().slice(0, maxUnitSelection)
            $(this).val(PREVIOUSVAL);
            $("#units").multiselect('rebuild');
            displayMessage(message.maximum_units);
        } else {
            PREVIOUSVAL = $(this).val();
            // $("#units").multiselect('rebuild');
        }
    });

    //group autocomplte textbox process
    GROUPNAME.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACGROUP, GROUPID, text_val,
            GROUPS, "cl_name", "cl_id",
            function(val) {
                onAutoCompleteSuccess(GROUPNAME, GROUPID, val);
            });
    });

    //legal entity autocomplte textbox process
    LEGALENTITYNAME.keyup(function(e) {
        var condetionFields = null;
        var condetionValues = null;
        var text_val = null;
        if (GROUPID.val() != '') {
            condetionFields = ["cl_id"];
            condetionValues = [GROUPID.val()];
            text_val = $(this).val();
            commonAutoComplete(
                e, ACLEGALENTITY, LEGALENTITYID, text_val,
                LEGAL_ENTITIES, "le_name", "le_id",
                function(val) {
                    onAutoCompleteSuccess(LEGALENTITYNAME, LEGALENTITYID, val);
                }, condetionFields, condetionValues);
        }
    });

    //upload file change event
    UPLOADFILE.change(function(e) {
        if ($(this).val() != '') {
            bu.uploadCSVFile(e, function(status, response) {
                if (status == false) {
                    displayMessage(response);
                }
                else {
                    CSVINFO = response
                }

            })
        }
    });

    function sleep(milliseconds) {
      var start = new Date().getTime();
      for (var i = 0; i < 1e7; i++) {
        if ((new Date().getTime() - start) > milliseconds){
          break;
        }
      }
    }

    //upload file button process
    UPLOADFILEBUTTON.click(function() {
        var args = {};
        var getValidCount = 0;
        clientId = GROUPID.val();
        legalentityId = LEGALENTITYID.val();
        legalentityName = LEGALENTITYNAME.val();

        if (UPLOADFILE.val() == '') {
            displayMessage(message.upload_csv);
            return false;
        } else if (CSVINFO == null) {
            displayMessage(message.invalid_file_format);
            return false;
        } else {
            args = {
                "csv_name": CSVINFO["file_name"],
                "csv_data": CSVINFO["file_content"],
                "csv_size": CSVINFO["file_size"]
            };
            $('#myModal').modal('show');

            var csv_name = null;
            // var count = 0;
            function apiCall(csv_name, callback){
                bu.getAssignStatutoryStatus(csv_name, callback);
            }
            function call_bck_fn(error, data){
                console.log("get status data: error"+ error + ", data:"+data)
                if (error == null) {
                    TOTALRECORD.text(data.total);
                    VALIDRECORD.text( parseInt(data.valid) - 
                        parseInt(data.invalid) );
                    INVALIDRECORD.text(data.invalid);
                    INVALIDFILENAME = null;
                    MANDATORYERROR.text("0");
                    DUPLICATEERROR.text("0");
                    STATUSERROR.text("0");
                    LENGTHERROR.text("0");
                    INVALIDERROR.text("0");
                    $('.view-summary').hide();
                    $('.download-options').hide();
                    displaySuccessMessage(message.upload_success);
                    hideLoader();
                    GROUPID.val('');
                    GROUPNAME.val('');
                    LEGALENTITYNAME.val('');
                    LEGALENTITYID.val('');
                    UNITNAMES = [];
                    UNITIDS = [];
                    DOMAINNAMES = [];
                    DOMAINIDS = [];
                    fetchDomainMultiselect()
                    MULTISELECTDOMAIN.multiselect('rebuild');
                    fetchUnitMultiselect()
                    // MULTISELECTUNIT.multiselect('rebuild');
                    UPLOADFILE.val('');
                    $('#myModal').modal('hide');
                }
                else{
                    if(error == 'UploadAssignStatutoryCSVFailed'){
                        displayMessage(message.upload_failed);
                        INVALIDFILENAME = data.invalid_file.split('.');;
                        TOTALRECORD.text(data.total);
                        getValidCount = (parseInt(data.total) - 
                            parseInt(data.invalid));
                        VALIDRECORD.text(getValidCount);
                        INVALIDRECORD.text(data.invalid);
                        MANDATORYERROR.text(data.mandatory_error);
                        DUPLICATEERROR.text(data.duplicate_error);
                        STATUSERROR.text(data.inactive_error);
                        LENGTHERROR.text(data.max_length_error);
                        getInvaliddataCount = parseInt(data.invalid_char_error) 
                            + parseInt(data.invalid_data_error);
                        INVALIDERROR.text(getInvaliddataCount);
                        $('.download-options').show();
                        $('.view-summary').show();
                        
                        csv_path = "/invalid_file/csv/" + INVALIDFILENAME[0] + 
                        '.csv';
                        xls_path = "/invalid_file/xlsx/" + INVALIDFILENAME[0] + 
                        '.xlsx';
                        ods_path = "/invalid_file/ods/" + INVALIDFILENAME[0] + 
                        '.ods';
                        txt_path = "/invalid_file/txt/" + INVALIDFILENAME[0] + 
                        '.txt';
                        $('#csv_type').attr("href", csv_path);
                        $('#xls_type').attr("href", xls_path);
                        $('#ods_type').attr("href", ods_path);
                    }else{
                        if (error == "Alive"){
                            console.log("inside if=====> going to get status again")
                            // count = count+1;
                            sleep(180000);
                            apiCall(csv_name, call_bck_fn);
                            // if(count <3){
                            //     apiCall(csv_name, call_bck_fn);
                            //     count++;
                            // }
                            
                        }else if(error == "InvalidCsvFile"){
                            displayMessage(message.invalid_csv_file);
                        }else if(error == "CsvFileBlank"){
                            displayMessage(message.csv_file_blank);
                        }else if(error == "UnitsNotAssignedToUser"){
                            displayMessage(message.units_not_assigned_to_user);
                        }else if(error == "UploadedRecordsCountNotMatch"){
                            displayMessage(
                                message.uploaded_record_count_invalid.replace(
                                'UNITS', data.u_names.toString()
                                )
                            );
                        }else{
                            displayMessage(error);
                        }
                        $('.view-summary').hide();
                        $('.download-options').hide();
                    }
                    $('#myModal').modal('hide');
                    UPLOADFILE.val('');
                }
            }

            bu.getUploadAssignStatutoryCSV(
            args, function(error, response){
                if(error == "Done" || response == "Done"){
                    csv_name = response.csv_name;
                    console.log("got csv name: "+ csv_name);
                    apiCall(csv_name, call_bck_fn);
                }else if(error == "RejectionMaxCountReached"){
                    $('#myModal').modal('hide');
                    UPLOADFILE.val('');
                    displayMessage(message.rejection_max_count_reached);
                }
                else if (error == "CsvFileExeededMaxLines") {
                    $('#myModal').modal('hide');
                    UPLOADFILE.val('');
                    displayMessage(message.csv_max_lines_exceeded.replace(
                        'MAX_LINES', response.csv_max_lines));
                }else if(error == "CsvFileBlank") {
                    $('#myModal').modal('hide');
                    UPLOADFILE.val('');
                    displayMessage(message.csv_file_blank);
                }else if(error == "InvalidCsvFile"){
                    $('#myModal').modal('hide');
                    UPLOADFILE.val('');
                    displayMessage(message.invalid_csv_file);
                }else if(error == "UnitsNotAssignedToUser"){
                    $('#myModal').modal('hide');
                    UPLOADFILE.val('');
                    displayMessage(message.units_not_assigned_to_user);
                }else if(error == "UploadedRecordsCountNotMatch"){
                    $('#myModal').modal('hide');
                    UPLOADFILE.val('');
                    displayMessage(
                        message.uploaded_record_count_invalid.replace(
                        'UNITS', data.u_names.toString()
                        )
                    );
                }else{
                    displayMessage(error);
                }
            });
        }

    });
}

document.getElementById("txt_type").addEventListener("click", function(){
    if(INVALIDFILENAME != null) {
        $.get(
            "/invalid_file/txt/" + INVALIDFILENAME[0] + ".txt", function(data)
            {
               download(INVALIDFILENAME[0]+".txt", "text/plain", data);
            },
        'text');
    }
});

function download(filename, mime_type, text) {
    var element = document.createElement('a');
    var href = 'data:' + mime_type + ';charset=utf-8,' + 
        encodeURIComponent(text);
    element.setAttribute('href', href);
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

//initialize function
function initialize() {
	fetchData();
    pageControls();
    
}

$(function() {
    $('.download-options').hide();
    MULTISELECTUNIT.multiselect({
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true,
        includeSelectAllOption: true
    });
    MULTISELECTDOMAIN.multiselect({
        includeSelectAllOption: true
    });
    MULTISELECTDOMAIN.multiselect({
        buttonWidth: '100%'
    });
    MULTISELECTUNIT.multiselect({
        buttonWidth: '100%'
    });
    initialize();
});