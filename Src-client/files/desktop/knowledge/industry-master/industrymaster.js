var industriesList;
var countriesList;
var domainList;
var filteredIndList = [];
var filteredCtryList = [];
var filteredDomList = [];
var industrybool=false, countrybool=false, domainbool=false;

$('.btn-industry-add').click(function () {
  $('#industry-view').hide();
  $('#industry-add').show();
  $('#industryname').val('');
  $('#industryid').val('');
  $('.error-message').html('');
  $('#industryname').focus();
});
$('.btn-industry-cancel').click(function () {
  $('#industry-add').hide();
  $('#industry-view').show();
});
// get industry list from api
function getIndustries() {
  function onSuccess(data) {
    industriesList = data.industries;
    domainList = data.domains;
    countriesList = data.countries;
    loadIndustryList(industriesList);
  }
  function onFailure(error) {
    custom_alert(error);
  }
  mirror.getIndustryList(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}
//display industry list in view page
function loadIndustryList(industriesList) {
  var j = 1;
  $('.tbody-industry-list-view').find('tr').remove();
  $.each(industriesList, function (key, value) {
    var country_id = value.country_id;
    var country_name = value.country_name;
    var domain_id = value.domain_id;
    //alert("domain:"+domain_id);
    var domain_name = value.domain_name;
    var industryId = value.industry_id;
    var industryName = value.industry_name;
    var isActive = value.is_active;
    var passStatus = null;
    var classValue = null;
    if (isActive == true) {
      passStatus = false;
      classValue = 'active-icon';
    } else {
      passStatus = true;
      classValue = 'inactive-icon';
    }
    var tableRow = $('#templates .table-industry-master .table-row');
    var clone = tableRow.clone();
    $('.sno', clone).text(j);
    $('.country-name', clone).text(country_name);
    $('.domain-name', clone).text(domain_name);
    $('.industry-name', clone).text(industryName);
    $('.edit-icon').attr('title', 'Edit');
    $('.edit-icon', clone).on('click', function () {
      displayEdit(country_id, domain_id, industryId, industryName);
    });
    $('.status', clone).addClass(classValue);
    $('.active-icon').attr('title', 'Deactivate');
    $('.inactive-icon').attr('title', 'Activate');
    $('.status', clone).on('click', function () {
      changeStatus(industryId, passStatus);
    });
    $('.tbody-industry-list-view').append(clone);
    j = j + 1;
  });
}
// validation
function validate() {
  var checkLength = industryValidate();
  if (checkLength) {
    if ($('#countryname').val().trim().length == 0) {
      displayMessage(message.country_required);
    } else {
      displayMessage('');
      return true;
    }
    if ($('#domainname').val().trim().length == 0) {
      displayMessage(message.domainname_required);
    } else {
      displayMessage('');
      return true;
    }
    if ($('#industryname').val().trim().length == 0) {
      displayMessage(message.industryname_required);
    } else {
      displayMessage('');
      return true;
    }
  }
}
//save or update industry master on enter key press
$('#industryname').keypress(function (e) {
  if (e.which == 13) {
    if (validate()) {
      jQuery('#submit').focus().click();
    }
  }
});
// save or update industry master
$('#submit').click(function () {
  var countryId = $('#countryid').val();
  //alert(countryId);
  var countryName = $('#countryname').val().trim();
  var domainId = $('#domainid').val();
  var domainName = $('#domainname').val().trim();
  var industryId = $('#industryid').val();
  var industryName = $('#industryname').val().trim();
  if (validate()) {
    if (industryId == '') {
      function onSuccess(response) {
        getIndustries();
        $('#industry-add').hide();
        $('#industry-view').show();
      }
      function onFailure(error) {
        if (error == 'InvalidIndustryId') {
          displayMessage(message.invalid_industryid);
        } else if (error == 'IndustryNameAlreadyExists') {
          displayMessage(message.industryname_exists);
        } else {
          displayMessage(error);
        }
      }
      industryDetail = [
        parseInt(countryId),
        parseInt(domainId),
        industryName
      ];

      industryDetailDict = mirror.getSaveIndustryDict(industryDetail);
      mirror.saveIndustry(industryDetailDict, function (error, response) {
        if (error == null) {
          onSuccess(response);
        } else {
          onFailure(error);
        }
      });
    } else {
      function onSuccess(response) {
        getIndustries();
        $('#industry-add').hide();
        $('#industry-view').show();
      }
      function onFailure(error) {
        if (error == 'IndustryNameAlreadyExists') {
          displayMessage(message.industryname_exists);
        } else {
          displayMessage(error);
        }
      }
      industryDetail = [
        parseInt(countryId),
        parseInt(domainId),
        parseInt(industryId),
        industryName
      ];
      //alert(industryDetail);
      var industryDetailDict = mirror.getUpdateIndustryDict(industryDetail);

      mirror.updateIndustry(industryDetailDict, function (error, response) {
        if (error == null) {
          onSuccess(response);
        } else {
          onFailure(error);
        }
      });
    }
  }
});
// edit industry master
function displayEdit(countryId, domainId, industryId, industryName) {
  //alert("disp:"+domainId);
  $('.error-message').text('');
  $('#industry-view').hide();
  $('#industry-add').show();

  //load country name
  for(var i in countriesList)
  {
    if(countriesList[i].country_id == countryId)
        $('#countryid').val(countryId);
        $('#countryname').val(countriesList[i].country_name);
        break;
  }

  //load domain name
  //alert("length:"+domainList.length)
  var j=0;
  for(j in domainList)
  {
    if(domainList[j].domain_id == domainId) {
      $('#domainid').val(domainList[j].domain_id);
      $('#domainname').val(domainList[j].domain_name);
      break;
    }
  }

  $('#industryname').val(industryName.replace(/##/gi, '"'));
  $('#industryid').val(industryId);
}
// activate / deactivate industry master
function changeStatus(industryId, isActive) {
  var msgstatus = message.deactive_message;
  if (isActive) {
    msgstatus = message.active_message;
  }
  $('.warning-confirm').dialog({
    title: message.title_status_change,
    buttons: {
      Ok: function () {
        $(this).dialog('close');
        function onSuccess(response) {
          getIndustries();
        }
        function onFailure(error) {
          if (error == 'TransactionExists') {
            custom_alert(message.trasaction_exists);
          } else {
            custom_alert(error);
          }
        }
        mirror.changeIndustryStatus(industryId, isActive, function (error, response) {
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
//filter process - industry name
$('#search-industry-name').keyup(function () {
  if(this.value.length >= 3) {
    industrybool=true;
    filteredIndList = [];
    var filterkey = this.value.toLowerCase();
    for (var entity in industriesList) {
      industryName = industriesList[entity].industry_name;
      if (~industryName.toLowerCase().indexOf(filterkey))
        filteredIndList.push(industriesList[entity]);
    }
    if($('#search-country-name').val().length >= 3)
    {
      countrybool=true;
      if(filteredIndList.length > 0)
      {
        filteredCtryList = [];
        for(var ctry in filteredIndList)
        {
          countryName=filteredIndList[ctry].country_name;
          //alert(countryName)
          if (~countryName.toLowerCase().indexOf($('#search-country-name').val()))
            filteredCtryList.push(industriesList[ctry]);
        }
        //alert(filteredCtryList.length);
      }
    }
    if($('#search-domain-name').val().length >= 3)
    {
      domainbool = true;
      if(filteredCtryList.length > 0)
      {
        filteredDomList = [];
        for(var domain in filteredCtryList)
        {
          domainName=filteredIndList[domain].domain_name;
          if (~domainName.toLowerCase().indexOf($('#search-domain-name').val()))
            filteredDomList.push(industriesList[domain]);
        }
      }
    }

    if(domainbool == true)
    {
     loadIndustryList(filteredDomList);
    }
    else if(countrybool == true)
    {
      loadIndustryList(filteredCtryList);
    }
    else
    {
      loadIndustryList(filteredIndList);
    }

  }
});

//filter process - country name
$('#search-country-name').keyup(function () {
  if(this.value.length >= 3) {
    countrybool=true;
    var filterkey = this.value.toLowerCase();
    filteredCtryList = [];
    for (var entity in countriesList) {
      countryName = industriesList[entity].country_name;
      if (~countryName.toLowerCase().indexOf(filterkey))
        filteredCtryList.push(industriesList[entity]);
    }
    if($('#search-industry-name').val().length >= 3)
    {
      if(filteredCtryList.length > 0)
      {
        industrybool=true;
        filteredIndList = [];
        for(var inds in filteredCtryList)
        {
          industryName=filteredCtryList[inds].country_name;
          //alert(industryName)
          if (~industryName.toLowerCase().indexOf($('#search-industry-name').val()))
            filteredIndList.push(industriesList[inds]);
        }
      }
    }
    if($('#search-domain-name').val().length >= 3)
    {
      if(filteredCtryList.length > 0)
      {
        domainbool=true;
        filteredDomList = [];
        for(var domain in filteredCtryList)
        {
          domainName=filteredIndList[domain].domain_name;
          if (~domainName.toLowerCase().indexOf($('#search-domain-name').val()))
            filteredDomList.push(industriesList[domain]);
        }
      }
    }
    if(domainbool == true)
    {
     loadIndustryList(filteredDomList);
    }
    else if(countrybool == true)
    {
      loadIndustryList(filteredCtryList);
    }
    else
    {
      loadIndustryList(filteredIndList);
    }
  }
});

//filter process - domain name
$('#search-domain-name').keyup(function () {
  if (this.value.length >= 3) {
  var filterkey = this.value.toLowerCase();
    domainbool = true;
  filteredDomList = [];
  for (var entity in domainList) {
    domainName = industriesList[entity].domain_name;
    if (~domainName.toLowerCase().indexOf(filterkey))
      filteredDomList.push(industriesList[entity]);
  }

  if($('#search-industry-name').val().length >= 3)
  {
    if(filteredDomList.length > 0)
    {
      industrybool=true;
      filteredIndList = [];
      for(var inds in filteredDomList)
      {
        industryName=filteredDomList[inds].country_name;
        //alert(industryName)
        if (~industryName.toLowerCase().indexOf($('#search-industry-name').val()))
          filteredIndList.push(industriesList[inds]);
      }
    }
  }

    if($('#search-country-name').val().length >= 3)
    {
      if(filteredIndList.length > 0)
      {
        countrybool=true;
        filteredCtryList = [];
        for(var ctry in filteredIndList)
        {
          countryName=filteredIndList[ctry].country_name;
          //alert(countryName)
          if (~countryName.toLowerCase().indexOf($('#search-country-name').val()))
            filteredCtryList.push(industriesList[ctry]);
        }
      }
    }
    if(domainbool == true)
    {
     loadIndustryList(filteredDomList);
    }
    else if(countrybool == true)
    {
      loadIndustryList(filteredCtryList);
    }
    else
    {
      loadIndustryList(filteredIndList);
    }
}
});


//load country list in autocomplete text box
$('#countryname').keyup(function (e) {
  var textval = $(this).val();
  getCountryAutocomplete(e, textval, countriesList, function (val) {
    onCountrynameSuccess(val);
  });
});

//store the selected country name and id
function onCountrynameSuccess(val)
{
  $('#countryname').val(val[1]);
  $('#countryid').val(val[0]);
  $('#countryname').focus();
}

//load domain list in autocomplete text box
$('#domainname').keyup(function (e) {
  var textval = $(this).val();
  getDomainAutocomplete(e, textval, domainList, function (val) {
    onDomainnameSuccess(val);
  });
});

//store the selected country name and id
function onDomainnameSuccess(val)
{
  $('#domainname').val(val[1]);
  $('#domainid').val(val[0]);
  $('#domainname').focus();
}

//initialization
$(document).ready(function () {
  getIndustries();
  });
$('#industry_name').on('input', function (e) {
  this.value = isAlphabetic($(this));
});