var countriesList;
var domains_list=[];
var SystemRejected="COMPFIE";

var GroupName = $('#cgroupval');
var GroupId = $('#cgroup-id');
var ACGroup = $('#ac-cgroup');


var Show_btn = $('#show');
var ReportView = $('.grid-table-rpt');
var PasswordSubmitButton = $('#password-submit');
var CurrentPassword = $('#current-password');
var RemoveUnitCsvId;
var ExistingUserId=[];
var allUserInfo='';
var DomainList='';
var CountryWiseDomain='';
var UserCategoryID=0;


var ACLegalEntity = $('#ac-legalentity');
var ACUnit = $('#ac-unit');
/*var GroupVal = $('#groupsval');
var Group = $('#cgroup-id');*/
var LegalEntityVal = $('#legalentityval');
var LegalEntity = $('#legalentityid');
var UnitVal = $('#unitval');
var Unit = $('#unitid');

var clientList;
var Domain = $('#domain');
var Domain_ids = [];

rsm_page = new AssignStatutoryBulkReport();



function pageControls()
{

 //load group form list in autocomplete text box
  GroupName.keyup(function(e) {
    var textval = $(this).val();
    commonAutoComplete(
        e, ACGroup, GroupId, textval,
        _clients, "group_name", "client_id",
        function(val) {
            onAutoCompleteSuccess(GroupName, GroupId, val);
        });

    resetfilter('clients');
  });

    //load legalentity form list in autocomplete text box
  LegalEntityVal.keyup(function (e) {
    resetfilter('le');
    var textval = $(this).val();
    var le_list = [];
    var client_id = $('#cgroup-id').val();
    /*var bgrp_id = $('#businessgroupid').val();*/
    if($('#cgroup-id').val() > 0)
    {
      var condition_fields = [];
      var condition_values = [];
      if(GroupId.val() != ''){
        condition_fields.push("client_id");
        condition_values.push(GroupId.val());
      }
      for(var i =0; i < clientList.length; i++)
      {
        if((clientList[i].client_id == client_id))
        {
          for(var j = 0; j < legelEntityList.length; j++)
          {
            if(legelEntityList[j].legal_entity_id == clientList[i].legal_entity_id)
            {
              le_list.push({
                "client_id": clientList[i].client_id,
                "business_group_id": legelEntityList[j].business_group_id,
                "legal_entity_id": legelEntityList[j].legal_entity_id,
                "legal_entity_name": legelEntityList[j].legal_entity_name
              });
            }
          }
        }
      }

      commonAutoComplete(
        e, ACLegalEntity, LegalEntity, textval,
        le_list, "legal_entity_name", "legal_entity_id", function (val) {
            onAutoCompleteSuccess(LegalEntityVal, LegalEntity, val);
            loadDomains();
        }, condition_fields, condition_values);

    }
  });
  Domain.on('change', function(e) {
     resetfilter('domains');
  });

  UnitVal.keyup(function (e) {
      var client_id = $('#cgroup-id').val();
      var le_id = LegalEntity.val();
      var domain_ids = Domain.val();
      var textval = $(this).val();
      var unit_list=[];
      var selectedDomain=[];
      var check_existing_domain=[];
      var check_existing_unit=[];

      if(domain_ids)
      {
        $.each(domain_ids, function(key, value){
          selectedDomain.push(parseInt(value));
        });
      }

      if(client_id > 0 && le_id > 0 && domain_ids.length > 0)
      {
        for(var i =0; i < assignedUnitList.length; i++)
        {

         if(assignedUnitList[i].client_id == client_id
            && assignedUnitList[i].legal_entity_id == le_id
            && $.inArray(assignedUnitList[i].d_id, selectedDomain) >= 0)
          {

            unit_code_name=assignedUnitList[i].unit_code_name;
            unit_code=unit_code_name.split("-");
            unit_code=unit_code[0];

            unit_list.push({
                "unit_id": unit_code,
                "unit_name": assignedUnitList[i].unit_code_name
              });
          }
        }
        commonAutoComplete(
          e, ACUnit, Unit, textval,
          unit_list, "unit_name", "unit_id", function (val) {
              onAutoCompleteSuccess(UnitVal, Unit, val);
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

function getDomainByCountryID(countriesList)
{
        var sText = '';
        var str='';
        $.each(countriesList, function(key, countryId)
        {
            var cId = countryId;
            var flag = true;

            $.each(DomainList, function(key1, v)
            {
                if (v.is_active == false)
                {
                    return;
                }
                if($.inArray(cId, v.country_ids) >= 0)
                {
                    var dVal = v.domain_id;
                    str += '<option value="' + dVal + '" ' + sText + '>' + v.domain_name + '</option>';
                    flag = false;
                }
            });

        });
        Domain.append(str);
        Domain.multiselect('rebuild');
}
function loadDomains() {

    /******** Load Domain Lists *********/

    var client_id = $('#cgroup-id').val();
    var legal_id = $('#legalentityid').val();
    var APIClientID;
    var APILegalEntityID;
    var countriesList=[];


    $.each(clientList, function(key, value)
    {
      APIClientID=parseInt(value["client_id"]);
      APILegalEntityID=parseInt(value["legal_entity_id"]);
      if(client_id==APIClientID && legal_id==APILegalEntityID)
      {
        countriesList.push(parseInt(value["country_id"]));

      }
    });
    getDomainByCountryID(countriesList);
}

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
    if(current_id == 'cgroup-id'){
      resetfilter('clients');
    }else if(current_id == 'domain'){
      resetfilter('domains');
    }
    else if(current_id == 'legalentityid'){
      resetfilter('le');
    }else if(current_id == 'unitid'){
      resetfilter('unit');
    }
}
function resetfilter(evt)
{

  if(evt=='clients')
  {
    LegalEntityVal.val('');
    LegalEntity.val('');

    Domain.empty();
    Domain.html();
    Domain.multiselect('rebuild');


    $('#unitval').val('');
    $('#unitid').val('');

  }
  if(evt == 'le')
  {
    Domain.empty();
    Domain.html();
    Domain.multiselect('rebuild');

    $('#unitval').val('');
    $('#unitid').val('');

  }
  if(evt == 'domains')
  {
    $('#unitval').val('');
    $('#unitid').val('');

  }

  $('.tbody-usermappingdetails-list').empty();
  $('.grid-table-rpt').hide();
  $('.details').hide();
}

function resetFields(){
  $('#group-id').val('');
  $('#legalentityid').val('');
  $('#unitid').val('');
}


function fetchFiltersData()
{
    displayLoader();
    mirror.getClientLoginTraceFilter(
        function(error, response) {

            if (error != null) {
                hideLoader();
                displayMessage(error);
            } else {
                _clientUsers = response.audit_client_users;
                _clients = response.clients;
                loadCurrentUserDetails();
                hideLoader();
            }
        }
    );
}

function onAutoCompleteSuccess(value_element, id_element, val)
{
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
}
// get statutory mapping report data from api
function processSubmit() {

    var client_id = parseInt(GroupId.val());
    var le_id = parseInt(LegalEntity.val());
    var domain_ids = Domain.val();
    var unit_id='';

    if(Unit.val())
    {
      unit_id=Unit.val();
    }

    var selectedDomain=[];
    $.each(domain_ids, function(key, value){
      selectedDomain.push(parseInt(value));
    });

    displayLoader();
    filterdata = {
           "client_id":client_id,
           "le_id":le_id,
           "domain_ids":selectedDomain,
           "asm_unit_code":unit_id
    };
    function onSuccess(data)
    {
        $('.details').show();
        $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
        .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
            $(this).removeClass();
            $(this).show();
         });

         RejectedAssignSMData = data.asm_rejected_data;

         if (RejectedAssignSMData.length == 0) {
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
                loadCountwiseResult(RejectedAssignSMData);
            }
    }

        function onFailure(error){
            displayMessage(error);
            hideLoader();
        }

        bu.getRejectedAssignSMData(filterdata, function(error, response){
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
        CsvName = filterList[entity].csv_name;
        TotalNoOfTasks = filterList[entity].total_records;
        RejectedOn = filterList[entity].rejected_on;


        IsFullyRejected = filterList[entity].is_fully_rejected;

        StatutoryAction = filterList[entity].statutory_action;
        FileDownloadCount = filterList[entity].file_download_count;
        FullyRejected=filterList[entity].rejected_reason;

        if(parseInt(IsFullyRejected)==1){
            RemoveHrefTag='';
            ReasonForRejection=FullyRejected;
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
          DownloadRejectedFiles='<i id="download_icon_'+CsvId+'" data-id="'+CsvId+'" class="fa fa-download text-primary c-pointer dropbtn" onclick="rejectedFiles(this)"></i>';
          DownloadRejectedFiles+='<div id="download_files_'+CsvId+'" class="dropdown-content">';
          DownloadRejectedFiles+='<a data-format="excel" onclick="downloadclick('+CsvId+',this)" href="javascript:void(0);">Download Excel</a>';
          DownloadRejectedFiles+='<a data-format="csv" onclick="downloadclick('+CsvId+',this)" href="javascript:void(0);">Download CSV</a>';
          DownloadRejectedFiles+='<a data-format="ods" onclick="downloadclick('+CsvId+',this)" href="javascript:void(0);">Download ODS</a>';
          DownloadRejectedFiles+='<a data-format="text" onclick="downloadclick('+CsvId+',this)" href="javascript:void(0);">Download Text</a>';
          DownloadRejectedFiles+='</div>';
          $('.tbl_rejected_file', clone1).html(DownloadRejectedFiles);
        }

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
    if (GroupName.val().trim().length == 0)
    {
        displayMessage(message.client_group_required);
        is_valid = false;
    }
    else if (LegalEntity.val().trim().length == 0)
    {
        displayMessage(message.legalentity_required);
        is_valid = false;
    }
    else if ($('#domain option:selected').text() == "")
    {
        displayMessage(message.domain_required);
        is_valid = false;
    }
    return is_valid;
};


//load all the filters
function initialize() {
    function onSuccess(data) {
        allUserInfo = data.user_details;
        userDetails = data.user_details[0];
        DomainList = data.domains;
        CountryWiseDomain = data.country_wise_domain;


        loadCurrentUserDetails();
        hideLoader();
    }
    function onFailure(error) {
        displayMessage(error);
        hideLoader();
    }
    mirror.getAdminUserList(function(error, response) {
        if (error == null)
        {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

//load all the filters
function UserGroupDetails() {
  function onSuccess(data) {
    clientList = data.usermapping_groupdetails;
    legelEntityList = data.usermapping_legal_entities;

    assignedUnitList = data.statutory_unit;

    resetAllfilter();
    resetFields();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  displayLoader();
  mirror.getUserMappingStatutoryFilters(function (error, response) {
    if (error == null) {
      onSuccess(response);
      hideLoader();
    } else {
      onFailure(error);
      hideLoader();
    }
  });
}

function loadCurrentUserDetails()
{
    //alert('load Current User Details');
    var user = mirror.getUserInfo();
    var logged_user_id=0;
    if(allUserInfo)
    {
     $.each(allUserInfo, function(key, value){
        if(user.user_id==value["user_id"]) {
            UserCategoryID=value["user_category_id"];
            logged_user_id=value["user_id"];
        }
     });
    }

    if(UserCategoryID==6)
    {

        // TE-Name  : Techno-Executive
        $('.active-techno-executive').attr('style','display:block');
        $('#techno-name').text(user.employee_code+" - "+user.employee_name.toUpperCase());
        ExistingUserId.push(logged_user_id);
    }
    else if(UserCategoryID==5 && UserCategoryID!=6 && logged_user_id>0)
    {
        // TE-Name  : Techno-Manager
        getUserMappingsList(logged_user_id);
    }

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
      /*displaySuccessMessage(message.password_authentication_success);*/
      CurrentPassword.empty();

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
  var Group_id=GroupId.val();
  CurrentPassword.val("");
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
          complete:   function() {

             CurrentPassword.focus();
             isAuthenticate = false;
          },
          close:   function() {
             if(isAuthenticate){
                RemoveUnitCsvId=$(event).attr("data-csv-id");
                RemoveStatutoryCsvData(RemoveUnitCsvId, Group_id);
             }
          }
        });
      }
    })
}

function RemoveStatutoryCsvData(RemoveUnitCsvId, Group_id)
{
    var client_id = parseInt(GroupId.val());
    var le_id = parseInt(LegalEntity.val());
    var domain_ids = Domain.val();
    var unit_id=Unit.val();

    var selectedDomain=[];
    $.each(domain_ids, function(key, value){
      selectedDomain.push(parseInt(value));
    });
    filterdata = {
         "client_id":client_id,
         "le_id":le_id,
         "domain_ids":selectedDomain,
         "asm_unit_code":unit_id,
         "csv_id":parseInt(RemoveUnitCsvId)
    };
    displayLoader();
    function onSuccess(data)
    {

      $('.details').show();

      $('.details').show();
      $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
      .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
      $(this).removeClass();
      $(this).show();
      });

      RejectedASMData = data.asm_rejected_data;
      if (RejectedASMData.length == 0)
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
        loadCountwiseResult(RejectedASMData);
      }
      displaySuccessMessage(message.record_deleted);

    }

    function onFailure(error)
    {
      displayMessage(error);
      hideLoader();
    }

   bu.deleteRejectedASMByCsvID(filterdata, function(error, response) {
            if (error == null) {
                onSuccess(response)
            } else {

                onFailure(error);
            }
        });
   hideLoader();
}

function downloadclick(csv_id, event)
{
  var download_file_format=$(event).attr("data-format");
  var client_id = parseInt(GroupId.val());
  var le_id = parseInt(LegalEntity.val());
  var domain_ids = Domain.val();
  var unit_id='';
  var selectedDomain=[];

    if(Unit.val())
    {
      unit_id=Unit.val();
    }
    $.each(domain_ids, function(key, value){
      selectedDomain.push(parseInt(value));
    });
    displayLoader();

    function onSuccess(data)
    {
      var updatedCount;
      var dataCSVid;
      var downloadCount;
      var eventID="download_files_";

      updatedCount = data.asm_updated_count;

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

  requestDownloadData = {
           "client_id":client_id,
           "le_id":le_id,
           "domain_ids":selectedDomain,
           "asm_unit_code":unit_id,
           "csv_id" :csv_id,
           "download_format" :download_file_format
    };

  /*bu.updateASMDownloadClickCount(filterdata, function(error, response) {
      if (error == null) {
          onSuccess(response)*/

          requestDownload(requestDownloadData, download_file_format);

/*      } else {

          onFailure(error);
      }
  });*/

//  hideLoader();
  return false;
}

function requestDownload(requestDownloadData, download_file_format)
{
  bu.downloadRejectedASMReportData(requestDownloadData, function(d_error, d_response)
  {
    if (d_error == null) {
          if(download_file_format=="csv")
          {
            $(location).attr('href', d_response.csv_link);
            hideLoader();
          }
          else if(download_file_format=="excel")
          {
            $(location).attr('href', d_response.xlsx_link);
            hideLoader();
          }
          else if(download_file_format=="text")
          {
            $(location).attr('href', d_response.txt_link);
            hideLoader();
          }
          else if(download_file_format=="ods")
          {
            $(location).attr('href', d_response.ods_link);
            hideLoader();
          }


      } else {

          //onFailure(d_error);
          hideLoader();
      }

  });
}

/* DownloadFileOptionList - Excel,CSV,ODS,Text  */
function rejectedFiles(event) {
  var eventID=$(event).attr("data-id");
  eventID="download_files_"+eventID;
  document.getElementById(eventID).classList.toggle("show");
}


function resetAllfilter()
{
  $('#groupsval').val('');
  LegalEntityVal.val('');
  $('#unitval').val('');
  $('.tbody-usermappingdetails-list').empty();
  $('.grid-table-rpt').hide();
  $('.details').hide();
  //$('#countryval').focus();
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
  UserGroupDetails();
  fetchFiltersData();
  pageControls();
  /*tempDatasetup();*/
});