//  Statutory mapping
//  List grid
//  Load Tabwise data
//  split functionality tab wise
//  Save and submit process
//  Edit process
//  status process
//

// MASTER DATA
var FREQUENCY_INFO;
var DURATION_INFO;
var REPEATSTYPE_INFO;
var APPROVALSTATUS_INFO;
var COUNTY_INFO;
var DOMAIN_INFO;
var ORGANISATION_INFO;
var NATURE_INFO;
var STATUTORY_INFO;
var STATUTORY_LEVEL_INFO;
var GEOGRAPHY_INFO;
var GEOGRAPHY_LEVEL_INFO;
var STATU_MAPPINGS;
var STATU_TOTALS;

var CURRENT_TAB = 1;
// controls
Spin_pan = $('.loading-indicator-spin');
Country = $('#country');
Domain = $("#domain");
Organisation = $("#industry");
Nature = $('#statutorynature');
Frequency = $('#compliance_frequency');
Duration = $('#duration_type');
Repeats = $('#repeats_type');

//buttons
AddButton = $('.btn-add');
NextButton = $('.btn-next');
PreviousButton = $(".btn-previous");
SubmitButton = $(".btn-submit");
BackButton = $(".btn-back");
SaveButton = $(".btn-save");

ListScreen = $('#statutorymapping-view');
ViewScreen = $('#statutorymapping-add');

option_pan = $('<option></option>')
list_template = $("#templates #list-template .items");
var msg = message;
var fetch = mirror;

_renderinput = null;
_fetchback = null;
_listPage = null;
_viewPage = null;

displayMsg = function(msg) {
    alert(msg);
};

possibleFailure = function(err, extra_details) {
    if (err == "StatutoryNameAlreadyExists") {
        displayMsg(msg.statutoryname_exists);
    }
    else if ( err == "ComplianceNameAlreadyExists") {
        displayMsg(msg.compliancename_exists + extra_details);
    }
    else if (err = "TransactionExists") {
        displayMsg(msg.transaction_exists);
    }
    else {
        displayMsg(err);
    }
};
//
// render list, select and multiselect box with data
//
function RenderInput() {

    this.country_id = null;
    this.county_name = null;
    this.domain_id = null;
    this.domain_name = null;
    this.org_ids = [];
    this.org_names = [];
    this.nature_id = null;
    this.nature_name = null;
    this.last_selected = null;

    this.remveItemFromList = function(item, mainlist) {
        if (!mainlist)
            return;
        idx = mainlist.indexOf(item);
        if (idx != -1)
            mainlist.splice(idx, 1);
        return mainlist;
    };

    this.make_option = function (oname, oid) {
        opt = option_pan;
        opt.val(oid);
        opt.text(oname);
        return opt;
    };

    this.resetField = function() {
        this.country_id = null;
        this.county_name = null;
        this.domain_id = null;
        this.domain_name = null;
        this.org_ids = [];
        this.org_names = [];
        this.nature_id = null;
        this.nature_name = null;
    };

    this.loadCounty = function() {
        this.resetField();
        Country.empty();

        $.each(COUNTY_INFO, function(ke, val) {
            if (val.is_active == false)
                return

            cObject = $("#templates #list-template li").clone();
            cObject.addClass('countrylist');
            cObject.attr('id', 'c'+val.c_id);

            cObject.on('click', function(cObject) {
                // highlight call
                $('.countrylist').removeClass('active');
                _renderinput.country_id = val.c_id;
                _renderinput.country_name = val.c_name;
                _renderinput.loadDomain(val.c_id);
                _renderinput.loadNature(val.c_id);
                $('#c'+val.c_id).addClass('active');
            });
            $('.name-holder', cObject).text(val.c_name);
            Country.append(cObject);
        });
    };

    this.loadDomain = function(c_id) {
        this.domain_id = null;
        this.domain_name = null;
        this.org_ids = [];
        this.org_names = [];
        Domain.empty();

        $.each(DOMAIN_INFO, function(ke, val) {
            if (val.is_active == false)
                return
            if (val.c_id != c_id)
                return
            dObject = $("#templates #list-template li").clone();
            dObject.addClass("domainlist");
            dObject.attr('id', 'd'+val.d_id);
            dObject.on('click', function() {
                $(".domainlist").removeClass('active');
                $("#d"+val.d_id).addClass('active');
                _renderinput.domain_id = val.d_id;
                _renderinput.domain_name = val.d_name;
                _renderinput.loadOrganisation(val.c_id, val.d_id);
            });
            $('.name-holder', dObject).text(val.d_name);
            Domain.append(dObject);
        });
        Organisation.empty();
    };

    this.loadOrganisation = function(c_id, d_id) {
        this.org_ids = [];
        this.org_names = [];
        Organisation.empty();

        // append select
        orgObject = list_template.clone();
        orgObject.addClass("organisationlist");
        orgObject.attr('id', 'o-1');
        $('.name-holder', orgObject).text('Select');
        Organisation.append(orgObject)
        orgObject.on('click', function() {
            sts = $('#o-1').hasClass('active');
            if (sts == true) {
                $('.organisationlist').removeClass('active');
                _renderinput.org_ids = [];
                _renderinput.org_names = [];

            }
            else {
                $('.organisationlist').addClass('active');
                $.each(ORGANISATION_INFO, function(k, v) {
                    if ((v.c_id != c_id) && (v.d_id != d_id))
                        return;
                    _renderList.org_ids.push(v.org_id);
                    _renderList.org_names.push(v.org_name);
                });
            }
        });

        $.each(ORGANISATION_INFO, function(ke, val) {
            if (val.is_active == false)
                return;
            if ((val.c_id != c_id) && (val.d_id != d_id))
                return;
            orgObject = list_template.clone();
            orgObject.addClass("organisationlist");
            orgObject.attr('id', 'o'+val.org_id);
            orgObject.on('click', function() {
                $('#o-1').removeClass('active');
                sts = $('#o'+val.org_id).hasClass('active');
                if (sts == true) {
                    $('#o'+val.org_id).removeClass('active');
                    _renderinput.org_id = _renderinput.remveItemFromList(
                        val.org_id, this.org_id
                    );
                    _renderinput.org_name = _renderinput.remveItemFromList(
                        val.org_name, this.org_name
                    );
                }
                else {
                    $('#o'+val.org_id).addClass('active');
                    _renderinput.org_id.push(val.org_id);
                    _renderinput.org_name.push(val.org_name);
                }
            });
            $('.name-holder', orgObject).text(val.org_name);
            Organisation.append(orgObject);
        });
    };

    this.loadNature = function(c_id) {
        this.nature_id = null;
        this.nature_name = null;
        Nature.empty();

        $.each(NATURE_INFO, function(ke, val) {
            if (val.is_active == false)
                return;
            if (val.c_id != c_id)
                return;
            nObject = $("#templates #list-template li").clone();
            nObject.addClass("naturelist");
            nObject.attr('id', 'n'+val.s_n_id);
            nObject.on('click', function() {
                $(".naturelist").removeClass('active');
                $('#n'+val.s_n_id).addClass('active');
                this.nature_id = val.s_n_id;
                this.nature_name = val.s_n__name;
            });
            $('.name-holder', nObject).text(val.s_n_name);
            Nature.append(nObject);
        });
    };

    this.loadDuration = function() {
        Duration.empty();
        Duration.append(
            this.make_option("Select", "")
        );
        $.each(DURATION_INFO, function(ke, val) {
            Duration.append(
                this.make_option(val.duration_type, val.duration_type_id)
            );
        });
    };

    this.loadRepeats = function() {
        Repeats.empty();
        Repeats.append(
            this.make_option("Select", "")
        );
        $.each(REPEATSTYPE_INFO, function(ke, val) {
            Repeats.append(
                this.make_option(val.repeat_type, val.repeat_type)
            );
        });
    };

    this.loadFrequency = function() {
        Frequency.empty();
        Frequency.append(
            this.make_option("Select", "")
        );
        $.each(FREQUENCY_INFO, function(ke, val) {
            Frequency.append(
                this.make_option(val.frequency, val.frequency_id)
            );
        });
    };

    this.loadStatuLevels = function() {

    };
    this.loadStatuesLevels = function() {
        if ((this.country_id == null) || (this.domain_id == null)) {
            return;
        }
        c_list = STATUTORY_LEVEL_INFO[this.country_id];
        if (!c_list)
            return
        s_list = c_list[this.domain_id];
        if (!s_list)
            return

        $.each(s_list, function(k, v) {
            slObject = $('#statutory-level-templates').clone();
            $('.statutory_title .scrollable', slObject).html(v.l_name);
            $('.statutory_levelvalue .filter-text-box', slObject).attr(
                'id', 'sf'+ v.l_position
            );
            $('.statutory_levelvalue .filter-text-box', slObject).on(
                'keyup', function(element, v){
                    // filter_statutory();
            });
            $('.statutory_levelvalue .sname-list', slObject).attr(
                'id', 'snl' + v.l_position
            );
            $('.statutory_levelvalue .bottomfield txtsname', slObject).attr(
                'id', 'dv' + v.l_position
            );
            $('.statutory_levelvalue .bottomfield txtsname', slObject).on(
                'keypress', function(element) {
                /// saverecord();
            });

            $('.statutory_levelvalue .bottomfield .edit-icon', slObject).on(
                'click', function(){
                // saverecord();
            });

            $('.tbody-statutory-level').append(slObject);

        });

    };
}
_renderinput = new RenderInput();
//
// callback with compfie input data
//
function FetchBack() {
    this.getMasterData = function() {
        fetch.getStatutoryMappingsMaster(function(status, response) {
            if (status != null) {
                displayMsg(status);
            }
            else {
                COUNTY_INFO = response.country_info;
                DOMAIN_INFO = response.domain_info;
                ORGANISATION_INFO = response.organisation_info;
                NATURE_INFO = response.nature_info;
                STATUTORY_LEVEL_INFO = response.statutory_levels;
                GEOGRAPHY_LEVEL_INFO = response.geography_level_info;
                GEOGRAPHY_INFO = response.geography_info;
                FREQUENCY_INFO = response.compliance_frequency;
                REPEATSTYPE_INFO = response.compliance_repeat_type;
                APPROVALSTATUS_INFO = response.compliance_approval_status;
                DURATION_INFO = response.compliance_duration_type;
            }
        });
    };

    this.getStatuMaster = function() {
        fetch.getStatutoryMaster(function(status, response) {
            if(status != null) {
                displayMsg(status);
            }
            else {
                STATUTORY_INFO = response.statutory_info;
            }
        });
    };

    this.getMappedList = function(approv_status, rcount) {
        fetch.getStatutoryMappings(approv_status, rcount,
            function(status, response){
                if (status != null) {
                    displayMsg(status);
                }
                else {
                    STATU_MAPPINGS = response.statu_mappings;
                    STATU_TOTALS = response.total_records;
                    _listPage.renderList(STATU_MAPPINGS, STATU_TOTALS);
                }
            }
        );
    };

    this.changeStatus = function(m_id, sts) {
        fetch.changeStatutoryMappingStatus(m_id, sts, function(status, response) {
            if (staus != null) {
                displayMsg(status);
            }
            else {
                this.getMappedList(0, 0);
            }
        });
    };

    this.saveStautory = function(d_id, s_l_id, s_name, p_ids, p_names){
        fetch.saveStautory(d_id, s_l_id, s_name, p_ids, p_names, function(
                status, response
            ){
                if(status != null) {
                    displayMsg(status);
                }
                else {
                    // load statutory list

                }
            }
        );
    };
}
_fetchback = new FetchBack();
//
// Render List Page
//
function ListPage() {

    this.renderList = function(data, tRecord) {
        $('.tbl-statutorymapping-list tr').find('mapping_row');
        $('.tbl-statutorymapping-list tr').find('compliance_row');

        function comp_row(rowObjec, cdata) {
            var x = 1;
            $.each(cdata, function(k, c) {
                row = $('#templates .compliance_row').clone();
                $('.comp_name', row).text(c.comp_name);
                $('.comp_approval_status', row).text(j);
                $('.comp_edit', row).attr('title', 'Edit');
                $('.comp_edit', row).on('click', function() {
                    this.displayEdit(v.comp_id);
                });
                rowObjec.append(row);
            });
        }

        var j = 1;
        $.each(data, function(k, v) {
            org_names = v.industry_names.join(' >> ');
            s_names = v.statutory_mappings.join(' >> ');
            crow = $('#templates .mapping-row').clone();
            $('.sno', crow).text(j);
            $('.c_name', crow).text(v.country_name);
            $('.d_name', crow).text(v.domain_name);
            $('.org_name', crow).text(org_names);
            $('.nature_name', crow).text(v.statutory_nature_name);
            $('.s_name', crow).text(s_names);
            $('.map_edit', crow).attr('title', 'Edit');
            $('.map_edit', crow).on('click', function() {
                this.displayEdit(v.mapping_id);
            });
            if (v.is_active == true){
                $('.map_status', crow).addClass("active-icon");
                $('.map_status', crow).attr('title', msg.active_tooltip);
            }
            else {
                $('.map_status', crow).addClass("inactive-icon");
                $('.map_status', crow).attr('title', msg.deactive_tooltip);
            }
            $('.map_status', crow).on('click', function() {
                if (v.is_active == true) {
                    passStatus = false;
                }
                else {
                    passStatus = true;
                }
                _fetchback.changeStatus(v.mapping_id, passStatus);
            });

            $('.approval_status', crow).text(v.approval_status_text);
            j = j + 1;
            $('.tbl-statutorymapping-list').append(crow);
            comp_row($('.tbl-statutorymapping-list'), v.mapped_compliances);
        });
    };

    this.displayEdit = function(map_id, comp_id) {
        // differentiate compliance edit and whole edit
    };

    this.show = function() {
        ListScreen.show();
        _fetchback.getMappedList(0, 0);
    };
    this.hide = function() {
        ListScreen.hide();
    };

}
//
// Render View Pages
//
function ViewPage() {
    this.showFirstTab = function(){
        _renderinput.loadCounty();
    };
    this.showSecondTab = function(){};
    this.showThirdTab = function(){};
    this.showFouthTab = function(){};
    this.show = function() {
        ViewScreen.show();
        this.showFirstTab();
    };
    this.hide = function() {
        ViewScreen.hide();
    };
}

function showTab(){
    if (CURRENT_TAB == 1) {
        $('#step-1').show();
        $('#step-2').hide();
        $('#step-3').hide();
        $('#step-4').hide();
    }

};
_listPage = new ListPage();
_viewPage = new ViewPage();

function initialize() {
    _listPage.show();
    _fetchback.getMasterData();
    _fetchback.getStatuMaster();

    AddButton.click(function() {
        _listPage.hide();
        _viewPage.show();
    });
    NextButton.click(function() {

    });
}

$(document).ready(function(){
    initialize();
});
