var geographyLevelsList;
var geographiesList;
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
var disp_statutories=[];

var sm_compliancedetails=[];
var compliances = [];
var statutory_dates = [];



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

    $("#statutory_date").empty();
    for (var i=1; i<=31; i++) {
        var option = $("<option></option>");
        option.val(i);
        option.text(i)
        $("#statutory_date").append(option);
    }

    $("#single_statutory_date").empty();
    for (var i=1; i<=31; i++) {
        var option = $("<option></option>");
        option.val(i);
        option.text(i)
        $("#single_statutory_date").append(option);
    }

    for(var j=1; j<=6; j++){
     $("#multiple_statutory_date"+j).empty();
    for (var i=1; i<=31; i++) {
        var option = $("<option></option>");
        option.val(i);
        option.text(i)
        $("#multiple_statutory_date"+j).append(option);
    }   
    }
});

function getStatutoryMappings(){
	function success(status,data){
		industriesList = data["industries"];
		statutoryLevelsList = data["statutory_levels"];
		statutoriesList = data["statutories"];
		countriesList = data["countries"];
		domainsList = data["domains"];
		geographyLevelsList = data["geography_levels"];
		statutoryNaturesList = data["statutory_natures"];
		geographiesList = data["geographies"];
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
        sm_statutoryids=[];
        
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
    if(sm_countryid != ''){
        loadGeographyLevels(sm_countryid);
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
    $(".breadcrumbs_1").html(sm_countryval + arrowimage + sm_domainval + arrowimage + sm_industryvals + arrowimage + sm_statutorynatureval);
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
      str += '<span class="eslist-filter'+setlevelstage+'" style="float:left;margin-right:5px;margin-left:5px;margin-top:3px;cursor:pointer;" onclick="editstaturoty('+setstatutoryid+',\''+statutoryList[i]["statutory_name"]+'\','+setlevelstage+')"><img src="/images/icon-edit.png" style="width:11px;height:11px"/> </span> <li id="'+setstatutoryid+'" class="'+clsval1+'" onclick="activate_statutorylist(this,'+setstatutoryid+',\''+clsval+'\','+countryval+','+domainval+','+setlevelstage+')" >'+statutoryList[i]["statutory_name"]+'</li> ';
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
              str += '<span class="eslist-filter'+setlevelstage+'" style="float:left;margin-right:5px;margin-left:5px;margin-top:3px;cursor:pointer;" onclick="editstaturoty('+setstatutoryid+',\''+statutoryList[i]["statutory_name"]+'\','+setlevelstage+')"><img src="/images/icon-edit.png" style="width:11px;height:11px"/></span> <li id="'+setstatutoryid+'" class="'+clsval1+'" onclick="activate_statutorylist(this,'+setstatutoryid+',\''+clsval+'\','+country+','+domain+','+setlevelstage+')" >'+statutoryList[i]["statutory_name"]+'</li> ';
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
    var slist_filter = document.getElementsByClassName('slist'+position);
    var eslist_filter = document.getElementsByClassName('eslist-filter'+position);
    var filter = $('#filter'+position).val().toLowerCase();
    for (var i = 0; i < slist_filter.length; i++) {
        name = slist_filter[i].innerHTML.trim();
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
    disp_statutories = [];
    $(".tbody-statutory-list").find("tr").remove();
    for(var i=0; i<sm_statutoryids.length; i++) {
        var dispstatutory = '';
        var statutoryList = statutoriesList[sm_countryid][sm_domainid];
        for(var statutory in statutoryList){
            if(statutoryList[statutory]["statutory_id"] == sm_statutoryids[i]){
                dispstatutory = statutoryList[statutory]["parent_mappings"];
                disp_statutories.push(dispstatutory);
            }
        }
        var tableRow=$('#statutory-templates .table-statutory .table-row');
        var clone=tableRow.clone();
        $('.sno', clone).text(i+1);
        $('.statutory', clone).html(dispstatutory.replace(/>>/gi,' <img src=\'/images/right_arrow.png\'/> '));
        $('.remove', clone).html('<img src=\'/images/icon-delete.png\' onclick="temp_removestatutories(\''+sm_statutoryids[i]+'\')"/>');
        $('.tbody-statutory-list').append(clone);
}
make_breadcrumbs2();
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
    remove = sm_statutoryids.indexOf(remove_id)
    sm_statutoryids.splice(remove,1);
    load_statories();
}

function temp_addcompliance(){
      var repeats='';
      var comp_id=$('#complianceid').val();
      var repeatstype = null;
      var repeatsevery = null;
      var duration = null;
      var durationtype= null;
      var compliance_frequency = $('#compliance_frequency').val();

      if(compliance_frequency == "onetime"){
        var statutory_date = {};
        statutory_date["statutory_date"] = $('#statutory_date').val();
        statutory_date["statutory_month"] = $('#statutory_month').val();
        statutory_date["trigger_before_days"] = $('#triggerbefore').val();
        statutory_dates.push(statutory_date);
      }else if (compliance_frequency == "periodical" || compliance_frequency == "review"){
        repeatstype = $('#repeats_type').val();
        repeatsevery = $('#repeats_every').val();
        if($('#repeats_type').val() == 'month' && $('.multipleinput').prop("checked") == 'true'){
           for(var i=1;i<=6;i++){
            if($('#multiple_statutory_month'+i).val() != "Select"){
            var statutory_date = {};
            statutory_date["statutory_date"] = $('#multiple_statutory_date'+i).val();
            statutory_date["statutory_month"] = $('#multiple_statutory_month'+i).val();
            statutory_date["trigger_before_days"] = $('#multiple_triggerbefore'+i).val();
            statutory_dates.push(statutory_date);
        }
        }
        }else{
            var statutory_date = {};
            statutory_date["statutory_date"] = $('#single_statutory_date').val();
            statutory_date["statutory_month"] = $('#single_statutory_month').val();
            statutory_date["trigger_before_days"] = $('#single_triggerbefore').val();
            statutory_dates.push(statutory_date);
          }
      }else{
        duration = $('#duration').val();
        durationtype = $('#duration_type').val();
      }
  
      if(comp_id == ''){         
          var compliance = {};
          compliance["statutory_provision"] = $('#statutory_provision').val();
          compliance["compliance_task"] = $('#compliance_task').val();
          compliance["description"] = $('#compliance_description').val();
          compliance["document"] = $('#compliance_document').val();
          compliance["format_file_name"] = $('#upload_file').val();
          compliance["penal_consequences"] = $('#penal_consequences').val();
          compliance["compliance_frequency"] = compliance_frequency;
          compliance["statutory_dates"] = statutory_dates;
          compliance["repeats_type"] = repeatstype;
          compliance["repeats_every"] = repeatsevery;
          compliance["duration_type"] = durationtype;
          compliance["duration"] = duration;
          compliance["is_active"] = 1;
          compliances.push(compliance);
      }else{
        compliances[comp_id]["statutory_provision"] = $('#statutory_provision').val();
        compliances[comp_id]["compliance_task"] = $('#compliance_task').val();
        compliances[comp_id]["description"] = $('#compliance_description').val();
        compliances[comp_id]["document"] = $('#compliance_document').val();
        compliances[comp_id]["format_file_name"] = $('#upload_file').val();
        compliances[comp_id]["penal_consequences"] = $('#penal_consequences').val();
        compliances[comp_id]["compliance_frequency"] = compliance_frequency;
        compliances[comp_id]["statutory_dates"] = statutory_dates;
        compliances[comp_id]["repeats_type"] = repeatstype;
        compliances[comp_id]["repeats_every"] = repeatsevery;
        compliances[comp_id]["duration_type"] = durationtype;
        compliances[comp_id]["duration"] = duration;
        compliances[comp_id]["is_active"] = 1;
    }
      
      $('#statutory_provision').val('');
      $('#compliance_task').val('');
      $('#compliance_description').val('');
      $('#compliance_frequency').val('');
      $('#compliance_document').val('');
      $('#upload_file').val('');
      $('#penal_consequences').val('');
      $('#Recurring').hide();
      $('#Occasional').hide();
      $('#One_Time').hide();
      $('#statutory_date').val('1');
      $('#single_statutory_date').val('1');
      $('#multiple_statutory_date1').val('1');
      $('#multiple_statutory_date2').val('1');
      $('#multiple_statutory_date3').val('1');
      $('#multiple_statutory_date4').val('1');
      $('#multiple_statutory_date5').val('1');
      $('#multiple_statutory_date6').val('1');
      $('#statutory_month').val('Select');
      $('#single_statutory_month').val('Select');
      $('#multiple_statutory_month1').val('Select');
      $('#multiple_statutory_month2').val('Select');
      $('#multiple_statutory_month3').val('Select');
      $('#multiple_statutory_month4').val('Select');
      $('#multiple_statutory_month5').val('Select');
      $('#multiple_statutory_month6').val('Select');
      $('#triggerbefore').val('');
      $('#single_triggerbefore').val('');
      $('#multiple_triggerbefore1').val('');
      $('#multiple_triggerbefore2').val('');
      $('#multiple_triggerbefore3').val('');
      $('#multiple_triggerbefore4').val('');
      $('#multiple_triggerbefore5').val('');
      $('#multiple_triggerbefore6').val('');
      $('.multipleinput').prop("checked") == false;

      $('#complianceid').val('');
      load_compliance();
}

function load_compliance(){
    $(".tbody-compliance-list").find("tr").remove();
     for(var entity in compliances) {
        complianceid = 0;
        var tableRow=$('#compliance-templates .table-compliance .table-row');
        var clone=tableRow.clone();
        $('.sno', clone).text(complianceid+1);
        $('.statutory-provision', clone).text(compliances[entity]["statutory_provision"]);
        $('.task', clone).text(compliances[entity]["compliance_task"]);
        $('.description', clone).text(compliances[entity]["description"]);
        $('.frequency', clone).text(compliances[entity]["compliance_frequency"]);
        $('.repeats', clone).text(compliances[entity]["repeats_every"] +" "+ compliances[entity]["repeats_type"]);
        $('.edit', clone).html('<img src=\'/images/icon-edit.png\' onclick="temp_editcompliance(\''+complianceid+'\')"/>');
        $('.status', clone).html('<img src=\'/images/icon-delete.png\' onclick="temp_removecompliance(\''+complianceid+'\')"/>');
        $('.tbody-compliance-list').append(clone);

        complianceid = complianceid + 1;
}

make_breadcrumbs3();
}

function temp_editcompliance(edit_id){
    $('#statutory_provision').val(compliances[edit_id]["statutory_provision"]);
    $('#compliance_task').val(compliances[edit_id]["compliance_task"]);
    $('#compliance_description').val(compliances[edit_id]["description"]);
    $('#compliance_frequency').val(compliances[edit_id]["compliance_frequency"]);
    $('#compliance_document').val(compliances[edit_id]["document"]);
    $('#upload_file').val(compliances[edit_id]["format_file_name"]);
    $('#penal_consequences').val(compliances[edit_id]["penal_consequences"]);
    $('#duration_type').val(compliances[edit_id]["duration_type"]);
    $('#duration').val(compliances[edit_id]["duration"]);
    $('#repeats_type').val(compliances[edit_id]["repeats_type"]);
    $('#repeats_every').val(compliances[edit_id]["repeats_every"]);

      var compliance_frequency = compliances[edit_id]["compliance_frequency"];
      if(compliance_frequency == "onetime"){
        $('#statutory_date').val(statutory_dates[0]["statutory_date"]);
        $('#statutory_month').val(statutory_dates[0]["statutory_month"]);
        $('#triggerbefore').val(statutory_dates[0]["trigger_before_days"]);
        $('#Recurring').hide();
        $('#Occasional').hide();
        $('#One_Time').show();

      }else if (compliance_frequency == "periodical" || compliance_frequency == "review"){
        $('#Recurring').show();
        $('#Occasional').hide();
        $('#One_Time').hide();

        if(statutory_dates.length > 0){
            $('.multipleinput').prop("checked") == true;
            $('.multipleselectnone').hide();
            $('.multipleselect').show();
        }
       for(var i=1;i<=statutory_dates.length;i++){
            $('#multiple_statutory_date'+i).val(statutory_dates[i-1]["statutory_date"]);
            $('#multiple_statutory_month'+i).val(statutory_dates[i-1]["statutory_month"]);
            $('#multiple_triggerbefore'+i).val(statutory_dates[i-1]["trigger_before_days"]);
        }
      }else{
            $('#Recurring').hide();
            $('#Occasional').show();
            $('#One_Time').hide();
      }
    $('#complianceid').val(edit_id);
}
function temp_removecompliance(remove_id){
    compliances.splice(remove_id,1);
    load_compliance();
}
function make_breadcrumbs2(){
    var arrowimage = " <img src=\'/images/right_arrow.png\'/> ";
    var statutories_name = '';
    for(var i=0;i<disp_statutories.length;i++){
        statutories_name = statutories_name + disp_statutories[i].replace(/>>/gi,' <img src=\'/images/right_arrow.png\'/> ') + '<br/>';
    }
    $(".breadcrumbs_2").html(statutories_name);
}

function make_breadcrumbs3(){
    var compliance_name = '';
    for(var entity in compliances) {
        compliance_name = compliance_name + compliances[entity]["document"] +" - " + compliances[entity]["statutory_provision"] + '<br/>';
    }
    $(".breadcrumbs_3").html(compliance_name);
}

function loadGeographyLevels(sm_countryid){
  $(".tbody-geography-level").find("div").remove();
  var geographyLevelList = geographyLevelsList[sm_countryid];
  var levelposition;
    for(var j in geographyLevelList){

      levelposition = geographyLevelList[j]["level_position"];
      var tableRow=$('#geography-level-templates');
      var clone=tableRow.clone();
      $('.title', clone).text(geographyLevelList[j]["level_name"]);
      $('.levelvalue', clone).html('<input type="text" class="filter-text-box" id="filter_geography'+levelposition+'" onkeyup="filter_geography('+levelposition+')"> <ul id="ulist'+levelposition+'"></ul><input type="hidden" id="glmid'+levelposition+'" value="'+geographyLevelList[j]["level_id"]+'"/><input type="hidden" id="level'+levelposition+'" value="'+levelposition+'" />');
      $('.tbody-geography-level').append(clone);
    }    
    var setlevelstage= 1;
    $('#datavalue'+setlevelstage).val('');
    $('#ulist'+setlevelstage).empty();
    var firstlevelid= $('#glmid'+setlevelstage).val();

    
    var idval='';
    var clsval='.list'+setlevelstage;
    var clsval1='list'+setlevelstage;
    var str='<li id="0" class="'+clsval1+'" onclick="activate_geography_all(this,'+sm_countryid+','+setlevelstage+')" > Select All</li>';

    var geographyList = geographiesList[sm_countryid];
    for(var i in geographyList){
      var setgeographyid = geographyList[i]["geography_id"];
      var setparentid = geographyList[i]["parent_id"];
      var combineid = setgeographyid + "," + setparentid;
      if((geographyList[i]["level_id"] == firstlevelid) && (geographyList[i]["is_active"] == 1)){
      str += '<li id="'+combineid+'" class="'+clsval1+'" onclick="activate_geography(this,'+sm_countryid+','+setlevelstage+')" >'+geographyList[i]["geography_name"]+'</li>';
    }
    }
    $('#ulist'+setlevelstage).append(str); 
}

//check & uncheck list data
function activate_geography(element,country,level){
    var chkstatus = $(element).attr('class');
    if(chkstatus == 'list'+level+' active'){
        $(element).removeClass("active");
    }else{
        $(element).addClass("active");
    } 
    load_geography(level,country); 
}

//select all geography level data
function activate_geography_all(element,country,level){
    var chkstatus = $(element).attr('class');
    if(chkstatus == 'list'+level+' active'){
    $('.list'+level+".active").each( function( index, el ) {
    $(el).removeClass( "active" );
      });
    }else{
        $('.list'+level).each( function( index, el ) {
            $(el).addClass( "active" );
        });
    } 
    load_geography(level,country); 
}

//load geographymapping sub level data dynamically
function load_geography(level,country){
    var sm_geographyids=[];
    $(".list"+level+".active").each( function( index, el ) {
        var split_id = el.id.split(',');
        sm_geographyids.push([parseInt(split_id[0]),el.innerHTML]);
    });
    
    var levelstages= parseInt(level) + 1;
    for(var k=levelstages;k<=10;k++){
        var setlevelstage= k;
        if($('#geographyid').val()==''){
            $('#datavalue'+setlevelstage).val('');
        }
        $('#ulist'+setlevelstage).empty();
        var splittext = '';
        var idval='';
        var clsval='.list'+setlevelstage;
        var clsval1='list'+setlevelstage;
        var str='';
        var sel_all='<li id="0" class="'+clsval1+'" onclick="activate_geography_all(this,'+sm_countryid+','+setlevelstage+')" > Select All</li>';
        var geographyLevelList = geographyLevelsList[country];
        var levelid=$('#glmid'+setlevelstage).val();
        var geographyList = geographiesList[country];

        //working order is even for multiple selection
       for(var j=0;j<sm_geographyids.length;j++){
        splittext = '';
        for(var i in geographyList){
          var setgeographyid = geographyList[i]["geography_id"];
          var setparentid = geographyList[i]["parent_id"];
          var combineid = setgeographyid + "," + setparentid;

          if( geographyList[i]["parent_id"] == sm_geographyids[j][0] && geographyList[i]["level_id"] == levelid && geographyList[i]["is_active"] == 1) {
            str += sel_all;
           if(splittext != '') {
            str += '<li id="'+combineid+'" class="'+clsval1+'" onclick="activate_geography(this,'+country+','+setlevelstage+')" > '+geographyList[i]["geography_name"]+'</li>';
           }else{
            splittext = '<h3 style="background-color:gray;padding:2px;font-size:13px;color:white;">'+sm_geographyids[j][1]+'</h3>';
            str += splittext + '<li id="'+combineid+'" class="'+clsval1+'" onclick="activate_geography(this,'+country+','+setlevelstage+')" >'+geographyList[i]["geography_name"]+'</li>';
           }
           sel_all = '';
        }
        }
       }
        //working but order is not even for multiple selection
        /*for(var i in geographyList){
          var setgeographyid = geographyList[i]["geography_id"];
          var checkstate = $.inArray(geographyList[i]["parent_id"], sm_geographyids);
          if( checkstate >= 0 && geographyList[i]["level_id"] == levelid && geographyList[i]["is_active"] == 1) {
          str += '<a href="#"> <span class="glist-filter'+setlevelstage+'"> <li id="'+setgeographyid+'" class="'+clsval1+'" onclick="activate_geography(this,'+country+','+setlevelstage+')" > '+geographyList[i]["geography_name"]+'</li></span> </a>';
        }
        }*/
        $('#ulist'+setlevelstage).append(str); 
    }
}

function getGeographyResult(){
      var selected_geography=[];
      for(k=1;k<=10;k++){
        $(".list"+k+".active").each( function( index, el ) {
            var split_id = el.id.split(',');
            var g_id = parseInt(split_id[0]);
            var p_id = parseInt(split_id[1]);
            selected_geography.push(g_id);
            if($.inArray(p_id, selected_geography) >= 0){
                var remove_geography = selected_geography.indexOf(p_id);
                selected_geography.splice(remove_geography,1);
            }
            
          });
      }
      alert(selected_geography);
}

function filter_geography(position){  
    var glist_filter = document.getElementsByClassName('list'+position);
    var filter = $('#filter_geography'+position).val().toLowerCase();
    for (var i = 0; i < glist_filter.length; i++) {
        name = glist_filter[i].innerHTML.trim();
        if (name.toLowerCase().indexOf(filter) == 0) {
            glist_filter[i].style.display = 'list-item';
        } else {
            glist_filter[i].style.display = 'none';
        }
    }
}