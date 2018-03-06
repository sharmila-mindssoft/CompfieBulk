var countriesList;
var domains_list=[];
var SystemRejected="COMPFIE";

var CountryVal = $('#countryval');
var Country = $('#country');
var Domain = $('#domain');
var DomainVal = $('#domainval');
var ACCountry = $('#ac-country');
var ACDomain = $('#ac-domain');

var Show_btn = $('#show');
var Export_csv = $('.export-csv');

var ReportView = $('.grid-table-rpt');
var PasswordSubmitButton = $('#password-submit');
var CurrentPassword = $('#current-password');
var RemoveStatutoryCsvId;



rsm_page = new AssignStatutoryBulkReport();

function pageControls()
{
  //load group form list in autocomplete text box
  CountryVal.keyup(function (e) {
    /*resetfilter('domains');*/
    var textval = $(this).val();
    var ctry_grps=[];
      for(var i=0;i<countriesList.length;i++)
      {
        if(countriesList[i].is_active==true)
        {
          var occur = -1
          for(var j=0;j<ctry_grps.length;j++){
            if(ctry_grps[j].country_id == countriesList[i].country_id){
              occur = 1;
              break;
            }
          }
          if(occur < 0){
            ctry_grps.push({
              "country_id": countriesList[i].country_id,
              "country_name": countriesList[i].country_name,
              "is_active": true
            });
          }

        }
      }
      commonAutoComplete(
          e, ACCountry, Country, textval,
          ctry_grps, "country_name", "country_id", function (val) {
            onAutoCompleteSuccess(CountryVal, Country, val);
      });
  });


  //load legalentity form list in autocomplete text box
  DomainVal.keyup(function (e) {
    var textval = $(this).val();
    var d_list = [];
    var country_id = $('#country').val();
    if($('#country').val() > 0)
    {
      var condition_fields = [];
      var condition_values = [];
      if($('#country').val() != ''){
        condition_fields.push("country_id");
        condition_values.push(Country.val());
      }
      for(var i =0; i < countriesList.length; i++)
      {

        if((countriesList[i].country_id == country_id))
        {
          for(var j = 0; j < domainsList.length; j++)
          {
            if ($.inArray(countriesList[i].country_id, domainsList[j].country_ids) >= 0)
            {
              d_list.push({
                "domain_id": domainsList[j].domain_id,
                "domain_name": domainsList[j].domain_name,
                "is_active": true
              });
            }
          }
        }
      }
        commonAutoComplete(
            e, ACDomain, Domain, textval,
            d_list, "domain_name", "domain_id", function (val) {
                onAutoCompleteSuccess(DomainVal, Domain, val);
            });
    }

  });

  Show_btn.click(function() {
    is_valid = rsm_page.validateMandatory();
    if (is_valid == true)
    {
        $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
        .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
            $(this).removeClass();
        });

        processSubmit();
     }
});
}
function resetfilter(evt)
{

  if(evt == 'domains')
  {
    //$('#domainid').val('');
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
      /*resetfilter('domains');*/
    }
    else if(current_id == 'domainid'){
    }
}
// get statutory mapping report data from api
function processSubmit() {
    var CountryID = parseInt(Country.val());
    var DomainID = parseInt(Domain.val());

        displayLoader();
        filterdata = {
            "c_id":CountryID,
            "d_id":DomainID,
        };
        function onSuccess(data) {

            $('.details').show();

            $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                $(this).removeClass();
                $(this).show();
            });
            console.log(data.rejected_data);


            RejectedStatutoryMappingData = data.rejected_data;
            if (RejectedStatutoryMappingData.length == 0) {
                $('.tbody-compliance').empty();
                var tableRow4 = $('#nocompliance-templates .table-nocompliances-list .table-row');
                var clone4 = tableRow4.clone();
                $('.tbl_norecords', clone4).text('No Records Found');
                $('.tbody-compliance').append(clone4);
                ReportView.show();
                hideLoader();
            } else {
                hideLoader();
                ReportView.show();
                loadCountwiseResult(RejectedStatutoryMappingData);
            }

        }

        function onFailure(error) {
            displayMessage(error);
            hideLoader();
        }

        bu.getRejectedStatutoryMappingBulkUploadData(filterdata, function(error, response) {
          console.log("error");
          console.log(error);
            if (error == null) {
                onSuccess(response);
            } else {

                onFailure(error);
            }
        });
        //temp_act = act;
    //}
}

//display statutory mapping details accoring to count
function loadCountwiseResult(filterList) {
    SNO=0;
    var CsvId;
    var CsvName;
    var TotalNoOfTasks;
    var RejectedOn;
    var ReasonForRejection;
    var StatutoryAction;
    var RemoveHrefTag;
    var RejectedBy;
    var DeclinedCount;
    var FileDownloadCount;
    var DownloadRejectedFiles;
    var deleteStatus;
    var ReasonForRejection;
    $('.tbody-compliance').empty();

    for (var entity in filterList) {

        deleteStatus='';
        SNO = parseInt(SNO) + 1;

        CsvId = filterList[entity].csv_id;
        CsvName = filterList[entity].csv_name_text;
        TotalNoOfTasks = filterList[entity].total_records;
        RejectedOn = filterList[entity].rejected_on;


        IsFullyRejected = filterList[entity].is_fully_rejected;
        RejectedReason = filterList[entity].rejected_reason;


        StatutoryAction = filterList[entity].statutory_action;
        FileDownloadCount = filterList[entity].file_download_count;

        if(parseInt(IsFullyRejected)==1){
            RemoveHrefTag='';
            ReasonForRejection=RejectedReason;
            $(allUserInfo).each(function(key,value){
              if(parseInt(filterList[entity].rejected_by)==value["user_id"])
              {
                  EmpCode = value["employee_code"];
                  EmpName = value["employee_name"];
                  RejectedBy=EmpCode+" - "+ EmpName.toUpperCase();
              }
            });
        }
        else if(parseInt(StatutoryAction)==3)
        {

           RejectedBy=SystemRejected;
           DeclinedCount = filterList[entity].declined_count;
           ReasonForRejection='';
        }

        if(parseInt(FileDownloadCount)<1)
        {
          deleteStatus='style="display:none;"';
        }
        console.log(parseInt(FileDownloadCount));
        console.log(parseInt(FileDownloadCount)<1);
        console.log(deleteStatus);


        RemoveHrefTag='<a id="delete_action_'+CsvId+'" '+deleteStatus+' data-csv-id="'+CsvId+'" onclick="confirm_alert(this)" title="'+CsvName+' - Click here to remove">';
        RemoveHrefTag+=' <i class="fa fa-times text-danger c-pointer"></i>';
        RemoveHrefTag+='</a>';


        var tableRow1 = $('#act-templates .table-act-list .table-row-act-list');
        var clone1 = tableRow1.clone();

        $('.tbl_sno', clone1).text(SNO);
        $('.tbl_upload_filename', clone1).text(CsvName);
        $(".tbl_rejected_on", clone1).text(RejectedOn);
        $('.tbl_rejected_by', clone1).text(RejectedBy);
        $('.tbl_no_of_tasks', clone1).text(TotalNoOfTasks);
        $('.tbl_declined_count', clone1).text(DeclinedCount);
        $('.tbl_reason_for_rejection', clone1).text(ReasonForRejection);

        /***** Rejected File Downloads ********/
        if(parseInt(FileDownloadCount)<2)
        {
          DownloadRejectedFiles='<i id="download_icon_'+SNO+'" data-id="'+SNO+'" class="fa fa-download text-primary c-pointer dropbtn" onclick="rejectedFiles(this)"></i>';
          DownloadRejectedFiles+='<div id="download_files_'+SNO+'" class="dropdown-content">';
          DownloadRejectedFiles+='<a class="export-excel" onclick="downloadclick('+SNO+')" href="javascript:void(0);">Download Excel</a>';
          DownloadRejectedFiles+='<a class="export-csv" onclick="downloadclick('+SNO+')" href="javascript:void(0);">Download CSV</a>';
          DownloadRejectedFiles+='<a class="export-ods" onclick="downloadclick('+SNO+')" href="javascript:void(0);">Download ODS</a>';
          DownloadRejectedFiles+='<a class="export-text" onclick="downloadclick('+SNO+')" href="javascript:void(0);">Download Text</a>';
          DownloadRejectedFiles+='</div>';
          $('.tbl_rejected_file', clone1).html(DownloadRejectedFiles);
        }

        /*$('.tbl_rejected_file', clone1).text('Link');*/

        /*<a href="/files/knowledge/files/rejected/Statutory_Mapping_Rejected.xlsx">Download Excel</a>
        <a href="/files/knowledge/files/rejected/Statutory_Mapping_Rejected.csv">Download CSV</a>
        <a href="/files/knowledge/files/rejected/Statutory_Mapping_Rejected.ods">Download ODS</a>
        <a href="/files/knowledge/files/rejected/Statutory_Mapping_Rejected.txt">Download Text</a>*/





        $('.tbl_remove', clone1).html(RemoveHrefTag);

        $('#datatable-responsive .tbody-compliance').append(clone1);
    }
    hideLoader();
}


function AssignStatutoryBulkReport() {}
// Fields Manadory validation
AssignStatutoryBulkReport.prototype.validateMandatory = function()
{
    is_valid = true;

    if (Country.val().trim().length == 0)
    {
        displayMessage(message.country_required);
        is_valid = false;
    }
    else if (Domain.val().trim().length == 0)
    {
        displayMessage(message.domain_required);
        is_valid = false;
    }
    return is_valid;
};


//load all the filters
function initialize() {
   function onSuccess(data) {
        countriesList = data.countries;
        domainsList = data.domains;
        allUserInfo = data.user_details;
        userDetails = data.user_details[0];
        Domain_ids = userDetails.country_wise_domain;
        EmpCode = userDetails.employee_code;
        EmpName = userDetails.employee_name;
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
  var password = CurrentPassword.val().trim();
  if (password.length == 0) {
    displayMessage(message.password_required);
    CurrentPassword.focus();
    return false;
  } else if(validateMaxLength('password', password, "Password") == false) {
    return false;
  }
  displayLoader();
  mirror.verifyPassword(password, function(error, response) {
    if (error == null) {
      hideLoader();
      isAuthenticate = true;
      Custombox.close();
      displaySuccessMessage(message.password_authentication_success);
    } else {
      hideLoader();
      if (error == 'InvalidPassword') {
        displayMessage(message.invalid_password);
      }
    }
  });
}


PasswordSubmitButton.click(function() {
  validateAuthentication();
});

function confirm_alert(event) {
  var CountryId=Country.val();
  var DomainId=Domain.val();

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
          target: '#authentication-modal-box',
          effect: 'contentscale',
          complete:   function() {
             CurrentPassword.focus();
             isAuthenticate = false;
             Country.val(CountryId);
             Domain.val(DomainId);
          },
          close:   function() {
            Country.val(CountryId);
            Domain.val(DomainId);
             if(isAuthenticate){
                RemoveStatutoryCsvId=$(event).attr("data-csv-id");
                RemoveStatutoryCsvData(RemoveStatutoryCsvId, CountryId, DomainId);
             }
          }
        });
      }
    })
}

function RemoveStatutoryCsvData(RemoveStatutoryCsvId, CountryId, DomainId) {
  displayLoader();

    function onSuccess(data)
    {

      $('.details').show();
      Country.val(CountryId);
      Domain.val(DomainId);

      $('.details').show();
      $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
      .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
      $(this).removeClass();
      $(this).show();
      });

      RejectedStatutoryMappingData = data.rejected_data;
      if (RejectedStatutoryMappingData.length == 0)
      {
        $('.tbody-compliance').empty();
        var tableRow4 = $('#nocompliance-templates .table-nocompliances-list .table-row');
        var clone4 = tableRow4.clone();
        $('.tbl_norecords', clone4).text('No Records Found');
        $('.tbody-compliance').append(clone4);
        ReportView.show();
        hideLoader();
      }
      else
      {
        hideLoader();
        ReportView.show();
        loadCountwiseResult(RejectedStatutoryMappingData);
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
            "csv_id":parseInt(RemoveStatutoryCsvId),
            "c_id":parseInt(CountryId)
        };

   bu.deleteRejectedStatutoryMappingByCsvID(filterdata, function(error, response) {
            if (error == null) {
                onSuccess(response)
            } else {

                onFailure(error);
            }
        });
   hideLoader();
}

function downloadclick(csv_id)
{
    displayLoader();
    function onSuccess(data)
    {
      var updatedCount;
      var dataCSVid;
      var downloadCount;
      var eventID="download_files_";
      //delete_action_
      updatedCount = data.updated_count;

      dataCSVid=updatedCount[0].csv_id;
      downloadCount=updatedCount[0].download_count;
      if(parseInt(downloadCount)==1)
      {
        eventID=eventID+dataCSVid;
        document.getElementById(eventID).classList.toggle("show");
        $("#delete_action_"+dataCSVid).attr("style","display:block");

      }
      else if(parseInt(downloadCount)>=2)
      {
        eventID=eventID+dataCSVid;
        document.getElementById(eventID).classList.toggle("show");
        $("#delete_action_"+dataCSVid).attr("style","display:block");
        $("#download_files_"+dataCSVid).remove();
        $("#download_icon_"+dataCSVid).remove();
      }
      displaySuccessMessage(message.download_files);
      hideLoader();
    }
    function onFailure(error)
    {
      displayMessage(error);
      hideLoader();
    }
  //csv_id
  filterdata = {
            "csv_id":parseInt(csv_id)
        };
  bu.setDownloadClickCount(filterdata, function(error, response) {
      if (error == null) {
          onSuccess(response)
      } else {

          onFailure(error);
      }
  });

  hideLoader();
  return false;

}
/******** Download Link Options *********

  $('[data-toggle=confirmation]').confirmation();
  $('[data-toggle=confirmation-singleton]').confirmation({ singleton: true });
  $('[data-toggle=confirmation-popout]').confirmation({ popout: true });

  $('[data-toggle=confirmation-custom]').confirmation({
    popout: true,
    buttons: [
      {
        label: 'Excel',
        class: 'btn btn-xs btn-primary m-r-5',
        icon: 'fa fa-file-excel-o text-white',
        onClick: function(){
          downloadFile("/files/knowledge/files/rejected/Statutory_Mapping_Rejected.xlsx");
         }
      },
      {
        label: 'CSV',
        class: 'btn btn-xs btn-primary m-r-5',
        icon: 'fa fa-file-excel-o  text-white',
        onClick: function(){
          downloadFile("/files/knowledge/files/rejected/Statutory_Mapping_Rejected.csv");
         }
      },
      {
        label: 'ODS',
        class: 'btn btn-xs btn-primary m-r-5',
        icon: 'fa fa-file-excel-o text-white',
        onClick: function(){
          downloadFile("/files/knowledge/files/rejected/Statutory_Mapping_Rejected.ods");
         }
      },
      {
        label: 'Text',
        class: 'btn btn-xs btn-primary',
        icon: 'fa fa-file-text-o text-white',
        onClick: function(){
          downloadFile("/files/knowledge/files/rejected/Statutory_Mapping_Rejected.txt");
         }
      }
    ]
  });*/

function downloadFile(filePath){
  var link = document.createElement('a');
  link.href = filePath;
  link.download = filePath.substr(filePath.lastIndexOf('/') + 1);
  link.click();
}


/* DownloadFileOptionList - Excel,CSV,ODS,Text  */
function rejectedFiles(event) {
  var eventID=$(event).attr("data-id");
  eventID="download_files_"+eventID;

  document.getElementById(eventID).classList.toggle("show");

  /*$(event).toggle("show");*/
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
  /*tempDatasetup();*/
});

/*function tempDatasetup()
{
  $('#countryval').val("India");
  $('#domainval').val("Industrial Law");
  $('#country').val(1);
  $('#domain').val(3);
  Show_btn.click();
}
*/