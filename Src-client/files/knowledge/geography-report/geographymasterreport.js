var countriesList;
var geographiesList;
var searchList = []

//filter controls initialized
var FilterBox = $('.filter-text-box');
var FilterGeography = $('#search-geography-name');

// auto complete - country
var country_val = $('#country');
var country_ac = $("#countryval");
var AcCountry = $('#ac-country');

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


//get geography master data from api
function getGeography() {
  function onSuccess(data) {
    console.log(data)
    geographiesList = data.geography_report;
    countriesList = data.countries;
  }
  function onFailure(error) {
    displayMessage(error);
  }
  mirror.getGeographyReport(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}

function processSearch()
{
  g_name = FilterGeography.val().toLowerCase();

  usr_status = $('.search-status-li.active').attr('value');


  var cId = '';
  if ($('#country').val() != ''){

    cId = $('#country').val();
    for(var i in geographiesList){
      data = geographiesList[i];
      if(cId == data.country_id)
      {
        data_g_name = data.geography_mapping.toLowerCase();
        data_is_active = data.is_active;

        if (
        (~data_g_name.indexOf(g_name)))
        {
          if ((usr_status == 'all' || Boolean(parseInt(usr_status)) == data.is_active)){
            searchList.push(data);
          }
        }
      }
    }
  }
  processPaging();
  //loadGeographyList(searchList);
}

//display geography master details in view page
function loadGeographyList(geographyList) {
  console.log("geographyList:"+geographyList)
  var sno = 0;
  var geography = '';
  var isActive = 0;
  var title;
  $('.tbody-geography-report-list').find('tr').remove();
  for (var list in geographyList) {
    geography = geographyList[list].geography_mapping;
    isActive = geographyList[list].is_active;
    //var geographyimage = geography.replace(/>>/gi, ' <img src=\'/common/images/right_arrow.png\'/> ');
    if (isActive == 1) {
      title = 'Active';
    } else {
      title = 'Inacive';
    }
    var tableRow = $('#templates .table-geography-report .table-row');
    var clone = tableRow.clone();
    sno = sno + 1;
    $('.sno', clone).text(sno);
    $('.geography-name', clone).html(geography);
    if (isActive == true){
      $('.status', clone).removeClass('fa-times text-danger');
      $('.status', clone).addClass('fa-check text-success');
    }
    else{
      $('.status', clone).removeClass('fa-check text-success');
      $('.status', clone).addClass('fa-times text-danger');
    }

    $('.status').hover(function(){
      showTitle(this);
    });
    $('.tbody-geography-report-list').append(clone);
  }
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
  getGeography();

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
      processSearch();
  });

  Search_status.change(function() {
      processSearch();
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
  console.log("sno:"+sno)
  var geographyList = geographiesList;

  totalRecord = geographyList.length;
  ReportData = pageData(on_current_page);
  if (totalRecord == 0) {
    $('.table-geography-report').empty();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    $('.table-geography-report').append(clone4);
    PaginationView.hide();
    hideLoader();
  } else {
    if(sno==0){
      createPageView(totalRecord);
    }
    PaginationView.show();
    //ReportView.show();
    loadGeographyList(ReportData);
  }
}

function pageData(on_current_page){
  data = [];
  _page_limit = parseInt(ItemsPerPage.val());
  recordLength = (parseInt(on_current_page) * _page_limit);
  var showFrom = sno + 1;
  var is_null = true;

  var cId = '';
  if ($('#country').val() != '')
    cId = $('#country').val();
  var geographyList = geographiesList;

  if(searchList.length > 0)
  {
    recordData = searchList;
  }
  else
  {
    recordData = geographyList;
  }

  for(i=sno;i<recordData.length;i++)
  {
    is_null = false;
    if(recordData[i].country_id == cId){
      data.push(recordData[i]);
    }
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
  console.log("data:"+data)
  return data;
}

//Autocomplete Script Starts
//retrive country autocomplete value
//callback for autocomplete success
function onAutoCompleteSuccess(value_element, id_element, val) {
  value_element.val(val[1]);
  id_element.val(val[0]);
  value_element.focus();
  var geographyList = geographiesList;
  $('#search-geography-name').val('');
  totalRecord = geographyList.length;
  processPaging();
}

//load country list in autocomplete text box
$('#countryval').keyup(function (e) {
  var condition_fields = ["is_active"];
  var condition_values = [true];
  var text_val = $(this).val();
  commonAutoComplete(
    e, AcCountry, country_val, text_val,
    countriesList, "country_name", "country_id", function (val) {
        onAutoCompleteSuccess(country_ac, country_val, val);
    }, condition_fields, condition_values);
});

//Autocomplete Script ends
//filter process
/*$('#search-geography-name').keyup(function () {
  var filterkey = $('#search-geography-name').val().toLowerCase();
  var filteredList = [];
  var cId = '';
  if ($('#country').val() != '')
    cId = $('#country').val();
  var geographyList = geographiesList[cId];
  for (var entity in geographyList) {
    geogtaphyname = geographyList[entity].geography;
    if (~geogtaphyname.toLowerCase().indexOf(filterkey)) {
      filteredList.push(geographyList[entity]);
    }
  }
  loadGeographyList(filteredList);
});*/

//initialization
$(function () {
  renderControls();
  loadItemsPerPage();
  $('#countryval').focus();
});