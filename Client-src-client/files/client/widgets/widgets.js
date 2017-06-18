var PageTitle = $('.page-title');
var widget_info;
var widget_list;
var SIDEBAR_MAP = {};
var WIDGET_INFO_ID = [];

function getLE_ids() {
    w_le_ids = []
    w_le_data = client_mirror.getSelectedLegalEntity();
    $.each(w_le_data, function(i, v) {
        w_le_ids.push(v.le_id);
    });
    return w_le_ids;
}


//
// Compliance status
//
function updateComplianceStatusStackBarChart(data, id) {
  var tot = '';
  var xAxisName = ''; // data['xaxis_name'];
  var xAxis = data['xaxis'];
  var chartDataSeries = data['widget_data'];
  var chartTitle = data['chart_title'];
  //var drilldownSeries = data[4];
  $.each(chartDataSeries, function(k ,v) {
    tot +=  v["data"].length;
  });
  if(tot == 0){
    chartDataSeries = "";
  }  
  var yAxisname = [
    'Complied',
    'Delayed Compliance',
    'Inprogress',
    'Not Complied'
  ];
  var highchart_cs;
  highchart_cs = new Highcharts.Chart({
    chart: {
      renderTo: 'cardbox'+id,
      type: 'bar'
    },
    title: { text: '' }, //chartTitle
    credits: { enabled: false },
    xAxis: {
      categories: xAxis,
      title: { text: xAxisName },
      labels: {
        // style: {
        //   cursor: 'pointer',
        //   color: 'blue',
        //   textDecoration: 'underline'
        // },
        // useHTML: true,
        formatter: function () {
          return '<div id="label_' + this.value + '">' + this.value + '</div>';
        }
      },
      tooltip: { pointFormat: '' }
    },
    yAxis: {
      min: 0,
      title: { text: 'Total compliances' },
      allowDecimals: false,
      reversedStacks: false
    },
    // tooltip: {
    //   headerFormat: '{point.series.name}: ',
    //   pointFormat: '<b>{point.y}</b>'
    // },
    legend: {
      itemStyle: {
          fontWeight: 'normal',
          fontSize: '11px'
      }
    },
    plotOptions: {
      series: { pointWidth: 35 },
      bar: {
        stacking: 'normal',
        cursor: 'pointer',
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
          }
        }
      }
    },
    colors: [
      '#3ec845',
      '#fe6271',
      '#fbca35',
      '#F32D2B'
    ],
    exporting: {
      enabled: false
    },
    series: chartDataSeries
  });
  // $('.highcharts-axis-labels text, .highcharts-axis-labels span').click(function () {
  //   var value = this.textContent || this.innerText;
  //   name = value;
  //   data_series = drilldownSeries[name];
  //   var title = chartTitle + ' - ' + name;
  //   // updateComplianceStatusPieChart(data_series, title, 'pie', name);
  //   complianceDrillDown(data_series, title, name);  // setChart(value);
  // });
  // year = chartInput.getChartYear();
  // if (year == 0) {
  //   year = chartInput.getCurrentYear();
  // }
  // domain_ids = chartInput.getDomains();
  // domain_names = [];
  // for (var x = 0; x < domain_ids.length; x++) {
  //   id = domain_ids[x];
  //   domain_names.push(DOMAINS[id]);
  // }
  // $.each(DOMAIN_INFO, function (key, value) {
  //   frame_title = 'Year : ' + year + '\n';
  //   for (var i = 0; i < value.length; i++) {
  //     info = value[i];
  //     if (domain_names.indexOf(info.domain_name) != -1) {
  //       frame_title += '' + info.domain_name + ' : ' + info.period_from + ' to ' + info.period_to + '\n';
  //     }
  //   }
  //   $('#label_' + key).attr({
  //     placement: 'bottom',
  //     title: frame_title
  //   });
  // });  // $("#label_India").attr({placement: 'bottom', title:"HELLO India!"});
  $(".dragdrophandles .resizable1").resizable({
    autoHide: true,    
    resize: function() {
      $(this).find("h2 .pins i").removeClass("ti-pin-alt");
      $(this).find("h2 .pins i").addClass("ti-pin2");
      // $(this).find("h2 .pins i").prop("title", "Click to save");
      $(this).find("h2 .pins i").attr("data-original-title", "Click to save");
      highchart_cs.setSize(
          this.offsetWidth - 40,
          this.offsetHeight - 50,
          false
      );
    },
    minWidth: 309,
  });
}
//
// Escalation chart
//
function updateEscalationChart(data, id) {
  var tot = 0;
  xAxis = data['xaxis'];
  chartDataSeries = data['widget_data'];
  chartTitle = data['chart_title'];  
  $.each(chartDataSeries, function(k ,v) {
    $.each(v["data"], function(k1 ,v1) {
      tot += v1["y"]; 
    });
  });
  if(tot == 0){
    chartDataSeries = "";
  }
  highchart_es = new Highcharts.Chart({
    colors: [
      '#fe6271',
      '#F32D2B'
    ],
    chart: {
      type: 'column',
      renderTo: 'cardbox'+id
    },
    title: { text: ''  },//chartTitle
    credits: { enabled: false },
    xAxis: {
      categories: xAxis,
      crosshair: true
    },
    yAxis: {
      min: 0,
      title: { text: 'Total Compliances' },
      allowDecimals: false
    },
    legend: {
      itemStyle: {
          fontWeight: 'normal',
          fontSize: '11px'
      }
    },
     tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.0f}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
    plotOptions: {
      series: {
        // pointWidth: 10,
         groupPadding: 0.2,
         pointPadding: 0,        
        dataLabels: {
                    enabled: true,
                    textShadow: null,
                    // format:'{point.percentage:.0f}%'
                    format: '{point.y}'
                },
      },
      column: {
        dataLabels: {
          enabled: false,
          textShadow: null,
          format: '{point.y}'
        }
      }
    },
    exporting: {
      enabled: false
    },
    series: chartDataSeries
  });
  // $('.highcharts-axis-labels text, .highcharts-axis-labels span').click(function () {
  //   var year = this.textContent || this.innerText;
  //   loadEscalationDrillDown(year);  // setChart(value);
  // });
  $(".dragdrophandles .resizable2").resizable({
    autoHide: true,
    minWidth: 309,
    resize: function() {
      $(this).find("h2 .pins i").removeClass("ti-pin-alt");
      $(this).find("h2 .pins i").addClass("ti-pin2");
      // $(this).find("h2 .pins i").prop("title", "Click to save");
      $(this).find("h2 .pins i").attr("data-original-title", "Click to save");
      highchart_es.setSize(
          this.offsetWidth - 40,
          this.offsetHeight - 50,
          false
      );
    }
  });
}
//
// Not complied
//
function updateNotCompliedChart(data, id) {
  // data = prepareNotCompliedChart(data);
  var tot = 0;
  chartDataSeries = data['widget_data'];
  chartTitle = data['chart_title'];  
  $.each(chartDataSeries, function(k, v) { tot=tot+v["y"]; return tot;});
  total = tot;
  // if(tot == 0){
  //   chartDataSeries = "";
  // }
  highchart_nc = new Highcharts.Chart({
    colors: [
      '#FF9C80',
      '#F2746B',
      '#FB4739',
      '#DD070C'
    ],
    chart: {
      plotBackgroundColor: null,
      plotBorderWidth: null,
      plotShadow: false,
      renderTo: 'cardbox'+id,
      type: 'pie',
      options3d: {
        enabled: true,
        alpha: 30 // 55
      }
    },
    title: { text: '' }, //chartTitle
    xAxis: { categories: true },
    credits: { enabled: false },
    tooltip: {
      headerFormat: '',
      pointFormat: '<span>{point.name}</span>: <b>{point.y:.0f}</b> out of ' + total
    },
    legend: {
      enabled: true,
      itemStyle: {
          fontWeight: 'normal',
          fontSize: '11px'
      }
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        depth: 35,
        dataLabels: {
          enabled: true,
          format: '{point.percentage: .0f}%'
        },
        showInLegend: true,
        point: {
          events: {
          }
        }
      }
    },
    series: [{
        name: 'compliance',
        colorByPoint: true,
        data: chartDataSeries
      }],
    exporting: {
      enabled: false
    },
  });
  $(".dragdrophandles .resizable3").resizable({
    autoHide: true,
    minWidth: 309,
    resize: function() {
      $(this).find("h2 .pins i").removeClass("ti-pin-alt");
      $(this).find("h2 .pins i").addClass("ti-pin2");
      // $(this).find("h2 .pins i").prop("title", "Click to save");
      $(this).find("h2 .pins i").attr("data-original-title", "Click to save");
      highchart_nc.setSize(
          this.offsetWidth - 40,
          this.offsetHeight - 50,
          false
      );
    }    
  });
}
//
// Trend  chart
//
function updateTrendChart(data, id) {
  //data = prepareTrendChartData(data);
  print_data = JSON.stringify(data, null, ' ');
  xAxis = data['xaxis'];
  chartTitle = data['chart_title'];
  chartDataSeries = data['widget_data'];

  highchart_tc = new Highcharts.Chart({
    chart: { renderTo: 'cardbox'+id },
    title: { text: '' }, //chartTitle
    credits: { enabled: false },
    xAxis: {
      categories: xAxis,
      title: { text: '' }, //Year
      labels: {
        style: {
          cursor: 'pointer',
          color: 'blue',
          textDecoration: 'underline'
        }
      }
    },
    yAxis: {
      min: 0,
      title: { text: 'Compliance (%)' },
      labels: {
        formatter: function () {
          return this.value + '%';
        }
      },
      allowDecimals: false
    },
    tooltip: {
      crosshair: true,
      shared: true,
      backgroundColor: '#FCFFC5',
      headerFormat: '<b>{point.x}</b>: {point.percentage:.0f}% ',
      pointFormat: '({point.point.y} out of {point.stackTotal})',
      formatter: function () {
        var s = '<b>' + this.x + '</b>', sum = 0;
        $.each(this.points, function (i, point) {
          total = point.point.t;
          tasks = Math.round(point.point.y * 100 / total, 2);
          color = point.color;
          s += '<br/><span style="color:' + color + '"> <b>' + point.series.name + '</b> </span>: ' + tasks + '% (' + point.point.y + ' out of ' + total + ')';
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
    legend: {
      itemStyle: {
          fontWeight: 'normal',
          fontSize: '11px'
      }
    },
    exporting: {
      enabled: false
    },
    series: chartDataSeries
  });
  // $('.highcharts-axis-labels text, .highcharts-axis-labels span').click(function () {
  //   var value = this.textContent || this.innerText;
  //   name = value;
  //   loadTrendChartDrillDown(value);
  //   $('.btn-back').show();
  //   $('.btn-back').on('click', function () {
  //     // updateTrendChart(data);
  //     loadTrendChart();
  //     $('.btn-back').hide();
  //   });  // setChart(value);
  // });
  $(".dragdrophandles .resizable4").resizable({
    autoHide: true,
    minWidth: 309,
    resize: function() {
      $(this).find("h2 .pins i").removeClass("ti-pin-alt");
      $(this).find("h2 .pins i").addClass("ti-pin2");
      // $(this).find("h2 .pins i").prop("title", "Click to save");
      $(this).find("h2 .pins i").attr("data-original-title", "Click to save");
      highchart_tc.setSize(
          this.offsetWidth - 40,
          this.offsetHeight - 50,
          false
      );
    }
  });
}
//
// Compliance applicability status
//
function updateComplianceApplicabilityChart(data, id) {
  //data = prepareComplianceApplicability(data);
  
  var tot = 0;
  chartTitle = data['chart_title'];
  chartDataSeries = data['widget_data'];  
  $.each(chartDataSeries, function(k ,v) {
    tot += v["y"]; return tot;
  }); 
  if(tot == 0){
    chartDataSeries = "";
  }
  highchart_ca = new Highcharts.Chart({
    colors: [
      '#FB4739',
      '#F2746B',      
      '#DD070C',
      '#FF9C80',
    ],
    chart: {
      plotBackgroundColor: null,
      plotBorderWidth: null,
      plotShadow: false,
      type: 'pie',
      renderTo: 'cardbox'+id,
      options3d: {
        enabled: true,
        alpha: 30,
        beta: 0
      }
    },
    title: { text: '' }, //chartTitle
    xAxis: { categories: true },
    credits: { enabled: false },
    tooltip: {
      headerFormat: '',
      pointFormat: '<span>{point.name}</span>: <b>{point.y:.0f}</b> out of ' + tot
    },
    legend: {
      enabled: true,
      itemStyle: {
          fontWeight: 'normal',
          fontSize: '11px'
      }
    },
    plotOptions: {
      pie: {
        allowPointSelect: true,
        cursor: 'pointer',
        depth: 35,
        dataLabels: {
          enabled: true,
          format: '{point.percentage: .0f}%'
        },
        showInLegend: true,
        point: {
          events: {
          }
        }
      }
    },
    series: [{
        name: 'compliance',
        colorByPoint: true,
        data: chartDataSeries
      }],
    exporting: {
      enabled: false
    },
  });
  $(".dragdrophandles .resizable5").resizable({
    autoHide: true,
    minWidth: 309,    
    resize: function() {
      $(this).find("h2 .pins i").removeClass("ti-pin-alt");
      $(this).find("h2 .pins i").addClass("ti-pin2");
      // $(this).find("h2 .pins i").prop("title", "Click to save");
      $(this).find("h2 .pins i").attr("data-original-title", "Click to save");
      highchart_ca.setSize(
          this.offsetWidth - 40,
          this.offsetHeight - 50,
          false
      );
    }
  });
}

function loadComplianceStatusChart(data, id){
  updateComplianceStatusStackBarChart(data, id);
}

function loadEscalationChart(data, id){
  updateEscalationChart(data, id)
}

function loadNotCompliedChart(data, id){
  updateNotCompliedChart(data, id)
}

function loadTrendChart(data, id){
  updateTrendChart(data, id);
}

function loadComplianceApplicabilityChart(data, id){
  updateComplianceApplicabilityChart(data, id);
}

function userScoreCard(data, id){
  var total_assignee = 0;
  var total_concur = 0;
  var total_approve = 0;
  var usc = $("#templates .user-score-card-templates .table");
  var uscclone = usc.clone();
  $("#cardbox"+id).append(uscclone);
  $.each(data.widget_data, function(k,v){
    var usc_tr = $("#templates .user-score-card-templates .usc-tr");
    var uscclone_tr = usc_tr.clone();
    $(".usc-role", uscclone_tr).html(v.Role);
    $(".usc-assignee", uscclone_tr).html(v.Assingee);
    $(".usc-concur", uscclone_tr).html(v.Concur);
    $(".usc-approve", uscclone_tr).html(v.Approver);
    total_assignee += v.Assingee;
    total_concur += v.Concur;
    total_approve += v.Approver;
    $("#cardbox"+id+" .tbody-usc").append(uscclone_tr);
  });

  var usc_total = $("#templates .user-score-card-templates .usc-total-tr");
  var uscclone_total = usc_total.clone();
  $(".total-usc-role", uscclone_total).html("Total");
  $(".total-usc-assignee", uscclone_total).html(total_assignee);
  $(".total-usc-concur", uscclone_total).html(total_concur);
  $(".total-usc-approve", uscclone_total).html(total_approve);
  $("#cardbox"+id+" .tbody-usc").append(uscclone_total);
  $(".dragdrophandles .resizable6").resizable({
    autoHide: true,
    minWidth: 309,
    resize: function() {
      $(this).find("h2 .pins i").removeClass("ti-pin-alt");
      $(this).find("h2 .pins i").addClass("ti-pin2");
      // $(this).find("h2 .pins i").prop("title", "Click to save");      
      $(this).find("h2 .pins i").attr("data-original-title", "Click to save");
    }
  });
}

function domainScoreCard(data, id){
  var dc_le_ids = [];
  var all_le_ids = [];
  var total_assigned = 0;
  var total_unassigned = 0;
  var total_notopted = 0;
  var total_subtotal = 0;
  var grandtotal = 0;
  var dsc = $("#templates .domain-score-card-templates .domain-sc");
  var dscclone = dsc.clone();
  var options = '';
  var selectedLegalentity = client_mirror.getSelectedLegalEntity();
  options += '<option value="">All</option>';
  $.each(selectedLegalentity, function(k, v){
    all_le_ids.push(v.le_id);
    options += '<option value="'+v.le_id+'">'+v.le_name+'</option>';
  });
  $(".domain-legalentity", dscclone).append(options); 
  $(".domain-legalentity", dscclone).on("change", function(){
    if($(this).val() == ""){
      dc_le_ids = all_le_ids;
    }else{
      dc_le_ids = [];
      dc_le_ids.push(parseInt($(this).val()));
    }
//    if($(this).val()){
      var settings = widgetSettings();
      settings[7](dc_le_ids, function(error1, data){
        if(error1 == null){
          $("#cardbox7 .tbody-dsc").html("");
          var total_assigned = 0;
          var total_unassigned = 0;
          var total_notopted = 0;
          var total_subtotal = 0;
          var grandtotal = 0;
          //widgetLoadChart()[7](data1, 7);
          $.each(data.widget_data, function(k,v){
            var dsc_tr = $("#templates .domain-score-card-templates .dsc-tr");
            var dscclone_tr = dsc_tr.clone();
            $(".dsc-domain", dscclone_tr).html(v.d_name);
            $(".dsc-assigned", dscclone_tr).html(v.assigned);
            $(".dsc-unassigned", dscclone_tr).html(v.unassinged);
            $(".dsc-notopted", dscclone_tr).html(v.notopted);
            total_subtotal = parseInt(v.notopted) + parseInt(v.assigned) + parseInt(v.unassinged);
            $(".dsc-subtotal", dscclone_tr).html(total_subtotal);
            grandtotal = grandtotal+total_subtotal;
            total_assigned += v.assigned;
            total_unassigned += v.unassinged;
            total_notopted += v.notopted;   

            $("#cardbox7 .tbody-dsc").append(dscclone_tr);
          });

          var dsc_total = $("#templates .domain-score-card-templates .dsc-total");
          var dscclone_total = dsc_total.clone();
          $(".dsc-total-text", dscclone_total).html("Total");
          $(".dsc-total-assigned", dscclone_total).html(total_assigned);
          $(".dsc-total-unassigned", dscclone_total).html(total_unassigned);
          $(".dsc-total-notopted", dscclone_total).html(total_notopted);
          $(".dsc-grandtotal", dscclone_total).html(grandtotal);
          $("#cardbox7 .tbody-dsc").append(dscclone_total);
          $(".dragdrophandles .resizable7").resizable({
            autoHide: true,
            minWidth: 309,
            resize: function() {
              $(this).find("h2 .pins i").removeClass("ti-pin-alt");
              $(this).find("h2 .pins i").addClass("ti-pin2");
              // $(this).find("h2 .pins i").prop("title", "Click to save"); 
              $(this).find("h2 .pins i").attr("data-original-title", "Click to save");             
            }
          });
        }
        else{
          console.log(error1);
        }
      });
    // }
  });
  $("#cardbox"+id).append(dscclone);

  var dsc_table = $("#templates .domain-score-card-templates .domain-table");
  var dscclone_table = dsc_table.clone();
  $("#cardbox"+id).append(dscclone_table);

  $.each(data.widget_data, function(k,v){
    var dsc_tr = $("#templates .domain-score-card-templates .dsc-tr");
    var dscclone_tr = dsc_tr.clone();
    $(".dsc-domain", dscclone_tr).html(v.d_name);
    $(".dsc-assigned", dscclone_tr).html(v.assigned);
    $(".dsc-unassigned", dscclone_tr).html(v.unassinged);
    $(".dsc-notopted", dscclone_tr).html(v.notopted);
    total_subtotal = parseInt(v.notopted) + parseInt(v.assigned) + parseInt(v.unassinged);
    $(".dsc-subtotal", dscclone_tr).html(total_subtotal);
    grandtotal = grandtotal+total_subtotal;
    total_assigned += v.assigned;
    total_unassigned += v.unassinged;
    total_notopted += v.notopted;   

    $("#cardbox"+id+" .tbody-dsc").append(dscclone_tr);
  });

  var dsc_total = $("#templates .domain-score-card-templates .dsc-total");
  var dscclone_total = dsc_total.clone();
  $(".dsc-total-text", dscclone_total).html("Total");
  $(".dsc-total-assigned", dscclone_total).html(total_assigned);
  $(".dsc-total-unassigned", dscclone_total).html(total_unassigned);
  $(".dsc-total-notopted", dscclone_total).html(total_notopted);
  $(".dsc-grandtotal", dscclone_total).html(grandtotal);
  $("#cardbox"+id+" .tbody-dsc").append(dscclone_total);
  $(".dragdrophandles .resizable7").resizable({
    autoHide: true,
    minWidth: 309,
    resize: function() {
      $(this).find("h2 .pins i").removeClass("ti-pin-alt");
      $(this).find("h2 .pins i").addClass("ti-pin2");
      // $(this).find("h2 .pins i").prop("title", "Click to save");      
      $(this).find("h2 .pins i").attr("data-original-title", "Click to save");
    }
  });
}



function calenderView(data, id){    

  var cts = $("#templates .calender-templates .cal-select");
  var ctclones = cts.clone();
  $("#cardbox"+id).append(ctclones);
  var options = '';
  var selectedLegalentity = client_mirror.getSelectedLegalEntity();
  $.each(selectedLegalentity, function(k, v){
    options += '<option value="'+v.le_id+'">'+v.le_name+'</option>';
  });
  $(".cal-legalentity").append(options);
  loadcalenderView(data, id);
}
function loadcalenderView(data, id){  
  $("#cardbox"+id+" .cal-rows").empty();
  var wid_data = data.widget_data;
  var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var current_date = new Date(wid_data[0]['CurrentMonth']);
  var month_value = current_date.getMonth();
  var year_value = current_date.getFullYear();
  var week_day = current_date.getDay();
  var html = '';
  var ct = $("#templates .calender-templates .cal-rows");
  var ctclone = ct.clone();
  $(".cal-caption", ctclone).html(months[month_value]+" - "+year_value);
  $("#cardbox"+id).append(ctclone);

  date = current_date;

  day = date.getDate();
  month = date.getMonth();
  year = date.getFullYear();

  months = new Array('January','February','March','April','May','June','July','August','September','October','November','December');
  this_month = new Date(year, month, 1);
  next_month = new Date(year, month + 1, 1);
  // Find out when this month starts and ends.
  first_week_day = this_month.getDay();
  days_in_this_month = Math.round((next_month.getTime() - this_month.getTime()) / (1000 * 60 * 60 * 24));

  calendar_html = '';
  calendar_html += '<tr>';
  for(week_day = 0; week_day < first_week_day; week_day++) {
    calendar_html += '<td class="cal-off"> </td>';
  }
  week_day = first_week_day;
  for(day_counter = 1; day_counter <= days_in_this_month; day_counter++) {
    week_day %= 7;
    if(week_day == 0)
      calendar_html += '</tr><tr>';
    if(day == day_counter)
      calendar_html += '<td class="dateid' + day_counter + '"><div class="date">' + day_counter + '</div></td>';
    else
      calendar_html += '<td class="dateid' + day_counter + '"><div class="date">' + day_counter + '</div></td>';

    week_day++;
  }

  calendar_html += '</tr>';

  $("#cardbox"+id+" .cal-body").append(calendar_html);

  var getdata = wid_data[0]['data'];
  $.each(getdata, function(k, v){
      if(v.inprogress > 0){
       $(".dateid"+v.date).append('<div class="count-round inprogress cur-none" data-toggle="tooltip" data-original-title="'+v.inprogress+' Inprogress Compliances"></div>');
      }
      if(v.duedate > 0){
       $(".dateid"+v.date).append('<div class="count-round due-date cur-none" data-toggle="tooltip" data-original-title="'+v.duedate+' Unassigned Compliances"></div>');
      }
      if(v.upcoming > 0){
       $(".dateid"+v.date).append('<div class="count-round upcomming cur-none" data-toggle="tooltip" data-original-title="'+v.upcoming+' Upcoming Compliances"></div>');
      }
      if(v.overdue > 0){
        $(".dateid"+v.date).append('<div class="count-round over-due cur-none" data-toggle="tooltip" data-original-title="'+v.overdue+' Not Complied"></div>');
      }
  });   
  $('.cal-legalentity').on('change', function(){
    var cal_le_ids = parseInt($(this).val());
    var settings = widgetSettings();
    settings[8]([cal_le_ids], function(error1, data1){
      if(error1 == null){
        loadcalenderView(data1, 8);        
      }
      else{
        console.log(error1);
      }
    });
  });  
}

function widgetLoadChart() {
  return {
      1: loadComplianceStatusChart,
      2: loadEscalationChart,
      3: loadNotCompliedChart,
      4: loadTrendChart,
      5: loadComplianceApplicabilityChart,
      6: userScoreCard,
      7: domainScoreCard,
      8: calenderView
  }
}

function widgetSettings(){
    return {
      1: client_mirror.getWidgetComplianceChart,
      2: client_mirror.getWidgetEscalationChart,
      3: client_mirror.getWidgetNotCompliedChart,
      4: client_mirror.getWidgetTrendChart,
      5: client_mirror.getWidgetRiskChart,
      6: client_mirror.getWidgetUserScoreCard,
      7: client_mirror.getWidgetDomainScoreCard,
      8: client_mirror.getWidgetCalender
    }
}

function charticon(){
    return {
      1: "zmdi-chart",
      2: "zmdi-chart",
      3: "zmdi-chart",
      4: "zmdi-chart",
      5: "zmdi-chart",
      6: "zmdi-layers",
      7: "zmdi-layers",
      8: "zmdi-calendar"
    }
}

function charturl(){
    return {
      1: "/dashboard",
      2: "/dashboard",
      3: "/dashboard",
      4: "/dashboard",
      5: "/dashboard",
      6: "/work-flow-score-card",
      7: "/domain-score-card",
      8: getFormUrl()
    }
}

function getFormUrl(){
    var url = '';
    navBarItems = client_mirror.getUserMenu();    
    var menus = null;
    menus = [
        'Master',
        'Transaction',
        'Report',
        'My Accounts'
    ];    
    for (var i = 0; i < menus.length; i++) {
      var key = menus[i];
      var forms = navBarItems[key];
      for (var form in forms) {       
        if(forms[form].form_id == 35){
          url = forms[form].form_url;
        }
      }
    }
    return url;
}


function loadChart(){  
  $.each(widget_list, function(k,v){
    var sidebarli = $("#templates .ul-sidebarmenu ul");
    var liclone = sidebarli.clone();
    $(".menu_widgets a span", liclone).text(v.w_name);
    $(".menu_widgets i", liclone).addClass(charticon()[v.w_id]);
    $(".menu_widgets a", liclone).attr("data-target", "#item"+v.w_id);
    if(v.active_status = true){
      $(".menu_widgets", liclone).removeClass("active_widgets");
    }
    $(".menu_widgets", liclone).click(function(e){
      $(".page-title").show();
      $(".welcome-title").hide();

        var flag = 0;
        $(".dragdrophandles li").each(function(){
          if($(this).attr("id") == v.w_id){
            flag = 1;
          }
        });
        if(flag == 0){
          // var width = $(this).css('width');
          // var height = $(this).css('height');
          var width = "0px";
          var height = "0px";
          var id = v.w_id;
          var pin_status = true;
          widget_info.push(client_mirror.saveUserWidgetDataDict(id, width, height, pin_status));
          client_mirror.saveUserWidgetData(widget_info, function(error, response){
            if(error == null){
              $(".dragbox .pins i").addClass("ti-pin-alt");
              $(".dragbox .pins i").removeClass("ti-pin2");
              // $(".dragbox .pins i").prop("title", "pinned");
              $(".dragbox .pins i").attr("data-original-title", "Pinned");

              var settings = widgetSettings();
              var cardbox = $(".chart-card-box li");
              var cardboxclone = cardbox.clone();
              cardboxclone.attr("id", v.w_id);
              $(".chart-title", cardboxclone).html(SIDEBAR_MAP[v.w_id]);
              $(".chart-title", cardboxclone).attr("href", charturl()[v.w_id]);
              $(".chart-title", cardboxclone).on("click", function(){
                window.sessionStorage.widget_to_dashboard_href = SIDEBAR_MAP[v.w_id];
              });
              $(".dragbox", cardboxclone).attr("id", "item"+v.w_id);
              $(".dragbox-content div", cardboxclone).attr("id", "cardbox"+v.w_id);
              cardboxclone.addClass("resizable"+v.w_id);

              $(".dragbox .pins .ti-pin-alt", cardboxclone).click(function(e){
                var status_check = 0;
                var widget_info = [];
                $(".dragdrophandles li").each(function(i, v){
                    var itemiddiv = $(this).find('div');
                    var getitem = itemiddiv.attr("id");
                    var getsplit = getitem.split("item");
                    var itemid = getsplit[1];

                    var width = $(this).css('width');
                    var height = $(this).css('height');
                    var id = itemid;
                    var pin_status = true;
                    widget_info.push(client_mirror.saveUserWidgetDataDict(parseInt(id), width, height, pin_status));
                    status_check++;
                });
                if(status_check != 0){
                  client_mirror.saveUserWidgetData(widget_info, function(error, response){
                    if(error == null){
                      // displaySuccessMessage(message.save_success);
                      $(".dragbox .pins i").addClass("ti-pin-alt");
                      $(".dragbox .pins i").removeClass("ti-pin2");
                      // $(".dragbox .pins i").prop("title", "pinned");
                      $(".dragbox .pins i").attr("data-original-title", "Pinned");
                    }else{
                      displayMessage(error);
                    }
                  });
                }
              });

              $(".closewidget", cardboxclone).click(function(e){
                var divitem = $(this).parent().parent();
                var getitem = divitem.attr('id');
                var getsplit = getitem.split("item");
                var itemid = getsplit[1];

                widget_info = $.grep(widget_info, function(e){
                  return e.w_id != itemid;
                });
                $(this).parent().parent().parent().remove();

                client_mirror.saveUserWidgetData(widget_info, function(error, response){
                  if(error == null){
                    $(".dragbox .pins i").addClass("ti-pin-alt");
                    $(".dragbox .pins i").removeClass("ti-pin2");
                    // $(".dragbox .pins i").prop("title", "pinned");
                    $(".dragbox .pins i").attr("data-original-title", "Pinned");

                    // displaySuccessMessage(message.save_success);
                  }else{
                    displayMessage(error);
                  }
                });
              });
              $('a.maxmin', cardboxclone).click(function() {
                if($(this).find("i").attr("class") == "zmdi zmdi-window-minimize"){
                  $(this).find("i").removeClass("zmdi zmdi-window-minimize");
                  $(this).find("i").addClass("zmdi zmdi-window-maximize");
                  $(this).find("i").attr("data-original-title", "Maximize");
                }else{
                  $(this).find("i").removeClass("zmdi zmdi-window-maximize");
                  $(this).find("i").addClass("zmdi zmdi-window-minimize");
                  $(this).find("i").attr("data-original-title", "Minimize");
                }
                $(this).parent().siblings('.dragbox-content').toggle();
              });
              $('.dragdrophandles', cardboxclone).sortable({
                handle: 'h2'
              });

              $(".dragdrophandles").append(cardboxclone);
              settings[v.w_id](getLE_ids(), function(error1, data1){
                if(error1 == null){
                  widgetLoadChart()[v.w_id](data1, v.w_id);
                }
                else{
                  console.log(error1);
                }
              });
              // displaySuccessMessage(message.save_success);
              // $(".dragbox .pins i", cardboxclone).removeClass();
              // $(".dragbox .pins i", cardboxclone).addClass("ti-pin-alt")
              // $(".dragbox .pins i", cardboxclone).prop("title", "Click to save");
            }else{
              displayMessage(error);
            }
          });
          
        }
    });

    
    SIDEBAR_MAP[v.w_id] = v.w_name;
    $("#sidebar-menu").append(liclone);
    // $(".dragdrophandles .resizable").resizable({
    //     autoHide: true,
    //     resize: function() {
    //       chart.setSize(
    //           this.offsetWidth - 40,
    //           this.offsetHeight - 50,
    //           false
    //       );
    //     }
    // });
  });
  if(widget_info.length == 0){
    var user = client_mirror.getUserInfo();
    $(".welcome-title h4").html("Welcome "+ user.emp_name +"!")
    $(".page-title").hide();
  }else{
    $(".page-title").show();
    $(".welcome-title").hide();
    $.each(widget_info, function(k,v){
      var status_check = 0;
      settings = widgetSettings();
      var cardbox = $(".chart-card-box li");
      var cardboxclone = cardbox.clone();
      cardboxclone.attr("id", v.w_id);
      if(v.width != "0px"){
        cardboxclone.css("width", v.width);
        cardboxclone.css("height", v.height);
      }
      $(".chart-title", cardboxclone).html(SIDEBAR_MAP[v.w_id]);
      $(".chart-title", cardboxclone).attr("href", charturl()[v.w_id]);
      $(".chart-title", cardboxclone).on("click", function(){
        window.sessionStorage.widget_to_dashboard_href = SIDEBAR_MAP[v.w_id];
      });
      $(".dragbox", cardboxclone).attr("id", "item"+v.w_id);
      $(".dragbox-content div", cardboxclone).attr("id", "cardbox"+v.w_id);
      //
      $(".dragbox .pins .ti-pin-alt", cardboxclone).click(function(e){
        var widget_info = [];
        $(".dragdrophandles li").each(function(i, v){
            var itemiddiv = $(this).find('div');
            var getitem = itemiddiv.attr("id");
            var getsplit = getitem.split("item");
            var itemid = getsplit[1];

            var width = $(this).css('width');
            var height = $(this).css('height');
            var id = itemid;
            var pin_status = true;
            widget_info.push(client_mirror.saveUserWidgetDataDict(parseInt(id), width, height, pin_status));
            status_check++;
        });
        if(status_check != 0){
          client_mirror.saveUserWidgetData(widget_info, function(error, response){
            if(error == null){
              // displaySuccessMessage(message.save_success);
              $(".dragbox .pins i").addClass("ti-pin-alt");
              $(".dragbox .pins i").removeClass("ti-pin2");
              // $(".dragbox .pins i").prop("title", "pinned");
              $(".dragbox .pins i").attr("data-original-title", "Pinned");

            }else{
              displayMessage(error);
            }
          });
        }
      });
      //Close Widget
      $(".closewidget", cardboxclone).click(function(e){
        var divitem = $(this).parent().parent();
        var getitem = divitem.attr('id');
        var getsplit = getitem.split("item");
        var itemid = getsplit[1];

        widget_info = $.grep(widget_info, function(e){
          return e.w_id != itemid;
        });
        $(this).parent().parent().parent().remove();

        client_mirror.saveUserWidgetData(widget_info, function(error, response){
          if(error == null){
            $(".dragbox .pins i").addClass("ti-pin2");
              $(".dragbox .pins i").removeClass("ti-pin-alt");
              //$(".dragbox .pins i").prop("title", "Click to save");
              $(".dragbox .pins i").attr("data-original-title", "Click to save");
            // displaySuccessMessage(message.save_success);
          }else{
            displayMessage(error);
          }
        });

      });
      cardboxclone.addClass("resizable"+v.w_id);

      $('.toggleWidget', cardboxclone).click(function(e) {
        e.preventDefault();
        $($(this).data('target')).css({
            "display": "block"
        });
        if ($(this).parent().hasClass("active_widgets") == false)
          $(this).parent().addClass('active_widgets');
      });

      // $('.closewidget', cardboxclone).click(function(e) {
      //   e.preventDefault();
      //   var item = $(this).parent().parent();
      //   var list = "#" + item.attr('id');
      //   item.css({
      //       "display": "none"
      //   });

      //   $(".has_sub", cardboxclone).each(function(index) {
      //     if ($(this).find('a').attr('data-target') === list) {
      //         if ($(this).hasClass("active_widgets") == true)
      //             $(this).removeClass('active_widgets');
      //     }
      //   });
      // });
      $('a.maxmin', cardboxclone).click(function() {
        if($(this).find("i").attr("class") == "zmdi zmdi-window-minimize"){
          $(this).find("i").removeClass("zmdi zmdi-window-minimize");
          $(this).find("i").addClass("zmdi zmdi-window-maximize");
          $(this).find("i").attr("data-original-title", "Maximize");
        }else{
          $(this).find("i").removeClass("zmdi zmdi-window-maximize");
          $(this).find("i").addClass("zmdi zmdi-window-minimize");
          $(this).find("i").attr("data-original-title", "Minimize");
        }
        $(this).parent().siblings('.dragbox-content').toggle();
      });

      $('a.delete', cardboxclone).click(
          function() {
              var sel = confirm('do you want to delete the widget?');
              if (sel) {
                  //del code here
              }
          }
      );

      $(".dragdrophandles").append(cardboxclone);

      settings[v.w_id](getLE_ids(), function(error, data){
        if(error == null){
          widgetLoadChart()[v.w_id](data, v.w_id);
        }
        else{
          console.log(error);
        }
      });
    });
    // $(".dragdrophandles .resizable").resizable({
    //     autoHide: true
    // });
  }
  $('.dragdrophandles').sortable({
      handle: 'h2'
  });
}

function loadSidebarMenu(){
  client_mirror.getUserWidgetData(function (error, data) {
    if(error == null){
        widget_info = data.widget_info;
        widget_list = data.widget_list;
        loadChart();
    }
    else{
      console.log(error);
    }
  });
}

$(document).ready(function () {
  delete window.sessionStorage.widget_to_dashboard_href;
  hideLoader();
  loadSidebarMenu();
  $('.dragdrophandles').sortable({
      handle: 'h2'
  });
});
