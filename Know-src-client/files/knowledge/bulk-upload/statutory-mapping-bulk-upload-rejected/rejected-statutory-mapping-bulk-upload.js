var COUNTRIES_LIST;
var DOMAIN_LIST;
var ALL_USER_INFO;
var USER_DETAILS;
var DOMAIN_IDS;
var EMP_CODE;
var EMP_NAME;
var REJECTED_STATUTORY_DATA;

var SYSTEM_REJECTED="COMPFIE";

var COUNTRY_VAL = $('#countryval');
var COUNTRY = $('#country');
var DOMAIN = $('#domain');
var DOMAIN_VAL = $('#domainval');
var AC_COUNTRY = $('#ac-country');
var AC_DOMAIN = $('#ac-domain');

var SHOW_BTN = $('#show');
var EXPORT_CSV = $('.export-csv');

var REPORT_VIEW = $('.grid-table-rpt');
var PASSWORD_SUBMIT_BTN = $('#password-submit');
var CURRENT_PASSWORD = $('#current-password');
var REMOVE_STATUTORY_CSV_ID;
var DOWNLOAD_LIMIT = 2;
var SYSTEM_REJECTED_ACTION = 3;

/**** User Level Category ***********/
var KM_USER_CATEGORY = 3;
var KE_USER_CATEGORY = 4;
var TM_USER_CATEGORY = 5;
var TM_USER_CATEGORY = 6;
var DM__USER_CATEGORY = 7;
var DE_USER_CATEGORY = 8;


// Creating New Class
rsm_page = new AssignStatutoryBulkReport();

function pageControls()
{
  //load group form list in autocomplete text box
  COUNTRY_VAL.keyup(function (e) {
    var textval = $(this).val();
    var ctry_grps=[];

      resetfilter("domain");
      for(var i=0;i<COUNTRIES_LIST.length;i++)
      {
        if(COUNTRIES_LIST[i].is_active==true){
          var occur = -1
          for(var j=0;j<ctry_grps.length;j++){
            if(ctry_grps[j].country_id == COUNTRIES_LIST[i].country_id){
              occur = 1;
              break;
            }
          }
          if(occur < 0){
            ctry_grps.push({
              "country_id": COUNTRIES_LIST[i].country_id,
              "country_name": COUNTRIES_LIST[i].country_name,
              "is_active": true
            });
          }

        }
      }
      commonAutoComplete(
          e, AC_COUNTRY, COUNTRY, textval,
          ctry_grps, "country_name", "country_id", function (val) {
            onAutoCompleteSuccess(COUNTRY_VAL, COUNTRY, val);
      });
  });


  //load legalentity form list in autocomplete text box
  DOMAIN_VAL.keyup(function (e) {
    resetfilter('');
    var textval = $(this).val();
    var d_list = [];
    var country_id = $('#country').val();
    var c_id;
    if($('#country').val() > 0)
    {
      var condition_fields = [];
      var condition_values = [];
      if($('#country').val() != ''){
        condition_fields.push("country_id");
        condition_values.push(COUNTRY.val());
      }
      for(var i =0; i < COUNTRIES_LIST.length; i++){
        if((COUNTRIES_LIST[i].country_id == country_id)){
          for(var j = 0; j < DOMAIN_LIST.length; j++){
            c_id=COUNTRIES_LIST[i].country_id
            if($.inArray(c_id, DOMAIN_LIST[j].country_ids) >= 0){
              d_list.push({
                "domain_id": DOMAIN_LIST[j].domain_id,
                "domain_name": DOMAIN_LIST[j].domain_name,
                "is_active": true
              });
            }
          }
        }
      }
        commonAutoComplete(
            e, AC_DOMAIN, DOMAIN, textval,
            d_list, "domain_name", "domain_id", function (val) {
                onAutoCompleteSuccess(DOMAIN_VAL, DOMAIN, val);
            });
    }

  });

  SHOW_BTN.click(function() {
    is_valid = rsm_page.validateMandatory();
    if (is_valid == true){
        processSubmit();
     }
});
}
function resetfilter(evt)
{
  if(evt=="domain")
  {
    DOMAIN_VAL.val('');
  }
  $('.tbody-usermappingdetails-list').empty();
  $('.grid-table-rpt').hide();
  $('.details').hide();
}
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
    if(current_id == 'country'){
    }
    else if(current_id == 'domainid'){
    }
}
// get statutory mapping report data from api
function processSubmit() {
    var CountryID = parseInt(COUNTRY.val());
    var DomainID = parseInt(DOMAIN.val());

        displayLoader();
        filterdata = {
            "c_id":CountryID,
            "d_id":DomainID,
        };
        function onSuccess(data) {

            $('.details').show();
            REJECTED_STATUTORY_DATA = data.rejected_data;
            if (REJECTED_STATUTORY_DATA.length == 0){
                $('.tbody-compliance').empty();
                var tableRow4 = $('#nocompliance-templates '
                  +'.table-nocompliances-list .table-row');
                var clone4 = tableRow4.clone();
                $('.tbl_norecords', clone4).text('No Records Found');
                $('.tbody-compliance').append(clone4);
                REPORT_VIEW.show();
                hideLoader();
            } else {
                REPORT_VIEW.show();
                loadCountwiseResult(REJECTED_STATUTORY_DATA);
                hideLoader();
            }
        }

        function onFailure(error) {
            displayMessage(error);
            hideLoader();
        }
        bu.getRejectedSMBulkData(filterdata, function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
}

//display statutory mapping details accoring to count
function loadCountwiseResult(data) {
    SNO=0;
    var csv_id;
    var csv_name;
    var total_no_of_tasks;
    var rejected_on;
    var reason_for_rejection;
    var statutory_action;
    var remove_action;
    var rejected_by;
    var decliened_count = '-';
    var file_download_count;
    var download_rejected_files;
    var delete_status;
    var reason_for_rejection;
    $('.tbody-compliance').empty();

    for (var entity in data) {
        delete_status='';
        SNO = parseInt(SNO) + 1;
        csv_id = data[entity].csv_id;
        csv_name = data[entity].csv_name_text;
        total_no_of_tasks = data[entity].total_records;
        rejected_on = data[entity].rejected_on;
        IsFullyRejected = data[entity].is_fully_rejected;
        RejectedReason = data[entity].rejected_reason;
        statutory_action = data[entity].statutory_action;
        file_download_count = data[entity].file_download_count;

        if(parseInt(IsFullyRejected)==1){
            remove_action='';
            reason_for_rejection=RejectedReason;
            $(ALL_USER_INFO).each(function(key,value){
              if(parseInt(data[entity].rejected_by)==value["user_id"]){
                  EMP_CODE = value["employee_code"];
                  EMP_NAME = value["employee_name"];
                  rejected_by=EMP_CODE+" - "+ EMP_NAME;
              }
            });
        }
        else if(parseInt(statutory_action)==SYSTEM_REJECTED_ACTION){
           rejected_by=SYSTEM_REJECTED;
           decliened_count = data[entity].declined_count;
           reason_for_rejection='';
        }

        if(parseInt(file_download_count)<1)
        {
          delete_status='style="display:none;"';
        }

        remove_action='<a id="delete_action_'+csv_id+'" '+delete_status+
        ' data-csv-id="'+csv_id+'" onclick="confirm_alert(this)" '+
        'title="Click here to remove">';

        remove_action+=' <i class="fa fa-times text-danger c-pointer"></i>';
        remove_action+='</a>';


        var tr = $('#act-templates .table-act-list .table-row-act-list');
        var clone1 = tr.clone();

        $('.tbl_sno', clone1).text(SNO);
        $('.tbl_upload_filename', clone1).text(csv_name);
        $(".tbl_rejected_on", clone1).text(rejected_on);
        $('.tbl_rejected_by', clone1).text(rejected_by);
        $('.tbl_no_of_tasks', clone1).text(total_no_of_tasks);
        $('.tbl_declined_count', clone1).text(decliened_count);
        $('.tbl_reason_for_rejection', clone1).text(reason_for_rejection);


        /***** Rejected File Downloads ********/
        if(parseInt(file_download_count)<2)
        {
          download_rejected_files='<i id="download_icon_'+csv_id+'" data-id="'+csv_id+'" class="fa fa-download text-primary c-pointer dropbtn" onclick="rejectedFiles(this)"></i>';
          download_rejected_files+='<div id="download_files_'+csv_id+'" class="dropdown-content">';
          download_rejected_files+='<a class="export-excel" data-format="excel" onclick="downloadClick('+csv_id+',this)" href="javascript:void(0);">Download Excel</a>';
          download_rejected_files+='<a class="export-csv" data-format="csv" onclick="downloadClick('+csv_id+', this)" href="javascript:void(0);">Download CSV</a>';
          download_rejected_files+='<a class="export-ods" data-format="ods" onclick="downloadClick('+csv_id+', this)" href="javascript:void(0);">Download ODS</a>';
          download_rejected_files+='<a class="export-text" data-format="text" onclick="downloadClick('+csv_id+', this)" href="javascript:void(0);">Download Text</a>';
          download_rejected_files+='</div>';
          $('.tbl_rejected_file', clone1).html(download_rejected_files);
        }
        $('.tbl_remove', clone1).html(remove_action);
        $('#datatable-responsive .tbody-compliance').append(clone1);
    }
    hideLoader();
}


function AssignStatutoryBulkReport() {}
// Fields Manadory validation
AssignStatutoryBulkReport.prototype.validateMandatory = function()
{
    is_valid = true;
    if (COUNTRY.val().trim().length == 0)
    {
        displayMessage(message.country_required);
        is_valid = false;
    }
    else if (DOMAIN.val().trim().length == 0)
    {
        displayMessage(message.domain_required);
        is_valid = false;
    }
    return is_valid;
};


//load all the filters
function initialize() {
   function onSuccess(data) {
        COUNTRIES_LIST = data.countries;
        DOMAIN_LIST = data.domains;
        ALL_USER_INFO = data.user_details;
        USER_DETAILS = data.user_details[0];
        DOMAIN_IDS = USER_DETAILS.country_wise_domain;
        EMP_CODE = USER_DETAILS.employee_code;
        EMP_NAME = USER_DETAILS.employee_name;
        hideLoader();
    }
    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
  mirror.getAdminUserList(function (error, response) {
    if (error == null) {
      onSuccess(response);
      hideLoader();
    } else {
      onFailure(error);
      hideLoader();
    }
  });
}

//validate password
function validateAuthentication(){
  var password = CURRENT_PASSWORD.val().trim();
  if (password.length == 0) {
    displayMessage(message.password_required);
    CURRENT_PASSWORD.focus();
    return false;
  } else if(validateMaxLength('password', password, "Password") == false) {
    return false;
  }
  displayLoader();
  mirror.verifyPassword(password, function(error, response) {
    if (error == null) {
      hideLoader();
      isAuthenticate = true;
      Custombox.close('#custom-modal-approve');
      displaySuccessMessage(message.password_authentication_success);
    } else {
      hideLoader();
      if (error == 'InvalidPassword') {
        displayMessage(message.invalid_password);
      }
    }
  });
}

PASSWORD_SUBMIT_BTN.click(function() {
  validateAuthentication();
});

function confirm_alert(event) {
  var country_id=COUNTRY.val();
  var DomainId=DOMAIN.val();
   swal({
        title: "Are you sure",
        text: "You want to permanently delete the file?",
        type: "success",
        showCancelButton: true,
        confirmButtonClass: 'btn-success waves-effect waves-light',
        confirmButtonText: 'Yes'
    }, function(isConfirm) {
      if(isConfirm){
          Custombox.open({
          target: '#custom-modal-approve',
          effect: 'contentscale',
          complete: function() {
            if (CURRENT_PASSWORD != null) {
                CURRENT_PASSWORD.focus();
                CURRENT_PASSWORD.val('');
            }
            isAuthenticate = false;
            COUNTRY.val(country_id);
            DOMAIN.val(DomainId);
        },
          close:   function() {
            COUNTRY.val(country_id);
            DOMAIN.val(DomainId);
             if(isAuthenticate){
                displayLoader();
                setTimeout(function() {
                  REMOVE_STATUTORY_CSV_ID=$(event).attr("data-csv-id");
                  RemoveStatutoryCsv(REMOVE_STATUTORY_CSV_ID, country_id,
                    DomainId);
                  hideLoader();
                }, 500);
             }

          }
        });
        return false;
      }
    })
}

function RemoveStatutoryCsv(REMOVE_STATUTORY_CSV_ID, country_id, DomainId){
    displayLoader();
    function onSuccess(data)
    {
      $('.details').show();
      COUNTRY.val(country_id);
      DOMAIN.val(DomainId);

      $('.details').show();
      $(this).show();

      REJECTED_STATUTORY_DATA = data.rejected_data;
      if (REJECTED_STATUTORY_DATA.length == 0)
      {
        $('.tbody-compliance').empty();
        var tableRow4 = $('#nocompliance-templates .table-nocompliances-list '
          +'.table-row');
        var clone4 = tableRow4.clone();
        $('.tbl_norecords', clone4).text('No Records Found');
        $('.tbody-compliance').append(clone4);
        REPORT_VIEW.show();
        hideLoader();
      }
      else
      {
        hideLoader();
        REPORT_VIEW.show();
        loadCountwiseResult(REJECTED_STATUTORY_DATA);
      }
      displaySuccessMessage(message.record_deleted);

    }
    function onFailure(error)
    {
      displayMessage(error);
      hideLoader();
    }

    filterdata = {
            "d_id":parseInt(DomainId),
            "csv_id":parseInt(REMOVE_STATUTORY_CSV_ID),
            "c_id":parseInt(country_id)
        };

   bu.deleteRejectedSMByCsvID(filterdata, function(error, response) {
            if (error == null) {
                onSuccess(response)
            } else {

                onFailure(error);
            }
        });
   hideLoader();
}

function downloadClick(CSV_ID, event)
{
  var c_id=COUNTRY.val();
  var d_id=DOMAIN.val();
  var download_file_format=$(event).attr("data-format");

    displayLoader();
    function onSuccess(data)
    {
      var updated_count;
      var data_csv_id;
      var download_count;
      var event_id="download_files_";
      //delete_action_
      updated_count = data.updated_count;

      data_csv_id=updated_count[0].csv_id;
      download_count=updated_count[0].download_count;
      if(parseInt(download_count)==1){
        event_id=event_id+data_csv_id;
        document.getElementById(event_id).classList.toggle("show");
        $("#delete_action_"+data_csv_id).attr("style","display:block");
      }
      else if(parseInt(download_count)>=parseInt(DOWNLOAD_LIMIT)){
        event_id=event_id+data_csv_id;
        document.getElementById(event_id).classList.toggle("show");
        $("#delete_action_"+data_csv_id).attr("style","display:block");
        $("#download_files_"+data_csv_id).remove();
        $("#download_icon_"+data_csv_id).remove();
      }
      displaySuccessMessage(message.download_files);
      hideLoader();
    }
    function onFailure(error){
      displayMessage(error);
      hideLoader();
    }
  //csv_id
  filterdata = {
            "csv_id":parseInt(CSV_ID)
          };

  request_dowload_data = {
            "csv_id":parseInt(CSV_ID),
            "c_id":parseInt(c_id),
            "d_id":parseInt(d_id),
            "download_format":download_file_format
        };
  bu.setDownloadClickCount(filterdata, function(error, response) {
      if (error == null) {
          onSuccess(response);
          requestDownload(request_dowload_data, download_file_format);
          displayLoader();
      } else {
          onFailure(error);
      }
  });
  hideLoader();
  return false;
}
function requestDownload(request_dowload_data, download_file_format)
{
  bu.downloadRejectedSMReportData(request_dowload_data, function(d_error, d_response)
  {
    if (d_error == null) {
          if(download_file_format=="csv") {
            $(location).attr('href', d_response.csv_link);
            hideLoader();
            return false;
          }
          else if(download_file_format=="excel") {
            $(location).attr('href', d_response.xlsx_link);
            hideLoader();
            return false;
          }
          else if(download_file_format=="text") {
            $(location).attr('href', d_response.txt_link);
            hideLoader();
            return false;
          }
          else if(download_file_format=="ods") {
            $(location).attr('href', d_response.ods_link);
            hideLoader();
            return false;
          }

      } else {
          hideLoader();
      }

  });
}

function downloadFile(filePath){
  var link = document.createElement('a');
  link.href = filePath;
  link.download = filePath.substr(filePath.lastIndexOf('/') + 1);
  link.click();
}


/* DownloadFileOptionList - Excel,CSV,ODS,Text  */
function rejectedFiles(event) {
  var event_id=$(event).attr("data-id");
  event_id="download_files_"+event_id;
  document.getElementById(event_id).classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}
$(function () {
  $('.grid-table-rpt').hide();
  initialize();
  pageControls();
});