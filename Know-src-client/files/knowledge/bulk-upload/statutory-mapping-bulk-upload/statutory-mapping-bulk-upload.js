
var ListContainer = $('.tbody-sm-csv-list1');
var AddScreen = $("#sm-csv-add");
var ViewScreen = $("#sm-csv-view");
var AddButton = $("#btn-csv-add");
var CancelButton = $("#btn-sm-csv-cancel");
var SubmitButton = $("#btn-submit");
var ListRowTemplate = $('#templates .table-sm-csv-info .table-row');

var TemplateDiv = $('.dwn-template')
var FileUploadCsv = $("#bu-upload-csv");

var DataSummary = $("#bu-data-summary");
var ErrorSummary = $('#bu-error-summary');

var SummaryTotal = $('#bu-summary-total');
var SummaryValid = $('#bu-summary-valid');
var SummaryInvalid = $('#bu-summary-invalid');
var SummaryMandatory = $('#bu-summary-mandatory');
var summaryMaxLength = $('#bu-summary-maxlength');
var SummaryDuplicate = $('#bu-summary-duplicate');
var SummaryInvalidChar = $('#bu-summary-invalidchar');
var SummaryInvalidData = $('#bu-summary-invaliddata');
var SummaryInactive = $('#bu-summary-inactive');
var SummaryFrequencyInvalid = $("#bu-frequency-invalid");

var UploadDocument = $("#bu-upload-docs");
var DocumentSummary = $('#bu-doc-summary');
var DocumentTotal = $('#bu-doc-total');
var DocumentUploaded = $('#bu-upload-total');
var DocumentRemaining = $('#bu-remain-total');

var lblCountryName = $('.lbl-c-name');
var lblDomainName = $('.lbl-d-name');
var txtCountryName = $('.txt-c-name');
var txtDomainName = $('.txt-d-name');

var inputFileControl = $('.inp-file')
var displayFileControl = $('.disp-file')

var Msg_pan = $(".error-message");
var buSmPage = null;

var SearchCsvName = $("#search-csv-name");

var ValidorInvalidButton = $('.dropbtn');


// auto complete - country
var countryVal = $('#countryid');
var countryAc = $("#countryname");
var AcCountry = $('#ac-country');

// auto complete - domain
var domainVal = $('#domainid');
var domainAc = $("#domainname");
var AcDomain = $('#ac-domain')

var csvInfo = null;
var docNames = [];
var csvId = null;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
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
    AddScreen.hide();
    ViewScreen.show();
    SearchCsvName.val('');
    this.fetchListData();
};
BulkUploadStatutoryMapping.prototype.hideSummary = function() {
    DataSummary.hide();
    ErrorSummary.hide();
    DocumentSummary.hide();
    ValidorInvalidButton.hide();
};
BulkUploadStatutoryMapping.prototype.showAddScreen = function() {
    ViewScreen.hide();
    AddScreen.show();
    countryAc.focus();
    UploadDocument.hide();

    lblDomainName.hide();
    lblCountryName.hide();
    txtCountryName.show();
    txtDomainName.show();

    inputFileControl.show();
    displayFileControl.hide();
    this.hideSummary();
    countryVal.val('');
    countryAc.val('');
    domainVal.val('');
    domainAc.val('');
    FileUploadCsv.val('');
    TemplateDiv.show();

    this._ActionMode = "add";

    this.fetchDropDownData();
};
BulkUploadStatutoryMapping.prototype.renderList = function(list_data) {
    var t_this = this;
    var j = 1;
    ListContainer.find('tr').remove();
    if(list_data.length == 0) {
        ListContainer.empty();
        var tableRow4 = $(
            '#no-record-templates .table-no-content .table-row-no-content'
        );
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        ListContainer.append(clone4);
    }
    else {
        $.each(list_data, function(idx, data) {
            var balance = data.no_of_documents - data.uploaded_documents ;
            var cloneRow = ListRowTemplate.clone();
            var cname_split = data.csv_name.split("_");
            cname_split.pop();
            var cname = cname_split.join("_");
            $('.sno', cloneRow).text(j);
            $('.csv-name', cloneRow).text(cname);
            $('.uploaded-on', cloneRow).text(data.uploaded_on);
            $('.tot-records', cloneRow).text(data.no_of_records);
            $('.expec-docs', cloneRow).text(data.no_of_documents);
            $('.uploaded-docs', cloneRow).text(data.uploaded_documents);
            $('.remaining-docs', cloneRow).text(balance);
            csvId = data.csv_id;
            docNames = data.doc_names;
            $('.upload i', cloneRow).on('click', function(){
                t_this.showEdit(data);
            });
            ListContainer.append(cloneRow);
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
                AddButton.hide();
            }
            else {
                AddButton.show();
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
    mirror.getDomainList(function (error, response) {
        if (error == null) {
            t_this._DomainList = response.domains;
            t_this._CountryList = response.countries
            hideLoader();
        }
        else{
            hideLoader();
            t_this.possibleFailures(error);
        }
    });
};
BulkUploadStatutoryMapping.prototype.uploadCsv = function() {
    var t_this = this;
    var args = {
        "c_id": parseInt(countryVal.val()),
        "c_name": countryAc.val(),
        "d_id": parseInt(domainVal.val()),
        "d_name": domainAc.val(),
        "csv_name": csvInfo["file_name"],
        "csv_data": csvInfo["file_content"],
        "csv_size": csvInfo["file_size"]

    };
    bu.uploadStatutoryMappingCSV(args, function (error, response) {
        console.log("error-> "+ error);
        console.log("Response-> "+ response);
        TemplateDiv.hide();
        if (error == null) {
            if (response.invalid == 0) {
                displaySuccessMessage(message.upload_success);
                if (response.doc_count > 0) {
                    csvId = response.csv_id;
                    DataSummary.show();
                    ErrorSummary.hide();
                    DataSummary.removeClass("col-sm-6");
                    DataSummary.addClass("col-sm-12");
                    SummaryTotal.text(response.total);
                    SummaryValid.text(response.valid);
                    SummaryInvalid.text(response.invalid);
                    docNames = response.doc_names;
                    UploadDocument.show();
                    DocumentSummary.hide();
                    t_this.changeTxttoLabel(countryAc.val(), domainAc.val(), response.csv_name)
                }
                else {
                    DataSummary.hide();
                    ErrorSummary.hide();
                    t_this.showList();
                }

            }
            else {
                displayMessage(message.upload_failed);
                DataSummary.show();
                ErrorSummary.show();
                // show error summary
                ValidorInvalidButton.show();

                SummaryTotal.text(response.total);
                SummaryValid.text(response.valid);
                SummaryInvalid.text(response.invalid);
                SummaryMandatory.text(response.mandatory_error);
                summaryMaxLength.text(response.max_length_error);
                SummaryDuplicate.text(response.duplicate_error);
                SummaryInvalidChar.text(response.invalid_char_error);
                SummaryInvalidData.text(response.invalid_data_error);
                SummaryInactive.text(response.inactive_error);
                SummaryFrequencyInvalid.text(response.invalid_frequency_error);

                invalid_file = response.invalid_file.split('.');
                var csv_path = "/invalid_file/csv/" + invalid_file[0] + '.csv';
                var xls_path = "/invalid_file/xlsx/" + invalid_file[0] + '.xlsx';
                var ods_path = "/invalid_file/ods/" + invalid_file[0] + '.ods';
                var txt_path = "/invalid_file/txt/" + invalid_file[0] + '.txt';
                $('#csv-type').attr("href", csv_path);
                $('#xls-type').attr("href", xls_path);
                $('#ods-type').attr("href", ods_path);
                $('#txt-type').attr("href", txt_path);
            }

        }
        else {
                if (error == "CsvFileExeededMaxLines") {
                    displayMessage(message.csv_max_lines_exceeded.replace(
                        'MAX_LINES', response.csv_max_lines));
                }
                else{
                    buSmPage.possibleFailures(error);
                }
        }
    })
};

BulkUploadStatutoryMapping.prototype.validateControls = function() {
    if (countryVal.val() == '') {
        displayMessage(message.country_required);
        return false;
    }
    else if (domainVal.val() == '') {
        displayMessage(message.domain_required);
        return false
    }
    else if (FileUploadCsv.val() == '') {
        displayMessage(message.upload_csv);
        return false
    }
    return true;
};
BulkUploadStatutoryMapping.prototype.changeTxttoLabel = function(
    c_name, d_name, csv_name
) {
    txtCountryName.hide();
    txtDomainName.hide();
    lblCountryName.show();
    lblDomainName.show();
    lblCountryName.text(c_name);
    lblDomainName.text(d_name);
    inputFileControl.hide();
    displayFileControl.show();
    var cname_split = csv_name.split("_");
    cname_split.pop();
    var cname = cname_split.join("_") + ".csv";
    $('.csv-file-name').text(cname);
    $('.csv-file-view').attr("href", "/uploaded_file/csv/"+csv_name);
    $('.csv-file-download').attr("href", "/uploaded_file/csv/"+csv_name);
    this._ActionMode = "upload"
};
BulkUploadStatutoryMapping.prototype.showEdit = function(data) {
    this.showAddScreen();
    countryAc.val(data.c_name);
    countryVal.val(data.c_id);
    domainAc.val(data.d_name);
    domainVal.val(data.d_id);
    this.changeTxttoLabel(data.c_name, data.d_name, data.csv_name)
    UploadDocument.show();
    DocumentSummary.show();
    DocumentTotal.text(data.no_of_documents);
    DocumentUploaded.text(data.uploaded_documents);
    DocumentRemaining.text(
        parseInt(data.no_of_documents) - parseInt(data.uploaded_documents)
    );


};
function key_search(mainList) {
    var csv_key = SearchCsvName.val().toLowerCase();
    var fList = [];
    for (var entity in mainList) {
        var csvName = mainList[entity].csv_name;
        var cname_split = csvName.split("_");
        cname_split.pop();
        var cname = cname_split.join("_");
        if (~cname.toLowerCase().indexOf(csv_key)) {
            fList.push(mainList[entity]);
        }
    }
    return fList
}
// page control events
function PageControls() {
    AddButton.click(function() {
        console.log("add button click")
        buSmPage.showAddScreen();
    });

    CancelButton.click(function() {
        buSmPage.showList();
    });

    countryAc.keyup(function(e){
        var condition_fields = ["is_active"];
        var condition_values = [true];
        var text_val = $(this).val();
        commonAutoComplete(
            e, AcCountry, countryVal, text_val,
            buSmPage._CountryList, "country_name", "country_id",
            function (val) {
                onAutoCompleteSuccess(countryAc, countryVal, val);
            }, condition_fields, condition_values
        );


    });

  domainAc.keyup(function(e){
    var domainList = buSmPage._DomainList;
    var text_val = $(this).val();
    var domain_list = [];
    var c_ids = null;
    var check_val = false;
    if(countryVal.val() != ''){
      for(var i=0;i<domainList.length;i++){
        c_ids = domainList[i].country_ids;

        for(var j=0;j<c_ids.length;j++){
          if(c_ids[j] == countryVal.val())
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
        e, AcDomain, domainVal, text_val,
        domain_list, "domain_name", "domain_id", function (val) {
            onAutoCompleteSuccess(domainAc, domainVal, val);
     });
    }
    else{
      displayMessage(message.country_required);
    }
  });

  FileUploadCsv.change(function(e) {
    if ($(this).val() != '') {
        bu.uploadCSVFile(e, function(status, response) {
            if (status == false) {
                buSmPage.possibleFailures(response)
            }
            else {
                csvInfo = response;
            }

        })
    }
  });

  SubmitButton.click(function() {
    buSmPage.hideSummary();
    if (buSmPage._ActionMode == "add") {
        if (buSmPage.validateControls() == true) {
            buSmPage.uploadCsv();

        }
    }
    else {
        displayLoader();
        myDropzone.processQueue();
    }
  });

  SearchCsvName.keyup(function(){
    var fList = key_search(buSmPage._ListDataForView);
    buSmPage.renderList(fList);
  });

}

function file_upload_rul() {
    var session_id = mirror.getSessionToken();

    var file_base_url = "/temp/upload?session_id=" +
        session_id + "&csvid=" + csvId
    console.log(file_base_url)
    return file_base_url;
}


Dropzone.autoDiscover = false;
Dropzone.autoProcessQueue = false;
var addedfiles = []
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
            if (jQuery.inArray(file.name, addedfiles) > -1) {
                myDropzone.removeFile(file);
            }
            if (jQuery.inArray(file.name, docNames) == -1) {
                myDropzone.removeFile(file);
            }
            else {
                addedfiles.push(file.name);
                queueCount += 1;
            }

        });
        this.on("removedfile", function(file) {
            console.log(file.name);
            if (jQuery.inArray(file.name, addedfiles) > -1) {
                addedfiles.pop(file.name);
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
            if (totalfileUploadSuccess == queueCount) {
                myDropzone.removeAllFiles(true);
                hideLoader()
                displaySuccessMessage(message.document_upload_success)
                buSmPage.showList();
            }

            //
            //
        });

        this.on("error", function(file, errorMessage) {
            displayMessage(errorMessage);
            addedfiles = []
            myDropzone.removeAllFiles(true);
        });
    }
});

buSmPage = new BulkUploadStatutoryMapping();

$(document).ready(function() {
    PageControls();
    buSmPage.showList();
});
