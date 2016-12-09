var legalEntityClosureList;
var toggle_le_id = null;

function loadLegalEntityClosureList()
{
	console.log("inside getGroupAdmin_Group")
	function onSuccess(data) {
		console.log("data:"+data)
		legalEntityClosureList = data.legalentity_closure;
		LegalEntityClosureData(legalEntityClosureList);
	}
	function onFailure(error) {
		custom_alert(error);
	}
	mirror.getLegalEntityClosureData(function (error, response) {
		if (error == null) {
	  		onSuccess(response);
		} else {
  			onFailure(error);
		}
	});
}

function LegalEntityClosureData(data)
{
	var j = 1;
	$('.tbody-le-closure-list').find('tr').remove();
	$.each(data, function(k, val){
		var tableRow = $('#templates .table-row');
		var clone = tableRow.clone();
		$('.sno', clone).text(j);
		$('.Country', clone).text(val.country_name);
		$('.Group', clone).text(val.group_name);
		$('.Business-group', clone).text(val.business_group_name);
		$('#le_id', clone).addClass('-'+val.legal_entity_id);
		$('.legal-entity', clone).text(val.legal_entity_name);
		$('.le_id', clone).text(val.legal_entity_id);

		if(val.is_active == true)
		{
			$('#close', clone).show();
			$('#close', clone).addClass('-'+val.legal_entity_id)
			$('#close', clone).on('click', function() {
	      Custombox.open({
	          target: '#custom-modal',
	          effect: 'contentscale',
	          open:   function() {
	            popup_toggle(this.className, val.legal_entity_id, 'close');
	          } 
	        });
	            
	    });
			//$('.modal')
			$('#reactive', clone).hide();
			$('.closed', clone).hide();
			$('.closed', clone).text('');
			//break;
		}
		else
		{
			console.log("validity:"+val.validity_days)
			if(parseInt(val.validity_days) > 90)
			{
				$('#close', clone).hide();
				$('#reactive', clone).hide();
				$('.closed', clone).show();
				$('.closed', clone).text('Closed');
				//break;
			}
			else
			{
				console.log('validity')
				$('#close', clone).hide();
				$('#reactive', clone).show();
				$('#reactive', clone).addClass('-'+val.legal_entity_id)
				$('#reactive', clone).on('click', function() {
					Custombox.open({
		        target: '#custom-modal',
		        effect: 'contentscale',
		        open:   function() {
		          popup_toggle(this.className, val.legal_entity_id, 'reactive');
		        } 
	  			});
	          
	      });
				$('#reactive', clone).attr('title', val.validity_days+' days left')
				$('.closed', clone).hide();
				$('.closed', clone).text('');
				//break;
			}
		}

		$('.tbody-le-closure-list').append(clone);
		j++;
	});
	// j = 1;
	// var status_select = $('#status_select').val();
	// console.log("status:"+status_select)
	// for(var i=0;i<data.length;i++)
	// {
	// 	if(status_select == "-1")
	// 	{
	// 		bindLegalEntityClosureData(data[i], j);
	// 		j = j + 1;
	// 	}
	// 	else if(status_select == "0")
	// 	{
	// 		if(data[i].validity_days != '' && data[i].validity_days > 90)
	// 		{
	// 			bindLegalEntityClosureData(data[i], j);
	// 			j = j + 1;
	// 		}
	// 	}
	// 	else if(status_select == "1")
	// 	{
	// 		if(data[i].is_active == true)
	// 		{
	// 			bindLegalEntityClosureData(data[i], j);
	// 			j = j + 1;
	// 		}
	// 	}
	// 	else if(status_select == "2")
	// 	{
	// 		if(data[i].validity_days != '' && data[i].validity_days < 90)
	// 		{
	// 			bindLegalEntityClosureData(data[i], j);
	// 			j = j + 1;
	// 		}
	// 	}
	// }
}
function bindLegalEntityClosureData(data, j)
{	
	console.log(data);
	val = data;
	var tableRow = $('#templates .table-row');
	var clone = tableRow.clone();
	$('.sno', clone).text(j);
	$('.Country', clone).text(val.country_name);
	$('.Group', clone).text(val.group_name);
	$('.Business-group', clone).text(val.business_group_name);
	$('#le_id', clone).addClass('-'+val.legal_entity_id);
	$('.legal-entity', clone).text(val.legal_entity_name);
	$('.le_id', clone).text(val.legal_entity_id);

	console.log(j)
	console.log("le:"+val.legal_entity_id)
	if(val.is_active == true)
	{
		$('#close', clone).show();
		$('#close', clone).addClass('-'+val.legal_entity_id)
		$('#close', clone).on('click', function() {
			Custombox.open({
			  target: '#custom-modal',
			  effect: 'contentscale',
			  open:   function() {
			    popup_toggle(this.className, val.legal_entity_id, 'close');
			  } 
			});	    
		});
		//$('.modal')
		$('#reactive', clone).hide();
		$('.closed', clone).hide();
		$('.closed', clone).text('');
		//break;
	}
	else
	{
		console.log("validity:"+val.validity_days)
		if(parseInt(val.validity_days) > 90)
		{
			$('#close', clone).hide();
			$('#reactive', clone).hide();
			$('.closed', clone).show();
			$('.closed', clone).text('Closed');
			//break;
		}
		else
		{
			console.log('validity')
			$('#close', clone).hide();
			$('#reactive', clone).show();
			$('#reactive', clone).addClass('-'+val.legal_entity_id)
			$('#reactive', clone).on('click', function() {
				Custombox.open({
			        target: '#custom-modal',
			        effect: 'contentscale',
			        open:   function() {
			          popup_toggle(this.className, val.legal_entity_id, 'reactive');
			        } 
  				});
            });
			$('#reactive', clone).attr('title', val.validity_days+' days left')
			$('.closed', clone).hide();
			$('.closed', clone).text('');
			//break;
		}
	}

	$('.tbody-le-closure-list').append(clone);
}

function popup_toggle(e, le_id, mode)
{
	var split_e_le_id = e.split("-")[2].trim();
	//$('.modal').show();
	$('#techno_pwd').val('');
	$('#remarks').val('');
	toggle_le_id = split_e_le_id+","+mode;
	alert(toggle_le_id);
}

function closeToggle()
{
	$('.modal').hide();
	toggle_le_id = null;
}

$('#update_status').click(function() {
	var txtpwd = $('#techno_pwd').val();
	var txtRemarks = $('#remarks').val();
	var le_id, action_mode;
	alert(toggle_le_id);
	if(txtpwd != '' && txtRemarks != '')
	{
		if(toggle_le_id.indexOf(",") >= 0)
		{
			le_id = toggle_le_id.split(',')[0];
			action_mode = toggle_le_id.split(',')[1];
			function onSuccess(data) {
				loadLegalEntityClosureList();
			}
			function onFailure(error) {
				custom_alert(error);
			}
			mirror.saveLegalEntityClosureData(txtpwd, txtRemarks, parseInt(le_id), action_mode, function (error, response) {
				if (error == null) {
					$('.modal').hide();
					toggle_le_id = null;
					if (action_mode == "close")
						displayMessage(message.legal_entity_closed);
					else if (action_mode == "reactive")
						displayMessage(message.legal_entity_reactivated);
			  		onSuccess(response);
				} else {
		  			onFailure(error);
				}
			});
		}
	}
	else
	{
		if(txtpwd == '')
		{
			displayMessage(message.enter_password);
		}
		else
		{
			displayMessage(message.remarks_required);
		}
	}
});

// function processFilterSearch()
// {
// 	ctryname_search = $('#search-country-name').val().toLowerCase();
// 	grpname_search = $('#search-Group-name').val().toLowerCase();
// 	bgrpname_search = $('#search-business-group').val().toLowerCase();
// 	lename_search = $('#search-legal-entity').val().toLowerCase();
// 	var status_select = $('#status_select').val();

// 	searchList = [];
// 	for(var v in legalEntityClosureList)
// 	{
// 		data = legalEntityClosureList[v];
// 		c_name = data.country_name.toLowerCase();
// 		g_name = data.group_name.toLowerCase();
// 		bg_name = data.business_group_name.toLowerCase();
// 		le_name = data.legal_entity_name.toLowerCase();


// 		if (
// 	      (~c_name.indexOf(ctryname_search)) && (~g_name.indexOf(grpname_search)) &&
// 	      (~bg_name.indexOf(bgrpname_search)) && (~le_name.indexOf(lename_search))
// 	    )
// 		{
// 			if(status_select == "-1")
// 			{
// 				searchList.push(data);
// 			}
// 			else if(status_select == "0")
// 			{
// 				if(data.validity_days != '' && data.validity_days > 90)
// 				{
// 					searchList.push(data);
// 				}
// 			}
// 			else if(status_select == "1")
// 			{
// 				if(data.is_active == true)
// 				{
// 					searchList.push(data);
// 				}
// 			}
// 			else if(status_select == "2")
// 			{
// 				if(data.validity_days != '' && data.validity_days < 90)
// 				{
// 					searchList.push(data);
// 				}
// 			}
// 		}
// 	}
// 	bindSearchList(searchList);
// }

// function bindSearchList(searchList)
// {
// 	if(searchList.length > 0)
// 	{
// 		$('.tbody-le-closure-list').find('tr').remove();
// 		j = 1;

// 		for(var i=0;i<searchList.length;i++)
// 		{
// 			bindLegalEntityClosureData(searchList[i], j);
// 			j = j + 1;
// 		}
// 	}
// }

// page load
function initialize() {
	console.log("initialize")
	clearMessage();
  	loadLegalEntityClosureList();
}

$(document).ready(function () {
  initialize();
});
$('#status_select').on('change', function(){
  findLegalEntityClosureData();
});
// $('.filter-text-box').keyup(function() {
//     processFilterSearch();
// });
$(document).find('.js-filtertable').each(function(){
    $(this).filtertable().addFilter('.js-filter');
});

