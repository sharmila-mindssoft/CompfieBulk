var LIST_CONTAINER = $('.tbody-sm-csv-list1');
var ADD_SCREEN = $("#sm_csv_add");
var VIEW_SCREEN = $("#sm_csv_view");
var ADD_BUTTON = $("#btn_csv_add");
var CANCEL_BUTTON = $("#btn_sm_csv_cancel");
var SUBMIT_BUTTON = $("#btn_submit");
var LIST_ROW_TEMPLATE = $('#templates .table-sm-csv-info .table-row');
var INVALID_FILE_NAME = null;

var TEMPLATE_DIV = $('.dwn-template')
var FILE_UPLOAD_CSV = $("#bu_upload_csv");

var DATA_SUMMARY = $("#bu_data_summary");
var ERROR_SUMMARY = $('#bu_error_summary');

var SUMMARY_TOTAL = $('#bu_summary_total');
var SUMMARY_VALID = $('#bu_summary_valid');
var SUMMARY_INVALID = $('#bu_summary_invalid');
var SUMMARY_MANDATORY = $('#bu_summary_mandatory');
var SUMMARY_MAX_LENGTH = $('#bu_summary_maxlength');
var SUMMARY_DUPLICATE = $('#bu_summary_duplicate');
var SUMMARY_INVALID_CHAR = $('#bu_summary_invalidchar');
var SUMMARY_INVALID_DATA = $('#bu_summary_invaliddata');
var SUMMARY_INACTIVE = $('#bu_summary_inactive');
var SUMMARY_FREQUENCY_INVALID = $("#bu_frequency_invalid");

var UPLOAD_DOCUMENT = $("#bu_upload_docs");
var DOCUMENT_SUMMARY = $('#bu_doc_summary');
var DOCUMENT_TOTAL = $('#bu_doc_total');
var DOCUMENT_UPLOADED = $('#bu_upload_total');
var DOCUMENT_REMAINING = $('#bu_remain_total');

var UPL_DOC_TXT = $("#bu_upl_txt");
var UPL_DOC_REM = $("#bu_upl_rem");

var LBL_COUNTRY_NAME = $('.lbl-c-name');
var LBL_DOMAIN_NAME = $('.lbl-d-name');
var TXT_COUNTRY_NAME = $('.txt-c-name');
var TXT_DOMAIN_NAME = $('.txt-d-name');

var INPUT_FILE_CONTROL = $('.inp-file');
var DISPLAY_FILE_CONTROL = $('.disp-file');
var MSG_PAN = $(".error-message");
var BU_SMPAGE = null;
var SEARCH_CSV_NAME = $("#search_csv_name");
var VALIDOR_INVALID_BUTTON = $('.dropbtn');

// auto complete - country
var COUNTRY_VAL = $('#countryid');
var COUNTRY_AC = $("#countryname");
var AC_COUNTRY = $('#ac_country');

// auto complete - domain
var DOMAIN_VAL = $('#domainid');
var DOMAIN_AC = $("#domainname");
var AC_DOMAIN = $('#ac_domain')

var CSV_INFO = null;
var DOC_NAMES = [];
var CSV_ID = null;
var ACTUAL_CSV_NAME = '';

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
function onAutoCompleteSuccess(value_element, id_element, val) {
    var current_id;
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    current_id = id_element[0].id;
    if(current_id == 'countryid'){
      $('#domainname').val('');
      $('domainid').val('');
    }
}

// page related methods
function BulkUploadStatutoryMapping() {
    this._CountryList = [];
    this._DomainList = [];
    this._ListDataForView = [];
    this._ActionMode = null;
}
BulkUploadStatutoryMapping.prototype.possibleFailures = function(error) {
    displayMessage(error);
};
BulkUploadStatutoryMapping.prototype.showList = function() {
    ADD_SCREEN.hide();
    VIEW_SCREEN.show();
    SEARCH_CSV_NAME.val('');
    this.fetchListData();
};
BulkUploadStatutoryMapping.prototype.hideSummary = function() {
    DATA_SUMMARY.hide();
    ERROR_SUMMARY.hide();
    DOCUMENT_SUMMARY.hide();
    VALIDOR_INVALID_BUTTON.hide();
};
BulkUploadStatutoryMapping.prototype.showAddScreen = function() {
    VIEW_SCREEN.hide();
    ADD_SCREEN.show();
    COUNTRY_AC.focus();
    UPLOAD_DOCUMENT.hide();

    LBL_DOMAIN_NAME.hide();
    LBL_COUNTRY_NAME.hide();
    TXT_COUNTRY_NAME.show();
    TXT_DOMAIN_NAME.show();

    INPUT_FILE_CONTROL.show();
    DISPLAY_FILE_CONTROL.hide();
    this.hideSummary();
    COUNTRY_VAL.val('');
    COUNTRY_AC.val('');
    DOMAIN_VAL.val('');
    DOMAIN_AC.val('');
    FILE_UPLOAD_CSV.val('');
    TEMPLATE_DIV.show();

    this._ActionMode = "add";
    this.fetchDropDownData();
};
BulkUploadStatutoryMapping.prototype.renderList = function(list_data) {
    var t_this = this;
    var j = 1;
    var tableRow4 ='';
    var clone4 = '';
    var balance;
    var cloneRow;
    var cname;
    var cname_split;
    LIST_CONTAINER.find('tr').remove();
    if(list_data.length == 0) {
        LIST_CONTAINER.empty();
        tableRow4 = $(
            '#no_record_templates .table-no-content .table-row-no-content'
        );
        clone4 = tableRow4.clone();
        $('.no-records', clone4).text('No Records Found');
        LIST_CONTAINER.append(clone4);
    }
    else {
        $.each(list_data, function(idx, data) {
            balance = data.no_of_documents - data.uploaded_documents ;
            cloneRow = LIST_ROW_TEMPLATE.clone();

            cname_split = data.csv_name.split("_");
            cname_split.pop();
            cname = cname_split.join("_");

            $('.sno', cloneRow).text(j);
            $('.csv-name', cloneRow).text(cname);
            $('.uploaded-on', cloneRow).text(data.uploaded_on);
            $('.tot-records', cloneRow).text(data.no_of_records);
            $('.expec-docs', cloneRow).text(data.no_of_documents);
            $('.uploaded-docs', cloneRow).text(data.uploaded_documents);
            $('.remaining-docs', cloneRow).text(balance);

            $('.upload i', cloneRow).on('click', function(){
                t_this.showEdit(data);
            });
            LIST_CONTAINER.append(cloneRow);
            j += 1;
        });
    }
    $('[data-toggle="tooltip"]').tooltip();
};
BulkUploadStatutoryMapping.prototype.fetchListData = function(first_argument) {
    var t_this = this;
    displayLoader();
    bu.getStatutoryMappingCsvList(function(error, response) {
        if (error == null) {
            t_this._ListDataForView = response.csv_list;
            t_this.renderList(t_this._ListDataForView);
            if (response.upload_more == false) {
                displayMessage(message.upload_limit)
                ADD_BUTTON.hide();
            }
            else {
                ADD_BUTTON.show();
            }
            hideLoader();
        }
        else{
            hideLoader();
            t_this.possibleFailures(error);
        }
    });
};
BulkUploadStatutoryMapping.prototype.fetchDropDownData = function() {
    var t_this = this;
    displayLoader();
    bu.getDomainList(function (error, response) {
        if (error == null) {
            t_this._DomainList = response.bsm_domains;
            t_this._CountryList = response.bsm_countries
            hideLoader();
        }
        else{
            hideLoader();
            t_this.possibleFailures(error);
        }
    });
};
BulkUploadStatutoryMapping.prototype.uploadCsv = function() {
    $('#myModal').modal('show');
    console.log("CSV_INFO -> "+ JSON.stringify(CSV_INFO));
    var t_this = this;
    var args = {
        "c_id": parseInt(COUNTRY_VAL.val()),
        "c_name": COUNTRY_AC.val(),
        "d_id": parseInt(DOMAIN_VAL.val()),
        "d_name": DOMAIN_AC.val(),
        "csv_name": CSV_INFO["file_name"],
        "csv_data": CSV_INFO["file_content"],
        "csv_size": CSV_INFO["file_size"]

    };
    bu.uploadStatutoryMappingCSV(args, function (error, response) {
        var csv_path;
        var xls_path;
        var ods_path;
        console.log("error-> "+ error);
        console.log("Response-> "+ response);
        $('#myModal').modal('hide');
        TEMPLATE_DIV.hide();
        if (error == null) {
            console.log(JSON.stringify(response));
            if (response.invalid == 0) {
                displaySuccessMessage(message.upload_success);
                if (response.doc_count > 0) {
                    CSV_ID = response.csv_id;
                    DATA_SUMMARY.show();
                    ERROR_SUMMARY.hide();
                    DATA_SUMMARY.removeClass("col-sm-6");
                    DATA_SUMMARY.addClass("col-sm-12");
                    SUMMARY_TOTAL.text(response.total);
                    SUMMARY_VALID.text(response.valid);
                    SUMMARY_INVALID.text(response.invalid);
                    DOC_NAMES = response.doc_names;

                    UPLOAD_DOCUMENT.show();
                    DOCUMENT_TOTAL.text(response.doc_count);
                    UPL_DOC_TXT.hide();
                    UPL_DOC_REM.hide();

                    DOCUMENT_SUMMARY.hide();
                    t_this.changeTxttoLabel(COUNTRY_AC.val(), DOMAIN_AC.val(),
                                            response.csv_name,
                                            response.new_csv_name)
                }
                else {
                    DATA_SUMMARY.hide();
                    ERROR_SUMMARY.hide();
                    t_this.showList();
                }
            }
            else {
                displayMessage(message.upload_failed);
                FILE_UPLOAD_CSV.val("");
                DATA_SUMMARY.removeClass("col-sm-12");
                DATA_SUMMARY.addClass("col-sm-6");
                DATA_SUMMARY.show();
                ERROR_SUMMARY.show();
                // show error summary
                VALIDOR_INVALID_BUTTON.show();

                SUMMARY_TOTAL.text(response.total);
                SUMMARY_VALID.text(response.valid);
                SUMMARY_INVALID.text(response.invalid);
                SUMMARY_MANDATORY.text(response.mandatory_error);
                SUMMARY_MAX_LENGTH.text(response.max_length_error);
                SUMMARY_DUPLICATE.text(response.duplicate_error);
                SUMMARY_INVALID_CHAR.text(response.invalid_char_error);
                SUMMARY_INVALID_DATA.text(response.invalid_data_error);
                SUMMARY_INACTIVE.text(response.inactive_error);
                SUMMARY_FREQUENCY_INVALID.text(
                    response.invalid_frequency_error
                    );

                INVALID_FILE_NAME = response.invalid_file.split('.');
                csv_path = "/invalid_file/csv/"
                            + INVALID_FILE_NAME[0] + '.csv';
                xls_path = "/invalid_file/xlsx/"
                            + INVALID_FILE_NAME[0] + '.xlsx';
                ods_path = "/invalid_file/ods/"
                            + INVALID_FILE_NAME[0] + '.ods';

                $('#csv_type').attr("href", csv_path);
                $('#xls_type').attr("href", xls_path);
                $('#ods_type').attr("href", ods_path);
            }

        }
        else {
            if(error == "RejectionMaxCountReached"){
                displayMessage(message.upload_limit);
            }
            else if (error == "CsvFileExeededMaxLines") {
                displayMessage(message.csv_max_lines_exceeded.replace(
                    'MAX_LINES', response.csv_max_lines));
                FILE_UPLOAD_CSV.val("");
            }else if(error == "CsvFileCannotBeBlank") {
                displayMessage(message.csv_file_blank);
                FILE_UPLOAD_CSV.val("");
            }
            else{
                BU_SMPAGE.possibleFailures(error);
                FILE_UPLOAD_CSV.val("");
            }
        }
    })
};

document.getElementById("txt_type").addEventListener("click", function(){
    if(INVALID_FILE_NAME != null) {
        $.get(
            "/invalid_file/txt/" + INVALID_FILE_NAME[0] + ".txt",
            function(data)
            {
               download(INVALID_FILE_NAME[0]+".txt", "text/plain", data);
            },
        'text');
    }
});

function download(filename, mime_type, text) {
    var element = document.createElement('a');
    var href = 'data:'+mime_type+';charset=utf-8,'+encodeURIComponent(text);
    element.setAttribute('href', href);
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

BulkUploadStatutoryMapping.prototype.validateControls = function() {
    if (COUNTRY_VAL.val() == '') {
        displayMessage(message.country_required);
        return false;
    }
    else if (DOMAIN_VAL.val() == '') {
        displayMessage(message.domain_required);
        return false
    }
    else if (FILE_UPLOAD_CSV.val() == '') {
        displayMessage(message.upload_csv);
        return false
    }
    return true;
};
BulkUploadStatutoryMapping.prototype.changeTxttoLabel = function(
    c_name, d_name, csv_name, uploadedCsvName
) {
    TXT_COUNTRY_NAME.hide();
    TXT_DOMAIN_NAME.hide();
    LBL_COUNTRY_NAME.show();
    LBL_DOMAIN_NAME.show();
    LBL_COUNTRY_NAME.text(c_name);
    LBL_DOMAIN_NAME.text(d_name);
    INPUT_FILE_CONTROL.hide();
    DISPLAY_FILE_CONTROL.show();
    $('.csv-file-name').text(csv_name);
    $('#uploaded_csv_view').attr(
        'href', "/uploaded_file/csv/"+uploadedCsvName);
    $('#uploaded_csv_dwnl').attr(
        'href', "/uploaded_file/csv/"+uploadedCsvName);
    this._ActionMode = "upload";
};
BulkUploadStatutoryMapping.prototype.showEdit = function(data) {
    CSV_ID = data.csv_id;
    DOC_NAMES = data.doc_names;
    ACTUAL_CSV_NAME = data.csv_name;
    var uploadedCsvName = data.csv_name;
    var csv_split_name = uploadedCsvName.substring(
        0, uploadedCsvName.lastIndexOf("_") );
    this.showAddScreen();
    COUNTRY_AC.val(data.c_name);
    COUNTRY_VAL.val(data.c_id);
    DOMAIN_AC.val(data.d_name);
    DOMAIN_VAL.val(data.d_id);
    this.changeTxttoLabel(
        data.c_name, data.d_name, csv_split_name + ".csv", uploadedCsvName);
    UPLOAD_DOCUMENT.show();
    DOCUMENT_SUMMARY.show();
    DOCUMENT_TOTAL.text(data.no_of_documents);

    UPL_DOC_TXT.show();
    UPL_DOC_REM.show();

    DOCUMENT_UPLOADED.text(data.uploaded_documents);
    DOCUMENT_REMAINING.text(
        parseInt(data.no_of_documents) - parseInt(data.uploaded_documents)
    );
    TEMPLATE_DIV.hide();
    totalfileUploadSuccess = 0;
    queueCount = 0;
};

function key_search(mainList) {
    var csv_key = SEARCH_CSV_NAME.val().toLowerCase();
    var fList = [];
    var csvName, cname;
    var entity, cname_split;
    for (entity in mainList) {
        csvName = mainList[entity].csv_name;
        cname_split = csvName.split("_");
        cname_split.pop();
        cname = cname_split.join("_");
        if (~cname.toLowerCase().indexOf(csv_key)) {
            fList.push(mainList[entity]);
        }
    }
    return fList
}

// page control events
function PageControls() {
    ADD_BUTTON.click(function() {
        console.log("add button click")
        BU_SMPAGE.showAddScreen();
    });

    CANCEL_BUTTON.click(function() {
        BU_SMPAGE.showList();
        $(".dropzone > .dz-preview").remove();
        $(".dropzone").removeClass("dz-started");
        addedfiles = [];
    });

    COUNTRY_AC.keyup(function(e){
        var condition_fields = ["is_active"];
        var condition_values = [true];
        var text_val = $(this).val();
        DOMAIN_VAL.val('');
        commonAutoComplete(
            e, AC_COUNTRY, COUNTRY_VAL, text_val,
            BU_SMPAGE._CountryList, "country_name", "country_id",
            function (val) {
                onAutoCompleteSuccess(COUNTRY_AC, COUNTRY_VAL, val);
            }, condition_fields, condition_values
        );
    });

  DOMAIN_AC.keyup(function(e){
    var domainList = BU_SMPAGE._DomainList;
    var text_val = $(this).val();
    var domain_list = [];
    var c_ids = null;
    var check_val = false;
    var i;
    var j;
    if(COUNTRY_VAL.val() != ''){
      for(i = 0;i < domainList.length; i++){
        c_ids = domainList[i].country_ids;

        for(j=0;j<c_ids.length;j++){
          if(c_ids[j] == COUNTRY_VAL.val())
          {
            check_val = true;
          }
        }

        if(check_val == true && domainList[i].is_active == true){
          domain_list.push({
            "domain_id": domainList[i].domain_id,
            "domain_name": domainList[i].domain_name
          });
          check_val = false;
          //break;
        }
      }
      commonAutoComplete(
        e, AC_DOMAIN, DOMAIN_VAL, text_val,
        domain_list, "domain_name", "domain_id", function (val) {
            onAutoCompleteSuccess(DOMAIN_AC, DOMAIN_VAL, val);
     });
    }
    else{
      displayMessage(message.country_required);
    }
  });

  FILE_UPLOAD_CSV.change(function(e) {
    if ($(this).val() != '') {
        bu.uploadCSVFile(e, function(status, response) {
            if (status == false) {
                BU_SMPAGE.possibleFailures(response)
                FILE_UPLOAD_CSV.val("")
            }
            else {
                CSV_INFO = response;
            }

        })
    }
  });

  SUBMIT_BUTTON.click(function() {
    BU_SMPAGE.hideSummary();
    if (BU_SMPAGE._ActionMode == "add") {
        if (BU_SMPAGE.validateControls() == true) {
            BU_SMPAGE.uploadCsv();

        }
    }
    else {
        // Todo mandatory check
        console.log($(".dropzone > .dz-preview").length)
        if($(".dropzone > .dz-preview").length > 0){
            displayLoader();
            myDropzone.processQueue();
        }
        else{
            displayMessage(message.document_required);
            return false;
        }
    }
  });

  SEARCH_CSV_NAME.keyup(function(){
    var fList;
    fList = key_search(BU_SMPAGE._ListDataForView);
    BU_SMPAGE.renderList(fList);
  });

}

function file_upload_rul() {
    var session_id = mirror.getSessionToken();
    var file_base_url = "/ktemp/upload?session_id=" +
        session_id + "&csvid=" + CSV_ID
    console.log(file_base_url);
    return file_base_url;
}


Dropzone.autoDiscover = false;
Dropzone.autoProcessQueue = false;
var addedfiles = []
var totalfileUploadSuccess = 0;
var perQueueUploadSuccess = 0;
var queueCount = 0;
var maxParallelCount = 2;
var zip;
var myDropzone = new Dropzone("div#myDrop", {
    addRemoveLinks: true,
    autoProcessQueue: false,
    parallelUploads: maxParallelCount,
    url: "#",
    transformFile: function transformFile(file, done) {
      zip = new JSZip();
      zip.file(file.name, file);
      zip.generateAsync(
        {
          type:"blob",
          compression: "DEFLATE"
        }
      ).then(function(content) {
        done(content);
      });
    },
    init: function() {
        this.on("addedfile", function(file) {
            console.log("Added file-> " + file.name);
            console.log("addedfiles-> " + addedfiles);
            console.log("DOC_NAMES-> " + DOC_NAMES);
            if (jQuery.inArray(file.name, addedfiles) > -1) {
                myDropzone.removeFile(file);
            }
            if (jQuery.inArray(file.name, DOC_NAMES) == -1) {
                myDropzone.removeFile(file);
            }
            else {
                addedfiles.push(file.name);
                queueCount += 1;
            }
            console.log("addedfiles> " + addedfiles);
        });
        this.on("removedfile", function(file) {
            console.log(file.name);
            if (jQuery.inArray(file.name, addedfiles) > -1) {
                // addedfiles.pop(file.name);
                var indOfAddedFiles = addedfiles.indexOf(file.name);
                console.log("indOfAddedFiles -> "+ indOfAddedFiles);
                addedfiles.splice(indOfAddedFiles, 1);
                queueCount -= 1;
            }
        })

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
            console.log("totalfileUploadSuccess-> "+ totalfileUploadSuccess);
            console.log("queueCount->> "+ queueCount);
            if (totalfileUploadSuccess == queueCount) {
                myDropzone.removeAllFiles(true);
                console.log("DOC_NAMES.length->> "+ DOC_NAMES.length);
                console.log("totalfileUploadSuccess->> "+ totalfileUploadSuccess);
                if(DOC_NAMES.length == totalfileUploadSuccess){
                    var args = {
                        "c_name": COUNTRY_AC.val(),
                        "d_name": DOMAIN_AC.val(),
                        "csv_name": ACTUAL_CSV_NAME
                    };
                    bu.saveExecutiveMessage(args, function (error, response) {
                        console.log("response-> "+ response);

                    });

                    console.log("Send request to send message to manager");
                }else{
                    console.log("Files not yet uploaded fully");
                }
                hideLoader();
                displaySuccessMessage(message.document_upload_success)
                BU_SMPAGE.showList();
            }
        });
        this.on("error", function(file, errorMessage) {
            displayMessage(errorMessage);
            addedfiles = []
            myDropzone.removeAllFiles(true);
        });
    }
});

BU_SMPAGE = new BulkUploadStatutoryMapping();
$(document).ready(function() {
    PageControls();
    BU_SMPAGE.showList();
});