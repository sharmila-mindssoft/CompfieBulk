var le_count = 0;
var edit_id = null;
var organization_details = {};
var country_domain_id_map = {};
var selected_textbox = '';
var selected_textid = '';
var logoFile = [];
var industry_id_map = {};
var industry_name_map = {};
var legal_entity_id_map = {};
var country_name_map = {};
var domain_name_map = {};
var business_group_name_map = {};
var industries_temp = [];
var domain_temp = [];
var le_name_duplicate_check_temp = [];

var COUNTRIES = '';
var DOMAINS = '';
var INDUSTRIES = '';
var GROUPNAME = '';
var USERNAME = '';
var SHORTNAME = '';
var VIEW_LICENCE = '';
var BUSSINESSGROUPS = '';
var LEGALENTITIES = '';
var DATECONFIGURATIONS = '';
var IS_APPROVED = '';
var SELECTED_ACTION = '';
var temp_i = 1;
var orgid_temp = [];

var FilterBox = $('.filter-text-box');

var Search_status = $('#search-status');
var Search_status_ul = $('.search-status-list');
var Search_status_li = $('.search-status-li');

var Search_astatus = $('#search-astatus');
var Search_astatus_ul = $('.search-astatus-list');
var Search_astatus_li = $('.search-astatus-li');


function initialize(type_of_initialization) {
    showPage(type_of_initialization);
    if (type_of_initialization == "list") {
        clearForm();

        function onSuccess(data) {
            GROUPS = data.groups;
            loadGroups(GROUPS);
        }

        function onFailure(error) {
            displayMessage(error);
        }
        mirror.getClientGroups(function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    } else if (type_of_initialization == "add") {
        showHideAddEditFields("add");

        function onSuccess(data) {
            COUNTRIES = data.countries;
            DOMAINS = data.domains;
            INDUSTRIES = data.industries;
            $.each(INDUSTRIES, function(key, value) {
                industry_id_map[value.industry_name] = parseInt(value.industry_id)
                industry_name_map[parseInt(value.industry_id)] = value.industry_name
            });
            $("#group-text").focus();
            $(".edit-date-config").hide();
            $(".email-edit-icon").hide();
            $(".portlet-title").html("Add Client");
            $(".cm-header").removeClass("col-sm-4");
            $(".cm-header").addClass("col-sm-6");
            $("#view-licence-text").removeClass("width-50px");
            addClient();
            $(".add-le").show();
        }

        function onFailure(error) {
            displayMessage(error);
        }
        mirror.getClientGroupFormData(function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });

    } else if (type_of_initialization == "edit") {
        showHideAddEditFields("edit");

        function onSuccess(data) {
            COUNTRIES = data.countries;
            DOMAINS = data.domains;
            INDUSTRIES = data.industries;
            BUSSINESSGROUPS = data.business_groups;
            GROUPNAME = data.group_name
            USERNAME = data.email_id
            SHORTNAME = data.short_name
            VIEW_LICENCE = data.no_of_licence
            LEGALENTITIES = data.legal_entities_list
            DATECONFIGURATIONS = data.date_configurations
            generateMaps();
            $(".portlet-title").html("Edit Client");
            $("#view-licence-text").addClass("width-50px");
            editClient();
        }

        function onFailure(error) {
            displayMessage(error);
        }
        mirror.getEditClientGroupFormData(edit_id, function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
    } else {
        // Invalid initialization Do nothing
    }
}

function showHideAddEditFields(type) {
    if (type == "add") {
        $(".action-div").hide();
        $(".remarks-div").hide();
        $(".edit-right-icon").hide();
    } else {
        $(".action-div").show();
        $(".remarks-div").show();
        $(".edit-right-icon").show();
    }
}

function showPage(type_of_initialization) {
    le_count = 0;
    organization_details = {};
    logoFile = [];
    country_domain_id_map = {};
    clearMessage();
    BUSINESSGROUPS = '';
    if (type_of_initialization == "list") {
        edit_id = null;
        $('.le-body').empty();
        $("#group-text").val("");
        $("#username").val("");
        $("#username").attr("readonly", false);
        $('.tbody-dateconfiguration-list').empty();
        $("#clientgroup-view").show();
        $("#clientgroup-add").hide();
    } else {
        if (type_of_initialization == "add") {
            edit_id = null;
            $("#username").attr("readonly", false);
        }
        $("#clientgroup-view").hide();
        $("#clientgroup-add").show();
    }
}

function generateMaps() {
    $.each(COUNTRIES, function(key, value) {
        if (value.is_active == true) {
            country_name_map[value.country_id] = value.country_name;
        }
    });
    $.each(DOMAINS, function(key, value) {
        if (value.is_active == true) {
            domain_name_map[value.domain_id] = value.domain_name;
        }
    });
    $.each(INDUSTRIES, function(key, value) {
        if (value.is_active == true) {
            industry_id_map[value.industry_name] = parseInt(value.industry_id)
            industry_name_map[parseInt(value.industry_id)] = value.industry_name
        }
    });
    $.each(BUSSINESSGROUPS, function(key, value) {
        business_group_name_map[value.business_group_id] = value.business_group_name
    });
}

function clearForm() {
    $("#group-text").parent().find("span").remove();
    $("#group-text").show();
    $("#group-text").val("");
    $("#view-licence-text").parent().find("span").remove();
    $("#view-licence-text").show();
    $("#view-licence-text").val("");
    $("#shortname").parent().find("span").remove();
    $("#shortname").show();
    $("#shortname").val("");
    $("#username").parent().find("span").remove();
    $("#username").show();
    $("#username").val("");
    SELECTED_ACTION = '';
    edit_id = '';
    IS_APPROVED = '';
}

/*
    Handling List
*/

function loadGroups(response) {
    $('.tbody-clientgroup-list').empty();
    var sno = 0;
    if (response == "") {
        data = GROUPS;
    } else {
        data = response;
    }
    var LastGroup = '';
    var actCount = 1;
    if (data.length == 0) {
        $("#accordion").html("<center>No Record Found.</center>");
    }
    $.each(data, function(key, value) {
        var clientId = value.group_id;
        var isActive = value.is_closed;
        var passStatus = null;
        var statusValue = null;
        if (isActive == true) {
            statusValue = 'InActive';
        } else {
            statusValue = 'Active';
        }

        if (LastGroup != value.group_name) {
            sno = 0;
            var acttableRow = $('#act-templates .p-head');
            var clone = acttableRow.clone();

            $('.acc-title', clone).attr('id', 'heading' + actCount);
            $('.panel-title a span', clone).text(value.group_name);
            $('.panel-title a', clone).attr('href', '#collapse' + actCount);
            $('.panel-title a', clone).attr('aria-controls', 'collapse' + actCount);
            if (actCount == 1) { //For First group open collapse
                $('.panel-title a', clone).attr('aria-expanded', true);
                $('.panel-title a', clone).removeClass('collapsed');
                $('.coll-title', clone).addClass('in');
            }

            $('.coll-title', clone).attr('id', 'collapse' + actCount);
            $('.coll-title', clone).attr('aria-labelledb', 'heading' + actCount);

            $('.edit-icon', clone).attr('title', 'Edit');
            $('.edit-icon', clone).attr('id', clientId);
            $('.edit-icon', clone).on('click', function() {
                edit_id = parseInt($(this).attr('id'));
                IS_APPROVED = value.is_approved;
                initialize("edit");
            });

            $('.tbody-clientgroup-list').append(clone);

            LastGroup = value.group_name;
            actCount = actCount + 1;
            /*$('.filter-text-box').keyup(function() {
                processFilter();
            });*/
        }

        var le_tableRow = $('#le-value .table-le-values .le-details');
        var clone_le = le_tableRow.clone();
        sno = sno + 1;
        $('.sno', clone_le).text(sno);
        $('.countryname', clone_le).text(value.country_name);
        $('.legalentityname', clone_le).text(value.legal_entity_name);
        $('.status', clone_le).text(statusValue);

        if (value.is_approved == 0) {
            $('.approvalstatus', clone_le).text("Pending");
        } else if (value.is_approved == 1) {
            $('.approvalstatus', clone_le).text("Approved");
        } else {
            var abbr_clone = $(".tooltip-templates .text-with-tooltip").clone();
            abbr_clone.attr("data-original-title", value.remarks);
            abbr_clone.attr("title", value.remarks);
            clone_le.css("color", "#f00");
            abbr_clone.html('<i class="fa fa-info-circle"></i> Rejected');
            $('.approvalstatus', clone_le).html(abbr_clone);
        }
        $(' #collapse' + (actCount - 1) + ' .tbody-le-list').append(clone_le);


    });
    $('.js-filtertable').each(function() {
        $(this).filtertable().addFilter('.js-filter');
    });
}

function validateAuthentication() {
    var password = $(".popup-password").val().trim();
    if (password.length == 0) {
        displayMessage(message.password_required);
        $(".popup-password").focus();
        return false;
    }
    mirror.verifyPassword(password, function(error, response) {
        if (error == null) {
            changeClientStatus();
            $(".popup-group-id").val("");
            $(".popup-pass-value").val("");
        } else {
            if (error == 'InvalidPassword') {
                displayMessage(message.invalid_password);
            }
        }
    });
}
/*
  Handling Button Clicks
*/
$(".btn-clientgroup-add").click(function() {
    displayLoader();
    initialize("add");
    hideLoader();
});
$(".add-business-group").click(function() {
    addOrSelectBusinessGroup("add", this, 0);
});
$(".cancel-add-business-group").click(function() {
    addOrSelectBusinessGroup("cancel", this, 0);
});
// $(".cancel-add-business-group").click(function() {
//     addOrSelectBusinessGroup("cancel");
// });
$(".add-le").click(function() {
    addClient();
});
$(".save").click(function() {
    saveClient();
});
$(".cancel").click(function() {
    initialize("list");
});
$(".org-submit").click(function() {
    saveOrganization();
});
$(".org-cancel, .close").click(function() {
    //closePopup();
    e.preventDefault();
    Custombox.close();
});
$(".add-organization").click(function() {
    addOrganization();
});
/*
    Handling Save or Update
*/

function saveOrganization() {
    var org_count = $("#o-cnt").val();
    var le_cnt = $("#le-cnt").val();
    var d_cnt = $("#d-cnt").val();
    for (var i = 1; i <= org_count; i++) {
        var org_selected_class = "org-selected-" + le_cnt + "-" + d_cnt + "-" + i;
        var org_id_class = "industry-" + le_cnt + "-" + d_cnt + "-" + i;
        var selected_org = $("." + org_selected_class).val();
        var selected_id = $("." + org_id_class).val();
        var no_of_units_class = "no-of-units-" + le_cnt + "-" + d_cnt + "-" + i
        var no_of_units = $("." + no_of_units_class).val();
        if ($(".organization-list .form-group").find("." + org_selected_class).length) {
            if (selected_org == '' || selected_org == null) {
                displayMessage(message.organization_required);
                organization_details = {};
                break;
            } else if (selected_id == '' || selected_id == null) {
                displayMessage(message.organization_invalid);
                organization_details = {};
                break;
            } else if (no_of_units == '' || no_of_units == 0 || no_of_units == '0') {
                displayMessage(message.no_of_units_required);
                organization_details = {};
                break;
            } else if (isNaN(no_of_units)) {
                displayMessage(message.no_of_units_invalid);
                organization_details = {};
                break;
            } else {
                if (!(le_cnt in organization_details)) {

                    organization_details[le_cnt] = {}
                }
                if (!(d_cnt in organization_details[le_cnt])) {

                    organization_details[le_cnt][d_cnt] = {}
                }
                if (selected_org in organization_details[le_cnt][d_cnt]) {
                    displayMessage(message.duplicate_industry);
                    organization_details = {};
                    break;
                } else {
                    organization_details[le_cnt][d_cnt][parseInt(industry_id_map[selected_org])] = parseInt(no_of_units);
                    clearMessage();
                    Custombox.close();
                }
            }
        }
    }
    console.log("save o d:--" + JSON.stringify(organization_details));
    //console.log("save o d:--"+organization_details.toSource());

}

$('.numeric').keypress(function(e) {
    var theEvent = e || window.event;
    var key = theEvent.keyCode || theEvent.which;
    if (key === 9) { //TAB was pressed
        return;
    }

    var regex = new RegExp("^[0-9|\b]+$");
    var str = String.fromCharCode(!e.charCode ? e.which : e.charCode);
    if (regex.test(str)) {
        return true;
    }
    e.preventDefault();
    return false;
});

function saveClient() {
    le_name_duplicate_check_temp = [];
    var group_id = [edit_id];
    var group_name = $('#group-text').val();
    var username = $("#username").val();
    var short_name = $("#shortname").val();
    var no_of_view_licence = $("#view-licence-text").val();
    if (group_name == '') {
        displayMessage(message.group_required);
        $('#group-text').focus();
    } else if (group_name.length > 50) {
        displayMessage(message.group_50);
        $('#group-text').focus();
    } else if (short_name == '') {
        displayMessage(message.short_name_required);
        $("#shortname").focus();
    } else if (short_name.length <= 2) {
        displayMessage(message.shortname_min3char);
        $("#shortname").focus();
    } else if (short_name.length > 20) {
        displayMessage(message.shortname_20);
        $("#shortname").focus();
    } else if (no_of_view_licence == '') {
        displayMessage(message.no_of_view_licence_required);
        $("#view-licence-text").focus();
    } else if (username == '') {
        displayMessage(message.emailid_required);
        $("#username").focus();
    } else if (username.length > 50) {
        displayMessage(message.email_50);
        $("#username").focus();
    } else if (validateEmail(username) == '') {
        displayMessage(message.invalid_emailid);
        $("#username").focus();
    } else {
        var is_valid = false
        var legal_entities = [];
        for (var i = 1; i <= le_count; i++) {
            var le_table = $(".le-table-" + i);
            var domains = [];
            var country_id = le_table.find(".country").val();
            var business_group_id = null;
            var business_group_name = null;
            business_group_id = le_table.find(".business-group").val();
            business_group_name = le_table.find(".business-group-text").val().trim();
            var le_name = le_table.find("#legal_entity_text").val();
            var uploadlogo = le_table.find('#upload-logo').val();

            var logo = logoFile[i - 1];

            if (logo) {

                if (typeof logo == 'string') {
                    var ext = logo.split('.').pop().toLowerCase();
                } else {
                    var ext = logo.file_name.split('.').pop().toLowerCase();
                }
            }
            var licenceVal = le_table.find('#no-of-user-licence').val();
            var fileSpaceVal = le_table.find('#file-space').val();
            var contractFromVal = le_table.find('.contract-from').val();
            var contractToVal = le_table.find('.contract-to').val();
            var domain_count = le_table.find('.domain-count').val();
            var edited = le_table.find('.edited').val();
            var d = new Date();
            var month = d.getMonth() + 1;
            var day = d.getDate();
            var output = d.getFullYear() + '/' + month + '/' + day;
            var currentDate = new Date(output);
            var convertDate = null;

            // if (contractToVal != '') {
            //     convertDate = convert_date(contractToVal);
            // }
            if (country_id == 0 || country_id == '0' || country_id == null) {
                displayMessage(message.country_required);
                break;
            } else if (le_name == '') {
                displayMessage(message.legalentity_required);
                break;
            } else if (jQuery.inArray(le_name, le_name_duplicate_check_temp) !== -1) {
                displayMessage(message.duplicate_legalentity + ":" + le_name);
                break;
            } else if (le_name.length > 50) {
                displayMessage(message.le_50);
                break;
            } else if (contractFromVal == '') {
                displayMessage(message.contractfrom_required);
                break;
            } else if (contractToVal == '') {
                displayMessage(message.contractto_required);
                break;
            }
            // else if (convertDate != null && convertDate < currentDate) {
            //     displayMessage(message.invalid_contractto);
            //     break;
            // }
            else if (licenceVal == '') {
                displayMessage(message.licence_required);
                break;
            } else if (licenceVal == '0' || licenceVal == '1') {
                displayMessage(message.licence_invalid);
                break;
            } else if (isNaN(licenceVal)) {
                displayMessage(message.licence_invalid);
                break;
            } else if (licenceVal.length > 3) {
                displayMessage(message.licence_max3);
                break;
            } else if (fileSpaceVal == '') {
                displayMessage(message.filespace_required);
                break;
            } else if (fileSpaceVal == '0') {
                displayMessage(message.filespace_invalid);
                break;
            } else if (!$.isNumeric(fileSpaceVal)) {
                displayMessage(message.filespace_invalid);
                break;
            } else if (fileSpaceVal.length > 3) {
                displayMessage(message.filespace_max3);
                break;
            } else if (domain_count <= 0) {

                displayMessage(message.domain_required + " for " + le_name);
                break;
            } else {
                if (uploadlogo != '') {
                    if ($.inArray(ext, ['gif', 'png', 'jpg', 'jpeg']) == -1) {
                        displayMessage(message.logo_invalid + " for " + le_name + ". " + message.logo_valid_file_format);
                        break;
                    }
                }
                var inner_is_valid = false;
                var domain_ids = []
                for (var j = 1; j <= domain_count; j++) {
                    var domain_id = $(".domain-" + i + "-" + j + " option:selected").val();
                    var activationdate = $(".activationdate-" + i + "-" + j).val();
                    if (domain_ids.indexOf(domain_id) > -1) {
                        displayMessage(message.duplicate_domain + " for " + le_name);
                        break;
                    } else if (domain_id == 0 || domain_id == '0' || domain_id == null) {
                        displayMessage(message.domain_required + " for1 " + le_name);
                        break;
                    } else if (activationdate == "") {
                        displayMessage(message.activationdate_required + " for " + le_name);
                        break;
                    } else if (!(i in organization_details)) {
                        console.log(i + "-> i not in " + JSON.stringify(organization_details));
                        displayMessage(message.organization_required + " for " + le_name);
                        break;
                    } else if (!(j in organization_details[i])) {
                        console.log(j + "->j not in " + JSON.stringify(organization_details[i]));
                        displayMessage(message.organization_required + " for " + le_name);
                        break;
                    } else if (Object.keys(organization_details[i][j]).length <= 0) {
                        console.log(organization_details[i][j].length + " <= 0");
                        displayMessage(message.organization_required + " for " + le_name);
                        break;
                    } else if (j == domain_count) {
                        inner_is_valid = true;
                    }
                    domain_ids.push(domain_id);
                    domains.push(
                        mirror.getDomainRow(
                            parseInt(domain_id), activationdate, organization_details[i][j]
                        )
                    )
                }
                if (inner_is_valid == false) {
                    break;
                }
            }
            if (i == le_count) {
                is_valid = true
            }
            legal_entity_id = legal_entity_id_map[i]
            var new_logo = null;
            if (typeof legal_entity_id == 'string' || typeof legal_entity_id == 'number') {
                legal_entity_id = legal_entity_id;
            } else {
                legal_entity_id = null;
            }
            if (edit_id == null) {
                if (logo == '' || logo == null) {
                    logo = null;
                }
                le_name_duplicate_check_temp.push(le_name);
                legal_entities.push(
                    mirror.getLegalEntityRow(
                        parseInt(country_id), parseInt(business_group_id), business_group_name,
                        le_name, logo, parseInt(licenceVal), parseInt(fileSpaceVal),
                        contractFromVal, contractToVal, domains
                    )
                )
            } else {
                if (edited != 0) {
                    var new_logo = null;
                    if (typeof logo == 'string') {
                        new_logo = null;
                    } else {
                        if (typeof logo != "undefined") {
                            new_logo = logo;
                            logo = null;
                        } else {
                            new_logo = null;
                            logo = null;
                        }

                    }
                    le_name_duplicate_check_temp.push(le_name);
                    legal_entities.push(
                        mirror.getLegalEntityUpdateRow(
                            parseInt(country_id), parseInt(business_group_id),
                            business_group_name, legal_entity_id, le_name,
                            logo, new_logo, parseInt(licenceVal),
                            parseInt(fileSpaceVal), contractFromVal,
                            contractToVal, domains
                        )
                    );
                }

            }

        }
        if (is_valid == true) {
            date_configurations = []
            $.each(country_domain_id_map, function(key, value) {
                var country_id = key;
                $.each(value["domain_names"], function(name_key, name_value) {
                    var domain_id = value["domains"][name_key];
                    var from = $('.tl-from-' + country_id + '-' + domain_id).val();
                    var to = $('.tl-to-' + country_id + '-' + domain_id).val();
                    date_configurations.push(
                        mirror.getDateConfigurations(
                            parseInt(country_id), parseInt(domain_id),
                            parseInt(from), parseInt(to)
                        )
                    )
                });
            });
            if (edit_id == null) {
                callSaveClientApi(
                    group_name, username, short_name, parseInt(no_of_view_licence),
                    legal_entities, date_configurations
                );
            } else {
                if ($("#remarks-text").val() != "") {
                    remarks = $("#remarks-text").val();
                } else {
                    remarks = null;
                }
                callUpdateClientApi(
                    edit_id, group_name, username, short_name, parseInt(no_of_view_licence), remarks,
                    legal_entities, date_configurations
                );
            }

        }
    }
}

function callSaveClientApi(
    group_name, username, short_name, no_of_view_licence, legal_entities, date_configurations
) {
    clearMessage();
    displayLoader();

    function onSuccess(data) {
        hideLoader();
        displaySuccessMessage(message.client_save_success);
        initialize("list");
    }

    function onFailure(error) {
        hideLoader();
        if (error == "GroupNameAlreadyExists") {
            displayMessage(message.groupname_exists);
        } else if (error == "GroupShortNameAlreadyExists") {
            displayMessage(message.groupshortname_exists);
        } else {
            displayMessage(error);
        }

    }
    mirror.saveClientGroup(group_name, username, short_name, no_of_view_licence,
        legal_entities, date_configurations,
        function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        }
    );
}

function callUpdateClientApi(
    group_id, group_name, username, short_name, no_of_view_licence, remarks,
    legal_entities, date_configurations
) {
    clearMessage();
    displayLoader();

    function onSuccess(data) {
        hideLoader();
        displaySuccessMessage(message.client_update_success);
        initialize("list");
    }

    function onFailure(error) {
        hideLoader();
        displayMessage(error);
    }
    mirror.updateClientGroup(group_id, group_name, username, short_name, no_of_view_licence, remarks,
        legal_entities, date_configurations,
        function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        }
    );
}

// function convert_date(data) {
//     var date = data.split('-');
//     var months = [
//         'Jan',
//         'Feb',
//         'Mar',
//         'Apr',
//         'May',
//         'Jun',
//         'Jul',
//         'Aug',
//         'Sep',
//         'Oct',
//         'Nov',
//         'Dec'
//     ];
//     for (var j = 0; j < months.length; j++) {
//         if (date[1] == months[j]) {
//             date[1] = months.indexOf(months[j]) + 1;
//         }
//     }
//     if (date[1] < 10) {
//         date[1] = '0' + date[1];
//     }
//     return new Date(date[2], date[1] - 1, date[0]);
// }

/*
  Handling Add & Edit
*/

function showNonEditable(element, id, value) {
    element.hide();
    if (element.attr("type") != "file") {
        if (id != null)
            element.val(id);
        else
            element.val(value);
    }
    // for File Space Alignment
    var forfile = element.selector.split(/[, ]+/).pop();
    if (forfile == "#file-space") {
        $("#file-space abbr").show();
    }

    var clone = $(".text span").clone()
    clone.html(value);
    element.parent().find("span").remove();
    element.parent().prepend(clone);
}

function showEditable(element, value) {
    element.parent().find("span").remove();
    if (element.attr("type") != "file") {
        element.val(value);
    }
    element.show();
}

$(".email-edit-icon").on("click", function() {
    if ($(".email-edit-icon i").hasClass("fa-pencil")) {
        showEditable($("#username"), USERNAME);
        showEditable($("#view-licence-text"), VIEW_LICENCE);
        $(".email-edit-icon i").addClass("fa-times");
        $(".email-edit-icon i").removeClass("fa-pencil");
    } else {
        showNonEditable($("#username"), null, USERNAME);
        showNonEditable($("#view-licence-text"), null, VIEW_LICENCE);
        $(".email-edit-icon i").removeClass("fa-times");
        $(".email-edit-icon i").addClass("fa-pencil");
    }

});

function editClient() {
    $(".cm-header").removeClass("col-sm-6");
    $(".cm-header").addClass("col-sm-4");
    showNonEditable($("#group-text"), null, GROUPNAME);
    showNonEditable($("#username"), null, USERNAME);
    $("#username").val(USERNAME);
    showNonEditable($("#shortname"), null, SHORTNAME);
    showNonEditable($("#view-licence-text"), null, VIEW_LICENCE);
    $("#view-licence-text").val(VIEW_LICENCE);
    loadActions();
    $(".input-notes").hide();
    $('.email-edit-icon').show();
    $(".help-block").hide();
    $("br").hide();
    le_count = 0
    logoFile = [];
    legal_entity_id_map = {}
    organization_details = {}
    $('.le-body').empty();
    $.each(LEGALENTITIES, function(key, value) {
        domain_temp = [];
        addClient();
        legal_entity_id_map[parseInt(le_count)] = value.legal_entity_id;
        showNonEditableEntityDetails(le_count, value, value.domain_details, true)
    });
    $(".edit-date-config").show();
    generateDateConfigurationList();
    $.each(DATECONFIGURATIONS, function(key, value) {
        var country_id = value.country_id
        var domain_id = value.domain_id
        showNonEditable(
            $('.tl-from-' + country_id + '-' + domain_id), value.month_from,
            month_id_name_map[value.month_from]
        );
        showNonEditable(
            $('.tl-to-' + country_id + '-' + domain_id), value.month_to,
            month_id_name_map[value.month_to]
        );
    });
}


function showNonEditableEntityDetails(le_count, value, domain_details, push_in_array) {
    console.log("welcome to showNonEditableEntityDetails");
    var le_table = $(".le-table-" + le_count);
    showNonEditable(le_table.find(".country"), value.country_id, country_name_map[value.country_id]);
    le_table.find(".edit-right-icon").show();
    le_table.find(".edited").val(0);
    addOrSelectBusinessGroup("cancel", this, le_count);
    le_table.find(".addbg").hide();
    le_table.find("add-business-group").hide();
    if (value.business_group) {
        showNonEditable(
            le_table.find(".business-group"), parseInt(value.business_group.business_group_id),
            business_group_name_map[value.business_group.business_group_id]
        );
        le_table.find(".business-group").val(value.business_group.business_group_id);
    } else {
        showNonEditable(le_table.find(".business-group"), null, '');
    }

    showNonEditable(le_table.find("#legal_entity_text"), null, value.legal_entity_name);
    showNonEditable(le_table.find("#no-of-user-licence"), null, value.no_of_licence);
    showNonEditable(le_table.find("#file-space"), null, value.file_space);
    showNonEditable(le_table.find(".contract-from"), null, value.contract_from);
    showNonEditable(le_table.find(".contract-to"), null, value.contract_to);

    le_table.find("#upload-logo-img").hide();
    if (value.old_logo != null) {
        name_array = value.old_logo.split("-");
        ext_array = name_array[1].split(".");
        old_logo_name = name_array[0] + "." + ext_array[ext_array.length - 1]
    } else {
        old_logo_name = null;
    }
    showNonEditable(le_table.find("#upload-logo"), null, old_logo_name);
    console.log("old_logo_name-" + old_logo_name);
    if (old_logo_name == null) {
        le_table.find("#upload-logo-img").hide();
    }

    if (push_in_array == true) {
        logoFile.push(value.old_logo);
    } else {
        logoFile.push('');
    }
    le_table.find(".edit-right-icon").on("click", function(e) {
        //displayLoader();
        console.log("welcome to editEntity--"+temp_i);
        temp_i++;
        editEntity(this, le_count, value, value.domain_details);
        //hideLoader();
        //e.preventDefault();
        //return false;
    });
    //le_table.find(".edit-right-icon").attr('onClick', 'editEntity('+le_count+', '+value+', '+value.domain_details+');');
    //le_table.find(".edit-right-icon").attr('onClick', 'editEntity('+le_count+', value, value.domain_details);');
    var domain_list_class = "domain-list-" + le_count;
    var domain_count_class = "domain-count-" + le_count;
    var domain_table_class = "domain-table-" + le_count;
    $(".add-domain").hide();
    $('.' + domain_list_class).empty();
    $("." + domain_count_class).val(0);
    for (var i = 1; i <= domain_details.length; i++) {
        var domain_class = "domain-" + le_count + "-" + i
        addDomain(domain_list_class, domain_count_class, le_count)
        showNonEditable(
            $("." + domain_class), value.domain_details[i - 1].d_id,
            domain_name_map[value.domain_details[i - 1].d_id]
        );
        orgs = value.domain_details[i - 1].org
        organization_details[le_count] = {}
        organization_details[le_count][i] = orgs
        organization_text = ""
        $.each(orgs, function(key, value) {
            organization_text += industry_name_map[key] + " - " + value + " Units\n <br />";
        });
        var organization_class = "addOrganizationType-" + le_count + "-" + i;
        showNonEditable(
            $("." + organization_class), null, organization_text
        );
        showNonEditable(
            $("." + domain_list_class).find(".remove-domain"), null, ""
        );
        // showNonEditable(
        //     $("." + domain_list_class).find(".remove-domain"), null, ""
        // );
        showNonEditable(
            $("." + domain_table_class).find(".remove-domain-heading"), null, ""
        );

        var activationdate_class = ".activationdate-" + le_count + "-" + i;
        $(activationdate_class).removeClass('hasDatepicker').removeAttr('id');
        $(activationdate_class).val(value.domain_details[i - 1].activation_date);

        showNonEditable(
            $(activationdate_class), null, value.domain_details[i - 1].activation_date
        );

    }
    // le_table.find('.org-header').text("Activation Date");
    // le_table.find('.org-header').attr("width", "20%");
    // le_table.find('.remove-header').text("Organization");
    // le_table.find('.remove-header').attr("width", "45%");
    le_table.find(".edit-right-icon").attr("src", "/images/icon-edit.png");
    le_table.find(".edit-right-icon i").removeClass("fa-times");
    le_table.find(".edit-right-icon i").addClass("fa-pencil");
    if (value.is_closed == true) {
        le_table.find(".edit-right-icon").hide();
    }
    console.log("End of episode");
    return false;
}

function loadActions() {
    $(".actions select").empty();
    $("#remarks-text").val("");
    actions = [];
    actions = ["Edit", "Renewal", "Amendment"];
    // if (IS_APPROVED == 0) {
    //     actions = ["Edit", "Renewal"];
    // } else if (IS_APPROVED == 1) {
    //     actions = ["Renewal", "Amendment"];
    // } else if (IS_APPROVED == 2) {
    //     actions = ["Edit", "Renewal", "Amendment"];
    // }
    $.each(actions, function(key, value) {
        var clone = $(".select-option option").clone();
        clone.text(value);
        var key_position = 0;
        if (value == "Renewal") key_position = 1;
        else if (value == "Amendment") key_position = 2;
        clone.val(key_position);
        $(".actions select").append(clone);
    });
    if (SELECTED_ACTION != '') {
        $(".actions select").val(SELECTED_ACTION)
    }
}

$(".actions select").change(function() {
    SELECTED_ACTION = $(".actions select").val()
    if (SELECTED_ACTION == 2) {
        $(".remarks-div").hide();
    } else {
        $(".remarks-div").show();
    }
    if (SELECTED_ACTION == 1) {
        $(".add-le").hide();
    } else {
        $(".add-le").show();
    }

    editClient();
});

function editEntity(e, le_count, value, domain_details) {
    var le_table = $(".le-table-" + le_count);
    // image = le_table.find(".edit-right-icon i").hasClass("fa-times"); //.split("?")[0].split("/")
    // image_name = image[image.length - 1];
    // if (image) {
    if (image_name == "icon-edit.png") {
        var image = le_table.find(".edit-right-icon").attr("src").split("?")[0].split("/");
        var image_name = image[image.length-1];
        selected_action = $(".actions select").val();
        if (selected_action == 1) {
            showEditable(le_table.find(".contract-from"), value.contract_from);
            showEditable(le_table.find(".contract-to"), value.contract_to);
            le_table.find(".edit-right-icon").attr("src", "/images/delete-icon-black.png");
            le_table.find(".edit-right-icon i").removeClass("fa-pencil");
            le_table.find(".edit-right-icon i").addClass("fa-times");
        } else {
            //showEditable(le_table.find(".country"), value.country_id);
            //le_table.find(".addbg").show();
            // if (value.business_group) {
            //     console.log("value.business_group.business_group_id--"+value.business_group.business_group_id);
            //     showEditable(le_table.find(".business-group"), value.business_group.business_group_id);
            // }
            le_table.find(".input_business_group").show();
            le_table.find(".cancel-add-business-group").hide();
            le_table.find(".select_business_group").hide();

            if (value.business_group) {
                showEditable(le_table.find(".business-group-text"), value.business_group.business_group_name);
            }

            le_table.find(".edited").val(1);
            showEditable(le_table.find("#legal_entity_text"), value.legal_entity_name);
            showEditable(le_table.find("#no-of-user-licence"), value.no_of_licence);
            showEditable(le_table.find("#file-space"), value.file_space);
            if (value.is_approved == 1) {
                showNonEditable(le_table.find(".contract-from"), null, value.contract_from);
                showNonEditable(le_table.find(".contract-to"), null, value.contract_to);
                $(".domain-" + le_count).hide();
            } else {
                showEditable(le_table.find(".contract-from"), value.contract_from);
                showEditable(le_table.find(".contract-to"), value.contract_to);
                $(".domain-" + le_count).show();
            }
            showEditable(le_table.find("#upload-logo"), value.old_logo);


            le_table.find("#upload-logo").show();
            img_clone = $(".logo-img span").clone();
            le_table.find("#upload-logo").parent().append(img_clone);
            if (logoFile[le_count - 1] != null) {
                le_table.find("#upload-logo-img").attr("src", "http://" + window.location.host + "/knowledge/clientlogo/" + logoFile[le_count - 1]);
            }
            if (value.old_logo == null) {
                le_table.find("#upload-logo-img").hide();
            } else {
                le_table.find("#upload-logo-img").show();
            }
            //$(".domain-"+le_count).show();
            var domain_list_class = "domain-list-" + le_count;
            var domain_count_class = "domain-count-" + le_count;
            $('.' + domain_list_class).empty();
            $("." + domain_count_class).val(0);
            for (var i = 1; i <= domain_details.length; i++) {
                var domain_class = "domain-" + le_count + "-" + i
                addDomain(domain_list_class, domain_count_class, le_count)
                showEditable($("." + domain_class), value.domain_details[i - 1].d_id);
                var activationdate_class = "activationdate-" + le_count + "-" + i
                showEditable($("." + activationdate_class), value.domain_details[i - 1].activation_date);
                orgs = value.domain_details[i - 1].org;
                organization_details[le_count][i] = orgs;
            }
            // le_table.find('.org-header').text("Organization");
            // le_table.find('.org-header').attr("width", "45%");
            // le_table.find('.remove-header').text("Remove");
            // le_table.find('.remove-header').attr("width", "10%");
            le_table.find(".edit-right-icon").attr("src", "/images/delete-icon-black.png");
            //le_table.find(".edit-right-icon i").removeClass("fa-times");
            //le_table.find(".edit-right-icon i").addClass("fa-pencil");
            le_table.find(".edit-right-icon i").removeClass("fa-pencil");
            le_table.find(".edit-right-icon i").addClass("fa-times");
            console.log("end of episode of icon-edit");


        }
    }
    if(image_name == "delete-icon-black.png") {
        console.log("welcome to delete-icon-black");
        le_table.find(".edit-right-icon").prop('onclick',null).off('click');
        showNonEditableEntityDetails(le_count, value, domain_details, false);
    }
}

$(".edit-username-viewlicence").click(function() {
    if ($(".actions select").val() == 0 || $(".actions select").val() == 2) {
        var image = $(".edit-username-viewlicence").attr("src").split("?")[0].split("/");
        var image_name = image[image.length - 1];
        if (image_name == "icon-edit.png") {
            showEditable($("#username"), USERNAME);
            showEditable($("#view-licence-text"), VIEW_LICENCE);
            // $(".edit-username-viewlicence").attr("src", "/images/delete-icon-black.png");
            $(".edit-username-viewlicence").removeClass("fa-pencil");
            $(".edit-username-viewlicence").addClass("fa-times");
        } else {
            showNonEditable($("#username"), null, USERNAME);
            showNonEditable($("#view-licence-text"), null, VIEW_LICENCE);
            // $(".edit-username-viewlicence").attr("src", "/images/icon-edit.png");
            $(".edit-username-viewlicence").removeClass("fa-pencil");
            $(".edit-username-viewlicence").addClass("fa-times");
        }
    }
});

$(".edit-date-config").click(function() {
    if ($(".actions select").val() == 0 || $(".actions select").val() == 2) {
        var image = $(".edit-date-config").attr("src").split("?")[0].split("/");
        var image_name = image[image.length - 1];
        if (image_name == "icon-edit.png") {
            $.each(DATECONFIGURATIONS, function(key, value) {
                var country_id = value.country_id
                var domain_id = value.domain_id
                showEditable(
                    $('.tl-from-' + country_id + '-' + domain_id), value.month_from
                );
                showEditable(
                    $('.tl-to-' + country_id + '-' + domain_id), value.month_to
                );
            });
            $(".edit-date-config").attr("src", "/images/delete-icon-black.png");
            $(".edit-date-config").find("i").addClass("fa-times");
            $(".edit-date-config").find("i").removeClass("fa-pencil");
        } else {
            $.each(DATECONFIGURATIONS, function(key, value) {
                var country_id = value.country_id
                var domain_id = value.domain_id
                showNonEditable(
                    $('.tl-from-' + country_id + '-' + domain_id), value.month_from,
                    month_id_name_map[value.month_from]
                );
                showNonEditable(
                    $('.tl-to-' + country_id + '-' + domain_id), value.month_to,
                    month_id_name_map[value.month_to]
                );
            });
            $(".edit-date-config").attr("src", "/images/icon-edit.png");
            $(".edit-date-config").find("i").removeClass("fa-times");
            $(".edit-date-config").find("i").addClass("fa-pencil");
        }
    }
});

function addClient() {

    var le_row = $('.legal-entity-config-template .grid-table');
    var clone = le_row.clone();
    le_count++;
    clone.find(".contract-from")
        .removeClass('hasDatepicker')
        .removeAttr('id')
        .datepicker({
            changeMonth: false,
            changeYear: false,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
            ],
            onClose: function(selectedDate) {
                $(".contract-to", clone).datepicker("option", "minDate", selectedDate);
            }
        });
    clone.find(".contract-to")
        .removeClass('hasDatepicker')
        .removeAttr('id')
        .datepicker({
            changeMonth: false,
            changeYear: false,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
            ],
            onClose: function(selectedDate) {
                $(".contract-from", clone).datepicker("option", "maxDate", selectedDate);
            }
        });
    $(".le-no", clone).val(le_count);
    $('.le-body').prepend(clone);

    var le_table_class = "le-table-" + le_count
    $('.letable', clone).addClass(le_table_class);
    $(".edited", clone).val(1);

    var country_class = "country-" + le_count
    $('.country', clone).addClass(country_class);
    loadCountries(country_class);


    var bg_class = "bg-" + le_count
    $(".business-group", clone).find('option').remove()
    $(".business-group", clone).addClass(bg_class);
    //loadBusinessGroups(bg_class);

    var contractfrom_class = "contract-from-" + le_count
    $('.contract-from', clone).addClass(contractfrom_class);


    var contractto_class = "contract-to-" + le_count
    $('.contract-to', clone).addClass(contractto_class);

    $('#upload-logo', clone).change(function(e) {
        if ($(this).val != '') {
            mirror.uploadFile(e, le_count, function result_data(data, le_count) {
                if (
                    data != 'File max limit exceeded' ||
                    data != 'File content is empty' ||
                    data != 'Invalid file format'
                ) {
                    logoFile[le_count - 1] = data;
                } else {
                    custom_alert(data);
                }
            });
        }
    });
    $("#file-space abbr").show();
    $(".edit-right-icon", clone).hide();
    $(".add-domain").show();
    var add_domain_class = "domain-" + le_count;
    var domain_list_class = "domain-list-" + le_count;
    var domain_count_class = "domain-count-" + le_count;
    var domain_table_class = "domain-table-" + le_count;
    $(".add-domain", clone).addClass(add_domain_class);
    $(".domain-list", clone).addClass(domain_list_class);
    $(".domain-count", clone).addClass(domain_count_class);
    $(".domain-table", clone).addClass(domain_table_class);
    $("." + domain_count_class).val(0);
    $("." + add_domain_class).click(function() {
        addDomain(domain_list_class, domain_count_class, le_count);
    });
    addDomain(domain_list_class, domain_count_class, le_count);
    $('.country', clone).on("change", function() {
        loadBusinessGroups(bg_class);
        //organization_details[le_count] = {};
        loadDomainsforcountry(parseInt($(this).val()), "domain-" + le_count, $("." + domain_count_class).val());
    });

}


function onAutoCompleteSuccess(value_element, id_element, val) {
    value_element.val(val[1]);
    id_element.val(val[0]);
    value_element.focus();
}

function addOrganization() {

    var le_cnt = $("#le-cnt").val();
    var d_cnt = $("#d-cnt").val();
    var o_cnt = $("#o-cnt").val();
    $("#o-cnt").val(++o_cnt);
    var org_row = $('.organization-template .org-row');
    var clone = org_row.clone();

    var org_class = "org-" + le_cnt + "-" + d_cnt + "-" + o_cnt
    $(".org", clone).addClass(org_class)

    var org_selected_class = "org-selected-" + le_cnt + "-" + d_cnt + "-" + o_cnt
    $('#orgselected', clone).addClass(org_selected_class);

    var ac_class = "ac-industry-" + le_cnt + "-" + d_cnt + "-" + o_cnt;
    $("#ac-industry", clone).addClass(ac_class);

    var val_class = "industry-" + le_cnt + "-" + d_cnt + "-" + o_cnt;
    $("#industry", clone).addClass(val_class);

    var no_of_units_class = "no-of-units-" + le_cnt + "-" + d_cnt + "-" + o_cnt;
    $(".no-of-units", clone).addClass(no_of_units_class);

    var org_list_class = "org-list-" + le_cnt + "-" + d_cnt + "-" + o_cnt
    $("#ulist-org", clone).addClass(org_list_class);
    $(".remove-organisation", clone).click(function(e) {
        e.preventDefault();
        $(this).parent().parent().remove();
    });

    var domainid = $(".domain-" + le_cnt + "-" + d_cnt).val();

    $(".organization-list").append(clone);

    $('.' + org_selected_class).keyup(function(e) {
        industries_temp = [];
        var condition_fields = [];
        var condition_values = [];
        if (domainid != '') {
            condition_fields.push("domain_id");
            condition_values.push(parseInt(domainid));
            condition_fields.push("is_active");
            condition_values.push(true);
        }

        if (o_cnt > 1) {
            for (var m = 1; m <= o_cnt; m++) {
                if ($(".industry-" + le_cnt + "-" + d_cnt + "-" + m).val() != "") {
                    orgid_temp.push(parseInt($(".industry-" + le_cnt + "-" + d_cnt + "-" + m).val()));
                }
            }
        }

        var text_val = $(this).val();
        selected_textbox = $(this);
        selected_textid = $("." + val_class);
        $.each(INDUSTRIES, function(k, val) {
            if (!(jQuery.inArray(val["industry_id"], orgid_temp) !== -1)) {
                industries_temp.push(val);
            }
        });
        //console.log("industries_temp--"+industries_temp.toSource());
        commonAutoComplete(
            e, $("." + ac_class), $('.' + val_class), text_val,
            industries_temp, "industry_name", "industry_id",
            function(val) {
                onOrgSuccess(val);
            }, condition_fields, condition_values
        );

        // var textval = $(this).val();
        // selected_textbox = $(this);
        // getOrgAutocomplete(e, textval, INDUSTRIES, ac_class, val_class,
        //     function(val) {
        //         onOrgSuccess(val);
        //     });
        // });
    });
}

function addDomain(domain_list_class, domain_count_class, le_count) {
    // if($(".country-"+le_count+" option:selected").val() == 0){
    //     displayMessage(message.country_required);
    //     return false;
    // }    
    domain_count = $("." + domain_count_class).val();
    $("." + domain_count_class).val(++domain_count);
    var domain_row = $('.domain_row_template tr');
    var clone = domain_row.clone();

    var remove_class = "remove-domain-" + le_count + "-" + domain_count;
    $(".domain_row", clone).addClass(remove_class);
    var domain_class_le = "domain-" + le_count;
    var domain_class = "domain-" + le_count + "-" + domain_count;
    //$(".domain", clone).addClass(domain_class_le)
    $(".domain", clone).addClass(domain_class)
    $(".domain", clone).change(function() {
        console.log(le_count + "--" + domain_count);
        if (organization_details[le_count])
            delete organization_details[le_count][domain_count];
        console.log("load domains organization_details--" + JSON.stringify(organization_details));

        generateDateConfigurationList();
    });
    $(".domain", clone).change(function() {
        //loadDomains(domain_class, le_count);
    });


    var activationdate_class = "activationdate-" + le_count + "-" + domain_count;
    $(".activationdate", clone).addClass(activationdate_class)

    // var contractfromval = $(".contract-from-"+le_count).val();
    // var contracttoval = $(".contract-to-"+le_count).val();
    // var splitcontractfrom = [];
    // var splitcontractto = [];
    // if(contractfromval != ''){
    //     splitcontractfrom = contractfromval.split('-');
    //     var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    //     for(var j=0;j<months.length;j++){
    //         if(splitcontractfrom[1]==months[j]){
    //              splitcontractfrom[1]=months.indexOf(months[j])+1;
    //          }                      
    //     } 
    // }
    // else{
    //     splitcontractfrom[2] = 0;
    //     splitcontractfrom[1] = 0;
    //     splitcontractfrom[0] = 0;
    // }    
    // console.log(contracttoval);
    // if(contracttoval != ''){
    //     splitcontractto = contracttoval.split('-');
    //     var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    //     for(var j=0;j<months.length;j++){
    //         if(splitcontractto[1]==months[j]){
    //              splitcontractto[1]=months.indexOf(months[j])+1;
    //          }                      
    //     } 
    // }
    // else{
    //     splitcontractto[2] = 0;
    //     splitcontractto[1] = 0;
    //     splitcontractto[0] = 0;
    // }    
    // $("."+activationdate_class, clone).click(function(e) { 
    //    console.log("welcome to activationdate_class");
    //    if(contractfromval != '' &&  contracttoval != ''){
    clone.find("." + activationdate_class)
        .removeClass('hasDatepicker')
        .removeAttr('id')
        .datepicker({
            changeMonth: false,
            changeYear: false,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
            ]
        });
    //     }else{
    //         displayMessage(message.first_select_contract_from_and_to);
    //     }
    // });

    $(".addOrganizationType", clone).attr("id", le_count + "-" + domain_count); //addOrganizationType
    $(".addOrganizationType", clone).addClass("addOrganizationType-" + le_count + "-" + domain_count);
    $(".addOrganizationType", clone).click(function(e) {
        if ($("." + domain_class + " option:selected").val() == 0) {
            displayMessage(message.domain_select_first);
            return false;
        } else {
            Custombox.open({
                target: '#custom-modal',
                effect: 'contentscale',
                open: function() {
                    displayPopup($(".addOrganizationType", clone).attr("id"));
                }
            });
            e.preventDefault();
        }
    });

    $(".remove-domain", clone).click(function(e) {
        e.preventDefault();
        if (organization_details[le_count])
            delete organization_details[le_count][domain_count];
        console.log("Remove domains organization_details--" + JSON.stringify(organization_details));
        $(this).parent().parent().remove();
        generateDateConfigurationList();
    });
    $('.' + domain_list_class).append(clone);

    loadDomains(domain_class, le_count);
}

function prepareCountryDomainMap() {
    for (var i = 1; i <= le_count; i++) {
        var country_id = $(".country-" + i + " option:selected").val();
        if (country_id != 'undefined' && country_id != '0' && country_id != null) {
            var country_name = $(".country-" + i + "  option:selected").text();
            if (!(country_id in country_domain_id_map)) {
                country_domain_id_map[country_id] = {
                    "country_name": country_name,
                    "domains": [],
                    "domain_names": [],
                    "from": [],
                    "to": []
                }
            }
            country_domain_id_map[country_id]["domains"] = [];
            country_domain_id_map[country_id]["domain_names"] = [];
            for (var j = 1; j <= domain_count; j++) {
                var domain_id = $(".domain-" + i + "-" + j + " option:selected").val();
                if (domain_id != 'undefined' && domain_id != '0' && domain_id != null) {
                    var domain_name = $(".domain-" + i + "-" + j + " option:selected").text();
                    if (country_domain_id_map[country_id]["domains"].indexOf(domain_id) == -1) {
                        country_domain_id_map[country_id]["domains"].push(domain_id);
                        country_domain_id_map[country_id]["domain_names"].push(domain_name);
                    }
                }
            }
        }
    }
}

function generateDateConfigurationList() {
    $('.tbody-dateconfiguration-list').empty();
    prepareCountryDomainMap();
    $.each(country_domain_id_map, function(key, value) {
        var tableRow = $('.dconfig-templates .table-dconfig-list .table-dconfig-countries-row');
        var clone = tableRow.clone();
        var country_id = key;
        $('.dconfig-country-name', clone).text(value["country_name"]);
        $('.dconfig-country-name', clone).addClass('heading');
        $('.inputCountry', clone).text(country_id);
        $('.tbody-dateconfiguration-list').append(clone);
        $.each(value["domain_names"], function(name_key, name_value) {
            var domain_id = value["domains"][name_key];
            var tableRowDomains = $('.dconfig-templates .table-dconfig-list .table-dconfig-domain-row');
            var clone1 = tableRowDomains.clone();
            $('.inputDomain', clone1).text(domain_id);
            $('.dconfig-domain-name', clone1).text(value["domain_names"][name_key]);
            $('.tl-from', clone1).addClass('tl-from-' + country_id + '-' + domain_id);
            $('.tl-to', clone1).addClass('tl-to-' + country_id + '-' + domain_id);
            $('.tbody-dateconfiguration-list').append(clone1);
        });
    });
}

function loadCountries(country_class) {
    $('.' + country_class + "  option:gt(0)").remove();
    country_html = "<option value = '0'>(Select Country)</option>"
    $.each(COUNTRIES, function(key, value) {
        if (value.is_active == true) {
            country_html += "<option value = " + value.country_id + ">" + value.country_name + "</option>";
        }
    });
    $('.' + country_class).html(country_html);
}

function loadDomains(domain_class, le_count) {

    function isAvailableDomain(domain_id, le_cnt) {
        var domaintotalcount = $(".domain-count-" + le_cnt).val();
        for (var i = 1; i <= domaintotalcount; i++) {
            if (domain_id == parseInt($(".domain-" + le_count + "-" + i).val())) {
                return 1;
            }
        }
    }

    var countryselected = parseInt($(".country-" + le_count + " option:selected").val());
    $('.' + domain_class + "  option:gt(0)").remove();
    domain_html = "<option value = '0'>(Select Domain)</option>";
    $.each(DOMAINS, function(key, value) {
        if (value.is_active == true && jQuery.inArray(countryselected, value.country_ids) !== -1 && isAvailableDomain(value.domain_id, le_count) != 1) {
            domain_html += "<option value = " + value.domain_id + ">" + value.domain_name + "</option>";
        }
    });
    $('.' + domain_class).html(domain_html);
}

function loadDomainsforcountry(country_val, domain_class, countval) {
    for (var count = 1; count <= countval; count++) {
        $('.' + domain_class + "-" + count + "  option:gt(0)").remove();
        domain_html = "<option value = '0'>(Select Domain)</option>"
        $.each(DOMAINS, function(key, value) {
            if (value.is_active == true && jQuery.inArray(country_val, value.country_ids) !== -1) {
                domain_html += "<option value = " + value.domain_id + ">" + value.domain_name + "</option>";
            }
        });
        $('.' + domain_class + "-" + count).html(domain_html);
    }


}

function loadBusinessGroups(bg_class) {
    $('.' + bg_class + " option:gt(0)").remove();
    bg_html = "<option value ='0'>(Select Business Group)</option>";
    if (BUSSINESSGROUPS.length > 0) {
        $.each(BUSSINESSGROUPS, function(key, value) {
            bg_html += "<option value = " + parseInt(value.business_group_id) + ">" + value.business_group_name + "</option>";
        });
    }
    $('.' + bg_class).html(bg_html);
}


function showHideUserMenu(selectboxview_class, is_active) {
    if (is_active == true) {
        $("." + selectboxview_class).show();
    } else {
        $("." + selectboxview_class).hide();
    }
}

function onOrgSuccess(val) {
    selected_textbox.val(val[1]);
    selected_textid.val(val[0]);
}

function addOrSelectBusinessGroup(type_of_icon, thisvalue, le_count) {
    var countval;
    if (le_count == 0) {
        var lename = $(thisvalue).closest('.letable').attr('class').split(' ').pop();
        countval = lename.split('-').pop();
    } else {
        countval = le_count;
    }

    if (type_of_icon == "add") {
        $(".le-table-" + countval + " .input_business_group").show();
        $(".le-table-" + countval + " .select_business_group").hide();
    } else if (type_of_icon == "cancel") {
        $(".le-table-" + countval + " .input_business_group").hide();
        $(".le-table-" + countval + " .select_business_group").show();
    }
}

function loadOrganization_details(le_cnt, d_cnt) {

}


function displayPopup(counts) {

    count_list = counts.split("-");
    le_cnt = count_list[0];
    d_cnt = count_list[1];
    $("#le-cnt").val(le_cnt);
    $("#d-cnt").val(d_cnt);
    $("#o-cnt").val(0);
    $('.organization-list').empty();


    if (le_cnt in organization_details) {
        if (d_cnt in organization_details[le_cnt]) {
            o_cnt = 0;
            $.each(organization_details[le_cnt][d_cnt], function(key, value) {
                ++o_cnt;
                addOrganization();
                $(".org-selected-" + le_cnt + "-" + d_cnt + "-" + o_cnt).val(industry_name_map[parseInt(key)]);
                $(".industry-" + le_cnt + "-" + d_cnt + "-" + o_cnt).val(key);
                $(".no-of-units-" + le_cnt + "-" + d_cnt + "-" + o_cnt).val(value);
            });
            $("#o-cnt").val(o_cnt);
        } else {
            addOrganization();
        }
    } else {
        addOrganization();
    }


}

// function closePopup(){
//     $('.overlay').css('visibility', 'hidden');
//     $('.overlay').css('opacity', '0');
// }

function changeClientStatus() {
    var group_id = $(".popup-group-id").val();
    var pass_value = $(".popup-pass-value").val();
    if (pass_value == "false") {
        pass_value = false;
    } else {
        pass_value = true;
    }

    function onSuccess(data) {
        displayMessage(message.client_change_status_success);
        initialize("list");
    }

    function onFailure(error) {
        displayMessage(error);
    }
    mirror.changeClientGroupStatus(
        parseInt(group_id), pass_value,
        function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        });
}

// List filter process
// function processFilter() {
//     country_search = $('#search-country').val().toLowerCase();
//     //group_search = $('#search-group').val().toLowerCase();
//     le_search = $('#search-legalentity').val().toLowerCase();

//     active_status = $('.search-status-li.active').attr('value');
//     grp_status = $('.search-astatus-li.active').attr('value');
//     filteredList = []
//     for (var g in GROUPS) {
//         data = GROUPS[g]
//         cn = data.country_name.toLowerCase();
//         grp = data.group_name.toLowerCase();
//         legname = (data.legal_entity_name).toString();
//         if (
//             (~cn.indexOf(country_search)) && (~grp.indexOf(group_search)) && (~legname.indexOf(le_search)) 
//         ) {
//             if ((active_status == 'all' || parseInt(active_status) == data.is_active) &&
//                 (grp_status == 'all' || parseInt(grp_status) == data.is_approved)) {
//                 filteredList.push(data);
//             }

//         }
//     }
//     loadGroups(filteredList);
// }

/*Search_status_ul.click(function(event) {
    Search_status_li.each(function(index, el) {
        $(el).removeClass('active');
    });
    $(event.target).parent().addClass('active');

    var currentClass = $(event.target).find('i').attr('class');
    
    Search_status.removeClass();
    if (currentClass != undefined) {

        Search_status.addClass(currentClass);
        Search_status.text('');
    } else {
        Search_status.addClass('fa');
        Search_status.text('All');
    }
    processFilter();
});*/

/*Search_astatus_ul.click(function(event) {
    Search_astatus_li.each(function(index, el) {
        $(el).removeClass('active');
    });
    $(event.target).parent().addClass('active');
    var currentClass = $(event.target).find('a').html();    
    //Search_astatus.removeClass();
    if (currentClass != undefined) {
        alert(currentClass);
    //    Search_astatus.addClass(currentClass);
        //Search_astatus.text('');
    } else {
        Search_astatus.addClass('fa');
        Search_astatus.text('All');
    }
    processFilter();
});*/


$(document).ready(function() {
    displayLoader();
    initialize("list");
    hideLoader();
    $('div[data-toggle="tooltip"]').tooltip();
});

$('#shortname').on('input', function(e) {
    this.value = isAlphanumeric_Shortname($(this));
});

// $('.no-of-units').on('input', function (e) {
//   this.value = isNumbers($(this));
// });

$('.status-submit').on("click", function() {
    validateAuthentication();
});
