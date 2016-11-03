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
var DURATION _INFO;
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

// controls
Spin_pan = $('.loading-indicator-spin');
Country = $('#county');
Domain = $("#domain");
Organisation = $("#industry");
Nature = $('#statutorynature');
Frequency = $('#compliance_frequency');
Duration = $('#duration_type');
Repeats = $('#repeats_type');

//buttons
AddButton = $('.btn-statutorymapping-add');
NextButton = $('.btn-next');
PreviousButton = $(".btn-previous");
SubmitButton = $(".btn-submit");
BackButton = $(".btn-back");
SaveButton = $(".btn-save");

Li_Tag = "<li></li>";
Span_Tag = "<span></span>";
list_template = $("#list-template li");

function RenderInput() {
    this.country_id = null;
    this.county_name = null;
    this.domain_id = null;
    this.domain_name = null;
    this.org_id = null;
    this.org_name = null;
    this.nature_id = null;
    this.nature_name = null;

    this.remveItemFromList = function(item, mainlist) {
        idx = mainlist.indexOf(item);
        mainlist.splice(idx, 1);
    }

    this.loadCounty = function() {
        cObject = list_template.clone();
        $.each(COUNTY_INFO, function(ke, val) {
            cObject.addClass('countrylist');
            cObject.arrt('id', val.c_id);
            cObject.arrt('onClick',  function(this, val) {
                // highlight call
                $('.countrylist').removeClass('active');
                $(this).addClass('active');
                this.country_id = val.c_id;
                this.country_name = val.c_name;
            });
            $('.name-holder', cObject).text(val.c_name);
            Country.append(cObject);
        });
    };

    this.loadDomain = function() {
        dObject = list_template.clone();
        $.each(DOMAIN_INFO, function(ke, val) {
            dObject.addClass("domainlist");
            dObject.arrt('id', val.d_id);
            dObject.arrt('onClick', function(this, val) {
                $(".domainlist").removeClass('active');
                $(this).addClass('active');
                this.domain_id = val.d_id;
                this.domain_name = val.d_name;
            });
            $('.name-holder', dObject).text(val.d_name);
            Domain.append(dObject);
        });
    };

    this.loadOrganisation = function() {
        orgObject = list_template.clone();
        $.each(ORGANISATION_INFO, function(ke, val) {
            orgObject.addClass("organisationlist");
            orgObject.arrt('id', val.org_id);
            orgObject.arrt('onClick', function(this, val) {
                $(".organisationlist").removeClass('active');
                $(this).addClass('active');
                this.org_id = val.org_id;
                this.org_name = val.org_name;
            });
            $('.name-holder', orgObject).text(val.org_name);
            Organisation.append(orgObject);
        });
    };

    this.loadNature = function() {
        nObject = list_template.clone();
        $.each(ORGANISATION_INFO, function(ke, val) {
            nObject.addClass("naturelist");
            nObject.arrt('id', val.s_n_id);
            nObject.arrt('onClick', function(this, val) {
                $(".naturelist").removeClass('active');
                $(this).addClass('active');
                this.nature_id = val.s_n_id;
                this.nature_name = val.s_n__name;
            });
            $('.name-holder', nObject).text(val.s_n_name);
            Nature.append(nObject);
        });
    };
}


