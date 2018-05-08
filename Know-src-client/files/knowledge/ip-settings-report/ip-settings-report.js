
var btnShow = $('.btn-show');
var btnExport = $('.btn-export');

var IPAddress = $('#ip-address');
var GroupVal = $('#groupval');
var Group = $('#group');
var ACGroup = $('#ac-group');

var CLIENT_GROUPS = '';
var FORMS_LIST = '';

var GROUP_IPS_LIST = '';
var form_map = {};
var group_map = {};

//Pagination variable declaration
var ItemsPerPage = $('#items_per_page');
var PaginationView = $('.pagination-view');
var Pagination = $('#pagination-rpt');
var CompliacneCount = $('.compliance_count');
var on_current_page = 1;
var sno = 0;
var totalRecord;

//Other variable declaration
var ReportView = $('.grid-table-rpt');

function initialize(){
    $(".details").hide();
    clearFields();
    
    function onSuccess(data) {
        FORMS_LIST = data.ip_setting_forms;
        CLIENT_GROUPS = data.client_groups;
        generateMaps();
        //loadList();
    }
    function onFailure(error) {
        displayMessage(error);
    }
    mirror.getIPSettingsReportFilter(function (error, response) {
        if (error == null) {
            onSuccess(response);
        } else {
            onFailure(error);
        }
    });
}


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
                getResult(false);
            }
        }
    });
};

function clearFields(){
    GroupVal.val("");
    Group.val("");
    form_map = {};
}

function generateMaps(){
    $.each(FORMS_LIST, function(key, value){
        form_map[value.form_id] = value.form_name
    });

    $.each(CLIENT_GROUPS, function(key, value){
        group_map[value.client_id] = value.group_name
    });
}

function getResult(csv){
    displayLoader();
    var g_id = null;
    var ip_address = null;
    var t_count = parseInt(ItemsPerPage.val());;
    if(Group.val() != ''){
        g_id = parseInt(Group.val());
    }
    if(IPAddress.val() != ''){
        ip_address = IPAddress.val();
    }


    if (on_current_page == 1) {
      sno = 0
    }
    else {
      sno = (on_current_page - 1) *  t_count;
    }

    t_count = sno + t_count;
    mirror.getIPSettingsReport(g_id, ip_address, (sno + 1), t_count, csv, function (error, response) {
        if (error == null) {

            if (csv) {
                hideLoader();
                var download_url = response.link;
                window.open(download_url, '_blank');
            } else {
                GROUP_IPS_LIST = response.group_ips_list;
                totalRecord = response.total_records;

                if (totalRecord == 0) {
                    var no_record_row = $("#templates .table-no-record tr");
                    var clone = no_record_row.clone();
                    $(".tbody-form-list").append(clone);
                    PaginationView.hide();
                    ReportView.show();
                    hideLoader();
                } else {
                    hideLoader();
                    if(sno==0){
                      createPageView(totalRecord);
                    }
                    PaginationView.show();
                    ReportView.show();
                    loadForms();
                }
            }

        } else {
            displayMessage(error);
        }
    });
}

//retrive  autocomplete value
function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
}

function pageControls() {

    btnShow.click(function(){
        $(".tbody-form-list").empty();
        on_current_page = 1;
        $('.details').show();
        $('#compliance_animation')
          .removeClass().addClass('bounceInLeft animated')
          .one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function(){
          $(this).removeClass();
        });

        getResult(false);
    });

    btnExport.click(function(){
        getResult(true);
        //saveIPSettings();
    });

    //load group list in autocomplete text box
    GroupVal.keyup(function(e) {
        var text_val = $(this).val();
        commonAutoComplete(
            e, ACGroup, Group, text_val,
            CLIENT_GROUPS, "group_name", "client_id",
            function(val) {
                onAutoCompleteSuccess(GroupVal, Group, val);
        });
    });

    ItemsPerPage.on('change', function (e) {
        perPage = parseInt($(this).val());
        sno = 0;
        on_current_page = 1;
        createPageView(totalRecord);
        getResult(false);
    });

    IPAddress.on('input', function(e) {
        //this.value = isNumbers_Dot_Comma($(this));
        isNumbers_Dot_Comma(this);
    });
}


function loadForms(){
    var lastGroup = '';
    $(".tbody-form-list").empty();

    var showFrom = sno + 1;
    var is_null = true;

    var g_row = $("#templates .table-form-list .table-row-head");
    $.each(GROUP_IPS_LIST, function(key, value){
        if(lastGroup != group_map[value.client_id]){
            is_null = false;
            sno++;
            var clone = g_row.clone();
            $(".sno", clone).text(sno);
            $('.group-name', clone).attr('href', '#collapse'+sno);
            $(".group-name", clone).text(group_map[value.client_id]);
            $(".tbody-form-list").append(clone);

            var c_row = $("#templates .table-form-list .table-row-child");
            var c_clone = c_row.clone();
            c_clone.attr('id', 'collapse'+sno);
            c_clone.find('tbody').addClass('tbody-iplist-'+sno);
            $(".tbody-form-list").append(c_clone);

            lastGroup = group_map[value.client_id];
        }

        var f_row = $("#templates .table-form-list .table-row-forms");
        var f_clone = f_row.clone();
        $(".form-name", f_clone).text(form_map[value.form_id]);
        $(".ip-address", f_clone).text(value.ip);
        $(".tbody-iplist-"+sno).append(f_clone);
    });

    if (is_null == true) {
      hidePagePan();
    }
    else {
      showPagePan(showFrom, sno, totalRecord);
    }
    hideLoader();
}

//initialization
$(function () {
  initialize("list");
  pageControls();
  loadItemsPerPage();
});
