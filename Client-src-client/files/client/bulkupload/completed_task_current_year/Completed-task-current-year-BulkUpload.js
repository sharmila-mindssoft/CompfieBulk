var LEGAL_ENTITIES = client_mirror.getSelectedLegalEntity();

var CANCELBUTTON = $("#cancelButton");
var ADDSCREEN = $("#add-screen");
var VIEWSCREEN = $("#list-screen");
var ADDBUTTON = $("#btn-add");
var DOWNLOADBUTTON = $("#btnDownloadFile");
var SUBMITBUTTON = $(".btn_submit");

var DIVUPLOAD = $('#divUploadFile');
var UploadFile = $("#fileInput");

var LegalEntityName = $("#txt_legal_entity_name");
var LegalEntityId = $("#hdn_legal_entity_id");
var LegalEntityNameLabel = $(".legal-entity-name");
var ACLegalEntity = $("#ac-entity");
var LegalEntityNameAC = $(".legal-entity-name-ac");

var LEGALENTITYNAMEUPLOAD = $("#txt_legal_entity_name_upload");
var LEGALENTITYIDUPLOAD = $("#hdn_legal_entity_id_upload");
var LEGALENTITYNAMELABELUPLOAD = $(".legal-entity-name-upload");
var ACLEGALENTITYUPLOAD = $("#ac-entity-upload");
var LEGALENTITYNAMEACUPLOAD = $(".legal-entity-name-ac-upload");

var ListContainer = $('.tbody-ct-csv-list');
var ListRowTemplate = $('#templates .table-ct-csv-info .table-row');

var txtdomain = $("#txtdomain");
var hdnDomain = $("#hdnDomain");
var divDomain = $("#divDomain");

var txtUnit = $('#txtUnit');
var hdnUnit = $('#hdnUnit');
var divUnit = $('#divUnit');

var BTNUPLOAD = $('#btnUpload');
var INVALIDFILENAME = null;

var unitList = [];
var domainList = [];
var docNames = [];
var csvInfo = null;
var csvId = null;
var buCtPage = null;

//error description variable declaration
var TOTALRECORD = $('.totalRecords');
var VALIDRECORD = $('.validRecords');
var INVALIDRECORD = $('.invalidRecords');
var MANDATORYERROR = $('.mandatoryErrors');
var DUPLICATEERROR = $('.duplicateErrors');
var STATUSERROR = $('.statusErrors');
var LENGTHERROR = $('.lengthErrors');
var INVALIDERROR = $('.invalidErrors');
var INVALIDFILEFORMATERROR = $('.invalidFileFormat');
var INVALIDFILENAME = null;

var unit_list_map = {};
var LEGAL_ENTITY_USR = [];


txtdomain.keyup(function(e) {
    var condition_fields = [];
    var condition_values = [];
    var text_val = $(this).val();
    commonAutoComplete(e, divDomain, hdnDomain, text_val, domainList,
        "d_name", "d_id",
        function(val) {
            onAutoCompleteSuccess(txtdomain, hdnDomain, val);
        }, condition_fields, condition_values);
});

//Unit Auto Complete
txtUnit.keyup(function(e) {
    var condition_fields = [];
    var condition_values = [];
    var text_val = $(this).val();
    commonAutoComplete(
        e, divUnit, hdnUnit, text_val,
        unitList, "unit_name", "unit_id",
        function(val) {
            onAutoCompleteSuccess(txtUnit, hdnUnit, val);
        }, condition_fields, condition_values);
});

function loadUnits(le_id, unit_id) {
    client_mirror.complianceFilters(le_id, function(error, response) {
        if (error == null) {
            unitList = response.user_units;
            $.each(unitList, function(key, u) {
                unit_list_map[parseInt(u["unit_id"])] = u["unit_code"];
            });
        }
    });
}
LegalEntityName.keyup(function(e) {
    var text_val = $(this).val();
    commonAutoComplete(
        e, ACLegalEntity, LegalEntityId, text_val,
        LEGAL_ENTITIES, "le_name", "le_id",
        function(val) {
            onAutoCompleteSuccess(LegalEntityName, LegalEntityId, val);
        });
});
LEGALENTITYNAMEUPLOAD.keyup(function(e) {
    var text_val = $(this).val();
    commonAutoComplete(
        e, ACLEGALENTITYUPLOAD, LEGALENTITYIDUPLOAD, text_val,
        LEGAL_ENTITIES, "le_name", "le_id",
        function(val) {
            onAutoCompleteSuccess(LEGALENTITYNAMEUPLOAD, LEGALENTITYIDUPLOAD, val);
        });
});

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    // alert(id_element[0].id);
    // hdn_legal_entity_id_upload
    if (id_element[0].id == 'hdn_legal_entity_id') {
        getPastRecords(parseInt(LegalEntityId.val()));
        loadUnits(parseInt(LegalEntityId.val()));
    }
}

function loadEntityDetails() {
    LEGAL_ENTITY_USR = [];
    if (LEGAL_ENTITIES.length > 1) {
        LegalEntityNameLabel.hide();
        LEGALENTITYNAMELABELUPLOAD.hide();
        LegalEntityNameAC.show();
        LEGALENTITYNAMEACUPLOAD.show();

        for (var i = 0; i < LEGAL_ENTITIES.length; i++) {
            console.log(LEGAL_ENTITIES[i]["le_id"]);
            LEGAL_ENTITY_USR.push(LEGAL_ENTITIES[i]["le_id"]);
        }
        console.log("loadEntityDetails>1>>" + LEGAL_ENTITY_USR);

    } else {
        var LE_NAME = LEGAL_ENTITIES[0]["le_name"];
        var LE_ID = LEGAL_ENTITIES[0]["le_id"];
        LEGAL_ENTITY_USR.push(LE_ID);
        console.log("loadEntityDetails=1>" + LEGAL_ENTITY_USR);

        LegalEntityNameLabel.show();
        LEGALENTITYNAMELABELUPLOAD.show();
        LegalEntityNameAC.hide();
        LEGALENTITYNAMEACUPLOAD.hide();

        LegalEntityNameLabel.text(LE_NAME);
        LEGALENTITYNAMELABELUPLOAD.text(LE_NAME);
        LegalEntityId.val(LE_ID);
        LEGALENTITYIDUPLOAD.val(LE_ID);

        loadUnits(parseInt(LegalEntityId.val()));
        getPastRecords(parseInt(LegalEntityId.val()));
    }
}

function getPastRecords(legalEntity) {
    displayLoader();

    function onSuccess(data) {
        // unitsList = data["in_units"];
        domainList = data.domains;
        // loadUnit();
        hideLoader();
    }

    function onFailure(error) {
        hideLoader();
    }
    client_mirror.getPastRecordsFormData(parseInt(legalEntity),
        function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        }
    );
}

function validateUpload() {
    if ($('#fileInput').val() == "" && buCtPage._ActionMode != 'upload') {
        displayMessage("Select file to upload");
        $('#myModal').modal('hide');
        return false;
    } else {

        $('#myModal').modal('show');
        console.log("_ActionMode>>", buCtPage._ActionMode);
        if (buCtPage._ActionMode == "add") {
            // alert(LEGALENTITYIDUPLOAD.val());

            var args = {
                "csv_name": csvInfo["file_name"],
                "csv_data": csvInfo["file_content"],
                "csv_size": csvInfo["file_size"],
                "legal_entity_id": parseInt(LEGALENTITYIDUPLOAD.val())
            };

            buClient.UploadCompletedTaskCurrentYearCSV(args, function(error, data) {
                if (error == null) {
                    // console.log("data>>" + JSON.stringify(data));
                    var csv_split_name = data.csv_name.substring(0, data.csv_name.lastIndexOf("_"));
                    $('#myModal').modal('hide');
                    TOTALRECORD.text(data.total);
                    VALIDRECORD.text(parseInt(data.valid) - parseInt(data.invalid));
                    INVALIDRECORD.text(data.invalid);
                    INVALIDFILENAME = null;
                    MANDATORYERROR.text("0");
                    DUPLICATEERROR.text("0");
                    STATUSERROR.text("0");
                    LENGTHERROR.text("0");
                    INVALIDERROR.text("0");
                    INVALIDFILEFORMATERROR.text(0);
                    $('.view-summary').hide();
                    $('.dropbtn').hide();
                    $('#hdnCsvId').val(data.new_csv_id);
                    csvId = data.new_csv_id;
                    $('.successFileName').text(csv_split_name);
                    csv_path = "../../../../../uploaded_file/csv/" + csv_split_name + '.csv';
                    $('.uploaded_data').attr("href", csv_path);
                    $('.uploaded_data').attr("download", csv_path);

                    if (data.doc_count > 0) {
                        $('.divSuccessDocument').show();
                        $('#divSuccessbutton').hide();
                        buCtPage._ActionMode = "upload";
                        BTNUPLOAD.show();
                        docNames = data.doc_names;
                    } else {
                        $('.divSuccessDocument').hide();
                        $('#divSuccessbutton').show();
                        // buCtPage._ActionMode = "upload";
                        BTNUPLOAD.hide();
                    }

                    $('.invaliddata').hide();
                    $('.view-summary').hide();
                    $('#divFileUpload').hide();
                    $('#divSuccessFile').show();

                    displaySuccessMessage("Records uploaded successfully");
                    hideLoader();
                } else {
                    console.log(JSON.stringify(data));
                    $('#myModal').modal('hide');
                    displayMessage(message.upload_failed);
                    INVALIDFILENAME = data.invalid_file.split('.');
                    TOTALRECORD.text(data.total);
                    var getValidCount = (parseInt(data.total) - parseInt(data.invalid));
                    VALIDRECORD.text(getValidCount);
                    INVALIDRECORD.text(data.invalid);
                    MANDATORYERROR.text(data.mandatory_error);
                    DUPLICATEERROR.text(data.duplicate_error);
                    STATUSERROR.text(data.inactive_error);
                    LENGTHERROR.text(data.max_length_error);
                    getInvaliddataCount = parseInt(data.invalid_char_error) +
                        parseInt(data.invalid_data_error);
                    INVALIDERROR.text(getInvaliddataCount);
                    INVALIDFILEFORMATERROR.text(data.invalid_file_format);
                    $('.dropbtn').show();
                    $('.view-summary').show();

                    $('.invaliddata').show();
                    $('.view-summary').show();
                    $('#divFileUpload').show();
                    $('#divSuccessFile').hide();
                    $('.divSuccessDocument').hide();
                    $('#divSuccessbutton').hide();

                    csv_path = "/invalid_file/csv/" + INVALIDFILENAME[0] +
                        '.csv';
                    xls_path = "/invalid_file/xlsx/" + INVALIDFILENAME[0] +
                        '.xlsx';
                    ods_path = "/invalid_file/ods/" + INVALIDFILENAME[0] +
                        '.ods';
                    $('#csv').attr("href", csv_path);
                    $('#excel').attr("href", xls_path);
                    $('#ods').attr("href", ods_path);

                    hideLoader();
                }
            });
        } else {
            $('#myModal').modal('hide');
            displayLoader();
            myDropzone.processQueue();
            hideLoader();
        }
    }
}

document.getElementById("txt").addEventListener("click", function() {
    if (INVALIDFILENAME != null) {
        $.get(
            "/invalid_file/txt/" + INVALIDFILENAME[0] + ".txt",
            function(data) {
                download(INVALIDFILENAME[0] + ".txt", "text/plain", data);
            },
            'text');
    }
});

function download(filename, mime_type, text) {
    var element = document.createElement('a');
    var href = 'data:' + mime_type + ';charset=utf-8,' + encodeURIComponent(text);
    element.setAttribute('href', href);
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

UploadFile.change(function(e) {
    if ($(this).val() != '') {
        buClient.uploadCSVFile(e, function(status, response) {
            if (status == false) {
                UploadFile.val("");
                displayMessage(response);
            } else {
                csvInfo = response;
            }
        });
    }
});

$(function() {
    loadEntityDetails();

});

function pageControls() {
    // Cancel Button Click Event
    CANCELBUTTON.click(function() {
        VIEWSCREEN.show();
        ADDSCREEN.hide();

        buCtPage.showList();
    });

    //Add Button Click Event
    ADDBUTTON.click(function() {
        VIEWSCREEN.hide();
        ADDSCREEN.show();
        buCtPage._ActionMode = "add";
        resetAdd();
    });

    //Add Button Click Event
    DOWNLOADBUTTON.click(function() {
        downloadData();
    });

    //Upload Button Click Event
    BTNUPLOAD.click(function() {
        validateUpload();
    });

    SUBMITBUTTON.click(function() {
        submitUpload();
    });
}

BulkCompletedTaskCurrentYear.prototype.showList = function() {
    var t_this = this;
    var args = {
        "legal_entity_id": parseInt(LegalEntityId.val()),
        "legal_entity_list": LEGAL_ENTITY_USR
    };

    displayLoader();
    buClient.GetCompletedTaskCsvUploadedList(args,
        function(error, data) {
            if (error == null) {
                // alert(data);
                t_this._ListDataForView = data.csv_list;
                t_this.renderList(t_this._ListDataForView);
                hideLoader();
            } else {
                hideLoader();
            }
        }
    );
};

BulkCompletedTaskCurrentYear.prototype.renderList = function(list_data) {
    // console.log("LEGAL_ENTITIES> " + LEGAL_ENTITIES);
    var t_this = this;
    var j = 1;
    ListContainer.find('tr').remove();
    if (list_data.length == 0) {
        ListContainer.empty();
        var tableRow4 = $(
            '#no-record-templates .table-no-content .table-row-no-content'
        );
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        ListContainer.append(clone4);
    } else {
        $.each(list_data, function(idx, data) {
            var balance = data.no_of_documents - data.uploaded_documents;
            var cloneRow = ListRowTemplate.clone();
            var cname_split = data.csv_name.split("_");
            cname_split.pop();
            var cname = cname_split.join("_");
            $('.sno', cloneRow).text(j);
            $('.legal-entity', cloneRow).text(data.legal_entity_name);
            $('.csv-name', cloneRow).text(cname);
            $('.uploaded-on', cloneRow).text(data.uploaded_on);
            $('.tot-records', cloneRow).text(data.total_records);
            $('.req-docs', cloneRow).text(data.total_documents);
            $('.uploaded-docs', cloneRow).text(data.uploaded_documents);
            $('.remaining-docs', cloneRow).text(data.remaining_documents);
            csvId = data.csv_id;
            docNames = data.doc_names;
            $('.upload i', cloneRow).on('click', function() {
                t_this.showEdit(data);
                console.log("upload fired");
            });
            ListContainer.append(cloneRow);
            j += 1;
        });
    }
    $('[data-toggle="tooltip"]').tooltip();
};

BulkCompletedTaskCurrentYear.prototype.showEdit = function(data) {
    // this.showAddScreen();
    resetEdit();
    // data
    console.log("data>>" + JSON.stringify(data));
    var uploadedCsvName = data.csv_name;

    $('#hdnCsvId').val(data.csv_past_id);
    csvId = data.csv_past_id;

    var csv_split_name = uploadedCsvName.substring(0, uploadedCsvName.lastIndexOf("_"));
    $('.successFileName').text(csv_split_name);
    csv_path = "../../../../../uploaded_file/csv/" + csv_split_name + '.csv';
    $('.uploaded_data').attr("href", csv_path);
    $('.uploaded_data').attr("download", csv_path);

    $('#bu-doc-total').text(data.total_documents);
    $('#bu-upload-total').text(data.uploaded_documents);
    $('#bu-remain-total').text(data.remaining_documents);

};


BulkCompletedTaskCurrentYear.prototype.possibleFailures = function(error) {
    displayMessage(error);
};

function downloadData() {
    var legalEntityName;

    if (LegalEntityId.val().trim() == "") {
        displayMessage(message.legalentity_required);
        LegalEntityName.focus();
        return false;
    }
    if (txtdomain.val().trim() == "") {
        displayMessage(message.domain_required);
        txtdomain.focus();
        return false;
    }
    if (txtUnit.val().trim() == "") {
        displayMessage(message.unit_required);
        txtUnit.focus();
        return false;
    }
    if (LegalEntityNameLabel.text() == "") {
        legalEntityName = LegalEntityName.val().trim();
    } else {
        legalEntityName = LegalEntityNameLabel.text();
    }

    var domainName = txtdomain.val();
    var unitName = txtUnit.val();
    var leId = LegalEntityId.val();
    var domainId = hdnDomain.val();
    var unitId = hdnUnit.val();
    var unitCode = unit_list_map[unitId];
    var frequency = "Periodical";
    var startCount = 0;

    console.log("leId->>>>>>> " + leId);
    buClient.getDownloadData(
        parseInt(leId), parseInt(domainId), parseInt(unitId), frequency, startCount,
        legalEntityName, domainName, unitName, unitCode,
        function(error, data) {
            if (error == null) {
                var download_url = data.link;
                console.log("download_url>>>>> " + download_url);
                if (download_url != null) {
                    window.open(download_url, '_blank');
                    hideLoader();
                } else {
                    displayMessage("message.empty_export");
                    hideLoader();
                }
            } else {
                displayMessage(error);
                hideLoader();
            }
        }
    );
}

function submitUpload() {

    var args = {
        "new_csv_id": parseInt($('#hdnCsvId').val()),
        "legal_entity_id": parseInt(LEGALENTITYIDUPLOAD.val())
    };
    $('#myModal').modal('show');
    buClient.saveBulkRecords(args, function(error, data) {
        if (error == null) {
            VIEWSCREEN.show();
            ADDSCREEN.hide();
            displaySuccessMessage("Record Submitted successfully");
            $('#myModal').modal('hide');
        } else {
            $('#myModal').modal('hide');
        }
    });
}



// $(function() {
//     loadEntityDetails();

// });

BulkCompletedTaskCurrentYear.prototype.possibleFailures = function(error) {
    displayMessage(error);
};

function file_upload_rul() {
    var session_id = client_mirror.getSessionToken();

    var file_base_url = "/client/temp/upload?session_id=" +
        session_id + "&csvid=" + csvId;
    console.log(file_base_url);
    return file_base_url;
}

function resetAdd() {
    $('#divDownloadSection').show();
    $('#divUploadSection').show();

    $('.divSuccessDocument').hide();
    $('#divSuccessbutton').hide();
    $('.invaliddata').hide();
    $('.view-summary').hide();
    $('#divFileUpload').show();
    $('#divSuccessFile').hide();
    $('.bu-doc-summary').hide();

    buCtPage._ActionMode = "add";
    UploadFile.val("");
}

function resetEdit() {
    VIEWSCREEN.hide();
    ADDSCREEN.show();

    $('#divDownloadSection').hide();
    $('#divUploadSection').show();

    $('.divSuccessDocument').show();
    $('.bu-doc-summary').show();
    // $('.successFileName').show();
    $('#divSuccessFile').show();

    $('.view-summary').hide();
    $('#divSuccessbutton').hide();
    $('.invaliddata').hide();
    $('#divFileUpload').hide();


    // $('#hdnCsvId').val(data.new_csv_id);
    // csvId = data.new_csv_id;
    // $('.successFileName').text(csv_split_name);
    // csv_path = "../../../../../uploaded_file/csv/" + csv_split_name + '.csv';
    // $('.uploaded_data').attr("href", csv_path);
    // $('.uploaded_data').attr("download", csv_path);

    buCtPage._ActionMode = "upload";
    UploadFile.val("");
}

Dropzone.autoDiscover = false;
Dropzone.autoProcessQueue = false;
var addedfiles = [];
var totalfileUploadSuccess = 0;
var perQueueUploadSuccess = 0;
var queueCount = 0;
var maxParallelCount = 2;
var myDropzone = new Dropzone("div#myDrop", {
    addRemoveLinks: true,
    autoProcessQueue: false,
    parallelUploads: maxParallelCount,
    url: "#",
    transformFile: function transformFile(file, done) {
        var zip = new JSZip();
        zip.file(file.name, file);
        zip.generateAsync({
            type: "blob",
            compression: "DEFLATE"
        }).then(function(content) {
            done(content);
        });
    },
    init: function() {
        this.on("addedfile", function(file) {
            if (jQuery.inArray(file.name, addedfiles) > -1) {
                console.log("addedfiles part");
                myDropzone.removeFile(file);
            }
            if (jQuery.inArray(file.name, docNames) == -1) {
                myDropzone.removeFile(file);
            } else {
                addedfiles.push(file.name);
                queueCount += 1;
            }
        });
        this.on("removedfile", function(file) {
            if (jQuery.inArray(file.name, addedfiles) > -1) {
                addedfiles.pop(file.name);
                queueCount -= 1;
            }
        });

        this.on("processing", function(file) {
            this.options.url = file_upload_rul();
        });

        this.on("success", function(file, response) {
            addedfiles.pop(file.name);
            if (totalfileUploadSuccess < queueCount) {
                totalfileUploadSuccess += 1;
                perQueueUploadSuccess += 1;
            }

            if (perQueueUploadSuccess == maxParallelCount) {
                perQueueUploadSuccess = 0;
                myDropzone.processQueue();
            }
            if (totalfileUploadSuccess == queueCount) {
                myDropzone.removeAllFiles(true);
                hideLoader();
                displaySuccessMessage(message.document_upload_success);

                $('.divSuccessDocument').hide();
                $('#divSuccessbutton').show();

                // VIEWSCREEN.show();
                // ADDSCREEN.hide();
                BTNUPLOAD.hide();

                buCtPage.showList();
            }
        });

        this.on("error", function(file, errorMessage) {
            displayMessage(errorMessage);
            addedfiles = [];
            myDropzone.removeAllFiles(true);
        });
    }
});

function BulkCompletedTaskCurrentYear() {
    this._ActionMode = null;
    this._ListDataForView = [];
}

buCtPage = new BulkCompletedTaskCurrentYear();

//initialization & master list filter
$(document).ready(function() {
    pageControls();
    buCtPage.showList();
});