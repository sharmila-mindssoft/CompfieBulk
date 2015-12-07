var countriesList;
var domainsList;
var industriesList;
var statutoryNaturesList;
var statutoryLevelsList;
var statutoriesList;
var sm_countryid='';
var sm_domainid='';
var sm_statutorynatureid='';
var sm_industryids=[];
var sm_countryval='';
var sm_domainval='';
var sm_industryvals=[];
var sm_statutorynatureval='';

var sm_statutoryids=[];

$(document).ready(function(){
	getStatutoryMappings();
	//start -filter process in select domain tab
	$("#filter_country").keyup( function() {
    var filter = $("#filter_country").val().toLowerCase();
    var lis = document.getElementsByClassName('countrylist');
    for (var i = 0; i < lis.length; i++) {
        var name = lis[i].getElementsByClassName('filter1_name')[0].innerHTML;
        if (name.toLowerCase().indexOf(filter) == 0) 
            lis[i].style.display = 'list-item';
        else
            lis[i].style.display = 'none';
    }
    });

    $("#filter_domain").keyup( function() {
    var filter = $("#filter_domain").val().toLowerCase();
    var lis = document.getElementsByClassName('domainlist');
    for (var i = 0; i < lis.length; i++) {
        var name = lis[i].getElementsByClassName('filter2_name')[0].innerHTML;
        if (name.toLowerCase().indexOf(filter) == 0) 
            lis[i].style.display = 'list-item';
        else
            lis[i].style.display = 'none';
    }
    });

    $("#filter_industry").keyup( function() {
    var filter = $("#filter_industry").val().toLowerCase();
    var lis = document.getElementsByClassName('industrylist');
    for (var i = 0; i < lis.length; i++) {
        var name = lis[i].getElementsByClassName('filter3_name')[0].innerHTML;
        if (name.toLowerCase().indexOf(filter) == 0) 
            lis[i].style.display = 'list-item';
        else
            lis[i].style.display = 'none';
    }
    });

    $("#filter_statutorynature").keyup( function() {
    var filter = $("#filter_statutorynature").val().toLowerCase();
    var lis = document.getElementsByClassName('statutorynaturelist');
    for (var i = 0; i < lis.length; i++) {
        var name = lis[i].getElementsByClassName('filter4_name')[0].innerHTML;
        if (name.toLowerCase().indexOf(filter) == 0) 
            lis[i].style.display = 'list-item';
        else
            lis[i].style.display = 'none';
    }
    });
    //end -filter process in select domain tab

});

function getStatutoryMappings(){
	function success(status,data){
		industriesList = data["industries"];
		statutoryLevelsList = data["statutory_levels"];
		statutoriesList = data["statutories"];
		countriesList = data["countries"];
		domainsList = data["domains"];
		var geographyLevelsList = data["geography_levels"];
		statutoryNaturesList = data["statutory_natures"];
		var geographiesList = data["geographies"];
		var statutoryMappingsList = data["statutory_mappings"];
		
		loadStatutoryMappingList(statutoryMappingsList);
	}
	function failure(data){
	}
	mirror.getStatutoryMappings(success, failure);
}
function loadStatutoryMappingList(statutoryMappingsList) {
	var j = 1;
	var imgName = '';
	var passStatus = '';
	var statutorymappingId = 0;
	var isActive = 0;
	var industryName = '';
	var statutoryNatureName = '';
	var countryName = '';
	var domainName = '';
	var approvalStatus = '';

	$(".tbody-statutorymapping-list").find("tr").remove();
	for(var entity in statutoryMappingsList) {
		statutorymappingId = entity;
        industryName = statutoryMappingsList[entity]["industry_names"];
        statutoryNatureName = statutoryMappingsList[entity]["statutory_nature_name"];        
        var statutoryMappings='';
        for(var i=0; i<statutoryMappingsList[entity]["statutory_mappings"].length; i++){
        	statutoryMappings = statutoryMappings + statutoryMappingsList[entity]["statutory_mappings"][i] + " <br>";
        }
        var complianceNames='';
        for(var i=0; i<statutoryMappingsList[entity]["compliance_names"].length; i++){
        	complianceNames = complianceNames + statutoryMappingsList[entity]["compliance_names"][i] + " <br>";
        }
        statutoryMappings = statutoryMappings.replace(/>>/gi,' <img src=\'/images/right_arrow.png\'/> ');
        countryName = statutoryMappingsList[entity]["country_name"];
        domainName = statutoryMappingsList[entity]["domain_name"];
        isActive = statutoryMappingsList[entity]["is_active"];
        approvalStatus = statutoryMappingsList[entity]["approval_status"];
        if(isActive == 1) {
          passStatus="0";
          imgName="icon-active.png"
        }
        else {
          passStatus="1";
          imgName="icon-inactive.png"
         }
         if(approvalStatus == '0'){
         	approvalStatus = "Pending";
         }
        var tableRow=$('#templates .table-statutorymapping .table-row');
        var clone=tableRow.clone();
        $('.sno', clone).text(j);
        $('.country', clone).text(countryName);
        $('.domain', clone).text(domainName);
        $('.industry', clone).text(industryName);
        $('.statutorynature', clone).text(statutoryNatureName);
        $('.statutory', clone).html(statutoryMappings);
        $('.compliancetask', clone).html(complianceNames);
        $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="displayEdit('+statutorymappingId+')"/>');
        $('.status', clone).html('<img src=\'/images/'+imgName+'\' onclick="changeStatus('+statutorymappingId+','+passStatus+')"/>');
        $('.approvalstatus', clone).text(approvalStatus);
        $('.tbody-statutorymapping-list').append(clone);
        j = j + 1;
      	}
      }

	function changeStatus (userId,isActive) {
		function success(status,data){
			getStatutoryMappings();
			$("#error").text("Status Changed Successfully");
		}
		function failure(data){
		}
		mirror.changeStatutoryMappingStatus(statutorymappingId, isActive, success, failure);
	}

	function filter (term, cellNr){
		var filterkey = term.value.toLowerCase();
		var table = document.getElementById("filter_statutorymapping");
		var ele;
		for (var r = 1; r < table.rows.length; r++){
			ele = table.rows[r].cells[cellNr].innerHTML.replace(/<[^>]+>/g,"");
			if (ele.toLowerCase().indexOf(filterkey)>=0 )
				table.rows[r].style.display = '';
			else table.rows[r].style.display = 'none';
		}
	}

	function displayAdd () {
	    $("#error").text('');
	    $("#listview").hide();
	    $("#addview").show();
        sm_industryid=[];
        sm_industryval=[];
        sm_countryid='';
        sm_domainid='';
        sm_statutorynatureid='';
        sm_countryval='';
        sm_domainval='';
        sm_statutorynatureval='';

	    //load country details
	    var clsval='.countrylist';
		var clsval1='countrylist';
		var str='';
		$('#country').empty();
	    for(var country in countriesList){
	    	var countryid = countriesList[country]["country_id"];
            var dispcountryname = countriesList[country]["country_name"];
	    	if(countriesList[country]["is_active"] == 1){
				str += '<li id="'+countryid+'" class="'+clsval1+'" onclick="activate(this,'+countryid+',\''+dispcountryname+'\',\''+clsval+'\')" ><span class="filter1_name">'+dispcountryname+'</span></li>';
			}
		}
		$('#country').append(str); 

		//load domain details
		var clsval='.domainlist';
    	var clsval1='domainlist';
    	var str='';
    	$('#domain').empty();
	    for(var domain in domainsList){
	    	var domainid = domainsList[domain]["domain_id"];
            var dispdomainname = domainsList[domain]["domain_name"];
	    	if(domainsList[domain]["is_active"] == 1){
				str += '<li id="'+domainid+'" class="'+clsval1+'" onclick="activate(this,'+domainid+',\''+dispdomainname+'\',\''+clsval+'\')" ><span class="filter2_name">'+dispdomainname+'</span></li>';
			}
		}
		$('#domain').append(str);

		//load industry details
		var clsval='.industrylist';
    	var clsval1='industrylist';
    	var str='';
    	$('#industry').empty();
	    for(var industry in industriesList){
	    	var industryid = industriesList[industry]["industry_id"];
            var dispindustryname = industriesList[industry]["industry_name"];
	    	if(industriesList[industry]["is_active"] == 1){
				str += '<li id="'+industryid+'" class="'+clsval1+'" onclick="multiactivate(this,'+industryid+',\''+dispindustryname+'\',\''+clsval+'\')" ><span class="filter3_name">'+dispindustryname+'</span></li>';
			}
		}
		$('#industry').append(str);

		//load statutorynature details
		var clsval='.statutorynaturelist';
    	var clsval1='statutorynaturelist';
    	var str='';
    	$('#statutorynature').empty();
	    for(var statutorynature in statutoryNaturesList){
	    	var statutorynatureid = statutoryNaturesList[statutorynature]["statutory_nature_id"];
            var dispstatutoryname = statutoryNaturesList[statutorynature]["statutory_nature_name"];
	    	if(statutoryNaturesList[statutorynature]["is_active"] == 1){
				str += '<li id="'+statutorynatureid+'" class="'+clsval1+'" onclick="activate(this,'+statutorynatureid+',\''+dispstatutoryname+'\',\''+clsval+'\')" ><span class="filter4_name">'+dispstatutoryname+'</span></li>';
			}
		}
		$('#statutorynature').append(str);
	} 
	//check & uncheck list data for single selection
	function activate(element, id, dispname, type){
		$(type).each( function( index, el ) {
    	$(el).removeClass( "active" );
    });
		$(element).addClass("active");
		var checkbox_status = $(element).attr('class');
	    if(checkbox_status == 'countrylist active'){
			sm_countryid = id;
            sm_countryval = dispname;
	    }

	    if(checkbox_status == 'domainlist active'){
			sm_domainid = id;
            sm_domainval = dispname;
	    }

        if(checkbox_status == 'statutorynaturelist active'){
            sm_statutorynatureid = id;
            sm_statutorynatureval = dispname;
        }
	    if(sm_countryid != '' && sm_domainid !=''){
		loadStatutoryLevels(sm_countryid,sm_domainid);
	}
    make_breadcrumbs();
	}

	//check & uncheck list data for multi selection
	function multiactivate(element, id, dispname, type){
	var chkstatus = $(element).attr('class');
	if(chkstatus == 'industrylist active'){
		$(element).removeClass("active");
        var removeid = sm_industryid.indexOf(id);
        sm_industryids.splice(removeid,1);
        var removename = sm_industryval.indexOf(dispname);
        sm_industryvals.splice(removename,1);
	}else{
		$(element).addClass("active");
        sm_industryids.push(id);
        sm_industryvals.push(dispname);
	}
    make_breadcrumbs();
}

function make_breadcrumbs(){
    var arrowimage = " <img src=\'/images/right_arrow.png\'/> ";
    $("#breadcrumbs_1").html(sm_countryval + arrowimage + sm_domainval + arrowimage + sm_industryvals + arrowimage + sm_statutorynatureval);
}
//load statutory levels
function loadStatutoryLevels(countryval,domainval){
  $(".tbody-statutory-level").find("div").remove();
  var statutoryLevelList = statutoryLevelsList[countryval][domainval];
  var levelposition;
    for(var j in statutoryLevelList){
      levelposition = statutoryLevelList[j]["level_position"];
      var tableRow=$('#statutory-level-templates');
      var clone=tableRow.clone();
      $('.statutory_title', clone).text(statutoryLevelList[j]["level_name"]);
      $('.statutory_levelvalue', clone).html('<input type="text" class="filter-text-box" id="filter'+levelposition+'" onkeyup="filter_statutory('+levelposition+')"> <ul id="statutorylist'+levelposition+'"></ul><div class="bottomfield"><input type="text" class="input-box addleft" placeholder="" id="datavalue'+levelposition+'" onkeypress="saverecord('+levelposition+',event)"/><span> <a href="#" class="addleftbutton" id="update'+levelposition+'"><img src="/images/icon-plus.png" formtarget="_self" onclick="saverecord('+levelposition+',\'clickimage\')" /></a></span></div><input type="hidden" id="statutorylevelid'+levelposition+'" value="'+statutoryLevelList[j]["level_id"]+'"/><input type="hidden" id="level'+levelposition+'" value="'+levelposition+'" />');
      $('.tbody-statutory-level').append(clone);
    }   

    var setlevelstage= 1;
    $('#datavalue'+setlevelstage).val('');
    $('#statutorylist'+setlevelstage).empty();
    var firstlevelid= $('#statutorylevelid'+setlevelstage).val();

    var str='';
    var idval='';
    var clsval='.slist'+setlevelstage;
    var clsval1='slist'+setlevelstage;

    var statutoryList = statutoriesList[countryval][domainval];
    for(var i in statutoryList){
      var setstatutoryid = statutoryList[i]["statutory_id"];
      if(statutoryList[i]["level_id"] == firstlevelid){
      str += '<span class="eslist-filter'+levelposition+'" style="float:left;margin-right:5px;margin-left:5px;margin-top:3px;cursor:pointer;" onclick="editstaturoty('+setstatutoryid+',\''+statutoryList[i]["statutory_name"]+'\','+levelposition+')"><img src="/images/icon-edit.png" style="width:11px;height:11px"/> </span> <span class="slist-filter'+levelposition+'"> <li id="'+setstatutoryid+'" class="'+clsval1+'" onclick="activate_statutorylist(this,'+setstatutoryid+',\''+clsval+'\','+countryval+','+domainval+','+setlevelstage+')" > '+statutoryList[i]["statutory_name"]+' </li> </span>';
    }
    }
    $('#statutorylist'+setlevelstage).append(str);
}

//check & uncheck list data
function activate_statutorylist(element,id,type,country,domain,level){
  $(type).each( function( index, el ) {
    $(el).removeClass( "active" );
      });
   $(element).addClass("active");
     load(id,level,country,domain);
  }

//load statutory sub level data dynamically
function load(id,level,country,domain){
          var levelstages= parseInt(level) + 1;
          for(var k=levelstages;k<=10;k++){
          var setlevelstage= k;
          if($('#statutoryid').val()==''){
          $('#datavalue'+setlevelstage).val('');
           }
          $('#statutorylist'+setlevelstage).empty();
          var str='';
          var idval='';
          var clsval='.slist'+setlevelstage;
          var clsval1='slist'+setlevelstage;
          var levelid=$('#statutorylevelid'+setlevelstage).val();
          var statutoryList = statutoriesList[country][domain];
            for(var i in statutoryList){
              var setstatutoryid = statutoryList[i]["statutory_id"];
              if( id == statutoryList[i]["parent_id"] && statutoryList[i]["level_id"] == levelid) {
              str += '<span class="eslist-filter'+setlevelstage+'" style="float:left;margin-right:5px;margin-left:5px;margin-top:3px;cursor:pointer;" onclick="editstaturoty('+setstatutoryid+',\''+statutoryList[i]["statutory_name"]+'\','+setlevelstage+')"><img src="/images/icon-edit.png" style="width:11px;height:11px"/></span> <span class="slist-filter'+setlevelstage+'"> <li id="'+setstatutoryid+'" class="'+clsval1+'" onclick="activate_statutorylist(this,'+setstatutoryid+',\''+clsval+'\','+country+','+domain+','+setlevelstage+')" >'+statutoryList[i]["statutory_name"]+'</li> </span>';
            }
            }
          $('#statutorylist'+setlevelstage).append(str); 
          }
    }

    //validate and insert records in statutory table
    function saverecord(j,e){
      var data = e.keyCode;
      if(data==13 || data ==undefined){
      $("#error").text("");
      var levelstage = $('#level'+j).val();
      var statutorylevel_id = $('#statutorylevelid'+j).val();
      var datavalue = $('#datavalue'+j).val();
      var map_statutory_id=[];
      var last_statutory_id=0;
      var last_level = 0;
      for(k=1;k<j;k++){
        $(".slist"+k+".active").each( function( index, el ) {
          map_statutory_id.push(el.id);
          last_statutory_id = el.id;
          last_level = k;
          });
      }
      if(map_statutory_id==0 && levelstage>1 ){
        $("#error").text("Level Selection Should not be Empty");
      }else if(datavalue==""){
        $("#error").text("Level-"+levelstage+" Value Should not be Empty");
      }else{

        if($("#statutoryid").val() == ''){
            function success(status,data){
          if(status == "success"){
            $("#error").text("Record Added Successfully");
            reload(last_statutory_id,last_level,sm_countryid,sm_domainid);
           
          }else{
            $("#error").text(status)
          }
        }
        function failure(data){
        }
        if(map_statutory_id.length == 0){
          map_statutory_id.push(0);
        }
        mirror.saveStatutory(parseInt(statutorylevel_id), datavalue, map_statutory_id, success, failure);
        }else{
            function success_update(status,data){
              if(status == "success"){
                $("#error").text("Record Updated Successfully");
                reload(last_statutory_id,last_level,sm_countryid,sm_domainid);
               
              }else{
                $("#error").text(status)
              }
        }
        function failure_update(data){
        }
        if(map_statutory_id.length == 0){
          map_statutory_id.push(0);
        }
        mirror.updateStatutory(parseInt($("#statutoryid").val()), parseInt(statutorylevel_id), datavalue, map_statutory_id, success_update, failure_update);
        $("#statutoryid").val('');
        $('#datavalue'+j).val('');
        }    
}
}}

function reload(last_statutory_id,last_level,country,domain){
  function success(status,data){
    statutoriesList = data["statutories"];
    load(last_statutory_id,last_level,country,domain)
  }
  function failure(data){
  }
  mirror.getStatutoryMappings(success, failure);
}

function filter_statutory(position){  
    var slist_filter = document.getElementsByClassName('slist-filter'+position);
    var eslist_filter = document.getElementsByClassName('eslist-filter'+position);
    var filter = $('#filter'+position).val().toLowerCase();
    for (var i = 0; i < slist_filter.length; i++) {
        name = slist_filter[i].innerHTML;
        if (name.toLowerCase().indexOf(filter) == 0) {
            slist_filter[i].style.display = 'list-item';
            eslist_filter[i].style.display = 'list-item';
        } else {
            slist_filter[i].style.display = 'none';
            eslist_filter[i].style.display = 'none';
        }
    }
}

function editstaturoty(statu_id, statu_name, position){
    $("#statutoryid").val(statu_id);
    $('#datavalue'+position).val(statu_name)
}

function load_statories(){
    $(".tbody-statutory-list").find("tr").remove();
    for(var i=0; i<sm_statutoryids.length; i++) {
    var tableRow=$('#statutory-templates .table-statutory .table-row');
    var clone=tableRow.clone();
    $('.sno', clone).text(i+1);
    $('.statutory', clone).text(sm_statutoryids[i]);
    $('.remove', clone).html('<img src=\'/images/icon-delete.png\' onclick="temp_removestatutories('+sm_statutoryids[i]+')"/>');
    $('.tbody-statutory-list').append(clone);
}
}

function temp_addstatutories(){
      var last_statutory_id=0;
      for(k=1;k<=10;k++){
        $(".slist"+k+".active").each( function( index, el ) {
          last_statutory_id = el.id;
          });
      }
      if(last_statutory_id==0){
        $("#error").text("No Statutory is selected");
      }else if($.inArray(last_statutory_id, sm_statutoryids) >= 0){
        $("#error").text("This Statutory already added");
      }else{
        sm_statutoryids.push(last_statutory_id);
      }
      load_statories();
}

function temp_removestatutories(remove_id){
    var remove = sm_statutoryids.indexOf(remove_id);
    sm_statutoryids.splice(remove,1);
    load_statories();
}


