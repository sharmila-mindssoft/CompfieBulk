var categoryList;

var addScreen = $("#add-screen");
var viewScreen = $("#list-screen");
var addButton = $("#btn-add");
var cancelButton = $("#cancelButton");
var btnSubmit = $('#btnSubmit');

// select box
var ddlUserCategory = $('#ddlUserCategory');

var um_page = null;

userManagementPage = function() {
    this._userManagementList = [];
    categoryList = response.user_groups;
}

//Load User Categories
function loadUserCategories() {
    ddlUserCategory.empty();
    ddlUserCategory.append($('<option></option>').val('').html('Select'));
    $.each(CategoryList, function(key, value) {
        ddlUserCategory.append($('<option></option>').val(CategoryList[key].user_category_id).html(CategoryList[key].user_category_name));
    });
}

userManagementPage.prototype.showAddScreen = function() {
    t_this = this;
    viewScreen.hide();
    addScreen.show();
    //txtServiceProviderName.focus();
};

//Page Control Events
PageControls = function() {
    //Add Button Click Event
    addButton.click(function() {
        um_page.showAddScreen();
    });
}

um_page = new userManagementPage();

$(document).ready(function() {
    PageControls();
    um_page.showList();
});