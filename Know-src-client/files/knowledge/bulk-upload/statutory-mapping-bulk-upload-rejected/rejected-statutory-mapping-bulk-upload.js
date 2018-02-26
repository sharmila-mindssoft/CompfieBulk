var countriesList;
var domains_list=[];
var FullyRejected="Fully Rejected";
var SystemRejected="COMPFIE";

var CountryVal = $('#countryval');
var Country = $('#country');
var Domain = $('#domain');
var DomainVal = $('#domainval');
var ACCountry = $('#ac-country');
var ACDomain = $('#ac-domain');

var Show_btn = $('#show');
var ExportButton = $('#export');
var ReportView = $('.grid-table-rpt');
var PasswordSubmitButton = $('#password-submit');
var CurrentPassword = $('#current-password');
var RemoveStatutoryCsvId;



rsm_page = new AssignStatutoryBulkReport();

function pageControls()
{
  //load group form list in autocomplete text box
  CountryVal.keyup(function (e) {
    resetfilter('domains');
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
    resetfilter('le');
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
    $('#domainid').val('');
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
      resetfilter('domains');
    }
    else if(current_id == 'domain'){
     resetfilter('domains'); 
    }
}
// get statutory mapping report data from api
function processSubmit() {
    var CountryID = parseInt(Country.val());
    var DomainID = parseInt(Domain.val());
      alert(DomainID);
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
    $('.tbody-compliance').empty();

    for (var entity in filterList) {

        
        SNO = parseInt(SNO) + 1;

        var CsvId = filterList[entity].csv_id;
        var CsvName = filterList[entity].csv_name;
        var TotalNoOfTasks = filterList[entity].total_records;
        var RejectedOn = filterList[entity].rejected_on;
        var ReasonForRejection = filterList[entity].is_fully_rejected;
        var StatutoryAction = filterList[entity].statutory_action;
        var RemoveHrefTag;
        var RejectedBy;
        var DeclinedCount;
        if(parseInt(ReasonForRejection)==1){
            
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


        var tableRow1 = $('#act-templates .table-act-list .table-row-act-list');
        var clone1 = tableRow1.clone();

        $('.tbl_sno', clone1).text(SNO);
        $('.tbl_upload_filename', clone1).text(CsvName);
        $(".tbl_rejected_on", clone1).text(RejectedOn);
        $('.tbl_rejected_by', clone1).text(RejectedBy);
        $('.tbl_no_of_tasks', clone1).text(TotalNoOfTasks);
        $('.tbl_declined_count', clone1).text(DeclinedCount);
        $('.tbl_reason_for_rejection', clone1).text(ReasonForRejection);

        $('.tbl_rejected_file', clone1).text('Link');

        RemoveHrefTag='<a data-csv-id="'+CsvId+'" onclick="confirm_alert(this)" title="'+CsvName+' - Click here to remove">';
        RemoveHrefTag+=' <i class="fa fa-times text-danger c-pointer"></i>';
        RemoveHrefTag+='</a>';

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
          target: '#custom-modal',
          effect: 'contentscale',
          complete:   function() {
             CurrentPassword.focus();
             isAuthenticate = false;
          },
          close:   function() {
            $("#singleCheckbox2").prop('checked',false)
             if(isAuthenticate){
                RemoveStatutoryCsvId=$(event).attr("data-csv-id");
                alert("RemoveStatutoryCsvId >> "+RemoveStatutoryCsvId);

                RemoveStatutoryCsvData(parseInt(RemoveStatutoryCsvId));
                /*Custombox.close();
                $(".firstTr").delay(500).hide(0);
                $(".inp_password").val("");*/
             }
          }
        });
      }else{
        $("#singleCheckbox2").prop('checked',false)
      }
    })
}

function RemoveStatutoryCsvData(RemoveStatutoryCsvId) {
  displayLoader();
  /*mirror.removeStatutoryCsvData(parseInt(countryId), isActive, function (error, response) {
    if (error == null) {
      if (isActive == 1)
        displaySuccessMessage(message.country_active);
      else
        displaySuccessMessage(message.country_deactive);
      initialize();
      hideLoader();
    } else {
      hideLoader();
      displayMessage(error);
    }
  });*/
    filterdata = {
            "d_id":parseInt(DomainID),
            "csv_id":RemoveStatutoryCsvId,
            "c_id":parseInt(CountryID)
        };

   bu.deleteRejectedStatutoryMappingByCsvID(filterdata, function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                
                onFailure(error);
            }
        });


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