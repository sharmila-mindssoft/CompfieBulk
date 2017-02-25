var PageTitle = $('.page-title');
var widget_info;
var widget_list;
var SIDEBAR_MAP = {};
var WIDGET_INFO_ID = [];
//
// Compliance status
//
function updateComplianceStatusStackBarChart(data, id) {  
  var xAxisName = data['xaxis_name'];
  var xAxis = data['xaxis'];
  var chartDataSeries = data['widget_data'];
  var chartTitle = data['chart_title'];
  //var drilldownSeries = data[4];
  var yAxisname = [
    'Complied',
    'Delayed Compliance',
    'Inprogress',
    'Not Complied'
  ];
  var highchart;
  highchart = new Highcharts.Chart({
    chart: {
      renderTo: 'cardbox'+id,
      type: 'bar'
    },
    title: { text: chartTitle },
    credits: { enabled: false },
    xAxis: {
      categories: xAxis,
      title: { text: xAxisName },
      labels: {
        style: {
          cursor: 'pointer',
          color: 'blue',
          textDecoration: 'underline'
        },
        useHTML: true,
        formatter: function () {
          return '<div id="label_' + this.value + '">' + this.value + '</div>';
        }
      },
      tooltip: { pointFormat: 'sfosdfksdfjds' }
    },
    yAxis: {
      min: 0,
      title: { text: 'Total compliances' },
      allowDecimals: false,
      reversedStacks: false
    },
    tooltip: {
      headerFormat: '<b>{point.series.name}</b>: {point.percentage:.0f}% ',
      pointFormat: '({point.y} out of {point.stackTotal})'
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
      '#A5D17A',
      '#F58835',
      '#F0F468',
      '#F32D2B'
    ],
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
}
//
// Escalation chart
//
function updateEscalationChart(data, id) {  
  xAxis = data['xaxis'];
  chartDataSeries = data['widget_data'];
  chartTitle = data['chart_title'];
  highchart = new Highcharts.Chart({
    colors: [
      '#F58835',
      '#F32D2B'
    ],
    chart: {
      type: 'column',
      renderTo: 'cardbox'+id
    },
    title: { text: chartTitle },
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
    plotOptions: {
      series: {
        pointWidth: 40,
        groupPadding: 0.4,
        pointPadding: -0,
        pointPlacement: -0
      },
      column: {
        dataLabels: {
          enabled: true,
          textShadow: null,
          format: '{point.y}'
        }
      }
    },
    series: chartDataSeries
  });
  // $('.highcharts-axis-labels text, .highcharts-axis-labels span').click(function () {
  //   var year = this.textContent || this.innerText;
  //   loadEscalationDrillDown(year);  // setChart(value);
  // });
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
  highchart = new Highcharts.Chart({
    colors: [
      '#FF9C80',
      '#F2746B',
      '#FB4739',
      '#DD070C'
    ],
    chart: {
      renderTo: 'cardbox'+id,
      type: 'pie',
      options3d: {
        enabled: true,
        alpha: 55
      }
    },
    title: { text: chartTitle },
    xAxis: { categories: true },
    credits: { enabled: false },
    tooltip: {
      headerFormat: '',
      pointFormat: '<span>{point.name} days</span>: <b>{point.y:.0f}</b> out of ' + total
    },
    legend: { enabled: true },
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
      }]
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
  var highchart;
  highchart = new Highcharts.Chart({
    chart: { renderTo: 'cardbox'+id },
    title: { text: chartTitle },
    credits: { enabled: false },
    xAxis: {
      categories: xAxis,
      title: { text: 'Year' },
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
}
//
// Compliance applicability status
//
function updateComplianceApplicabilityChart(data, id) {
  //data = prepareComplianceApplicability(data);
  chartTitle = data['chart_title'];
  chartDataSeries = data['widget_data'];
  total = data[2];
  highchart = new Highcharts.Chart({
    colors: [
      '#66FF66',
      '#FFDC52',
      '#CE253C'
    ],
    chart: {
      type: 'pie',
      renderTo: 'cardbox'+id,
      options3d: {
        enabled: true,
        alpha: 55
      }
    },
    title: { text: chartTitle },
    xAxis: { categories: true },
    credits: { enabled: false },
    tooltip: {
      headerFormat: '',
      pointFormat: '<span>{point.name}</span>: <b>{point.y:.0f}</b> out of ' + total
    },
    legend: { enabled: true },
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
      }]
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
  var usc = $("#templates .user-score-card-templates .table");
  var uscclone = usc.clone();  
  $("#cardbox"+id).append(uscclone);

  var usc_tr = $("#templates .user-score-card-templates .usc-tr");
  var uscclone_tr = usc_tr.clone();  
  $(".usc-role").html();
  $(".usc-assignee").html();
  $(".usc-concur").html();
  $(".usc-approve").html();
  $("#cardbox"+id+" .tbody-usc").append(uscclone_tr);
}

function domainScoreCard(data, id){
  var total_assigned = 0;
  var total_unassigned = 0;
  var total_notopted = 0;
  var total_subtotal = 0;
  var grandtotal = 0;
  var dsc = $("#templates .domain-score-card-templates .table");
  var dscclone = dsc.clone();  
  $("#cardbox"+id).append(dscclone);

  var dsc_tr = $("#templates .domain-score-card-templates .dsc-tr");
  var dscclone_tr = dsc_tr.clone();  
  $(".dsc-domain").html();
  $(".dsc-assigned").html();
  $(".dsc-unassigned").html();
  $(".dsc-notopted").html();
  total_subtotal = total_subtotal;
  $(".dsc-subtotal").html(total_subtotal);
  grandtotal = grandtotal+total_subtotal;
  $("#cardbox"+id+" .tbody-dsc").append(dscclone_tr);

  var dsc_total = $("#templates .domain-score-card-templates .dsc-tr");
  var dscclone_total = dsc_total.clone(); 
  $(".dsc-total-assigned").html(total_assigned);
  $(".dsc-total-unassigned").html(total_unassigned);
  $(".dsc-total-notopted").html(total_notopted);
  $(".dsc-grandtotal").html(grandtotal);
  $("#cardbox"+id+" .tbody-dsc").append(dscclone_total);


}

function calenderView(data, id){
  var ct = $("#templates .calender-templates div");
  var ctclone = ct.clone();  
  $('#mycalendar', ctclone).monthly({
      mode: 'event',
      //jsonUrl: 'events.json',
      //dataType: 'json'
      //xmlUrl: 'events.xml'
    });
  $("#cardbox"+id).append(ctclone);

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
      6: client_mirror.getUserScoreCard,
      7: client_mirror.getDomainScoreCard,
      8: client_mirror.getCalenderView
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
        if($.inArray(v.w_id, WIDGET_INFO_ID) == -1){
          console.log("welcome to widget_info");
          var width = $(this).css('width');
          var height = $(this).css('height');
          var id = v.w_id;
          var pin_status = true;
          widget_info.push(client_mirror.saveUserWidgetDataDict(id, width, height, pin_status));
          client_mirror.saveUserWidgetData(widget_info, function(error, response){
            if(error == null){
              var settings = widgetSettings();
              var cardbox = $(".chart-card-box li");
              var cardboxclone = cardbox.clone();
              $(".chart-title", cardboxclone).html(SIDEBAR_MAP[v.w_id]);
              $(".dragbox", cardboxclone).attr("id", "item"+v.w_id);
              $(".dragbox-content div", cardboxclone).attr("id", "cardbox"+v.w_id);
              cardboxclone.addClass("resizable"+v.w_id); 
              $(".dragdrophandles").append(cardboxclone);
              settings[v.w_id](function(error1, data1){
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
              // $(".dragbox .pins i", cardboxclone).attr("title", "unpin")
            }else{
              displayMessage(error);
            }
          });
          WIDGET_INFO_ID.push(v.w_id);
        }        
    });
    SIDEBAR_MAP[v.w_id] = v.w_name;
    $("#sidebar-menu").append(liclone);

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
      $(".chart-title", cardboxclone).html(SIDEBAR_MAP[v.w_id]);
      $(".dragbox", cardboxclone).attr("id", "item"+v.w_id);
      $(".dragbox-content div", cardboxclone).attr("id", "cardbox"+v.w_id);
      $(".dragbox .pins .ti-pin2", cardboxclone).click(function(e){
        var widget_info_save = [];
        $.each(".dragdrophandles li", function(i, v){
          if(v.w_id != 100 ){
            var width = $(this).css('width');
            var height = $(this).css('height');
            var id = v.w_id;
            var pin_status = true;
            widget_info.push(client_mirror.saveUserWidgetDataDict(id, width, height, pin_status));
            status_check++;
          }
        });
        if(status_check != 0){
          client_mirror.saveUserWidgetData(widget_info, function(error, response){
            if(error == null){
              displaySuccessMessage(message.save_success);
              $(".dragbox .pins i", cardboxclone).removeClass();
              $(".dragbox .pins i", cardboxclone).addClass("ti-pin-alt")
              $(".dragbox .pins i", cardboxclone).attr("title", "unpin")

            }else{
              displayMessage(error);
            }
          });
        }
        
      });
      $(".closewidget", cardboxclone).click(function(e){
        var divitem = $(this).parent().parent();
        console.log(divitem);
        var getitem = divitem.attr('id');
        var getsplit = getitem.split("item");
        var itemid = getsplit[1];
        //$(this).parent().parent().parent().remove();

      });
      cardboxclone.addClass("resizable"+v.w_id); 
      $(".resizable"+v.w_id, cardboxclone).resizable({
        autoHide: true
      });    
      $('.toggleWidget', cardboxclone).click(function(e) {
        e.preventDefault();
        console.log($(this).data('target'));
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

      settings[v.w_id](function(error, data){
        if(error == null){
          widgetLoadChart()[v.w_id](data, v.w_id);  
        }
        else{
          console.log(error);
        }      
      });
    });
  }
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
  hideLoader();
  loadSidebarMenu();
  $('.dragdrophandles').sortable({
      handle: 'h2'
  });

});