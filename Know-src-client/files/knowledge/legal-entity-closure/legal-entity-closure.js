var legalEntityClosureList;
var toggle_le_id = null;
var FilterBox = $('.filter-text-box');
var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

var Search_status_1 = $('#search-status-1');
var Search_status_ul_1 = $('.search-status-list-1');
var Search_status_li_1 = $('.search-status-li-1');

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

function loadLegalEntityClosureList() {
    function onSuccess(data) {
        legalEntityClosureList = data.legalentity_closure;
        LegalEntityClosureData(legalEntityClosureList);
    }

    function onFailure(error) {
        displayMessage(error);
    }
    displayLoader();
    mirror.getLegalEntityClosureData(function(error, response) {
        if (error == null) {
            onSuccess(response);
            hideLoader();
        } else {
            onFailure(error);
            hideLoader();
        }
    });
}

function LegalEntityClosureData(data) {
    var j = 1;
    $('.tbody-le-closure-list').find('tr').remove();
    if (data.length == 0) {
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        $('.tbody-le-closure-list').append(clone4);
      }
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

        if (val.is_active == false && val.validity_days <= checkValidityDays()) {
            $('#close', clone).css("display", "block");
            $('#close', clone).addClass('-' + val.legal_entity_id)
            $('#close', clone).on('click', function(e) {
                console.log("1:"+val.legal_entity_id)
                showModalDialog(e, val.legal_entity_id, 'close');
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
                $('#reactive', clone).on('click', function(e) {
                    showModalDialog(e, val.legal_entity_id, 'reactive');
                });
                day_left = checkValidityDays() - parseInt(val.validity_days);
                $('#reactive', clone).attr('title', day_left + ' days left')
                $('.closed', clone).hide();
                $('.closed', clone).text('');
                $('.status', clone).text('In Active');
                //break;
            }
        }

        $('.tbody-le-closure-list').append(clone);
        j++;
    });
}
//open password dialog
function showModalDialog(e, leId, mode){
    console.log("2:"+leId)
    $(".popup_legal_entity_id").val(le_id);
    $(".popup_mode").val(mode);
    $('#techno_pwd').val('');
    $('#remarks').val('');
    $('#techno_pwd').focus();
    if (mode == "close")
        statusmsg = message.le_close;
    else
        statusmsg = message.le_activate;
    confirm_alert(statusmsg, function(isConfirm){
        if(isConfirm){
            Custombox.open({
                target: '#custom-modal',
                effect: 'contentscale',
                complete:   function() {
                  $('#techno_pwd').focus();
                  isAuthenticate = false;
                },
                close:   function()
                {
                    if(isAuthenticate)
                    {
                        popup_toggle(leId, mode);
                    }
                },
            });
            e.preventDefault();
        }
  });
}

function popup_toggle(le_id, mode) {
    console.log("3:"+le_id)
    $(".popup_legal_entity_id").val(le_id);
    $(".popup_mode").val(mode);
    /////////////save
    var txtpwd = $('#techno_pwd').val();
    var txtRemarks = $('#remarks').val();
    var le_id, action_mode;
    //if (validateAuthentication() == true) {
    //le_id = $(".popup_legal_entity_id").val();
    //action_mode = $(".popup_mode").val();
    console.log("4:"+le_id)
    function onSuccess(data) {
        if (mode == "close")
            displaySuccessMessage(message.legal_entity_closed);
        else if (mode == "reactive")
            displaySuccessMessage(message.legal_entity_reactivated);
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
    displayLoader();
    mirror.saveLegalEntityClosureData(txtpwd, txtRemarks, parseInt(le_id), mode, function(error, response) {
        console.log(error, response)
        if (error == null) {
            $(".popup_legal_entity_id").val('');
            $(".popup_mode").val('');
            onSuccess(response);
            hideLoader();
        } else {
            onFailure(error);
            hideLoader();
        }
    });
}

//validate password
function validateAuthentication(){
  var password = $('#techno_pwd').val().trim();
  var txtRemarks = $('#remarks').val();
  var remarks
  if (password.length == 0) {
    displayMessage(message.password_required);
    $('#techno_pwd').focus();
    return false;
  } else if (validateMaxLength('password', password, "Password") == false){
    return false;
  } else if(txtRemarks == ""){
    displayMessage(message.reason_required);
    $('#remarks').focus();
    return false;
  } else if(validateMaxLength("remark", txtRemarks, "Reason") == false) {
        return false;
    } else {
        isAuthenticate = true;
        Custombox.close();
        return true;
    }

}

$('#update_status').click(function() {
    validateAuthentication();
    //}
});

function processFilterSearch()
{
	ctryname_search = $('#search-country-name').val().toLowerCase();
	grpname_search = $('#search-Group-name').val().toLowerCase();
	bgrpname_search = $('#search-business-group').val().toLowerCase();
	lename_search = $('#search-legal-entity').val().toLowerCase();
    var status_select = $('.search-status-li.active').attr('value');
    var closure_select = $('.search-status-li-1.active').attr('value');
    var data_is_active = false;
    var data_closure = 0;
	searchList = [];
    console.log("1:"+closure_select, status_select)
	for(var v in legalEntityClosureList)
	{
        data_is_active = false;
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
		le_name = data.legal_entity_name.toLowerCase();
        if((data.validity_days <= checkValidityDays()) && (data.is_active == false)){
            data_is_active = true;
            data_closure = 1;
        }
        if(data.validity_days > checkValidityDays()){
            data_closure = 2;
            data_is_active = false;
        }
		if (
	      (~c_name.indexOf(ctryname_search)) && (~g_name.indexOf(grpname_search)) &&
	      (~bg_name.indexOf(bgrpname_search)) && (~le_name.indexOf(lename_search)) &&
            ((closure_select == 'all') || (~closure_select.indexOf(data_closure))) &&
            ((status_select == 'all') || (Boolean(parseInt(status_select)) == data_is_active))
	    )
		{
            searchList.push(data);
		}
	}
	LegalEntityClosureData(searchList);
}

function renderSearch() {
  // body...
  //status of the list
  Search_status_ul.click(function (event) {
    Search_status_li.each(function (index, el) {
      $(el).removeClass('active');
    });
    $(event.target).parent().addClass('active');

    /*var currentClass = $(event.target).find('i').attr('class');
    Search_status.removeClass();
    if(currentClass != undefined){
      Search_status.addClass(currentClass);
      Search_status.text('');
    }else{
      Search_status.addClass('fa');
      Search_status.text('All');
    }*/
    var currentClass = $(event.target).html();
    Search_status.html(currentClass);

    processFilterSearch();
  });

  Search_status_ul_1.click(function (event) {
    Search_status_li_1.each(function (index, el) {
      $(el).removeClass('active');
    });
    $(event.target).parent().addClass('active');

    var currentClass = $(event.target).html();
    Search_status_1.html(currentClass);
    /*Search_status_1.removeClass();
    if(currentClass != undefined){
      Search_status_1.addClass(currentClass);
      Search_status_1.text('');
    }else{
      Search_status_1.addClass('fa');
      Search_status_1.text('All');
    }*/
    processFilterSearch();
  });
}

// page load
function initialize() {
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

