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

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

function initialize()
{
	function onSuccess(data) {
		userCategoryList = data.user_categories;
		userList = data.reassign_user_clients;
		userClientGroups = data.clients;
		userDomainList = data.reassign_domains;
		//userGroupAssignedList = data.reassign_assignedgroups;
		console.log(data);
		resetAllfilter();
	}
	function onFailure(error) {
		displayMessage(error);
	}
	mirror.getAssignedUserClientGroups(function (error, response) {
		if (error == null) {
		  onSuccess(response);
		} else {
		  onFailure(error);
		}
	});
}

$('.btn-show').click(function () {
  alert("show");
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
      console.log("success")
      console.log(data);
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
      		totalRecord = userGroupAssignedList.length;
			processPaging();
		}else if(categoryName == "Techno Executive"){
			$('.techno-manager').hide();
      		$('.techno-executive').show();
      		$('.domain-user').hide();
      		$('.tbody-reassignuserrpt-techno-exec-list').find('tr').remove();
      		userGroupAssignedList = data.reassign_user_list;
      		totalRecord = userGroupAssignedList.length;
			processPaging();
		}else if(categoryName == "Domain Manager"){
			$('.techno-manager').hide();
      		$('.techno-executive').hide();
      		$('.domain-user').show();
      		$('.tbody-reassignuserrpt-domain-user-list').find('tr').remove();
      		userGroupAssignedList = data.reassign_domains_list;
      		totalRecord = userGroupAssignedList.length;
			processPaging();
		}else if(categoryName == "Domain Executive"){
			$('.techno-manager').hide();
      		$('.techno-executive').hide();
      		$('.domain-user').show();
      		$('.tbody-reassignuserrpt-domain-user-list').find('tr').remove();
      		userGroupAssignedList = data.reassign_domains_list;
      		totalRecord = userGroupAssignedList.length;
			processPaging();
		}

    }
    function onFailure(error) {
      displayMessage(error);
    }
    if(categoryName == "Techno Manager" || categoryName == "Techno Executive"){
    	mirror.getReassignUserReportData(parseInt(category_val), parseInt(user_id), parseInt(group_id_none), function (error, response) {
    		if (error == null) {
	        onSuccess(response);
	      } else {
	        onFailure(error);
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
			mirror.getReassignUserDomainReportData(parseInt(category_val), parseInt(user_id), parseInt(group_id_none), parseInt(bg_id_none), parseInt(LegalEntity.val()), parseInt(Domain.val()), function (error, response) {
	    		if (error == null) {
		        onSuccess(response);
		      } else {
		        onFailure(error);
		      }
		    });
		}
		else
		{
			if(Group.val() == '')
				displayMessage(message.group_required);
			else if(LegalEntity.val() == '')
				displayMessage(message.legal_entity_required);
			else if(Domain.val() == '')
				displayMessage(message.domain_required);
		}
	}

  }
  else
  {
  	if(user_id == '')
  	{
  		displayMessage(message.employeename_required);
  	}
  }
});

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
		for(var i=0;i<data.length;i++)
		{
			client_occur_cnt = 0;
			var arr_clients = [];
			element = $('#group-id').val();
			arr_clients = data.reduce(function(arr, e, i) {
				console.log("e:"+e.client_id)
			    if (e.client_id === element)
			        arr.push(i);
			    console.log(arr)
			    return arr;
			}, []);

			console.log("arr len:"+arr_clients.length);
			if(arr_clients.length > 0)
			{
				if(client_occur_cnt == 0)
				{
					if(arr_clients > 1)
					{
						bindReassignedTechUserData(data[i], j, tbodyClass, true);
					}
					else
					{
						bindReassignedTechUserData(data[i], j, tbodyClass, false);
					}
					j = j + 1;
					client_occur_cnt = client_occur_cnt + 1;
				}
				else
				{
					bindReassignTechSubData(data[i], tbodyClass);
				}

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
			console.log("element:"+element)
			var arr_clients = []
			arr_clients = data.reduce(function(arr, e, i) {
				console.log("e:"+e.client_id)
			    if (e.client_id === element)
			        arr.push(i);
			    console.log(arr)
			    return arr;
			}, []);

			console.log("arr len:"+arr_clients.length);
			if(arr_clients.length > 0)
			{
				for(var k=0;k<arr_clients.length;k++)
				{
					arr_indx = arr_clients[k];
					if(client_occur_cnt == 0)
					{
						bindReassignedTechUserData(data[arr_indx], j, tbodyClass);
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

function bindReassignedTechUserData(data, j, tbodyClass, rowClass)
{
	console.log("j:"+j)
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
	$('.group-name', clone).text(val.group_name);
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
	var tableSubRow = $('#templates .tree-data');
	var clone = tableSubRow.clone();
	$('.empty', clone).text();
	$('.assigned-date', clone).text(val.unit_email_date);
	//$('.assigned-date', clone).text("01/06/2016");
	$('.assigned', clone).text(val.emp_code_name);
	//$('.assigned', clone).text("EMP0011 - Murali");
	$('.remarks', clone).text(val.remarks);
	//$('.remarks', clone).text("Sample remarks");
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
		for(var i=0;i<data.length;i++)
		{
			client_occur_cnt = 0;
			var arr_clients = [];
			element = $('#group-id').val();
			arr_clients = data.reduce(function(arr, e, i) {
				console.log("e:"+e.client_id)
			    if (e.client_id === element)
			        arr.push(i);
			    console.log(arr)
			    return arr;
			}, []);

			console.log("arr len:"+arr_clients.length);
			if(arr_clients.length > 0)
			{
				if(client_occur_cnt == 0)
				{
					if(arr_clients > 1)
					{
						bindReassignedTechexecData(data[i], j, tbodyClass, true);
					}
					else
					{
						bindReassignedTechexecData(data[i], j, tbodyClass, false);
					}
					j = j + 1;
					client_occur_cnt = client_occur_cnt + 1;
				}
				else
				{
					bindReassignTechexecSubData(data[i], tbodyClass);
				}

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
			console.log("element:"+element)
			var arr_clients = []
			arr_clients = data.reduce(function(arr, e, i) {
				console.log("e:"+e.client_id)
			    if (e.client_id === element)
			        arr.push(i);
			    console.log(arr)
			    return arr;
			}, []);

			console.log("arr len:"+arr_clients.length);
			if(arr_clients.length > 0)
			{
				for(var k=0;k<arr_clients.length;k++)
				{
					arr_indx = arr_clients[k];
					if(client_occur_cnt == 0)
					{
						bindReassignedTechexecData(data[arr_indx], j, tbodyClass);
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
	console.log("j:"+j)
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
	$('.no-of-le', clone).text(le_name);
	$('.assigned-date', clone).text(val.unit_email_date);
	$('.assigned', clone).text(val.emp_code_name);
	$('.remarks', clone).text(val.remarks);
	tbodyClass.append(clone);
	//bindReassignSubData(data, tbodyClass);
}

function bindReassignTechexecSubData(data, tbodyClass)
{
	val = data;
	var tableSubRow = $('#templates .tree-data');
	var clone = tableSubRow.clone();
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
	j = 1;

	for(var i=0;i<userGroupAssignedList.length;i++)
	{
		client_occur_cnt = 0;
		element = userGroupAssignedList[i].unit_id;
		console.log("element:"+element)
		var arr_clients = []
		arr_clients = data.reduce(function(arr, e, i) {
			console.log("e:"+e.unit_id)
		    if (e.unit_id === element)
		        arr.push(i);
		    console.log(arr)
		    return arr;
		}, []);

		console.log("arr len:"+arr_clients.length);
		if(arr_clients.length > 0)
		{
			for(var k=0;k<arr_clients.length;k++)
			{
				arr_indx = arr_clients[k];
				if(client_occur_cnt == 0)
				{
					bindReassignedDomainData(data[arr_indx], j, tbodyClass);
					j = j + 1;
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
	console.log("j:"+j)
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
	//$('.zmdi-info', clone).addClass('-'+val.unit_id);
	$('.zmdi-info').hover(function(){
      showTitle(this, val.address, val.postal_code);
    });
	$('.unit-name', clone).text(val.unit_name);
	$('.no-of-le', clone).text(val.geography_name);
	$('.assigned-date', clone).text(val.unit_email_date);
	$('.assigned', clone).text(val.emp_code_name);
	$('.remarks', clone).text(val.remarks);
	tbodyClass.append(clone);
	//bindReassignSubData(data, tbodyClass);
}

//Status Title
function showTitle(e, address, postal_code){
	console.log("hiover")
  var titleText = address+","+postal_code;
    e.title = titleText;

}
function bindReassignDomainSubData(data, tbodyClass)
{
	val = data;
	var tableSubRow = $('#templates .tree-data');
	var clone = tableSubRow.clone();
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
  totalRecord = userGroupAssignedList.length;
  ReportData = pageData(on_current_page);
  if (totalRecord == 0) {
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
  console.log(totalRecord,_page_limit)
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
  var text_val = $(this).val();
  var user_list = []
  console.log("usercategory:"+$('#usercategory').val());
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
  var text_val = $(this).val();
  var group_list=[];
  if($('#manager-id').val() > 0)
  {
    for(var i=0;i<userList.length;i++)
    {
      if(userList[i].user_id == $('#manager-id').val())
      {
      	for(var j=0;j<userClientGroups.length;j++)
      	{
      		console.log("client list")
      		if(jQuery.inArray(userList[i].client_ids, userClientGroups[j].client_id)){
      			console.log("true")
      			group_list.push({
		          "client_id": userClientGroups[j].client_id,
		          "group_name": userClientGroups[j].group_name,
		          "is_active":userClientGroups[j].is_active
		        });
      		}
      	}
      }
    }
    console.log(group_list.length)
    commonAutoComplete(
      e, ACGroup, Group, text_val,
      group_list, "group_name", "client_id", function (val) {
        onAutoCompleteSuccess(GroupVal, Group, val);
    });
  }
  else
  {
    displayMessage(message.employeename_required);
  }
});

//load businessgroup form list in autocomplete text box
$('#businessgroupsval').keyup(function (e) {
  var text_val = $(this).val();
  var bg_grp = [];
  if($('#group-id').val() > 0)
  {
    for(var i=0;i<userDomainList.length;i++)
    {
      if(userDomainList[i].user_id == $('#manager-id').val() && userDomainList[i].client_id == $('#group-id').val())
      {
        bg_grp.push({
            "business_group_id": userDomainList[i].business_group_id,
            "business_group_name": userDomainList[i].business_group_name
        });
      }
    }
    console.log(bg_grp.length)
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
  var le_list = [];
  var bg_id = $('#businessgroupid').val();
  var condition_fields = [];
    var condition_values = [];
  if($('#group-id').val() > 0)
  {

    for(var i=0;i<userDomainList.length;i++)
    {
      var bg_check = bg_id>0?(bg_id == userDomainList[i].business_group_id):false;
      if(($('#group-id').val() == userDomainList[i].client_id)
      	&& (bg_check == true || bg_check == false) &&
      	(userDomainList[i].user_id == $('#manager-id').val()))
      {
        le_list.push({
          "legal_entity_id": userDomainList[i].legal_entity_id,
          "legal_entity_name": userDomainList[i].legal_entity_name
        });
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
  console.log("inside domains")
  var client_id = $('#group-id').val();
  var bgrp_id = $('#businessgroupid').val();
  var le_id = $('#legalentityid').val();
  var user_id = $('#manager-id').val();
  console.log("user:"+user_id)
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
            domain_list.push({
              "domain_id": userDomainList[i].domain_id,
              "domain_name": userDomainList[i].domain_name,
            });
            break;
        }
	}
	console.log("len:"+domain_list.length)
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
      displayMessage(message.legal_entity_required);
    }
  }
});
function loadSearchFilter(categoryName)
{
	if(categoryName == "Techno Manager"){
		$(".mandatory").hide();
		$(".filter-business").hide();
    	$(".filter-legal").hide();
    	$(".filter-domain").hide();
	}
	else if(categoryName == "Techno Executive"){
		$(".mandatory").hide();
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
	loadUserCategory();
	$('#groupsval').val('');
	$('#managerval').val('');
	$('.tbody-reassignuserrpt-list').find('tr').remove();
	$('.grid-table-rpt').hide();
}

function resetfilter(evt)
{
  //alert("jhjh");'
  console.log(evt);
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
  loadItemsPerPage();
});
$('#usercategory').on('change', function(e){
	$('.user_category_name').text($('#usercategory option:selected').text())
	loadSearchFilter($('#usercategory option:selected').text());
	resetfilter('category');
});