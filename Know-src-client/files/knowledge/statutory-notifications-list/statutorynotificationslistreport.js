//List items variable declaration
var CountryList;
var DomainList;
var Level1List;
var ReportData;

//Autocomplete variable declaration
var ACCountry = $('#ac-country');
var ACLevel1 = $('#ac-statutory');
var ACDomain = $('#ac-domain');

//Input field variable declaration
var CountryVal = $('#countryval');
var Country = $('#country');
var DomainVal = $('#domainval');
var Domain = $('#domain');
var Level1Val = $('#level1val');
var Level1 = $('#level1');
var FromDate = $('#fromdate');
var ToDate = $('#todate');
var SubmitButton = $('#submit');

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;

//Other variable declaration
var ReportView = $('.grid-table-rpt');


function initialize(){
    //resetValues();
    displayLoader();
    mirror.getStatutoryNotificationsFilters(function (error, data) {
        if (error == null) {
          CountryList = data.countries;
          DomainList = data.domains;
          Level1List = data.level_one_statutories;
          hideLoader();
        }else {
          displayMessage(error);
          hideLoader();
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
    else if (field_name == "domain") {
        d_id = Domain.val().trim();
        if (d_id == '') {
            return null;
        }
        return parseInt(d_id);
    }
    else if (field_name == "level1") {
        s_id = Level1.val().trim();
        if (s_id == '') {
            return null;
        }
        return parseInt(s_id);
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
    else if (getValue("domain") == null) {
      displayMessage(message.domain_required);
      is_valid = false;
    }
    return is_valid;
};

function showPagePan(showFrom, showTo, total) {
    var showText = 'Showing ' + showFrom + ' to ' + showTo +  ' of ' + total + ' entries ';
    CompliacneCount.text(showText);
    PaginationView.show();
};

function hidePagePan() {
    CompliacneCount.text('');
    PaginationView.hide();
}

function createPageView(total_records) {
    perPage = parseInt(ItemsPerPage.val());
    Pagination.empty();
    Pagination.removeData('twbs-pagination');
    Pagination.unbind('page');

    Pagination.twbsPagination({
        totalPages: Math.ceil(total_records/perPage),
        visiblePages: visiblePageCount,
        onPageClick: function(event, page) {
            cPage = parseInt(page);
            if (parseInt(on_current_page) != cPage) {
                on_current_page = cPage;
                processSubmit();
            }
        }
    });
};

function loadCompliances(data){
    $('.table-statutory-notifications-list').empty();
    var showFrom = sno + 1;
    var is_null = true;
    var tableRow_tr = $('#templates .table-statutory-notification-list .heading-list');
    var clonetr = tableRow_tr.clone();
    $('.table-statutory-notifications-list').append(clonetr);

    $.each(data, function (key, value) {
      is_null = false;
      var tableRow = $('#templates .table-statutory-notification-list .tbody-statutory-notification-list');
      var clone = tableRow.clone();
      sno = sno + 1;
      $('.sno', clone).text(sno);
      $('.act', clone).html(value.statutory_name);
      var compl_ctrl = "<i class='zmdi zmdi-info address-title' data-toggle='tooltip' title='"+value.description+"'></i>&nbsp;&nbsp;"+value.compliance_task;
      $('.compliancetask', clone).html(compl_ctrl);
      $('.c-pointer', clone);
      $('.c-pointer').hover(function(){
        showTitle(this, value.description);
      });
      //$('.c-pointer').attr('title',value.notification_text);
      $('.date', clone).html(value.notification_date);
      $('.notification', clone).html(value.notification_text);
      $('.table-statutory-notifications-list').append(clone);
    });
    if (is_null == true) {
      hidePagePan();
    }
    else {
      showPagePan(showFrom, sno, totalRecord);
    }
    hideLoader();
}
//Status Title
function showTitle(e, notf_text){
  var titleText = notf_text;
    e.title = titleText;
    console.log(e.title)
}
function processSubmit (){
  if(validateMandatory()){
    displayLoader();
    _country = getValue("country");
    _domain = getValue("domain");
    _level1 = getValue("level1");
    _from_date = getValue("from_date");
    _to_date = getValue("to_date");
    _page_limit = parseInt(ItemsPerPage.val());

    if (on_current_page == 1) {
      sno = 0
    }
    else {
      sno = (on_current_page - 1) *  _page_limit;
    }

    mirror.getStatutoryNotificationsReportData(_country, _domain, _level1,
    _from_date, _to_date, sno, _page_limit,
        function(error, response) {
            if (error != null) {
              displayMessage(error);
            }
            else {
              $('.details').show();
              $('#compliance_animation')
                .removeClass().addClass('bounceInLeft animated')
                .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
                $(this).removeClass();
              });
              sno  = sno;
              ReportData = response.statutory_notifictions_list;
              totalRecord = response.total_count;
              console.log(totalRecord)

              $('.disp_country').text(CountryVal.val());
              $('.disp_domain').text(DomainVal.val());

              if (totalRecord == 0) {
                $('.table-statutory-notifications-list').empty();
                var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
                var clone4 = tableRow4.clone();
                $('.no_records', clone4).text('No Records Found');
                $('.table-statutory-notifications-list').append(clone4);
                PaginationView.hide();
                ReportView.show();
                hideLoader();
              } else {
                hideLoader();
                if(sno==0){
                  createPageView(totalRecord);
                }
                PaginationView.show();
                ReportView.show();
                loadCompliances(ReportData);
              }
            }
        }
    );
  }
}

//retrive  autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
  console.log("val:"+val)
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();

    var current_id = id_element[0].id;
    if(current_id == 'country'){
      DomainVal.val('');
      Domain.val('');
      Level1Val.val('');
      Level1.val('');
    }
    else if(current_id == 'domain'){
      Level1Val.val('');
      Level1.val('');
    }
}

function pageControls() {
  ItemsPerPage.on('change', function (e) {
    perPage = parseInt($(this).val());
    sno = 0;
    on_current_page = 1;
    createPageView(totalRecord);
    processSubmit();
  });

  SubmitButton.click(function () {
    on_current_page = 1;
    processSubmit();
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
  Level1Val.keyup(function(e){
    if(Country.val() != '' && Domain.val() != ''){
      var condition_fields = [];
      var condition_values = [];

      condition_fields.push("country_id", "domain_id");
      condition_values.push(Country.val(), Domain.val());

      var text_val = $(this).val();
      commonAutoComplete(
        e, ACLevel1, Level1, text_val,
        Level1List, "level_1_statutory_name", "level_1_statutory_id", function (val) {
            onAutoCompleteSuccess(Level1Val, Level1, val);
        }, condition_fields, condition_values);
    }
  });
}
$(document).ready(function () {
    initialize();
    pageControls();
    loadItemsPerPage();
});