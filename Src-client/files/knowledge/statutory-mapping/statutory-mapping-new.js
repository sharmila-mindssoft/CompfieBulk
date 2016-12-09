
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
IS_EDIT = false;
// controls
Spin_pan = $('.loading-indicator-spin');

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
ComplianceTask = $('#compliance_task');
Provision = $('#statutory_provision');
Description = $('#compliance_description');
Document = $('#compliance_document');
Format = $('#upload_file');
Penal = $('#penal_consequences');
ReferenceLink = $('#reference_link');
Comp_id = $('#comp_id');
Temp_id = $('#temp_id');



//buttons
AddButton = $('#btn-add');

NextButton = $('#btn-next');
PreviousButton = $('#btn-previous');
SubmitButton = $("#btn-submit");
BackButton = $("#btn-back");
SaveButton = $("#btn-save");

AddStatuButton = $('#temp_addstatutories');
AddComplianceButton = $('#temp_addcompliance');

ListScreen = $('#statutorymapping-view');
ViewScreen = $('#statutorymapping-add');

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
        displayMessage(msg.statutoryname_exists);
    }
    else if ( err == "ComplianceNameAlreadyExists") {
        displayMessage(msg.compliancename_exists + extra_details);
    }
    else if (err = "TransactionExists") {
        displayMessage(msg.transaction_exists);
    }
    else {
        displayMessage(err);
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
    this.selected_geos_parent=[];
    this.child_geos= [];
    this.selected_sids = [];
    this.selected_iids = [];
    this.mapping_id = null;

    this.remveItemFromList = function(item, mainlist) {
        if (!mainlist)
            return;
        idx = mainlist.indexOf(item);
        if (idx != -1)
            mainlist.splice(idx, 1);
        return mainlist;
    };

    this.make_option = function (oname, oid) {
        opt = $('<option></option>');
        opt.val(oid);
        opt.html(oname);
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
        this.selected_geos_parent=[];
        this.child_geos= [];
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
    };
    this.getMonthAndDataSets = function() {
        return [
            {'m_id': 1, 'm_name': 'Jan', 'range':31},
            {'m_id': 2, 'm_name': 'Feb', 'range': 28},
            {'m_id': 3, 'm_name': 'Mar', 'range': 31},
            {'m_id': 4, 'm_name': 'Apr', 'range': 30},
            {'m_id': 5, 'm_name': 'May', 'range': 31},
            {'m_id': 6, 'm_name': 'Jun', 'range': 30},
            {'m_id': 7, 'm_name': 'Jul', 'range': 31},
            {'m_id': 8, 'm_name': 'Aug', 'range': 31},
            {'m_id': 9, 'm_name': 'Sep', 'range': 30},
            {'m_id': 10, 'm_name': 'Oct', 'range': 31},
            {'m_id': 11, 'm_name': 'Nov', 'range': 30},
            {'m_id': 12, 'm_name': 'Dec', 'range': 31}
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
            cObject.attr('id', 'c'+val.c_id);

            cObject.on('click', function(cObject) {
                $('.countrylist').removeClass('active');
                $('.countrylist i').removeClass('fa-check');
                _renderinput.country_id = val.c_id;
                _renderinput.country_name = val.c_name;
                _renderinput.loadDomain(val.c_id);
                _renderinput.loadNature(val.c_id);
                $('#c'+val.c_id).addClass('active');
                $('#c'+val.c_id + ' i').addClass("fa-check");
            });
            $('.name-holder', cObject).text(val.c_name);
            Country.append(cObject);
            if(_renderinput.country_id == val.c_id)
            {
                $('#c'+val.c_id).addClass('active');
                $('#c'+val.c_id + ' i').addClass("fa-check");
                _renderinput.loadDomain(_renderinput.country_id);
                _renderinput.loadNature(_renderinput.country_id);
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
            dObject.attr('id', 'd'+val.d_id);
            dObject.on('click', function() {
                $(".domainlist").removeClass('active');
                $(".domainlist i").removeClass('fa-check');

                $("#d"+val.d_id).addClass('active');
                $("#d"+val.d_id + ' i').addClass('fa-check');
                _renderinput.domain_id = val.d_id;
                _renderinput.domain_name = val.d_name;
                _renderinput.loadOrganisation(val.c_id, val.d_id);
            });
            $('.name-holder', dObject).text(val.d_name);
            Domain.append(dObject);
            if (_renderinput.domain_id == val.d_id){
                $("#d"+val.d_id).addClass('active');
                $("#d"+val.d_id + ' i').addClass('fa-check');
                _renderinput.loadOrganisation(c_id, _renderinput.domain_id);
            }

        });
    };

    this.loadOrganisation = function(c_id, d_id) {
        // this.org_ids = [];
        // this.org_names = [];
        console.log(c_id, d_id);
        Organisation.empty();

        // append select
        orgObject = list_template.clone();
        orgObject.addClass("organisationlist");
        orgObject.attr('id', 'o-1');
        $('.name-holder', orgObject).text('Select');
        Organisation.append(orgObject)

        orgObject.on('click', function() {
            _renderinput.org_ids = [];
            _renderinput.org_names = [];
            sts = $('#o-1').hasClass('active');
            if (sts == true) {
                $('.organisationlist').removeClass('active');
                $('.organisationlist i').removeClass('fa-check');
            }
            else {
                $('.organisationlist').addClass('active');
                $('.organisationlist i').addClass('fa-check');
                $.each(ORGANISATION_INFO, function(k, v) {
                    if ((v.c_id != c_id) && (v.d_id != d_id))
                        return;
                    _renderinput.org_ids.push(v.org_id);
                    _renderinput.org_names.push(v.org_name);
                });
            }
        });

        $.each(ORGANISATION_INFO, function(ke, val) {
            if (val.is_active == false)
                return;
            if (
                (parseInt(val.c_id) == parseInt(c_id)) &&
                (parseInt(val.d_id) == parseInt(d_id))
            ){
                console.log("if")
                orgObject = list_template.clone();
                orgObject.addClass("organisationlist");
                orgObject.attr('id', 'o'+val.org_id);

                orgObject.on('click', function() {
                    $('#o-1').removeClass('active');
                    sts = $('#o'+val.org_id).hasClass('active');
                    if (sts == true) {
                        $('#o'+val.org_id).removeClass('active');
                        $('#o'+val.org_id+ ' i').removeClass('fa-check');
                        _renderinput.org_id = _renderinput.remveItemFromList(
                            val.org_id, this.org_id
                        );
                        _renderinput.org_name = _renderinput.remveItemFromList(
                            val.org_name, this.org_name
                        );
                    }
                    else {
                        $('#o'+val.org_id).addClass('active');
                        $('#o'+val.org_id+ ' i').addClass('fa-check');
                        _renderinput.org_ids.push(val.org_id);
                        _renderinput.org_names.push(val.org_name);
                    }
                });

                $('.name-holder', orgObject).text(val.org_name);
                Organisation.append(orgObject);

                if (_renderinput.selected_iids.indexOf(val.org_id) > -1){
                    $('#o'+val.org_id).addClass('active');
                    $('#o'+val.org_id+ ' i').addClass('fa-check');
                    _renderinput.org_ids.push(val.org_id);
                    _renderinput.org_names.push(val.org_name);
                }

            }
        });
    };

    this.loadNature = function(c_id) {
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
                $(".naturelist i").removeClass('fa-check');
                $('#n'+val.s_n_id).addClass('active');
                $('#n'+val.s_n_id+' i').addClass('fa-check');
                _renderinput.nature_id = val.s_n_id;
                _renderinput.nature_name = val.s_n__name;
            });
            $('.name-holder', nObject).text(val.s_n_name);
            Nature.append(nObject);

            if (_renderinput.nature_id == val.s_n_id){
                $('#n'+val.s_n_id).addClass('active');
                $('#n'+val.s_n_id+' i').addClass('fa-check');
                _renderinput.nature_id = val.s_n_id;
                _renderinput.nature_name = val.s_n__name;
            }

        });
    };

    this.loadRepeats = function() {
        RepeatsType.empty();
        RepeatsType.append(
            _renderinput.make_option("Select", "")
        );
        $.each(REPEATSTYPE_INFO, function(ke, val) {
            RepeatsType.append(
                _renderinput.make_option(val.repeat_type, val.repeat_type)
            );
        });
    };

    this.loadMonthAndData = function(mainMonObj) {
        sets = this.getMonthAndDataSets();
        mainMonObj.append(this.make_option("Select", ""));
        $.each(sets, function(k, v) {
            opt =_renderinput.make_option(v.m_name, v.m_id);
            mainMonObj.append(opt);
        });
    };
    this.loadFrequency = function() {
        Frequency.empty();
        Frequency.append(
            this.make_option("Select", "")
        );
        $.each(FREQUENCY_INFO, function(ke, val) {
            opt =_renderinput.make_option(val.frequency, val.frequency_id);
            Frequency.append(opt);
        });
    };
    this.clearSubLevel = function(l_position) {
        for (var i=l_position+1; i<11; i++) {
            // console.log($('.statutory_levelvalue #snl'+i));
            $('.statutory_levelvalue #snl'+i).empty();
        }
    }
    this.loadStatuNames = function(data, l_position) {
        // console.log(STATUTORY_INFO);
        this.clearSubLevel(l_position);
        $.each(data, function(k,v) {
            liObject = $('#templates #statutory-li-template li').clone();

            liObject.attr('id', 'sid'+v.s_id);
            liObject.addClass('slp'+v.l_position);

            $('.sname-holder', liObject).on('click', function() {
                $('.statutory_levelvalue #dv'+v.l_position).val('');
                $('.statutory_levelvalue #dvid'+v.l_position).val('');
                $('.statutory_levelvalue #dvpid'+v.l_position).val('');
                var _s_names = [];
                var _s_pids = [];
                _renderinput.s_id = v.s_id;
                $('.slp'+v.l_position).removeClass('active');
                $('.slp'+v.l_position+' #select-act').removeClass('fa-check');
                $('#sid'+v.s_id).addClass('active');
                $('#sid'+v.s_id+' #select-act').addClass('fa-check');
                if (v.p_ids != null){
                    $.merge(_s_pids, v.p_ids);
                    _renderinput.l_one_id = v.p_ids[0];
                }
                else {
                    _renderinput.l_one_id = v.s_id;
                }

                if (v.p_maps != null) {
                    $.merge(_s_names, v.p_maps);
                }
                $.merge(_s_names, [v.s_name]);
                _renderinput.s_names = _s_names;
                $.merge(_s_pids, [v.s_id]);
                _renderinput.s_pids = _s_pids;
                _renderinput.renderStatuNames(v.s_id, v.l_position);
            });
            $('.edit-icon', liObject).on('click', function() {
                if (v.p_ids == null) {
                    pid = 0;
                }
                else {
                    pid = v.p_ids[v.p_ids.length - 1];
                }

                $('.statutory_levelvalue #dv'+v.l_position).val(v.s_name);
                $('.statutory_levelvalue #dvid'+v.l_position).val(v.s_id);
                $('.statutory_levelvalue #dvpid'+v.l_position).val(pid);
            });
            $('#sname', liObject).text(v.s_name);
            $('#tbody-statutory-level .statutory_levelvalue #snl'+v.l_position).append(liObject)
        });
    };
    this.renderStatuNames = function(p_id, l_position) {
        var data = []
        $.each(STATUTORY_INFO, function(k, v) {
            if (
                (v.c_id == _renderinput.country_id) &&
                (v.d_id == _renderinput.domain_id)
            ){
                if (p_id == v.p_id)
                {
                    if (l_position == v.l_position) {
                        data.push(v);
                    }
                    else {
                        _renderinput.loadStatuNames(data, l_position);
                        data = [];
                        l_position = v.l_position;
                        data.push(v);
                    }
                }
                else {
                    return ;
                }
            }
        });
        _renderinput.loadStatuNames(data, l_position);
    };
    this.loadStatuesLevels = function(loadFromLevel) {
        // $('#tbody-statutory-level').empty();
        if ((this.country_id == null) || (this.domain_id == null)) {
            return;
        }
        c_list = STATUTORY_LEVEL_INFO[this.country_id];
        if (!c_list)
            return
        s_list = c_list[this.domain_id];
        if (!s_list)
            return
        len = s_list.length;
        wid = 100/len;
        if (len > 3) {
            main_wid = 400 * len + 10 ;
            wid = "400px";
            $("#tab2 #datatable-fixed-header").width(main_wid+'px');
        }
        else {
            wid += "%";
            $("#tab2 #datatable-fixed-header").width('100%');
        }

        $.each(s_list, function(k, v) {
            if (loadFromLevel > v.l_position ) {
                return;
            }
            if (v.l_position == 1) {
                _renderinput.level_one_name = v.l_name;
            }

            slObject = $('#templates .statutory_levelvalue').clone();
            slObject.width(wid);

            $('.filter-text-box', slObject).attr(
                'id', 'sf'+ v.l_position
            );
            $('.statutory_title', slObject).html(v.l_name);
            $('.filter-text-box', slObject).on(
                'keyup', function(){
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
            $('.bottomfield .txtsname', slObject).on(
                'keypress', function(event) {
                if (event.keyCode == 13) {
                    new_value = $('#dv'+ v.l_position).val();
                    _sid = $('#dvid'+v.l_position).val();
                    console.log(_sid);
                    if(_sid == '') {
                        _fetchback.saveStautory(
                            v.l_id, new_value, v.l_position
                        );
                    }
                    else {
                        _fetchback.updateStatutory(
                            new_value, parseInt(_sid), v.l_position
                        );
                    }
                    // if (v.l_position == 1){
                    //     _renderinput.renderStatuNames(
                    //         0, v.l_position
                    //     );
                    // }

                    $('#dv'+ v.l_position).val('');
                    $('#dvid'+ v.l_position).val('');
                }
            });

            $('.bottomfield .statut-add', slObject).on(
                'click', function(){
                new_value = $('#dv'+ v.l_position).val();
                _sid = $('#dvid'+v.l_position).val();
                if (_sid == '') {
                    _fetchback.saveStautory(
                        v.l_id, new_value, v.l_position
                    );
                }
                else {
                    _fetchback.updateStatutory(
                        new_value, _sid, v.l_position
                    );
                }

                // if (v.l_position == 1){
                //     _renderinput.renderStatuNames(
                //         0, v.l_position
                //     );
                // }
            });

            $('#tbody-statutory-level').append(slObject);
            if (v.l_position == 1){
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
                console.log(k);
                console.log(v);
                _renderinput.mapped_statu.splice(k, 1);
                _renderinput.renderStatuGrid();
            });
            $('.tbody-statutory-list').append(trObj);
            j += 1;
        });
    };
    this.loadMonths = function(freq_val) {
        if (freq_val == 1) {
            $('#otstatutory_month').empty();
            this.loadMonthAndData($('#otstatutory_month'));
            $('#otstatutory_month').change(function(){
                $('#otstatutory_date').empty();
                $.each(_renderinput.getMonthAndDataSets(), function(kk, v) {
                    if (v.m_id == parseInt($('#otstatutory_month').val())) {
                        for (var i=1; i<=v.range; i++) {
                            dopt =_renderinput.make_option(i, i);
                            $('#otstatutory_date').append(dopt);
                        }
                    }
                });
            });
        }
        else {
            $('#rcstatutory_month').empty();
            this.loadMonthAndData($('#rcstatutory_month'));
            $('#rcstatutory_month').change(function(){
                $('#rcstatutory_date').empty();
                $.each(_renderinput.getMonthAndDataSets(), function(kk, v) {
                    if (v.m_id == parseInt($('#rcstatutory_month').val())) {
                        for (var i=1; i<=v.range; i++) {
                            dopt =_renderinput.make_option(i, i);
                            $('#rcstatutory_date').append(dopt);
                        }
                    }
                });
            });
        }
    }
    this.loadCompliance = function(data){

        Provision.val(data.s_provision);
        ComplianceTask.val(data.c_task);
        Description.val(data.description);
        Document.val(data.doc_name);
        Penal.val(data.p_consequences);
        ReferenceLink.val(data.reference);
        Frequency.val(data.f_id);
        this.hideFrequencyAll();
        this.showFrequencyVal();
        if (data.f_id == 1) {
        // this.loadMonths();

            if (data.statu_dates.length > 0) {
                $('#otstatutory_month').val(data.statu_dates[0]['statutory_month']);

                $('#otstatutory_date').empty();
                $.each(_renderinput.getMonthAndDataSets(), function(kk, v) {
                    if (v.m_id == parseInt($('#otstatutory_month').val())) {
                        for (var i=1; i<=v.range; i++) {
                            dopt =_renderinput.make_option(i, i);
                            $('#otstatutory_date').append(dopt);
                        }
                    }
                });
                $('#otstatutory_date').val(data.statu_dates[0]['statutory_date']);
                $('ottriggerbefore').val(data.statu_dates[0]['trigger_before_days']);
            }
        }
        else if (data.f_id == 5) {
            Duration.text(data.duration);
            alert(data.d_type_id);
            DurationType.val(data.d_type_id);
        }
        else {
            RepeatsType.val(data.r_type_id);
            RepeatsEvery.val(data.r_every);

        }
        console.log(data.comp_id);
        console.log(data.temp_id);
        Comp_id.val(data.comp_id);
        if (data.comp_id == null) {
            Temp_id.val(data.temp_id);
        }
        else {
            Temp_id.val(data.comp_id);
        }
        console.log(Comp_id.val());
        console.log(Temp_id.val());

    };
    this.clearCompliance = function(){
        Provision.val('');
        ComplianceTask.val('');
        Description.val('');
        Document.val('');
        Penal.val('');
        ReferenceLink.val('');

        // Duration.val('');
        // DurationType.val('');
        // RepeatsType.val('');
        // RepeatsEvery.val('');

        Comp_id.val('');
        Temp_id.val('');
        Frequency.val('');
        $('.frequency-set').empty();
        $('#counter').html('');
        $('#counter1').html('')
        $('#counter2').html('');
        $('#counter3').html('');
        this.hideFrequencyAll();
    };
    this.renderComplianceGrid = function() {
        $('.tbody-compliance-list').empty();
        var j = 1;
        $.each(_renderinput.mapped_compliances, function(ke, v) {
            cObj = $('#templates #compliance-templates .table-row').clone();
            console.log(cObj);
            $('.sno', cObj).text(j);
            $('.statutory-provision', cObj).text(v.s_provision);
            $('.task', cObj).text(v.c_task);
            $('.description', cObj).text(v.description);
            $('.frequency', cObj).text(v.frequency);
            $('.repeats', cObj).val();
            $('#edit-icon', cObj).attr('title', 'Edit');
            $('#edit-icon', cObj).on('click', function () {
                _renderinput.loadCompliance(v);
            });
            if (v.comp_id == null) {
                $('#status', cObj).addClass('remove');
                $('#status', cObj).addClass('fa-trash text-primary');
                $('#status', cObj).attr('title', "Click here to remove compliance");
            }
            else {
                if (v.is_active == true){
                    classValue = "active-icon";
                    $('#status', cObj).addClass(classValue);
                    $('#status', cObj).addClass("fa-check text-success");
                    $('#status', cObj).attr('title', msg.active_tooltip);
                }
                else{
                    classValue = "inactive-icon";
                    $('#status', cObj).addClass(classValue);
                    $('#status', cObj).addClass("fa-times text-danger");
                    $('#status', cObj).attr('title', msg.deactive_tooltip);
                }
            }

            $('#status', cObj).on('click', function () {

                if ($('#status', cObj).hasClass('remove')) {
                    _renderinput.mapped_compliances.splice(ke, 1);
                }
                else {
                    if (v.is_active == true) {
                        v.is_active = false;
                    }
                    else {
                        v.is_active = true;
                    }
                }
                _renderinput.renderComplianceGrid();
            });
            $('.tbody-compliance-list').append(cObj);
            j += 1;
        });
    };
    this.clearGeosSubLevel = function(l_position) {
        for (var i=l_position+1; i<11; i++) {
            $('.levelvalue #gnl'+i).empty();
        }
    };
    this.unloadGeosNames = function(l_position, p_id) {
        for (var i=l_position+1; i<11; i++) {
            // $('.levelvalue #gnl'+i).empty();
            $('#gnl'+i).children().each(function(){
                // var cls = $(this).attr('class').match(/pid[\w,]*\b/);
                var cls = $(this).attr('class');
                if (cls.indexOf(p_id.toString()) > 0) {
                    $(this).remove();
                }

            });
        }
    };
    this.loadGeosNames = function(data, l_position, parent_name) {


        this.clearSubLevel(l_position);
        $.each(data, function(k,v) {

            liObject = $('#templates #list-template li').clone();
            liObject.attr('id', 'gid'+v.g_id);
            // liObject.addClass('glp'+v.l_position);
            // console.log(v.p_ids);
            liObject.addClass('pid'+v.p_ids.toString());
            liObject.val(v.g_id);
            liObject.attr('name',v.p_ids);
            liObject.on('click', function() {
                if ($('#gid'+v.g_id).hasClass('active')) {
                    $('#gid'+v.g_id).removeClass('active');
                    $('#gid'+v.g_id+' i').removeClass('fa-check');
                    _renderinput.unloadGeosNames(v.l_position, v.g_id);
                }else {
                    $('#gid'+v.g_id).addClass('active');
                    $('#gid'+v.g_id+' i').addClass('fa-check');
                    _renderinput.renderGeosNames(v.g_id, v.l_position, v.g_name);
                }

            });
            $('.name-holder', liObject).text(v.g_name);
            if ((v.l_position > 1) && (k == 0)) {
                $('.tbody-geography-level #gnl'+ v.l_position).append(
                    '<h3 class='+ "head" + v.p_ids +' style="background-color:gray;padding:2px;font-size:13px;color:white;">' + parent_name + '</h3>'
                );
            }
            $('.tbody-geography-level #gnl'+v.l_position).append(liObject)
            console.log(_renderinput.selected_geos_parent);
            if (_renderinput.selected_geos_parent.indexOf(v.g_id) > -1) {
                console.log("****");
                $('#gid'+v.g_id).addClass('active');
                $('#gid'+v.g_id+' i').addClass('fa-check');
                _renderinput.renderGeosNames(v.g_id, v.l_position, v.g_name);
            }

        });
    };
    this.renderGeosNames = function(p_id, l_position, parent_name) {
        var data = []
        $.each(GEOGRAPHY_INFO, function(k, v) {
            if (v.c_id == _renderinput.country_id)
            {
                if (p_id == v.p_id)
                {
                    if (l_position == v.l_position) {
                        data.push(v);
                    }
                    else {
                        _renderinput.loadGeosNames(data, l_position, parent_name);
                        data = [];
                        l_position = v.l_position;
                        data.push(v);
                    }
                }
                else {
                    return ;
                }
            }
        });
        _renderinput.loadGeosNames(data, l_position, parent_name);
    };
    this.loadGeosLevels = function(loadFromLevel) {
        if (this.country_id == null) {
            return;
        }
        $.each(GEOGRAPHY_LEVEL_INFO, function(k, v) {
            if (loadFromLevel > v.l_id ) {
                return;
            }
            if (_renderinput.country_id != v.c_id) {
                return;
            }

            slObject = $('#templates #geography-level-templates').clone();
            $('.title', slObject).html(v.l_name);

            $('.gname-list', slObject).attr(
                'id', 'gnl' + v.l_position
            );
            $('.tbody-geography-level').append(slObject);

        });
    };


    this.hideFrequencyAll = function() {
        Onetimepan.hide();
        RecurringPan.hide();
        OccasionalPan.hide();
    };

    this.showFrequencyVal = function(){
        var freq_val = Frequency.val();
        if (freq_val == '') {
            this.hideFrequencyAll();
        }
        else {
            // $('.frequency-set').empty();
            if (freq_val == 1){
                Onetimepan.show();
                _renderinput.loadMonths(freq_val);
            }
            else if (freq_val == 5) {
                OccasionalPan.show();
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
                DurationType.keyup(function(e){
                    e.preventDefault();
                    d_select = $('#duration_type option:selected');
                    if ((DurationType.val() != '') && (Duration.val() != '')) {
                        _renderinput.summary =  "To complete with in " + this.value + " "+ d_select.text();
                        $('.occasional_summary').text(_renderinput.summary);
                    }

                });
                $('#duration_type').change(function(){
                    d_select = $('#duration_type option:selected');
                    if ((DurationType.val() != '') && (Duration.val() != '')) {
                        _renderinput.summary = "To complete with in " + Duration.val() +" "+ d_select.text();
                        $('.occasional_summary').text(_renderinput.summary);
                    }
                    else {
                        _renderinput.summary = '';
                        $('.occasional_summary').text(_renderinput.summary);

                    }
                });

            }
            else {
                RecurringPan.show();
                _renderinput.loadMonths(freq_val);
            }

        }
    };


}

//
// callback with compfie input data
//
function FetchBack() {
    this.getMasterData = function() {
        fetch.getStatutoryMappingsMaster(function(status, response) {
            if (status != null) {
                displayMessage(status);
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

    this.getStatuMaster = function(l_position, callback) {
        fetch.getStatutoryMaster(function(status, response) {
            if(status != null) {
                displayMessage(status);
            }
            else {
                STATUTORY_INFO = response.statutory_info;
                console.log(l_position)
                if (l_position == 0){
                    _renderinput.loadStatuesLevels(l_position);
                }
                else {
                    callback();
                }
            }
        });
    };

    this.getMappedList = function(approv_status, rcount) {
        fetch.getStatutoryMappings(approv_status, rcount,
            function(status, response){
                if (status != null) {
                    displayMessage(status);
                }
                else {
                    STATU_MAPPINGS = response.statu_mappings;
                    STATU_TOTALS = response.total_records;
                    _listPage.renderList(STATU_MAPPINGS, STATU_TOTALS);
                }
            }
        );
    };

    this.getMapDatabyId = function(mapping_id, compliance_id) {
        fetch.getStatutoryMappingsEdit(mapping_id, compliance_id,
            function(status, response){
                if (status != null) {
                    displayMessage(status);
                }
                else {
                    _renderinput.resetField();

                    _renderinput.country_id = response.c_id;
                    _renderinput.domain_id = response.d_id;
                    _renderinput.nature_id = response.s_n_id;
                    _renderinput.selected_iids = response.i_ids;
                    _renderinput.selected_geos = response.g_ids;
                    _renderinput.selected_geos_parent = [];
                    _renderinput.mapped_compliances = response.comp_list;
                    _renderinput.mapping_id = response.m_id;

                    $.each(GEOGRAPHY_INFO, function(k, v) {
                        if(response.g_ids.indexOf(v.g_id) > -1) {
                            $.each(v.p_ids, function(idx, pid) {
                                if (_renderinput.selected_geos_parent.indexOf(pid) == -1) {
                                    _renderinput.selected_geos_parent.push(pid);
                                }
                            });
                        }
                    });
                    $.merge(_renderinput.selected_geos_parent, _renderinput.selected_geos);
                    $.each(STATUTORY_INFO, function(k, v) {
                        if (response.s_ids.indexOf(v.s_id) > -1) {
                            info = {}
                            info["s_id"] = v.s_id;
                            if (v.p_names != null)
                                info["s_names"] = v.p_maps
                            else
                                info["s_names"] = [];
                            info["s_names"].push(v.s_name)
                            if (v.p_ids == null) {
                                info["l_one_id"] = 0;
                            }
                            else {
                                info["l_one_id"] = v.p_ids[0];
                            }
                            _renderinput.mapped_statu.push(info);
                        }
                    });

                    _renderinput.renderStatuGrid();
                    _renderinput.renderComplianceGrid();

                    showTab();
                    _listPage.hide();
                    _viewPage.show();
                }
            }
        );
    }

    this.changeStatus = function(m_id, sts) {
        fetch.changeStatutoryMappingStatus(m_id, sts, function(status, response) {
            if (status != null) {
                possibleFailure(status);
            }
            else {
                this.getMappedList(0, 0);
            }
        });
    };

    this.updateStatutory = function(s_name, s_id, l_position) {
        fetch.updateStatutory(s_id, s_name, function(status, response){
            if (status != null) {
                possibleFailure(status);
            }
            else {
                $('#dv'+ l_position).val('');
                $('#dvid'+ l_position).val('');
                $('#dvpid'+ l_position).val('');
            }
        })
    };

    this.saveStautory = function(s_l_id, s_name, l_position){
        d_id = _renderinput.domain_id;
        p_ids = _renderinput.s_pids;
        p_names = _renderinput.s_names;
        if (p_ids.length == 0)
            p_ids = null;
        if (p_names.length == 0)
            p_names = null;

        if (l_position == 1) {
            p_ids = p_names = null;
        }
        else {
            if (p_ids.length == 0) {
                displayMessage(msg.levelselection_required);
            }
        }

        fetch.saveStatutory(d_id, s_l_id, s_name, p_ids, p_names, function(
                status, response
            ){
                if(status != null) {
                    possibleFailure(status);
                }
                else {
                    // load statutory list
                    $('#dv'+ l_position).val('');
                    $('#dvid'+ l_position).val('');
                    $('#dvpid'+ l_position).val('');
                    _fetchback.getStatuMaster(l_position, function() {

                        if (p_ids != null) {
                            pid = p_ids[p_ids.length - 1];
                        }
                        else{
                            pid = 0;
                            l_position = 1;
                        }
                        $('.statutory_levelvalue #snl'+l_position).empty();
                        _renderinput.renderStatuNames(pid, l_position);
                    });
                }
            }
        );
    };

    this.saveMapping = function(data) {
        fetch.saveStatutoryMapping(data, function(status, response) {
            if (status == null) {
                // show list
                _viewPage.hide();
                _listPage.show();
                _renderinput.resetField();
            }
            else {
                console.log(status, response.compliance_name);
                possibleFailure(status, response.compliance_name);
                return false;
            }
        });
    };

    this.updateMapping = function(data) {
        fetch.updateStatutoryMapping(data, function(status, response) {
            if (status == null) {
                _viewPage.hide();
                _listPage.show();
                _renderinput.resetField();
                IS_EDIT = false;
            }
            else {
                possibleFailure(status);
                return false;
            }
        });
    };
}

//
// Render List Page
//
function ListPage() {

    this.renderList = function(data, tRecord) {
        // $('.tbl-statutorymapping-list tr').find('mapping_row');
        // $('.tbl-statutorymapping-list tr').find('compliance_row');
        $('.tbl-statutorymapping-list .mapping-row').remove();
        $('.tbl-statutorymapping-list .compliance-row').remove();

        function comp_row(rowObjec, cdata, mapping_id) {
            var x = 1;
            $.each(cdata, function(k, c) {
                row = $('#templates .compliance-row').clone();
                $('.comp_name', row).text(c.comp_name);
                $('.comp_approval_status', row).text(c.approval_status_text);
                $('.comp_edit', row).attr('title', 'Edit');
                $('.comp_edit', row).addClass('fa-pencil text-primary');
                $('.comp_edit', row).on('click', function() {
                    _listPage.displayMappingEdit(mapping_id, c.comp_id);
                });
                rowObjec.append(row);
            });
        }

        var j = 1;
        $.each(data, function(k, v) {
            org_names = v.i_names.join(' , ');
            s_names = v.s_maps.join(' >> ');
            crow = $('#templates .mapping-row').clone();
            $('.sno', crow).text(j);
            $('.c_name', crow).text(v.c_name);
            $('.d_name', crow).text(v.d_name);
            $('.org_name', crow).text(org_names);
            $('.nature_name', crow).text(v.s_n_name);
            $('.s_name', crow).text(s_names);
            $('.map_edit', crow).attr('title', 'Client Here to Edit');
            $('.map_edit', crow).addClass('fa-pencil text-primary');
            $('.map_edit', crow).on('click', function() {
                _listPage.displayMappingEdit(v.m_id, null);
            });
            if (v.is_active == true){
                $('.map_status', crow).addClass("fa-check text-success");
                $('.map_status', crow).attr('title', msg.active_tooltip);
            }
            else {
                $('.map_status', crow).addClass("fa-times text-danger");
                $('.map_status', crow).attr('title', msg.deactive_tooltip);
            }
            $('.map_status', crow).on('click', function() {
                if (v.is_active == true) {
                    passStatus = false;
                }
                else {
                    passStatus = true;
                }
                _fetchback.changeStatus(v.m_id, passStatus);
            });

            $('.approval_status', crow).text("");
            j = j + 1;
            $('.tbl-statutorymapping-list').append(crow);
            comp_row($('.tbl-statutorymapping-list'), v.mapped_comps, v.m_id);
        });
    };

    this.displayMappingEdit = function(map_id, comp_id) {
        IS_EDIT = true;
        _fetchback.getMapDatabyId(map_id, comp_id);
    };

    this.show = function() {
        CURRENT_TAB = 1;
        ListScreen.show();
        ViewScreen.hide();
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

        console.log(_renderinput.country_id);
        console.log(_renderinput.domain_id);
        console.log(_renderinput.org_ids);
        console.log(_renderinput.nature_id);
        _renderinput.loadCounty();
    };
    this.validateFirstTab = function() {
        console.log(_renderinput.country_id);
        console.log(_renderinput.domain_id);
        console.log(_renderinput.org_ids);
        console.log(_renderinput.nature_id);
        if (_renderinput.country_id == null) {
            displayMessage(msg.country_required);
            return false;
        }
        else if (_renderinput.domain_id == null) {
            displayMessage(msg.domain_required);
            return false;
        }
        else if (_renderinput.org_ids.length == 0) {
            displayMessage(msg.industry_required);
            return false;
        }
        else if (_renderinput.nature_id == null) {
            displayMessage(msg.statutorynature_required);
            return false;
        }
        return true;
    };
    this.showSecondTab = function(){
        $('#tbody-statutory-level').empty();;
        _renderinput.loadStatuesLevels(0);
    };
    this.validateSecondTab = function() {
        console.log(_renderinput.mapped_statu);
        if (_renderinput.mapped_statu.length == 0) {
            displayMessage(msg.nostatutory_selected);
            return false;
        }
        return true;
    };
    this.showThirdTab = function(){
        _renderinput.loadFrequency();
        _renderinput.loadRepeats();
        //validate mandatory
        // if file uploaded validate file format and size
        // frequency validate and render multiple input
        // add to temp
    };
    this.validateComplianceTab = function() {
        if (Provision.val().length == 0) {
            displayMessage(msg.statutoryprovision_required);
            return false;
        }
        else if (ComplianceTask.val().length == 0) {
            displayMessage(msg.compliancetask_required)
            return false;
        }
        else if(Description.val().length == 0) {
            displayMessage(msg.compliancedescription_required);
            return false;
        }
        else if (Frequency.val() == '') {
            displayMessage(msg.compliancefrequency_required);
            return false;
        }
        else {
            if (
                (Frequency.val() == 2) ||
                (Frequency.val() == 3)
            ){
                if(RepeatsType.val().trim() == '') {
                    displayMessage(msg.repeatstype_required);
                    return false;
                }
                else if(RepeatsEvery.val().trim() == '') {
                    displayMessage(msg.repeatsevery_required);
                    return false;
                }
            }
            else if(Frequency.val() == 5) {
                if($('#duration').val().trim() == '') {
                    displayMessage(msg.duration_required);
                    return false;
                }
                else if ($('#duration').val().trim() == 0) {
                    displayMessage(msg.invalid_duration);
                    return false;
                }
                else if($('#duration_type').val().trim() == '') {
                    displayMessage(msg.durationtype_required);
                    return false;
                }

            }
            return true;
        }

    };
    this.showFouthTab = function(){
        $('.tbody-geography-level').empty();
        _renderinput.loadGeosLevels(0);
        _renderinput.renderGeosNames(0, 1);
    };
    this.show = function() {
        ViewScreen.show();
        this.showFirstTab();
    };
    this.hide = function() {
        ViewScreen.hide();
    };
    this.getFourthTabValues = function(){
        // get selected value from all geo levels
        _renderinput.selected_geos = [];
        _renderinput.selected_geos_parent = [];
        for (var i=1; i<11; i++) {
            $('#gnl'+i).children().each(function(){
                if ($(this).hasClass('active')) {
                    _renderinput.selected_geos.push($(this).val());
                    _renderinput.selected_geos_parent.push($(this).attr('name'));
                }
            });
        }
        // get last child only
        idx = [];
        $.each(_renderinput.selected_geos, function(i, val) {
            //finding parent
            $.each(_renderinput.selected_geos_parent, function(j, x) {
                if (x.indexOf(val) > -1) {
                    idx.push(i);
                    return false;
                }
            });
        });
        // removing parent from selected list
        $.each(idx.reverse(), function(z, y) {
            _renderinput.selected_geos.splice(y, 1);
        });
    };
    this.make_data_format = function(trType){
        _viewPage.getFourthTabValues();
        map_data = {};
        if (_renderinput.mapping_id != null) {
            map_data["m_id"] = _renderinput.mapping_id;
        }
        map_data["c_id"] = _renderinput.country_id;
        map_data["d_id"] = _renderinput.domain_id;
        map_data["i_ids"] = _renderinput.org_ids;
        map_data["s_n_id"] = _renderinput.nature_id;
        var s_ids = [];
        var mappings = [];
        $.each(_renderinput.mapped_statu, function(k, s) {
            if (s["s_id"]){
                s_ids.push(s["s_id"]);
                mappings.push((s["s_names"].join('>>')))
            }
        });
        map_data["s_ids"] = s_ids;
        map_data["g_ids"] = _renderinput.selected_geos;
        map_data["mappings"] = mappings;
        // var compliances = [];
        $.each(_renderinput.mapped_compliances, function(k, v){
            delete v.temp_id;
        });
        map_data["compliances"] = _renderinput.mapped_compliances;
        map_data["tr_type"] = trType;
        return map_data;
    }
}

function showTab(){
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
        }
        else if (tab == 2) {
            $('.tab-step-2 a').attr('href', '#tab2');
        }
        else if (tab == 3) {
            $('.tab-step-3 a').attr('href', '#tab3');
        }
        else if (tab == 4) {
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
    }
    else if (CURRENT_TAB == 2) {
        if(!_viewPage.validateFirstTab()) {
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
    }
    else if (CURRENT_TAB == 3) {
        if (!_viewPage.validateSecondTab()) {
            CURRENT_TAB -= 1;
            return false;
        }
        hideall();
        enabletabevent(3);
        $('.tab-step-3').addClass('active')
        $('#tab3').addClass('active in');
        $('#tab3').show();
        NextButton.show();
        PreviousButton.show();
        _viewPage.showThirdTab();
    }
    else if (CURRENT_TAB == 4) {
        console.log(_renderinput.mapped_compliances.length);
        if (_renderinput.mapped_compliances.length == 0) {
            CURRENT_TAB -=1;
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

};
_renderinput = new RenderInput();
_fetchback = new FetchBack();
_listPage = new ListPage();
_viewPage = new ViewPage();

function pageControls() {
    AddButton.click(function() {
        showTab();
        _listPage.hide();
        _viewPage.show();

    });
    NextButton.click(function() {
        CURRENT_TAB += 1;
        showTab();
    });
    PreviousButton.click(function() {
        CURRENT_TAB = CURRENT_TAB - 1;
        showTab();
    });
    AddStatuButton.click(function() {
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
            displayMessage(msg.invalid_levelone + _renderinput.level_one_name);
        }
        else {
            if (add_new) {
                _renderinput.mapped_statu.push(info)
                _renderinput.renderStatuGrid();
            }
        }
    });


    Frequency.change(function() {
        _renderinput.hideFrequencyAll();
        _renderinput.showFrequencyVal();
    });

    Description.keyup(function(e) {
        countDown = $('#counter');
        var mxlength = 500;
        var txtlen = this.value.length;
        if(mxlength < txtlen) {
            countDown.html(msg.should_not_exceed + mxlength + "characters");
            this.value = this.value.substring(0, mxlength);
            e.preventDefault();
        }
        else {
            countDown.html(mxlength - txtlen + "characters");
        }
    });
    Provision.keyup(function(e) {
        countDown = $('#counter1');
        var mxlength = 500;
        var txtlen = this.value.length;
        if(mxlength < txtlen) {
            countDown.html(msg.should_not_exceed + mxlength + "characters");
            this.value = this.value.substring(0, mxlength);
            e.preventDefault();
        }
        else {
            countDown.html(mxlength - txtlen + "characters");
        }
    });
    Penal.keyup(function(e) {
        countDown = $('#counter2');
        var mxlength = 500;
        var txtlen = this.value.length;
        if(mxlength < txtlen) {
            countDown.html(msg.should_not_exceed + mxlength + "characters");
            this.value = this.value.substring(0, mxlength);
            e.preventDefault();
        }
        else {
            countDown.html(mxlength - txtlen + "characters");
        }
    });
    ReferenceLink.keyup(function(e) {
        countDown = $('#counter3');
        var mxlength = 500;
        var txtlen = this.value.length;
        if(mxlength < txtlen) {
            countDown.html(msg.should_not_exceed + mxlength + "characters");
            this.value = this.value.substring(0, mxlength);
            e.preventDefault();
        }
        else {
            countDown.html(mxlength - txtlen + "characters");
        }
    });

    AddComplianceButton.click(function(){
        if (!_viewPage.validateComplianceTab()) {
            return false;
        }

        _renderinput.statu_dates = [];
        info = {};

        if (Comp_id.val() == '')
            info['comp_id'] = null;
        else
            info['comp_id'] = parseInt(Comp_id.val());

        if (Temp_id.val() == '')
            info['temp_id'] = null;
        else
            info['temp_id'] = Temp_id.val();

        info['s_provision'] = Provision.val().trim();
        info['c_task'] = ComplianceTask.val().trim();
        info['description'] = Description.val().trim();
        info['doc_name'] = Document.val().trim();
        info['f_f_list'] = null;
        info['p_consequences'] = Penal.val().trim();
        info['reference'] = ReferenceLink.val().trim();
        info['f_id'] = parseInt(Frequency.val());
        info['d_type_id'] = null;
        info['duration'] = null;
        info['r_type_id'] = null;
        info['r_every'] = null;
        if (Frequency.val() == 5) {
            info['d_type_id'] = parseInt(DurationType.val());
            info['duration'] = parseInt(Duration.val());
        }
        else if (
            (Frequency.val() == 2) && (Frequency.val() == 3) &&
            (Frequency.val() == 4)
        ){
            info['r_type_id'] = parseInt(RepeatsType.val());
            info['r_every'] = parseInt(RepeatsEvery.val());
        }
        else {
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
                statu['trigger_before_days'] = parseInt(trig)
            }
            _renderinput.statu_dates.push(statu);
        }
        info['statu_dates'] = _renderinput.statu_dates;
        info['is_active'] = true;
        info['frequency'] = $('#compliance_frequency option:selected').text();
        info['summary'] = _renderinput.summary;

        is_duplidate = false;

        $.each(_renderinput.mapped_compliances, function(k, v) {
            if ((Temp_id.val() == Comp_id.val()) && (Comp_id.val() == v.comp_id)) {
                _renderinput.mapped_compliances.splice(k, 1);
                return false;
            }
        });
        $.each(_renderinput.mapped_compliances, function(k, v) {
            if (
                (v.s_provision == Provision.val().trim()) &&
                (v.c_task == ComplianceTask.val().trim()) &&
                ((Comp_id.val().trim() == '') || (Temp_id.val().trim() != Comp_id.val().trim()))
            ){
                displayMessage(msg.compliancetask_duplicate);
                is_duplidate = true;
                return false;
            }
        });
        if (!is_duplidate) {
            _renderinput.mapped_compliances.push(info);
            _renderinput.renderComplianceGrid();
            _renderinput.clearCompliance();
        }
    });

    SaveButton.click(function() {

        console.log(_renderinput.country_id);
        console.log(_renderinput.domain_id);
        console.log(_renderinput.org_ids);
        console.log(_renderinput.nature_id);
        console.log(_renderinput.mapped_statu);
        console.log(_renderinput.mapped_compliances);
        console.log(_renderinput.selected_geos);

        map_data = _viewPage.make_data_format(0);
        if (IS_EDIT)
            _fetchback.updateMapping(map_data);
        else {
            _fetchback.saveMapping(map_data);
        }

    });

    SubmitButton.click(function() {

        map_data = _viewPage.make_data_format(1);
        if (IS_EDIT)
            _fetchback.updateMapping(map_data);
        else {
            _fetchback.saveMapping(map_data);
        }
    });

    BackButton.click(function() {
        _renderinput.resetField();
        _viewPage.hide();
        _listPage.show();
    });

}
function initialize() {
    _listPage.show();
    _fetchback.getMasterData();
    _fetchback.getStatuMaster(0);
    pageControls();
}

$(document).ready(function(){
    initialize();
});
