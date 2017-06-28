var isAuthenticate;
var compliance_edit = false;

var CURRENT_TAB = 1;
IS_EDIT = false;
IS_SAVE = false;

// password popup

var CurrentPassword = $('#current-password');


// list filter control
approveStatusUL = $('#ap-status-list');
approveStatusLI = $('.ap-status-li');
approveStatusText = $('#ap-status');
filterBox = $('.filter-box');
searchStatusUi = $('.search-status-list');
searchStatusLi = $('.search-status-li');
searchStatus = $('#search-status');
// Tab 1
Country = $('#country');
Domain = $("#domain");
Organisation = $("#industry");
Nature = $('#statutorynature');

// Teb 3
Onetimepan = $('#One_Time');
RecurringPan = $('#Recurring');
OccasionalPan = $('#Occasional');

Frequency = $('#compliance_frequency');
DurationType = $('#duration_type');
Duration = $('#duration');

RepeatsType = $('#repeats_type');
RepeatsEvery = $('#repeats_every')
MultiselectDate = $('.multi-date-box');

ComplianceTask = $('#compliance_task');
Provision = $('#statutory_provision');
Description = $('#compliance_description');
Document = $('#compliance_document');
Format = $('#upload_file');
Penal = $('#penal_consequences');
ReferenceLink = $('#reference_link');
Comp_id = $('#comp_id');
Temp_id = $('#temp_id');
Comp_status = $('#comp_status_id');
RepeatBy = null;

//buttons
AddButton = $('#btn-add');

NextButton = $('#btn-next');
PreviousButton = $('#btn-previous');
SubmitButton = $("#btn-submit");
BackButton = $("#btn-back");
SaveButton = $("#btn-save");

AddStatuButton = $('#temp_addstatutories');
AddComplianceButton = $('#temp_addcompliance');

PasswordSubmitButton = $('#password-submit');

ListScreen = $('#statutorymapping-view');
ViewScreen = $('#statutorymapping-add');

listTemplate = $("#templates #list-template .items");
var file_type = [
    "doc", "docx", "rtf", "pdf", "txt", "zip", "png", "jpeg", "gif", "csv", "xls", "xlsx",
    "rar", "tar", "gz", "ppt", "pptx", "jpg", "bmp", "odt", "odf", "ods"
]

_renderinput = null;
_fetchback = null;
_listPage = null;
_viewPage = null;


//
// render list, select and multiselect box with data
//
function RenderInput() {

    this.countryId = null;
    this.countyName = null;
    this.domainId = null;
    this.domainName = null;
    this.orgIds = [];
    this.orgNames = [];
    this.natureId = null;
    this.natureName = null;
    this.last_selected = null;
    this.s_names = [];
    this.s_pids = [];
    this.s_id = null;
    this.mapped_statu = [];
    this.l_one_id = null;
    this.l_one_name = null;
    this.level_one_name = null;
    this.mapped_compliances = [];
    this.summary = null;
    this.statu_dates = [];
    this.selected_geos = [];
    this.selected_geos_parent = [];
    this.child_geos = [];
    this.selected_sids = [];
    this.selected_iids = [];
    this.mapping_id = null;
    this.is_file_uploaded = true;
    this.uploaded_files = [];
    this.uploaded_files_fcids = {};
    this.form_data = new FormData();
    this.file_removed = false;
    this.f_f_list = [];
    this.allow_domain_edit = true;
    this.show_map_count = 0;


    this.remveItemFromList = function(item, mainlist) {
        if (!mainlist)
            return;
        idx = mainlist.indexOf(item);
        if (idx != -1)
            mainlist.splice(idx, 1);
        return mainlist;
    };

    this.make_option = function(oname, oid) {
        opt = $('<option></option>');
        opt.val(oid);
        opt.html(oname);
        return opt;
    };

    this.resetField = function() {
        IS_EDIT = false;
        IS_SAVE = false;
        compliance_edit = false;
        this.countryId = null;
        this.countyName = null;
        this.domainId = null;
        this.domainName = null;
        this.orgIds = [];
        this.orgNames = [];
        this.natureId = null;
        this.natureName = null;
        this.last_selected = null;
        this.s_names = [];
        this.s_pids = [];
        this.s_id = null;
        this.mapped_statu = [];
        this.l_one_id = null;
        this.level_one_name = null;
        this.mapped_compliances = [];
        this.summary = null;
        this.statu_dates = [];
        this.selected_geos = [];
        this.selected_geos_parent = [];
        this.child_geos = [];
        this.selected_sids = [];
        this.selected_iids = [];
        this.mapping_id = null;
        Country.empty();
        Domain.empty();
        Organisation.empty();
        Nature.empty();
        RepeatsType.empty();
        Frequency.empty();
        $('.tbody-statutory-list').empty();
        $('.tbody-compliance-list').empty();
        this.clearCompliance();
        this.allow_domain_edit = true;
    };
    this.getMonthAndDataSets = function() {
        return [
            { 'm_id': 1, 'm_name': 'Jan', 'range': 31 },
            { 'm_id': 2, 'm_name': 'Feb', 'range': 28 },
            { 'm_id': 3, 'm_name': 'Mar', 'range': 31 },
            { 'm_id': 4, 'm_name': 'Apr', 'range': 30 },
            { 'm_id': 5, 'm_name': 'May', 'range': 31 },
            { 'm_id': 6, 'm_name': 'Jun', 'range': 30 },
            { 'm_id': 7, 'm_name': 'Jul', 'range': 31 },
            { 'm_id': 8, 'm_name': 'Aug', 'range': 31 },
            { 'm_id': 9, 'm_name': 'Sep', 'range': 30 },
            { 'm_id': 10, 'm_name': 'Oct', 'range': 31 },
            { 'm_id': 11, 'm_name': 'Nov', 'range': 30 },
            { 'm_id': 12, 'm_name': 'Dec', 'range': 31 }
        ];
    };

    this.loadCounty = function() {
        // this.resetField();
        Country.empty();
        t_this = this;

        $.each(COUNTY_INFO, function(ke, val) {
            if (val.is_active == false)
                return

            cObject = $("#templates #list-template li").clone();
            cObject.addClass('countrylist');
            cObject.attr('id', 'c' + val.c_id);
            if (IS_EDIT == false) {
                cObject.on('click', function(cObject) {
                    $('.countrylist').removeClass('active');
                    $('.countrylist i').removeClass('fa-check');
                    _renderinput.countryId = val.c_id;
                    _renderinput.countryName = val.c_name;
                    _renderinput.domainId = null;
                    _renderinput.loadDomain(val.c_id);
                    _renderinput.natureId = null;
                    _renderinput.loadNature(val.c_id);

                    _renderinput.orgIds = [];
                    _renderinput.orgNames = [];
                    _renderinput.selected_iids = [];
                    Organisation.empty();
                    _renderinput.loadOrganisation(_renderinput.countryId, _renderinput.domainId);
                    $('#c' + val.c_id).addClass('active');
                    $('#c' + val.c_id + ' i').addClass("fa-check");
                });
            }

            $('.name-holder', cObject).text(val.c_name);
            Country.append(cObject);
            if (_renderinput.countryId == val.c_id) {
                $('#c' + val.c_id).addClass('active');
                $('#c' + val.c_id + ' i').addClass("fa-check");
                _renderinput.loadDomain(_renderinput.countryId);
                _renderinput.loadNature(_renderinput.countryId);
            }

        });
    };

    this.loadDomain = function(c_id) {
        Domain.empty();

        $.each(DOMAIN_INFO, function(ke, val) {
            if (val.is_active == false)
                return
            if (val.c_id != c_id)
                return
            dObject = $("#templates #list-template li").clone();
            dObject.addClass("domainlist");
            dObject.attr('id', 'd' + val.d_id);
            if (_renderinput.allow_domain_edit == true) {
                dObject.on('click', function() {
                    $(".domainlist").removeClass('active');
                    $(".domainlist i").removeClass('fa-check');

                    $("#d" + val.d_id).addClass('active');
                    $("#d" + val.d_id + ' i').addClass('fa-check');
                    _renderinput.domainId = val.d_id;
                    _renderinput.domainName = val.d_name;
                    _renderinput.selected_iids = [];
                    _renderinput.loadOrganisation(val.c_id, val.d_id);
                    _renderinput.mapped_statu = [];
                    $('.tbody-statutory-list').empty();
                });
            }
            $('.name-holder', dObject).text(val.d_name);
            Domain.append(dObject);
            if (_renderinput.domainId == val.d_id) {
                $("#d" + val.d_id).addClass('active');
                $("#d" + val.d_id + ' i').addClass('fa-check');
                _renderinput.loadOrganisation(c_id, _renderinput.domainId);
            }

        });
    };

    this.loadOrganisation = function(c_id, d_id) {
        // this.orgIds = [];
        // this.orgNames = [];
        $('.organisationlist', Organisation).removeClass('active');
        $('.organisationlist i', Organisation).removeClass('fa-check');
        Organisation.empty();
        var first_li = true;

        // append select
        _renderinput.orgIds = [];
        _renderinput.orgNames = [];
        $.each(ORGANISATION_INFO, function(ke, val) {
            if (val.is_active == false)
                return;
            if (
                (parseInt(val.c_id) == parseInt(c_id)) &&
                (parseInt(val.d_id) == parseInt(d_id))
            ) {
                if (first_li == true) {
                    orgObject = listTemplate.clone();
                    orgObject.addClass("organisationlist");
                    orgObject.attr('id', 'o-1');
                    $('.name-holder', orgObject).text('Select All');
                    Organisation.append(orgObject)

                    orgObject.on('click', function() {
                        _renderinput.orgIds = [];
                        _renderinput.orgNames = [];
                        sts = $('#o-1').hasClass('active');
                        if (sts == true) {
                            $('.organisationlist').removeClass('active');
                            $('.organisationlist i').removeClass('fa-check');
                            _renderinput.selected_iids = [];
                        } else {
                            $('.organisationlist').addClass('active');
                            $('.organisationlist i').addClass('fa-check');
                            _renderinput.selected_iids = [];
                            $.each(ORGANISATION_INFO, function(k, v) {
                                if ((v.c_id == _renderinput.countryId) && (v.d_id == _renderinput.domainId)) {
                                    _renderinput.selected_iids.push(v.org_id)
                                }
                            });
                        }
                    });
                }
                first_li = false;
                orgObject = listTemplate.clone();
                orgObject.addClass("organisationlist");
                orgObject.attr('id', 'o' + val.org_id);

                orgObject.on('click', function() {
                    $('#o-1').removeClass('active');
                    $('#o-1 i').removeClass('fa-check');
                    sts = $('#o' + val.org_id).hasClass('active');
                    if (sts == true) {
                        $('#o' + val.org_id).removeClass('active');
                        $('#o' + val.org_id + ' i').removeClass('fa-check');
                        _renderinput.selected_iids = _renderinput.remveItemFromList(val.org_id, _renderinput.selected_iids)
                    } else {
                        $('#o' + val.org_id).addClass('active');
                        $('#o' + val.org_id + ' i').addClass('fa-check');
                        _renderinput.selected_iids.push(val.org_id);
                    }
                });

                $('.name-holder', orgObject).text(val.org_name);
                Organisation.append(orgObject);
                if (_renderinput.selected_iids.length > 0) {
                    if (_renderinput.selected_iids.indexOf(val.org_id) > -1) {
                        $('#o' + val.org_id).addClass('active');
                        $('#o' + val.org_id + ' i').addClass('fa-check');
                        _renderinput.orgIds.push(val.org_id);
                        _renderinput.orgNames.push(val.org_name);
                    }
                }

            }
        });
    };

    this.loadNature = function(c_id) {
        Nature.empty();
        $('.naturelist').remove();
        // _renderinput.natureId = null;
        $.each(NATURE_INFO, function(ke, val) {
            if (val.is_active == false)
                return;
            if (val.c_id != c_id)
                return;
            nObject = $("#templates #list-template li").clone();
            nObject.addClass("naturelist");
            nObject.attr('id', 'n' + val.s_n_id);
            nObject.on('click', function() {
                $(".naturelist").removeClass('active');
                $(".naturelist i").removeClass('fa-check');
                $('#n' + val.s_n_id).addClass('active');
                $('#n' + val.s_n_id + ' i').addClass('fa-check');
                _renderinput.natureId = val.s_n_id;
                _renderinput.natureName = val.s_n__name;
            });
            $('.name-holder', nObject).text(val.s_n_name);
            Nature.append(nObject);

            if (_renderinput.natureId == val.s_n_id) {
                $('#n' + val.s_n_id).addClass('active');
                $('#n' + val.s_n_id + ' i').addClass('fa-check');
                _renderinput.natureId = val.s_n_id;
                _renderinput.natureName = val.s_n__name;
            }

        });
    };

    this.loadRepeats = function() {
        RepeatsType.empty();
        RepeatsType.append(
            _renderinput.make_option("Select", "")
        );
        var p = 0;
        $.each(REPEATSTYPE_INFO, function(ke, val) {
            RepeatsType.append(
                _renderinput.make_option(val.repeat_type, val.repeat_type_id)
            );
            p = 1
        });
        if(p == 1) {
            if (RepeatsType.val() != '') {
                dat = RepeatsEvery.val();
                mon = $('#repeats_type option:selected').text();
                summary = 'Repeats every ' + dat + " " + mon
                $('.recurr-summary', RecurringPan).text(summary);
                _renderinput.summary = summary
            }
        }
        RepeatsType.on('change', function() {
            if(RepeatsEvery.val().trim() == "") {
                displayMessage(message.repeatsevery_required);
                RepeatsType.val('');
                return false;
            }
            _renderinput.changeRepeatType();
            if (RepeatsType.val() != '') {
                dat = RepeatsEvery.val();
                mon = $('#repeats_type option:selected').text();
                summary = 'Repeats every ' + dat + " " + mon
                $('.recurr-summary', RecurringPan).text(summary);
                _renderinput.summary = summary
            } else {
                $('.recurr-summary', RecurringPan).text("");
            }
        });
        this.changeRepeatType = function() {
            // trigger-label
            if (parseInt(RepeatsEvery.val()) == 0) {
                displayMessage(message.invalid_repeatsevery);
            }
            if (RepeatsType.val() == 2) {
                if ((12 % parseInt(RepeatsEvery.val()) == 0) && (parseInt(RepeatsEvery.val()) < 12)) {
                    $('.multicheckbox', RecurringPan).show();
                    _renderinput.loadMultipleDate();
                } else {
                    $('.multicheckbox', RecurringPan).hide();
                    MultiselectDate.prop('checked', false);
                }
            } else {
                $('.multicheckbox', RecurringPan).hide();
                MultiselectDate.prop('checked', false);
            }

            r_by = $("input[name='radioSingle1']:checked").val();

            if (RepeatsType.val() == 1) {
                // hide repeat by, statutoty date and statutory month
                // show only trigger days
                $('.date-list').empty();
                date_pan = _renderinput.loadDate(0)
                $('.date-list').append(date_pan);
                $('.repeat-by', RecurringPan).hide();
                $(".statu-date-label", RecurringPan).hide();
                $(".date-list").each(function() {
                    $(".statu-date-div", this).hide();
                });
                $('.trigger-label').removeClass("text-right");
            } else if (RepeatsType.val() == 2) {
                // hide statutory month
                // show statutory date and trigger days
                $('.repeat-by', RecurringPan).show();
                $(".statu-date-label", RecurringPan).show();
                $(".date-list").each(function() {

                    $(".month-select-div", this).hide();
                    if (r_by == 1) {
                        $(".statu-date-div", this).show();
                        $(".date-select-div", this).show();
                    } else {
                        $(".statu-date-label", RecurringPan).hide();
                        $(".date-select-div", this).hide();
                        $(".statu-date-div", this).hide();
                    }
                    _renderinput.loadDays(0, 1);
                });
                $('.trigger-label').addClass("text-right");
            } else {
                // show month, date annd trigger days
                $('.repeat-by', RecurringPan).show();
                $(".statu-date-label", RecurringPan).show();
                $('.date-list').empty();
                date_pan = _renderinput.loadDate(0)
                $('.date-list').append(date_pan);
                _renderinput.loadedDateEvent(0);
                $(".date-list").each(function() {
                    $(".statu-date-div", this).show();

                    $(".month-select-div", this).show();
                    if (r_by == 1) {
                        $(".date-select-div", this).show();
                    } else {
                        $(".date-select-div", this).hide();
                    }
                });
                $('.trigger-label').addClass("text-right");
            }
        };
    };
    this.loadDate = function(idx) {
        date_pan = $("#templates #date-list-templates").clone();
        date_pan.attr('id', 'dt' + idx);
        $('.month-select', date_pan).empty();
        _renderinput.loadMonthAndData($('.month-select', date_pan));

        $('.date-select', date_pan).empty();
        $('.date-select', date_pan).append(_renderinput.make_option("Select", ''));
        for (var i = 1; i <= 31; i++) {
            dopt = _renderinput.make_option(i, i);
            $('.date-select', date_pan).append(dopt);
        }


        $('.trigger-value', date_pan).on('input', function(e) {
            this.value = isNonZeroNumbers($(this));
        });
        repeat_by = $("input[name='radioSingle1']:checked").val();

        if (RepeatsType.val() == 2) {
            if (MultiselectDate.prop('checked') == false) {
                $('.month-select-div', date_pan).hide();
            }

            if (repeat_by == 2) {
                $('.date-select', date_pan).hide();
                $('.statu-date-div', date_pan).hide();
                $(".statu-date-label", RecurringPan).hide();
                if (MultiselectDate.prop('checked') == true) {
                    $('.statu-date-div', date_pan).show();
                } else {
                    $('.statu-date-div', date_pan).hide();
                }
            } else {
                $('.date-select', date_pan).show();
                $('.statu-date-div', date_pan).show();
                $(".statu-date-label", RecurringPan).show();
            }

        }
        return date_pan;
    };
    this.loadDays = function(idx, key) {
        $.each(_renderinput.getMonthAndDataSets(), function(kk, v) {
            if (v.m_id == key) {
                $('.date-select', '#dt' + idx).empty();
                $('.date-select', '#dt' + idx).append(_renderinput.make_option("Select", ''));
                for (var i = 1; i <= v.range; i++) {
                    dopt = _renderinput.make_option(i, i);
                    $('.date-select', '#dt' + idx).append(dopt);
                }
            }
        });
    }
    this.loadedDateEvent = function(idx) {
        $('.month-select', '#dt' + idx).change(function() {
            if (parseInt(RepeatsEvery.val()) == 0) {
                displayMessage(message.invalid_repeatsevery);
            }

            _renderinput.loadDays(idx, $('.month-select', '#dt' + idx).val());
            if ((idx == 0) && (MultiselectDate.prop('checked') == true)) {
                // auto select month from first index value
                every_val = parseInt(RepeatsEvery.val());
                actual_len = 12 / every_val
                first_month = $('.month-select', '#dt0').val();

                if (first_month != '') {
                    for (i = 1; i < actual_len; i++) {
                        next_val = parseInt(first_month) + (i * parseInt(every_val));
                        if (next_val > 12) {
                            next_val = next_val - 12;
                        }
                        $('.month-select', '#dt' + i).val(next_val);
                        _renderinput.loadDays(i, next_val);
                    }
                }
            }
        });

    };
    this.loadMultipleDate = function() {

        MultiselectDate.on('click', function(e) {
            $('.date-list').empty();

            if (MultiselectDate.prop('checked')) {
                if (12 % parseInt(RepeatsEvery.val()) == 0) {
                    len = 12 / parseInt(RepeatsEvery.val());
                    for (i = 0; i < len; i++) {
                        $('.date-list').append(_renderinput.loadDate(i));
                        _renderinput.loadedDateEvent(i);
                    }
                }
                $(".statu-date-label", RecurringPan).show();
            } else {

                $('.date-list').append(_renderinput.loadDate(0));
                _renderinput.loadedDateEvent(0);
                _renderinput.loadDays(0, 1);
            }
        });
    };

    this.loadMonthAndData = function(mainMonObj) {
        sets = this.getMonthAndDataSets();
        mainMonObj.append(this.make_option("Select", ""));
        $.each(sets, function(k, v) {
            opt = _renderinput.make_option(v.m_name, v.m_id);
            mainMonObj.append(opt);
        });
    };
    this.loadFrequency = function() {
        Frequency.empty();
        Frequency.append(
            this.make_option("Select", "")
        );
        $.each(FREQUENCY_INFO, function(ke, val) {
            opt = _renderinput.make_option(val.frequency, val.frequency_id);
            Frequency.append(opt);
        });
    };
    this.clearSubLevel = function(l_position) {
        for (var i = l_position + 1; i < 11; i++) {

            $('.statutory_levelvalue #snl' + i).empty();
        }
    }
    this.loadStatuNames = function(data, l_position) {

        this.clearSubLevel(l_position);
        $.each(data, function(k, v) {
            liObject = $('#templates #statutory-li-template li').clone();

            liObject.attr('id', 'sid' + v.s_id);
            liObject.addClass('slp' + v.l_position);

            $('.sname-holder', liObject).on('click', function() {
                $('.statutory_levelvalue #dv' + v.l_position).val('');
                $('.statutory_levelvalue #dvid' + v.l_position).val('');
                $('.statutory_levelvalue #dvpid' + v.l_position).val('');
                var _s_names = [];
                var _s_pids = [];
                _renderinput.s_id = v.s_id;
                $('.slp' + v.l_position).removeClass('active');
                $('.slp' + v.l_position + ' #select-act').removeClass('fa-check');
                $('#sid' + v.s_id).addClass('active');
                $('#sid' + v.s_id + ' #select-act').addClass('fa-check');
                if (v.p_ids != null) {
                    $.merge(_s_pids, v.p_ids);
                    _renderinput.l_one_id = v.p_ids[0];
                    _renderinput.l_one_name = v.p_maps[0];
                } else {
                    _renderinput.l_one_id = v.s_id;
                    _renderinput.l_one_name = v.s_name;
                }

                if (v.p_maps != null) {
                    $.merge(_s_names, v.p_maps);
                }
                $.merge(_s_names, [v.s_name]);
                _renderinput.s_names = _s_names;
                $.merge(_s_pids, [v.s_id]);
                _renderinput.s_pids = _s_pids;
                _renderinput.last_selected = v.l_position;
                _renderinput.renderStatuNames(v.s_id, v.l_position);
            });
            $('.edit-icon', liObject).on('click', function() {
                $('.txtsname').val('');
                if (v.p_ids == null) {
                    pid = 0;
                } else {
                    pid = v.p_ids[v.p_ids.length - 1];
                }

                $('.statutory_levelvalue #dv' + v.l_position).val(v.s_name);
                $('.statutory_levelvalue #dvid' + v.l_position).val(v.s_id);
                $('.statutory_levelvalue #dvpid' + v.l_position).val(pid);
            });
            $('#sname', liObject).text(v.s_name);
            $('#tbody-statutory-level .statutory_levelvalue #snl' + v.l_position).append(liObject)
        });
    };
    this.renderStatuNames = function(p_id, l_position) {
        var data = []
        $.each(STATUTORY_INFO, function(k, v) {
            if (
                (v.c_id == _renderinput.countryId) &&
                (v.d_id == _renderinput.domainId) &&
                (v.l_position >= l_position)
            ) {
                if (p_id == v.p_id) {
                    if (l_position == v.l_position) {
                        data.push(v);
                    } else {
                        _renderinput.loadStatuNames(data, l_position);
                        data = [];
                        l_position = v.l_position;
                        data.push(v);
                    }
                } else {
                    return;
                }
            }
        });
        _renderinput.loadStatuNames(data, l_position);
    };
    this.loadStatuesLevels = function(loadFromLevel) {
        // $('#tbody-statutory-level').empty();
        if ((this.countryId == null) || (this.domainId == null)) {
            return;
        }
        c_list = STATUTORY_LEVEL_INFO[this.countryId];
        if (!c_list)
            return
        s_list = c_list[this.domainId];
        if (!s_list)
            return
        len = s_list.length;
        // wid = 100/len;
        // if (len > 3) {
        main_wid = 400 * len + 10;
        wid = "360px";
        $("#tab2 #datatable-fixed-header").width(main_wid + 'px');
        // }
        // else {
        //     wid = "30%";
        //     $("#tab2 #datatable-fixed-header").width('100%');
        // }

        $.each(s_list, function(k, v) {
            if (loadFromLevel > v.l_position) {
                return;
            }
            if (v.l_position == 1) {
                _renderinput.level_one_name = v.l_name;
            }

            slObject = $('#templates .statutory_levelvalue').clone();
            slObject.width(wid);

            $('.filter-text-box', slObject).attr(
                'id', 'sf' + v.l_position
            );
            $('.statutory_title', slObject).html(v.l_name);
            $('.filter-text-box', slObject).on(
                'keyup',
                function() {
                    // filter_statutory();
                });
            $('.sname-list', slObject).attr(
                'id', 'snl' + v.l_position
            );

            $('.bottomfield .txtsname', slObject).attr(
                'id', 'dv' + v.l_position
            );
            $('.bottomfield .snameid', slObject).attr(
                'id', 'dvid' + v.l_position
            );
            $('.bottomfield .snamepid', slObject).attr(
                'id', 'dvpid' + v.l_position
            );
            $('.bottomfield .txtsname', slObject).on('input', function(e) {
                this.value = isLegislationChar($(this));
            });

            $('.bottomfield .txtsname', slObject).on(
                'keypress',
                function(event) {
                    if (event.keyCode == 13) {
                        new_value = $('#dv' + v.l_position).val().trim();
                        if (new_value.length == 0) {
                            displayMessage(message.statutory_required);
                            return false;
                        }
                        else {
                            if (!validateMaxLength('statutoryname', new_value, "Statutory Name"))
                                return false;
                        }
                        if ((v.l_position > 1) && (_renderinput.l_one_id == null)) {
                            displayMessage(message.statutory_selection_required);
                            return false;
                        }
                        _sid = $('#dvid' + v.l_position).val();

                        if (_sid == '') {
                            _fetchback.saveStautory(
                                v.l_id, new_value, v.l_position
                            );
                        } else {
                            _fetchback.updateStatutory(
                                parseInt(_sid), new_value, v.l_position
                            );
                        }

                        $('#dv' + v.l_position).val('');
                        $('#dvid' + v.l_position).val('');
                    }
                });

            $('.bottomfield .statut-add', slObject).on(
                'click',
                function() {

                    new_value = $('#dv' + v.l_position).val().trim();
                    if (new_value.length == 0) {
                        displayMessage(message.statutory_required);
                        return false;
                    }
                    else {
                        if (!validateMaxLength('statutoryname', new_value, "Statutory Name"))
                            return false;
                    }
                    if ((v.l_position > 1) && (_renderinput.l_one_id == null)) {
                        displayMessage(message.statutory_selection_required);
                        return false;
                    }
                    _sid = $('#dvid' + v.l_position).val();

                    if (_sid == '') {
                        _fetchback.saveStautory(
                            v.l_id, new_value, v.l_position
                        );
                    } else {
                        _fetchback.updateStatutory(
                            parseInt(_sid), new_value, v.l_position
                        );
                    }

                    $('#dv' + v.l_position).val('');
                    $('#dvid' + v.l_position).val('');
                });

            $('#sf' + v.l_position, slObject).keyup(function() {
                var searchText = $(this).val().toLowerCase();
                $('#snl' + v.l_position + ' > li').each(function() {
                    var currentLiText = $(this).text().toLowerCase(),
                        showCurrentLi = currentLiText.indexOf(searchText) !== -1;
                    $(this).toggle(showCurrentLi);
                });
            });


            $('#tbody-statutory-level').append(slObject);
            if (v.l_position == 1) {
                _renderinput.renderStatuNames(
                    0, v.l_position
                );
            }
        });
    };
    this.renderStatuGrid = function() {
        var j = 1;
        $('.tbody-statutory-list').empty();
        $.each(this.mapped_statu, function(k, v) {
            trObj = $('#templates #statutory-grid-templates .table-row').clone();
            $('.sno', trObj).text(j);
            $('.statutory', trObj).text(v.s_names.join(' >> '));
            $('.remove', trObj).on('click', function() {
                CurrentPassword.val('');
                confirm_alert(message.delete_record, function(isConfirm) {
                    if (isConfirm) {
                        _renderinput.mapped_statu.splice(k, 1);
                        _renderinput.renderStatuGrid();

                    }
                });

            });
            $('.tbody-statutory-list').append(trObj);
            j += 1;
        });
    };
    this.loadMonths = function(freq_val) {
        if (freq_val == 1) {
            $('#otstatutory_month').empty();
            _renderinput.loadMonthAndData($('#otstatutory_month'));
            $('#otstatutory_date').empty();
            $('#otstatutory_date').append(_renderinput.make_option("Select", ''));
            for (var i = 1; i <= 31; i++) {
                dopt = _renderinput.make_option(i, i);
                $('#otstatutory_date').append(dopt);
            }
            $('#otstatutory_month').change(function() {
                $('#otstatutory_date').empty();
                $('#otstatutory_date').append(_renderinput.make_option("Select", ''));
                $.each(_renderinput.getMonthAndDataSets(), function(kk, v) {
                    if (v.m_id == parseInt($('#otstatutory_month').val())) {
                        for (var i = 1; i <= v.range; i++) {
                            dopt = _renderinput.make_option(i, i);
                            $('#otstatutory_date').append(dopt);
                        }
                    }
                });
            });
        } else {
            $('#rcstatutory_month').empty();
            _renderinputs.loadMonthAndData($('#rcstatutory_month'));
            $('#rcstatutory_month').change(function() {
                $('#rcstatutory_date').empty();
                $('#rcstatutory_date').append(_renderinput.make_option("Select", "0"));
                $.each(_renderinput.getMonthAndDataSets(), function(kk, v) {
                    if (v.m_id == parseInt($('#rcstatutory_month').val())) {
                        for (var i = 1; i <= v.range; i++) {
                            dopt = _renderinput.make_option(i, i);
                            $('#rcstatutory_date').append(dopt);
                        }
                    }
                });
            });
        }
    }
    this.loadCompliance = function(data) {

        Provision.val(data.s_provision);
        ComplianceTask.val(data.comp_task);
        Description.val(data.description);
        Document.val(data.doc_name);
        Penal.val(data.p_consequences);
        ReferenceLink.val(data.reference);
        Frequency.val(data.f_id);
        this.hideFrequencyAll();
        this.showFrequencyVal();
        _renderinput.summary = data.summary;
        if (data.f_id == 1) {
            if (data.statu_dates.length > 0) {
                $('#otstatutory_month').val(data.statu_dates[0]['statutory_month']);

                $('#otstatutory_date').empty();
                $('#otstatutory_date').append(_renderinput.make_option("Select", ''));
                $.each(_renderinput.getMonthAndDataSets(), function(kk, v) {
                    if (v.m_id == parseInt($('#otstatutory_month').val())) {
                        for (var i = 1; i <= v.range; i++) {
                            dopt = _renderinput.make_option(i, i);
                            $('#otstatutory_date').append(dopt);
                        }
                    }
                });
                $('#otstatutory_date').val(data.statu_dates[0]['statutory_date']);
                $('#ottriggerbefore').val(data.statu_dates[0]['trigger_before_days']);
            }
        } else if (data.f_id == 5) {
            Duration.val(data.duration);

            DurationType.val(data.d_type_id);
            $('.occasional_summary').text(data.summary);
        } else {

            RepeatsType.val(data.r_type_id);
            RepeatsEvery.val(data.r_every);
            $('.recurr-summary').text(data.summary);
            if (data.statu_dates.length > 1) {
                MultiselectDate.prop('checked', true);
            }
            if (data.r_type_id == 1) {
                // hide repeat by, statutoty date and statutory month
                // show only trigger days
                $('.repeat-by', RecurringPan).hide();
                $(".statu-date-label", RecurringPan).hide();

            } else if (data.r_type_id == 2) {
                $('.multicheckbox', RecurringPan).show();
                $('.repeat-by', RecurringPan).show();
                $(".statu-date-label", RecurringPan).show();
            } else {
                // show month, date annd trigger days
                $('.multicheckbox', RecurringPan).hide();
                $('.repeat-by', RecurringPan).show();
                $(".statu-date-label", RecurringPan).show();
            }


            $('.date-list').empty();
            $.each(data.statu_dates, function(k, v) {

                date_pan = _renderinput.loadDate(k);
                $(".statu-date-div", date_pan).show();
                $(".date-select-div", date_pan).show();
                $(".month-select-div", date_pan).show();

                if (v['repeat_by'] == 1) {
                    $('#singleRadio1').prop('checked', true);
                } else {
                    $('#singleRadio2').prop('checked', true);
                    $(".date-select-div", date_pan).hide();
                }

                if (data.r_type_id == 1) {
                    $(".statu-date-div", date_pan).hide();
                } else if (data.r_type_id == 2) {
                    if (data.statu_dates.length > 1) {
                        $(".month-select-div", date_pan).show();
                    } else {
                        $(".month-select-div", date_pan).hide();
                        if (v['repeat_by'] == 1) {
                            $('.statu-date-div', date_pan).show();
                            $(".statu-date-label", RecurringPan).show();
                        } else {
                            $('.statu-date-div', date_pan).hide();
                            $(".statu-date-label", RecurringPan).hide();
                        }
                    }
                }

                $('.month-select', date_pan).val(v['statutory_month']);
                $('.trigger-value', date_pan).val(v['trigger_before_days']);
                $.each(_renderinput.getMonthAndDataSets(), function(kk, vv) {
                    if (vv.m_id == v["statutory_month"]) {
                        $('.date-select', date_pan).empty();
                        for (var i = 1; i <= vv.range; i++) {
                            opt = _renderinput.make_option(i, i);
                            $('.date-select', date_pan).append(opt);
                        }
                        return false;
                    }
                });
                $('.date-select', date_pan).val(v['statutory_date']);
                $('.date-list').append(date_pan);
                _renderinput.loadedDateEvent(k);
            });

        }
        if (data.is_active == false) {
            Comp_status.val(false);
        }
        else {
            Comp_status.val(true);
        }
        Comp_id.val(data.comp_id);
        if (data.comp_id == null) {
            Temp_id.val(data.temp_id);
        } else {
            Temp_id.val(data.comp_id);
        }

        // display file name
        _renderinput.f_f_list = data.f_f_list;
        if (data.f_f_list.length > 0) {
            var tFN = data.f_f_list[0]['file_name'];
            $('#uploaded_fileview').show();
            $('#uploaded_filename').html(tFN + '   <img src=\'/knowledge/images/close-icon-black.png\' onclick=\'remove_temp_file()\' />');
        }

    };
    this.clearCompliance = function() {
        Provision.val('');
        ComplianceTask.val('');
        Description.val('');
        Document.val('');
        Penal.val('');
        ReferenceLink.val('');
        RepeatsEvery.val('');
        RepeatsType.val();
        Duration.val('');
        DurationType.val('');
        $('#otstatutory_date').val('');
        $('#otstatutory_month').val('');
        $('#ottriggerbefore').val('');

        Comp_id.val('');
        Temp_id.val('');
        Frequency.val('');
        Comp_status.val('');
        $('.frequency-set').empty();
        $('#counter').html('');
        $('#counter1').html('')
        $('#counter2').html('');
        $('#counter3').html('');
        $('#upload_file').val('');
        MultiselectDate.attr('checked', false);
        this.hideFrequencyAll();
        $('#uploaded_fileview').hide();
        _renderinput.f_f_list = [];
        _renderinput.summary = null;

    };
    this.renderComplianceGrid = function() {
        // function showTitle(e) {
        //     // if (e.className == "fa c-pointer inactive-icon fa-times text-danger") {
        //     //     e.title = "Click here to activate";
        //     // } else if (e.className == "fa c-pointer active-icon fa-check text-success") {
        //     //     e.title = "Click here to deactivate";
        //     if (e.className == "fa c-pointer remove fa-trash text-primary") {
        //         e.title = 'Click here to remove compliance';
        //     }
        // }
        $('.tbody-compliance-list').empty();
        var j = 1;

        $.each(_renderinput.mapped_compliances, function(ke, vc) {
            cObj = $('#templates #compliance-templates .table-row').clone();
            $('.sno', cObj).text(j);
            $('.statutory-provision', cObj).text(vc.s_provision);
            $('.task', cObj).text(vc.comp_task);
            $('.description', cObj).text(vc.description);
            $('.frequency', cObj).text(vc.frequency);
            $('.summary-repeats', cObj).text(vc.summary.trim().slice(0, -1));
            $('#edit-icon', cObj).attr('title', 'Click here to edit');
            $('#edit-icon', cObj).on('click', function() {
                if ((vc.comp_id == null) && (vc.temp_id == undefined)) {
                    vc.temp_id = ke;
                }
                _renderinput.loadCompliance(vc);
            });
            $('#status', cObj).removeClass('remove');
            if (vc.comp_id == null) {
                $('#status', cObj).addClass('remove');
                $('#status', cObj).addClass('fa-trash text-primary');
                $('#status', cObj).attr('title', 'Click here to remove compliance');
                $('#status', cObj).on('click', function(e) {
                    if ($('#status', cObj).hasClass('remove')) {
                        statusmsg = message.delete_record;
                        confirm_alert(statusmsg, function(isConfirm) {
                            if (isConfirm) {
                                _renderinput.mapped_compliances.splice(ke, 1);
                                _renderinput.renderComplianceGrid();
                            }
                        });
                    }
                });
            } else {
                $('#status', cObj).removeClass('remove');
                if (vc.is_active == true) {
                    classValue = "active-icon";
                    $('#status', cObj).addClass(classValue);
                    $('#status', cObj).addClass("fa-check text-success");
                    $('#status', cObj).attr('title', 'Click here to Deactivate');
                } else {
                    classValue = "inactive-icon";
                    $('#status', cObj).addClass(classValue);
                    $('#status', cObj).addClass("fa-times text-danger");
                    $('#status', cObj).attr('title', 'Click here to Activate');
                }
                $('#status', cObj).on('click', function(e) {
                    if (vc.is_active == true) {
                        statusmsg = message.deactive_message;
                    } else {
                        statusmsg = message.active_message;
                    }

                    CurrentPassword.val('');
                    confirm_alert(statusmsg, function(isConfirm) {
                        if (isConfirm) {
                            Custombox.open({
                                target: '#custom-modal',
                                effect: 'contentscale',
                                complete: function() {
                                    CurrentPassword.focus();
                                    isAuthenticate = false;
                                },
                                close: function() {
                                    if (isAuthenticate) {
                                         if (vc.is_active == true) {
                                            vc.is_active = false;
                                            statusmsg = message.deactive_message;
                                        } else {
                                            vc.is_active = true;
                                            statusmsg = message.active_message;
                                        }
                                        _renderinput.renderComplianceGrid();
                                    }
                                },
                            });
                            e.preventDefault();
                        }
                    });
                    // _renderinput.renderComplianceGrid();
                });
            }

            // $('#status', cObj).hover(function() {
            //     showTitle(this);
            // });

            $('.tbody-compliance-list').append(cObj);
            j += 1;
        });
    };
    this.clearGeosSubLevel = function(l_position) {
        for (var i = l_position + 1; i < 11; i++) {
            $('.tbody-geography-level #gnl' + i).empty();
        }
    };
    this.unloadGeosNames = function(l_position, p_id) {
        for (var i = l_position + 1; i < 11; i++) {
            // $('.levelvalue #gnl'+i).empty();
            $('#gnl' + i).children().each(function() {
                // var cls = $(this).attr('class').match(/pid[\w,]*\b/);
                var cls = $(this).attr('class');
                if (cls.indexOf(p_id.toString()) > 0) {
                    $(this).remove();
                }

            });
            if ($('#gnl' + i).children().length == 1) {
                $('#gidall' + i).remove();
            }
        }
    };
    this.loadGeosNames = function(data, l_position, parent_name) {
        // select all functionality
        function geo_select_all(g_l_position) {
            saved_geos = $('.items', '#gnl' + g_l_position);
            // add as a first element
            if (saved_geos.length == 0) {
                liObject = $('#templates #list-template li').clone();
                liObject.addClass('select-all');
                liObject.attr('id', 'gidall' + g_l_position);
                $('.name-holder', liObject).text('Select all');
                $('.tbody-geography-level #gnl' + g_l_position).append(liObject)
                liObject.on('click', function() {
                    if ($('#gidall' + g_l_position).hasClass('active')) {
                        $('#gidall' + g_l_position).removeClass('active');
                        $('#gidall' + g_l_position + ' i').removeClass('fa-check');
                        // _renderinput.clearGeosSubLevel(g_l_position);
                        _renderinput.selected_geos_parent = [];
                        $.each($('#gnl' + g_l_position + ' li'), function(k, v) {
                            $(this).removeClass('active');
                            $(this).find('i').removeClass('fa-check');
                            _tpid = $(this).val();
                            _renderinput.unloadGeosNames(g_l_position, _tpid);
                        });

                    } else {
                        $('#gidall' + g_l_position).addClass('active');
                        $('#gidall' + g_l_position + ' i').addClass('fa-check');
                        check_gids = [];
                        load_g_ids = [];
                        $.each($('#gnl' + g_l_position + ' li'), function(k, v) {
                            val = $(this).val();
                            if ($(this).hasClass('active')) {
                                check_gids.push(val);
                            } else {
                                load_g_ids.push(val);
                            }
                            $(this).addClass('active');
                            $(this).find('i').addClass('fa-check');
                        });

                        // _renderinput.clearGeosSubLevel(g_l_position);
                        _renderinput.renderAllGeoNames(g_l_position, check_gids, load_g_ids);
                    }
                });
            }
        }

        // this.clearGeosSubLevel(l_position);
        $.each(data, function(k, v) {
            if (v.is_active == false) {
                return;
            }
            // select all
            geo_select_all(v.l_position);

            liObject = $('#templates #list-template li').clone();
            liObject.attr('id', 'gid' + v.g_id);
            // liObject.addClass('glp'+v.l_position);

            liObject.addClass('pid' + v.p_ids.toString());
            liObject.val(v.g_id);
            liObject.attr('name', v.p_ids);
            liObject.on('click', function() {
                if ($('#gid' + v.g_id).hasClass('active')) {
                    $('#gid' + v.g_id).removeClass('active');
                    $('#gid' + v.g_id + ' i').removeClass('fa-check');
                    $('#gidall' + v.l_position).removeClass('active');
                    $('#gidall' + v.l_position + ' i').removeClass('fa-check');
                    _renderinput.unloadGeosNames(v.l_position, v.g_id);
                } else {
                    $('#gid' + v.g_id).addClass('active');
                    $('#gid' + v.g_id + ' i').addClass('fa-check');
                    _renderinput.renderGeosNames(v.g_id, v.l_position, v.g_name);
                }

            });
            $('.name-holder', liObject).text(v.g_name);
            if ((v.l_position > 1) && (k == 0)) {
                $('.tbody-geography-level #gnl' + v.l_position).append(
                    '<h3 class=' + "head" + v.p_ids + ' style="background-color:gray;padding:2px;font-size:13px;color:white;">' + parent_name + '</h3>'
                );
            }
            $('.tbody-geography-level #gnl' + v.l_position).append(liObject)

            if (_renderinput.selected_geos_parent.indexOf(v.g_id) > -1) {

                $('#gid' + v.g_id).addClass('active');
                $('#gid' + v.g_id + ' i').addClass('fa-check');
                _renderinput.renderGeosNames(v.g_id, v.l_position, v.g_name);
            }

        });
    };
    this.renderGeosNames = function(p_id, l_position, parent_name) {
        var data = []

        $.each(GEOGRAPHY_INFO, function(k, v) {
            if (v.c_id == _renderinput.countryId) {
                if (p_id == v.p_id) {
                    if (l_position == v.l_position) {
                        data.push(v);
                    } else {
                        _renderinput.loadGeosNames(data, l_position, parent_name);
                        data = [];
                        l_position = v.l_position;
                        data.push(v);
                    }
                } else {
                    return;
                }
            }
        });
        _renderinput.loadGeosNames(data, l_position, parent_name);
    };
    this.loadGeosLevels = function(loadFromLevel) {
        if (this.countryId == null) {
            return;
        }
        $.each(GEOGRAPHY_LEVEL_INFO, function(k, v) {
            if (loadFromLevel > v.l_id) {
                return;
            }
            if (_renderinput.countryId != v.c_id) {
                return;
            }

            slObject = $('#templates #geography-level-templates').clone();
            $('.title', slObject).html(v.l_name);

            $('.gname-list', slObject).attr(
                'id', 'gnl' + v.l_position
            );
            $('.geo-name-filter', slObject).attr('id', 'gnf' + v.l_position);
            $('.geo-name-filter', slObject).attr('placeholder', v.l_name);

            $('#gnf' + v.l_position, slObject).keyup(function() {
                var searchText = $(this).val().toLowerCase();
                $('#gnl' + v.l_position + ' > li').each(function() {
                    var currentLiText = $(this).text().toLowerCase(),
                        showCurrentLi = currentLiText.indexOf(searchText) !== -1;
                    $(this).toggle(showCurrentLi);
                });
            });

            $('.tbody-geography-level').append(slObject);

        });
    };

    this.renderAllGeoNames = function(l_position, loaded_gids, load_g_ids) {
        $.each(GEOGRAPHY_INFO, function(k, v) {
            if (v.c_id == _renderinput.countryId) {
                if ((v.l_position == l_position) && (load_g_ids.indexOf(v.g_id) != -1)) {
                    // $('#gnl'+l_position).empty();
                    if (loaded_gids.indexOf(v.g_id) == -1) {
                        _renderinput.renderGeosNames(v.g_id, v.l_position, v.g_name);
                    }
                }
            }
        });
    };

    this.hideFrequencyAll = function() {
        Onetimepan.hide();
        RecurringPan.hide();
        OccasionalPan.hide();
    };

    this.showFrequencyVal = function() {
        var freq_val = Frequency.val();
        if (freq_val == '') {
            this.hideFrequencyAll();
        } else {
            // $('.frequency-set').empty();
            if (freq_val == 1) {
                Onetimepan.show();
                _renderinput.loadMonths(freq_val);
            } else if (freq_val == 5) {
                $('.date-list').empty();
                MultiselectDate.attr('checked', false);
                OccasionalPan.show();
                DurationType.empty();
                DurationType.append(
                    _renderinput.make_option("Select", "")
                );
                $.each(DURATION_INFO, function(ke, val) {
                    DurationType.append(
                        _renderinput.make_option(
                            val.duration_type, val.duration_type_id
                        )
                    );
                });
                DurationType.keyup(function(e) {
                    e.preventDefault();
                    _renderinput.occasionalSummary();

                });
                $('#duration_type').change(function() {
                    _renderinput.occasionalSummary();
                });

            } else {
                $('.recurr-summary').text('');
                RepeatsEvery.val('');
                MultiselectDate.prop('checked', false);
                $('#singleRadio1').prop('checked', true);
                RecurringPan.show();
                if (freq_val == 2) {
                    txt = "Periodical";
                    $('.mandatory', RecurringPan).show();
                } else if (freq_val == 3) {
                    txt = "Review";
                    $('.mandatory', RecurringPan).show();
                } else {
                    txt = "Flexi Review";
                    $('.mandatory', RecurringPan).hide();
                }
                $('.header-title', RecurringPan).html(txt);
                _renderinput.loadRepeats();
                $('.date-list').empty();
                date_pan = _renderinput.loadDate(0)
                $('.date-list').append(date_pan);
                _renderinput.loadedDateEvent(0);
            }

        }
    };

    this.occasionalSummary = function() {
        d_select = $('#duration_type option:selected');
        if ((DurationType.val() != '') && (Duration.val() != '')) {
            _renderinput.summary = "To complete within " + Duration.val() + " " + d_select.text();
            $('.occasional_summary').text(_renderinput.summary);
        } else {
            _renderinput.summary = '';
            $('.occasional_summary').text(_renderinput.summary);

        }
    };

}

function showTab() {
    hideall = function() {
        // $('.setup-panel li').addClass('disabled');
        $('.statutory_mapping_tab li').removeClass('active');
        $('.tab-pane').removeClass('active in');
        $('#tab1').hide();
        $('#tab2').hide();
        $('#tab3').hide();
        $('#tab4').hide();
        SaveButton.hide();
        SubmitButton.hide();
        NextButton.hide();
        PreviousButton.hide();
    }

    enabletabevent = function(tab) {
        if (tab == 1) {
            $('.tab-step-1 a').attr('href', '#tab1');
        } else if (tab == 2) {
            $('.tab-step-2 a').attr('href', '#tab2');
        } else if (tab == 3) {
            $('.tab-step-3 a').attr('href', '#tab3');
        } else if (tab == 4) {
            $('.tab-step-4 a').attr('href', '#tab4');
        }
    }
    disabletabevent = function() {
        $('.tab-step-1 a').removeAttr('href');
        $('.tab-step-2 a').removeAttr('href');
        $('.tab-step-3 a').removeAttr('href');
        $('.tab-step-4 a').removeAttr('href');
    }

    if (CURRENT_TAB == 1) {
        hideall();
        disabletabevent();
        enabletabevent(1);
        $('.tab-step-1').addClass('active')
        $('#tab1').addClass("active in");
        $('#tab1').show();
        NextButton.show();
        _viewPage.showFirstTab();
    } else if (CURRENT_TAB == 2) {
        if (!_viewPage.validateFirstTab()) {
            CURRENT_TAB -= 1;
            return false;
        }
        hideall();
        enabletabevent(2);
        $('.tab-step-2').addClass('active')
        $('#tab2').addClass('active in');
        $('#tab2').show();
        NextButton.show();
        PreviousButton.show();
        _viewPage.showSecondTab();
    } else if (CURRENT_TAB == 3) {
        if (!_viewPage.validateSecondTab()) {
            CURRENT_TAB -= 1;
            return false;
        }
        hideall();
        enabletabevent(3);
        $('.tab-step-3').addClass('active')
        $('#tab3').addClass('active in');
        $('#tab3').show();
        if (compliance_edit == true) {
            NextButton.hide();
            PreviousButton.hide();
            SaveButton.show();
            SubmitButton.show();
        } else {
            NextButton.show();
            PreviousButton.show();
            SaveButton.hide();
            SubmitButton.hide();
        }

        _viewPage.showThirdTab();
    } else if (CURRENT_TAB == 4) {
        if (_renderinput.mapped_compliances.length == 0) {
            displayMessage(message.compliance_selection_required);
            CURRENT_TAB -= 1;
            return false;
        }

        hideall();
        enabletabevent(4);
        $('.tab-step-4').addClass('active')
        $('#tab4').addClass('active in');
        $('#tab4').show();

        SubmitButton.show();
        PreviousButton.show();
        SaveButton.show();
        _viewPage.showFouthTab();
    }
}

_renderinput = new RenderInput();
_fetchback = new FetchBack();
_listPage = new ListPage();
_viewPage = new ViewPage();

function pageControls() {
    AddButton.click(function() {
        _renderinput.resetField();
        showTab();
        _listPage.hide();
        _viewPage.show();

    });
    NextButton.click(function() {
        CURRENT_TAB += 1;
        showTab();
        _renderinput.l_one_id = null;
    });
    PreviousButton.click(function() {
        CURRENT_TAB = CURRENT_TAB - 1;
        showTab();
    });
    AddStatuButton.click(function() {
        if (_renderinput.s_id == null) {
            displayMessage(message.statutory_selection_required);
            return false;
        }
        // if (_renderinput.mapped_statu.length >= 3) {
        //     displayMessage(message.statutory_selection_exceed);
        //     return false;
        // }
        info = {};
        info['s_id'] = _renderinput.s_id;
        info['s_names'] = _renderinput.s_names;
        info['l_one_id'] = _renderinput.l_one_id;
        add_new = true;
        differnt_level = false;
        $.each(_renderinput.mapped_statu, function(k, v) {
            if (v.s_id == _renderinput.s_id) {
                add_new = false;
            }
            if (v.l_one_id != _renderinput.l_one_id) {
                differnt_level = true;
            }
        });
        if (differnt_level) {
            displayMessage(message.invalid_levelone + _renderinput.l_one_name + " should not be selected in first level");
        } else {
            if (add_new) {
                _renderinput.mapped_statu.push(info)
                _renderinput.renderStatuGrid();
            } else {
                displayMessage(message.statutory_already_added);
            }
        }
    });

    Frequency.change(function() {
        _renderinput.hideFrequencyAll();
        _renderinput.showFrequencyVal();
    });
    ComplianceTask.on('input', function(e) {
        this.value = isAllowSpecialChar($(this));
    });
    Document.on('input', function(e) {
        this.value = isCommon($(this));
    });
    Description.keyup(function(e) {
        countDown = $('#counter');
        var mxlength = 500;
        var txtlen = this.value.length;
        if (mxlength < txtlen) {
            countDown.html(message.should_not_exceed + mxlength + "characters");
            this.value = this.value.substring(0, mxlength);
            e.preventDefault();
        } else {
            countDown.html(mxlength - txtlen + "characters");
        }
    });
    Description.on('input', function(e) {
        this.value = isAllowSpecialChar($(this));
    });
    Provision.on('input', function(e) {
        this.value = isAllowSpecialChar($(this));
    });
    Provision.keyup(function(e) {
        countDown = $('#counter1');
        var mxlength = 500;
        var txtlen = this.value.length;
        if (mxlength < txtlen) {
            countDown.html(message.should_not_exceed + mxlength + "characters");
            this.value = this.value.substring(0, mxlength);
            e.preventDefault();
        } else {
            countDown.html(mxlength - txtlen + "characters");
        }
    });
    Penal.on('input', function(e) {
        this.value = isAllowSpecialChar($(this));
    });
    Penal.keyup(function(e) {
        countDown = $('#counter2');
        var mxlength = 500;
        var txtlen = this.value.length;
        if (mxlength < txtlen) {
            countDown.html(message.should_not_exceed + mxlength + "characters");
            this.value = this.value.substring(0, mxlength);
            e.preventDefault();
        } else {
            countDown.html(mxlength - txtlen + "characters");
        }
    });


    ReferenceLink.keyup(function(e) {
        countDown = $('#counter3');
        var mxlength = 500;
        var txtlen = this.value.length;
        if (mxlength < txtlen) {
            countDown.html(message.should_not_exceed + mxlength + "characters");
            this.value = this.value.substring(0, mxlength);
            e.preventDefault();
        } else {
            countDown.html(mxlength - txtlen + "characters");
        }
    });

    AddComplianceButton.click(function() {
        if (!_viewPage.validateComplianceTabTextLength()) {
            return false;
        }

        if (!_viewPage.validateComplianceTab()) {
            return false;
        }

        if ((compliance_edit == true) && (Comp_id.val() == '')) {
            displayMessage(message.cannot_add_compliance_inedit);
            return false;
        }

        _renderinput.statu_dates = [];
        info = {};

        if (Comp_id.val() == '')
            info['comp_id'] = null;
        else
            info['comp_id'] = parseInt(Comp_id.val());
        if (Temp_id.val() == '')
            info['temp_id'] = parseInt(_renderinput.mapped_compliances.length + 1);
        else
            info['temp_id'] = parseInt(Temp_id.val());


        info['s_provision'] = Provision.val().replace( /\s\s+/g, ' ' ).trim();
        info['comp_task'] = ComplianceTask.val().replace( /\s\s+/g, ' ' ).trim();
        info['description'] = Description.val().replace( /\s\s+/g, ' ' ).trim();
        info['doc_name'] = Document.val().trim();

        info['p_consequences'] = Penal.val().replace( /\s\s+/g, ' ' ).trim();
        info['reference'] = ReferenceLink.val().trim();
        info['f_id'] = parseInt(Frequency.val());
        info['d_type_id'] = null;
        info['duration'] = null;
        info['r_type_id'] = null;
        info['r_every'] = null;
        is_all_true = true;
        _renderinput.statu_dates = [];
        if (Frequency.val() == 5) {

            info['d_type_id'] = parseInt(DurationType.val());
            info['duration'] = parseInt(Duration.val());
        } else if (
            (Frequency.val() == 2) ||
            (Frequency.val() == 3) ||
            (Frequency.val() == 4)
        ) {

            info['r_type_id'] = null;
            info['r_every'] = null;
            if (RepeatsEvery.val() != '') {
                info['r_every'] = parseInt(RepeatsEvery.val());
            }
            if (RepeatsType.val() != '') {
                info['r_type_id'] = parseInt(RepeatsType.val());
            }

            if (info["r_type_id"] == 2) {
                if (info['r_every'] > 99) {
                    displayMessage(message.months_maximum);
                    return false;
                }
            } else if (info["r_type_id"] == 3) {
                if (info['r_every'] > 9) {
                    displayMessage(message.years_maximum);
                    return false;
                }
            } else {
                if (info['r_every'] > 999) {
                    displayMessage(message.days_maximum);
                    return false;
                }
            }

            date_list = [];
            repeat_by = $("input[name='radioSingle1']:checked").val();
            repeat_by = parseInt(repeat_by);

            mons = []
            dats = []
            temp_dates = []
            date_empty = false;
            is_dup_date = false;
            $(".statu-date-pan").each(function(idx, val) {
                if (RepeatsType.val() == 1) {
                    if ($('.trigger-value', '#dt' + idx).val() == undefined) {
                        return false;
                    }
                } else {
                    // if ((MultiselectDate.prop('checked') == true) && ($('.date-select', '#dt'+idx).val() == undefined)){
                    if ($('.date-select', '#dt' + idx).val() == undefined) {
                        return false;
                    }
                }

                statu = {};
                statu['statutory_date'] = null;
                statu['statutory_month'] = null;
                statu['trigger_before_days'] = null;
                statu['repeat_by'] = null;

                if (repeat_by == 1) {
                    dt = $(".date-select", '#dt' + idx).val();
                } else {
                    dt = $(".date-select option:last", '#dt' + idx).val();
                }
                mon = $(".month-select", this).val();
                trig = $(".trigger-value", this).val();
                if (trig != '')
                    trig = parseInt(trig);
                if ((RepeatsType.val() == 1) && (RepeatsEvery.val() < trig)) {
                    // validate trigger before days
                    displayMessage(message.invalid_triggerbefore);
                    is_all_true = false;

                }
                if ((RepeatsType.val() == 2) && ((RepeatsEvery.val() * 30) < trig)) {
                    displayMessage(message.invalid_triggerbefore);
                    is_all_true = false;
                }

                statu['repeat_by'] = repeat_by;
                if (dt == null) {
                    dt = '';
                }
                if (dt != '') {
                    dt = parseInt(dt);
                    statu['statutory_date'] = dt;
                } else {
                    if (MultiselectDate.prop('checked') == true) {
                        displayMessage(message.statsutorydate_triggerdte_mandatory_multipleinputs)
                        _renderinput.statu_dates = [];
                        is_all_true = false;
                    }
                }
                if (mon == null) {
                    mon = '';
                }
                if (mon != '') {
                    mon = parseInt(mon);
                    statu['statutory_month'] = mon;
                } else {
                    if (MultiselectDate.prop('checked') == true) {
                        displayMessage(message.statutorydate_triggerdte_mandatory_multipleinputs)
                        _renderinput.statu_dates = [];
                        is_all_true = false;
                    }
                }
                if (trig == null) {
                    trig = '';
                }
                if (trig != '') {
                    if (trig == 0) {
                        displayMessage(message.triggerbefore_iszero);
                        is_all_true = false;
                    } else if (trig > 100) {
                        displayMessage(message.triggerbefore_exceed);
                        is_all_true = false;
                    }
                    statu['trigger_before_days'] = parseInt(trig)
                } else {
                    if (MultiselectDate.prop('checked') == true) {
                        displayMessage(message.statutorydate_triggerdte_mandatory_multipleinputs)
                        _renderinput.statu_dates = []
                        is_all_true = false;
                    }
                }
                _renderinput.statu_dates.push(statu);
                $.each(temp_dates, function(x, y) {
                    if (y == (mon + '-' + dt)) {
                        is_dup_date = true;
                    }
                });
                temp_dates.push(mon + "-" + dt);
            });

            if (is_all_true == false) {
                return false;
            }

            if (is_dup_date == true) {
                displayMessage(message.statudate_duplicate);
                return false;
            }
        } else {

            statu = {};
            statu['statutory_date'] = null;
            statu['statutory_month'] = null;
            statu['trigger_before_days'] = null;
            statu['repeat_by'] = null;

            dt = $('#otstatutory_date').val();
            mon = $('#otstatutory_month').val();
            trig = $('#ottriggerbefore').val();

            if (dt != '') {
                statu['statutory_date'] = parseInt(dt);
            }
            if (mon != '') {
                statu['statutory_month'] = parseInt(mon);
            }
            if (trig != '') {
                if (trig == 0) {
                    displayMessage(message.triggerbefore_iszero);
                    return false;
                } else if (trig > 100) {
                    displayMessage(message.triggerbefore_exceed);
                    return false;
                }
                statu['trigger_before_days'] = parseInt(trig)
            }
            _renderinput.statu_dates.push(statu);
        }
        if (is_all_true == false) {
            return false;
        }


        if ((MultiselectDate.prop('checked') == true) && (_renderinput.statu_dates.length == 0)) {
            displayMessage(message.statutorydate_triggerdte_mandatory_multipleinputs)
            return false;
        }
        if((Comp_status.val() === false) || (Comp_status.val() === "false")) {
            info['is_active'] = false;
        }
        else {
            info['is_active'] = true;
        }

        info['statu_dates'] = _renderinput.statu_dates;

        info['frequency'] = $('#compliance_frequency option:selected').text();
        if (info["f_id"] == 1) {
            info['summary'] = "";
        }
        else {
            info['summary'] = _renderinput.summary;
        }
        fCId = info['temp_id'];
        info['f_f_list'] = _renderinput.f_f_list;
        info['is_file_removed'] = _renderinput.file_removed;
        temp_dates = [];

        if (_renderinput.uploaded_files.length > 0) {
            f_list = {};
            var file_data = _renderinput.uploaded_files[0];
            var fullname = _renderinput.uploaded_files[0].name;
            var fN = fullname.substring(0, fullname.indexOf('.'));
            var fE = fullname.substring(fullname.lastIndexOf('.') + 1);
            var uniqueId = Math.floor(Math.random() * 90000) + 10000;
            f_Name = fN + '-' + uniqueId + '.' + fE;

            _renderinput.form_data.append('file' + fCId, file_data, f_Name);
            // _renderinput.form_data.append('session_token', mirror.getSessionToken());
            _renderinput.uploaded_files_fcids[fCId] = true;
            f_list['file_size'] = file_data.size;
            f_list['file_name'] = f_Name;
            f_list['file_content'] = null;
            info['f_f_list'] = [f_list];
        } else {
            _renderinput.uploaded_files_fcids[fCId] = false;
        }

        is_duplidate = false

        var deleted_index = null;

        $.each(_renderinput.mapped_compliances, function(k, v) {
            console.log(k)
            if (
                (v.s_provision == Provision.val().trim()) &&
                (v.comp_task.toLowerCase() == ComplianceTask.val().trim().toLowerCase()) &&
                ((Comp_id.val().trim() == '' && Temp_id.val() != v.temp_id) || (Comp_id.val().trim() != '' && Comp_id.val().trim() != v.comp_id))
            ) {
                displayMessage(message.compliancetask_duplicate);
                is_duplidate = true;
                return false;
            }
        });

        if (Temp_id.val() != '') {
            // $.each(_renderinput.mapped_compliances, function(k, v) {
            for (var i = 0; i < _renderinput.mapped_compliances.length; i++) {
                k = i;
                v = _renderinput.mapped_compliances[i];

                compid = v.comp_id;
                if (compid == null)
                    compid = '';
                // console.log(Temp_id.val(), + ", " + Comp_id.val() + ", " + v.temp_id);
                // if ((Temp_id.val() == Comp_id.val()) || (Temp_id.val() == v.temp_id)) {
                if ((v.comp_id == null && Temp_id.val() == v.temp_id) || (Temp_id.val() == v.comp_id)) {
                    // if (Temp_id.val() == v.comp_id) {
                    _renderinput.mapped_compliances.splice(k, 1);
                    deleted_index = k;
                    break;
                }
            }
        }


        if (!is_duplidate) {
            if (deleted_index == null) {
                _renderinput.mapped_compliances.push(info);
            } else {
                _renderinput.mapped_compliances.splice(deleted_index, 0, info);
            }

            _renderinput.renderComplianceGrid();
            _renderinput.clearCompliance();
            deleted_index = null;
        }
    });

    SaveButton.click(function() {
        displayLoader();
        IS_SAVE = true;
        map_data = _viewPage.make_data_format(0);
        if (map_data == false) {
            hideLoader();
            displayMessage(message.location_selection_required);
            return false;
        }
        if (compliance_edit == false) {
            if (IS_EDIT)
                _fetchback.updateMapping(map_data);
            else {
                _fetchback.saveMapping(map_data);
            }
        } else {
            _fetchback.updateOnlyCompliance(map_data);
        }


    });

    SubmitButton.click(function() {
        displayLoader();
        IS_SAVE = false;
        map_data = _viewPage.make_data_format(1);
        if (map_data == false) {
            hideLoader();
            displayMessage(message.location_selection_required);
            return false;
        }
        if (compliance_edit == false) {
            if (IS_EDIT)
                _fetchback.updateMapping(map_data);
            else {
                _fetchback.saveMapping(map_data);
            }
        } else {
            _fetchback.updateOnlyCompliance(map_data);
        }
    });

    BackButton.click(function() {
        _renderinput.resetField();
        _viewPage.hide();
        _listPage.show();

    });

    $(".radio-class").click(function() {
        selected_val = $("input[name='radioSingle1']:checked").val();
        if (selected_val == 1) {
            $(".date-list").each(function() {
                $(".date-select", this).show();
                $(".date-select-div", this).show();
                if ((RepeatsType.val() == 2) && (MultiselectDate.prop('checked') == false)) {
                    $(".statu-date-div", this).show();
                }
            });
            if ((RepeatsType.val() == 2) && (MultiselectDate.prop('checked') == false)) {
                $(".statu-date-label", RecurringPan).show();
            }
        } else {
            $(".date-list").each(function() {
                $(".date-select", this).hide();
                $(".date-select-div", this).hide();
                if ((RepeatsType.val() == 2) && (MultiselectDate.prop('checked') == false)) {
                    $(".statu-date-div", this).hide();
                }
            });
            if ((RepeatsType.val() == 2) && (MultiselectDate.prop('checked') == false)) {
                $(".statu-date-label", RecurringPan).hide();
            } else if ((RepeatsType.val() == 2) && (MultiselectDate.prop('checked') == true)) {
                $(".statu-date-label", RecurringPan).show();
            }
        }
    });

    approveStatusUL.click(function(event) {
        approveStatusLI.each(function(index, el) {
            $(el).removeClass('active');
        });

        $(event.target).parent().addClass('active');
        approveStatusText.text($(event.target).text());
        _renderinput.show_map_count = 0;
        _renderinput.mapping_id = [];
        _on_current_page = 1;
        x = 1;
        j = 1;
        // _fetchback.createPageView();
        _fetchback.getMappedList();
        // searchStatus.removeClass();
        // searchStatus.addClass('fa');
        // searchStatus.text('All');
    });

    PasswordSubmitButton.click(function() {
        _fetchback.validateAuthentication();
    });
    
    $('#ottriggerbefore').on('input', function(e) {
        //this.value = isNumbers($(this));
        isNumbers(this);
    });

    RepeatsEvery.on('input', function(e) {
        //this.value = isNumbers($(this));
        isNumbers(this);
        MultiselectDate.attr('checked', false);
        $('.multicheckbox').hide();
        // $('.date-list').empty();
        $('.recurr-summary').empty();
        _renderinput.loadedDateEvent(0);
        _renderinput.changeRepeatType();
        _renderinput.loadRepeats();

    });
    Duration.on('input', function(e) {
        //this.value = isNumbers($(this));
        isNumbers(this);
        _renderinput.occasionalSummary();
    });

    filterBox.keyup(function() {
        _listPage.listFilter();
    });

    searchStatusUi.click(function(event) {
        searchStatusLi.each(function(index, el) {
            $(el).removeClass('active');
        });
        $(event.target).parent().addClass('active');

        var currentClass = $(event.target).find('i').attr('class');
        searchStatus.removeClass();
        if (currentClass != undefined) {
            searchStatus.addClass(currentClass);
            searchStatus.text('');
        } else {
            searchStatus.addClass('fa');
            searchStatus.text('All');
        }
        _renderinput.show_map_count = 0;
        _renderinput.mapping_id = [];
        _on_current_page = 1;
        x = 1;
        j = 1;
        _fetchback.getMappedList();
        // _listPage.listFilter();
    });

    $('#ct-search').keyup(function() {
        var searchText = $(this).val().toLowerCase();
        $('#country > li').each(function() {
            var currentLiText = $(this).text().toLowerCase(),
                showCurrentLi = currentLiText.indexOf(searchText) !== -1;
            $(this).toggle(showCurrentLi);
        });
    });

    $('#dt-search').keyup(function() {
        var searchText = $(this).val().toLowerCase();
        $('#domain > li').each(function() {
            var currentLiText = $(this).text().toLowerCase(),
                showCurrentLi = currentLiText.indexOf(searchText) !== -1;
            $(this).toggle(showCurrentLi);
        });
    });

    $('#orglist-search').keyup(function() {
        var searchText = $(this).val().toLowerCase();
        $('#industry > li').each(function() {
            var currentLiText = $(this).text().toLowerCase(),
                showCurrentLi = currentLiText.indexOf(searchText) !== -1;
            $(this).toggle(showCurrentLi);
        });
    });

    $('#naturelist-search').keyup(function() {
        var searchText = $(this).val().toLowerCase();
        $('#statutorynature > li').each(function() {
            var currentLiText = $(this).text().toLowerCase(),
                showCurrentLi = currentLiText.indexOf(searchText) !== -1;
            $(this).toggle(showCurrentLi);
        });
    });

    $('#upload_file').on('change', function(e) {
        var tFN = this.files[0].name;
        var fN = tFN.substring(0, tFN.indexOf('.'));
        var fE = tFN.substring(tFN.lastIndexOf('.') + 1);
        f_Size = this.files[0].size;
        if (tFN.indexOf('.') !== -1) {
            if (f_Size > max_limit) {
                displayMessage(message.file_maxlimit_exceed);
                $('#uploaded_fileview').hide();
                $('#uploaded_filename').html('');
                $('#upload_file').val('');
            } else if (file_type.indexOf(fE.toLowerCase()) < 0) {
                displayMessage(message.invalid_file_format);
                $('#uploaded_fileview').hide();
                $('#uploaded_filename').html('');
                $('#upload_file').val('');
            } else {
                _renderinput.uploaded_files = e.target.files;
                _renderinput.file_removed = false;
                $('#uploaded_fileview').show();
                $('#uploaded_filename').html(tFN + '  <img src=\'/knowledge/images/close-icon-black.png\' onclick=\'remove_temp_file()\' />');
            }
        } else {
            displayMessage(message.invalid_file_format);
            $('#uploaded_fileview').hide();
            $('#uploaded_filename').html('');
            $('#upload_file').val('');
        }
    });

    $('#items_per_page').on('change', function(e) {
        // t_this.perPage = parseInt($(this).val());
        // t_this._sno = 0;
        _on_current_page = 1;
        _fetchback.createPageView();
        _fetchback.getMappedList();
    });


}

function remove_temp_file(edit_id) {
    _renderinput.form_data.delete('file' + edit_id);
    $.each(_renderinput.uploaded_files_fcids, function(k, v) {
        if (k == edit_id) {
            delete k;
        }
    });
    _renderinput.file_removed = true;
    $('#uploaded_fileview').hide();
    $('#uploaded_filename').html('');
    $('#upload_file').val('');
}

function initialize() {
    _listPage.show();
    _fetchback.getMasterData();
    _fetchback.getStatuMaster(0);
    pageControls();
}

$(document).ready(function() {
    $('html').offset().top;
    loadItemsPerPage();
    initialize();
    $(".table-fixed").stickyTableHeaders();
});
