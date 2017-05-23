var unitClosureList;
var LegalEntityList;
var toggle_le_id = null;
var LegalEntityId = null;
var _entities = [];
var leSelect = $('#legal_entity_option');
var LegalEntityNameLabel = $(".legal-entity-name");

var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

var Search_status_1 = $('#search-status-1');
var Search_status_ul_1 = $('.search-status-list-1');
var Search_status_li_1 = $('.search-status-li-1');


function loadLegalEntities(){
    if(_entities.length > 1){
        LegalEntityNameLabel.hide();
        leSelect.show();
        var obj_le = $(".le-drop-down option");
        var clone_le = obj_le.clone();
        clone_le.attr("value", 0);
        clone_le.text("Select");
        leSelect.append(clone_le);
        $.each(LegalEntityList, function(key, value) {
            var lentityId = value.le_id;
            var lentityName = value.le_name;

            var obj = $(".le-drop-down option");
            var clone = obj.clone();
            clone.attr("value", lentityId);
            clone.text(lentityName);
            leSelect.append(clone);
        });
    }else{
        le_name = _entities[0]["le_name"];
        LegalEntityId = _entities[0]["le_id"];
        LegalEntityNameLabel.show();
        leSelect.hide();
        LegalEntityNameLabel.text(le_name);
    }
}

$('.btn-show').click(function() {
    $('.js-filter').val('');
    if (LegalEntityNameLabel.attr('style').indexOf("display: block") >= 0)
        LegalEntityId = LegalEntityId;
    else
	   LegalEntityId = leSelect.val();
	if(LegalEntityId != '' && LegalEntityId != 0){
		function onSuccess(data) {
	        unitClosureList = data.unit_closure_units;
	        LoadUnitClosureUnits(unitClosureList);
	    }

	    function onFailure(error) {
	        displayMessage(error);
	    }
        displayLoader();
	    client_mirror.getUnitClosureUnitList(parseInt(LegalEntityId), function(error, response) {
	        if (error == null) {
	            onSuccess(response);
	        } else {
	            onFailure(error);
	        }
            hideLoader();
	    });
	}
	else{
		displayMessage(message.legalentity_required);
	}
});

function LoadUnitClosureUnits(data){
	var j = 1;
    $('.tbody-unit-closure-list').empty();
    if (data.length == 0){
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        $('.tbody-unit-closure-list').append(clone4);
    }else {
        $.each(data, function(k, val) {
            var tableRow = $('#templates .table-row');
            var clone = tableRow.clone();
            $('.sno', clone).text(j);
            if(val.business_group_name == null || val.business_group_name == "")
                $('.Business-group', clone).text("-");
            else
                $('.Business-group', clone).text(val.business_group_name);
            $('.legal-entity', clone).text(val.legal_entity_name);
            if(val.division_name == "---" || val.division_name == null || val.division_name == "")
            {
                $('.division-name', clone).text("-");
            }
            else
                $('.division-name', clone).text(val.division_name);
            if(val.category_name == "---" || val.category_name == null || val.category_name == "")
                $('.category-name', clone).text("-");
            else
                $('.category-name', clone).text(val.category_name);
            $('#unit_id', clone).addClass('-' + val.unit_id);
            var unit_addr = val.address+", "+val.postal_code;
            var unit_ctrl = "<i class='zmdi zmdi-info address-title' data-toggle='tooltip' title='"+unit_addr+"'></i>&nbsp;&nbsp;"+val.unit_code+" - "+val.unit_name;
            $('.unit-name', clone).append($.parseHTML(unit_ctrl));
            $('.unit_id', clone).text(val.unit_id);
            if(val.is_active == true){
                $('.status', clone).text('In Active');
            }
            else{
                $('.status', clone).text('Active');
            }

            if ((val.is_active == false) && (parseInt(val.validity_days) <= 30)){
                $('#close', clone).css("display", "block");
                $('#close', clone).addClass('-' + val.unit_id)
                $('#close', clone).on('click', function(e) {
                    showModalDialog(e, val.unit_id, 'close');
                });
                //$('.modal')
                $('#reactive', clone).css("display", "none");
                $('.closed', clone).css("display", "none");
                $('.closed', clone).text('');
                //break;
            } else {
                if (parseInt(val.validity_days) > 30 && val.is_active == true) { //isclose=1
                    $('#close', clone).hide();
                    $('#reactive', clone).hide();
                    $('.closed', clone).css("display", "block");
                    $('.closed', clone).text('Closed');
                    //break;
                } else if (parseInt(val.validity_days) <= 30 && val.is_active == true){
                    $('#close', clone).hide();
                    $('#reactive', clone).css("display", "block");
                    $('#reactive', clone).addClass('-' + val.unit_id)
                    $('#reactive', clone).on('click', function(e) {
                        showModalDialog(e, val.unit_id, 'reactive');
                    });
                    val_days = 30 - parseInt(val.validity_days);
                    $('#reactive', clone).attr('title', val_days + ' days left')
                    $('.closed', clone).hide();
                    $('.closed', clone).text('');
                    //break;
                }
            }

            $('.tbody-unit-closure-list').append(clone);
            j++;
        });
    }
}

//open password dialog
function showModalDialog(e, unitId, mode){
    $(".popup_unit_id").val(unitId);
    $(".popup_mode").val(mode);
    $('#client_pwd').val('');
    $('#remarks').val('');
    $('#client_pwd').focus();
    if (mode == "close")
        statusmsg = message.unit_close;
    else
        statusmsg = message.unit_activate;
    confirm_alert(statusmsg, function(isConfirm){
        if(isConfirm){
            Custombox.open({
                target: '#custom-modal',
                effect: 'contentscale',
                complete:   function() {
                  $('#client_pwd').focus();
                  isAuthenticate = false;
                },
                close:   function()
                {
                    if(isAuthenticate)
                    {
                        popup_toggle(unitId, mode);
                    }
                },
            });
            e.preventDefault();
        }
  });
}

function popup_toggle(unit_id, mode) {
    $(".popup_unit_id").val(unit_id);
    $(".popup_mode").val(mode);
    var txtpwd = $('#client_pwd').val();
    var txtRemarks = $('#remarks').val();
    if (LegalEntityNameLabel.attr('style').indexOf("display: block") >= 0)
        LegalEntityId = LegalEntityId;
    else
       LegalEntityId = leSelect.val();
    function onSuccess(data) {
        if (mode == "close")
            displaySuccessMessage(message.unit_closed);
        else if (mode == "reactive")
            displaySuccessMessage(message.unit_reactivated);
        $('.js-filter').val('');
        $('.btn-show').trigger( "click" );
        //loadUnitClosureList();
    }

    function onFailure(error) {
        if(error == "InvalidPassword") {
            displayMessage(message.invalid_password);
            return false;
        }
        else if(error == "InvalidCurrentPassword"){
            displayMessage(message.invalid_password);
            return false;
        }
        else{
            displayMessage(error);
        }
    }
    client_mirror.saveUnitClosureData(parseInt(LegalEntityId), txtpwd, txtRemarks, parseInt(unit_id), mode, function(error, response) {
        console.log(error, response)
        if (error == null) {
            $(".popup_unit_id").val('');
            $(".popup_mode").val('');
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}

//validate password
function validateAuthentication(){
    var password = $('#client_pwd').val().trim();
    var txtRemarks = $('#remarks').val();
    var remarks
    if (password.length == 0) {
        displayMessage(message.password_required);
        $('#client_pwd').focus();
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
});

function processFilterSearch()
{
	var status_select = $('.search-status-li.active').attr('value');
    var closure_select = $('.search-status-li-1.active').attr('value');
    var data_is_active = false;
    var data_closure = -1;
	searchList = [];
    i =0;
	for(var v in unitClosureList)
	{
        data_closure =-1;
		data = unitClosureList[v];
        data_is_active = data.is_active;

        if((data_is_active == false) && (parseInt(data.validity_days) <= 30)){
            data_closure = 0;
            i++;
            //data_is_active = true;
        }


		if((data.validity_days < 30 && data.validity_days >= 0) && (data_is_active == true)){
            //data_is_active = false;
            data_closure = 2;
        }

        if(data.validity_days > 30){
            data_closure = 1;
            //data_is_active = false;
        }
        if(
        	((closure_select == 'all') || (closure_select == data_closure))
    	)
        {
            if ((status_select == 'all') || (Boolean(parseInt(status_select)) == data_is_active))
            {
                searchList.push(data);
            }
        }
	}
	LoadUnitClosureUnits(searchList);
}

function renderSearch() {
  // body...
  //status of the list
  Search_status_ul.click(function (event) {
    Search_status_li.each(function (index, el) {
      $(el).removeClass('active');
    });
    $(event.target).parent().addClass('active');
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
    processFilterSearch();
  });
}

// page load
function initialize() {
    clearMessage();
    $('.tbody-unit-closure-list').empty();
    LegalEntityList = user.entity_info;
    _entities = client_mirror.getSelectedLegalEntity();
    loadLegalEntities();
}

Search_status.change(function() {
    processFilterSearch();
});

Search_status_1.change(function() {
    processFilterSearch();
});


$(document).ready(function() {
    initialize();
    $('.js-filter').val('');
    $(document).find('.js-filtertable').each(function() {
        $(this).filtertable().addFilter('.js-filter');
    });

    renderSearch();
});
