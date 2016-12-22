var domainList;
var searchList = [];

//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterCountry = $('#search-country-name');
var FilterDomain = $('#search-domain-name');

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

function initialize() {
  function success(status, data) {
    domainList = data.domains;
    console.log(data)
    totalRecord = domainList.length;
    processPaging();
  }
  function failure(status, data) {
  }
  mirror.getDomainReport(success, failure);
}

function processSearch()
{
  c_name = FilterCountry.val().toLowerCase();
  d_name = FilterDomain.val().toLowerCase();
  usr_status = $('.search-status-li.active').attr('value');

  if(d_name.length > 0 || c_name.length > 0){
    for (var entity in domainList) {
      dName = domainList[entity].domain_name;
      cnames = domainList[entity].c_names;
      dStatus = domainList[entity].is_active;
      var flg = false;
      if (c_name.length == 0)  {
          flg = true;
      }
      else {
        for (var c in cnames) {
          if (~cnames[c].toLowerCase().indexOf(c_name)){
              flg = true;
              continue;
          }
        }
      }
      if ((~dName.toLowerCase().indexOf(d_name)) && flg == true) {
        if ((usr_status == 'all') || (Boolean(parseInt(usr_status)) == dStatus)){
            searchList.push(domainList[entity]);
        }
      }
    }
  }
  console.log("len:"+searchList.length)
  console.log(searchList)
  processPaging();
}

function loadDomainList(domainList) {
  var sno = 0;
  var title;
  var j =1;
  $('.tbody-domain-list').find('tr').remove();
  $.each(domainList, function(k, v) {
      var cloneRow = $('#templates .table-domain-report .table-row').clone();
      $('.sno', cloneRow).text(j);

      var c_n = v.c_names.join(', ');

      $('.c_names', cloneRow).text(c_n);
      $('.domain-name', cloneRow).text(v.domain_name);

      if (v.is_active == true){
          $('.status', cloneRow).text("Active")
      }
      else{
          $('.status', cloneRow).text("Inactive")
      }

      $('.status').hover(function(){
        showTitle(this);
      });

      $('.tbody-domain-list').append(cloneRow);
      j = j + 1;

  });

}

//Status Title
function showTitle(e){
  if(e.className == "fa c-pointer status fa-times text-danger"){
    e.title = 'Active';
  }
  else if(e.className == "fa c-pointer status fa-check text-success")
  {
    e.title = 'Inactive';
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

    var currentClass = $(event.target).find('i').attr('class');
    Search_status.removeClass();
    if(currentClass != undefined){
      Search_status.addClass(currentClass);
      Search_status.text('');
    }else{
      Search_status.addClass('fa');
      Search_status.text('All');
    }
    processSearch();
  });

  FilterBox.keyup(function() {
      searchList = [];
      processSearch();
  });

  Search_status.change(function() {
      processSearch();
  });

  $('input').on('keypress', function (e) {
    /*var regex = new RegExp("^[a-zA-Z0-9]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)) {
       event.preventDefault();
       return false;
    }*/
    var k = e.which;
      var ok = k >= 65 && k <= 90 || // A-Z
          k >= 97 && k <= 122; // a-z
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
  totalRecord = domainList.length;
  ReportData = pageData(on_current_page);
  if (totalRecord == 0) {
    $('.table-domain-list').empty();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    $('.table-domain-list').append(clone4);
    PaginationView.hide();
    hideLoader();
  } else {
    if(sno==0){
      createPageView(totalRecord);
    }
    PaginationView.show();
    //ReportView.show();
    loadDomainList(ReportData);
  }
}

function pageData(on_current_page){
  data = [];
  recordData = [];
  _page_limit = parseInt(ItemsPerPage.val());
  recordLength = (parseInt(on_current_page) * _page_limit);
  var showFrom = sno + 1;
  var is_null = true;

  if(searchList.length > 0)
  {
    recordData = searchList;
  }
  else
  {
    recordData = domainList;
  }
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
$(function () {
  renderControls();
  loadItemsPerPage();
});