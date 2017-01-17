var legalEntityClosureList;
var toggle_le_id = null;
var FilterBox = $('.filter-text-box');
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

var Search_status_1 = $('#search-status-1');
var Search_status_ul_1 = $('.search-status-list-1');
var Search_status_li_1 = $('.search-status-li-1');

function loadLegalEntityClosureList() {
    console.log("inside getGroupAdmin_Group")

    function onSuccess(data) {
        legalEntityClosureList = data.legalentity_closure;
        LegalEntityClosureData(legalEntityClosureList);
    }

    function onFailure(error) {
        displayMessage(error);
    }
    mirror.getLegalEntityClosureData(function(error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

function LegalEntityClosureData(data) {
    var j = 1;
    $('.tbody-le-closure-list').find('tr').remove();
    $.each(data, function(k, val) {
        var tableRow = $('#templates .table-row');
        var clone = tableRow.clone();
        $('.sno', clone).text(j);
        $('.Country', clone).text(val.country_name);
        $('.Group', clone).text(val.group_name);
        $('.Business-group', clone).text(val.business_group_name);
        $('#le_id', clone).addClass('-' + val.legal_entity_id);
        $('.legal-entity', clone).text(val.legal_entity_name);
        $('.le_id', clone).text(val.legal_entity_id);

        if (val.is_active == false && val.validity_days < checkValidityDays()) {
            $('#close', clone).css("display", "block");
            $('#close', clone).addClass('-' + val.legal_entity_id)
            $('#close', clone).on('click', function() {
                Custombox.open({
                    target: '#custom-modal',
                    effect: 'contentscale',
                    open: function() {
                        popup_toggle(val.legal_entity_id, 'close');
                    }
                });

            });
            //$('.modal')
            $('#reactive', clone).css("display", "none");
            $('.closed', clone).css("display", "none");
            $('.closed', clone).text('');
            $('.status', clone).text('Active');
            //break;
        } else {
            if (val.validity_days > checkValidityDays()) { //isclose=0=close
                $('#close', clone).hide();
                $('#reactive', clone).hide();
                $('.closed', clone).css("display", "block");;
                $('.closed', clone).text('Closed');
                $('.status', clone).text('In Active');
                //break;
            } else {
                $('#close', clone).hide();
                $('#reactive', clone).css("display", "block");
                $('#reactive', clone).addClass('-' + val.legal_entity_id)
                $('#reactive', clone).on('click', function() {
                    Custombox.open({
                        target: '#custom-modal',
                        effect: 'contentscale',
                        open: function() {
                            popup_toggle(val.legal_entity_id, 'reactive');
                        }
                    });
                });
                $('#reactive', clone).attr('title', val.validity_days + ' days left')
                $('.closed', clone).hide();
                $('.closed', clone).text('');
                $('.status', clone).text('In Active');
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
// function bindLegalEntityClosureData(data, j)
// {
// 	console.log(data);
// 	val = data;
// 	var tableRow = $('#templates .table-row');
// 	var clone = tableRow.clone();
// 	$('.sno', clone).text(j);
// 	$('.Country', clone).text(val.country_name);
// 	$('.Group', clone).text(val.group_name);
// 	$('.Business-group', clone).text(val.business_group_name);
// 	$('#le_id', clone).addClass('-'+val.legal_entity_id);
// 	$('.legal-entity', clone).text(val.legal_entity_name);
// 	$('.le_id', clone).text(val.legal_entity_id);

// 	console.log(j)
// 	console.log("le:"+val.legal_entity_id)
// 	if(val.is_active == true)
// 	{
// 		$('#close', clone).show();
// 		$('#close', clone).addClass('-'+val.legal_entity_id)
// 		$('#close', clone).on('click', function() {
// 			Custombox.open({
// 			  target: '#custom-modal',
// 			  effect: 'contentscale',
// 			  open:   function() {
// 			    popup_toggle(this.className, val.legal_entity_id, 'close');
// 			  }
// 			});
// 		});
// 		//$('.modal')
// 		$('#reactive', clone).hide();
// 		$('.closed', clone).hide();
// 		$('.closed', clone).text('');
// 		//break;
// 	}
// 	else
// 	{
// 		console.log("validity:"+val.validity_days)
// 		if(parseInt(val.validity_days) > 90)
// 		{
// 			$('#close', clone).hide();
// 			$('#reactive', clone).hide();
// 			$('.closed', clone).show();
// 			$('.closed', clone).text('Closed');
// 			//break;
// 		}
// 		else
// 		{
// 			console.log('validity')
// 			$('#close', clone).hide();
// 			$('#reactive', clone).show();
// 			$('#reactive', clone).addClass('-'+val.legal_entity_id)
// 			$('#reactive', clone).on('click', function() {
// 				Custombox.open({
// 			        target: '#custom-modal',
// 			        effect: 'contentscale',
// 			        open:   function() {
// 			          popup_toggle(val.legal_entity_id, 'reactive');
// 			        }
//   				});
//             });
// 			$('#reactive', clone).attr('title', val.validity_days+' days left')
// 			$('.closed', clone).hide();
// 			$('.closed', clone).text('');
// 			//break;
// 		}
// 	}

// 	$('.tbody-le-closure-list').append(clone);
// }

function popup_toggle(le_id, mode) {
    $(".popup_legal_entity_id").val(le_id);
    $(".popup_mode").val(mode);
    //console.log("e--------"+e);
    //var split_e_le_id = e.split("-")[2].trim();
    //$('.modal').show();
    $('#techno_pwd').val('');
    $('#remarks').val('');
    //toggle_le_id = split_e_le_id+","+mode;
    //alert(toggle_le_id);
}

// function closeToggle()
// {
// 	$('.modal').hide();
// 	toggle_le_id = null;
// }

$('#update_status').click(function() {
    var txtpwd = $('#techno_pwd').val();
    var txtRemarks = $('#remarks').val();
    var le_id, action_mode;
    if (txtpwd != '' && txtRemarks != '') {
        le_id = $(".popup_legal_entity_id").val();
        action_mode = $(".popup_mode").val();

        function onSuccess(data) {
            displaySuccessMessage(message.action_success);
            loadLegalEntityClosureList();
        }

        function onFailure(error) {
            if(error == "InvalidPassword"){
                displayMessage(message.invalid_password);
                return false;
            }
            else{
                displayMessage(error);
            }
        }
        mirror.saveLegalEntityClosureData(txtpwd, txtRemarks, parseInt(le_id), action_mode, function(error, response) {
            if (error == null) {
                Custombox.close();
                $(".popup_legal_entity_id").val('');
                $(".popup_mode").val('');
                if (action_mode == "close")
                    displayMessage(message.legal_entity_closed);
                else if (action_mode == "reactive")
                    displayMessage(message.legal_entity_reactivated);
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    } else {
        console.log("Welcome2");
        if (txtpwd == '') {
            displayMessage(message.enter_password);
        } else {
            displayMessage(message.reason_required);
        }
    }
});

function processFilterSearch()
{
	ctryname_search = $('#search-country-name').val().toLowerCase();
	grpname_search = $('#search-Group-name').val().toLowerCase();
	bgrpname_search = $('#search-business-group').val().toLowerCase();
	lename_search = $('#search-legal-entity').val().toLowerCase();
    var status_select = $('.search-status-li.active').attr('value');
    var closure_select = $('.search-status-li-1.active').attr('value');
    console.log("closure_select:"+closure_select)
    var data_is_active = false;
    var data_closure = 0;
	searchList = [];
	for(var v in legalEntityClosureList)
	{
        data_is_active = true;
        data_closure = 0;
		data = legalEntityClosureList[v];
		c_name = data.country_name.toLowerCase();
		g_name = data.group_name.toLowerCase();

        if (data.business_group_name == null){
            bg_name = "";
        }
        else{
            bg_name = data.business_group_name.toLowerCase();
        }
        console.log("active:"+data.is_active)
		le_name = data.legal_entity_name.toLowerCase();
        if((data.validity_days < checkValidityDays() && data.validity_days > 0) && (data.is_active == true)){
            console.log("1:"+data.validity_days)
            data_is_active = false;
            data_closure = 2;
        }

        if(data.validity_days > checkValidityDays()){
            console.log(data.validity_days)
            data_closure = 1;
            data_is_active = false;
        }
		if (
	      (~c_name.indexOf(ctryname_search)) && (~g_name.indexOf(grpname_search)) &&
	      (~bg_name.indexOf(bgrpname_search)) && (~le_name.indexOf(lename_search)) &&
            ((closure_select == 'all') || (~closure_select.indexOf(data_closure)))
	    )
		{
            if ((status_select == 'all') || (Boolean(parseInt(status_select)) == data_is_active))
            {
                console.log("2:"+data.validity_days,g_name)
                searchList.push(data);

            }
		}
	}
    console.log(searchList.length)
	LegalEntityClosureData(searchList);
}

/*function bindSearchList(searchList)
{
	if(searchList.length > 0)
	{
		$('.tbody-le-closure-list').find('tr').remove();
		j = 1;

		for(var i=0;i<searchList.length;i++)
		{
			bindLegalEntityClosureData(searchList[i], j);
			j = j + 1;
		}
	}
}*/

function renderSearch() {
  // body...
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
    processFilterSearch();
  });

  Search_status_ul_1.click(function (event) {
    Search_status_li_1.each(function (index, el) {
      $(el).removeClass('active');
    });
    $(event.target).parent().addClass('active');

    var currentClass = $(event.target).find('i').attr('class');
    Search_status_1.removeClass();
    if(currentClass != undefined){
      Search_status_1.addClass(currentClass);
      Search_status_1.text('');
    }else{
      Search_status_1.addClass('fa');
      Search_status_1.text('All');
    }
    processFilterSearch();
  });
}

// page load
function initialize() {
    console.log("initialize")
    clearMessage();
    loadLegalEntityClosureList();
}

Search_status.change(function() {
    processFilterSearch();
});

Search_status_1.change(function() {
    processFilterSearch();
});

FilterBox.keyup(function() {
    processFilterSearch();
});

$(document).ready(function() {
    initialize();

    /*$(document).find('.js-filtertable').each(function() {
        $(this).filtertable().addFilter('.js-filter');
    });*/

    renderSearch();
});

