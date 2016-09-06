var splist;
$('#btn-service-provider-add').click(function () {
  $('#service-provider-view').hide();
  $('#service-provider-add').show();
  $('#service-provider-id').val('');
  $('#service-provider-name').focus();
  $('input[id$=\'contract-from\'], input[id$=\'contract-to\']').datepicker('option', 'maxDate', null);
  $('input[id$=\'contract-from\'], input[id$=\'contract-to\']').datepicker('option', 'minDate', null);
  clearMessage();
  var x = document.getElementsByTagName('input');
  for (i = 0; i <= x.length - 1; i++) {
    if (x.item(i).type != 'submit') {
      x.item(i).value = '';
    }
  }
  $('#address').val('');
  $('#contract-from').datepicker({
    changeMonth: true,
    changeYear: true,
    numberOfMonths: 1,
    dateFormat: 'd-M-yy',
    monthNames: [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec'
    ],
    onClose: function (selectedDate) {
      $('#contract-to').datepicker('option', 'minDate', selectedDate);
    }
  });
  $('#contract-to').datepicker({
    changeMonth: true,
    changeYear: true,
    numberOfMonths: 1,
    dateFormat: 'd-M-yy',
    monthNames: [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec'
    ],
    mindate: 0,
    onClose: function (selectedDate) {
      $('#contract-from').datepicker('option', 'maxDate', selectedDate);
    }
  });
});
$('#btn-service-provider-cancel').click(function () {
  $('#service-provider-add').hide();
  $('#service-provider-view').show();
  $('input[id$=\'contract-from\'], input[id$=\'contract-to\']').datepicker('option', 'maxDate', null);
  $('input[id$=\'contract-from\'], input[id$=\'contract-to\']').datepicker('option', 'minDate', null);
  $('#contract-from').datepicker({
    changeMonth: true,
    changeYear: true,
    numberOfMonths: 1,
    dateFormat: 'd-M-yy',
    monthNames: [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec'
    ],
    onClose: function (selectedDate) {
      $('#contract-to').datepicker('option', 'minDate', selectedDate);
    }
  });
  $('#contract-to').datepicker({
    changeMonth: true,
    changeYear: true,
    numberOfMonths: 1,
    dateFormat: 'd-M-yy',
    monthNames: [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec'
    ],
    mindate: 0,
    onClose: function (selectedDate) {
      $('#contract-from').datepicker('option', 'maxDate', selectedDate);
    }
  });
});
function initialize() {
  function onSuccess(data) {
    $('.js-filter').val('');
    splist = data;
    loadServiceProviderList(data);
  }
  function onFailure(error) {
    custom_alert(error);
  }
  client_mirror.getServiceProviders(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
function loadServiceProviderList(serviceProviderList) {
  $('.tbody-service-provider-list').find('tr').remove();
  var sno = 0;
  var imageName, title;
  for (var i in serviceProviderList) {
    var serviceProvider = serviceProviderList[i];
    for (var j in serviceProvider) {
      var serviceProviderId = serviceProvider[j].service_provider_id;
      var serviceProviderName = serviceProvider[j].service_provider_name;
      var contactPerson = serviceProvider[j].contact_person;
      var contactNo = serviceProvider[j].contact_no;
      var isActive = serviceProvider[j].is_active;
      if (isActive == true) {
        imageName = 'icon-active.png';
        title = 'Click here to deactivate';
        statusVal = false;
      } else {
        imageName = 'icon-inactive.png';
        title = 'Click here to Activate';
        statusVal = true;
      }
      var tableRow = $('#templates .table-service-provider-list .table-row');
      var clone = tableRow.clone();
      sno = sno + 1;
      $('.sno', clone).text(sno);
      $('.service-provider-name', clone).text(serviceProviderName);
      $('.contact-person', clone).text(contactPerson);
      $('.contact-number', clone).text(contactNo.replace(/-/g, ' '));
      $('.edit', clone).html('<img src="/images/icon-edit.png" id="editid" onclick="serviceprovider_edit(' + serviceProviderId + ')"/>');
      $('.is-active', clone).html('<img src="/images/' + imageName + '" title="' + title + '" onclick="serviceprovider_active(' + serviceProviderId + ', ' + statusVal + ')"/>');
      $('.tbody-service-provider-list').append(clone);
    }
  }
}
$('#submit').click(function () {
  var checkLength = serviceProviderValidate();
  if (checkLength) {
    function parseMyDate(s) {
      return new Date(s.replace(/^(\d+)\W+(\w+)\W+/, '$2 $1 '));
    }
    var serviceProviderIdValue = $('#service-provider-id').val().trim();
    var serviceProviderNameValue = $('#service-provider-name').val().trim();
    var contactPersonValue = $('#contact-person').val().trim();
    var countryCodeValue = $('#country-code').val().trim();
    var areaCodeValue = $('#area-code').val().trim();
    var mobileNumberValue = $('#mobile-number').val().trim();
    var addressValue = $('#address').val().trim();
    var contractFromValue = $('#contract-from').val().trim();
    var contractToValue = $('#contract-to').val().trim();
    var todaydate = new Date();
    if (serviceProviderNameValue == '') {
      displayMessage(message.spname_required);
    } else if (serviceProviderNameValue.length > 50) {
      displayMessage(message.spname_max50);
    } else if (contactPersonValue == '') {
      displayMessage(message.contactpersonname_required);
    } else if (contactPersonValue.length > 50) {
      displayMessage(message.contactpersonname_max50);
    }  // else if(countryCodeValue == ''){
       //     displayMessage('Enter Contact No. Country Code');
       // }
    else if (countryCodeValue.length > 4) {
      displayMessage(message.countrycode_max4);
    } else if (areaCodeValue.length > 4) {
      displayMessage(message.areacode_max4);
    }  // else if(mobileNumberValue == ''){
       //     displayMessage('Enter Contact No.');
       // }
    else if (mobileNumberValue.length > 10) {
      displayMessage(message.contactno_max10);
    } else if (addressValue.length > 250) {
      displayMessage(message.address_max250);
    } else if (contractFromValue == '') {
      displayMessage(message.contractfrom_required);
    } else if (contractToValue == '') {
      displayMessage(message.contractto_required);
    } else if (todaydate > parseMyDate(contractToValue)) {
      displayMessage(message.contractto_maxi_today);
    } else if (serviceProviderIdValue == '') {
      function onSuccess(data) {
        $('#service-provider-add').hide();
        $('#service-provider-view').show();
        initialize();
      }
      function onFailure(error) {
        if (error == 'ServiceProviderNameAlreadyExists') {
          displayMessage(message.spname_exists);
        } else if (error == 'ContactNumberAlreadyExists') {
          displayMessage(message.contactno_exists);
        } else {
          displayMessage(error);
        }
      }
      var serviceProviderDetail;
      var contactNo = countryCodeValue + '-' + areaCodeValue + '-' + mobileNumberValue;
      serviceProviderDetail = [
        serviceProviderNameValue,
        addressValue,
        contractFromValue,
        contractToValue,
        contactPersonValue,
        contactNo
      ];
      serviceProviderDetail = client_mirror.getSaveServiceProviderDict(serviceProviderDetail);
      client_mirror.saveServiceProvider(serviceProviderDetail, function (error, response) {
        if (error == null) {
          onSuccess(response);
        } else {
          onFailure(error);
        }
      });
    } else {
      function onSuccess(data) {
        $('#service-provider-add').hide();
        $('#service-provider-view').show();
        initialize();
      }
      function onFailure(error) {
        if (error == 'ServiceProviderNameAlreadyExists') {
          displayMessage(message.spname_exists);
        } else if (error == 'ContactNumberAlreadyExists') {
          displayMessage(message.contactno_exists);
        } else {
          displayMessage(error);
        }
      }
      var serviceProviderDetail;
      var contactNo = countryCodeValue + '-' + areaCodeValue + '-' + mobileNumberValue;
      serviceProviderDetail = [
        parseInt(serviceProviderIdValue),
        serviceProviderNameValue,
        addressValue,
        contractFromValue,
        contractToValue,
        contactPersonValue,
        contactNo
      ];
      serviceProviderDetail = client_mirror.getUpdateServiceProviderDict(serviceProviderDetail);
      client_mirror.updateServiceProvider(serviceProviderDetail, function (error, response) {
        if (error == null) {
          onSuccess(response);
        } else {
          onFailure(error);
        }
      });
    }
  }
});
function serviceprovider_edit(serviceProviderId) {
  $('#service-provider-view').hide();
  $('#service-provider-add').show();
  clearMessage();
  $('input[id$=\'contract-from\'], input[id$=\'contract-to\']').datepicker('option', 'maxDate', null);
  $('input[id$=\'contract-from\'], input[id$=\'contract-to\']').datepicker('option', 'minDate', null);
  $('#service-provider-id').val(serviceProviderId);
  for (var i in splist) {
    var lists = splist[i];
    for (var j in lists) {
      if (lists[j].service_provider_id == serviceProviderId) {
        $('#service-provider-name').val(lists[j].service_provider_name);
        $('#contact-person').val(lists[j].contact_person);
        if (lists[j].address != 'None') {
          $('#address').val(lists[j].address);
        }
        $('#contract-from').val(lists[j].contract_from);
        $('#contract-to').val(lists[j].contract_to);
        var mobileno = lists[j].contact_no.split('-');
        $('#country-code').val(mobileno[0]);
        $('#area-code').val(mobileno[1]);
        $('#mobile-number').val(mobileno[2]);
      }
    }
    $('#contract-from').datepicker({
      changeMonth: true,
      changeYear: true,
      numberOfMonths: 1,
      dateFormat: 'd-M-yy',
      monthNames: [
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec'
      ],
      onClose: function (selectedDate) {
        $('#contract-to').datepicker('option', 'minDate', selectedDate);
      }
    });
    $('#contract-to').datepicker({
      changeMonth: true,
      changeYear: true,
      numberOfMonths: 1,
      dateFormat: 'd-M-yy',
      monthNames: [
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec'
      ],
      mindate: 0,
      onClose: function (selectedDate) {
        $('#contract-from').datepicker('option', 'maxDate', selectedDate);
      }
    });
  }
}
function serviceprovider_active(serviceProviderId, isActive) {
  var msgstatus = message.deactive_message;
  if (isActive) {
    msgstatus = message.active_message;
  }
  $('.warning-confirm').dialog({
    title: message.title_status_change,
    buttons: {
      Ok: function () {
        $(this).dialog('close');
        function onSuccess(data) {
          initialize();
        }
        function onFailure(error) {
          if (error == 'CannotDeactivateUserExists') {
            custom_alert(message.cannot_deactivate_sp);
          } else if (error == 'CannotChangeStatusOfContractExpiredSP') {
            custom_alert(message.cannot_change_status);
          } else {
            custom_alert(error);
          }
        }
        client_mirror.changeServiceProviderStatus(parseInt(serviceProviderId), isActive, function (error, response) {
          if (error == null) {
            onSuccess(response);
          } else {
            onFailure(error);
          }
        });
      },
      Cancel: function () {
        $(this).dialog('close');
      }
    },
    open: function () {
      $('.warning-message').html(msgstatus);
    }
  });
}
$(function () {
  initialize();
});
$(document).find('.js-filtertable').each(function () {
  $(this).filtertable().addFilter('.js-filter');
});
$('#service-provider-name').on('input', function (e) {
  this.value = isCommon_Name($(this));
});
$('#contact-person').on('input', function (e) {
  this.value = isCommon_Name($(this));
});
$('#address').on('input', function (e) {
  this.value = isCommon_Address($(this));
});
$('#mobile-number').on('input', function (e) {
  this.value = isNumbers($(this));
});
$('#area-code').on('input', function (e) {
  this.value = isNumbers($(this));
});
$('#country-code').on('input', function (e) {
  this.value = isNumbers_Countrycode($(this));
});