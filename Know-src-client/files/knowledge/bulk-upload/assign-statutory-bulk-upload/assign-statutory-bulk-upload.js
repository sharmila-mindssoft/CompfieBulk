//button variable declaration
var DOWNLOADFILEBUTTON = $(".btn-download-file");
var UPLOADFILEBUTTON = $(".btn-upload-file");

//autocomplte variable declaration
var GROUPNAME = $('#group_name');
var GROUPID = $("#group_id");
var ACGROUP = $("#ac-group");
var LEGALENTITYNAME = $("#legal_entity_name");
var LEGALENTITYID = $("#legal_entity_id");
var ACLEGALENTITY = $("#ac-entity");
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
        MULTISELECTUNIT.multiselect('rebuild');
    } else if (currentId == 'legal_entity_id') {
        UNITNAMES = [];
        UNITIDS = [];
        DOMAINNAMES = [];
        DOMAINIDS = [];
        fetchDomainMultiselect()
        MULTISELECTDOMAIN.multiselect('rebuild');
        fetchUnitMultiselect()
        MULTISELECTUNIT.multiselect('rebuild');
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
    if(MULTISELECTDOMAIN.val() != null){
        checkDomain = MULTISELECTDOMAIN.val().map(Number);
        if (UNITS.length > 0 && checkDomain.length > 0) {
            for (var i in UNITS) {
                if(UNITS[i].le_id == LEGALENTITYID.val() &&
                    containsAll(checkDomain, UNITS[i].d_ids)
                    ){
                        var ISVALID = true;
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
        clientId = GROUPID.val();
        legalentityId = LEGALENTITYID.val();
        clientName = GROUPNAME.val();
        legalentityName = LEGALENTITYNAME.val();
        
        if (clientId.trim().length <= 0) {
            displayMessage('Client Group Required');
            return false;
        } else if (legalentityId.trim().length <= 0) {
            displayMessage(message.legalentity_required);
            return false;
        } else if (MULTISELECTDOMAIN.val() == null) {
            displayMessage(message.domain_required);
            return false;
        } else {
            DOMAINIDS = MULTISELECTDOMAIN.val().map(Number);
            DOMAINNAMES = [];
            $("#domains option:selected").each(function () {
               var $this = $(this);
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

                        var ISVALID = true;
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
                   var $this = $(this);
                   if ($this.length) {
                    var selText = $this.text().split('-').pop();
                    UNITNAMES.push(selText.trim());
                   }
                });
                UNITIDS = MULTISELECTUNIT.val().map(Number);
            }

            displayLoader();
            bu.getDownloadAssignStatutory(parseInt(clientId), 
                parseInt(legalentityId), 
                DOMAINIDS, UNITIDS, clientName, 
                legalentityName, DOMAINNAMES, UNITNAMES, 
                function(error, data) {
                if (error == null) {
                    var downloadURL = data.link;
                    if (downloadURL != null){
                        window.open(downloadURL, '_blank');
                        hideLoader();
                    }
                    else{
                        displayMessage(message.no_compliance_assign_statutory);
                        hideLoader();
                    }
                } else {
                    displayMessage(error);
                    hideLoader();
                }
            });
        }
    });

    //domain multiselect box change process
    MULTISELECTDOMAIN.change(function(e) {
        UNITNAMES = [];
        UNITIDS = [];
        fetchUnitMultiselect()
        MULTISELECTUNIT.multiselect('rebuild');
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
        if (GROUPID.val() != '') {
            var condetionFields = ["cl_id"];
            var condetionValues = [GROUPID.val()];
            
            var text_val = $(this).val();
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

    //upload file button process
    UPLOADFILEBUTTON.click(function() {
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
            var args = {
                "csv_name": CSVINFO["file_name"],
                "csv_data": CSVINFO["file_content"],
                "csv_size": CSVINFO["file_size"]
            };
            displayLoader();
            bu.getUploadAssignStatutoryCSV(args, function(error, data) {
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
                    MULTISELECTUNIT.multiselect('rebuild');
                    UPLOADFILE.val('');
                    
                } else {
                   if(error == 'UploadAssignStatutoryCSVFailed'){
                        displayMessage(message.upload_failed);
                        INVALIDFILENAME = data.invalid_file.split('.');;
                        TOTALRECORD.text(data.total);
                        var getValidCount = (parseInt(data.total) - 
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
                        $('#csv').attr("href", csv_path);
                        $('#excel').attr("href", xls_path);
                        $('#ods').attr("href", ods_path);
                        $('#txt').attr("href", txt_path);
                    }else{
                        if(error == "InvalidCsvFile"){
                            displayMessage(message.invalid_csv_file);
                        }else if(error == "CsvFileBlank"){
                            displayMessage(message.csv_file_blank);
                        }else if(error == "RejectionMaxCountReached"){
                            displayMessage(message.rejection_max_count_reached);
                        }else if(error == "UnitsNotAssignedToUser"){
                            displayMessage(message.units_not_assigned_to_user);
                        }else{
                            displayMessage(error);
                        }
                        $('.view-summary').hide();
                        $('.download-options').hide();
                    }
                    hideLoader();
                }
            });
            


            
        }

    });
}

//initialize function
function initialize() {
	fetchData();
    pageControls();
    
}

$(function() {
    $('.download-options').hide();
    $('#units').multiselect({
        includeSelectAllOption: true
    });
    $('#domains').multiselect({
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