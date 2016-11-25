var CountryList;
var DomainList;
var GroupList;
var BusinessGroupList;
var LegalEntityList;
var ReportData;

var on_current_page = 1;
var sno = 0;
var totalRecord;

var ACCountry = $('#ac-country');
var ACGroup = $('#ac-group');
var ACBusinessGroup = $('#ac-businessgroup');
var ACLegalEntity = $('#ac-legalentity');
var ACDomain = $('#ac-domain');

var CountryVal = $('#countryval');
var Country = $('#country');
var GroupVal = $('#groupval');
var Group = $('#group');
var BusinessGroupVal = $('#businessgroupval');
var BusinessGroup = $('#businessgroup');
var LegalEntityVal = $('#legalentityval');
var LegalEntity = $('#legalentity');
var DomainVal = $('#domainval');
var Domain = $('#domain');
var FromDate = $('#fromdate');
var ToDate = $('#todate');


var SubmitButton = $('#submit');
var ExportButton = $('#export');

var LoaderIcon = $('.loading-indicator-spin');

var lastGroup = '';
var lastBusinessGroup = '';
var lastLE = '';
var acc_count = 1;

function displayLoader() {
  LoaderIcon.show();
}
function hideLoader() {
  LoaderIcon.hide();
}


function resetValues(){
  displayMessage('');
}

function initialize(){
	resetValues();
  mirror.getClientAgreementReportFilters(function (error, data) {
      if (error == null) {
        CountryList = data.countries;
        DomainList = data.domains;
        GroupList = data.client_group_master;
        BusinessGroupList = data.business_groups;
        LegalEntityList = data.unit_legal_entity;
      }else {
        custom_alert(error);
      }
  });
}

function getValue(field_name){
   if (field_name == "country") {
        c_id = Country.val().trim();
        if (c_id == '') {
            return null;
        }
        return parseInt(c_id);
    }
    else if (field_name == "group") {
        g_id = Group.val().trim();
        if (g_id == '') {
            return null;
        }
        return parseInt(g_id);
    }
    else if (field_name == "businessgroup") {
        bg_id = BusinessGroup.val().trim();
        if (bg_id == '') {
            return null;
        }
        return parseInt(bg_id);
    }
    else if (field_name == "legalentity") {
        le_id = LegalEntity.val().trim();
        if (le_id == '') {
            return null;
        }
        return parseInt(le_id);
    }
    else if (field_name == "domain") {
        d_id = Domain.val().trim();
        if (d_id == '') {
            return null;
        }
        return parseInt(d_id);
    }
    else if (field_name == "from_date") {
        f_date = FromDate.val().trim();
        if (f_date == '') {
            return null;
        }
        return f_date;
    }

    else if (field_name == "to_date") {
        t_date = ToDate.val().trim();
        if (t_date == '') {
            return null;
        }
        return t_date;
    }
};

function validateMandatory(){
    is_valid = true;
    if (getValue("country") == null) {
      displayMessage(message.country_required);
      is_valid = false;
    }
    return is_valid;
};

$('.close').click(function () {
  $('.overlay').css('visibility', 'hidden');
  $('.overlay').css('opacity', '0');
});

function displayPopup(LE_ID, D_ID){
    mirror.getOrganizationWiseUnitCount(LE_ID, D_ID,
        function(error, response) {
            if (error != null) {
              displayMessage(error);
            }
            else {
              $('.overlay').css('visibility', 'visible');
              $('.overlay').css('opacity', '1');
              $('.popup-list').find('tr').remove();
              var unit_count_list = response.organizationwise_unit_count_list;

              $.each(unit_count_list, function (key, value) {
                 var domain_units = value.domain_used_unit + ' / ' + value.domain_total_unit;
                $('.popup-heading').text(value.domain_name);
                var tableRow = $('#templates .table-popup-list .table-row');
                var clone = tableRow.clone();
                $('.popup_organization_name', clone).text(value.organization_name);
                $('.popup_unit_count', clone).text(domain_units);
                $('.popup-list').append(clone);
              });
            }
        }
    );
}

function loadCompliances(data){
    $('.table-client-agreement-list').empty();
    var tableRow_tr = $('#templates .table-agreement-list .heading-list');
    var clonetr = tableRow_tr.clone();
    $('.table-client-agreement-list').append(clonetr);

    $.each(data, function (key, value) {

      var domain_units = value.domain_used_unit + ' / ' + value.domain_total_unit;
      var license_details = value.used_licence + ' / ' + value.total_licence;
      var file_space_details = value.used_file_space + ' / ' + value.file_space;

      if (lastGroup != value.group_name) {
        var tableRowHeading = $('#templates .table-agreement-list .group-list');
        var cloneHeading = tableRowHeading.clone();
        $('.group-name', cloneHeading).text(value.group_name);
        $('.group-admin-email', cloneHeading).text(value.group_admin_email);

        $('.table-client-agreement-list').append(cloneHeading);
        lastGroup = value.group_name;
      }

      if (lastBusinessGroup != value.business_group_name) {
        var tableRowHeading = $('#templates .table-agreement-list .business-group-list');
        var cloneHeading = tableRowHeading.clone();
        $('.business-group-name', cloneHeading).text(value.business_group_name);

        $('.table-client-agreement-list').append(cloneHeading);
        lastBusinessGroup = value.business_group_name;
      }

      if (lastLE != value.legal_entity_name) {
        var tableRow = $('#templates .table-agreement-list .tbody-agreement-list');
        var clone = tableRow.clone();
        sno = sno + 1;

        var status = 'Active';
        if(value.is_active ==  false){
          status = 'Closed';
        }
        $('.sno', clone).text(sno);
        $('.le', clone).html(value.legal_entity_name);
        $('.user-license', clone).html(license_details);
        $('.file-space', clone).html(file_space_details);
        $('.le-email', clone).html(value.legal_entity_admin_email);
        $('.le-contactno', clone).html(value.legal_entity_admin_contactno);
        $('.domain-count', clone).html(value.domain_count);
        $('.contract-from', clone).html(value.contract_from);
        $('.contract-to', clone).html(value.contract_to);
        $('.status', clone).html(status);
        $('.table-client-agreement-list').append(clone);

        $('.table-client-agreement-list').append('<tbody class="accordion-content accordion-content' + acc_count + '"></tbody>');
        $('.accordion-content' + acc_count).addClass('default');

        lastLE = value.legal_entity_name;
        acc_count++;

        var tableRowvalues_ul = $('#templates .agreement-inner-list');
        var cloneval_ul = tableRowvalues_ul.clone();
        $('.inner-domain-name', cloneval_ul).html(value.d_name);
        $('.inner-domain-units', cloneval_ul).text(domain_units);
        $('.inner-domain-units', cloneval_ul).on('click', function () {
          displayPopup(value.legal_entity_id, value.domain_id);
        });
        $('.inner-activation-date', cloneval_ul).html(value.activation_date);
        $('.accordion-content' + (acc_count-1)).append(cloneval_ul);

      }else{
        var tableRowvalues_ul = $('#templates .agreement-inner-list');
        var cloneval_ul = tableRowvalues_ul.clone();
        $('.inner-domain-name', cloneval_ul).html(value.d_name);
        $('.inner-domain-units', cloneval_ul).text(domain_units);
        $('.inner-domain-units', cloneval_ul).on('click', function () {
          displayPopup(value.legal_entity_id, value.domain_id);
        });
        $('.inner-activation-date', cloneval_ul).html(value.activation_date);
        $('.accordion-content' + (acc_count-1)).append(cloneval_ul);
      }
    });

    $('#accordion').find('.accordion-toggle').click(function () {
      $(this).next().slideToggle('fast');
      $('.accordion-content').not($(this).next()).slideUp('fast');
    });

}

function processSubmit (csv){
  if(validateMandatory()){
    displayLoader();
    _country = getValue("country");
    _domain = getValue("domain");
    _group = getValue("group");
    _businessgroup = getValue("businessgroup");
    _legalentity = getValue("legalentity");
    _from_date = getValue("from_date");
    _to_date = getValue("to_date");

    //_page_limit = parseInt($('#items_per_page').val());
    _page_limit = 10;

    if (on_current_page == 1) {
      sno = 0
    }
    else {
      sno = (on_current_page - 1) *  _page_limit;
    }

    mirror.getClientAgreementReport(_country, _group, _businessgroup,
    _legalentity, _domain, _from_date, _to_date, csv, sno, _page_limit,
        function(error, response) {
            if (error != null) {
                displayMessage(error);
            }
            else {
              if (csv) {
                var download_url = response.link;
                window.open(download_url, '_blank');
              }else{
                sno  = sno;
                ReportData = response.client_agreement_list;
                totalRecord = response.total_count;
                lastGroup = '';
                lastBusinessGroup = '';
                lastLE = '';
                if (totalRecord == 0) {
                  $('.table-client-agreement-list').empty();
                  var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
                  var clone4 = tableRow4.clone();
                  $('.no_records', clone4).text('No Records Found');
                  $('.table-client-agreement-list').append(clone4);
                  //$('#pagination').hide();
                  $('.total-records').text('');
                  hideLoader();
                } else {
                  if(sno==0){
                    //createPageView(totalRecord);
                  }
                  //$('.pagination-view').show();
                  $('.grid-table-rpt').show();
                  loadCompliances(ReportData);

                }
              }
            }
        }
    );
  }
}

//retrive  autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();

    var current_id = id_element[0].id;
    if(current_id == 'country'){
      GroupVal.val('');
      Group.val('');
      BusinessGroupVal.val('');
      BusinessGroup.val('');
      LegalEntityVal.val('');
      LegalEntity.val('');
      DomainVal.val('');
      Domain.val('');
    }else if(current_id == 'domain'){
      GroupVal.val('');
      Group.val('');
      BusinessGroupVal.val('');
      BusinessGroup.val('');
      LegalEntityVal.val('');
      LegalEntity.val('');
    }else if(current_id == 'group'){
      BusinessGroupVal.val('');
      BusinessGroup.val('');
      LegalEntityVal.val('');
      LegalEntity.val('');
    }else if(current_id == 'businessgroup'){
      LegalEntityVal.val('');
      LegalEntity.val('');
    }
}

function pageControls() {
  SubmitButton.click(function () {
    processSubmit(false);
  });

  ExportButton.click(function () {
    processSubmit(true);
  });

  //load country list in autocomplete text box
  CountryVal.keyup(function(e){
    var text_val = $(this).val();
    commonAutoComplete(
      e, ACCountry, Country, text_val,
      CountryList, "country_name", "country_id", function (val) {
        onAutoCompleteSuccess(CountryVal, Country, val);
      });
  });

  //load domain list in autocomplete text box
  DomainVal.keyup(function(e){
    var condition_fields = [];
    var condition_values = [];
    if(Country.val() != ''){
      condition_fields.push("country_ids");
      condition_values.push(Country.val());
    }
    var text_val = $(this).val();
    commonAutoComplete(
      e, ACDomain, Domain, text_val,
      DomainList, "domain_name", "domain_id", function (val) {
          onAutoCompleteSuccess(DomainVal, Domain, val);
      }, condition_fields, condition_values);
  });

  //load group list in autocomplete text box
  GroupVal.keyup(function(e){
    if(Country.val() != ''){
      var condition_fields = [];
      var condition_values = [];

      condition_fields.push("country_ids");
      condition_values.push(Country.val());
      var text_val = $(this).val();
      commonAutoComplete(
        e, ACGroup, Group, text_val,
        GroupList, "group_name", "group_id", function (val) {
            onAutoCompleteSuccess(GroupVal, Group, val);
        }, condition_fields, condition_values);
    }
  });

  //load businessgroup list in autocomplete text box
  BusinessGroupVal.keyup(function(e){
    if(Country.val() != ''){
      var condition_fields = [];
      var condition_values = [];
      if(Group.val() != ''){
        condition_fields.push("client_id");
        condition_values.push(Group.val());
      }
      var text_val = $(this).val();
      commonAutoComplete(
        e, ACBusinessGroup, BusinessGroup, text_val,
        BusinessGroupList, "business_group_name", "business_group_id", function (val) {
            onAutoCompleteSuccess(BusinessGroupVal, BusinessGroup, val);
        }, condition_fields, condition_values);
    }
  });

  //load legalentity list in autocomplete text box
  LegalEntityVal.keyup(function(e){
    if(Country.val() != ''){
      var condition_fields = [];
      var condition_values = [];
      if(Group.val() != ''){
        condition_fields.push("client_id");
        condition_values.push(Group.val());
      }
      if(BusinessGroup.val() != ''){
        condition_fields.push("business_group_id");
        condition_values.push(BusinessGroup.val());
      }
      var text_val = $(this).val();
      commonAutoComplete(
        e, ACLegalEntity, LegalEntity, text_val,
        LegalEntityList, "legal_entity_name", "legal_entity_id", function (val) {
            onAutoCompleteSuccess(LegalEntityVal, LegalEntity, val);
        }, condition_fields, condition_values);
    }
  });
}
$(document).ready(function () {
    initialize();
    pageControls();
});
