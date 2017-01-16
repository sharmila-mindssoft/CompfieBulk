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
        displayLoader();
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
                hideLoader();
            }
        );
    };

    this.getMapDatabyId = function(mapping_id, compliance_id) {
        displayLoader();
        fetch.getStatutoryMappingsEdit(mapping_id, compliance_id,
            function(status, response){
                if (status != null) {
                    displayMessage(status);
                }
                else {
                    _renderinput.countryId = response.c_id;
                    _renderinput.domainId = response.d_id;
                    _renderinput.natureId = response.s_n_id;
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
                            if (v.p_maps != null)
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
                            // alert(info);
                            _renderinput.mapped_statu.push(info);
                        }
                    });
                    _renderinput.renderStatuGrid();
                    _renderinput.renderComplianceGrid();

                    showTab();
                    _listPage.hide();
                    _viewPage.show();
                    hideLoader();
                }
            }
        );
    }

    this.changeStatus = function(m_id, sts) {
        displayLoader();
        fetch.changeStatutoryMappingStatus(m_id, sts, function(status, response) {
            if (status != null) {
                possibleFailure(status);
            }
            else {
                ap_status = $('.ap-status-li.active').attr('value');
                _fetchback.getMappedList(ap_status, 0);
            }
            hideLoader();
        });
    };

    this.updateStatutory = function(s_id, s_name, l_position) {
        if (_renderinput.last_selected >= l_position) {
            displayMessage("Select proper levels before add/edit");
            return false;
        }
        p_ids = _renderinput.s_pids;
        p_names = _renderinput.s_names;
        fetch.updateStatutory(s_id, s_name, p_ids, p_names, function(status, response){
            if (status != null) {
                possibleFailure(status);
            }
            else {
                $('.txtsname').val('');
                $('#dv'+ l_position).val('');
                $('#dvid'+ l_position).val('');
                $('#dvpid'+ l_position).val('');
                _fetchback.getStatuMaster(l_position, function() {
                    if(p_ids.length > 0) {
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
        })
    };

    this.saveStautory = function(s_l_id, s_name, l_position){
        if (_renderinput.last_selected >= l_position) {
            displayMessage("Select proper levels before add/edit");
            return false;
        }
        d_id = _renderinput.domainId;
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
                    $('.txtsname').val('');
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
        displayLoader();
        fetch.saveStatutoryMapping(data, function(status, response) {
            if (status == null) {
                // show list
                if (IS_SAVE == true) {
                    displaySuccessMessage(msg.mapping_success);
                }
                else {
                    displaySuccessMessage(msg.mapping_submit_success);
                }

                _viewPage.hide();
                _listPage.show();
                _renderinput.resetField();

            }
            else {

                possibleFailure(status, response.compliance_name);
                return false;
            }
            hideLoader();
        });
    };

    this.updateMapping = function(data) {
        displayLoader();
        fetch.updateStatutoryMapping(data, function(status, response) {
            if (status == null) {
                if (IS_SAVE == true) {
                    displaySuccessMessage(msg.mapping_success);
                }
                else {
                    displaySuccessMessage(msg.mapping_submit_success);
                }
                _viewPage.hide();
                _listPage.show();
                _renderinput.resetField();
            }
            else {

                possibleFailure(status);
                return false;
            }
            hideLoader();
        });
    };

    this.validateAuthentication = function() {
        var password = CurrentPassword.val().trim();
        if (password.length == 0) {
            displayMessage(msg.password_required);
            CurrentPassword.focus();
            return false;
        } else {
            validateMaxLength('password', password, "Password");
        }
        fetch.verifyPassword(password, function(error, response) {
            if (error == null) {
                isAuthenticate = true;
                Custombox.close();
            } else {
                possibleFailure(error);
            }
        });
    };

    this.uploadFileProcess = function() {
        displayLoader();
        frmData = _renderinput.form_data;
        fetch.uploadFormatFile(frmData, function(error, response){
            if (error == null) {

            }
            else {
                possibleFailure(error);
            }
        });
    }
}

//
// Render List Page
//
function ListPage() {

    this.renderList = function(data, tRecord) {
        $('.tbl-statutorymapping-list .table-no-record').remove();
        $('.tbl-statutorymapping-list .mapping-row').remove();
        $('.tbl-statutorymapping-list .compliance-row').remove();

        if (data.length == 0) {
            norow = $('#templates .table-no-record').clone();
            $('.tbl-statutorymapping-list').append(norow);
            return;
        }
        // $('.tbl-statutorymapping-list tr').find('mapping_row');
        // $('.tbl-statutorymapping-list tr').find('compliance_row');

        function comp_row(rowObjec, cdata, mapping_id) {
            var x = 1;
            $.each(cdata, function(k, c) {
                row = $('#templates .compliance-row').clone();

                $('.comp_name', row).text(c.comp_name);
                $('.comp_edit', row).attr('title', 'Client here to edit compliance');
                $('.comp_edit', row).addClass('fa-pencil text-primary');
                $('.comp_edit', row).on('click', function() {
                    _listPage.displayMappingEdit(mapping_id, c.comp_id);
                });
                if (c.is_approved == 4) {
                    console.log(c.remarks);
                    row.addClass('rejected_row');
                    $('.comp_approval_status', row).append(
                        '<i class="fa fa-info-circle text-primary c-pointer" data-toggle="tooltip" title="'+ c.remarks +'" data-original-title="Rejected reason goes here."></i>'
                    );
                }

                $('.comp_approval_status', row).append(c.approval_status_text);
                rowObjec.append(row);
            });
        }

        function showTitle(e){
          if(e.className == "fa c-pointer map_status fa-times text-danger"){
            e.title = 'Click Here to Activate';
          }
          else if(e.className == "fa c-pointer map_status fa-check text-success")
          {
            e.title = 'Click Here to Deactivate';
          }
        }

        var j = 1;
        $.each(data, function(k, v) {
            orgNames = v.i_names.join(' , ');
            s_names = v.s_maps.join(', ');
            crow = $('#templates .mapping-row').clone();
            $('.sno', crow).text(j);
            $('.c_name', crow).text(v.c_name);
            $('.d_name', crow).text(v.d_name);
            $('.org_name', crow).text(orgNames);
            $('.nature_name', crow).text(v.s_n_name);
            $('.s_name', crow).text(s_names);
            $('.map_edit', crow).attr('title', 'Click here to edit');
            $('.map_edit', crow).addClass('fa-pencil text-primary');
            $('.map_edit', crow).on('click', function() {
                _listPage.displayMappingEdit(v.m_id, null);
            });
            if (v.is_active == true){
                $('.map_status', crow).attr('title', msg.active_tooltip);
                $('.map_status', crow).addClass("fa-check text-success");

            }
            else {
                $('.map_status', crow).attr('title', msg.deactive_tooltip);
                $('.map_status', crow).addClass("fa-times text-danger");

            }
            $('.map_status', crow).hover(function(){
                showTitle(this);
            });
            $('.map_status', crow).on('click', function(e) {
                if (v.is_active == true) {
                    statusmsg = msg.deactive_message;
                    passStatus = false;
                }
                else {
                    statusmsg = msg.active_message;
                    passStatus = true;
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
                                    _fetchback.changeStatus(v.m_id, passStatus);
                                }
                            },
                        });
                        e.preventDefault();
                    }
                });
            });

            $('.approval_status', crow).text("");
            j = j + 1;
            $('.tbl-statutorymapping-list').append(crow);
            comp_row($('.tbl-statutorymapping-list'), v.mapped_comps, v.m_id);
        });
    };

    this.displayMappingEdit = function(map_id, comp_id) {
        _renderinput.resetField();
        _fetchback.getMapDatabyId(map_id, comp_id);
        IS_EDIT = true;
    };

    this.show = function() {
        CURRENT_TAB = 1;
        ListScreen.show();
        ViewScreen.hide();
        ap_status = $('.ap-status-li.active').attr('value');
        _fetchback.getMappedList(ap_status, 0);
    };
    this.hide = function() {
        ListScreen.hide();
    };
    this.listFilter = function() {
        country_search = $('#country-search').val().toLowerCase();
        domain_search = $('#domain-search').val().toLowerCase();
        org_search = $('#org-search').val().toLowerCase();
        nature_search = $('#nature-search').val().toLowerCase();
        statu_search = $('#statu-search').val().toLowerCase();

        map_status = $('.search-status-li.active').attr('value');
        // usr_disable = $('#ap-status-list.active').attr('value');

        filteredList = []
        $.each(STATU_MAPPINGS, function(k, data){
            c_name = data.c_name.toLowerCase();
            d_name = data.d_name.toLowerCase();
            org_name = data.i_names.join(' , ');
            org_name = org_name.toLowerCase();
            nature_name = data.s_n_name.toLowerCase();
            map_name = data.s_maps.join(' , ');
            map_name = map_name.toLowerCase();

            if (
                (~c_name.indexOf(country_search)) && (~d_name.indexOf(domain_search)) &&
                (~org_name.indexOf(org_search)) && (~nature_name.indexOf(nature_search)) &&
                (~map_name.indexOf(statu_search)) && ((map_status == 'all') || (parseInt(map_status) == data.is_active))
            ) {
                filteredList.push(data);
            }
        });
        _listPage.renderList(filteredList, filteredList.length);
    };
}


//
// Render View Pages
//
function ViewPage() {
    this.showFirstTab = function(){
        _renderinput.loadCounty();
    };
    this.validateFirstTab = function() {
        if (_renderinput.countryId == null) {
            displayMessage(msg.country_required);
            return false;
        }
        else if (_renderinput.domainId == null) {
            displayMessage(msg.domain_required);
            return false;
        }
        else if (_renderinput.selected_iids.length == 0) {
            displayMessage(msg.industry_required);
            return false;
        }
        else if (_renderinput.natureId == null) {
            displayMessage(msg.statutorynature_required);
            return false;
        }
        return true;
    };
    this.showSecondTab = function(){
        _renderinput.last_selected = null;
        $('#tbody-statutory-level').empty();;
        _renderinput.loadStatuesLevels(0);
    };
    this.validateSecondTab = function() {
        if (_renderinput.mapped_statu.length == 0) {
            displayMessage(msg.nostatutory_selected);
            return false;
        }
        return true;
    };
    this.showThirdTab = function(){
        Provision.focus();
        _renderinput.loadFrequency();
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
        else if ((ReferenceLink.val().length > 0) && (isWebUrl(ReferenceLink) == false)) {
            // isValid = isWebUrl(ReferenceLink);
            // if (isValid == false) {
            displayMessage(msg.invalid_reference);
            return false;
            // }
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
                else if(RepeatsEvery.val().trim() == 0) {
                    displayMessage(msg.invalid_repeatsevery);
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
        if (_renderinput.selected_geos.length == 0)
        {
            return false;
        }
        map_data = {};
        if (_renderinput.mapping_id != null) {
            map_data["m_id"] = _renderinput.mapping_id;
        }
        map_data["c_id"] = _renderinput.countryId;
        map_data["d_id"] = _renderinput.domainId;
        map_data["i_ids"] = _renderinput.selected_iids;
        map_data["s_n_id"] = _renderinput.natureId;
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
