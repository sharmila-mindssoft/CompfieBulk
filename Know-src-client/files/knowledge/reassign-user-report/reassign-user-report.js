var userCategoryList;
var userList;
var userDomainList;
var userClientGroups;
var userGroupAssignedList;
var totalrecord = 0;

//autocomplete varaiable
var ACGroup = $('#ac-group');
var ACBusinessGroup = $('#ac-businessgroup');
var ACLegalEntity = $('#ac-legalentity');
var ACDomain = $('#ac-domain');
var ACUser = $('#ac-user');

//Input field variable declaration
var GroupVal = $('#groupsval');
var Group = $('#group-id');
var BusinessGroupVal = $('#businessgroupsval');
var BusinessGroup = $('#businessgroupid');
var LegalEntityVal = $('#legalentityval');
var LegalEntity = $('#legalentityid');
var UserVal = $('#managerval');
var User = $('#manager-id');
var DomainVal = $('#domainval');
var Domain = $('#domainid');

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;
var ReassignedUsersList;

var ExportButton = $('#export');
var csv = false;

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

function initialize()
{
	var t0, t1;
	function onSuccess(data) {
		userCategoryList = data.user_categories;
		userList = data.reassign_user_clients;
		userClientGroups = data.clients;
		userDomainList = data.reassign_domains;
		//userGroupAssignedList = data.reassign_assignedgroups;
		//.log(data);
		//resetAllfilter();
		loadUserCategory();
	}
	function onFailure(error) {
		displayMessage(error);
	}
	displayLoader();
	t0 = performance.now();
	mirror.getAssignedUserClientGroups(function (error, response) {
		if (error == null) {
		  onSuccess(response);
		  hideLoader();
		} else {
		  onFailure(error);
		  hideLoader();
		}
	});
	t1 = performance.now();
}

ExportButton.click(function () {
	//if($('#datatable-responsive').find('tbody').find('tr').length > 0){
	csv = true;
	var category_val = $('#usercategory').val();
	var user_id = $('#manager-id').val();
	var group_id_none = $('#group-id').val();
	categoryName = $('#usercategory option:selected').text();
	if(group_id_none == '')
  	{
  		group_id_none = 0;
  	}
  	var u_m_none = null;
  	if(category_val > 0 && user_id > 0)
  	{
  		if(categoryName == "Techno Manager" || categoryName == "Techno Executive"){
	  		function onSuccess(data) {
				if (csv) {
					var download_url = data.link;
					$(location).attr('href', download_url);
				}
			}
			function onFailure(error) {
				if (error == "ExportToCSVEmpty") {
			        displayMessage(message.empty_export);
			    }else {
					displayMessage(error);
				}
			}
	    	displayLoader();
	    	mirror.exportReassignUserReportData(parseInt(category_val), parseInt(user_id), parseInt(group_id_none), u_m_none, csv, function (error, response) {
	    		if (error == null) {
		        onSuccess(response);
		        hideLoader();
		      } else {
		        onFailure(error);
		        hideLoader();
		      }
		    });
	    }else{
	    	if(Group.val() != '' && LegalEntity.val() !='' && Domain.val() != '')
			{
		    	var bg_id_none = null;
				if(BusinessGroup.val() != '')
				{
					bg_id_none = BusinessGroup.val();
				}
				u_m_none = bg_id_none +","+LegalEntity.val()+","+Domain.val();
				function onSuccess(data) {
					if (csv) {
						var download_url = data.link;
						window.open(download_url, '_blank');
					}
				}
				function onFailure(error) {
					if (error == "ExportToCSVEmpty") {
				        displayMessage(message.empty_export);
				    }else {
						displayMessage(error);
					}
				}
				displayLoader();
				mirror.exportReassignUserReportData(parseInt(category_val), parseInt(user_id), parseInt(group_id_none), u_m_none, csv, function (error, response) {
		    		if (error == null) {
			        onSuccess(response);
			        hideLoader();
			      } else {
			        onFailure(error);
			        hideLoader();
			      }
			    });
			}
			else{
				if(group_id_none == '')
	  			{
	  				displayMessage(message.group_required);
	  			}
	  			else if(LegalEntity.val() == ''){
	  				displayMessage(message.legalentity_required);
	  			}
	  			else if(Domain.val() == '')
					displayMessage(message.domain_required);
			}
	    }
  	}
  	else {
  		if(user_id == '')
	  	{
	  		if(categoryName == "Techno Manager")
	  			displayMessage(message.techno_manager_required);
	  		else if(categoryName == "Techno Executive")
	  			displayMessage(message.techno_executive_required);
	  		else if(categoryName == "Domain Manager")
	  			displayMessage(message.domain_manager_required);
	  		else if(categoryName == "Domain Executive")
	  			displayMessage(message.domain_executive_required);
	  	}
  	}

	/*}else{
		displayMessage(message.export_empty);
	}*/
});

$('.btn-show').click(function () {
  var category_val = $('#usercategory').val();
  var user_id = $('#manager-id').val();
  var group_id_none = $('#group-id').val();
  categoryName = $('#usercategory option:selected').text();

  if(category_val > 0 && user_id > 0)
  {
  	if(group_id_none == '')
  	{
  		group_id_none = 0;
  	}
  	function onSuccess(data) {
      //.log(data);
      $('.details').show();
	    $('#compliance_animation')
	      .removeClass().addClass('bounceInLeft animated')
	      .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
	      $(this).removeClass();
	    });
      if(categoryName == "Techno Manager"){
      		$('.techno-manager').show();
      		$('.techno-executive').hide();
      		$('.domain-user').hide();
      		$('.tbody-reassignuserrpt-techno-manager-list').find('tr').remove();
      		userGroupAssignedList = data.reassign_user_list;
      		totalRecord = getTechnoRecordLength("techno");
			processPaging();
		}else if(categoryName == "Techno Executive"){
			$('.techno-manager').hide();
      		$('.techno-executive').show();
      		$('.domain-user').hide();
      		$('.tbody-reassignuserrpt-techno-exec-list').find('tr').remove();
      		userGroupAssignedList = data.reassign_user_list;
      		totalRecord = getTechnoRecordLength("techno");
			processPaging();
		}else if(categoryName == "Domain Manager"){
			$('.techno-manager').hide();
      		$('.techno-executive').hide();
      		$('.domain-user').show();
      		$('.tbody-reassignuserrpt-domain-user-list').find('tr').remove();
      		userGroupAssignedList = data.reassign_domains_list;
      		totalRecord = getTechnoRecordLength("domain");
			processPaging();
		}else if(categoryName == "Domain Executive"){
			$('.techno-manager').hide();
      		$('.techno-executive').hide();
      		$('.domain-user').show();
      		$('.tbody-reassignuserrpt-domain-user-list').find('tr').remove();
      		userGroupAssignedList = data.reassign_domains_list;
      		totalRecord = getTechnoRecordLength("domain");
			processPaging();
		}
		/*if(totalRecord > 0){
			ExportButton.show();
		}else{
			ExportButton.hide();
		}*/
    }
    function onFailure(error) {
      displayMessage(error);
    }
    if(categoryName == "Techno Manager" || categoryName == "Techno Executive"){
    	displayLoader();
    	mirror.getReassignUserReportData(parseInt(category_val), parseInt(user_id), parseInt(group_id_none), function (error, response) {
    		if (error == null) {
	        onSuccess(response);
	        hideLoader();
	      } else {
	        onFailure(error);
	        hideLoader();
	      }
	    });
	}
	else
	{
		if(Group.val() != '' && LegalEntity.val() !='' && Domain.val() != '')
		{
			var bg_id_none = null;
			if(BusinessGroup.val() != '')
			{
				bg_id_none = BusinessGroup.val();
			}
			displayLoader();
			mirror.getReassignUserDomainReportData(parseInt(category_val), parseInt(user_id), parseInt(group_id_none), parseInt(bg_id_none), parseInt(LegalEntity.val()), parseInt(Domain.val()), function (error, response) {
	    		if (error == null) {
		        onSuccess(response);
		        hideLoader();
		      } else {
		        onFailure(error);
		        hideLoader();
		      }
		    });
		}
		else
		{
			if(Group.val() == '')
				displayMessage(message.group_required);
			else if(LegalEntity.val() == '')
				displayMessage(message.legalentity_required);
			else if(Domain.val() == '')
				displayMessage(message.domain_required);
		}
	}

  }
  else
  {
  	if(user_id == '')
  	{
  		if(categoryName == "Techno Manager")
  			displayMessage(message.techno_manager_required);
  		else if(categoryName == "Techno Executive")
  			displayMessage(message.techno_executive_required);
  		else if(categoryName == "Domain Manager")
  			displayMessage(message.domain_manager_required);
  		else if(categoryName == "Domain Executive")
  			displayMessage(message.domain_executive_required);
  	}
  }
});

function getTechnoRecordLength(category){
	var arr_clients = [];
	var recordCOunt = 0;

	/*for(var i=0;i<userClientGroups.length;i++)
	{
		client_occur_cnt = 0;
		element = userClientGroups[i].client_id
		arr_clients = userClientGroups.reduce(function(arr, e, i) {
		    if (e.client_id === element)
		        arr.push(i);
		    return arr;
		}, []);
	}*/
	if(category == "techno"){
		for(var i=0;i<userGroupAssignedList.length;i++){
			recordCOunt = 0;
			if(i==0){
				arr_clients.push(userGroupAssignedList[i].client_id);
			}
			else{
				for(var j=0;j<userGroupAssignedList.length;j++){
					if(arr_clients[j] == userGroupAssignedList[i].client_id){
						recordCOunt++;
					}
				}
				if(recordCOunt == 0){
					arr_clients.push(userGroupAssignedList[i].client_id);
				}
			}
		}
	}
	else{
		for(var i=0;i<userGroupAssignedList.length;i++){
			var occur = -1;
			for(var j=0;j<arr_clients.length;j++){
				if(arr_clients[j] == userGroupAssignedList[i].unit_id){
					occur = 1;
					break;
				}
			}
			if(occur < 0){
				arr_clients.push(userGroupAssignedList[i].unit_id)
			}
		}
	}
	return arr_clients.length;
}

function getAllIndexes(arr, val) {
    var indexes = [], i = -1;
    while ((i = arr.indexOf(val, i+1)) != -1){
        indexes.push(i);
    }
    return indexes;
}

//Techno manager start------------------------------------------------------------
function loaduserGroupAssignedList(tbodyClass, data)
{
	//data = userGroupAssignedList;
	tbodyClass.find('tr').remove();
	$('.categoryval').text($('#usercategory option:selected').text());
	$('.userval').text($('#managerval').val());
	var tableheading = $('#templates .tr-heading');
	var cloneheading = tableheading.clone();
	tbodyClass.append(cloneheading);
	j = 1;

	if($('#group-id').val() > 0)
	{
		client_occur_cnt = 0;
		for(var i=0;i<data.length;i++)
		{
			if(client_occur_cnt == 0)
			{
				bindReassignedTechUserData(data[i], j, tbodyClass, true);
				j = j + 1;
				client_occur_cnt = client_occur_cnt + 1;
			}
			else
			{
				bindReassignTechSubData(data[i], tbodyClass);
			}

		}
		client_occur_cnt = 0;
	}
	else
	{
		for(var i=0;i<userClientGroups.length;i++)
		{
			client_occur_cnt = 0;
			element = userClientGroups[i].client_id
			var arr_clients = []
			arr_clients = data.reduce(function(arr, e, i) {
			    if (e.client_id === element)
			        arr.push(i);
			    return arr;
			}, []);
			if(arr_clients.length > 0)
			{
				for(var k=0;k<arr_clients.length;k++)
				{

					arr_indx = arr_clients[k];
					if(client_occur_cnt == 0)
					{
						val = data[arr_indx];
						bindReassignedTechUserData(data[arr_indx], j, tbodyClass, true);
						j = j + 1;
						client_occur_cnt = client_occur_cnt + 1;
					}
					else
					{
						bindReassignTechSubData(data[arr_indx], tbodyClass);
					}
				}
				client_occur_cnt = 0;
			}
		}
	}

}

function tree_open_close(e) {
	var len = e.className.split("-").length;
	id = e.className.split("-")[len-1];
    $('.tree' + id).toggle("slow");
}

function bindReassignedTechUserData(data, j, tbodyClass, rowClass)
{
	val = data;
	var tableRow;
	if($('#usercategory option:selected').text() == "Techno Manager")
	{
		if(rowClass == true)
		{
			tableRow = $('#templates .techno-manager .tree-open-close');
		}
		else{
			tableRow = $('#templates .techno-manager .table-row');
		}
	}

	var clone = tableRow.clone();
	$('.sno', clone).text(j);
	$('.country-name', clone).text(val.c_names);
	$('.group-name', clone).html(val.group_name);
	$('.group-name', clone).addClass("-"+val.client_id);
	$('.group-name', clone).on('click', function() { tree_open_close(this); });

	$('.no-of-le', clone).text(val.le_count);
	$('.assigned-date', clone).text(val.unit_email_date);
	$('.assigned', clone).text(val.emp_code_name);
	$('.remarks', clone).text(val.remarks);
	tbodyClass.append(clone);
	//bindReassignSubData(data, tbodyClass);
}

function bindReassignTechSubData(data, tbodyClass)
{
	val = data;
	var tableSubRow = $('#templates .techno-manager .tree-data');
	var clone = tableSubRow.clone().addClass('tree' + val.client_id);
	//tbodyClass.empty();
	$('.empty', clone).text();
	$('.assigned-date', clone).text(val.unit_email_date);
	//$('.assigned-date', clone).text("01/06/2016");
	$('.assigned', clone).text(val.emp_code_name);
	//$('.assigned', clone).text("EMP0011 - Murali");
	$('.remarks', clone).text(val.remarks);
	//$('.remarks', clone).text("Sample remarks");
	//tbody-reassignuserrpt-techno-manager-list
	tbodyClass.append(clone);
}
//Techno manager end------------------------------------------------------------------

//Techno exec start-------------------------------------------------------------------
function loadtechnoexecGroupAssignedList(tbodyClass, data)
{
	//data = userGroupAssignedList;
	tbodyClass.find('tr').remove();
	$('.categoryval').text($('#usercategory option:selected').text());
	$('.userval').text($('#managerval').val());
	var tableheading = $('#templates .tr-heading');
	var cloneheading = tableheading.clone();
	tbodyClass.append(cloneheading);
	j = 1;

	if($('#group-id').val() > 0)
	{
		client_occur_cnt = 0;

		for(var i=0;i<data.length;i++)
		{
			if(client_occur_cnt == 0)
			{
				bindReassignedTechexecData(data[i], j, tbodyClass, true);
				j = j + 1;
				client_occur_cnt = client_occur_cnt + 1;
			}
			else
			{
				bindReassignTechexecSubData(data[i], tbodyClass);
			}

		}
		client_occur_cnt = 0;
	}
	else
	{
		for(var i=0;i<userClientGroups.length;i++)
		{
			client_occur_cnt = 0;
			element = userClientGroups[i].client_id
			var arr_clients = []
			arr_clients = data.reduce(function(arr, e, i) {
			    if (e.client_id === element)
			        arr.push(i);
			    return arr;
			}, []);

			if(arr_clients.length > 0)
			{
				for(var k=0;k<arr_clients.length;k++)
				{
					arr_indx = arr_clients[k];
					if(client_occur_cnt == 0)
					{
						bindReassignedTechexecData(data[arr_indx], j, tbodyClass, true);
						j = j + 1;
						client_occur_cnt = client_occur_cnt + 1;
					}
					else
					{
						bindReassignTechexecSubData(data[arr_indx], tbodyClass);
					}
				}
				client_occur_cnt = 0;
			}
		}
	}

}

function bindReassignedTechexecData(data, j, tbodyClass, rowClass)
{
	val = data;
	var tableRow;
	if($('#usercategory option:selected').text() == "Techno Executive")
	{
		if(rowClass == true)
		{
			tableRow = $('#templates .techno-exec .tree-open-close');
		}
		else{
			tableRow = $('#templates .techno-exec .table-row');
		}
	}

	var clone = tableRow.clone();
	$('.sno', clone).text(j);
	$('.group-name', clone).text(val.group_name);
	var le_name, bg_name;
	for(var i=0;i<userDomainList.length;i++)
	{
		if(val.client_id == userDomainList[i].client_id)
		{
			bg_name = userDomainList[i].business_group_name;
			le_name = userDomainList[i].legal_entity_name;
			break;
		}
	}
	$('.bg-name', clone).text(bg_name);
	$('.country-name', clone).text(val.c_names);

	$('.no-of-le', clone).html(le_name);
	$('.no-of-le', clone).addClass("-"+val.client_id);
	$('.no-of-le', clone).on('click', function() { tree_open_close(this); });

	//$('.no-of-le', clone).text(le_name);
	$('.assigned-date', clone).text(val.unit_email_date);
	$('.assigned', clone).text(val.emp_code_name);
	$('.remarks', clone).text(val.remarks);
	tbodyClass.append(clone);
	//bindReassignSubData(data, tbodyClass);
}

function bindReassignTechexecSubData(data, tbodyClass)
{
	val = data;
	var tableSubRow = $('#templates .techno-exec .tree-data');
	var clone = tableSubRow.clone().addClass('tree' + val.client_id);
	$('.empty', clone).text();
	$('.assigned-date', clone).text(val.unit_email_date);
	//$('.assigned-date', clone).text("01/06/2016");
	$('.assigned', clone).text(val.emp_code_name);
	//$('.assigned', clone).text("EMP0011 - Murali");
	$('.remarks', clone).text(val.remarks);
	//$('.remarks', clone).text("Sample remarks");
	tbodyClass.append(clone);
}
//Techno exec end---------------------------------------------------------------------------

function getDomainUnits(){
	var unit_ids =[];
	for(var i=0;i<userGroupAssignedList.length;i++){
		var occur = -1;
		for(var j=0;j<unit_ids.length;j++){
			if(unit_ids[j] == userGroupAssignedList[i].unit_id){
				occur = 1;
				break;
			}
		}
		if(occur < 0){
			unit_ids.push(userGroupAssignedList[i].unit_id)
		}
	}
	return unit_ids;
}

//Domain manager or exec start------------------------------------------------------------
function loaddomainexecGroupAssignedList(tbodyClass, data)
{
	data = userGroupAssignedList;
	tbodyClass.find('tr').remove();
	$('.categoryval').text($('#usercategory option:selected').text());
	$('.userval').text($('#managerval').val());
	$('.groupval').text(GroupVal.val());
	$('.bgval').text(BusinessGroupVal.val());
	$('.leval').text(LegalEntityVal.val());
	$('.domainval').text(DomainVal.val());
	var tableheading = $('#templates .tr-heading');
	var cloneheading = tableheading.clone();
	tbodyClass.append(cloneheading);
	s_no = 1;
	unit_ids = getDomainUnits();


	for(var i=0;i<unit_ids.length;i++)
	{
		client_occur_cnt = 0;
		element = unit_ids[i];
		var arr_clients = []
		arr_clients = data.reduce(function(arr, e, i) {
		    if (e.unit_id === element)
		        arr.push(i);
		    return arr;
		}, []);
		if(arr_clients.length > 0)
		{
			for(var k=0;k<arr_clients.length;k++)
			{
				arr_indx = arr_clients[k];
				if(client_occur_cnt == 0)
				{
					bindReassignedDomainData(data[arr_indx], s_no, tbodyClass, true);
					s_no = s_no + 1;
					client_occur_cnt = client_occur_cnt + 1;
				}
				else
				{
					bindReassignDomainSubData(data[arr_indx], tbodyClass);
				}
			}
			client_occur_cnt = 0;
		}
	}
}

function bindReassignedDomainData(data, j, tbodyClass, rowClass)
{
	val = data;
	var tableRow;
	if($('#usercategory option:selected').text() == "Domain Manager" ||
		$('#usercategory option:selected').text() == "Domain Executive")
	{
		if(rowClass == true)
		{
			tableRow = $('#templates .domain-user .tree-open-close');
		}
		else{
			tableRow = $('#templates .domain-user .table-row');
		}
	}

	var clone = tableRow.clone();
	$('.sno', clone).text(j);
	$('.country-name', clone).text(val.unit_code);

    var titleText = val.address+","+val.postal_code;
    $('.unit-name', clone).addClass("unit-name-"+val.unit_id);
	$('.unit-name', clone).text(val.unit_name);
	var unit_ctrl = null;
	$('.unit-name', clone).on('click', function() { tree_open_close(this); });
	$('.no-of-le', clone).text(val.geography_name);
	$('.assigned-date', clone).text(val.unit_email_date);
	$('.assigned', clone).text(val.emp_code_name);
	$('.remarks', clone).text(val.remarks);
	tbodyClass.append(clone);
	//bindReassignSubData(data, tbodyClass);
	unit_ctrl = '<span class="fa fa-info-circle text-primary c-pointer" data-toggle="tooltip" title="' + titleText + '"></span>&nbsp;';
	$('.unit-name-'+val.unit_id).parent().prepend(unit_ctrl);
    $('[data-toggle="tooltip"]').tooltip();
}

//Status Title
function showTitle(e, address, postal_code){
  var titleText = address+","+postal_code;
    e.title = titleText;

}
function bindReassignDomainSubData(data, tbodyClass)
{
	val = data;
	var tableSubRow = $('#templates .domain-user .tree-data');
	var clone = tableSubRow.clone().addClass('tree' + val.unit_id);
	//var clone = tableSubRow.clone();
	$('.empty', clone).text();
	$('.assigned-date', clone).text(val.unit_email_date);
	//$('.assigned-date', clone).text("01/06/2016");
	$('.assigned', clone).text(val.emp_code_name);
	//$('.assigned', clone).text("EMP0011 - Murali");
	$('.remarks', clone).text(val.remarks);
	//$('.remarks', clone).text("Sample remarks");
	tbodyClass.append(clone);
}
//Domain manager or exec end------------------------------------------------------------------


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

function processPaging(tbodyClass){
	var tbodyClass;
	categoryName = $('#usercategory option:selected').text();
	if(categoryName == "Techno Manager"){
		tbodyClass = $('.tbody-reassignuserrpt-techno-manager-list');
	}else if(categoryName == "Techno Executive"){
		tbodyClass = $('.tbody-reassignuserrpt-techno-exec-list');
	}else if(categoryName == "Domain Manager"){
		tbodyClass = $('.tbody-reassignuserrpt-domain-user-list');
	}else if(categoryName == "Domain Executive"){
		tbodyClass = $('.tbody-reassignuserrpt-domain-user-list');
	}
  _page_limit = parseInt(ItemsPerPage.val());
  if (on_current_page == 1) {
    sno = 0
  }
  else {
    sno = (on_current_page - 1) *  _page_limit;
  }
  sno  = sno;
  //totalRecord = userGroupAssignedList.length;
  ReportData = pageData(on_current_page);
  if (totalRecord == 0) {
  	if(categoryName == "Techno Manager"){
  		$('.categoryval').text($('#usercategory option:selected').text());
		$('.userval').text($('#managerval').val());
		var tableheading = $('#templates .tr-heading');
		var cloneheading = tableheading.clone();
		tbodyClass.append(cloneheading);
	}else if(categoryName == "Techno Executive"){
  		$('.categoryval').text($('#usercategory option:selected').text());
		$('.userval').text($('#managerval').val());
		var tableheading = $('#templates .tr-heading');
		var cloneheading = tableheading.clone();
		tbodyClass.append(cloneheading);
	}else if(categoryName == "Domain Manager"){
  		$('.categoryval').text($('#usercategory option:selected').text());
		$('.userval').text($('#managerval').val());
		$('.groupval').text(GroupVal.val());
		$('.bgval').text(BusinessGroupVal.val());
		$('.leval').text(LegalEntityVal.val());
		$('.domainval').text(DomainVal.val());
		var tableheading = $('#templates .tr-heading');
		var cloneheading = tableheading.clone();
		tbodyClass.append(cloneheading);
	}else if(categoryName == "Domain Executive"){
  		$('.categoryval').text($('#usercategory option:selected').text());
		$('.userval').text($('#managerval').val());
		$('.groupval').text(GroupVal.val());
		$('.bgval').text(BusinessGroupVal.val());
		$('.leval').text(LegalEntityVal.val());
		$('.domainval').text(DomainVal.val());
		var tableheading = $('#templates .tr-heading');
		var cloneheading = tableheading.clone();
		tbodyClass.append(cloneheading);
	}
    tbodyClass.empty();
    var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
    var clone4 = tableRow4.clone();
    $('.no_records', clone4).text('No Records Found');
    tbodyClass.append(clone4);
    PaginationView.hide();
    hideLoader();
  } else {
    if(sno==0){
      createPageView(totalRecord);
    }
    PaginationView.show();
    //ReportView.show();
    if(categoryName == "Techno Manager"){
  		loaduserGroupAssignedList($('.tbody-reassignuserrpt-techno-manager-list'), ReportData);
	}else if(categoryName == "Techno Executive"){
  		loadtechnoexecGroupAssignedList($('.tbody-reassignuserrpt-techno-exec-list'), ReportData);
	}else if(categoryName == "Domain Manager"){
  		loaddomainexecGroupAssignedList($('.tbody-reassignuserrpt-domain-user-list'), ReportData);
	}else if(categoryName == "Domain Executive"){
  		loaddomainexecGroupAssignedList($('.tbody-reassignuserrpt-domain-user-list'), ReportData);
	}
  }
}

function pageData(on_current_page){
  data = [];
  _page_limit = parseInt(ItemsPerPage.val());
  recordLength = (parseInt(on_current_page) * _page_limit);
  var showFrom = sno + 1;
  var is_null = true;
  for(i=sno;i<userGroupAssignedList.length;i++)
  {
    is_null = false;
    data.push(userGroupAssignedList[i]);
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

function loadUserCategory()
{
	$.each(userCategoryList, function (key, value) {
		var obj = $('.category-drop-down option');
		var clone = obj.clone();
		var u_cg_id = value.user_category_id;
		var u_cg_name = value.user_category_name;
		clone.attr("value", u_cg_id);
		clone.text(u_cg_name);
		$('#usercategory').append(clone);
	});
	//.timeEnd("end loading user categories");
}

function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
    var current_id = id_element[0].id;
    if(current_id == 'manager-id'){
      resetfilter('user');
    }else if(current_id == 'group-id'){
      resetfilter('clients');
    }else if(current_id == 'businessgroupid'){
      resetfilter('bg');
    }else if(current_id == 'legalentityid'){
      resetfilter('le');
    }
}

//load country list in autocomplete textbox
UserVal.keyup(function (e) {
	resetfilter('user');
  var text_val = $(this).val();
  var user_list = []
  for(var i=0;i<userList.length;i++)
  {
	if($('#usercategory').val() == userList[i].user_category_id)
	{
		user_list.push({
			"user_id":userList[i].user_id,
			"employee_name": userList[i].emp_code_name
		});
	}
  }
  commonAutoComplete(
    e, ACUser, User, text_val,
    user_list, "employee_name", "user_id", function (val) {
      onAutoCompleteSuccess(UserVal, User, val);
  });
});


//load group form list in autocomplete text box
$('#groupsval').keyup(function (e) {
	resetfilter('clients');
  var text_val = $(this).val();
  var group_list=[];
  if($('#manager-id').val() > 0)
  {
    for(var i=0;i<userList.length;i++)
    {
    	if(userList[i].user_id == $('#manager-id').val())
		{
	      	var client_ids = userList[i].client_ids;
	      	for(var j=0;j<client_ids.length;j++)
	      	{
	      		for(var c=0;c<userClientGroups.length;c++)
	      		{
	      			if(client_ids[j] == userClientGroups[c].client_id){
	      				var occur = -1;
		      			for(var k=0;k<group_list.length;k++){
		      				if(group_list[k].client_id == userClientGroups[c].client_id){
		      					occur = 1;
		      					break;
		      				}
		      			}
		      			if(occur < 0){
			      			group_list.push({
					          "client_id": userClientGroups[c].client_id,
					          "group_name": userClientGroups[c].group_name,
					          "is_active":userClientGroups[c].is_active
					        });
		      			}
		      			break;
	      			}
	      		}
			}
		}
	}
    commonAutoComplete(
      e, ACGroup, Group, text_val,
      group_list, "group_name", "client_id", function (val) {
        onAutoCompleteSuccess(GroupVal, Group, val);
    });
  }
  else
  {
    //displayMessage(message.employeename_required);
    var categoryName = $('#usercategory option:selected').text();
    if(categoryName == "Techno Manager")
		displayMessage(message.techno_manager_required);
	else if(categoryName == "Techno Executive")
		displayMessage(message.techno_executive_required);
	else if(categoryName == "Domain Manager")
		displayMessage(message.domain_manager_required);
	else if(categoryName == "Domain Executive")
		displayMessage(message.domain_executive_required);
  }
});

//load businessgroup form list in autocomplete text box
$('#businessgroupsval').keyup(function (e) {
	resetfilter('bg');
  var text_val = $(this).val();
  var bg_grp = [];
  if($('#group-id').val() > 0)
  {
  	console.log("1:"+$('#manager-id').val())
  	console.log("2:"+$('#group-id').val())
  	console.log(userDomainList)
    for(var i=0;i<userDomainList.length;i++)
    {

      if(userDomainList[i].user_id == $('#manager-id').val() && userDomainList[i].client_id == $('#group-id').val())
      {
      	var occur = -1;
      	for(var k=0;k<bg_grp.length;k++){
      		if(bg_grp[k].business_group_id == userDomainList[i].business_group_id){
      			occur = 1;
      		}
      	}
      	if(occur < 0 && userDomainList[i].business_group_id != null){
      		bg_grp.push({
	            "business_group_id": userDomainList[i].business_group_id,
	            "business_group_name": userDomainList[i].business_group_name
	        });
      	}
      }
    }
    commonAutoComplete(
      e, ACBusinessGroup, BusinessGroup, text_val,
      bg_grp, "business_group_name", "business_group_id", function (val) {
        onAutoCompleteSuccess(BusinessGroupVal, BusinessGroup, val);
    });
  }
  else
  {
    if($('#group-id').val() == 0)
    {
      displayMessage(message.group_required);
    }
  }
});

//load legalentity form list in autocomplete text box
$('#legalentityval').keyup(function (e) {
	resetfilter('le');
  var le_list = [];
  var bg_id = $('#businessgroupid').val();
  var condition_fields = [];
  var condition_values = [];
  if($('#group-id').val() > 0)
  {
    for(var i=0;i<userDomainList.length;i++)
    {
      var bg_check = true;
      if(bg_id>0 && (bg_id != userDomainList[i].business_group_id)){
        bg_check =false;
      }
      if(($('#group-id').val() == userDomainList[i].client_id)
      	&& bg_check == true && (userDomainList[i].user_id == $('#manager-id').val()))
      {
      	var occur = -1;
      	for(var k=0;k<le_list.length;k++){
      		if(le_list[k].legal_entity_id == userDomainList[i].legal_entity_id){
      			occur = 1;
      			break;
      		}
      	}
      	if(occur < 0){
      		le_list.push({
	          "legal_entity_id": userDomainList[i].legal_entity_id,
	          "legal_entity_name": userDomainList[i].legal_entity_name
	        });
      	}
      }
    }
    var text_val = $(this).val();
    commonAutoComplete(
      e, ACLegalEntity, LegalEntity, text_val,
      le_list, "legal_entity_name", "legal_entity_id", function (val) {
          onAutoCompleteSuccess(LegalEntityVal, LegalEntity, val);
      });
  }
  else
  {
    if($('#group-id').val() == 0)
    {
      displayMessage(message.group_required);
    }
  }
});

 //load unit wwith condition form list in autocomplete text box
$('#domainval').keyup(function (e) {
  var client_id = $('#group-id').val();
  var bgrp_id = $('#businessgroupid').val();
  var le_id = $('#legalentityid').val();
  var user_id = $('#manager-id').val();
  var domain_list = [];
  var condition_fields = [];
	var condition_values = [];

  if(client_id > 0 && le_id > 0)
  {
    for(var i=0;i<userDomainList.length;i++)
    {
      var bg_check = bgrp_id>0?(bgrp_id == userDomainList[i].business_group_id):false;
      if((userDomainList[i].user_id == user_id && userDomainList[i].client_id == client_id &&
        userDomainList[i].legal_entity_id == le_id) && (bg_check == true || bg_check == false))
      	{
      		var occur = -1;
      		for(var k=0;k<domain_list.length;k++){
      			if(domain_list[k].domain_id == userDomainList[i].domain_id){
      				occur = 1;
      			}
      		}
      		if(occur < 0){
      			domain_list.push({
	              "domain_id": userDomainList[i].domain_id,
	              "domain_name": userDomainList[i].domain_name,
	            });
      		}
        }
	}
    var text_val = $(this).val();
    commonAutoComplete(
    e, ACDomain, Domain, text_val,
    domain_list, "domain_name", "domain_id", function (val) {
        onAutoCompleteSuccess(DomainVal, Domain, val);
    });
  }
  else
  {
    if(client_id == 0 || client_id == '')
    {
      displayMessage(message.group_required);
    }
    if(le_id == 0 || le_id == '')
    {
      displayMessage(message.legalentity_required);
    }
  }
});
function loadSearchFilter(categoryName)
{
	if(categoryName == "Techno Manager"){
		$(".mandatory").show();
		$("#te").hide();
		$(".filter-business").hide();
    	$(".filter-legal").hide();
    	$(".filter-domain").hide();
	}
	else if(categoryName == "Techno Executive"){
		$("#te").hide();
		$(".filter-business").hide();
    	$(".filter-legal").hide();
    	$(".filter-domain").hide();
	}else if(categoryName == "Domain Manager"){
		$(".mandatory").show();
		$(".filter-business").show();
    	$(".filter-legal").show();
    	$(".filter-domain").show();
	}else if(categoryName == "Domain Executive"){
		$(".mandatory").show();
		$(".filter-business").show();
    	$(".filter-legal").show();
    	$(".filter-domain").show();
	}
}
function resetAllfilter()
{
	$('#usercategory').empty();
	$('#groupsval').val('');
	$('#managerval').val('');
	UserVal.val('');
  	User.val('');
  	GroupVal.val('');
  	Group.val('')
  	BusinessGroupVal.val('');
  	BusinessGroup.val('');
  	LegalEntityVal.val('');
  	LegalEntity.val('');
  	DomainVal.val('');
  	Domain.val('');
	$('.tbody-reassignuserrpt-list').find('tr').remove();
}

function resetfilter(evt)
{
  //alert("jhjh");'
  if(evt == 'category')
  {
  	UserVal.val('');
  	User.val('');
  	GroupVal.val('');
  	Group.val('')
  	BusinessGroupVal.val('');
  	BusinessGroup.val('');
  	LegalEntityVal.val('');
  	LegalEntity.val('');
  	DomainVal.val('');
  	Domain.val('');
  }
  if(evt == "user")
  {
  	GroupVal.val('');
  	Group.val('')
  	BusinessGroupVal.val('');
  	BusinessGroup.val('');
  	LegalEntityVal.val('');
  	LegalEntity.val('');
  	DomainVal.val('');
  	Domain.val('');
  }
  if(evt == 'clients')
  {
    BusinessGroupVal.val('');
  	BusinessGroup.val('');
  	LegalEntityVal.val('');
  	LegalEntity.val('');
  	DomainVal.val('');
  	Domain.val('');
  }
  if(evt == 'bg')
  {
    LegalEntityVal.val('');
  	LegalEntity.val('');
  	DomainVal.val('');
  	Domain.val('');
  }
  if(evt == 'le')
  {
    DomainVal.val('');
  	Domain.val('');
  }
}

ItemsPerPage.on('change', function (e) {
    perPage = parseInt($(this).val());
      sno = 0;
      on_current_page = 1;
      createPageView(totalRecord);
      processPaging();
  });

$(function () {
  $('.grid-table-rpt').hide();
  initialize();
  resetAllfilter();
  loadItemsPerPage();
  $('.tree-open-close').click(function() {
	    $('.tree-data').toggle("slow");
	});
});
$('#usercategory').on('change', function(e){
	$('.user_category_name').text($('#usercategory option:selected').text())
	loadSearchFilter($('#usercategory option:selected').text());
	resetfilter('category');
	$('.details').hide();
});
