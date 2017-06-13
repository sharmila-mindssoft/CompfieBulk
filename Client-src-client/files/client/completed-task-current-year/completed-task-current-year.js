var legalentitiesList;
var divisionsList;
var categoryList;
var unitsList;
var domainsList;
var frequencyList;
var actList;

var file_list = [];
var usersList;
var statutoriesList;

var CURRENT_TAB = 1;
var sno = 0;
var totalRecord;
var lastAct = '';
var startcount = 0;
var ACCORDIONCOUNT = 0;

var ULRow = $("#templates .ul-row li");
var legalentityul = $("#legalentity");
var divisionul = $("#division");
var categoryul = $("#category");
var unitul = $("#units");
var domainul = $("#domain");
var actul = $("#level_1");
var frequencyul = $("#frequency");

var LE_ID = null;

var ACTIVE_UNITS = [];
var ACTIVE_FREQUENCY = [];

var NextButton = $('#btn-next');
var PreviousButton = $('#btn-previous');
var SubmitButton = $("#btn-submit");
var ShowMore = $(".btn-showmore");
var Filter_List = $('.filter-list');

function activate_assignee(element, checkval, checkname, clickvalue) {
    $("#assigneeval" + clickvalue).val(checkname);
    $("#assignee" + clickvalue).val(checkval);
}

//load available compliance in third wizard
function load_thirdwizard() {
    if (sno == 0) {
        $('#accordion').empty();
    }

    for (var entity in statutoriesList) {

        var actname = statutoriesList[entity]["level_1_statutory_name"];
        var actCompliances = statutoriesList[entity]["pr_compliances"];
        // alert(LastAct);
        // alert(actname);
        if (LastAct != actname) {
            ACCORDIONCOUNT += 1;
            // accordion-list
            var accRow = $('#templates .accordion-list .panel');
            var clone1 = accRow.clone();

            $('.actname', clone1).html(actname);
            $('.panel-title a', clone1).attr('href', '#collapse' + ACCORDIONCOUNT);
            $('.panel-title a', clone1).attr('aria-controls', 'collapse' + ACCORDIONCOUNT);
            if (ACCORDIONCOUNT == 1) { //For First group open collapse
                $('.panel-title a', clone1).attr('aria-expanded', true);
                $('.panel-title a', clone1).removeClass('collapsed');
                $('.coll-title', clone1).addClass('in');
            }
            $('.coll-title', clone1).attr('id', 'collapse' + ACCORDIONCOUNT);
            $('#accordion').append(clone1);
            LastAct = actname;
        }
        for (var ac in actCompliances) {
            sno++;
            var compliance_id = actCompliances[ac]["compliance_id"];
            var compliance_name = actCompliances[ac]["compliance_name"];

            compliance_name = compliance_name + ' - ' + compliance_id;

            var compliance_description = actCompliances[ac]["description"];
            var assignee_name = actCompliances[ac]["assignee_name"];
            var assignee_id = actCompliances[ac]["assignee_id"];
            var frequency = actCompliances[ac]["compliance_task_frequency"];
            var statutory_date = actCompliances[ac]["pr_statutory_date"];
            var due_date = actCompliances[ac]["due_date"];
            var statutorydate = actCompliances[ac]["statutory_date"];
            var complianceDetailtableRow = $('#statutory-values .table-statutory-values .compliance-details');
            var clone2 = complianceDetailtableRow.clone();

            $('.compliancetask i', clone2).attr('data-original-title', compliance_description);
            $('.compliancetask span', clone2).html(compliance_name);
            $('.compliancefrequency', clone2).html(frequency +
                '<input type="hidden" id="complianceid' + sno + '" value="' + compliance_id + '"/>' +
                '<input type="hidden" id="compliancename' + sno + '" value="' + compliance_name + '"/>' +
                '<input type="hidden" id="frequency' + sno + '" value="' + frequency + '"/>');
            $('.statutorydate', clone2).html(statutory_date);
            $('.duedate', clone2).html('<input type="text" value="' + due_date + '" readonly="readonly" class="form-control input-sm" id="duedate' + sno + '" />');
            $('.completiondate', clone2).html('<input type="text" value="" readonly="readonly" class="form-control input-sm" id="completiondate' + sno + '" />');
            $('.documentupload', clone2).html('<input type="file" class="form-control input-sm" id="upload' + sno + '" multiple />');
            //$('.assignee', clone2).html('<input type="text" value="'+assignee_name+'" class="input-box icon-autocomplete" id="assigneeval'+sno+'" style="width:100px;" /> <input type="hidden" id="assignee'+sno+'" value="'+assignee_id+'"> <div id="autocomplete_assignee'+sno+'" class="ac-textbox default-display-none"> <ul id="ulist_assignee'+sno+'" style="width:115px;" class="hidemenu"></ul></div>');

            $('.assignee', clone2).html('<input class="form-control input-sm domain" type="text" value="' + assignee_name + '"  id="assigneeval' + sno + '" ><i class="fa-1-2x form-control-feedback"></i><input type="hidden"  id="assignee' + sno + '" value="' + assignee_id + '"><div id="autocomplete_assignee' + sno + '"  class="ac-textbox default-display-none"><ul class="hidemenu"></ul></div>');

            $('.completedstatus', clone2).html(' <input type="checkbox" class="text-center" id="completedstatus' + sno + '"> <label for="checkbox8"></label>');
            $('#collapse' + ACCORDIONCOUNT + ' .tbody-pastRecords').append(clone2);

            $("#upload" + sno).on("change", function(e) {
                client_mirror.uploadFile(e, function result_data(data) {
                    if (data != 'File max limit exceeded' || data != 'File content is empty') {
                        uploadFile = data;
                        file_list = data
                    } else {
                        file_list = [];
                    }
                });
            });

            $("#duedate" + sno).datepicker({
                changeMonth: true,
                changeYear: true,
                numberOfMonths: 1,
                dateFormat: "dd-M-yy",
                monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
                ],
            });

            $("#completiondate" + sno).datepicker({
                changeMonth: true,
                changeYear: true,
                numberOfMonths: 1,
                dateFormat: "dd-M-yy",
                monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
                ],
            });

            var User = $("#assigneeval" + sno);
            var Userid = $(".assignee");
            var AcUser = $("#ac-domain");

            User.keyup(function(e) {
                var text_val = User.val().trim();
                commonAutoComplete(e, AcUser, Userid, text_val, usersList, "employee_name", "user_id", function(val) {
                    onUserAutoCompleteSuccess(val);
                });
            });
            onUserAutoCompleteSuccess = function(val) {
                User.val(val[1]);
                Userid.val(val[0]);
                AcUser.focus();
            }
        }
    }

    $(".hidemenu").click(function() {
        $(".ac-textbox").hide();
    });

    if (totalRecord == 0) {
        var no_record_row = $("#templates .table-no-record");
        var noclone = no_record_row.clone();
        $('#accordion').append(noclone);
        ShowMore.hide();
        $(".total_count_view").hide();

    } else {
        $(".total_count").text('Showing 1 to ' + sno + ' of ' + totalRecord + ' entries');
        $(".total_count_view").show();
        if (sno >= totalRecord) {
            ShowMore.hide();
        } else {
            ShowMore.show();
        }
    }
    hideLoader();
}

//validation in first wizard
function validate_firsttab() {
    if (legalentityul.find('.active').text() == '') {
        displayMessage(message.legalentity_required);
        return false;
    } else if (unitul.find('.active').text() == '') {
        displayMessage(message.unit_required + "--");
        return false;
    }
}

//validation in second wizard
function validate_secondtab() {
    if ($('.domainlist.active').text() == '') {
        displayMessage(message.domain_required);
        return false;
    } else if (frequencyul.find('.active') == 0) {
        displayMessage(message.frequency_required);
        return false;
    } else {
        return true;
    }
}

function validate_thirdtab() {
    return true;
}

//convert string to date format
function convert_date(data) {
    var date = data.split("-");
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    for (var j = 0; j < months.length; j++) {
        if (date[1] == months[j]) {
            date[1] = months.indexOf(months[j]) + 1;
        }
    }
    if (date[1] < 10) {
        date[1] = '0' + date[1];
    }
    return new Date(date[2], date[1] - 1, date[0]);
}

//find date difference between two dates
function daydiff(first, second) {
    return (second - first) / (1000 * 60 * 60 * 24)
}

//save past records data
function submitcompliance() {
    displayLoader();
    var unit_id = parseInt(unitul.find('.active').attr('id'));
    compliance_list = [];

    for (var i = 1; i <= sno; i++) {
        var complianceApplicable = false;

        if ($('#completedstatus' + i).is(":checked")) {
            complianceApplicable = true;
        }
        console.log("complianceApplicable--" + complianceApplicable + "--" + i);
        if (complianceApplicable) {
            var compliance_id = parseInt($('#complianceid' + i).val());
            //var validity_date = $('#validitydate'+i).val();
            var due_date = $('#duedate' + i).val();
            var completion_date = $('#completiondate' + i).val();
            var completed_by = $('#assignee' + i).val();
            var frequency_ = $('#frequency' + i).val();
            var compliance_name = $('#complaincename' + i).val();
            if (completed_by != '') completed_by = parseInt(completed_by);

            if (due_date == '') {
                displayMessage(message.duedate_required);
                hideLoader();
                return false;
            } else if (completion_date == '') {
                displayMessage(message.compliancedate_required);
                hideLoader();
                return false;
            } else if (completed_by == null) {
                displayMessage(message.assignee_required);
                hideLoader();
                return false;
            }

            compliance = client_mirror.getPastRecordsComplianceDict(unit_id, compliance_id, due_date, completion_date, file_list, completed_by);
            compliance_list.push(compliance);
        }
    }
    console.log(JSON.stringify(compliance_list));
    if (compliance_list.length == 0) {
        displayMessage(message.select_atleast_one_compliance);
        hideLoader();
        return false;
    }

    function onSuccess(data) {
        displaySuccessMessage(message.compliance_submit_success);
        clearValues('legalentity');
        CURRENT_TAB = 1;
        $("#accordion").empty();
        getLegalEntity();
        showTab();
        $(".total_count_view").hide();
        hideLoader();
    }

    function onFailure(error) {
        displayMessage(error[1]["error"]);
        hideLoader();
    }
    client_mirror.savePastRecords(parseInt(LE_ID), compliance_list,
        function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        }
    );
}

//get compliances for selected unit
function getStatutories() {
    displayLoader();
    var le_id = null;
    var u_id = null;
    var d_id = null;
    var actname = null;
    var freqname = null;

    le_id = legalentityul.find("li.active").attr("id");
    u_id = unitul.find("li.active").attr("id");
    d_id = domainul.find("li.active").attr("id");
    actname = actul.find("li.active").text();
    if (frequencyul.find('li.active').attr('id') != undefined) {
        freqname = frequencyul.find("li.active").attr("id");
    }

    if (u_id != null && d_id != null) {
        function onSuccess(data) {
            //console.log(JSON.stringify(data["statutory_wise_compliances"]));
            statutoriesList = data["statutory_wise_compliances"];
            usersList = data["pr_users"];
            totalRecord = data["total_count"];
            load_thirdwizard();
            hideLoader();
        }

        function onFailure(error) {
            hideLoader();
        }
        //pastRecordsCountryId
        client_mirror.getStatutoriesByUnit(
            parseInt(le_id), parseInt(u_id), parseInt(d_id), actname, freqname, sno,
            function(error, response) {
                if (error == null) {
                    onSuccess(response);
                } else {
                    onFailure(error);
                }
            }
        );
    }
}

function loadDivision() {
    $.each(divisionsList, function(key, value) {
        id = value.div_id;
        text = value.div_name;

        var le_id = legalentityul.find("li.active").attr("id");
        if (le_id == value.le_id) {
            var clone = ULRow.clone();
            clone.html(text + '<i></i>');
            clone.attr('id', id);
            divisionul.append(clone);
            clone.click(function() {
                activateList(this, 'division');
            });
        }
    });
}

function loadCategory() {
    $.each(categoryList, function(key, value) {
        id = value.cat_id;
        text = value.cat_name;

        var le_id = legalentityul.find("li.active").attr("id");
        var div_id = '';
        if (divisionul.find("li.active").attr("id") != undefined) {
            div_id = divisionul.find("li.active").attr("id");
        }
        if (le_id == value.le_id && (div_id == '' || div_id == value.div_id)) {
            var clone = ULRow.clone();
            clone.html(text + '<i></i>');
            clone.attr('id', id);
            categoryul.append(clone);
            clone.click(function() {
                activateList(this, 'category');
            });
        }
    });
}

function loadDomain() {
    $.each(domainsList, function(key, value) {
        id = value.d_id;
        text = value.d_name;

        var le_id = legalentityul.find("li.active").attr("id");

        if (le_id == value.le_id) {
            var clone = ULRow.clone();
            clone.html(text + '<i></i>');
            clone.attr('id', id);
            domainul.append(clone);
            clone.click(function() {
                activateList(this, 'domain');
            });
        }
    });
}

function loadUnit() {
    $.each(unitsList, function(key, value) {
        id = value.unit_id;
        text = value.unit_code + "-" + value.unit_name;
        var div_id = '';
        if (divisionul.find("li.active").attr("id") != undefined) {
            div_id = divisionul.find("li.active").attr("id");
        }
        var cat_id = '';
        if (categoryul.find("li.active").attr("id") != undefined) {
            cat_id = categoryul.find("li.active").attr("id");
        }
        var le_id = legalentityul.find("li.active").attr("id");
        if (le_id == value.legal_entity_id && (div_id == '' || div_id == value.division_id) && (cat_id == '' || cat_id == value.category_id)) {
            var clone = ULRow.clone();
            clone.html(text + '<i></i>');
            clone.attr('id', id);
            unitul.append(clone);
            clone.click(function() {
                activateList(this, 'units');
            });
        }
    });
}

function loadAct() {
    var d_id = domainul.find("li.active").attr("id");
    $.each(actList, function(key, value) {
        id = key;
        text = value;
        if (d_id == key) {
            for (var i = 0; i < text.length; i++) {
                var clone = ULRow.clone();
                clone.html(text[i] + '<i></i>');
                clone.attr('id', text[i]);
                actul.append(clone);
                clone.click(function() {
                    activateList(this, 'level_1');
                });
            }
        }
    });
}

function loadFrequency() {
    $.each(frequencyList, function(key, value) {
        id = value.frequency_id;
        text = value.frequency;
        var clone = ULRow.clone();
        clone.html(text + '<i></i>');
        clone.attr('id', text);
        frequencyul.append(clone);
        clone.click(function() {
            activateList(this, 'frequency');
        });
    });
}

function pageControls() {
    NextButton.click(function() {
        //$('.tbody-compliance-list').empty();
        CURRENT_TAB += 1;
        showTab();
    });
    PreviousButton.click(function() {
        $(".total_count_view").hide();
        CURRENT_TAB = CURRENT_TAB - 1;
        // alert(CURRENT_TAB);
        showTab();
    });
    ShowMore.click(function() {
        getStatutories();
        //callAPI(GET_COMPLIANCE);
    });
    SubmitButton.click(function() {
        if (validate_thirdtab()) {
            displayLoader();
            submitcompliance();
            // setTimeout(function() {
            //     callAPI(SUBMIT_API)
            // }, 500);

        }
    });
    showTab();

    Filter_List.keyup(function() {
        var currentFilter = '#' + $(this).attr("class").split(' ').pop() + ' > li';
        var searchText = $(this).val().toLowerCase();
        $(currentFilter).each(function() {
            var currentLiText = $(this).text().toLowerCase();
            showCurrentLi = currentLiText.indexOf(searchText) !== -1;
            $(this).toggle(showCurrentLi);
        });
    });
}


function showTab() {
    hideall = function() {
        $('.statutory_mapping_tab li').removeClass('active');
        $('.tab-pane').removeClass('active in');
        $('#tab1').hide();
        $('#tab2').hide();
        $('#tab3').hide();
        ShowMore.hide();
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
        }
    }
    disabletabevent = function() {
        $('.tab-step-1 a').removeAttr('href');
        $('.tab-step-2 a').removeAttr('href');
        $('.tab-step-3 a').removeAttr('href');
    }

    if (CURRENT_TAB == 1) {
        hideall();
        disabletabevent();
        enabletabevent(1);
        $('.tab-step-1').addClass('active')
        $('#tab1').addClass("active in");
        $('#tab1').show();
        SubmitButton.hide();
        NextButton.show();
    } else if (CURRENT_TAB == 2) {
        if (validateFirstTab() == false) {
            CURRENT_TAB -= 1;
            return false;
        } else {
            //displayLoader();
            hideall();
            enabletabevent(2);
            $('.tab-step-2').addClass('active')
            $('#tab2').addClass('active in');
            $('#tab2').show();
            PreviousButton.show();
            NextButton.show();
        }
    } else if (CURRENT_TAB == 3) {

        if (validateSecondTab() == false) {
            CURRENT_TAB -= 1;
            return false;
        } else {
            displayLoader();
            var le_id = null,
                u_id = null,
                d_id = null,
                actname = null,
                freqname = null;

            le_id = legalentityul.find("li.active").attr("id");
            u_id = unitul.find("li.active").attr("id");
            d_id = domainul.find("li.active").attr("id");
            actname = actul.find("li.active").text();
            if (frequencyul.find('li.active').attr('id') != undefined) {
                freqname = frequencyul.find("li.active").attr("id");
            }

            client_mirror.getStatutoriesByUnit(
                parseInt(le_id), parseInt(u_id), parseInt(d_id), actname, freqname, startcount,
                function(error, data) {
                    if (error == null) {
                        hideall();
                        enabletabevent(3);
                        $('.tab-step-3').addClass('active')
                        $('#tab3').addClass('active in');
                        $('#tab3').show();
                        PreviousButton.show();
                        SubmitButton.show();
                        statutoriesList = data["statutory_wise_compliances"];
                        usersList = data["pr_users"];
                        totalRecord = data["total_count"];
                        ACCORDIONCOUNT = 0
                        load_thirdwizard();
                    } else {
                        displayMessage(error);
                        hideLoader();
                        CURRENT_TAB -= 1;
                        return false;
                    }
                }
            );
        }
    }
};



//load master date in first wizard
function load_firstwizard() {
    divisionul.empty();
    categoryul.empty();
    unitul.empty();
}

function validateFirstTab() {
    var le_id = legalentityul.find("li.active").attr("id");
    var u_id = unitul.find("li.active").attr("id");

    if (le_id == undefined) {
        displayMessage(message.legalentity_required)
        return false;
    } else if (u_id == undefined) {
        displayMessage(message.unit_required);
        return false;
    } else {
        LastAct = '';
        SCOUNT = 1;
        ACOUNT = 1;
        return true;
    }
};

function validateSecondTab() {
    var d_id = domainul.find("li.active").attr("id");
    var f_id = frequencyul.find("li.active").attr("id");

    if (d_id == undefined) {
        displayMessage(message.domain_required);
        return false;
    } else if (f_id == undefined) {
        displayMessage(message.compliancefrequency_required);
        return false;
    } else {
        LastAct = '';
        SCOUNT = 1;
        ACOUNT = 1;
        sno = 0;
        return true;
    }
}



function getPastRecords() {
    displayLoader();

    function onSuccess(data) {
        divisionsList = data["client_divisions"];
        categoryList = data["pr_categories"];
        unitsList = data["in_units"];
        actList = data["level_1_statutories"];
        frequencyList = data["compliance_frequency"];
        domainsList = data["domains"];
        loadDivision();
        loadCategory();
        loadDomain();
        loadUnit();
        loadAct();
        loadFrequency();
        hideLoader();
    }

    function onFailure(error) {
        hideLoader();
    }
    client_mirror.getPastRecordsFormData(parseInt(LE_ID),
        function(error, response) {
            if (error == null) {
                onSuccess(response);
            } else {
                onFailure(error);
            }
        }
    );
}

function getLegalEntity() {
    legalentityul.empty();
    legalentitiesList = client_mirror.getSelectedLegalEntity();
    $.each(legalentitiesList, function(key, value) {
        id = value.le_id;
        text = value.le_name;
        var clone = ULRow.clone();
        clone.html(text + '<i></i>');
        clone.attr('id', id);
        legalentityul.append(clone);
        clone.click(function() {
            LE_ID = clone.attr('id');
            activateList(this, 'legalentity');
        });
    });

}

function activateList(element, levelvalue) {
    $('#' + levelvalue + ' li').each(function(index, el) {
        $(el).removeClass('active');
        $(el).find('i').removeClass('fa fa-check pull-right');
    });

    $(element).addClass('active');
    $(element).find('i').addClass('fa fa-check pull-right');
    clearValues(levelvalue);
    loadChild(levelvalue);
}

//clear list values
function clearValues(levelvalue) {
    if (levelvalue == 'legalentity') {
        ACTIVE_UNITS = [];
        ACTIVE_FREQUENCY = [];
        divisionul.empty();
        categoryul.empty();
        domainul.empty();
        unitul.empty();
        actul.empty();
        frequencyul.empty();
    } else if (levelvalue == 'division') {
        categoryul.empty();
        domainul.empty();
        unitul.empty();
        actul.empty();
        frequencyul.empty();
        ACTIVE_UNITS = [];
        ACTIVE_FREQUENCY = [];
    } else if (levelvalue == 'category') {
        domainul.empty();
        unitul.empty();
        actul.empty();
        frequencyul.empty();
        ACTIVE_UNITS = [];
        ACTIVE_FREQUENCY = [];
    } else if (levelvalue == 'units') {
        domainul.empty();
        actul.empty();
        frequencyul.empty();
        ACTIVE_FREQUENCY = [];
    } else if (levelvalue == 'domain') {
        actul.empty();
        frequencyul.empty();
        ACTIVE_FREQUENCY = [];
    }

}

function loadChild(levelvalue) {
    if (levelvalue == 'legalentity') {
        getPastRecords();
    } else if (levelvalue == 'division') {
        loadCategory();
        loadUnit();
        loadDomain();
        loadFrequency();
    } else if (levelvalue == 'category') {
        loadUnit();
        loadDomain();
        loadFrequency();
    } else if (levelvalue == 'units') {
        loadDomain();
        loadFrequency();
    } else if (levelvalue == 'domain') {
        loadAct();
        loadFrequency();
    }
}

//initialization & master list filter
$(document).ready(function() {
    getLegalEntity();
    pageControls();
});