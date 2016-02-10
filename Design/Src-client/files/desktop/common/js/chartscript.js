function chartScript() {
	$("#radio6").prop('checked', true);
       $("#domainradio").prop('checked', true);
      $("#year-para").hide();
      $(".dropdown-box-container").click(function() {
        $(".filter-dropdown-container").slideToggle();
      })
      window.testSelAll2 = $('.testSelAll2').SumoSelect({selectAll:false });
      $("#entity-auto").hide();
      $("#division-auto").hide();
      $("#unit-auto").hide();	

      $(".textboxdomain").show();
            $(".textboxgroup").hide();
            $(".textboxcompany").hide();
            $(".textboxdivision").hide();
            $(".textboxbranch").hide();
            $(".textboxbusiness").hide();
            $(".textboxdate").show();
            $("#previousyear").show();
            $("#nextyear").show();

            $("#radio1").click(function () {
               //$(".textboxdomain").show();
                $(".textboxgroup").hide();
                $(".textboxcompany").hide();
                $(".textboxdivision").hide();
                $(".textboxbranch").hide();
                $(".textboxbusiness").hide();
              //  $(".textboxdate").show();
                $("#previousyear").show();
                $("#nextyear").show();
               // $("#radio6").prop('checked', true);
            });
           $("#radio2").click(function () {
             //$(".textboxdomain").show();
                $(".textboxgroup").hide();
                $(".textboxcompany").show();
                $(".textboxdivision").hide();
                $(".textboxbranch").hide();
                $(".textboxbusiness").hide();
               // $(".textboxdate").show();
                $("#previousyear").show();
                $("#nextyear").show();
               // $("#radio6").prop('checked', true);
            });
           $("#radio3").click(function () {
            // $(".textboxdomain").show();
                $(".textboxgroup").hide();
                $(".textboxcompany").hide();
                $(".textboxdivision").show();
                $(".textboxbranch").hide();
                $(".textboxbusiness").hide();
              //  $(".textboxdate").show();
                $("#previousyear").show();
                $("#nextyear").show();
              //  $("#radio6").prop('checked', true);
            });
           $("#radio4").click(function () {
           //  $(".textboxdomain").show();
                $(".textboxgroup").hide();
              //  $(".textboxdate").show();
                $(".textboxcompany").hide();
                $(".textboxdivision").hide();
                $(".textboxbranch").show();
                $(".textboxbusiness").hide();
                $("#previousyear").show();
                $("#nextyear").show();
                // $("#radio6").prop('checked', true);
            });
           $("#radio5").click(function () {
             //$(".textboxdomain").show();
                $(".textboxgroup").hide();
                $(".textboxcompany").hide();
                $(".textboxdivision").hide();
                $(".textboxbranch").hide();
                $(".textboxbusiness").show();
              //  $(".textboxdate").show();
                $("#previousyear").show();
                $("#nextyear").show();
              //  $("#radio6").prop('checked', true);
            });
           $("#radioConsolidated").click(function () {
             //$(".textboxdomain").show();
                $(".textboxgroup").hide();
                $(".textboxcompany").hide();
                $(".textboxdivision").hide();
                $(".textboxbranch").hide();
                $(".textboxbusiness").hide();
              //  $(".textboxdate").show();
                $("#previousyear").hide();
                $("#nextyear").hide();
              //  $("#radio6").prop('checked', true);
              loadConsolidated();
            });
           
           // $("#radio6").click(function () {
           //    $(".textboxdomain").show();
           //    $(".textboxdate").show();
           //    $("#previousyear").hide();
           //    $("#nextyear").hide();
           //  });
          $('#radio6').click(function() {
             if( $(".textboxdate").is(":hidden") ) {
              $(".textboxdate").show();
               $("#radio6").prop('checked', true);
             }
             else
             {
              $(".textboxdate").hide();
               $("#radio6").prop('checked', false);
             }
             });
           $('#domainradio').click(function() {
             if( $(".textboxdomain").is(":hidden") ) {
               $(".textboxdomain").show();
               $("#domainradio").prop('checked', true);
             }
             else
             {
               $(".textboxdomain").hide();
               $("#domainradio").prop('checked', false);
             }
             });
           $('#countryradio').click(function() {
             if( $(".textboxcountry").is(":hidden") ) {
               $(".textboxcountry").show();
               $("#countryradio").prop('checked', true);
             }
             else
             {
               $(".textboxcountry").hide();
               $("#countryradio").prop('checked', false);
             }
             });

           loadGroup();
      $("#viewaspie").hide();

      $("#previous").click(function() {
            if($("#radio1").is(':checked')){
            }else if($("#radio2").is(':checked')){
              loadCompany();
            }else if($("#radio3").is(':checked')){
              loadDivision();
            }else if($("#radio4").is(':checked')){
              loadUnit();
            }
       })

      $("#next").click(function() {
            if($("#radio1").is(':checked')){

            }else if($("#radio2").is(':checked')){
              loadCompanyNext();
            }else if($("#radio3").is(':checked')){
              loadDivisionNext();
            }else if($("#radio4").is(':checked')){
              loadUnitNext();
            }
       })

      $("#previousyear").click(function() {
            if($("#radio1").is(':checked')){
              loadGroup();
            }else if($("#radio2").is(':checked')){
              loadCompany();
            }else if($("#radio3").is(':checked')){
              loadDivision();
            }else if($("#radio4").is(':checked')){
              loadUnit();
            }else if($("#radio5").is(':checked')){
              loadBusinessGroup();
            }
       })

      $("#nextyear").click(function() {
            if($("#radio1").is(':checked')){
              loadGroup();
            }else if($("#radio2").is(':checked')){
              loadCompany();
            }else if($("#radio3").is(':checked')){
              loadDivision();
            }else if($("#radio4").is(':checked')){
              loadUnit();
            }else if($("#radio5").is(':checked')){
              loadBusinessGroup();
            }
       })

      $("#viewaspie").click(function() {
              if($("#radio1").is(':checked')){
      				loadCountrySpecific();
      			}else if($("#radio2").is(':checked')){
      				loadCompanySingleSelectionPie();
      			}else if($("#radio3").is(':checked')){
      				loadCompanySingleSelectionPie();
      			}else if($("#radio4").is(':checked')){
      				loadCompanySingleSelectionPie();
      			}
       })

      $("#viewasbar").click(function() {
              if($("#radio1").is(':checked')){
      				loadCountrySpecificBar();
      			}else if($("#radio2").is(':checked')){
      				loadCompanySingleSelection($("#hidden").val());
      			}else if($("#radio3").is(':checked')){
      				loadCompanySingleSelection($("#hidden").val());
      			}else if($("#radio4").is(':checked')){
      				loadCompanySingleSelection($("#hidden").val());
      			}
           
       })

      $("#back").click(function() {
              $("#next").show();
              $("#previous").show();
           		if($("#radio1").is(':checked')){
                  var value = $("#hidden").val();
                  if(value == "singlepie"){
                    loadCountrySpecific();
                  }else if(value == "singlebar"){
                    loadCountrySpecificBar();
                  }else{
          				  loadGroup();
                  }
          			}else if($("#radio2").is(':checked')){
          				loadCompany();
          			}else if($("#radio3").is(':checked')){
          				loadDivision();
          			}else if($("#radio4").is(':checked')){
          				loadUnit();
          			}
       })

      $("#go-le").click(function() {
              loadCompany();
       })

      $("#go-d").click(function() {
              loadDivision();
       })

      $("#go-u").click(function() {
              loadUnit();
       })

      $("#go-date").click(function() {
              if($("#radio1").is(':checked')){
                  loadGroup();
                }else if($("#radio2").is(':checked')){
                  loadCompany();
                }else if($("#radio3").is(':checked')){
                  loadDivision();
                }else if($("#radio4").is(':checked')){
                  loadUnit();
                }
       })

      $("#go-co").click(function() {
        var values = $("#country").val();
        if(values.length == 1){
            loadCompanySingleSelection(values[0])
        }else{
              loadGroup();
        }
       })

      $("#radio1").click(function() {
              loadGroup();
       })

      $("#radio2").click(function() {
              loadCompany();
       })

      $("#radio3").click(function() {
              loadDivision();
       })

      $("#radio4").click(function() {
              loadUnit();
       })

      $("#radio5").click(function() {
              loadBusinessGroup();
       })

      $(".task-status-tab").click(function() {
        $("#year-para").hide();
      	$(".task-status-tab").addClass("active")
        //$(".actwise-tab").removeClass("active")
        $(".ageing-tab").removeClass("active")
        $(".compliance-tab").removeClass("active")
        $(".esc-tab").removeClass("active")
    		$(".usecom-tab").removeClass("active")
        $(".trend-tab").removeClass("active")
    		$(".graph-box").show();
    		$(".grid-table-dash").hide();
    		$(".grid-table-dash1").hide();
        $("#level-filter").fadeIn();
        $("#viewaspie").hide();
        $("#unit-auto").hide();
        $("#entity-auto").hide();
        $("#division-auto").hide();
        $(".SumoSelect").show();
        $("#next").show();
        $("#previous").show();
        loadGroup();
      })
    })

    function loadCompanySingleSelectionPie(){
    	$("#viewaspie").hide();
    	$("#viewasbar").show();
      $("#container").show();
      $("#imgcontainer").hide();
    	var name = $("#hidden").val();
    	$(function () {
            $('#container').highcharts({
       
       colors:['#A5D17A','#F58835','#F0F468','#F32D2B'],
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45,
                beta: 0
            }
        },
        title: {
            text: name
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.y}</b> <br>Total Compliances: 70'
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
                            click: function() {
                                var drilldown = this.drilldown;
                                $("#hidden").val("singlepie");
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
                        name:"Complied",
                        y:15,
                        drilldown:"Complied"
                      },{
                        name:"Delayed compliance",
                        y:15,
                        drilldown:"Delayed"
                      },{
                        name:"In progress",
                        y:18,
                        drilldown:"Inprogress"
                      },{
                        name:"Not complied",
                        y:22,
                        drilldown:"NotComplied"
                      },
                    ]
        }]
    });
        });
    }

    function loadCompanySingleSelection(name){
    	$(function () {
    		$("#viewaspie").show();
    		$("#viewasbar").hide();
    		$("#hidden").val(name);
        $("#container").show();
        $("#imgcontainer").hide();
		    $('#container').highcharts({
		    // colors:['#239e13','#a3d202','#faf216','#e70808'],
            colors:['#A5D17A','#F58835','#F0F468','#F32D2B',],
		        chart: {
		            type: 'column'
		        },
		        title: {
		            text: name
		        },
		        xAxis: {
		            type: 'category',
                title: {
                    text: 'Compliance Status'
                },
		        },
		        yAxis: {
		            title: {
		                text: 'Total Compliances'
		            },
                allowDecimals: false

		        },
		        legend: {
		            enabled: false
		        },
		        plotOptions: {
		        	column:{
                dataLabels: {
                        enabled: true,
                        style: {
                           textShadow:null,
                        },
                        /*format:'{point.percentage:.0f}%'*/
                        format:'{point.y}'
                    },
		        		point: {
                        events: {
                            click: function() {
                                var drilldown = this.drilldown;
                                $("#hidden").val("singlebar");
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
							
							formatter:function() {
							var dataSum = (5 + 2 + 8 + 3);
							var pcnt = (this.y / dataSum) * 100;
							return Highcharts.numberFormat(pcnt,0) + '%';
						}
		                    /*format: '{point.y:.0f}'*/
		                }
		            }
		        },

		        tooltip: {
                            headerFormat: '<b>{series.name}</b>:{point.percentage:.0f}%<br/>',
                            pointFormat: 'Total Compliances: 18'
		        },

		        series: [{
		            name: "Compliance - Group wise",
		            colorByPoint: true,
		            data: [{
		                name: "Complied",
		                y: 5,
		                drilldown:"Complied"
		            }, {
		                name: "Delayed compliance",
		                y: 2,
		                drilldown:"Delayed"
		            }, {
		                name: "In progress",
		                y: 8,
		                drilldown: "Inprogress"
		            }, {
		                name: "Not complied",
		                y: 3,
		                drilldown:"NotComplied"
		            }]
		        }],
		    });
		});
    }

    function loadCompanyNext(){
      $("#previous").show();
      $("#next").show();
      $("#container").show();
      $("#imgcontainer").hide();
      $(function () {  
        var inprogress_data = [10];
        var pending_data = [10];
        var completed_data = [10];
        var not_complied = [10];
              inprogress_data[0] = {name: 'KG Hospitals',y: 20,drilldown:"Inprogress"};
              pending_data[0] = {name: 'KG Hospitals',y: 20,drilldown:"Delayed"};
              completed_data[0] = {id:'fin',name: 'KG Hospitals',y: 10,drilldown:"Complied"};
              not_complied[0] = {name: 'KG Hospitals',y: 30,drilldown:"NotComplied"};

              inprogress_data[1] = {name: 'KG Bakeries',y: 12,};
              pending_data[1] = {name: 'KG Bakeries',y: 18,};
              completed_data[1] = {id:'fin',name: 'KG Bakeries',y: 27};
              not_complied[1] = {name:"KG Bakeries", y:13}

              inprogress_data[2] = {name: 'KG Hotels',y: 15};
              pending_data[2] = {name: 'KG Hotels',y: 25};
              completed_data[2] = {id:'fin',name: 'KG Hotels',y: 10};
              not_complied[2] = {name:"KG Hotels", y:10}
            
              inprogress_data[3] = {name: 'KG Schools',y: 10};
              pending_data[3] = {name: 'KG Schools',y: 24};
              completed_data[3] = {id:'fin',name: 'KG Schools',y: 24};
              not_complied[3] = {name:"KG Schools", y:17}
            
              inprogress_data[4] = {name: 'KG University',y: 24};
              pending_data[4] = {name: 'KG University',y: 23};
              completed_data[4] = {id:'fin',name: 'KG University',y: 31};
              not_complied[4] = {name:"KG Mobiles", y:13}
         

      $('#container').highcharts({
            // colors:['#239e13','#a3d202','#faf216','#e70808'],
            //colors:['#125900','#FF7700','#FFDA0F','#D10018'],
			colors:['#A5D17A','#F58835','#F0F468','#F32D2B',],
            chart: {
                type: 'bar',
                width:'850',
               
            },
            title: {
                text: 'Legal entity wise compliances'
            },
            xAxis: {
                categories: ['KG Hospitals','KG Bakeries','KG Hotels','KG Schools','KG University'],
                title: {
                    text: 'Legal entities'
                },
                labels: {
                              useHTML: true,
                              formatter: function() {
                                  var name=this.value;
                                  if(name == "KG Autoparts"){
                                    $("#hidden").val("KG Autoparts");
                                    var link = '<a href="#"  id="'+name+'" onclick=loadCompanySingleSelectionPie(this.id)>'+
                                        name +'</a>'
                                    return link;
                                  }else{
                                    var link = '<span  id="'+name+'" >'+
                                        name +'</span>'
                                    return link;
                                  }
                             }
                          },
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Total Compliances'
                },
                allowDecimals: false
            },
            legend: {
                reversed: true
            },
            tooltip: {
              headerFormat: '<b>{point.x}</b><br/>',
              pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
            },
            plotOptions: {
                series: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: true,
                        color:  '#000000',
                        style: {
                            /*textShadow: '0 0 3px black',*/
                            textShadow:null,
                        },
                        // format:'{point.percentage:.0f}%'
                        format:'{point.y}'
                    },
                    point: {
                                events: {
                                    click: function() {
                                        var drilldown = this.drilldown;
                                        if (drilldown) {
                                        loadDrillDownData(drilldown); 
                                        }
                                    }
                                  }
                                }
                },
            },
            series: [{
                    name: 'Complied',
                    data : completed_data
                }, {
                    name: 'Delayed compliance',
                        data : pending_data
                }, {
                    name: 'In progress',
                         data : inprogress_data
                }, {
                    name: 'Not complied',
                        data : not_complied
                }]
        });
      });
    }

    function loadCompany(){
      $("#previous").show();
      $("#next").show();
      $("#container").show();
      $("#imgcontainer").hide();
    	$(function () {  
    	  var inprogress_data = [10];
    	  var pending_data = [10];
    	  var completed_data = [10];
    	  var not_complied = [10];
    	  var values = $("#legal-entity").val();
    	  if(values.length > 1){
	    	  for(var i=0;i<7;i++){
	    	  	if (values[i] ==  "KG Transports"){
	    	  		inprogress_data[i] = {name: 'KG Transports',y: 24,drilldown:"EntityInprogress"};
	    	  		pending_data[i] = {name: 'KG Transports',y: 13,drilldown:"EntityDelayed"};
	    	  		completed_data[i] = {id:'fin',name: 'KG Transports',y: 18,drilldown:"EntityComplied"};
	    	  		not_complied[i] = {name: 'KG Transports',y: 22,drilldown:"NotComplied"};
	    	  	}else if(values[i] ==  "KG Autoparts"){
	    	  		inprogress_data[i] = {name: 'KG Autoparts',y: 15,};
	    	  		pending_data[i] = {name: 'KG Autoparts',y: 23,};
	    	  		completed_data[i] = {id:'fin',name: 'KG Autoparts',y: 12};
	    	  		not_complied[i] = {name:"KG Autoparts", y:18};
	    	  	}else if(values[i] ==  "KG Booking"){
	    	  		inprogress_data[i] = {name: 'KG Booking',y: 23};
	    	  		pending_data[i] = {name: 'KG Booking',y: 22};
	    	  		completed_data[i] = {id:'fin',name: 'KG Booking',y: 19};
	    	  		not_complied[i] = {name:"KG Booking", y:21};
	    	  	}else if(values[i] ==  "KG Electricals"){
	    	  		inprogress_data[i] = {name: 'KG Electricals',y: 23};
	    	  		pending_data[i] = {name: 'KG Electricals',y: 10};
	    	  		completed_data[i] = {id:'fin',name: 'KG Electricals',y: 18};
	    	  		not_complied[i] = {name:"KG Electricals", y:22};
	    	  	}else if(values[i] ==  "KG Mobiles"){
	    	  		inprogress_data[i] = {name: 'KG Mobiles',y: 24};
	    	  		pending_data[i] = {name: 'KG Mobiles',y: 24};
	    	  		completed_data[i] = {id:'fin',name: 'KG Mobiles',y: 13};
	    	  		not_complied[i] = {name:"KG Mobiles", y:21}
	    	  	}else if(values[i] ==  "KG HealthCare"){
				  inprogress_data[i] = {name: 'KG HealthCare',y: 20};
				  pending_data[i] = {name: 'KG HealthCare',y: 25};
				  completed_data[i] = {id:'fin',name: 'KG HealthCare',y: 22};
				  not_complied[i] = {name:"KG HealthCare", y:18};
				}else if(values[i] ==  "KG HR Services"){
				  inprogress_data[i] = {name: 'KG HR Services',y: 22};
				  pending_data[i] = {name: 'KG HR Services',y: 18};
				  completed_data[i] = {id:'fin',name: 'KG HR Services',y: 22};
				  not_complied[i] = {name:"KG HR Services", y:23}
				}
				else {
					continue;
					}
	    	  }
			  
	      }else if(values.length <=0){
	      	alert("Select atleast one legal entity to load chart");
	      }else{
	      	loadCompanySingleSelection(values[0]);
	      }

      $('#container').highcharts({
            // colors:['#239e13','#a3d202','#faf216','#e70808'],
            //colors:['#125900','#FF7700','#FFDA0F','#D10018'],
			colors:['#F32D2B','#F0F468','#F58835','#A5D17A',],
            chart: {
                type: 'bar',
                width:'850',
                
            },
            title: {
                text: 'Legal entity wise compliances'
            },
            xAxis: {
                categories: ['KG Transports', 'KG Autoparts', 'KG Booking', 'KG Electricals', 'KG Mobiles', 'KG HR Services', 'KG HealthCare'],
                endOnTick: true,
                title: {
                    text: 'Legal entities'
                },
                labels: {
                              useHTML: true,
                              formatter: function() {
                                  var name=this.value;
                                  if(name == "KG Booking"){
                                    $("#hidden").val("KG Booking");
                                    var link = '<a href="#"  id="'+name+'" onclick=loadCompanySingleSelectionPie(this.id)>'+
                                        name +'</a>'
                                    return link;
                                  }else{
                                    var link = '<span  id="'+name+'" >'+
                                        name +'</span>'
                                    return link;
                                  }
                             }
                          },
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Total Compliances'
                },
                  allowDecimals: false,
                  endOnTick: true,
            },
            legend: {
                reversed: true
            },
            tooltip: {
              // headerFormat: '<b>{point.x}</b><br/>',
              // pointFormat: '{series.name}: {point.y} out of Total: {point.stackTotal}'
              headerFormat: '<b>{point.x}</b><br/>',
              pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
            },
            plotOptions: {
                series: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: true,
                        color:  '#000000',
                        style: {
                            /*textShadow: '0 0 3px black',*/
                            textShadow:null,
                        },
                        // format:'{point.percentage:.0f}%'
                        format:'{point.y}'
                    },
                    point: {
                                events: {
                                    click: function() {
                                        var drilldown = this.drilldown;
                                        if (drilldown) {
                                        loadDrillDownData(drilldown); 
                                        }
                                    }
                                  }
                                }
                },
            },
            series: [{
                    name: 'Not complied',
                        data : not_complied
                }, {
                    name: 'In progress',
                         data : inprogress_data
                }, {
                    name: 'Delayed compliance',
                        data : pending_data
                }, {
                    name: 'Complied',
                    data : completed_data
                }]
        });
      });
    }

    function loadDivisionNext(){
      $("#previous").show();
      $("#next").show();
      $("#container").show();
      $("#imgcontainer").hide();
      $(function () {  
        var inprogress_data = [10];
        var pending_data = [10];
        var completed_data = [10];
        var not_complied = [10];
              inprogress_data[0] = {name: 'KG HR Unit',y: 30,drilldown:"Inprogress"};
              pending_data[0] = {name: 'KG HR Unit',y: 20,drilldown:"Delayed"};
              completed_data[0] = {id:'fin',name: 'KG HR Unit',y: 10,drilldown:"Complied"};
              not_complied[0] = {name: 'KG HR Unit',y: 20,drilldown:"NotComplied"};

              inprogress_data[1] = {name: 'KG Development',y: 21,};
              pending_data[1] = {name: 'KG Development',y: 29,};
              completed_data[1] = {id:'fin',name: 'KG Development',y: 16};
              not_complied[1] = {name:"KG Development", y:28}
         

      $('#container').highcharts({
            // colors:['#239e13','#a3d202','#faf216','#e70808'],
            //colors:['#125900','#FF7700','#FFDA0F','#D10018'],
			colors:['#F32D2B','#F0F468','#F58835','#A5D17A',],
            chart: {
                type: 'bar',
                width:'850',
              
            },
            title: {
                text: 'Division wise compliances'
            },
            xAxis: {
                categories: ['KG HR Unit','KG Development'],
                title: {
                    text: 'Division'
                },
                labels: {
                              useHTML: true,
                              formatter: function() {
                                  var name=this.value;
                                  if(name == "KG Security"){
                                    $("#hidden").val("KG Security");
                                    var link = '<a href="#"  id="'+name+'" onclick=loadCompanySingleSelectionPie(this.id)>'+
                                        name +'</a>'
                                    return link;
                                  }else{
                                    var link = '<span  id="'+name+'" >'+
                                        name +'</span>'
                                    return link;
                                  }
                             }
                          },
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Total Compliances'
                },
                allowDecimals: false
            },
            legend: {
                reversed: true
            },
            tooltip: {
              // headerFormat: '<b>{point.x}</b><br/>',
              // pointFormat: '{series.name}: {point.y} out of Total: {point.stackTotal}'
              headerFormat: '<b>{point.name}</b><br/>',
              pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
            },
            plotOptions: {
                series: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: true,
                        color:  '#000000',
                        style: {
                            /*textShadow: '0 0 3px black',*/
                            textShadow:null,
                        },
                        // format:'{point.percentage:.0f}%'
                        format:'{point.y}'
                    },
                    point: {
                                events: {
                                    click: function() {
                                        var drilldown = this.drilldown;
                                        if (drilldown) {
                                        loadDrillDownData(drilldown); 
                                        }
                                    }
                                  }
                                }
                },
            },
            series: [{
                    name: 'Complied',
                    data : completed_data
                }, {
                    name: 'Delayed compliance',
                        data : pending_data
                }, {
                    name: 'In progress',
                         data : inprogress_data
                }, {
                    name: 'Not complied',
                        data : not_complied
                }]
        });
      });
    }


    function loadDivision(){
      $("#previous").show();
      $("#next").show();
      $("#container").show();
      $("#imgcontainer").hide();
      $(function () { 
      	  var inprogress_data = [10];
    	  var pending_data = [10];
    	  var completed_data = [10];
    	  var not_complied = [10];
    	  var values = $("#division").val();
    	  if(values.length > 1){
	    	  for(var i=0;i<values.length;i++){
	    	  	if (values[i] ==  "KG Manufacturing"){
	    	  		inprogress_data[i] = {name: 'KG Manufacturing',y: 24,drilldown:"Inprogress"};
	    	  		pending_data[i] = {name: 'KG Manufacturing',y: 22,drilldown:"DivisionDelayed"};
	    	  		completed_data[i] = {id:'fin',name: 'KG Manufacturing',y: 25,drilldown:"DivisionComplied"};
	    	  		not_complied[i] = {name: 'KG Manufacturing',y: 23,drilldown:"NotComplied"};
	    	  	}else if(values[i] ==  "KG Quality Checking"){
	    	  		inprogress_data[i] = {name: 'KG Quality Checking',y: 18,};
	    	  		pending_data[i] = {name: 'KG Quality Checking',y: 15,};
	    	  		completed_data[i] = {id:'fin',name: 'KG Quality Checking',y: 23};
	    	  		not_complied[i] = {name:"KG Quality Checking", y:24}
	    	  	}else if(values[i] ==  "KG Sales"){
	    	  		inprogress_data[i] = {name: 'KG Sales',y: 25};
	    	  		pending_data[i] = {name: 'KG Sales',y: 13};
	    	  		completed_data[i] = {id:'fin',name: 'KG Sales',y: 26};
	    	  		not_complied[i] = {name:"KG Sales", y:14}
	    	  	}else if(values[i] ==  "KG Testing"){
	    	  		inprogress_data[i] = {name: 'KG Testing',y: 15};
	    	  		pending_data[i] = {name: 'KG Testing',y: 12};
	    	  		completed_data[i] = {id:'fin',name: 'KG Testing',y: 23};
	    	  		not_complied[i] = {name:"KG Testing", y:24}
	    	  	}else if(values[i] ==  "KG Administration"){
	    	  		inprogress_data[i] = {name: 'KG Administration',y: 22};
	    	  		pending_data[i] = {name: 'KG Administration',y: 36};
	    	  		completed_data[i] = {id:'fin',name: 'KG Administration',y: 13};
	    	  		not_complied[i] = {name:"KG Administration", y:14}
	    	  	}else if(values[i] ==  "KG Security"){
              inprogress_data[i] = {name: 'KG Security',y: 22};
              pending_data[i] = {name: 'KG Security',y: 26};
              completed_data[i] = {id:'fin',name: 'KG Security',y: 23};
              not_complied[i] = {name:"KG Security", y:14}
            }else if(values[i] ==  "KG Research"){
              inprogress_data[i] = {name: 'KG Research',y: 32};
              pending_data[i] = {name: 'KG Research',y: 16};
              completed_data[i] = {id:'fin',name: 'KG Research',y: 13};
              not_complied[i] = {name:"KG Research", y:14}
            }else{
              continue;
            }

	    	  }
	      }else if(values.length <=0){
	      	alert("Select atleast one division to load chart");
	      }else{
	      	loadCompanySingleSelection(values[0]);
	      }

        $('#container').highcharts({
        // colors:['#239e13','#a3d202','#faf216','#e70808'],
        //colors:['#125900','#FF7700','#FFDA0F','#D10018'],
		    colors:['#F32D2B','#F0F468','#F58835','#A5D17A'],
        chart: {
            type: 'bar',
            width:'850'
        },
        title: {
            text: 'Division wise compliances'
        },
        xAxis: {
            categories: ['KG Manufacturing', 'KG Sales', 'KG Quality Checking', 'KG Administration', 'KG Testing', 'KG Security', 'KG Research'],
            title: {
                text: 'Divisions'
            },
            labels: {
                          useHTML: true,
                          formatter: function() {
                              var name=this.value;
                              if(name == "KG Manufacturing"){
                                      $("#hidden").val("KG Manufacturing");
                                var link = '<a href="#"  id="'+name+'" onclick=loadCompanySingleSelectionPie(this.id)>'+
                                    name +'</a>'
                                return link;
                              }else{
                                var link = '<span  id="'+name+'" >'+
                                    name +'</span>'
                                return link;
                              }
                         }
                      },
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total Compliances'
            },
            allowDecimals: false
        },
        legend: {
            reversed: true
        },
        tooltip: {
              // headerFormat: '<b>{point.x}</b><br/>',
              // pointFormat: '{series.name}: {point.y} out of Total: {point.stackTotal}'
              headerFormat: '<b>{point.x}</b><br/>',
              pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
            },
        plotOptions: {
            series: {
                stacking: 'normal',
                dataLabels: {
                        enabled: true,
                        color:  '#000000',
                        style: {
                            /*textShadow: '0 0 3px black',*/
                            textShadow:null,
                        },
                        // format:'{point.percentage:.0f}%'
                        format:'{point.y}'
                    },
                point: {
                            events: {
                                click: function() {
                                    var drilldown = this.drilldown;
                                    if (drilldown) {
                                      loadDrillDownData(drilldown); 
                                    }
                                }
                              }
                            }
            },
        },
        series: [ {
                name: 'Not complied',
                    data :not_complied
            },
            {
                name: 'In progress',
                     data :inprogress_data
            }, {
                name: 'Delayed compliance',
                    data :pending_data
            }, 
            {
                name: 'Complied1',
                data : completed_data
            }]
    });
      });
    }

    function loadUnit(){
     $("#previous").show();
     $("#next").show();
     $("#container").show();
      $("#imgcontainer").hide();
     $(function () { 
     	  var inprogress_data = [10];
    	  var pending_data = [10];
    	  var completed_data = [10];
    	  var not_complied = [10];
    	  var values = $("#unit").val();
        if(values.length > 1){
	    	  for(var i=0;i<values.length;i++){

	    	  	if (values[i] ==  "Branch Office - 1"){
	    	  		inprogress_data[i] = {name: 'Branch Office - 1',y: 23,drilldown:"UnitInprogress"};
	    	  		pending_data[i] = {name: 'Branch Office - 1',y: 22,drilldown:"UnitDelayed"};
	    	  		completed_data[i] = {id:'fin',name: 'Branch Office - 1',y: 19,drilldown:"UnitComplied"};
	    	  		not_complied[i] = {name: 'Branch Office - 1',y: 31,drilldown:"UnitNotComplied"};
	    	  	}else if(values[i] ==  "Branch Office - 2"){
	    	  		inprogress_data[i] = {name: 'Branch Office - 2',y: 19,};
	    	  		pending_data[i] = {name: 'Branch Office - 2',y: 27,};
	    	  		completed_data[i] = {id:'fin',name: 'Branch Office - 2',y: 28};
	    	  		not_complied[i] = {name:"Branch Office - 2", y:15}
	    	  	}else if(values[i] ==  "Branch Office - 3"){
	    	  		inprogress_data[i] = {name: 'Branch Office - 3',y: 15};
	    	  		pending_data[i] = {name: 'Branch Office - 3',y: 23};
	    	  		completed_data[i] = {id:'fin',name: 'Branch Office - 3',y: 16};
	    	  		not_complied[i] = {name:"Branch Office - 3", y:23}
	    	  	}else if(values[i] ==  "Branch Office - 4"){
	    	  		inprogress_data[i] = {name: 'Branch Office - 4',y: 25};
	    	  		pending_data[i] = {name: 'Branch Office - 4',y: 32};
	    	  		completed_data[i] = {id:'fin',name: 'Branch Office - 4',y: 13};
	    	  		not_complied[i] = {name:"Branch Office - 4", y:24}
	    	  	}else if(values[i] ==  "Branch Office - 5"){
	    	  		inprogress_data[i] = {name: 'Branch Office - 5',y: 12};
	    	  		pending_data[i] = {name: 'Branch Office - 5',y: 26};
	    	  		completed_data[i] = {id:'fin',name: 'Branch Office - 5',y: 33};
	    	  		not_complied[i] = {name:"Branch Office - 5", y:14}
	    	  	}else if(values[i] ==  "Branch Office - 6"){
              inprogress_data[i] = {name: 'Branch Office - 6',y: 12};
              pending_data[i] = {name: 'Branch Office - 6',y: 26};
              completed_data[i] = {id:'fin',name: 'Branch Office - 6',y: 13};
              not_complied[i] = {name:"Branch Office - 6", y:24}
            }else if(values[i] ==  "Branch Office - 7"){
              inprogress_data[i] = {name: 'Branch Office - 7',y: 32};
              pending_data[i] = {name: 'Branch Office - 7',y: 16};
              completed_data[i] = {id:'fin',name: 'Branch Office - 7',y: 23};
              not_complied[i] = {name:"Branch Office - 7", y:24}
            }
	    	  }
	      }else if(values.length <=0){
	      	alert("Select atleast one unit to load chart");
	      }else{
	      	loadCompanySingleSelection(values[0]);
	      }  
          $('#container').highcharts({
        // colors:['#239e13','#a3d202','#faf216','#e70808'],
        //colors:['#125900','#FF7700','#FFDA0F','#D10018'],
		    colors:['#F32D2B','#F0F468','#F58835','#A5D17A',],
        chart: {
            type: 'bar',
            width:'850',
        },
        title: {
            text: 'Unit wise compliances'
        },
        xAxis: {
            categories: ['Branch Office - 1', 'Branch Office - 2', 'Branch Office - 3', 'Branch Office - 4', 'Branch Office - 5','Branch Office - 6','Branch Office - 7'],
            title: {
                text: 'Units'
            },
            labels: {
                          useHTML: true,
                          formatter: function() {
                              var name=this.value;
                              if(name == "Branch Office - 1"){
                                      $("#hidden").val("Branch Office - 1");
                                var link = '<a href="#"  id="'+name+'" onclick=loadCompanySingleSelectionPie(this.id)>'+
                                    name +'</a>'
                                return link;
                              }else{
                                var link = '<span  id="'+name+'" >'+
                                    name +'</span>'
                                return link;
                              }
                         }
                      },
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total Compliances'
            },
            allowDecimals: false
        },
        legend: {
            reversed: true
        },
        tooltip: {
              // headerFormat: '<b>{point.x}</b><br/>',
              // pointFormat: '{series.name}: {point.y} out of total: {point.stackTotal}'
              headerFormat: '<b>{point.x}</b><br/>',
              pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
            },
        plotOptions: {
            series: {
                stacking: 'normal',
                dataLabels: {
                        enabled: true,
                        color:  '#000000',
                        style: {
                            /*textShadow: '0 0 3px black',*/
                            textShadow:null,
                        },
                        // format:'{point.percentage:.0f}%'
                        format:'{point.y}'
                    },
                point: {
                            events: {
                                click: function() {
                                    var drilldown = this.drilldown;
                                    if (drilldown) {
                                      loadDrillDownData(drilldown); 
                                    }
                                }
                              }
                            }
            },
        },
        series: [{
                name: 'Not complied',
                    data : not_complied
            },  {
                name: 'In progress',
                     data : inprogress_data
            },{
                name: 'Delayed compliance',
                    data : pending_data
            },{
                name: 'Complied',
                data : completed_data
            } ]
        });
      });
    }

    function loadBusinessGroup(){
      $("#viewaspie").hide();
    $("#back").hide();
    $("#viewasbar").hide();
    $(".SumoSelect").show();
    $("#entity-auto").hide();
    $("#division-auto").hide();
    $("#unit-auto").hide();
    $("#previous").hide();
    $("#next").hide();
    $("#container").show();
      $("#imgcontainer").hide();
    $(function () {
        $('#container').highcharts({
          // colors:['#125900','#FF7700','#FFDA0F','#D10018'],
          // colors order: Complied-Green, Delayed-Compliance-Orange, Inprogress-Yellow, Non-compliance-Red
          // 2E9559
          colors:['#F32D2B','#F0F468','#F58835','#A5D17A',],
          // colors:['#2E9559','rgba(255, 191, 0, 1)','rgba(255, 255, 0, 0.9)','rgba(255, 0, 0, 0.8)'],
          chart: {
              type: 'bar',
              width:'850',
              
          },
          title: {
              text: 'Business Group wise compliances'
          },
          xAxis: {
             title: {
                    text: 'Business Groups'
                },
              categories: ['KG Business group 1', 'KG Business group 2', 'KG Business group 3', 'KG Business group 4', 'KG Business group 5'],
              labels: {
                            useHTML: true,
                            formatter: function() {
                                var name=this.value;
                                if(name == "India"){
                                  var link = '<a href="#"  id="'+name+'" onclick=loadCountrySpecific(this.id)>'+
                                      name +'</a>'
                                  return link;
                                }else{
                                  var link = '<span  id="'+name+'" >'+
                                      name +'</span>'
                                  return link;
                                }
                           }
                        },
          },
          yAxis: {
              min: 0,
              title: {
                  text: 'Total Compliances'
              },
              allowDecimals: false
          },
          legend: {
              reversed: true,
          },
          tooltip: {
              // headerFormat: '<b>{point.x}</b><br/>',
              // pointFormat: '{series.name}: {point.y} out of {point.stackTotal}'
              headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
          },
          plotOptions: {
              series: {
                  stacking: 'normal',
                  dataLabels: {
                          enabled: true,
                          color:  '#000000',
                          style: {
                              textShadow:null,
                              color:'#000000'
                          },
                          // format:'{point.percentage:.0f}%'
                          format:'{point.y}'
                      },
                  point: {
                              events: {
                                  click: function() {
                                      var drilldown = this.drilldown;
                                      if (drilldown) {
                                        loadDrillDownData(drilldown); 
                                      }
                                  }
                                }
                              }
              },
          },
          series: [ {
                  name: 'Not complied',
                      data : [
                          {
                              y:22,
                              drilldown:"busNotComplied",
                          },{
                              y:15,
                          },{
                              y:30,
                          }, {
                              y:10,
                          },{
                              y:20,
                          },                   
                      ]
              },{
                  name: 'In progress',
                       data : [
                          {
                              y:18,
                              drilldown:"busInprogress",
                          },{
                              y:25,
                          },{
                              y:10,
                          }, {
                              y:25,
                          },{
                              y:30,
                          },                   
                      ]
              },{
                  name: 'Delayed Compliance',
                      data : [
                          {
                              y:15,
                              drilldown:"busDelayed",
                          },{
                              y:20,
                          },{
                              y:20,
                          }, {
                              y:15,
                          },{
                              y:10,
                          },                   
                      ]
              },{
                  name: 'Complied',
                  data : [
                          {
                              y:15,
                              drilldown:"busComplied",
                          },{
                              y:30,
                          },{
                              y:20,
                          }, {
                              y:20,
                          },{
                              y:30,
                          },                   
                      ]
              },  ]
      });
  });
    }

     function loadUnitNext(){
      $("#previous").show();
      $("#next").show();
      $("#container").show();
      $("#imgcontainer").hide();
      $(function () {  
        var inprogress_data = [10];
        var pending_data = [10];
        var completed_data = [10];
        var not_complied = [10];
              inprogress_data[0] = {name: 'KG Namakal Unit',y: 20,drilldown:"Inprogress"};
              pending_data[0] = {name: 'KG Namakal Unit',y: 16,drilldown:"Delayed"};
              completed_data[0] = {id:'fin',name: 'KG Namakal Unit',y: 25,drilldown:"Complied"};
              not_complied[0] = {name: 'KG Namakal Unit',y: 23,drilldown:"NotComplied"};

              inprogress_data[1] = {name: 'Suseendram, Kanyakumari',y: 18,};
              pending_data[1] = {name: 'Suseendram, Kanyakumari',y: 22,};
              completed_data[1] = {id:'fin',name: 'Suseendram, Kanyakumari',y: 25};
              not_complied[1] = {name:"Suseendram, Kanyakumari", y:21}

              inprogress_data[2] = {name: 'Nagercoil, Kanyakumari',y: 15};
              pending_data[2] = {name: 'Nagercoil, Kanyakumari',y: 23};
              completed_data[2] = {id:'fin',name: 'Nagercoil, Kanyakumari',y: 26};
              not_complied[2] = {name:"Nagercoil, Kanyakumari", y:18}
            
              inprogress_data[3] = {name: 'Naloor, Tuticorin',y: 15};
              pending_data[3] = {name: 'Naloor, Tuticorin',y: 22};
              completed_data[3] = {id:'fin',name: 'Naloor, Tuticorin',y: 31};
              not_complied[3] = {name:"Naloor, Tuticorin", y:23};
         

      $('#container').highcharts({
            // colors:['#239e13','#a3d202','#faf216','#e70808'],
            // colors:['#125900','#FF7700','#FFDA0F','#D10018'],
            colors:['#F32D2B','#F0F468','#F58835','#A5D17A',],
            chart: {
                type: 'bar',
                width:'850',
                
            },
            title: {
                text: 'Unitwise compliances'
            },
            xAxis: {
                categories: ['KG Namakal unit','Suseendram, Kanyakumari','Nagercoil, Kanyakumari','Naloor, Tuticorin'],
                title: {
                    text: 'Units'
                },
                labels: {
                              useHTML: true,
                              formatter: function() {
                                  var name=this.value;
                                  if(name == "KG Autoparts"){
                                    $("#hidden").val("KG Autoparts");
                                    var link = '<a href="#"  id="'+name+'" onclick=loadCompanySingleSelectionPie(this.id)>'+
                                        name +'</a>'
                                    return link;
                                  }else{
                                    var link = '<span  id="'+name+'" >'+
                                        name +'</span>'
                                    return link;
                                  }
                             }
                          },
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Total Compliances'
                },
                allowDecimals: false
            },
            legend: {
                reversed: true
            },
            tooltip: {
              // headerFormat: '<b>{point.x}</b><br/>',
              // pointFormat: '{series.name}: {point.y} out of Total: {point.stackTotal}'
              headerFormat: '<b>{point.x}</b><br/>',
              pointFormat: '{series.name}: {point.percentage:.0f}%<br>Total Compliances: {point.stackTotal}'
            },
            plotOptions: {
                series: {
                    stacking: 'normal',
                    dataLabels: {
                        enabled: true,
                        color:"#000000",
                        style: {
                           textShadow:null,
                        },
                        // format:'{point.percentage:.0f}%'
                        format:'{point.y}'
                    },
                    point: {
                                events: {
                                    click: function() {
                                        var drilldown = this.drilldown;
                                        if (drilldown) {
                                        loadDrillDownData(drilldown); 
                                        }
                                    }
                                  }
                                }
                },
            },
            series: [{
                    name: 'Complied',
                    data : completed_data
                }, {
                    name: 'Delayed compliance',
                        data : pending_data
                }, {
                    name: 'In progress',
                         data : inprogress_data
                }, {
                    name: 'Not complied',
                        data : not_complied
                }]
        });
      });
     }

    function loadDrillDownData(name){
    	$("#viewaspie").hide();
    	$("#viewasbar").hide();
      $("#next").hide();
      $("#previous").hide();
      $("#nextyear").hide();
      $("#previousyear").hide();
    	$("#back").show();
      $("#container").hide();
      $("#imgcontainer").show();
    	var img_name="";
    	var margin_style="";
      if(name == "EntityInprogress"){
        img_name = "/images/dash-list/task-entity-inprogress.png";
        name = "KG Booking";
        com_name="In progress ";
    	}else if(name == "EntityComplied"){
          img_name = "/images/dash-list/task-entity-complied.png";
          name = "KG Booking";
        com_name="Complied ";
          margin_style = "margin-left:3px";
      }else if(name == "EntityDelayed"){
          img_name = "/images/dash-list/task-entity-delayed.png";
          name = "KG Booking";
        com_name="Delayed ";
          margin_style = "margin-left:3px";
      }else if(name == "Inprogress"){
          img_name = "/images/dash-list/task-group-inprogress.png";
          name = "India";
        com_name="In progress ";
    	}else if(name == "Delayed"){
          img_name = "/images/dash-list/task-group-delayed.png";
          name = "India";
        com_name="Delayed ";
    	}else if(name == "NotComplied"){
        img_name = "/images/dash-list/task-group-notcomplied.png";
    		name = "India";
        com_name="Not complied ";
    	}else if(name == "Complied"){
        img_name = "/images/dash-list/task-group-complied.png";
    		name = "India";
        com_name="Complied ";
    	}else if(name == "busInprogress"){
          img_name = "/images/dash-list/task-business-inprogress.png";
          name = "Business Group 1";
        com_name="In progress ";
      }else if(name == "busDelayed"){
          img_name = "/images/dash-list/task-business-delayed.png";
          name = "Business Group 1";
        com_name="Delayed compliance";
      }else if(name == "busNotComplied"){
        img_name = "/images/dash-list/task-business-notcomplied.png";
        name = "Business Group 1 ";
        com_name="Not complied ";
      }else if(name == "busComplied"){
        img_name = "/images/dash-list/task-business-complied.png";
        name = "Business Group 1";
        com_name="Complied ";
      }else if(name == "UnitComplied"){
        img_name = "/images/dash-list/task-unit-complied.png";
        name = "Branch Office 1";
        com_name="Complied ";
      }else if(name == "UnitDelayed"){
        img_name = "/images/dash-list/task-unit-delayed.png";
        name = "Branch Office 1";
        com_name="Delayed";
      }else if(name == "DivisionComplied"){
        img_name = "/images/dash-list/task-division-complied.png";
        name = "KG Manufacturing";
        com_name="Complied ";
      }else if(name == "DivisionDelayed"){
        img_name = "/images/dash-list/task-division-delayed.png";
        name = "KG Manufacturing";
        com_name="Delayed";
      }else if(name == "unitesc"){
    		img_name = "/images/dash-list/escalations-unit-delayed.png";
    		name = "South gate, Madurai - escalations";
    		margin_style="margin-left:200px";
    	}else if(name == "divisionesc"){
    		img_name = "/images/dash-list/escalations-division-delayed.png";
    		name = "KG Manufacturing - escalations";
    		margin_style="margin-left:100px";
    	}else if(name == "entityesc"){
    		img_name = "/images/dash-list/escalations-entity-delayed.png";
    		name = "KG - escalations";
    		margin_style="margin-left:55px";
    	}else if(name == "groupesc"){
    		img_name = "/images/dash-list/escalations-group-delayed.png";
    		name = "KG Groups - escalations";
    	}else if(name == "unitcomp"){
    		img_name = "/images/dash-list/complienceopportunity-unit-not.png";
    		name = "South gate, Madurai - Applicable compliance tasls";
    		margin_style="margin-left:200px";
    	}else if(name == "divisioncomp"){
    		img_name = "/images/dash-list/complienceopportunity-division-not.png";
    		name = "Manufacturing division - Applicable compliances";
    		margin_style="margin-left:150px";
    	}else if(name == "entitycomp"){
    		img_name = "/images/dash-list/complienceopportunity-entity-not.png";
    		name = "KG Entity- Applicable compliances";
    		margin_style="margin-left:40px";
    	}else if(name == "groupcomp"){
    		img_name = "/images/dash-list/complienceopportunity-group-not.png";
    		name = "KG Groups - Applicable compliances";
    	}else if(name == "Jan"){
        if($("#radio1").is(':checked')){
             img_name = "/images/dash-list/drill-group-completed.png";
        }else if($("#radio2").is(':checked')){
              img_name = "/images/dash-list/drill-entity-completed.png";
               margin_style="margin-left:30px";
            }else if($("#radio3").is(':checked')){
              img_name = "/images/dash-list/drill-division-completed.png";
               margin_style="margin-left:120px";
            }else if($("#radio4").is(':checked')){
              img_name = "/images/dash-list/drill-unit-completed.png";
               margin_style="margin-left:140px";
            }
        // img_name = "/images/Company-completed-drill.png";
        name = "";
      }
    	var htmlstr = '<div style="'+margin_style+'" align="left"><table width="100%" style="margin-left:10px;"><tr><td style="margin-left:10px;font-size:1em" width="100%">Compliances - Country: '+name+', Status: '+com_name+'</td></tr></table><br><img src='+img_name+'></div>';
       $(function () {
        $('#imgcontainer').html(htmlstr);
      });
    }

    function loadCountrySpecificBar(value){
    	$("#viewaspie").show();
    	$("#viewasbar").hide();
    	$("#back").show();
      $("#container").show();
      $("#imgcontainer").hide();
    	$(function () {
		    $('#container').highcharts({
		        // colors:['#239e13','#a3d202','#faf216','#e70808'],
                        colors:['#A5D17A','#F58835','#F0F468','#F32D2B',],
		        chart: {
		            type: 'column'
		        },
		        title: {
		            text: 'Country wise Compliances - India'
		        },
		        xAxis: {
		            type: 'category',
                  title: {
                    text: 'Compliance Status'
                },
		        },
		        yAxis: {
		            title: {
		                text: 'Total Compliances'
		            },
                allowDecimals: false

		        },
		        legend: {
		            enabled: false
		        },
		        plotOptions: {
		        	column:{
                dataLabels: {
                        enabled: true,
                        style: {
                            /*textShadow: '0 0 3px black',*/
                            textShadow:null,
                        },
                        /*format:'{point.percentage:.0f}%'*/
                        format:'{point.y}'
					// 	formatter:function() {
					// 	var dataSum = (5 + 2 +8 + 3);
					// 	var pcnt = (this.y / dataSum) * 100;
					// 	return Highcharts.numberFormat(pcnt,0) + '%';
					// }
                    },
		        		point: {
                        events: {
                            click: function() {
                                var drilldown = this.drilldown;
                                if (drilldown) {
                                  $("#hidden").val("singlebar");
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
		                    /*format: '{point.y:.0f}'*/
		                }
		            }
		        },

		        tooltip: {
                            headerFormat: '',
                            pointFormat: '<span>{point.name}</span>: <b>{point.y:.0f} Out of 70'

		        },

		        series: [{
		            name: "Compliances - Group wise",
		            colorByPoint: true,
		            data: [{
		                name: "Complied",
		                y: 15,
		                drilldown: "Complied"
		            }, {
		                name: "Delayed compliance",
		                y: 15,
		                drilldown: "Delayed"
		            }, {
		                name: "In progress",
		                y: 18,
		                drilldown: "Inprogress"
		            }, {
		                name: "Not complied",
		                y: 22,
		                drilldown: "NotComplied"
		            }]
		        }],
		    });
		});

    }

    function loadCountrySpecific(value){
    	$("#viewaspie").hide();
    	$("#back").show();
    	$("#viewasbar").show();
      $("#container").show();
      $("#imgcontainer").hide();
        $(function () {
            $('#container').highcharts({
        colors:['#A5D17A','#F58835', '#F0F468', '#F32D2B'],
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45,
                beta: 0
            }
        },
        title: {
            text: "Country wise Compliances - India"
        },
        tooltip: {
              headerFormat : '',
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
                            click: function() {
                                var drilldown = this.drilldown;
                                $("#hidden").val("singlepie");
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
                        name:"Complied",
                        y:15,
                        drilldown:"Complied"
                      },{
                        name:"Delayed compliance",
                        y:15,
                        drilldown:"Delayed"
                      },{
                        name:"In progress",
                        y:18,
                        drilldown:"Inprogress"
                      },{
                        name:"Not complied",
                        y:22,
                        drilldown:"NotComplied"
                      },
                    ]
        }]
    });
        });
    }


	function loadGroup(){
		$("#viewaspie").hide();
    $("#back").hide();
    $("#viewasbar").hide();
    $(".SumoSelect").show();
    $("#entity-auto").hide();
    $("#division-auto").hide();
    $("#unit-auto").hide();
    $("#previous").hide();
    $("#next").hide();
    $("#container").show();
    $("#imgcontainer").hide();
    var values = $("#country").val();
    var inprogress_data = [10];
        var pending_data = [10];
        var completed_data = [10];
        var not_complied = [10];
        
        if(values.length <= 1){
          loadCompanySingleSelection(values[0]);
        }else if(values.length > 1){
          for(var i=0;i<values.length;i++){
            if (values[i] ==  "India"){
              inprogress_data[i] = {name: 'India',y: 23,drilldown:"Inprogress"};
              pending_data[i] = {name: 'India',y: 22,drilldown:"Delayed"};
              completed_data[i] = {id:'fin',name: 'India',y: 19,drilldown:"Complied"};
              not_complied[i] = {name: 'India',y: 31,drilldown:"NotComplied"};
            }else if(values[i] ==  "US"){
              inprogress_data[i] = {name: 'US',y: 19,};
              pending_data[i] = {name: 'US',y: 27,};
              completed_data[i] = {name: 'US',y: 28};
              not_complied[i] = {name:"US", y:15}
            }else if(values[i] ==  "Singapore"){
              inprogress_data[i] = {name: 'Singapore',y: 15};
              pending_data[i] = {name: 'Singapore',y: 23};
              completed_data[i] = {name: 'Singapore',y: 16};
              not_complied[i] = {name:"Singapore", y:23}
            }else if(values[i] ==  "Malaysia"){
              inprogress_data[i] = {name: 'Malaysia',y: 25};
              pending_data[i] = {name: 'Malaysia',y: 32};
              completed_data[i] = {name: 'Malaysia',y: 13};
              not_complied[i] = {name:"Malaysia", y:24}
            }else if(values[i] ==  "China"){
              inprogress_data[i] = {name: 'China',y: 12};
              pending_data[i] = {name: 'China',y: 26};
              completed_data[i] = {id:'fin',name: 'China',y: 33};
              not_complied[i] = {name:"China", y:14}
            }
          }
        }else{
          alert("Select atleast one unit to load chart");
        } 
		$(function () {
          $('#container').highcharts({
            // colors:['#125900','#FF7700','#FFDA0F','#D10018'],
            // colors order: Complied-Green, Delayed-Compliance-Orange, Inprogress-Yellow, Non-compliance-Red
            // 2E9559
            colors:['#F32D2B','#F0F468','#F58835','#A5D17A',],
            // colors:['#2E9559','rgba(255, 191, 0, 1)','rgba(255, 255, 0, 0.9)','rgba(255, 0, 0, 0.8)'],
            chart: {
                type: 'bar',
                width:'850',
               
            },
            title: {
                text: 'Country wise Compliances'
            },
            xAxis: {
               title: {
                text: 'Countries'
            },
                categories: ['India', 'US', 'Singapore', 'Malaysia', 'China'],
                labels: {
                              useHTML: true,
                              formatter: function() {
                                  var name=this.value;
                                  if(name == "India"){
                                    var link = '<abbr class="page-load" style="width:200px" title="Year: 2014\nFinance : April to March\nIndustrial Law : January to Dececmber\nLabour Law : January to December"><a href="#"  id="'+name+'" onclick=loadCountrySpecific(this.id)>'+
                                        name +'</a><abbr>'
                                    return link;
                                  }else{
                                    var link = '<span  id="'+name+'" >'+
                                        name +'</span>'
                                    return link;
                                  }
                             }
                          },
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Total Compliances'
                },
                allowDecimals: false
            },
            legend: {
                reversed: true,
            },
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
                            color:  '#000000',
                            style: {
                                textShadow:null,
                                color:'#000000'
                            },
                            // format:'{point.percentage:.0f}%'
                            format:'{point.y}'
                        },
                    point: {
                                events: {
                                    click: function() {
                                        var drilldown = this.drilldown;
                                        $("#hidden").val("group");
                                        if (drilldown) {
                                          loadDrillDownData(drilldown); 
                                        }
                                    }
                                  }
                                }
                },
            },
            series: [{
                name: 'Not complied',
                    data : not_complied
            },  {
                name: 'In progress',
                     data : inprogress_data
            },{
                name: 'Delayed compliance',
                    data : pending_data
            },{
                name: 'Complied',
                data : completed_data
            } ]
        });
    });
	}

 function loadConsolidated(value){
      $("#viewaspie").hide();
      $("#back").hide();
      $("#viewasbar").hide();
      $("#container").show();
      $("#imgcontainer").hide();
        $(function () {
            $('#container').highcharts({
        colors:['#A5D17A','#F58835', '#F0F468', '#F32D2B'],
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45,
                beta: 0
            }
        },
        title: {
            text: "Consolidated Chart"
        },
        tooltip: {
              headerFormat : '',
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
                        
                        }
            }
        },
        series: [{
            type: 'pie',
                    name: 'Compliance',
                    data: [
                      {
                        name:"Complied",
                        y:15,
                        drilldown:"Complied"
                      },{
                        name:"Delayed compliance",
                        y:15,
                        drilldown:"Delayed"
                      },{
                        name:"In progress",
                        y:18,
                        drilldown:"Inprogress"
                      },{
                        name:"Not complied",
                        y:22,
                        drilldown:"NotComplied"
                      },
                    ]
        }]
    });
	
	 });

}

$(document).ready(function() {
	chartScript();
});

