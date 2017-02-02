var unitClosureList;
var LegalEntityList;
var toggle_le_id = null;
var LegalEntityId = null;

var leSelect = $('#legal_entity_option');

var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

var Search_status_1 = $('#search-status-1');
var Search_status_ul_1 = $('.search-status-list-1');
var Search_status_li_1 = $('.search-status-li-1');


function loadLegalEntities(){
	var obj_le = $(".le-drop-down option");
    var clone_le = obj_le.clone();
    clone_le.attr("value", 0);
    clone_le.text("Select");
    leSelect.append(clone_le);
	$.each(LegalEntityList, function(key, value) {
        var lentityId = value.legal_entity_id;
        var lentityName = value.legal_entity_name;

        var obj = $(".le-drop-down option");
        var clone = obj.clone();
        clone.attr("value", lentityId);
        clone.text(lentityName);
        leSelect.append(clone);
    });
}

$('.btn-show').click(function() {
	LegalEntityId = leSelect.val();
    console.log("le:"+LegalEntityId)

	if(LegalEntityId != ''){
		function onSuccess(data) {
	        unitClosureList = data.unit_closure_units;
	        LoadUnitClosureUnits(unitClosureList);
	    }

	    function onFailure(error) {
	        displayMessage(error);
	    }
	    client_mirror.getUnitClosureUnitList(parseInt(LegalEntityId), function(error, response) {
	        if (error == null) {
	            onSuccess(response);
	        } else {
	            onFailure(error);
	        }
	    });
	}
	else{
		displayMessage(message.legalentity_required);
	}
});

function LoadUnitClosureUnits(data){
	var j = 1;
    $('.tbody-unit-closure-list').empty();
    $.each(data, function(k, val) {
        var tableRow = $('#templates .table-row');
        var clone = tableRow.clone();
        $('.sno', clone).text(j);
        $('.Business-group', clone).text(val.business_group_name);
        $('.legal-entity', clone).text(val.legal_entity_name);
        $('.division-name', clone).text(val.division_name);
        if(val.category_name == "---")
            $('.category-name', clone).text();
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
            $('#close', clone).on('click', function() {
                Custombox.open({
                    target: '#custom-modal',
                    effect: 'contentscale',
                    open: function() {
                        popup_toggle(val.unit_id, 'close');
                    }
                });

            });
            //$('.modal')
            $('#reactive', clone).css("display", "none");
            $('.closed', clone).css("display", "none");
            $('.closed', clone).text('');
            //break;
        } else {
            if (parseInt(val.validity_days) > 30) { //isclose=0=close
                $('#close', clone).hide();
                $('#reactive', clone).hide();
                $('.closed', clone).css("display", "block");
                $('.closed', clone).text('Closed');
                //break;
            } else {
                $('#close', clone).hide();
                $('#reactive', clone).css("display", "block");
                $('#reactive', clone).addClass('-' + val.unit_id)
                $('#reactive', clone).on('click', function() {
                Custombox.open({
                        target: '#custom-modal',
                        effect: 'contentscale',
                        complete: function() {
                            $('#client_pwd').focus();
                            popup_toggle(val.unit_id, 'reactive');
                        }
                    });
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

function popup_toggle(unit_id, mode) {
    $(".popup_unit_id").val(unit_id);
    $(".popup_mode").val(mode);
    //console.log("e--------"+e);
    //var split_e_le_id = e.split("-")[2].trim();
    //$('.modal').show();
    $('#client_pwd').val('');
    $('#remarks').val('');
    //toggle_le_id = split_e_le_id+","+mode;
    //alert(toggle_le_id);
}

$('#update_status').click(function() {
    var txtpwd = $('#client_pwd').val();
    var txtRemarks = $('#remarks').val();
    var unit_id, action_mode;
    if (txtpwd != '' && txtRemarks != '') {
        unit_id = $(".popup_unit_id").val();
        action_mode = $(".popup_mode").val();

        function onSuccess(data) {
            displaySuccessMessage(message.action_success);
            loadUnitClosureList();
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
        client_mirror.saveUnitClosureData(txtpwd, txtRemarks, parseInt(unit_id), action_mode, function(error, response) {
            if (error == null) {
                Custombox.close();
                $(".popup_unit_id").val('');
                $(".popup_mode").val('');
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    } else {
        if (txtpwd == '') {
            displayMessage(message.enter_password);
        } else {
            displayMessage(message.remarks_required);
        }
    }
});

function processFilterSearch()
{
	var status_select = $('.search-status-li.active').attr('value');
    var closure_select = $('.search-status-li-1.active').attr('value');
    var data_is_active = false;
    var data_closure = -1;
	searchList = [];
    i =0;
    console.log("1:"+status_select,closure_select)
	for(var v in unitClosureList)
	{
        data_closure =-1;
		data = unitClosureList[v];
        data_is_active = data.is_active;

        if((data_is_active == false) && (parseInt(data.validity_days) <= 30)){
            console.log(data.unit_id)
            data_closure = 0;
            i++;
            //data_is_active = true;
        }


		if((data.validity_days < 30 && data.validity_days >= 0) && (data_is_active == true)){
            console.log("1:"+data.validity_days)
            //data_is_active = false;
            data_closure = 2;
        }

        if(data.validity_days > 30){
            data_closure = 1;
            //data_is_active = false;
        }
        console.log("2:"+data_closure)
        console.log("3:"+(closure_select == data_closure));
        if(
        	((closure_select == 'all') || (closure_select == data_closure))
    	)
        {
            if ((status_select == 'all') || (Boolean(parseInt(status_select)) == data_is_active))
            {
                searchList.push(data);
                console.log(searchList.length, data_closure, data.unit_id)
            }
        }
	}
	console.log(searchList.length)
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
    $('.tbody-unit-closure-list').empty();
    LegalEntityList = client_mirror.getUserLegalEntity();
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

    $(document).find('.js-filtertable').each(function() {
        $(this).filtertable().addFilter('.js-filter');
    });

    renderSearch();
});