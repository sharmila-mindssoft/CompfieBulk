var GroupList = [];
var LegalEntityList = [];
var AllocatedServerList = [];
var SearchedList = [];

var ACGroup = $('#ac-group');
var ACLegalEntity = $('#ac-legalentity');
var GroupVal = $('#groupsval');
var Group = $('#group-id');
var LegalEntityVal = $('#legalentityval');
var LegalEntity = $('#legalentityid');

var clientId = null;
var legalentityId = null;
var showHit = false;

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;
var csv = false;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

function initialize() {
  function onSuccess(data) {
    AllocatedServerList = data.allocate_db_list;
    console.log(data)
    bindGroups();
    totalRecord = GroupList.length;
    hideLoader();
    //processPaging();
    //loadAllocateDBEnvReport(AllocatedServerList);
  }
  function onFailure(error) {
    displayMessage(error);
  }
  displayLoader();
  mirror.getAllocateServerReportData(function (error, response) {
    if (error == null) {
      onSuccess(response);
    } else {
      onFailure(error);
    	hideLoader();
    }
  });
}

function bindGroups(){
	for(var i=0;i<AllocatedServerList.length;i++){
		if(GroupList.length==0)
		{
			GroupList.push({
				"client_id":AllocatedServerList[i].client_id,
				"group_name":AllocatedServerList[i].group_name
			});
		}
		else
		{
			var arr_grp = [];
			element = AllocatedServerList[i].client_id;
			arr_grp = GroupList.reduce(function(arr, e, i) {
			  if (e.client_id === element)
			      arr.push(i);
			  return arr;
			}, []);

			if(arr_grp.length == 0){
				GroupList.push({
					"client_id":AllocatedServerList[i].client_id,
					"group_name":AllocatedServerList[i].group_name
				});
			}
		}
	}
}

$('.btn-show').click(function () {
	csv = false;
	clientId = Group.val();
	legalentityId = LegalEntity.val();
	SearchedList = [];

	if(clientId != '' && legalentityId != ''){
		showHit = true;
		for(var i=0;i<AllocatedServerList.length;i++){
			if(AllocatedServerList[i].client_id == clientId &&
				AllocatedServerList[i].legal_entity_id == legalentityId){
				totalRecord = 1;
				SearchedList.push(AllocatedServerList[i]);
			}
		}
	}
	else if(clientId != '' && legalentityId == ''){
		showHit = true;
		for(var i=0;i<AllocatedServerList.length;i++){
			if(AllocatedServerList[i].client_id == clientId){
				totalRecord = 1;
				SearchedList.push(AllocatedServerList[i]);
			}
		}
	}
	else if(clientId == '' && legalentityId != ''){
		showHit = true;
		for(var i=0;i<AllocatedServerList.length;i++){
			if(AllocatedServerList[i].legal_entity_id == legalentityId){
				totalRecord = 1;
				SearchedList.push(AllocatedServerList[i]);
			}
		}
	}
	else if(clientId == '' && legalentityId == ''){
		showHit = false;
		totalRecord = 1;
		clientIds = [];
		for (var i=0;i<AllocatedServerList.length;i++){
	        var occur = -1;
	        for(var j=0;j<clientIds.length;j++){
	            if(AllocatedServerList[i].client_id == clientIds[j]){
	                occur = 1;
	                break;
	            }
	        }
	        if(occur < 0){
	            clientIds.push(AllocatedServerList[i].client_id);
	        }
	    }
	    totalRecord = clientIds.length;
		SearchedList = AllocatedServerList;
	}
	processPaging();
});

$('.btn-export').click(function () {
	csv = true;
	clientId = Group.val();
	if(clientId == "")
		clientId = 0;
	legalentityId = LegalEntity.val();
	if(legalentityId == "")
		legalentityId = 0;
	function onSuccess(data) {
		var download_url = data.link;
        $(location).attr('href', download_url);
	}
	function onFailure(error) {
		if (error == "ExportToCSVEmpty") {
	        displayMessage(message.empty_export);
	    }else {
			displayMessage(error);
		}
	}
	displayLoader();
	mirror.exportAllocateServerReportData(parseInt(clientId), parseInt(legalentityId), csv, function (error, response) {
		console.log(error, response)
		if (error == null) {
			onSuccess(response);
			hideLoader();
		} else {
			onFailure(error);
			hideLoader();
		}
	});
});

function loadAllocateDBEnvReport(data){
	$('.tbody-allocate-db-env-list').empty();
	//$('.allocate-grp-inner-list').empty();
	$('.grid-table-rpt').show();
	$('.details').show();
	  $('#compliance_animation')
	    .removeClass().addClass('bounceInLeft animated')
	    .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
	    $(this).removeClass();
	  });
	var r = 1;
	for(var i=0;i<GroupList.length;i++){
		var cl_id = GroupList[i].client_id;
		var cl_count = 0;
		for(var j=0;j<data.length;j++){
			value = data[j];
			if(data[j].client_id == cl_id && cl_count == 0){
				cl_count++;
				var tableData = $('#templates .allocate-grp-list');
				var cloneData = tableData.clone();
				$('.sno', cloneData).text(r);
				console.log("tree-"+cl_id)
				//$('.appl-group-name', cloneData).addClass(value.client_id)
				$('.appl-group-name', cloneData).addClass("-"+value.client_id);
				$('.appl-group-name', cloneData).html(value.group_name).on('click', function() { tree_open_close(this); });
				$('.grp-appl-name', cloneData).text(value.machine_name);
				$('.grp-db-name', cloneData).text(value.client_db_server_name);
				$('.tbody-allocate-db-env-list').append(cloneData);

				var tableData_1 = $('#templates .allocate-grp-inner-list');
				var cloneData_1 = tableData_1.clone().addClass('tree' + value.client_id);
				$('.le-name', cloneData_1).text(value.legal_entity_name);
				$('.inner-db-name', cloneData_1).text(value.db_server_name);
				$('.inner-file-name', cloneData_1).text(value.file_server_name);
				$('.tbody-allocate-db-env-list').append(cloneData_1);
				r++;
			}
			else
			{
				//console.log(cl_count);
				if(data[j].client_id == cl_id){
					console.log("le:"+value.legal_entity_name)
					var tableData_1 = $('#templates .allocate-grp-inner-list');
					var cloneData_1 = tableData_1.clone().addClass('tree' + cl_id);
					$('.le-name', cloneData_1).text(value.legal_entity_name);
					$('.inner-db-name', cloneData_1).text(value.db_server_name);
					$('.inner-file-name', cloneData_1).text(value.file_server_name);
					$('.tbody-allocate-db-env-list').append(cloneData_1);
				}
			}
		}
	}
}

function loadSearchedData(data){
	$('.tbody-allocate-db-env-list').empty();
	//$('.allocate-grp-inner-list').empty();
	console.log($('.tbody-allocate-db-env-list .allocate-grp-inner-list').length)
	$('.grid-table-rpt').show();
	$('.details').show();
	  $('#compliance_animation')
	    .removeClass().addClass('bounceInLeft animated')
	    .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
	    $(this).removeClass();
	  });
	var r = 1;

	var cl_count = 0;
	for(var j=0;j<data.length;j++){
		value = data[j];
		if(data[j].client_id == clientId && cl_count == 0){
			cl_count++;
			var tableData = $('#templates .allocate-grp-list');
			var cloneData = tableData.clone();
			$('.sno', cloneData).text(r);
			//$('.appl-group-name', cloneData).addClass(value.client_id)
			$('.appl-group-name', cloneData).addClass("-"+value.client_id);
			$('.appl-group-name', cloneData).html(value.group_name).on('click', function() { tree_open_close(this); });
			$('.grp-appl-name', cloneData).text(value.machine_name);
			$('.grp-db-name', cloneData).text(value.client_db_server_name);
			$('.tbody-allocate-db-env-list').append(cloneData);

			var tableData_1 = $('#templates .allocate-grp-inner-list');
			var cloneData_1 = tableData_1.clone().addClass('tree' + value.client_id);
			$('.le-name', cloneData_1).text(value.legal_entity_name);
			$('.inner-db-name', cloneData_1).text(value.db_server_name);
			$('.inner-file-name', cloneData_1).text(value.file_server_name);
			$('.tbody-allocate-db-env-list').append(cloneData_1);
			r++;
		}
		else
		{
			//console.log(cl_count);
			if(data[j].client_id == clientId){

				console.log($('.tbody-allocate-db-env-list .allocate-grp-inner-list').length)
				var tableData_1 = $('#templates .allocate-grp-inner-list');
				var cloneData_1 = tableData_1.clone().addClass('tree' + value.client_id);
				$('.le-name', cloneData_1).text(value.legal_entity_name);
				$('.inner-db-name', cloneData_1).text(value.db_server_name);
				$('.inner-file-name', cloneData_1).text(value.file_server_name);
				$('.tbody-allocate-db-env-list').append(cloneData_1);
			}
		}
	}
	showHit = false;
}

function tree_open_close(e) {
	console.log("click:"+e.className)
	id = e.className.split("-")[4];
    $('.tree' + id).toggle("slow");
}

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
    if(current_id == "group-id"){
    	LegalEntityVal.val('');
		LegalEntity.val('');
    }
}
GroupVal.keyup(function (e) {
	var text_val = $(this).val();
    commonAutoComplete(
      e, ACGroup, Group, text_val,
      GroupList, "group_name", "client_id", function (val) {
        onAutoCompleteSuccess(GroupVal, Group, val);
    });
});


LegalEntityVal.keyup(function (e) {
	clientId = Group.val();
	LegalEntityList = [];
	if(clientId != '')
	{
		for(var i=0;i<AllocatedServerList.length;i++)
		{
			if(AllocatedServerList[i].client_id == clientId)
			{
				if(LegalEntityList.length==0)
				{
					LegalEntityList.push({
						"legal_entity_id":AllocatedServerList[i].legal_entity_id,
						"legal_entity_name":AllocatedServerList[i].legal_entity_name
					});
				}
				else
				{
					var arr_le = [];
					element = AllocatedServerList[i].legal_entity_id;
					arr_le = LegalEntityList.reduce(function(arr, e, i) {
					  if (e.legal_entity_id === element)
					      arr.push(i);
					  return arr;
					}, []);

					if(arr_le.length == 0){
						LegalEntityList.push({
							"legal_entity_id":AllocatedServerList[i].legal_entity_id,
							"legal_entity_name":AllocatedServerList[i].legal_entity_name
						});
					}
				}
			}
		}

		var text_val = $(this).val();
	    commonAutoComplete(
	      e, ACLegalEntity, LegalEntity, text_val,
	      LegalEntityList, "legal_entity_name", "legal_entity_id", function (val) {
	        onAutoCompleteSuccess(LegalEntityVal, LegalEntity, val);
	    });
	}
});

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
		$('.tbody-allocate-db-env-list').empty();
		var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
		var clone4 = tableRow4.clone();
		$('.no_records', clone4).text('No Records Found');
		$('.tbody-allocate-db-env-list').append(clone4);
		PaginationView.hide();
		hideLoader();
	} else {
	if(sno==0){
		createPageView(totalRecord);
	}
	PaginationView.show();
	//ReportView.show();
	if(showHit == true)
		loadSearchedData(ReportData);
	else
		loadAllocateDBEnvReport(ReportData);
	}
}

function pageData(on_current_page){
	data = [];
	dataView = [];
	_page_limit = parseInt(ItemsPerPage.val());
	recordLength = (parseInt(on_current_page) * _page_limit);
	console.log(totalRecord,_page_limit)
	var showFrom = sno + 1;
	var is_null = true;
	if(showHit == true){
		dataView = SearchedList;
	}else{
		dataView = SearchedList;
	}
	for(i=sno;i<dataView.length;i++)
	{
		is_null = false;
		data.push(dataView[i]);
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

function resetForm(){
	GroupVal.val('');
	Group.val('');
	LegalEntityVal.val('');
	LegalEntity.val('');
	$('.grid-table-rpt').hide();
	csv = false;
	totalRecord = 0;
	on_current_page = 1;
	sno = 0;
}

function renderControls(){
  initialize();
  resetForm();
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
	$('.tree-open-close').click(function() {
	    $('.tree-data').toggle("slow");
	});
});