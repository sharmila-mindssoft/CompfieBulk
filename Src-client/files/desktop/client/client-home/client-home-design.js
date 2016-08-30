$(document).ready(function () {
  // written  by gnaneswaran
  $('.btn-country').click(function () {
    $('.btn-country').addClass('active');
    $('.btn-domain').removeClass('active');
    $('.btn-date').removeClass('active');
    $('.textboxcountry').show();
    $('.textboxdomain').hide();
    $('.date-para1').hide();
  });
  $('.btn-domain').click(function () {
    $('.btn-country').removeClass('active');
    $('.btn-domain').addClass('active');
    $('.btn-date').removeClass('active');
    $('.textboxcountry').hide();
    $('.textboxdomain').show();
    $('.date-para1').hide();
  });
  $('.btn-date').click(function () {
    $('.btn-country').removeClass('active');
    $('.btn-domain').removeClass('active');
    $('.btn-date').addClass('active');
    $('.textboxcountry').hide();
    $('.textboxdomain').hide();
    $('.date-para1').show();
  });
  // code end here
  $('#radio6').prop('checked', true);
  $('#domainradio').prop('checked', true);
  $('#year-para').hide();
  $('.dropdown-box-container').click(function () {
    $('.filter-dropdown-container').slideToggle();
  });
  // window.testSelAll2 = $('.testSelAll2').SumoSelect({
  //     selectAll: false
  // });
  $('#entity-auto').hide();
  $('#division-auto').hide();
  $('#unit-auto').hide();
  $('.textboxdomain').show();
  $('.textboxgroup').hide();
  $('.textboxcompany').hide();
  $('.textboxdivision').hide();
  $('.textboxbranch').hide();
  $('.textboxbusiness').hide();
  $('.textboxdate').show();
  $('#previousyear').show();
  $('#nextyear').show();
  $('.btn-group').click(function () {
    $('.btn-group').addClass('de-active');
    $('.textboxgroup').hide();
    $('.textboxcompany').hide();
    $('.textboxdivision').hide();
    $('.textboxbranch').hide();
    $('.textboxbusiness').hide();
    $('#previousyear').show();
    $('#nextyear').show();
    if ($('.compliance-status-tab').hasClass('active')) {
      loadGroup();
    } else if ($('.not-complied-tab').hasClass('active')) {
      ageingwiseCompliance();
    } else if ($('.applicability-status-tab').hasClass('active')) {
      loadPieChart();
    } else if ($('.escalations-tab').hasClass('active')) {
      loadEscalations();
    } else if ($('.compliance-report-tab').hasClass('active')) {
    } else if ($('.trend-chart-tab').hasClass('active')) {
      loadTrendChart();
    }
  });
  $('#radio2').click(function () {
    $('.textboxgroup').hide();
    $('.textboxcompany').show();
    $('.textboxdivision').hide();
    $('.textboxbranch').hide();
    $('.textboxbusiness').hide();
    $('#previousyear').show();
    $('#nextyear').show();
  });
  $('#radio3').click(function () {
    $('.textboxgroup').hide();
    $('.textboxcompany').hide();
    $('.textboxdivision').show();
    $('.textboxbranch').hide();
    $('.textboxbusiness').hide();
    $('#previousyear').show();
    $('#nextyear').show();
  });
  $('#radio4').click(function () {
    $('.textboxgroup').hide();
    $('.textboxcompany').hide();
    $('.textboxdivision').hide();
    $('.textboxbranch').show();
    $('.textboxbusiness').hide();
    $('#previousyear').show();
    $('#nextyear').show();
  });
  $('.btn-group').click(function () {
    $('.btn-group').addClass('active');
    $('.btn-business-group').removeClass('active');
    $('.btn-legal-entity').removeClass('active');
    $('.btn-division').removeClass('active');
    $('.btn-unit').removeClass('active');
    $('.textboxbusiness').hide();
    $('.textboxcompany').hide();
    $('.textboxdivision').hide();
    $('.textboxbranch').hide();
  });
  $('.btn-business-group').click(function () {
    $('.btn-group').removeClass('active');
    $('.btn-business-group').addClass('active');
    $('.btn-legal-entity').removeClass('active');
    $('.btn-division').removeClass('active');
    $('.btn-unit').removeClass('active');
    $('.textboxbusiness').show();
    $('.textboxcompany').hide();
    $('.textboxdivision').hide();
    $('.textboxbranch').hide();
  });
  $('.btn-legal-entity').click(function () {
    $('.btn-business-group').removeClass('active');
    $('.btn-legal-entity').addClass('active');
    $('.btn-division').removeClass('active');
    $('.btn-unit').removeClass('active');
    $('.textboxbusiness').hide();
    $('.textboxcompany').show();
    $('.textboxdivision').hide();
    $('.textboxbranch').hide();
  });
  $('.btn-division').click(function () {
    $('.btn-business-group').removeClass('active');
    $('.btn-legal-entity').removeClass('active');
    $('.btn-division').addClass('active');
    $('.btn-unit').removeClass('active');
    $('.textboxbusiness').hide();
    $('.textboxcompany').hide();
    $('.textboxdivision').show();
    $('.textboxbranch').hide();
  });
  $('.btn-unit').click(function () {
    $('.btn-business-group').removeClass('active');
    $('.btn-legal-entity').removeClass('active');
    $('.btn-division').removeClass('active');
    $('.btn-unit').addClass('active');
    $('.textboxbusiness').hide();
    $('.textboxcompany').hide();
    $('.textboxdivision').hide();
    $('.textboxbranch').show();
  });
  $('.btn-consolidated').click(function () {
    $('.btn-consolidated').addClass('active');
  });
  $('#radio5').click(function () {
    $('.textboxgroup').hide();
    $('.textboxcompany').hide();
    $('.textboxdivision').hide();
    $('.textboxbranch').hide();
    $('.textboxbusiness').show();
    $('#previousyear').show();
    $('#nextyear').show();
  });
  $('#radioConsolidated').click(function () {
    $('.textboxgroup').hide();
    $('.textboxcompany').hide();
    $('.textboxdivision').hide();
    $('.textboxbranch').hide();
    $('.textboxbusiness').hide();
    $('#previousyear').hide();
    $('#nextyear').hide();
    loadConsolidated();
  });
  $('#radio6').click(function () {
    if ($('.textboxdate').is(':hidden')) {
      $('.textboxdate').show();
      $('#radio6').prop('checked', true);
    } else {
      $('.textboxdate').hide();
      $('#radio6').prop('checked', false);
    }
  });
  $('#domainradio').click(function () {
    if ($('.textboxdomain').is(':hidden')) {
      $('.textboxdomain').show();
      $('#domainradio').prop('checked', true);
    } else {
      $('.textboxdomain').hide();
      $('#domainradio').prop('checked', false);
    }
  });
  $('#countryradio').click(function () {
    if ($('.textboxcountry').is(':hidden')) {
      $('.textboxcountry').show();
      $('#countryradio').prop('checked', true);
    } else {
      $('.textboxcountry').hide();
      $('#countryradio').prop('checked', false);
    }
  });
  $('#viewaspie').hide();
  $('#previous').click(function () {
    if ($('#radio1').is(':checked')) {
    } else if ($('#radio2').is(':checked')) {
      loadCompany();
    } else if ($('#radio3').is(':checked')) {
      loadDivision();
    } else if ($('#radio4').is(':checked')) {
      loadUnit();
    }
  });
  $('#next').click(function () {
    if ($('#radio1').is(':checked')) {
    } else if ($('#radio2').is(':checked')) {
      loadCompanyNext();
    } else if ($('#radio3').is(':checked')) {
      loadDivisionNext();
    } else if ($('#radio4').is(':checked')) {
      loadUnitNext();
    }
  });
  $('#previousyear').click(function () {
    if ($('#radio1').is(':checked')) {
      loadGroup();
    } else if ($('#radio2').is(':checked')) {
      loadCompany();
    } else if ($('#radio3').is(':checked')) {
      loadDivision();
    } else if ($('#radio4').is(':checked')) {
      loadUnit();
    } else if ($('#radio5').is(':checked')) {
      loadBusinessGroup();
    }
  });
  $('#nextyear').click(function () {
    if ($('#radio1').is(':checked')) {
      loadGroup();
    } else if ($('#radio2').is(':checked')) {
      loadCompany();
    } else if ($('#radio3').is(':checked')) {
      loadDivision();
    } else if ($('#radio4').is(':checked')) {
      loadUnit();
    } else if ($('#radio5').is(':checked')) {
      loadBusinessGroup();
    }
  });
  $('#viewaspie').click(function () {
    if ($('#radio1').is(':checked')) {
      loadCountrySpecific();
    } else if ($('#radio2').is(':checked')) {
      loadCompanySingleSelectionPie();
    } else if ($('#radio3').is(':checked')) {
      loadCompanySingleSelectionPie();
    } else if ($('#radio4').is(':checked')) {
      loadCompanySingleSelectionPie();
    }
  });
  $('#viewasbar').click(function () {
    if ($('#radio1').is(':checked')) {
      loadCountrySpecificBar();
    } else if ($('#radio2').is(':checked')) {
      loadCompanySingleSelection($('#hidden').val());
    } else if ($('#radio3').is(':checked')) {
      loadCompanySingleSelection($('#hidden').val());
    } else if ($('#radio4').is(':checked')) {
      loadCompanySingleSelection($('#hidden').val());
    }
  });
  $('#back').click(function () {
    $('#next').show();
    $('#previous').show();
    if ($('#radio1').is(':checked')) {
      var value = $('#hidden').val();
      if (value == 'singlepie') {
        loadCountrySpecific();
      } else if (value == 'singlebar') {
        loadCountrySpecificBar();
      } else {
        loadGroup();
      }
    } else if ($('#radio2').is(':checked')) {
      loadCompany();
    } else if ($('#radio3').is(':checked')) {
      loadDivision();
    } else if ($('#radio4').is(':checked')) {
      loadUnit();
    } else {
      loadConsolidated();
    }
  });
  $('#go-le').click(function () {
    if ($('.compliance-status-tab').hasClass('active')) {
      loadCompany();
    } else if ($('.not-complied-tab').hasClass('active')) {
      ageingwiseCompliance();
    } else if ($('.applicability-status-tab').hasClass('active')) {
      loadPieChart();
    } else if ($('.escalations-tab').hasClass('active')) {
      loadEscalations();
    } else if ($('.compliance-report-tab').hasClass('active')) {
    } else if ($('.trend-chart-tab').hasClass('active')) {
      loadTrendChart();
    }
  });
  $('#go-bu').click(function () {
    if ($('.compliance-status-tab').hasClass('active')) {
      loadBusinessGroup();
    } else if ($('.not-complied-tab').hasClass('active')) {
      ageingwiseCompliance();
    } else if ($('.applicability-status-tab').hasClass('active')) {
      loadPieChart();
    } else if ($('.escalations-tab').hasClass('active')) {
      loadEscalations();
    } else if ($('.compliance-report-tab').hasClass('active')) {
    } else if ($('.trend-chart-tab').hasClass('active')) {
      loadTrendChart();
    }
  });
  $('#go-d').click(function () {
    if ($('.compliance-status-tab').hasClass('active')) {
      loadDivision();
    } else if ($('.not-complied-tab').hasClass('active')) {
      ageingwiseCompliance();
    } else if ($('.applicability-status-tab').hasClass('active')) {
      loadPieChart();
    } else if ($('.escalations-tab').hasClass('active')) {
      loadEscalations();
    } else if ($('.compliance-report-tab').hasClass('active')) {
    } else if ($('.trend-chart-tab').hasClass('active')) {
      loadTrendChart();
    }
  });
  $('#go-u').click(function () {
    if ($('.compliance-status-tab').hasClass('active')) {
      loadUnit();
    } else if ($('.not-complied-tab').hasClass('active')) {
      ageingwiseCompliance();
    } else if ($('.applicability-status-tab').hasClass('active')) {
      loadPieChart();
    } else if ($('.escalations-tab').hasClass('active')) {
      loadEscalations();
    } else if ($('.compliance-report-tab').hasClass('active')) {
    } else if ($('.trend-chart-tab').hasClass('active')) {
      loadTrendChart();
    }
  });
  $('#go-date').click(function () {
    if ($('#radio1').is(':checked')) {
      loadGroup();
    } else if ($('#radio2').is(':checked')) {
      loadCompany();
    } else if ($('#radio3').is(':checked')) {
      loadDivision();
    } else if ($('#radio4').is(':checked')) {
      loadUnit();
    } else if ($('#radio5').is(':checked')) {
      loadBusinessGroup();
    } else {
      loadConsolidated();
    }
  });
  $('#go-co').click(function () {
    var values = $('.country-filter').val();
    if ($('.compliance-status-tab').hasClass('active')) {
      if ($('#radio1').is(':checked')) {
        var value = $('#hidden').val();
        if (value == 'singlepie') {
          loadCountrySpecific();
        } else if (value == 'singlebar') {
          loadCountrySpecificBar();
        } else {
          loadGroup();
        }
        if (values.length == 1) {
          loadCompanySingleSelection(values[0]);
        } else {
          loadGroup();
        }
      } else if ($('#radio2').is(':checked')) {
        loadCompany();
      } else if ($('#radio3').is(':checked')) {
        loadDivision();
      } else if ($('#radio4').is(':checked')) {
        loadUnit();
      } else if ($('#radio5').is(':checked')) {
        loadBusinessGroup();
      } else {
        loadConsolidated();
      }
    } else if ($('.not-complied-tab').hasClass('active')) {
      ageingwiseCompliance();
    } else if ($('.applicability-status-tab').hasClass('active')) {
      loadPieChart();
    } else if ($('.escalations-tab').hasClass('active')) {
      loadEscalations();
    } else if ($('.compliance-report-tab').hasClass('active')) {
    } else if ($('.trend-chart-tab').hasClass('active')) {
      loadTrendChart();
    }
  });
  $('#go-do').click(function () {
    var values = $('#domain').val();
    if ($('.compliance-status-tab').hasClass('active')) {
      if ($('#radio1').is(':checked')) {
        var value = $('#hidden').val();
        if (value == 'singlepie') {
          loadCountrySpecific();
        } else if (value == 'singlebar') {
          loadCountrySpecificBar();
        } else {
          loadGroup();
        }
        if (values.length == 1) {
          loadCompanySingleSelection(values[0]);
        } else {
          loadGroup();
        }
      } else if ($('#radio2').is(':checked')) {
        loadCompany();
      } else if ($('#radio3').is(':checked')) {
        loadDivision();
      } else if ($('#radio4').is(':checked')) {
        loadUnit();
      } else if ($('#radio5').is(':checked')) {
        loadBusinessGroup();
      } else {
        loadConsolidated();
      }
    } else if ($('.not-complied-tab').hasClass('active')) {
      ageingwiseCompliance();
    } else if ($('.applicability-status-tab').hasClass('active')) {
      loadPieChart();
    } else if ($('.escalations-tab').hasClass('active')) {
      loadEscalations();
    } else if ($('.compliance-report-tab').hasClass('active')) {
    } else if ($('.trend-chart-tab').hasClass('active')) {
      loadTrendChart();
    }
  });
  $('.compliance-status-tab').click(function () {
    $('#year-para').hide();
    $('.compliance-status-tab').addClass('active');
    $('.not-complied-tab').removeClass('active');
    $('.applicability-status-tab').removeClass('active');
    $('.escalations-tab').removeClass('active');
    $('.compliance-report-tab').removeClass('active');
    $('.trend-chart-tab').removeClass('active');
    $('.graph-box').show();
    $('#graph-1').show();
    $('#graph-2').hide();
    $('#graph-3').hide();
    $('#graph-4').hide();
    $('#graph-5').hide();
    $('#assignee').hide();
    $('#assignee-wise-compliance').hide();
    $('.grid-table-dash').hide();
    $('.grid-table-dash1').hide();
    $('#viewaspie').hide();
    $('#unit-auto').hide();
    $('#bg-auto').hide();
    $('#entity-auto').hide();
    $('#division-auto').hide();
    $('.SumoSelect').show();
    $('#business-para1').show();
    $('#entity-para1').show();
    $('#division-para1').show();
    $('#next').show();
    $('#previous').show();
    $('td#DateSelection').show();
    $('td#consolidate').show();
    $('#level-filter1').show();
    loadGroup();
  });
  $('.escalations-tab').click(function () {
    $('#year-para').hide();
    $('.escalations-tab').addClass('active');
    $('.not-complied-tab').removeClass('active');
    $('.applicability-status-tab').removeClass('active');
    $('.compliance-status-tab').removeClass('active');
    $('.trend-chart-tab').removeClass('active');
    $('.compliance-report-tab').removeClass('active');
    $('#graph-1').hide();
    $('#graph-2').show();
    $('#graph-3').hide();
    $('#graph-4').hide();
    $('#graph-5').hide();
    $('#assignee').hide();
    $('#assignee-wise-compliance').hide();
    $('.grid-table-dash').hide();
    $('.grid-table-dash1').hide();
    $('#viewaspie').hide();
    $('#unit-auto').show();
    $('#entity-auto').show();
    $('#division-auto').show();
    $('#business-para1').hide();
    $('#entity-para1').hide();
    $('#division-para1').hide();
    $('#unit-para1').hide();
    $('#bg-auto').show();
    $('td#DateSelection').hide();
    $('td#consolidate').hide();
    $('#level-filter1').show();
    loadEscalations();
  });
  $('.not-complied-tab').click(function () {
    $('#year-para').hide();
    $('.escalations-tab').removeClass('active');
    $('.not-complied-tab').addClass('active');
    $('.applicability-status-tab').removeClass('active');
    $('.compliance-status-tab').removeClass('active');
    $('.trend-chart-tab').removeClass('active');
    $('.compliance-report-tab').removeClass('active');
    $('#graph-1').hide();
    $('#graph-2').hide();
    $('#graph-3').show();
    $('#graph-4').hide();
    $('#graph-5').hide();
    $('#assignee').hide();
    $('#assignee-wise-compliance').hide();
    $('.grid-table-dash').hide();
    $('.grid-table-dash1').hide();
    $('#viewaspie').hide();
    $('#unit-auto').show();
    $('#entity-auto').show();
    $('#bg-auto').show();
    $('#business-para1').hide();
    $('#entity-para1').hide();
    $('#division-para1').hide();
    $('#unit-para1').hide();
    $('#division-auto').show();
    $('td#DateSelection').hide();
    $('td#consolidate').hide();
    $('#level-filter1').show();
    ageingwiseCompliance();
  });
  $('.trend-chart-tab').click(function () {
    $('.trend-chart-tab').addClass('active');
    $('.applicability-status-tab').removeClass('active');
    $('.not-complied-tab').removeClass('active');
    $('.escalations-tab').removeClass('active');
    $('.compliance-status-tab').removeClass('active');
    $('.compliance-report-tab').removeClass('active');
    $('#graph-1').hide();
    $('#graph-2').hide();
    $('#graph-3').hide();
    $('#graph-4').show();
    $('#graph-5').hide();
    $('#assignee-wise-compliance').hide();
    $('#assignee').hide();
    $('.grid-table-dash').hide();
    $('.grid-table-dash1').hide();
    $('#viewaspie').hide();
    $('#viewasbar').hide();
    $('#back').hide();
    $('#unit-auto').show();
    $('#entity-auto').show();
    $('#bg-auto').show();
    $('#business-para1').hide();
    $('#entity-para1').hide();
    $('#division-para1').hide();
    $('#unit-para1').hide();
    $('#division-auto').show();
    $('#legal-entity').hide();
    $('#division').hide();
    $('#unit').hide();
    $('#year-para').show();
    $('td#DateSelection').hide();
    $('td#consolidate').hide();
    $('#level-filter1').show();
    loadTrendChart('KG Groups');
  });
  $('.applicability-status-tab').click(function () {
    $('#year-para').hide();
    $('.applicability-status-tab').addClass('active');
    $('.not-complied-tab').removeClass('active');
    $('.escalations-tab').removeClass('active');
    $('.trend-chart-tab').removeClass('active');
    $('.compliance-report-tab').removeClass('active');
    $('.compliance-status-tab').removeClass('active');
    $('#graph-1').hide();
    $('#graph-2').hide();
    $('#graph-3').hide();
    $('#graph-4').hide();
    $('#graph-5').show();
    $('#assignee-wise-compliance').hide();
    $('#assignee').hide();
    $('.grid-table-dash').hide();
    $('.grid-table-dash1').hide();
    $('#viewaspie').fadeIn();
    $('#unit-auto').show();
    $('#entity-auto').show();
    $('#bg-auto').show();
    $('#division').hide();
    $('#business-para1').hide();
    $('#entity-para1').hide();
    $('#division-para1').hide();
    $('#unit-para1').hide();
    $('#unit').hide();
    $('td#DateSelection').hide();
    $('td#consolidate').hide();
    $('#level-filter1').show();
    loadPieChart();
  });
  $();
  $('.usecom1-tab').click(function () {
    $('#year-para').hide();
    $('.compliance-report-tab').addClass('active');
    $('.not-complied-tab').removeClass('active');
    $('.applicability-status-tab').removeClass('active');
    $('.trend-chart-tab').removeClass('active');
    $('.compliance-status-tab').removeClass('active');
    $('.escalations-tab').removeClass('active');
    $('#level-filter1').hide();
    $('.grid-table-dash').hide();
    $('.grid-table-dash1').show();
    $('#viewaspie').hide();
    $('#graph-1').hide();
    $('#graph-2').hide();
    $('#graph-3').hide();
    $('#graph-4').hide();
    $('#graph-5').hide();
    $('#assignee').show();
  });
  $('.compliance-report-tab').click(function () {
    alert('usercom-tb clicked');
    $('#year-para').hide();
    $('.compliance-status-tab').removeClass('active');
    $('.compliance-report-tab').addClass('active');
    $('.not-complied-tab').removeClass('active');
    $('.applicability-status-tab').removeClass('active');
    $('.trend-chart-tab').removeClass('active');
    $('.escalations-tab').removeClass('active');
    $('#level-filter1').hide();
    $('.archive-tab-content').show();
    $('.grid-table-dash').show();
    $('.grid-table-dash1').hide();
    $('#viewaspie').hide();
    $('#graph-1').hide();
    $('#graph-2').hide();
    $('#graph-3').hide();
    $('#graph-4').hide();
    $('#graph-5').hide();
    $('#assignee-wise-compliance').show();
    $('#previousyear').hide();
    $('#nextyear').hide();
    $('#assignee').show();
  });
  $('#history').click(function () {
    $('#dialog-box').toggle();
  });
  $('#history-close').click(function () {
    $('#dialog-box').toggle();
  });
  $('.toggleModal').on('click', function (e) {
    $('.modal').toggleClass('active');
    $('.modal1').toggleClass('active');
  });
  $('.toggleModal1').on('click', function (e) {
    $('.modal1').toggleClass('active');
  });
  $('.dropdown-box-container').click(function () {
    $('.filter-dropdown-container').slideToggle();
  });
  $('#graph-1').show();
  $('#graph-2').hide();
  $('#graph-3').hide();
  $('#graph-4').hide();
  $('#graph-5').hide();
  loadGroup();
});
function loadCompanySingleSelectionPie() {
  $('#viewaspie').hide();
  $('#viewasbar').show();
  $('#graph-1').show();
  $('#imgcontainer').hide();
  var name = $('#hidden').val();
  $(function () {
    $('#graph-1').highcharts({
      colors: [
        '#A5D17A',
        '#F58835',
        '#F0F468',
        '#F32D2B'
      ],
      chart: {
        type: 'pie',
        options3d: {
          enabled: true,
          alpha: 45,
          beta: 0
        }
      },
      title: { text: name },
      tooltip: { pointFormat: '{series.name}: <b>{point.y}</b> <br>Total Compliances: 70' },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          depth: 35,
          dataLabels: {
            enabled: true,
            format: '{point.percentage:.0f}%'
          },
          showInLegend: true,
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                $('#hidden').val('singlepie');
                if (drilldown) {
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        }
      },
      series: [{
          type: 'pie',
          name: 'Compliance',
          data: [
            {
              name: 'Complied',
              y: 15,
              drilldown: 'Complied'
            },
            {
              name: 'Delayed compliance',
              y: 15,
              drilldown: 'Delayed'
            },
            {
              name: 'In progress',
              y: 18,
              drilldown: 'Inprogress'
            },
            {
              name: 'Not complied',
              y: 22,
              drilldown: 'NotComplied'
            }
          ]
        }]
    });
  });
}
function loadCompanySingleSelection(name) {
  $(function () {
    $('#viewaspie').show();
    $('#viewasbar').hide();
    $('#hidden').val(name);
    $('#graph-1').show();
    $('#imgcontainer').hide();
    $('#graph-1').highcharts({
      colors: [
        '#A5D17A',
        '#F58835',
        '#F0F468',
        '#F32D2B'
      ],
      chart: { type: 'column' },
      title: { text: name },
      xAxis: {
        type: 'category',
        title: { text: 'Compliance Status' }
      },
      yAxis: {
        title: { text: 'Total Compliances' },
        allowDecimals: false
      },
      legend: { enabled: false },
      plotOptions: {
        column: {
          dataLabels: {
            enabled: true,
            style: { textShadow: null },
            format: '{point.y}'
          },
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                $('#hidden').val('singlebar');
                if (drilldown) {
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        },
        series: {
          borderWidth: 0,
          dataLabels: {
            enabled: true,
            formatter: function () {
              var dataSum = 5 + 2 + 8 + 3;
              var pcnt = this.y / dataSum * 100;
              return Highcharts.numberFormat(pcnt, 0) + '%';
            }
          }
        }
      },
      tooltip: {
        headerFormat: '<b>{series.name}</b>:{point.percentage:.0f}%<br/>',
        pointFormat: 'Total Compliances: 18'
      },
      series: [{
          name: 'Compliance - Group wise',
          colorByPoint: true,
          data: [
            {
              name: 'Complied',
              y: 5,
              drilldown: 'Complied'
            },
            {
              name: 'Delayed compliance',
              y: 2,
              drilldown: 'Delayed'
            },
            {
              name: 'In progress',
              y: 8,
              drilldown: 'Inprogress'
            },
            {
              name: 'Not complied',
              y: 3,
              drilldown: 'NotComplied'
            }
          ]
        }]
    });
  });
}
function loadCompanyNext() {
  $('#previous').show();
  $('#next').show();
  $('#graph-1').show();
  $('#imgcontainer').hide();
  $(function () {
    var inprogress_data = [10];
    var pending_data = [10];
    var completed_data = [10];
    var not_complied = [10];
    inprogress_data[0] = {
      name: 'KG Hospitals',
      y: 20,
      drilldown: 'Inprogress'
    };
    pending_data[0] = {
      name: 'KG Hospitals',
      y: 20,
      drilldown: 'Delayed'
    };
    completed_data[0] = {
      id: 'fin',
      name: 'KG Hospitals',
      y: 10,
      drilldown: 'Complied'
    };
    not_complied[0] = {
      name: 'KG Hospitals',
      y: 30,
      drilldown: 'NotComplied'
    };
    inprogress_data[1] = {
      name: 'KG Bakeries',
      y: 12
    };
    pending_data[1] = {
      name: 'KG Bakeries',
      y: 18
    };
    completed_data[1] = {
      id: 'fin',
      name: 'KG Bakeries',
      y: 27
    };
    not_complied[1] = {
      name: 'KG Bakeries',
      y: 13
    };
    inprogress_data[2] = {
      name: 'KG Hotels',
      y: 15
    };
    pending_data[2] = {
      name: 'KG Hotels',
      y: 25
    };
    completed_data[2] = {
      id: 'fin',
      name: 'KG Hotels',
      y: 10
    };
    not_complied[2] = {
      name: 'KG Hotels',
      y: 10
    };
    inprogress_data[3] = {
      name: 'KG Schools',
      y: 10
    };
    pending_data[3] = {
      name: 'KG Schools',
      y: 24
    };
    completed_data[3] = {
      id: 'fin',
      name: 'KG Schools',
      y: 24
    };
    not_complied[3] = {
      name: 'KG Schools',
      y: 17
    };
    inprogress_data[4] = {
      name: 'KG University',
      y: 24
    };
    pending_data[4] = {
      name: 'KG University',
      y: 23
    };
    completed_data[4] = {
      id: 'fin',
      name: 'KG University',
      y: 31
    };
    not_complied[4] = {
      name: 'KG Mobiles',
      y: 13
    };
    $('#graph-1').highcharts({
      colors: [
        '#A5D17A',
        '#F58835',
        '#F0F468',
        '#F32D2B'
      ],
      chart: {
        type: 'bar',
        width: '850'
      },
      title: { text: 'Legal entity wise compliances' },
      xAxis: {
        categories: [
          'KG Hospitals',
          'KG Bakeries',
          'KG Hotels',
          'KG Schools',
          'KG University'
        ],
        title: { text: 'Legal entities' },
        labels: {
          useHTML: true,
          formatter: function () {
            var name = this.value;
            if (name == 'KG Autoparts') {
              $('#hidden').val('KG Autoparts');
              var link = '<a href="#"  id="' + name + '" onclick=loadCompanySingleSelectionPie(this.id)>' + name + '</a>';
              return link;
            } else {
              var link = '<span  id="' + name + '" >' + name + '</span>';
              return link;
            }
          }
        }
      },
      yAxis: {
        min: 0,
        title: { text: 'Total Compliances' },
        allowDecimals: false
      },
      legend: { reversed: true },
      tooltip: {
        headerFormat: '<b>{point.x}</b><br/>',
        pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
      },
      plotOptions: {
        series: {
          stacking: 'normal',
          dataLabels: {
            enabled: true,
            color: '#000000',
            style: { textShadow: null },
            format: '{point.y}'
          },
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                if (drilldown) {
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        }
      },
      series: [
        {
          name: 'Complied',
          data: completed_data
        },
        {
          name: 'Delayed compliance',
          data: pending_data
        },
        {
          name: 'In progress',
          data: inprogress_data
        },
        {
          name: 'Not complied',
          data: not_complied
        }
      ]
    });
  });
}
function loadCompany() {
  $('#previous').show();
  $('#next').show();
  $('#graph-1').show();
  $('#imgcontainer').hide();
  $(function () {
    var inprogress_data = [10];
    var pending_data = [10];
    var completed_data = [10];
    var not_complied = [10];
    var values = $('#legal-entity').val();
    if (values.length > 1) {
      for (var i = 0; i < 7; i++) {
        if (values[i] == 'KG Transports') {
          inprogress_data[i] = {
            name: 'KG Transports',
            y: 24,
            drilldown: 'EntityInprogress'
          };
          pending_data[i] = {
            name: 'KG Transports',
            y: 13,
            drilldown: 'EntityDelayed'
          };
          completed_data[i] = {
            id: 'fin',
            name: 'KG Transports',
            y: 18,
            drilldown: 'EntityComplied'
          };
          not_complied[i] = {
            name: 'KG Transports',
            y: 22,
            drilldown: 'NotComplied'
          };
        } else if (values[i] == 'KG Autoparts') {
          inprogress_data[i] = {
            name: 'KG Autoparts',
            y: 15
          };
          pending_data[i] = {
            name: 'KG Autoparts',
            y: 23
          };
          completed_data[i] = {
            id: 'fin',
            name: 'KG Autoparts',
            y: 12
          };
          not_complied[i] = {
            name: 'KG Autoparts',
            y: 18
          };
        } else if (values[i] == 'KG Booking') {
          inprogress_data[i] = {
            name: 'KG Booking',
            y: 23
          };
          pending_data[i] = {
            name: 'KG Booking',
            y: 22
          };
          completed_data[i] = {
            id: 'fin',
            name: 'KG Booking',
            y: 19
          };
          not_complied[i] = {
            name: 'KG Booking',
            y: 21
          };
        } else if (values[i] == 'KG Electricals') {
          inprogress_data[i] = {
            name: 'KG Electricals',
            y: 23
          };
          pending_data[i] = {
            name: 'KG Electricals',
            y: 10
          };
          completed_data[i] = {
            id: 'fin',
            name: 'KG Electricals',
            y: 18
          };
          not_complied[i] = {
            name: 'KG Electricals',
            y: 22
          };
        } else if (values[i] == 'KG Mobiles') {
          inprogress_data[i] = {
            name: 'KG Mobiles',
            y: 24
          };
          pending_data[i] = {
            name: 'KG Mobiles',
            y: 24
          };
          completed_data[i] = {
            id: 'fin',
            name: 'KG Mobiles',
            y: 13
          };
          not_complied[i] = {
            name: 'KG Mobiles',
            y: 21
          };
        } else if (values[i] == 'KG HealthCare') {
          inprogress_data[i] = {
            name: 'KG HealthCare',
            y: 20
          };
          pending_data[i] = {
            name: 'KG HealthCare',
            y: 25
          };
          completed_data[i] = {
            id: 'fin',
            name: 'KG HealthCare',
            y: 22
          };
          not_complied[i] = {
            name: 'KG HealthCare',
            y: 18
          };
        } else if (values[i] == 'KG HR Services') {
          inprogress_data[i] = {
            name: 'KG HR Services',
            y: 22
          };
          pending_data[i] = {
            name: 'KG HR Services',
            y: 18
          };
          completed_data[i] = {
            id: 'fin',
            name: 'KG HR Services',
            y: 22
          };
          not_complied[i] = {
            name: 'KG HR Services',
            y: 23
          };
        } else {
          continue;
        }
      }
    } else if (values.length <= 0) {
      alert('Select atleast one legal entity to load chart');
    } else {
      loadCompanySingleSelection(values[0]);
    }
    $('#graph-1').highcharts({
      colors: [
        '#F32D2B',
        '#F0F468',
        '#F58835',
        '#A5D17A'
      ],
      chart: {
        type: 'bar',
        width: '850'
      },
      title: { text: 'Legal entity wise compliances' },
      xAxis: {
        categories: [
          'KG Transports',
          'KG Autoparts',
          'KG Booking',
          'KG Electricals',
          'KG Mobiles',
          'KG HR Services',
          'KG HealthCare'
        ],
        endOnTick: true,
        title: { text: 'Legal entities' },
        labels: {
          useHTML: true,
          formatter: function () {
            var name = this.value;
            if (name == 'KG Booking') {
              $('#hidden').val('KG Booking');
              var link = '<a href="#"  id="' + name + '" onclick=loadCompanySingleSelectionPie(this.id)>' + name + '</a>';
              return link;
            } else {
              var link = '<span  id="' + name + '" >' + name + '</span>';
              return link;
            }
          }
        }
      },
      yAxis: {
        min: 0,
        title: { text: 'Total Compliances' },
        allowDecimals: false,
        endOnTick: true
      },
      legend: { reversed: true },
      tooltip: {
        headerFormat: '<b>{point.x}</b><br/>',
        pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
      },
      plotOptions: {
        series: {
          stacking: 'normal',
          dataLabels: {
            enabled: true,
            color: '#000000',
            style: { textShadow: null },
            format: '{point.y}'
          },
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                if (drilldown) {
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        }
      },
      series: [
        {
          name: 'Not complied',
          data: not_complied
        },
        {
          name: 'In progress',
          data: inprogress_data
        },
        {
          name: 'Delayed compliance',
          data: pending_data
        },
        {
          name: 'Complied',
          data: completed_data
        }
      ]
    });
  });
}
function loadDivisionNext() {
  $('#previous').show();
  $('#next').show();
  $('#graph-1').show();
  $('#imgcontainer').hide();
  $(function () {
    var inprogress_data = [10];
    var pending_data = [10];
    var completed_data = [10];
    var not_complied = [10];
    inprogress_data[0] = {
      name: 'KG HR Unit',
      y: 30,
      drilldown: 'Inprogress'
    };
    pending_data[0] = {
      name: 'KG HR Unit',
      y: 20,
      drilldown: 'Delayed'
    };
    completed_data[0] = {
      id: 'fin',
      name: 'KG HR Unit',
      y: 10,
      drilldown: 'Complied'
    };
    not_complied[0] = {
      name: 'KG HR Unit',
      y: 20,
      drilldown: 'NotComplied'
    };
    inprogress_data[1] = {
      name: 'KG Development',
      y: 21
    };
    pending_data[1] = {
      name: 'KG Development',
      y: 29
    };
    completed_data[1] = {
      id: 'fin',
      name: 'KG Development',
      y: 16
    };
    not_complied[1] = {
      name: 'KG Development',
      y: 28
    };
    $('#graph-1').highcharts({
      colors: [
        '#F32D2B',
        '#F0F468',
        '#F58835',
        '#A5D17A'
      ],
      chart: {
        type: 'bar',
        width: '850'
      },
      title: { text: 'Division wise compliances' },
      xAxis: {
        categories: [
          'KG HR Unit',
          'KG Development'
        ],
        title: { text: 'Division' },
        labels: {
          useHTML: true,
          formatter: function () {
            var name = this.value;
            if (name == 'KG Security') {
              $('#hidden').val('KG Security');
              var link = '<a href="#"  id="' + name + '" onclick=loadCompanySingleSelectionPie(this.id)>' + name + '</a>';
              return link;
            } else {
              var link = '<span  id="' + name + '" >' + name + '</span>';
              return link;
            }
          }
        }
      },
      yAxis: {
        min: 0,
        title: { text: 'Total Compliances' },
        allowDecimals: false
      },
      legend: { reversed: true },
      tooltip: {
        headerFormat: '<b>{point.name}</b><br/>',
        pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
      },
      plotOptions: {
        series: {
          stacking: 'normal',
          dataLabels: {
            enabled: true,
            color: '#000000',
            style: { textShadow: null },
            format: '{point.y}'
          },
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                if (drilldown) {
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        }
      },
      series: [
        {
          name: 'Complied',
          data: completed_data
        },
        {
          name: 'Delayed compliance',
          data: pending_data
        },
        {
          name: 'In progress',
          data: inprogress_data
        },
        {
          name: 'Not complied',
          data: not_complied
        }
      ]
    });
  });
}
function loadDivision() {
  $('#previous').show();
  $('#next').show();
  $('#graph-1').show();
  $('#imgcontainer').hide();
  $(function () {
    var inprogress_data = [10];
    var pending_data = [10];
    var completed_data = [10];
    var not_complied = [10];
    var values = $('#division').val();
    if (values.length > 1) {
      for (var i = 0; i < values.length; i++) {
        if (values[i] == 'KG Manufacturing') {
          inprogress_data[i] = {
            name: 'KG Manufacturing',
            y: 24,
            drilldown: 'Inprogress'
          };
          pending_data[i] = {
            name: 'KG Manufacturing',
            y: 22,
            drilldown: 'DivisionDelayed'
          };
          completed_data[i] = {
            id: 'fin',
            name: 'KG Manufacturing',
            y: 25,
            drilldown: 'DivisionComplied'
          };
          not_complied[i] = {
            name: 'KG Manufacturing',
            y: 23,
            drilldown: 'NotComplied'
          };
        } else if (values[i] == 'KG Quality Checking') {
          inprogress_data[i] = {
            name: 'KG Quality Checking',
            y: 18
          };
          pending_data[i] = {
            name: 'KG Quality Checking',
            y: 15
          };
          completed_data[i] = {
            id: 'fin',
            name: 'KG Quality Checking',
            y: 23
          };
          not_complied[i] = {
            name: 'KG Quality Checking',
            y: 24
          };
        } else if (values[i] == 'KG Sales') {
          inprogress_data[i] = {
            name: 'KG Sales',
            y: 25
          };
          pending_data[i] = {
            name: 'KG Sales',
            y: 13
          };
          completed_data[i] = {
            id: 'fin',
            name: 'KG Sales',
            y: 26
          };
          not_complied[i] = {
            name: 'KG Sales',
            y: 14
          };
        } else if (values[i] == 'KG Testing') {
          inprogress_data[i] = {
            name: 'KG Testing',
            y: 15
          };
          pending_data[i] = {
            name: 'KG Testing',
            y: 12
          };
          completed_data[i] = {
            id: 'fin',
            name: 'KG Testing',
            y: 23
          };
          not_complied[i] = {
            name: 'KG Testing',
            y: 24
          };
        } else if (values[i] == 'KG Administration') {
          inprogress_data[i] = {
            name: 'KG Administration',
            y: 22
          };
          pending_data[i] = {
            name: 'KG Administration',
            y: 36
          };
          completed_data[i] = {
            id: 'fin',
            name: 'KG Administration',
            y: 13
          };
          not_complied[i] = {
            name: 'KG Administration',
            y: 14
          };
        } else if (values[i] == 'KG Security') {
          inprogress_data[i] = {
            name: 'KG Security',
            y: 22
          };
          pending_data[i] = {
            name: 'KG Security',
            y: 26
          };
          completed_data[i] = {
            id: 'fin',
            name: 'KG Security',
            y: 23
          };
          not_complied[i] = {
            name: 'KG Security',
            y: 14
          };
        } else if (values[i] == 'KG Research') {
          inprogress_data[i] = {
            name: 'KG Research',
            y: 32
          };
          pending_data[i] = {
            name: 'KG Research',
            y: 16
          };
          completed_data[i] = {
            id: 'fin',
            name: 'KG Research',
            y: 13
          };
          not_complied[i] = {
            name: 'KG Research',
            y: 14
          };
        } else {
          continue;
        }
      }
    } else if (values.length <= 0) {
      alert('Select atleast one division to load chart');
    } else {
      loadCompanySingleSelection(values[0]);
    }
    $('#graph-1').highcharts({
      colors: [
        '#F32D2B',
        '#F0F468',
        '#F58835',
        '#A5D17A'
      ],
      chart: {
        type: 'bar',
        width: '850'
      },
      title: { text: 'Division wise compliances' },
      xAxis: {
        categories: [
          'KG Manufacturing',
          'KG Sales',
          'KG Quality Checking',
          'KG Administration',
          'KG Testing',
          'KG Security',
          'KG Research'
        ],
        title: { text: 'Divisions' },
        labels: {
          useHTML: true,
          formatter: function () {
            var name = this.value;
            if (name == 'KG Manufacturing') {
              $('#hidden').val('KG Manufacturing');
              var link = '<a href="#"  id="' + name + '" onclick=loadCompanySingleSelectionPie(this.id)>' + name + '</a>';
              return link;
            } else {
              var link = '<span  id="' + name + '" >' + name + '</span>';
              return link;
            }
          }
        }
      },
      yAxis: {
        min: 0,
        title: { text: 'Total Compliances' },
        allowDecimals: false
      },
      legend: { reversed: true },
      tooltip: {
        headerFormat: '<b>{point.x}</b><br/>',
        pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
      },
      plotOptions: {
        series: {
          stacking: 'normal',
          dataLabels: {
            enabled: true,
            color: '#000000',
            style: { textShadow: null },
            format: '{point.y}'
          },
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                if (drilldown) {
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        }
      },
      series: [
        {
          name: 'Not complied',
          data: not_complied
        },
        {
          name: 'In progress',
          data: inprogress_data
        },
        {
          name: 'Delayed compliance',
          data: pending_data
        },
        {
          name: 'Complied1',
          data: completed_data
        }
      ]
    });
  });
}
function loadUnit() {
  $('#previous').show();
  $('#next').show();
  $('#graph-1').show();
  $('#imgcontainer').hide();
  $(function () {
    var inprogress_data = [10];
    var pending_data = [10];
    var completed_data = [10];
    var not_complied = [10];
    var values = $('#unit').val();
    if (values.length > 1) {
      for (var i = 0; i < values.length; i++) {
        if (values[i] == 'Branch Office - 1') {
          inprogress_data[i] = {
            name: 'Branch Office - 1',
            y: 23,
            drilldown: 'UnitInprogress'
          };
          pending_data[i] = {
            name: 'Branch Office - 1',
            y: 22,
            drilldown: 'UnitDelayed'
          };
          completed_data[i] = {
            id: 'fin',
            name: 'Branch Office - 1',
            y: 19,
            drilldown: 'UnitComplied'
          };
          not_complied[i] = {
            name: 'Branch Office - 1',
            y: 31,
            drilldown: 'UnitNotComplied'
          };
        } else if (values[i] == 'Branch Office - 2') {
          inprogress_data[i] = {
            name: 'Branch Office - 2',
            y: 19
          };
          pending_data[i] = {
            name: 'Branch Office - 2',
            y: 27
          };
          completed_data[i] = {
            id: 'fin',
            name: 'Branch Office - 2',
            y: 28
          };
          not_complied[i] = {
            name: 'Branch Office - 2',
            y: 15
          };
        } else if (values[i] == 'Branch Office - 3') {
          inprogress_data[i] = {
            name: 'Branch Office - 3',
            y: 15
          };
          pending_data[i] = {
            name: 'Branch Office - 3',
            y: 23
          };
          completed_data[i] = {
            id: 'fin',
            name: 'Branch Office - 3',
            y: 16
          };
          not_complied[i] = {
            name: 'Branch Office - 3',
            y: 23
          };
        } else if (values[i] == 'Branch Office - 4') {
          inprogress_data[i] = {
            name: 'Branch Office - 4',
            y: 25
          };
          pending_data[i] = {
            name: 'Branch Office - 4',
            y: 32
          };
          completed_data[i] = {
            id: 'fin',
            name: 'Branch Office - 4',
            y: 13
          };
          not_complied[i] = {
            name: 'Branch Office - 4',
            y: 24
          };
        } else if (values[i] == 'Branch Office - 5') {
          inprogress_data[i] = {
            name: 'Branch Office - 5',
            y: 12
          };
          pending_data[i] = {
            name: 'Branch Office - 5',
            y: 26
          };
          completed_data[i] = {
            id: 'fin',
            name: 'Branch Office - 5',
            y: 33
          };
          not_complied[i] = {
            name: 'Branch Office - 5',
            y: 14
          };
        } else if (values[i] == 'Branch Office - 6') {
          inprogress_data[i] = {
            name: 'Branch Office - 6',
            y: 12
          };
          pending_data[i] = {
            name: 'Branch Office - 6',
            y: 26
          };
          completed_data[i] = {
            id: 'fin',
            name: 'Branch Office - 6',
            y: 13
          };
          not_complied[i] = {
            name: 'Branch Office - 6',
            y: 24
          };
        } else if (values[i] == 'Branch Office - 7') {
          inprogress_data[i] = {
            name: 'Branch Office - 7',
            y: 32
          };
          pending_data[i] = {
            name: 'Branch Office - 7',
            y: 16
          };
          completed_data[i] = {
            id: 'fin',
            name: 'Branch Office - 7',
            y: 23
          };
          not_complied[i] = {
            name: 'Branch Office - 7',
            y: 24
          };
        }
      }
    } else if (values.length <= 0) {
      alert('Select atleast one unit to load chart');
    } else {
      loadCompanySingleSelection(values[0]);
    }
    $('#graph-1').highcharts({
      colors: [
        '#F32D2B',
        '#F0F468',
        '#F58835',
        '#A5D17A'
      ],
      chart: {
        type: 'bar',
        width: '850'
      },
      title: { text: 'Unit wise compliances' },
      xAxis: {
        categories: [
          'Branch Office - 1',
          'Branch Office - 2',
          'Branch Office - 3',
          'Branch Office - 4',
          'Branch Office - 5',
          'Branch Office - 6',
          'Branch Office - 7'
        ],
        title: { text: 'Units' },
        labels: {
          useHTML: true,
          formatter: function () {
            var name = this.value;
            if (name == 'Branch Office - 1') {
              $('#hidden').val('Branch Office - 1');
              var link = '<a href="#"  id="' + name + '" onclick=loadCompanySingleSelectionPie(this.id)>' + name + '</a>';
              return link;
            } else {
              var link = '<span  id="' + name + '" >' + name + '</span>';
              return link;
            }
          }
        }
      },
      yAxis: {
        min: 0,
        title: { text: 'Total Compliances' },
        allowDecimals: false
      },
      legend: { reversed: true },
      tooltip: {
        headerFormat: '<b>{point.x}</b><br/>',
        pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
      },
      plotOptions: {
        series: {
          stacking: 'normal',
          dataLabels: {
            enabled: true,
            color: '#000000',
            style: { textShadow: null },
            format: '{point.y}'
          },
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                if (drilldown) {
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        }
      },
      series: [
        {
          name: 'Not complied',
          data: not_complied
        },
        {
          name: 'In progress',
          data: inprogress_data
        },
        {
          name: 'Delayed compliance',
          data: pending_data
        },
        {
          name: 'Complied',
          data: completed_data
        }
      ]
    });
  });
}
function loadBusinessGroup() {
  $('#viewaspie').hide();
  $('#back').hide();
  $('#viewasbar').hide();
  $('.SumoSelect').show();
  $('#entity-auto').hide();
  $('#division-auto').hide();
  $('#unit-auto').hide();
  $('#previous').hide();
  $('#next').hide();
  $('#graph-1').show();
  $('#imgcontainer').hide();
  $(function () {
    $('#graph-1').highcharts({
      colors: [
        '#F32D2B',
        '#F0F468',
        '#F58835',
        '#A5D17A'
      ],
      chart: {
        type: 'bar',
        width: '850'
      },
      title: { text: 'Business Group wise compliances' },
      xAxis: {
        title: { text: 'Business Groups' },
        categories: [
          'KG Business group 1',
          'KG Business group 2',
          'KG Business group 3',
          'KG Business group 4',
          'KG Business group 5'
        ],
        labels: {
          useHTML: true,
          formatter: function () {
            var name = this.value;
            if (name == 'India') {
              var link = '<a href="#"  id="' + name + '" onclick=loadCountrySpecific(this.id)>' + name + '</a>';
              return link;
            } else {
              var link = '<span  id="' + name + '" >' + name + '</span>';
              return link;
            }
          }
        }
      },
      yAxis: {
        min: 0,
        title: { text: 'Total Compliances' },
        allowDecimals: false
      },
      legend: { reversed: true },
      tooltip: {
        headerFormat: '<b>{point.x}</b><br/>',
        pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
      },
      plotOptions: {
        series: {
          stacking: 'normal',
          dataLabels: {
            enabled: true,
            color: '#000000',
            style: {
              textShadow: null,
              color: '#000000'
            },
            format: '{point.y}'
          },
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                if (drilldown) {
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        }
      },
      series: [
        {
          name: 'Not complied',
          data: [
            {
              y: 22,
              drilldown: 'busNotComplied'
            },
            { y: 15 },
            { y: 30 },
            { y: 10 },
            { y: 20 }
          ]
        },
        {
          name: 'In progress',
          data: [
            {
              y: 18,
              drilldown: 'busInprogress'
            },
            { y: 25 },
            { y: 10 },
            { y: 25 },
            { y: 30 }
          ]
        },
        {
          name: 'Delayed Compliance',
          data: [
            {
              y: 15,
              drilldown: 'busDelayed'
            },
            { y: 20 },
            { y: 20 },
            { y: 15 },
            { y: 10 }
          ]
        },
        {
          name: 'Complied',
          data: [
            {
              y: 15,
              drilldown: 'busComplied'
            },
            { y: 30 },
            { y: 20 },
            { y: 20 },
            { y: 30 }
          ]
        }
      ]
    });
  });
}
function loadUnitNext() {
  $('#previous').show();
  $('#next').show();
  $('#graph-1').show();
  $('#imgcontainer').hide();
  $(function () {
    var inprogress_data = [10];
    var pending_data = [10];
    var completed_data = [10];
    var not_complied = [10];
    inprogress_data[0] = {
      name: 'KG Namakal Unit',
      y: 20,
      drilldown: 'Inprogress'
    };
    pending_data[0] = {
      name: 'KG Namakal Unit',
      y: 16,
      drilldown: 'Delayed'
    };
    completed_data[0] = {
      id: 'fin',
      name: 'KG Namakal Unit',
      y: 25,
      drilldown: 'Complied'
    };
    not_complied[0] = {
      name: 'KG Namakal Unit',
      y: 23,
      drilldown: 'NotComplied'
    };
    inprogress_data[1] = {
      name: 'Suseendram, Kanyakumari',
      y: 18
    };
    pending_data[1] = {
      name: 'Suseendram, Kanyakumari',
      y: 22
    };
    completed_data[1] = {
      id: 'fin',
      name: 'Suseendram, Kanyakumari',
      y: 25
    };
    not_complied[1] = {
      name: 'Suseendram, Kanyakumari',
      y: 21
    };
    inprogress_data[2] = {
      name: 'Nagercoil, Kanyakumari',
      y: 15
    };
    pending_data[2] = {
      name: 'Nagercoil, Kanyakumari',
      y: 23
    };
    completed_data[2] = {
      id: 'fin',
      name: 'Nagercoil, Kanyakumari',
      y: 26
    };
    not_complied[2] = {
      name: 'Nagercoil, Kanyakumari',
      y: 18
    };
    inprogress_data[3] = {
      name: 'Naloor, Tuticorin',
      y: 15
    };
    pending_data[3] = {
      name: 'Naloor, Tuticorin',
      y: 22
    };
    completed_data[3] = {
      id: 'fin',
      name: 'Naloor, Tuticorin',
      y: 31
    };
    not_complied[3] = {
      name: 'Naloor, Tuticorin',
      y: 23
    };
    $('#graph-1').highcharts({
      colors: [
        '#F32D2B',
        '#F0F468',
        '#F58835',
        '#A5D17A'
      ],
      chart: {
        type: 'bar',
        width: '850'
      },
      title: { text: 'Unitwise compliances' },
      xAxis: {
        categories: [
          'KG Namakal unit',
          'Suseendram, Kanyakumari',
          'Nagercoil, Kanyakumari',
          'Naloor, Tuticorin'
        ],
        title: { text: 'Units' },
        labels: {
          useHTML: true,
          formatter: function () {
            var name = this.value;
            if (name == 'KG Autoparts') {
              $('#hidden').val('KG Autoparts');
              var link = '<a href="#"  id="' + name + '" onclick=loadCompanySingleSelectionPie(this.id)>' + name + '</a>';
              return link;
            } else {
              var link = '<span  id="' + name + '" >' + name + '</span>';
              return link;
            }
          }
        }
      },
      yAxis: {
        min: 0,
        title: { text: 'Total Compliances' },
        allowDecimals: false
      },
      legend: { reversed: true },
      tooltip: {
        headerFormat: '<b>{point.x}</b><br/>',
        pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
      },
      plotOptions: {
        series: {
          stacking: 'normal',
          dataLabels: {
            enabled: true,
            color: '#000000',
            style: { textShadow: null },
            format: '{point.y}'
          },
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                if (drilldown) {
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        }
      },
      series: [
        {
          name: 'Complied',
          data: completed_data
        },
        {
          name: 'Delayed compliance',
          data: pending_data
        },
        {
          name: 'In progress',
          data: inprogress_data
        },
        {
          name: 'Not complied',
          data: not_complied
        }
      ]
    });
  });
}
function loadDrillDownData(name) {
  $('#viewaspie').hide();
  $('#viewasbar').hide();
  $('#next').hide();
  $('#previous').hide();
  $('#nextyear').hide();
  $('#previousyear').hide();
  $('#back').show();
  $('#graph-1').hide();
  $('#imgcontainer').show();
  var img_name = '';
  var margin_style = '';
  if (name == 'EntityInprogress') {
    img_name = '/images/dash-list/task-entity-inprogress.png';
    name = 'KG Booking';
    com_name = 'In progress ';
  } else if (name == 'EntityComplied') {
    img_name = '/images/dash-list/task-entity-complied.png';
    name = 'KG Booking';
    com_name = 'Complied ';
    margin_style = 'margin-left:3px';
  } else if (name == 'EntityDelayed') {
    img_name = '/images/dash-list/task-entity-delayed.png';
    name = 'KG Booking';
    com_name = 'Delayed ';
    margin_style = 'margin-left:3px';
  } else if (name == 'Inprogress') {
    img_name = '/images/dash-list/task-group-inprogress.png';
    name = 'India';
    com_name = 'In progress ';
  } else if (name == 'Delayed') {
    img_name = '/images/dash-list/task-group-delayed.png';
    name = 'India';
    com_name = 'Delayed ';
  } else if (name == 'NotComplied') {
    img_name = '/images/dash-list/task-group-notcomplied.png';
    name = 'India';
    com_name = 'Not complied ';
  } else if (name == 'Complied') {
    img_name = '/images/dash-list/task-group-complied.png';
    name = 'India';
    com_name = 'Complied ';
  } else if (name == 'busInprogress') {
    img_name = '/images/dash-list/task-business-inprogress.png';
    name = 'Business Group 1';
    com_name = 'In progress ';
  } else if (name == 'busDelayed') {
    img_name = '/images/dash-list/task-business-delayed.png';
    name = 'Business Group 1';
    com_name = 'Delayed compliance';
  } else if (name == 'busNotComplied') {
    img_name = '/images/dash-list/task-business-notcomplied.png';
    name = 'Business Group 1 ';
    com_name = 'Not complied ';
  } else if (name == 'busComplied') {
    img_name = '/images/dash-list/task-business-complied.png';
    name = 'Business Group 1';
    com_name = 'Complied ';
  } else if (name == 'UnitComplied') {
    img_name = '/images/dash-list/task-unit-complied.png';
    name = 'Branch Office 1';
    com_name = 'Complied ';
  } else if (name == 'UnitDelayed') {
    img_name = '/images/dash-list/task-unit-delayed.png';
    name = 'Branch Office 1';
    com_name = 'Delayed';
  } else if (name == 'DivisionComplied') {
    img_name = '/images/dash-list/task-division-complied.png';
    name = 'KG Manufacturing';
    com_name = 'Complied ';
  } else if (name == 'DivisionDelayed') {
    img_name = '/images/dash-list/task-division-delayed.png';
    name = 'KG Manufacturing';
    com_name = 'Delayed';
  } else if (name == 'unitesc') {
    img_name = '/images/dash-list/escalations-unit-delayed.png';
    name = 'South gate, Madurai - escalations';
    margin_style = 'margin-left:200px';
  } else if (name == 'divisionesc') {
    img_name = '/images/dash-list/escalations-division-delayed.png';
    name = 'KG Manufacturing - escalations';
    margin_style = 'margin-left:100px';
  } else if (name == 'entityesc') {
    img_name = '/images/dash-list/escalations-entity-delayed.png';
    name = 'KG - escalations';
    margin_style = 'margin-left:55px';
  } else if (name == 'groupesc') {
    img_name = '/images/dash-list/escalations-group-delayed.png';
    name = 'KG Groups - escalations';
  } else if (name == 'unitcomp') {
    img_name = '/images/dash-list/complienceopportunity-unit-not.png';
    name = 'South gate, Madurai - Applicable compliance tasls';
    margin_style = 'margin-left:200px';
  } else if (name == 'divisioncomp') {
    img_name = '/images/dash-list/complienceopportunity-division-not.png';
    name = 'Manufacturing division - Applicable compliances';
    margin_style = 'margin-left:150px';
  } else if (name == 'entitycomp') {
    img_name = '/images/dash-list/complienceopportunity-entity-not.png';
    name = 'KG Entity- Applicable compliances';
    margin_style = 'margin-left:40px';
  } else if (name == 'groupcomp') {
    img_name = '/images/dash-list/complienceopportunity-group-not.png';
    name = 'KG Groups - Applicable compliances';
  } else if (name == 'Jan') {
    if ($('#radio1').is(':checked')) {
      img_name = '/images/dash-list/drill-group-completed.png';
    } else if ($('#radio2').is(':checked')) {
      img_name = '/images/dash-list/drill-entity-completed.png';
      margin_style = 'margin-left:30px';
    } else if ($('#radio3').is(':checked')) {
      img_name = '/images/dash-list/drill-division-completed.png';
      margin_style = 'margin-left:120px';
    } else if ($('#radio4').is(':checked')) {
      img_name = '/images/dash-list/drill-unit-completed.png';
      margin_style = 'margin-left:140px';
    }
    name = '';
  }
  var htmlstr = '<div style="' + margin_style + '" align="left"><table width="100%" style="margin-left:10px;"><tr><td style="margin-left:10px;font-size:1em" width="100%">Compliances - Country: ' + name + ', Status: ' + com_name + '</td></tr></table><br><img src=' + img_name + '></div>';
  $('#imgcontainer').html(htmlstr);
  $('#imgcontainer').show();
  $('#graph-1').hide();
  $('#graph-2').hide();
  $('#graph-3').hide();
  $('#graph-4').hide();
  $('#graph-5').hide();
}
function loadCountrySpecificBar(value) {
  $('#viewaspie').show();
  $('#viewasbar').hide();
  $('#back').show();
  $('#graph-1').show();
  $('#imgcontainer').hide();
  $(function () {
    $('#graph-1').highcharts({
      colors: [
        '#A5D17A',
        '#F58835',
        '#F0F468',
        '#F32D2B'
      ],
      chart: { type: 'column' },
      title: { text: 'Country wise Compliances - India' },
      xAxis: {
        type: 'category',
        title: { text: 'Compliance Status' }
      },
      yAxis: {
        title: { text: 'Total Compliances' },
        allowDecimals: false
      },
      legend: { enabled: false },
      plotOptions: {
        column: {
          dataLabels: {
            enabled: true,
            style: {
              /*textShadow: '0 0 3px black',*/
              textShadow: null
            },
            /*format:'{point.percentage:.0f}%'*/
            format: '{point.y}'  // 	formatter:function() {
                         // 	var dataSum = (5 + 2 +8 + 3);
                         // 	var pcnt = (this.y / dataSum) * 100;
                         // 	return Highcharts.numberFormat(pcnt,0) + '%';
                         // }
          },
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                if (drilldown) {
                  $('#hidden').val('singlebar');
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        },
        series: {
          borderWidth: 0,
          dataLabels: { enabled: true }
        }
      },
      tooltip: {
        headerFormat: '',
        pointFormat: '<span>{point.name}</span>: <b>{point.y:.0f} Out of 70'
      },
      series: [{
          name: 'Compliances - Group wise',
          colorByPoint: true,
          data: [
            {
              name: 'Complied',
              y: 15,
              drilldown: 'Complied'
            },
            {
              name: 'Delayed compliance',
              y: 15,
              drilldown: 'Delayed'
            },
            {
              name: 'In progress',
              y: 18,
              drilldown: 'Inprogress'
            },
            {
              name: 'Not complied',
              y: 22,
              drilldown: 'NotComplied'
            }
          ]
        }]
    });
  });
}
function loadCountrySpecific(value) {
  $('#viewaspie').hide();
  $('#back').show();
  $('#viewasbar').show();
  $('#graph-1').show();
  $('#imgcontainer').hide();
  $(function () {
    $('#graph-1').highcharts({
      colors: [
        '#A5D17A',
        '#F58835',
        '#F0F468',
        '#F32D2B'
      ],
      chart: {
        type: 'pie',
        options3d: {
          enabled: true,
          alpha: 45,
          beta: 0
        }
      },
      title: { text: 'Country wise Compliances - India' },
      tooltip: {
        headerFormat: '',
        pointFormat: '{point.name}:{point.y} Out of 70'
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          depth: 35,
          dataLabels: {
            enabled: true,
            format: '{point.percentage:.0f}%'
          },
          showInLegend: true,
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                $('#hidden').val('singlepie');
                if (drilldown) {
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        }
      },
      series: [{
          type: 'pie',
          name: 'Compliance',
          data: [
            {
              name: 'Complied',
              y: 15,
              drilldown: 'Complied'
            },
            {
              name: 'Delayed compliance',
              y: 15,
              drilldown: 'Delayed'
            },
            {
              name: 'In progress',
              y: 18,
              drilldown: 'Inprogress'
            },
            {
              name: 'Not complied',
              y: 22,
              drilldown: 'NotComplied'
            }
          ]
        }]
    });
  });
}
function loadGroup() {
  $('#viewaspie').hide();
  $('#back').hide();
  $('#viewasbar').hide();
  $('.SumoSelect').show();
  $('#entity-auto').hide();
  $('#division-auto').hide();
  $('#unit-auto').hide();
  $('#previous').hide();
  $('#next').hide();
  $('#graph-1').show();
  $('#imgcontainer').hide();
  var values = $('.country-filter').val();
  var inprogress_data = [10];
  var pending_data = [10];
  var completed_data = [10];
  var not_complied = [10];
  if (values.length <= 1) {
    loadCompanySingleSelection(values[0]);
  } else if (values.length > 1) {
    for (var i = 0; i < values.length; i++) {
      if (values[i] == 'India') {
        inprogress_data[i] = {
          name: 'India',
          y: 23,
          drilldown: 'Inprogress'
        };
        pending_data[i] = {
          name: 'India',
          y: 22,
          drilldown: 'Delayed'
        };
        completed_data[i] = {
          id: 'fin',
          name: 'India',
          y: 19,
          drilldown: 'Complied'
        };
        not_complied[i] = {
          name: 'India',
          y: 31,
          drilldown: 'NotComplied'
        };
      } else if (values[i] == 'US') {
        inprogress_data[i] = {
          name: 'US',
          y: 19
        };
        pending_data[i] = {
          name: 'US',
          y: 27
        };
        completed_data[i] = {
          name: 'US',
          y: 28
        };
        not_complied[i] = {
          name: 'US',
          y: 15
        };
      } else if (values[i] == 'Singapore') {
        inprogress_data[i] = {
          name: 'Singapore',
          y: 15
        };
        pending_data[i] = {
          name: 'Singapore',
          y: 23
        };
        completed_data[i] = {
          name: 'Singapore',
          y: 16
        };
        not_complied[i] = {
          name: 'Singapore',
          y: 23
        };
      } else if (values[i] == 'Malaysia') {
        inprogress_data[i] = {
          name: 'Malaysia',
          y: 25
        };
        pending_data[i] = {
          name: 'Malaysia',
          y: 32
        };
        completed_data[i] = {
          name: 'Malaysia',
          y: 13
        };
        not_complied[i] = {
          name: 'Malaysia',
          y: 24
        };
      } else if (values[i] == 'China') {
        inprogress_data[i] = {
          name: 'China',
          y: 12
        };
        pending_data[i] = {
          name: 'China',
          y: 26
        };
        completed_data[i] = {
          id: 'fin',
          name: 'China',
          y: 33
        };
        not_complied[i] = {
          name: 'China',
          y: 14
        };
      }
    }
  } else {
    alert('Select atleast one unit to load chart');
  }
  $(function () {
    $('#graph-1').highcharts({
      colors: [
        '#F32D2B',
        '#F0F468',
        '#F58835',
        '#A5D17A'
      ],
      chart: {
        type: 'bar',
        width: '850'
      },
      title: { text: 'Country wise Compliances' },
      xAxis: {
        title: { text: 'Countries' },
        categories: [
          'India',
          'US',
          'Singapore',
          'Malaysia',
          'China'
        ],
        labels: {
          useHTML: true,
          formatter: function () {
            var name = this.value;
            if (name == 'India') {
              var link = '<abbr class="page-load" style="width:200px" title="Year: 2014\nFinance : April to March\nIndustrial Law : January to Dececmber\nLabour Law : January to December"><a href="#"  id="' + name + '" onclick=loadCountrySpecific(this.id)>' + name + '</a><abbr>';
              return link;
            } else {
              var link = '<span  id="' + name + '" >' + name + '</span>';
              return link;
            }
          }
        }
      },
      yAxis: {
        min: 0,
        title: { text: 'Total Compliances' },
        allowDecimals: false
      },
      legend: { reversed: true },
      tooltip: {
        // headerFormat: '<b>{point.x}</b><br/>',
        // pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
        headerFormat: '<b>{point.x}</b>: {point.percentage:.0f}% ',
        pointFormat: '({point.y} Out of {point.stackTotal})'
      },
      plotOptions: {
        series: {
          stacking: 'normal',
          dataLabels: {
            enabled: true,
            color: '#000000',
            style: {
              textShadow: null,
              color: '#000000'
            },
            // format:'{point.percentage:.0f}%'
            format: '{point.y}'
          },
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                $('#hidden').val('group');
                if (drilldown) {
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        }
      },
      series: [
        {
          name: 'Not complied',
          data: not_complied
        },
        {
          name: 'In progress',
          data: inprogress_data
        },
        {
          name: 'Delayed compliance',
          data: pending_data
        },
        {
          name: 'Complied',
          data: completed_data
        }
      ]
    });
  });
}
function loadEscalations() {
  $('#viewasbar').hide();
  $('#viewaspie').hide();
  $('#back').hide();
  $('#previous').hide();
  $('#next').hide();
  $('#previousyear').hide();
  $('#nextyear').hide();
  $(function () {
    var not_complied = 0;
    var drill = '';
    var delayed = 0;
    var title = '';
    var total = 0;
    var data1 = [
      5,
      1,
      3,
      6,
      7
    ];
    var data2 = [
      0,
      0,
      1,
      1,
      2
    ];
    if ($('#radio4').is(':checked')) {
      colors:
        [
          '#FF7700',
          '#D10018'
        ], not_complied = 3;
      drill = 'unitesc';
      delayed = 10;
      title = 'Branch Office - 1';
      total = 28;
      data1 = [
        8,
        8,
        4,
        1,
        9
      ];
      data2 = [
        0,
        1,
        0,
        2,
        1
      ];
    } else if ($('#radio3').is(':checked')) {
      color = [
        '#FFA500',
        '#FF0000',
        '#FFC0CB',
        '#00FF00',
        '#008000'
      ];
      not_complied = 4;
      drill = 'divisionesc';
      delayed = 5;
      total = 29;
      title = 'Manufacturing division';
      data1 = [
        9,
        6,
        9,
        10,
        2
      ];
      data2 = [
        0,
        0,
        1,
        2,
        1
      ];
    } else if ($('#radio2').is(':checked')) {
      color = [
        '#008000',
        '#FFA500',
        '#FF0000',
        '#FFC0CB',
        '#00FF00'
      ];
      not_complied = 6;
      drill = 'entityesc';
      delayed = 10;
      total = 50;
      title = 'KG';
      data1 = [
        3,
        9,
        5,
        8,
        8
      ];
      data2 = [
        0,
        2,
        1,
        3,
        1
      ];
    } else if ($('#radio1').is(':checked')) {
      color = [
        Highcharts.getOptions().colors[2],
        Highcharts.getOptions().colors[5],
        '#FFC0CB',
        '#00FF00',
        '#008000'
      ];
      not_complied = 8;
      drill = 'groupesc';
      delayed = 10;
      total = 48;
      title = 'KG Groups';
      data1 = [
        9,
        5,
        9,
        8,
        4
      ];
      data2 = [
        0,
        1,
        2,
        3,
        1
      ];
    } else if ($('#radio5').is(':checked')) {
      title = 'KG';
    }
    $('#graph-2').highcharts({
      colors: [
        '#F58835',
        '#F32D2B'
      ],
      chart: { type: 'column' },
      title: { text: 'Escalations of ' + title },
      subtitle: { text: '' },
      xAxis: {
        categories: [
          '2011',
          '2012',
          '2013',
          '2014',
          '2015'
        ],
        crosshair: true,
        labels: {
          useHTML: true,
          formatter: function () {
            var name = this.value;
            if ($('#radio1').is(':checked')) {
              if (name == '2012') {
                $('#hidden').val('Escalations of ' + title);
                var link = '<a href="#"  id="' + name + '" onclick=loadDrillDownData()>' + name + '</a>';
                return link;
              } else {
                var link = '<span  id="' + name + '" >' + name + '</span>';
                return link;
              }
            } else {
              var link = '<span  id="' + name + '" >' + name + '</span>';
              return link;
            }
          }
        }
      },
      yAxis: {
        min: 0,
        title: { text: 'Total Compliances' },
        allowDecimals: false
      },
      tooltip: {
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="padding:0">{series.name}: </td>' + '<td style="padding:0"><b>{point.y:.0f}</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
      },
      plotOptions: {
        column: {
          pointPadding: 0,
          groupPadding: 0.3,
          borderWidth: 0,
          dataLabels: {
            enabled: true,
            textShadow: null,
            // format:'{point.percentage:.0f}%'
            format: '{point.y}'
          },
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                if (drilldown) {
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        }
      },
      series: [
        {
          name: 'Delayed Compliance',
          data: data1
        },
        {
          name: 'Not Complied',
          data: data2
        }
      ]
    });
  });
}
function ageingwiseCompliance() {
  $('#viewasbar').hide();
  $('#viewaspie').hide();
  $('#previous').hide();
  $('#next').hide();
  $('#back').hide();
  $('#previousyear').hide();
  $('#nextyear').hide();
  $(function () {
    var ztt = 0;
    var drill = '';
    var tts = 0;
    var chartColor = [
      '#FF9C80',
      '#F2746B',
      '#FB4739',
      '#DD070C'
    ];
    var stn = 0;
    var above90 = 0;
    var title = '';
    var total = 0;
    if ($('#radio4').is(':checked')) {
      colors:
        chartColor;
      // colors:['#a3d202','#e70808'],
      drill = 'unitesc';
      var tts = 8;
      var stn = 3;
      var above90 = 2;
      var ztt = 5;
      total = 8 + 3 + 2 + 5;
      title = 'Branch Office - 1 ';
      total = 28;
    } else if ($('#radio3').is(':checked')) {
      colors:
        chartColor;
      drill = 'divisionesc';
      var tts = 6;
      var stn = 1;
      var above90 = 9;
      var ztt = 10;
      total = 6 + 1 + 9 + 10;
      title = 'Manufacturing division';
    } else if ($('#radio2').is(':checked')) {
      colors:
        chartColor;
      var tts = 8;
      var stn = 5;
      var above90 = 7;
      var ztt = 12;
      total = 8 + 5 + 7 + 12;
      drill = 'entityesc';
      title = 'KG';
    } else if ($('#radio1').is(':checked')) {
      colors:
        chartColor;
      drill = 'groupesc';
      var tts = 11;
      var stn = 3;
      var above90 = 8;
      var ztt = 5;
      total = 11 + 3 + 8 + 5;
      title = 'KG groups';
    } else if ($('#radio5').is(':checked')) {
      colors:
        chartColor;
      drill = 'businessesc';
      var tts = 11;
      var stn = 3;
      var above90 = 8;
      var ztt = 5;
      total = 11 + 3 + 8 + 5;
      title = 'KG Business Group 1';
    }
    $('#graph-3').highcharts({
      colors: chartColor,
      chart: {
        type: 'pie',
        options3d: {
          enabled: true,
          alpha: 30
        }
      },
      title: { text: 'Over due compliance of ' + title },
      subtitle: { text: '' },
      plotOptions: {
        pie: {
          depth: 45,
          dataLabels: {
            enabled: true,
            format: '{point.percentage}%'
          },
          showInLegend: true,
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                if (drilldown) {
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        }
      },
      tooltip: {
        headerFormat: '',
        pointFormat: '<span>{point.name}</span>: <b>{point.y:.0f}</b> out of ' + total
      },
      series: [{
          name: 'Compliances',
          dataLabels: {
            enabled: true,
            format: '{point.percentage:.0f}%'
          },
          data: [
            {
              name: '0-30 days',
              y: ztt
            },
            {
              name: '31-60 days',
              y: tts
            },
            {
              name: '61-90 days',
              y: stn
            },
            {
              name: 'Above 90 days',
              y: above90
            }
          ]
        }]
    });
  });
}
function loadTrendChart(title) {
  $('#back').hide();
  $('#next').hide();
  $('#previous').hide();
  $('#previousyear').hide();
  $('#nextyear').hide();
  $(function () {
    $('#graph-4').highcharts({
      title: { text: 'Complied (2009 to 2014)' },
      subtitle: { text: '' },
      xAxis: {
        categories: [
          '2009',
          '2010',
          '2011',
          '2012',
          '2013',
          '2014'
        ],
        labels: {
          useHTML: true,
          formatter: function () {
            var name = this.value;
            if (name == 'Jan') {
              var link = '<a href="#"  id="' + name + '" onclick=loadDrillDownData(this.id) >' + name + '</a>';
              return link;
            } else {
              var link = '<span  id="' + name + '" onclick=loadDrillDownData(this.id) >' + name + '</span>';
              return link;
            }
          }
        },
        title: { text: 'Year' }
      },
      yAxis: {
        title: { text: 'Compliance (%)' },
        labels: {
          formatter: function () {
            return this.value + '%';
          }
        },
        allowDecimals: false
      },
      tooltip: {
        crosshairs: true,
        shared: true,
        backgroundColor: '#FCFFC5',
        formatter: function () {
          var s = '<b>' + this.x + '</b>', sum = 0;
          $.each(this.points, function (i, point) {
            total = point.y + 240;
            tasks = point.y / 100 * total;
            color = point.color;
            s += '<br/><span style="color:' + color + ';"><b>' + point.series.name + '</b></span>: ' + point.y + '% (' + Math.round(tasks) + ' out of ' + total + ')';
            sum += point.y;
          });
          return s;
        }
      },
      plotOptions: {
        spline: {
          marker: {
            radius: 4,
            lineColor: '#666666',
            lineWidth: 1
          }
        }
      },
      series: [
        {
          name: 'India',
          marker: { symbol: 'square' },
          data: [
            93,
            94,
            95,
            96,
            97,
            98
          ]
        },
        {
          name: 'US',
          marker: { symbol: 'diamond' },
          data: [
            90,
            91,
            93,
            93,
            95,
            96
          ]
        },
        {
          name: 'Singapore',
          marker: { symbol: 'square' },
          data: [
            91,
            92,
            93,
            94,
            95,
            97
          ]
        },
        {
          name: 'Malaysia',
          marker: { symbol: 'circle' },
          data: [
            90,
            90,
            92,
            93,
            95,
            96
          ]
        }
      ]
    });
  });
}
function loadPieChart() {
  $('#viewaspie').hide();
  $('#viewasbar').hide();
  $('#division-para2').show();
  $('#unit-para1').hide();
  $('#unit-para2').show();
  $('#back').hide();
  $('#previousyear').hide();
  $('#nextyear').hide();
  $(function () {
    var color = [6];
    var applied = 0;
    var not_opted = 0;
    var not_applicable = 0;
    var drill1 = '';
    var drill2 = '';
    var drill3 = '';
    title = '';
    if ($('#radio4').is(':checked')) {
      applied = 815;
      not_opted = 20;
      not_applicable = 12;
      var dataSum = 815 + 20 + 12;
      drill1 = 'unitapp';
      drill2 = 'unitnotapp';
      drill3 = 'unitnotopt';
      title = ' - Branch Office - 1';
    } else if ($('#radio3').is(':checked')) {
      applied = 49;
      not_opted = 160;
      not_applicable = 41;
      var dataSum = 160 + 49 + 41;
      drill1 = 'divapp';
      drill2 = 'divnotapp';
      drill3 = 'divnotopt';
      title = ' - Manufacturing division';
    } else if ($('#radio5').is(':checked')) {
      applied = 40;
      not_opted = 126;
      not_applicable = 12;
      var dataSum = 126 + 40 + 12;
      drill1 = 'bgapp';
      drill2 = 'bgnotapp';
      drill3 = 'bgnotopt';
      title = ' - KG Business Group 1';
    } else if ($('#radio2').is(':checked')) {
      applied = 158;
      not_opted = 48;
      not_applicable = 8;
      var dataSum = 158 + 48 + 8;
      drill1 = 'entityapp';
      drill2 = 'entitynotapp';
      drill3 = 'entitynotopt';
      title = ' - KG & Sons';
    } else if ($('#radio1').is(':checked')) {
      color = [
        Highcharts.getOptions().colors[2],
        Highcharts.getOptions().colors[5],
        '#FFC0CB',
        '#00FF00',
        '#008000'
      ];
      applied = 179;
      not_opted = 21;
      not_applicable = 12;
      var dataSum = 179 + 21 + 12;
      drill1 = 'groupapp';
      drill2 = 'groupnotapp';
      drill3 = 'groupnotopt';
      title = ' - KG groups';
    }
    $('#graph-5').highcharts({
      colors: [
        '#66FF66',
        '#FFDC52',
        '#CE253C'
      ],
      chart: {
        type: 'pie',
        options3d: {
          enabled: true,
          alpha: 45,
          beta: 0
        }
      },
      title: { text: 'Compliance Applicability Status ' + title },
      tooltip: {
        headerFormat: '',
        pointFormat: '{point.name}: <b>{point.y:.0f}</b> of ' + dataSum
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          depth: 35,
          dataLabels: {
            enabled: true,
            format: '{point.percentage:.0f}%',
            formatter: function () {
              var pcnt = this.y / dataSum * 100;
              return Highcharts.numberFormat(pcnt, 0) + '%';
            }
          },
          showInLegend: true,
          point: {
            events: {
              click: function () {
                var drilldown = this.drilldown;
                if (drilldown) {
                  loadDrillDownData(drilldown);
                }
              }
            }
          }
        }
      },
      series: [{
          name: 'Compliance',
          colorByPoint: true,
          data: [
            {
              name: 'Applicable',
              y: applied,
              drilldown: drill1
            },
            {
              name: 'Not Applicable',
              y: not_applicable,
              drilldown: drill2
            },
            {
              name: 'Not opted',
              y: not_opted,
              drilldown: drill3
            }
          ]
        }]
    });
  });
}
function loadConsolidated(value) {
  $('#viewaspie').hide();
  $('#back').hide();
  $('#viewasbar').hide();
  $('#graph-1').show();
  $('#imgcontainer').hide();
  $('#previous').hide();
  $('#next').hide();
  $(function () {
    $('#graph-1').highcharts({
      colors: [
        '#A5D17A',
        '#F58835',
        '#F0F468',
        '#F32D2B'
      ],
      chart: {
        type: 'pie',
        options3d: {
          enabled: true,
          alpha: 45,
          beta: 0
        }
      },
      title: { text: 'Consolidated Chart' },
      tooltip: {
        headerFormat: '',
        pointFormat: '{point.name}:{point.y} Out of 70'
      },
      plotOptions: {
        pie: {
          allowPointSelect: true,
          cursor: 'pointer',
          depth: 35,
          dataLabels: {
            enabled: true,
            format: '{point.percentage:.0f}%'
          },
          showInLegend: true,
          point: {}
        }
      },
      series: [{
          type: 'pie',
          name: 'Compliance',
          data: [
            {
              name: 'Complied',
              y: 15,
              drilldown: 'Complied'
            },
            {
              name: 'Delayed compliance',
              y: 15,
              drilldown: 'Delayed'
            },
            {
              name: 'In progress',
              y: 18,
              drilldown: 'Inprogress'
            },
            {
              name: 'Not complied',
              y: 22,
              drilldown: 'NotComplied'
            }
          ]
        }]
    });
  });
}
// $('.country-filter').multipleSelect({
//     filter: true,
//     multiple: true
// });
// $('#unit-para1').find('select').multipleSelect({
//     filter: true,
//     multiple: true
// });
$(function () {
  $('#text2').autoComplete({
    minChars: 1,
    source: function (term, suggest) {
      term = term.toLowerCase();
      var choices = [
        'Bajaj Allianz Group',
        'PRG Group',
        'TVS Group'
      ];
      var suggestions = [];
      for (i = 0; i < choices.length; i++)
        if (~choices[i].toLowerCase().indexOf(term))
          suggestions.push(choices[i]);
      suggest(suggestions);
    }
  });
  $('#text3').autoComplete({
    minChars: 1,
    source: function (term, suggest) {
      term = term.toLowerCase();
      var choices = [
        'Auto Parts - Manufacturing',
        'Division 1',
        'Division 2'
      ];
      var suggestions = [];
      for (i = 0; i < choices.length; i++)
        if (~choices[i].toLowerCase().indexOf(term))
          suggestions.push(choices[i]);
      suggest(suggestions);
    }
  });
  $('#text4').autoComplete({
    minChars: 1,
    source: function (term, suggest) {
      term = term.toLowerCase();
      var choices = [
        'South Gate, Madurai',
        'Periyar, Madurai',
        'Mattuthavani, Madurai'
      ];
      var suggestions = [];
      for (i = 0; i < choices.length; i++)
        if (~choices[i].toLowerCase().indexOf(term))
          suggestions.push(choices[i]);
      suggest(suggestions);
    }
  });
});