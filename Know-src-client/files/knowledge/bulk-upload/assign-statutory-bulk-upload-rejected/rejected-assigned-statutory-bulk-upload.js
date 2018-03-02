var countriesList;
var domains_list=[];
var FullyRejected="Fully Rejected";
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

  Domain.change(function(){
    /*  $('#domain').empty();
    $('#domain').html();
    //$('#domain').append('None Selected');
    $('#domain').multiselect('rebuild');*/
    
  });

  //load group form list in autocomplete text box
  GroupName.keyup(function(e) {
    console.log("Groups");
    var textval = $(this).val();
    commonAutoComplete(
        e, ACGroup, GroupId, textval,
        _clients, "group_name", "client_id",
        function(val) {
            onAutoCompleteSuccess(GroupName, GroupId, val);
        });

    resetfilter();
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
        }, condition_fields, condition_values);
        loadDomains();
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
function loadDomains() {
    
    /******** Load Domain Lists *********/ 

    var client_id = $('#cgroup-id').val();
    var client_id = $('#legalentityid').val();

    Domain.empty();
    if (Country.val() != null)
    {
        var sCountries = Country.val().map(Number);
        var str = '';
        
        $.each(countriesList, function(key, value)
        {
            var cId = value.country_id;
        
            if ($.inArray(cId, sCountries) >= 0)
            {
                var flag = true;
        
                $.each(domainsList, function(key1, v)
                {

                    if (v.is_active == false)
                    {
                        return;
                    }
                    
                    if ($.inArray(cId, v.country_ids) >= 0)
                    {
                        var sText = '';
                        $.each(Domain_ids, function(key2, value2)
                        {
                            if (v.domain_id == value2.d_id && cId == value2.c_id)
                            {
                                sText = 'selected="selected"'
                            }
                        });

                        if (flag)
                        {
                            str += '<optgroup label="' + value.country_name + '">';
                        }

                        var dVal = cId + '-' + v.domain_id;
                        str += '<option value="' + dVal + '" ' + sText + '>' + v.domain_name + '</option>';
                        flag = false;
                    }
                });
                if (flag == false) str += '</optgroup>'
            }
        });
        $('#domain').append(str);
        $('#domain').multiselect('rebuild');
  }

}

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
    if(current_id == 'cgroup-id'){
      resetfilter('clients');
    }else if(current_id == 'businessgroupid'){
      resetfilter('bg');
    }
    else if(current_id == 'legalentityid'){
      resetfilter('le');
    }else if(current_id == 'unitid'){
      resetfilter('unit');
    }
}
function resetfilter(evt)
{

  if(evt == 'clients')
  {
    $('#legalentityval').val('');
    $('#domain').val('');
    $('#unitval').val('');
  }
  if(evt == 'le')
  {    
    $('#domain').val('');
    $('#unitval').val('');
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
            console.log(response)
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
    var GroupID = parseInt(GroupId.val());
      
        displayLoader();
        filterdata = {
            "bu_client_id":GroupID
        };
        function onSuccess(data) {

            $('.details').show();
            $('#mapping_animation').removeClass().addClass('bounceInLeft animated')
            .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                $(this).removeClass();
                $(this).show();
            });                       
            RejectedClientUnitData = data.rejected_unit_data;
            if (RejectedClientUnitData.length == 0) {
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
                loadCountwiseResult(RejectedClientUnitData);
            }

        }

        function onFailure(error) {
            displayMessage(error);
            hideLoader();
        }

        bu.getClientUnitRejectedData(filterdata, function(error, response) {
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
        CsvName = filterList[entity].csv_name;
        TotalNoOfTasks = filterList[entity].total_records;
        RejectedOn = filterList[entity].rejected_on;

        
        IsFullyRejected = filterList[entity].is_fully_rejected;

        StatutoryAction = filterList[entity].statutory_action;
        FileDownloadCount = filterList[entity].file_download_count;

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
          DownloadRejectedFiles='<i id="download_icon_'+CsvId+'" data-id="'+CsvId+'" class="fa fa-download text-primary c-pointer dropbtn" onclick="rejectedFiles(this)"></i>';
          DownloadRejectedFiles+='<div id="download_files_'+CsvId+'" class="dropdown-content">';
          DownloadRejectedFiles+='<a onclick="downloadclick('+CsvId+')" href="javascript:void(0);">Download Excel</a>';
          DownloadRejectedFiles+='<a onclick="downloadclick('+CsvId+')" href="javascript:void(0);">Download CSV</a>';
          DownloadRejectedFiles+='<a onclick="downloadclick('+CsvId+')" href="javascript:void(0);">Download ODS</a>';
          DownloadRejectedFiles+='<a onclick="downloadclick('+CsvId+')" href="javascript:void(0);">Download Text</a>';
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
        displayMessage(message.group_required);
        is_valid = false;
    }
    return is_valid;
};


//load all the filters
function initialize() {
    function onSuccess(data) {
        allUserInfo = data.user_details;
        userDetails = data.user_details[0];
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

    assignedUnitList = data.usermapping_unit;
    resetAllfilter();
    resetFields();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  displayLoader();
  mirror.getUserMappingReportFilters(function (error, response) {
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
      displaySuccessMessage(message.password_authentication_success);
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

      RejectedUnitData = data.rejected_unit_data;
      if (RejectedUnitData.length == 0)
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
        loadCountwiseResult(RejectedUnitData);
      }
      displaySuccessMessage(message.record_deleted);

    }

    function onFailure(error)
    {
      displayMessage(error);
      hideLoader();
    }

    filterdata = {
            "csv_id":parseInt(RemoveUnitCsvId),
            "bu_client_id":parseInt(Group_id)
        };

   bu.deleteRejectedUnitByCsvID(filterdata, function(error, response) {
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
      
      updatedCount = data.updated_unit_count;

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
  bu.updateDownloadClickCount(filterdata, function(error, response) {
      if (error == null) {
          onSuccess(response)
      } else {
          
          onFailure(error);
      }
  });

  hideLoader();
  return false;

}

/*function downloadFile(filePath){
  var link = document.createElement('a');
  link.href = filePath;
  link.download = filePath.substr(filePath.lastIndexOf('/') + 1);
  link.click();
}*/


/* DownloadFileOptionList - Excel,CSV,ODS,Text  */
function rejectedFiles(event) {
  var eventID=$(event).attr("data-id");
  eventID="download_files_"+eventID;
  document.getElementById(eventID).classList.toggle("show");
}


function resetAllfilter()
{
  $('#groupsval').val('');
  $('#legalentityval').val('');
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