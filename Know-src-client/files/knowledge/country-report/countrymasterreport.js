var countriesList;
var searchList = []


//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterCountry = $('#search-country-name');

//search status controls
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;
var ReportData;
var searchStatus = false;

var Key = {
  LEFT:   37,
  UP:     38,
  RIGHT:  39,
  DOWN:   40
};

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

function initialize() {
  function success(status, data) {
    countriesList = data.countries;
    totalRecord = countriesList.length;
    processPaging();
    hideLoader();
  }
  function failure(status, data) {
    hideLoader();
  }
  displayLoader();
  mirror.getCountryReport(success, failure);
}

function processSearch()
{
  searchList = [];
  usr_status = $('.search-status-li.active').attr('value');
  for(var i in countriesList){
    data = countriesList[i];
    data_is_active = data.is_active;

  if ((usr_status == 'all' || Boolean(parseInt(usr_status)) == data.is_active)){
      searchList.push(data);
    }
  }
  totalRecord = searchList.length;
  processPaging();
}

function loadCountriesList(countriesList) {
  var title;
  $('.tbody-country-list').find('tr').remove();
  for (var i in countriesList) {
    var countries = countriesList[i];
    var isActive = countries.is_active;

    var tableRow = $('#templates .table-country-report .table-row');
    var clone = tableRow.clone();
    sno = sno + 1;
    $('.sno', clone).text(sno);
    $('.country-name', clone).text(countries.country_name);
    if (isActive == true){
      $('.status', clone).text("Active")
    }
    else{
      $('.status', clone).text("Inactive")
    }

    $('.tbody-country-list').append(clone);
  }
}

//render controls
function renderControls(){
  initialize();

  ItemsPerPage.on('change', function (e) {
    perPage = parseInt($(this).val());
      sno = 0;
      on_current_page = 1;
      createPageView(totalRecord);
      processPaging();
  });

  //status of the list
  Search_status_ul.click(function (event) {
    Search_status_li.each(function (index, el) {
      $(el).removeClass('active');
    });
    $(event.target).parent().addClass('active');

    var currentClass = $(event.target).html();
    Search_status.html(currentClass);

    /*Search_status.removeClass();
    if(currentClass != undefined){
      Search_status.addClass(currentClass);
      Search_status.text('');
    }else{
      Search_status.addClass('fa');
      Search_status.text('All');
    }*/
    searchStatus = true;
    processSearch();
  });

  FilterBox.keyup(function() {
      searchList = [];
      processSearch();
  });

  Search_status.change(function() {
      searchList = [];
      processSearch();
  });

  $('input').on('keypress', function (e) {
    /*var regex = new RegExp("^[a-zA-Z]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
       event.preventDefault();
       return false;
    }*/
    var k = e.which || e.keyCode;
      var ok = k >= 65 && k <= 90 || // A-Z
          k >= 97 && k <= 122 || k == 46 || k ==8 || k == 9 || k == 32 || k == Key.LEFT ||
                k == Key.RIGHT; // a-z
          //k >= 48 && k <= 57; // 0-9

      if (!ok){
          e.preventDefault();
      }
  });
}

//pagination - functions
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
                processPaging();
            }
        }
    });
};

function processPaging(){
  _page_limit = parseInt(ItemsPerPage.val());
  if (on_current_page == 1) {
    sno = 0
  }
  else {
    sno = (on_current_page - 1) *  _page_limit;
  }
  sno  = sno;
  ReportData = pageData(on_current_page);
  if (totalRecord == 0) {
    $('.tbody-country-list').find('tr').remove();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();processSearch
    $('.no_records', clone4).text('No Records Found');
    $('.tbody-country-list').append(clone4);
    PaginationView.hide();
    hideLoader();
  } else {
    if(sno==0){
      createPageView(totalRecord);
    }
    PaginationView.show();
    //ReportView.show();
    loadCountriesList(ReportData);
  }
}

function pageData(on_current_page){
  data = [];
  recordData = [];
  _page_limit = parseInt(ItemsPerPage.val());
  recordLength = (parseInt(on_current_page) * _page_limit);
  var showFrom = sno + 1;
  var is_null = true;
  if(searchStatus == true)
  {
    searchStatus = false;
    recordData = searchList;
  }
  else
  {
    recordData = countriesList;
  }
  totalRecord = recordData.length;
  for(i=sno;i<recordData.length;i++)
  {
    is_null = false;
    data.push(recordData[i]);
    if(i == (recordLength-1))
    {
      break;
    }
  }
  if (is_null == true) {
    hidePagePan();
  }
  else {
    if(recordLength < totalRecord)
      showPagePan(showFrom, recordLength, totalRecord);
    else
      showPagePan(showFrom, totalRecord, totalRecord);
  }
  return data;
}

/*$('#search-country-name').keyup(function () {
  var count = 0;
  var value = this.value.toLowerCase();
  $('table').find('tr:not(:first):not(:last)').each(function (index) {
    if (index === 0)
      return;
    var id = $(this).find('.country-name').text().toLowerCase();
    $(this).toggle(id.indexOf(value) !== -1);
  });
  count = $('tr:visible').length - 3;
  $('#total-records').html('Total : ' + count + ' records');
});*/

$(function () {
  renderControls();
  loadItemsPerPage();
});
$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});