var GroupList = [];
var LegaleEntityList = [];
var AllocatedServerList = [];

var ACGroup = $('#ac-group');
var ACLegalEntity = $('#ac-legalentity');
var GroupVal = $('#groupsval');
var Group = $('#group-id');
var LegalEntityVal = $('#legalentityval');
var LegalEntity = $('#legalentityid');
var SubmitButton = $('#show-button');
var ExportButton = $('#export');

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;


function initialize() {
  function onSuccess(data) {
    GroupList = data.allocate_groups;
    LegaleEntityList = data.allocate_legal_entity;
    AllocatedServerList = data.allocated_client_dbs;
    console.log(data)
    resetAllfilter();
  }
  function onFailure(error) {
    displayMessage(error);
  }
  mirror.getAllocateServerReportData(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    }
  });
}

function renderControls(){
  initialize();

  ItemsPerPage.on('change', function (e) {
    perPage = parseInt($(this).val());
      sno = 0;
      on_current_page = 1;
      createPageView(totalRecord);
      processPaging();
  });
}

$(function () {
  $('.grid-table-rpt').hide();
  renderControls();
  loadItemsPerPage();
});