
var ListContainer = $('.tbody-sm-csv-list1');
var AddScreen = $("#sm-csv-add");
var ViewScreen = $("#sm-csv-view");
var AddButton = $("#btn-csv-add");
var CancelButton = $("#btn-sm-csv-cancel");
var SubmitButton = $("#btn-submit");
var ListRowTemplate = $('#templates .table-sm-csv-info .table-row');

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
var bu_sm_page = null;

var SearchCsvName = $("#search-csv-name");


// auto complete - country
var country_val = $('#countryid');
var country_ac = $("#countryname");
var AcCountry = $('#ac-country');

// auto complete - domain
var domain_val = $('#domainid');
var domain_ac = $("#domainname");
var AcDomain = $('#ac-domain')

var csvInfo = null;
var docNames = [];

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
BulkUploadStatutoryMapping.prototype.showAddScreen = function() {
    ViewScreen.hide();
    AddScreen.show();
    country_ac.focus();
    UploadDocument.hide();
    DocumentSummary.hide();
    DataSummary.hide();
    ErrorSummary.hide();
    lblDomainName.hide();
    lblCountryName.hide();
    txtCountryName.show();
    txtDomainName.show();
    inputFileControl.show();
    displayFileControl.hide();
    this._ActionMode = "add";
    this.fetchDropDownData();
};
BulkUploadStatutoryMapping.prototype.renderList = function(list_data) {
    t_this = this;
    var j = 1;
    ListContainer.find('tr').remove();
    if(list_data.length == 0) {
        ListContainer.empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        ListContainer.append(clone4);
    }
    else {
        $.each(list_data, function(idx, data) {
            balance = data.no_of_documents - data.uploaded_documents ;
            var cloneRow = ListRowTemplate.clone();
            cname_split = data.csv_name.split("_");
            cname_split.pop();
            cname = cname_split.join("_") + ".csv";
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
            ListContainer.append(cloneRow);
            j += 1;
        });
    }
    $('[data-toggle="tooltip"]').tooltip();
};
BulkUploadStatutoryMapping.prototype.fetchListData = function(first_argument) {
    t_this = this;
    displayLoader();
    bu.getStatutoryMappingCsvList(function(error, response) {
        if (error == null) {
            t_this._ListDataForView = response.csv_list;
            t_this.renderList(t_this._ListDataForView);
            hideLoader();
        }
        else{
            hideLoader();
            t_this.possibleFailures(error);
        }
    });
};
BulkUploadStatutoryMapping.prototype.fetchDropDownData = function() {
    t_this = this;
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
    t_this = this;
    var args = {
        "c_id": parseInt(country_val.val()),
        "c_name": country_ac.val(),
        "d_id": parseInt(domain_val.val()),
        "d_name": domain_ac.val(),
        "csv_name": csvInfo["file_name"],
        "csv_data": csvInfo["file_content"],
        "csv_size": csvInfo["file_size"]

    };
    bu.uploadStatutoryMappingCSV(args, function (error, response) {
        if (error == null) {
            if (response.invalid == 0) {
                displayMessage(message.upload_success);
                if (response.doc_count > 0) {
                    DataSummary.show();
                    ErrorSummary.hide();
                    SummaryTotal.text(response.total);
                    SummaryValid.text(response.valid);
                    SummaryInvalid.text(response.invalid);
                    docNames = response.doc_names;
                    UploadDocument.show();
                }
                else {
                    DataSummary.hide();
                    ErrorSummary.hide();
                    t_this.showList();
                }

            }
            else {
                DataSummary.show();
                ErrorSummary.show();
                // show error summary

                SummaryTotal.text(response.total);
                SummaryValid.text(response.valid);
                SummaryInvalid.text(response.invalid);
                SummaryMandatory.text(response.mandatory_error);
                summaryMaxLength.text(response.max_length_error);
                SummaryDuplicate.text(response.duplicate_error);
                SummaryInvalidChar.text(response.invalid_char_error);
                SummaryInvalidData.text(response.invalid_data_error);
                SummaryInactive.text(response.inactive_error);
            }

        }
    })
};

BulkUploadStatutoryMapping.prototype.validateControls = function() {
    if (country_val.val() == '') {
        displayMessage(message.country_required);
        return false;
    }
    else if (domain_val.val() == '') {
        displayMessage(message.domain_required);
        return false
    }
    else if (FileUploadCsv.val() == '') {
        displayMessage(message.upload_csv);
        return false
    }
    return true;
};
BulkUploadStatutoryMapping.prototype.showEdit = function(data) {
    this.showAddScreen();
    country_ac.val(data.c_name);
    country_val.val(data.c_id);
    domain_ac.val(data.d_name);
    domain_val.val(data.d_id);
    txtCountryName.hide();
    txtDomainName.hide();
    lblCountryName.show();
    lblDomainName.show();
    lblCountryName.text(data.c_name);
    lblDomainName.text(data.d_name);
    inputFileControl.hide();
    displayFileControl.show();
    cname_split = data.csv_name.split("_");
    cname_split.pop();
    cname = cname_split.join("_") + ".csv";
    $('.csv-file-name').text(cname);
    $('.csv-file-view').attr("href", "/uploaded_csv/"+data.csv_name);
    $('.csv-file-download').attr("href", "/uploaded_csv/"+data.csv_name);
    UploadDocument.show();
    DocumentSummary.show();
    DocumentTotal.text(data.no_of_documents);
    DocumentUploaded.text(data.uploaded_documents);
    DocumentRemaining.text(parseInt(data.no_of_documents) - parseInt(data.uploaded_documents));
    this._ActionMode = "edit"

};
function key_search(mainList) {
    csv_key = SearchCsvName.val().toLowerCase();


    var fList = [];
    for (var entity in mainList) {
        csvName = mainList[entity].csv_name;

        if (~csvName.toLowerCase().indexOf(csv_key)) {
            fList.push(mainList[entity]);
        }
    }
    return fList
}
// page control events
function PageControls() {
    AddButton.click(function() {
        console.log("add button click")
        bu_sm_page.showAddScreen();
    });

    CancelButton.click(function() {
        bu_sm_page.showList();
    });

    country_ac.keyup(function(e){
        var condition_fields = ["is_active"];
        var condition_values = [true];
        var text_val = $(this).val();
        commonAutoComplete(
            e, AcCountry, country_val, text_val,
            bu_sm_page._CountryList, "country_name", "country_id", function (val) {
                onAutoCompleteSuccess(country_ac, country_val, val);
            }, condition_fields, condition_values
        );


    });

  domain_ac.keyup(function(e){
    var domainList = bu_sm_page._DomainList;
    var text_val = $(this).val();
    var domain_list = [];
    var c_ids = null;
    var check_val = false;
    if(country_val.val() != ''){
      for(var i=0;i<domainList.length;i++){
        c_ids = domainList[i].country_ids;

        for(var j=0;j<c_ids.length;j++){
          if(c_ids[j] == country_val.val())
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
        e, AcDomain, domain_val, text_val,
        domain_list, "domain_name", "domain_id", function (val) {
            onAutoCompleteSuccess(domain_ac, domain_val, val);
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
                bu_sm_page.possibleFailures(response)
            }
            else {
                csvInfo = response;
            }

        })
    }
  });

  SubmitButton.click(function() {
    if (bu_sm_page._ActionMode == "add") {
        if (bu_sm_page.validateControls() == true) {
            bu_sm_page.uploadCsv();
        }
    }
    else {

    }
  });

  SearchCsvName.keyup(function(){
    fList = key_search(bu_sm_page._ListDataForView);
    bu_sm_page.renderList(fList);
  });

}
bu_sm_page = new BulkUploadStatutoryMapping();

$(document).ready(function() {
    PageControls();
    bu_sm_page.showList();
});
