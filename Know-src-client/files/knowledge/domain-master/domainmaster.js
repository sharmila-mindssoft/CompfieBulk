
var ListContainer = $('.tbody-domain-list1');
var AddScreen = $("#domain-add");
var ViewScreen = $("#domain-view");
var AddButton = $("#btn-domain-add");
var CancelButton = $("#btn-domain-cancel");
var SubmitButton = $("#btn-submit");
var PasswordSubmitButton = $('#password-submit');

var CurrentPassword = $('#current-password');
var Remark = $('#remark');
var RemarkView = $('.remark-view');
var isAuthenticate;

var Country = $("#countryselected");
var MultiSelect_Country = $('#countries');
var Select_Box_Country = $('#selectboxview-country');
var Country_li_list = $('#ulist-country');
var Country_li_active = "active_selectbox_country";

var Domain_name = $("#domainname");
var Domain_id = $("#domainid");
var SearchDomain = $("#search-domain-name");

var Country_name = $("#countryname");
var SearchCountry = $("#search-country-name");

var Msg_pan = $(".error-message");
var d_page = null;
var item_selected = '';

var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

function displayLoader() {
  $('.loading-indicator-spin').show();
}
function hideLoader() {
  $('.loading-indicator-spin').hide();
}

function DomainPage() {
    this._CountryList = [];
    this._DomainList = [];
    this._country_ids = [];
}

DomainPage.prototype.possibleFailures = function(error) {
    if (error == "DomainNameAlreadyExists") {
        displayMessage(message.domainname_exists);
    }
    else if (error == 'InvalidDomainId') {
        displayMessage(message.invalid_domainid);
    }
    else if (error == 'InvalidPassword') {
        displayMessage(message.invalid_password);
    }
    else {
        displayMessage(error);
    }
};

DomainPage.prototype.popupWarning = function(message, callback) {
    var Warning_popup = $('.warning-confirm');
        Warning_popup.dialog({
        title: message.title_status_change,
        buttons: {
        Ok: function() {
            $(this).dialog('close');
            callback(true);
        },
        Cancel: function() {
            $(this).dialog('close');
            callback(false);
        }
        },
        open: function() {
        $('.warning-message').html(message);
        }
    });
};

DomainPage.prototype.showList = function() {
    AddScreen.hide();
    ViewScreen.show();
    Domain_id.val('');
    SearchDomain.val('');
    SearchCountry.val('');

    this.fetchDomain();
    Search_status.removeClass();
    Search_status.addClass('fa');
    Search_status.text('All');
};
DomainPage.prototype.showAddScreen = function() {
    ViewScreen.hide();
    AddScreen.show();
    Domain_id.val('');
    Domain_name.val('');
    this._country_ids = [];
    this.fetchCountryMultiselect();
    MultiSelect_Country.focus();
};
DomainPage.prototype.renderList = function(d_data) {
    t_this = this;
    var j =1;
    ListContainer.find('tr').remove();
    if(d_data.length == 0){
        $('.tbody-domain-list1').empty();
        var tableRow4 = $('#no-record-templates .table-no-content .table-row-no-content');
        var clone4 = tableRow4.clone();
        $('.no_records', clone4).text('No Records Found');
        $('.tbody-domain-list1').append(clone4);
    }else{
        $.each(d_data, function(k, v) {
            var cloneRow = $('#templates .table-domain-master .table-row').clone();
            $('.sno', cloneRow).text(j);

            var c_n = v.c_names.join(', ');

            $('.c_names', cloneRow).text(c_n);
            $('.domain-name', cloneRow).text(v.domain_name);

            $('.edit').attr('title', 'Click Here to Edit');
            $('.edit', cloneRow).addClass('fa-pencil text-primary');
            $('.edit', cloneRow).attr("onClick", "t_this.showEdit(" + v.domain_id + ",'" + v.domain_name + "','"+ v.country_ids +"')");

            if (v.is_active == true) {
                $('.status').attr('title', 'Click Here to Deactivate');
                $('.status', cloneRow).removeClass('fa-times text-danger');
                $('.status', cloneRow).addClass('fa-check text-success');
            } else {
                $('.status').attr('title', 'Click Here to Activate');
                $('.status', cloneRow).removeClass('fa-check text-success');
                $('.status', cloneRow).addClass('fa-times text-danger');
            }
            $('.status', cloneRow).attr("onClick", "showModalDialog(" + v.domain_id + "," + v.is_active + ")");
            ListContainer.append(cloneRow);
            j = j + 1;

        });
    }
    $('[data-toggle="tooltip"]').tooltip();
};

//Status Title
function showTitle(e){
  if(e.className == "fa c-pointer status fa-times text-danger"){
    e.title = 'Click Here to Activate';
  }
  else if(e.className == "fa c-pointer status fa-check text-success")
  {
    e.title = 'Click Here to Deactivate';
  }
}

//open password dialog
function showModalDialog(e, domainId, isActive){
    t_this = this;
    var passStatus = null;
    if (isActive == true) {
        passStatus = false;
        statusmsg = message.deactive_message;
    } else {
        passStatus = true;
        statusmsg = message.active_message;
    }
    CurrentPassword.val('');
    confirm_alert(statusmsg, function(isConfirm){
    if(isConfirm){
        Custombox.open({
        target: '#custom-modal',
        effect: 'contentscale',
        complete:   function() {
          CurrentPassword.focus();
          isAuthenticate = false;
        },
        close:   function() {
          if(isAuthenticate){
            t_this.changeStatus(domainId, passStatus);
          }
        },
      });
      e.preventDefault();
    }
  });
}

//validate
DomainPage.prototype.validateAuthentication = function() {
    t_this = this;
    var password = CurrentPassword.val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        CurrentPassword.focus();
        return false;
    } else if (validateMaxLength('password', password, "Password") == false) {
        return false;
    }
    displayLoader();
    mirror.verifyPassword(password, function(error, response) {
    if (error == null) {
        hideLoader();
        isAuthenticate = true;
        Custombox.close();
    }
    else {
        hideLoader();
        t_this.possibleFailures(error);
    }
  });
}

DomainPage.prototype.fetchDomain = function() {
    t_this = this;
    displayLoader();
    mirror.getDomainList(function (error, response) {
        if (error == null) {
            t_this._DomainList = response.domains;
            t_this._CountryList = response.countries
            t_this.renderList(t_this._DomainList);
            hideLoader();
        } else {
            hideLoader();
            t_this.possibleFailures(error);
        }
    });
};

DomainPage.prototype.fetchCountryMultiselect = function() {
    var str = '';
    for (var i in d_page._CountryList) {
        d = d_page._CountryList[i];
        if (d.is_active == true) {
            var selected = '';
            if ($.inArray(d.country_id, d_page._country_ids) >= 0)
                selected = ' selected ';
            else
                selected = '';
            str += '<option value="'+ d.country_id +'" '+ selected +'>'+ d.country_name +'</option>';
        }
    }
    MultiSelect_Country.html(str).multiselect('rebuild');
};

DomainPage.prototype.showEdit = function(d_id, d_name, d_country) {
    this.showAddScreen();
    Domain_name.val(d_name);
    Domain_id.val(d_id);
    this._country_ids = d_country;
    this.fetchCountryMultiselect();
};

DomainPage.prototype.changeStatus = function(d_id, status) {
    displayLoader();
    mirror.changeDomainStatus(d_id, status, function(error, response) {
        if (error == null) {
            if(status == 1)
                displaySuccessMessage(message.domain_active);
            else
                displaySuccessMessage(message.domain_deactive);
            t_this.showList();
            t_this.fetchDomain();
            hideLoader();
        }
        else {
            hideLoader();
            displayMessage(error);
        }
    });
};

DomainPage.prototype.validate = function() {

    if (MultiSelect_Country.val() == null) {
      displayMessage(message.country_required);
      MultiSelect_Country.focus();
      return false;
    }
    if (Domain_name.val().trim().length == 0) {
      displayMessage(message.domainname_required);
      Domain_name.focus();
      return false;
    } else {
      validateMaxLength('domainname', Domain_name.val(), "Domain name");
    }
    return true;
};

function DomainValidate() {
    if (MultiSelect_Country.val() == null) {
      displayMessage(message.country_required);
      MultiSelect_Country.focus();
      return false;
    }
    else if (Domain_name.val().trim().length == 0) {
      displayMessage(message.domainname_required);
      Domain_name.focus();
      return false;
    } else if(validateMaxLength('domainname', Domain_name.val(), "Domain name") == false){
        return false;
    }else{
        return true;
    }
}

DomainPage.prototype.submitProcess = function() {

    d_id = parseInt(Domain_id.val());
    name = Domain_name.val().trim();
    c_ids = MultiSelect_Country.val().map(Number);

    t_this = this;
    if (DomainValidate()) {
       if (Domain_id.val() == '') {
            displayLoader();
            mirror.saveDomain(name, c_ids, function(error, response) {
                if (error == null) {
                    displaySuccessMessage(message.domain_save_success);
                    t_this.showList();
                    hideLoader();
                } else {
                    hideLoader();
                    t_this.possibleFailures(error);
                }
            });
        } else {
            displayLoader();
            mirror.updateDomain(d_id, name, c_ids, function(error, response) {
                if (error == null) {
                    displaySuccessMessage(message.domain_update_success);
                    t_this.showList();
                    hideLoader();
                } else {
                    hideLoader();
                    t_this.possibleFailures(error);
                }
            });
        }
    }
};

function chkbox_select(item, id, name, active) {
    a_klass = Country_li_active;
    eveClick = "";
    li_string= ''
    if (active == true) {
        li_string  = '<li id="'+ id +'" class="'+ a_klass + '" onclick=list_click(this) >'+ name +'</li>';
    } else {
        li_string  = '<li id="'+ id +'" onclick=list_click(this) >'+ name +'</li>';
    }
    return li_string;
}

function list_click(element) {
    country_class = 'active_selectbox_country';

    klass = $(element).attr('class');
    if (klass == country_class) {
        $(element).removeClass(country_class);
        d_page._country_ids.splice(d_page._country_ids.indexOf(parseInt(element.id)));
    }
    else {
        $(element).addClass(country_class);
        d_page._country_ids.push(parseInt(element.id));
    }
    Country.val(d_page._country_ids.length + ' Selected');
}

function key_search(mainList) {
    d_key = SearchDomain.val().toLowerCase();
    c_key = SearchCountry.val().toLowerCase();
    d_status = $('.search-status-li.active').attr('value');
    var fList = [];
    for (var entity in mainList) {
        dName = mainList[entity].domain_name;
        cnames = mainList[entity].c_names;
        dStatus = mainList[entity].is_active;

        var flg = false;

        if (c_key.length == 0)  {
            flg = true;
        }
        else {
            for (var c in cnames) {
                if (~cnames[c].toLowerCase().indexOf(c_key)){
                    flg = true;
                    continue;
                }
            }
        }

        if ((~dName.toLowerCase().indexOf(d_key)) && flg == true) {
            if ((d_status == 'all') || (Boolean(parseInt(d_status)) == dStatus)){
                fList.push(mainList[entity]);
            }
        }


    }
    return fList
}

function PageControls() {
    function onKeyUpDownSelect(e, item) {
        // Key code : 40- down arrow , 38- up arrow , 32- space , 13- enter key.
        li_val = $('#' + item + ' li');
        function highlight_row(n_item) {
            li_val.removeClass('auto-selected');
            $('#' + item + ' li:eq('+ n_item + ')').addClass('auto-selected');
        }

        function remove_select(n_item, rklass) {
            $('#' + item + ' li:eq('+ n_item + ')').removeClass(rklass);
        }

        function add_select(n_item, aklass) {
            $('#' + item + ' li:eq('+ n_item + ')').addClass(aklass);
        }

        function get_id(n_item) {
            g_id = $('#' + item + ' li:eq('+ n_item + ')').attr('id');
            return g_id;
        }

        function get_class(n_item) {
            g_c = $('#' + item + ' li:eq('+ n_item + ')').attr('class');
            return g_c;
        }

        if(e.keyCode != 40 && e.keyCode != 38 && e.keyCode != 32) {
            item_selected = '';
        }
        if (e.keyCode == 13) {
            Select_Box_Country.hide()
        }

        if (e.keyCode == 40) {
            if(item_selected == '') {
                item_selected = 0;
            }
            else if (parseInt(item_selected) + 1 < li_val.length) {
                item_selected++;
            }
            highlight_row(item_selected);
            return false;
        }

        if (e.keyCode == 38) {
            if(item_selected == '') {
                item_selected = 0;
            }
            else if (item_selected > 0) {
                item_selected--;
            }
            highlight_row(item_selected);
            return false;
        }

        if (e.keyCode == 32) {
            remove_select(item_selected, 'auto-selected');
            var multi_select_id = parseInt(get_id(item_selected));
            var item_class = get_class(item_selected);

                // country select box
            if (item_class == Country_li_active) {
                remove_select(item_selected, Country_li_active);
                d_page._country_ids.splice(d_page._country_ids.indexOf(multi_select_id));
            }
            else {
                add_select(item_selected, Country_li_active);
                d_page._country_ids.push(multi_select_id);
            }
            Country.val(d_page._country_ids.length + ' Selected');
            return false;
        }
    }

    //status of the list
    Search_status_ul.click(function (event) {
        Search_status_li.each(function (index, el) {
          $(el).removeClass('active');
        });
        $(event.target).parent().addClass('active');

        var currentClass = $(event.target).find('i').attr('class');
        Search_status.removeClass();
        if(currentClass != undefined) {
          Search_status.addClass(currentClass);
          Search_status.text('');
        }else{
          Search_status.addClass('fa');
          Search_status.text('All');
        }
        fList = key_search(d_page._DomainList);
        d_page.renderList(fList);
    });

    Domain_name.keypress(function(e) {
        if (e.which == 13) {
            if (d_page.validate()) {
                d_page.submitProcess();
            }
        }
    });

    Country.keyup(function(e) {
        onKeyUpDownSelect(e, 'ulist-country');
    });

    $('.hideselect').mouseleave(function() {
        item_selected = '';
        Select_Box_Country.hide();
    });

    Domain_name.on('input', function(e) {
        this.value = isCommon_Name($(this));
    });

    SubmitButton.click(function() {
        if (d_page.validate()) {
            d_page.submitProcess();
        }
    });

    AddButton.click(function() {
        d_page.showAddScreen();
    });

    CancelButton.click(function() {
        d_page.showList();
    })

    SearchDomain.keyup(function() {
        fList = key_search(d_page._DomainList);
        d_page.renderList(fList);
    });

    SearchCountry.keyup(function() {
        fList = key_search(d_page._DomainList);
        d_page.renderList(fList);
    });

    PasswordSubmitButton.click(function() {
        d_page.validateAuthentication();
    });
}

d_page = new DomainPage();

$(document).ready(function() {
    MultiSelect_Country.multiselect({
        buttonWidth: '100%'
    });
    PageControls();
    d_page.showList();
});

