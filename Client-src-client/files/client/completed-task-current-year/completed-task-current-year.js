//var countriesList;
//var businessgroupsList;
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


//clear list values
function clearValues(levelvalue) {
  // if(levelvalue == 'country'){
  //   //$('#businessgroup').empty();
  //   legalentityul.empty();
  //   divisionul.empty();
  //   unitul.empty();
  // }

  // if(levelvalue == 'businessgroup'){
  //   legalentityul.empty();
  //   divisionul.empty();
  //   unitul.empty();
  // }

  if(levelvalue == 'legalentity'){
    divisionul.empty();
    categoryul.empty();
    unitul.empty();
  }

  if(levelvalue == 'division'){
    categoryul.empty();
    unitul.empty();
  }
  if(levelvalue == 'category'){    
    unitul.empty();
  }
   
}

function activate_assignee (element,checkval,checkname, clickvalue) {
  $("#assigneeval"+clickvalue).val(checkname);
  $("#assignee"+clickvalue).val(checkval);
}

//load available compliance in third wizard
function load_thirdwizard(){  
  for(var entity in statutoriesList){
    ACCORDIONCOUNT += 1;
    // accordion-list
    var accRow=$('#templates .accordion-list .panel');
    var clone1=accRow.clone();
   
    var actname = statutoriesList[entity]["level_1_statutory_name"];;
    var actCompliances = statutoriesList[entity]["pr_compliances"];
    $('.actname', clone1).html(actname);    
    $('.panel-title a', clone1).attr('href', '#collapse' + ACCORDIONCOUNT);
    $('.panel-title a', clone1).attr('aria-controls', 'collapse' + ACCORDIONCOUNT);
     if (ACCORDIONCOUNT == 1) { //For First group open collapse
        $('.panel-title a', clone1).attr('aria-expanded', true);
        $('.panel-title a', clone1).removeClass('collapsed');
        $('.coll-title', clone1).addClass('in');
        $('.coll-title', clone1).attr('id', 'collapse' + ACCORDIONCOUNT);
    }
    $('#accordion').append(clone1); 
      for(var ac in actCompliances){
        sno++;
        var compliance_id = actCompliances[ac]["compliance_id"];
        var compliance_name = actCompliances[ac]["compliance_name"];
        var compliance_description = actCompliances[ac]["description"];
        var assignee_name =  actCompliances[ac]["assignee_name"];
        var assignee_id =  actCompliances[ac]["assignee_id"];
        var frequency =  actCompliances[ac]["compliance_task_frequency"];
        var statutory_date =  actCompliances[ac]["pr_statutory_date"];
        var due_date =  actCompliances[ac]["due_date"];
        var statutorydate = actCompliances[ac]["statutory_date"];
        var complianceDetailtableRow = $('#statutory-values .table-statutory-values .compliance-details');
        var clone2=complianceDetailtableRow.clone();       

        $('.compliancetask i', clone2).attr('data-original-title', compliance_description);
        $('.compliancetask span', clone2).html(compliance_name);
        //$('.compliancefrequency', clone2).html(frequency);
         $('.compliancefrequency', clone2).html(frequency +
        '<input type="hidden" id="complianceid'+sno+'" value="'+compliance_id+'"/>' +
        '<input type="hidden" id="compliancename'+sno+'" value="'+compliance_name+'"/>' +
        '<input type="hidden" id="frequency'+sno+'" value="'+frequency+'"/>');
        $('.statutorydate', clone2).html(statutory_date);
        $('.duedate', clone2).html('<input type="text" value="'+due_date+'" readonly="readonly" class="form-control input-sm" id="duedate'+sno+'" />');
        $('.completiondate', clone2).html('<input type="text" value="" readonly="readonly" class="form-control input-sm" id="completiondate'+sno+'" />');
        // if(frequency == 'Periodical' || frequency == 'Review'){
        //   $('.validitydate', clone2).html('<input type="text" value="" class="form-control input-sm" readonly="readonly" id="validitydate'+sno+'" />');
        // }else{
        //   $('.validitydate', clone2).html("");
        // }
        $('.documentupload', clone2).html('<input type="file" class="form-control input-sm" id="upload'+sno+'" multiple />');
        //$('.assignee', clone2).html('<input type="text" value="'+assignee_name+'" class="input-box icon-autocomplete" id="assigneeval'+sno+'" style="width:100px;" /> <input type="hidden" id="assignee'+sno+'" value="'+assignee_id+'"> <div id="autocomplete_assignee'+sno+'" class="ac-textbox default-display-none"> <ul id="ulist_assignee'+sno+'" style="width:115px;" class="hidemenu"></ul></div>');

        $('.assignee', clone2).html('<input class="form-control input-sm domain" type="text" value="'+assignee_name+'"  id="assigneeval'+sno+'" ><i class="fa-1-2x form-control-feedback fa fa-search"></i><input type="hidden"  id="assignee'+sno+'" value="'+assignee_id+'"><div id="autocomplete_assignee'+sno+'"  class="ac-textbox default-display-none"><ul class="hidemenu"></ul></div>');



        $('.completedstatus', clone2).html(' <input type="checkbox" class="text-center" id="completedstatus'+sno+'"> <label for="checkbox8"></label>');
        $('#collapse'+ACCORDIONCOUNT+' .tbody-pastRecords').append(clone2);


        $("#upload"+sno).on("change", function(e) {
        client_mirror.uploadFile(e, function result_data(data) {
          if(data != 'File max limit exceeded' || data != 'File content is empty'){
            uploadFile = data;
            file_list = data
          }
          else{
            file_list = [];
          }
         });
        });

        $("#duedate"+sno).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        });

        // $("#validitydate"+sno ).datepicker({
        //     changeMonth: true,
        //     changeYear: true,
        //     numberOfMonths: 1,
        //     dateFormat: "dd-M-yy",
        //     monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        //     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        // });

        $("#completiondate"+sno ).datepicker({
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            dateFormat: "dd-M-yy",
            monthNames: ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        });

        var User = $("#assigneeval"+sno);
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


        // $("#assigneeval"+sno).keyup(function(){
        //   var textval = $(this).val();
        //   var text = $(this).attr('id');
        //   var clickvalue = text.substring(text.lastIndexOf('l') + 1);
        //   $("#autocomplete_assignee"+clickvalue).show();

        //   var assignees = usersList;
        //   var suggestions = [];
        //   $('#ulist_assignee'+clickvalue).empty();
        //   if(textval.length>0){
        //     for(var i in assignees){
        //       if (~assignees[i]["employee_name"].toLowerCase().indexOf(textval.toLowerCase())) suggestions.push([assignees[i]["user_id"],assignees[i]["employee_name"]]);
        //     }
        //     var str='';
        //     for(var i in suggestions){
        //               str += '<li id="'+suggestions[i][0]+'"onclick="activate_assignee(this,\''+suggestions[i][0]+'\',\''+suggestions[i][1]+'\','+clickvalue+')">'+suggestions[i][1]+'</li>';

        //     }
        //     $('#ulist_assignee'+clickvalue).append(str);
        //     $("#assignee"+clickvalue).val('');
        //     }else{
        //       $("#assignee"+clickvalue).val('');
        //       $("#autocomplete_assignee"+clickvalue).hide();
        //     }
        // });
      }
  }

  $(".hidemenu").click(function(){
    $(".ac-textbox").hide();
  });

  if(totalRecord == 0){
      var tableRow4=$('#no-record-templates .table-no-content .table-row-no-content');
      var clone4=tableRow4.clone();
      $('.no_records', clone4).text('No Compliance Found');
      $('.tbody-pastRecords').append(clone4);
      $('#pagination').hide();
      $('.compliance_count').text('');
  }else{
      $('.compliance_count').text("Showing " + 1 + " to " + sno + " of " + totalRecord);
      if(sno >= totalRecord){
        $('#pagination').hide();
      }else{
        $('#pagination').show();
      }
  }
}

//validation in first wizard
function validate_firsttab(){
  // if($('.countrylist.active').text() == ''){
  //   displayMessage(message.country_required);
  //   return false;
  // }else
  if (legalentityul.find('.active').text() == ''){
    displayMessage(message.legalentity_required);
    return false;
  }else if (unitul.find('.active').text() == ''){
    displayMessage(message.unit_required+"--");
    return false;
  }
  // }else{
  //   displayMessage("");
  //   return true;
  // }
}

//validation in second wizard
function validate_secondtab(){
  if($('.domainlist.active').text() == ''){
    displayMessage(message.domain_required);
    return false;
  }else if(frequencyul.find('.active') == 0 ){
    displayMessage(message.frequency_required);
    return false;
  }else{
    return true;
  }
}

function validate_thirdtab(){
  return true;
}

//convert string to date format
function convert_date (data){
  var date = data.split("-");
  var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  for(var j=0;j<months.length;j++){
      if(date[1]==months[j]){
           date[1]=months.indexOf(months[j])+1;
       }
  }
  if(date[1]<10){
      date[1]='0'+date[1];
  }
  return new Date(date[2], date[1]-1, date[0]);
}

//find date difference between two dates
function daydiff(first, second) {
    return (second-first)/(1000*60*60*24)
}

//save past records data
function submitcompliance(){
    displayLoader();
    var unit_id = parseInt(unitul.find('.active').attr('id'));
    compliance_list = [];

    for(var i=1; i<=sno; i++){
        var complianceApplicable = false;

        if($('#completedstatus'+i).is(":checked")){
          complianceApplicable = true;
        }
        console.log("complianceApplicable--"+complianceApplicable+"--"+i);
        if(complianceApplicable){
          var compliance_id = parseInt($('#complianceid'+i).val());
          //var validity_date = $('#validitydate'+i).val();
          var due_date = $('#duedate'+i).val();
          var completion_date = $('#completiondate'+i).val();
          var completed_by = $('#assignee'+i).val();
          var frequency_ = $('#frequency'+i).val();
          var compliance_name = $('#complaincename'+i).val();
          if(completed_by != '') completed_by = parseInt(completed_by);

          if(due_date == ''){
            displayMessage(message.duedate_required);
            hideLoader();
            return false;
          }
          else if(completion_date == ''){
            displayMessage(message.compliancedate_required);
            hideLoader();
            return false;
          }
          // else if(validity_date == '' && frequency_ == 'Periodical'){
          //   displayMessage(message.validitydate_required);
          //   hideLoader();
          //   return false;
          // }
          else if(completed_by == null){
            displayMessage(message.assignee_required);
            hideLoader();
            return false;
          }
          // else if(validity_date != '' && frequency_ == 'Periodical'){
          //   var convertDueDate = convert_date(due_date);
          //   var convertValidityDate = convert_date(validity_date);
          //   var dateDifference = daydiff(convertDueDate, convertValidityDate);
          //   if (convertDueDate > convertValidityDate) {
          //     displayMessage(message.duedatelessthanvaliditydate_compliance + compliance_name);
          //     hideLoader();
          //     return false;
          //   }else if(dateDifference > 90){
          //     displayMessage(message.invalid_duedate + compliance_name);
          //     hideLoader();
          //     return false;
          //   }else{
          //     displayMessage("");
          //   }
          // }
          // else{
          //   displayMessage("");
          // }
          compliance = client_mirror.getPastRecordsComplianceDict(unit_id, compliance_id, due_date, completion_date, file_list, completed_by);
          compliance_list.push(compliance);
        }

    }
    console.log(JSON.stringify(compliance_list));
  if(compliance_list.length == 0){
    displayMessage(message.select_atleast_one_compliance);
    return false;
  }

  function onSuccess(data){
    displaySuccessMessage(message.save_success);
    clearValues('legalentity');
    CURRENT_TAB = 1;
    $("#accordion").empty();
    getLegalEntity();
    pageControls();
    //load_firstwizard();
    hideLoader();
  }
  function onFailure(error){
    displayMessage(error[1]["error"]);
    hideLoader();
  }
  client_mirror.savePastRecords(parseInt(LE_ID), compliance_list,
    function (error, response) {
    if (error == null){
      onSuccess(response);
    }
    else {
      onFailure(error);
    }
  }
  );
}

// //create wizard
// var navListItems = $('ul.setup-panel li a'),
// allWells = $('.setup-content');
// allWells.hide();
// navListItems.click(function(e)
// {
// e.preventDefault();
// var $target = $($(this).attr('href')),
// $item = $(this).closest('li');
// if (!$item.hasClass('disabled')) {
// navListItems.closest('li').removeClass('active');
// $item.addClass('active');
// allWells.hide();
// $target.show();
// }
// });
// $('ul.setup-panel li.active a').trigger('click');
// $('#activate-step-2').on('click', function(e) {
// if (validate_firsttab()){
// $('ul.setup-panel li:eq(1)').removeClass('disabled');
// $('ul.setup-panel li a[href="#step-2"]').trigger('click');
// }
// })

// $('#activate-step-3').on('click', function(e) {
// if (validate_secondtab()){
//   sno = 0;
//   $(".tbody-pastRecords").find("tr").remove();
//   getStatutories();
//   $('#activate-step-finish').show();
//   $('ul.setup-panel li:eq(2)').removeClass('disabled');
//   $('ul.setup-panel li a[href="#step-3"]').trigger('click');
// }
// })

// $('#backward-step-1').on('click', function(e) {
// $('ul.setup-panel li:eq(1)').removeClass('disabled');
// $('ul.setup-panel li a[href="#step-1"]').trigger('click');

// })

// $('#backward-step-2').on('click', function(e) {
//   $('ul.setup-panel li:eq(2)').removeClass('disabled');
//   $('ul.setup-panel li a[href="#step-2"]').trigger('click');

// })

// $('#activate-step-finish').on('click', function(e) {
//   if (validate_thirdtab()){
//   submitcompliance();
//   }
// })

//get compliances for selected unit
function getStatutories(){
  displayLoader();
  var pastRecordsUnitId = null;
  var pastRecordsDomainId = null;
  var pastRecordsActId = null;
  var pastRecordsFrequencyId = null;
  //var pastRecordsCountryId = null;  
  console.log("frequencyul.find('.active').attr('id') --"+frequencyul.find('.active').attr('id') );
  //if($('.countrylist.active').attr('id') != undefined) pastRecordsCountryId = parseInt($('.countrylist.active').attr('id'));
  if(unitul.find('.active').attr('id') != undefined) pastRecordsUnitId = parseInt(unitul.find('.active').attr('id'));
  if(domainul.find('.active').attr('id') != undefined) pastRecordsDomainId = parseInt(domainul.find('.active').attr('id'));
  if(actul.find('.active').attr('id') != undefined) pastRecordsActId = actul.find('.active').attr('id');
  if(frequencyul.find('.active').attr('id') != undefined) pastRecordsFrequencyId = frequencyul.find('.active').attr('id');

  if(pastRecordsUnitId != null && pastRecordsDomainId != null){
    function onSuccess(data){
      console.log(JSON.stringify(data["statutory_wise_compliances"]));
      statutoriesList = data["statutory_wise_compliances"];
      usersList = data["pr_users"];
      totalRecord = data["total_count"];
      load_thirdwizard();
      hideLoader();
    }
    function onFailure(error){
      hideLoader();
    }
    //pastRecordsCountryId
    client_mirror.getStatutoriesByUnit(
      pastRecordsUnitId, pastRecordsDomainId, pastRecordsActId,
      pastRecordsFrequencyId, sno,
      function (error, response) {
            if (error == null){
              onSuccess(response);
            }
            else {
              onFailure(error);
            }
        }
    );
    }
}

//pagination process
$('#pagination').click(function(){
  getStatutories();
});

//load unit in unit list based on filter selection
// function loadunit(){

//   var pastRecordsLegalEntityId = null;
//   if($('.legalentitylist.active').attr('id') != undefined)
//     pastRecordsLegalEntityId = parseInt($('.legalentitylist.active').attr('id'));

//   var pastRecordsDivisionId = null;
//   if($('.divisionlist.active').attr('id') != undefined)
//     pastRecordsDivisionId = parseInt($('.divisionlist.active').attr('id'));

//   // var pastRecordsBusinessGroupId = null;
//   // if($('.businessgrouplist.active').attr('id') != undefined)
//   //   pastRecordsBusinessGroupId = parseInt($('.businessgrouplist.active').attr('id'));

//   // var pastRecordsCountryId = parseInt($('.countrylist.active').attr('id'));

//   if(pastRecordsLegalEntityId != null){
//       var str='';
//       var splittext='';
//       unitul.empty();
//       for(var u in unitsList){
//         var iUnits = unitsList[u]["units"];
//         var iName = unitsList[u]["industry_name"];
//         splittext = '<h3 style="background-color:gray;padding:2px;font-size:13px;color:white;">'+iName+'</h3>';
//         for(var unit in iUnits){
//           //iUnits[unit]["business_group_id"] == pastRecordsBusinessGroupId && iUnits[unit]["country_id"] == pastRecordsCountryId
//           if(iUnits[unit]["division_id"] == pastRecordsDivisionId &&
//             iUnits[unit]["legal_entity_id"] == pastRecordsLegalEntityId){
//             str += splittext + '<li id="'+iUnits[unit]["unit_id"]+'" class="unitlist" > <abbr class="page-load" title="'+
//             iUnits[unit]["address"]+'"><img src="/images/icon-info.png" style="margin-right:10px"></abbr>'+
//             iUnits[unit]["unit_name"]+'</li>';
//             splittext = '';
//         }
//         }
//       }
//       unitul.append(str);
//   }
// }

// $("#unit").click(function(event){
//   if($(event.target).attr('class') == 'unitlist'){
//     $('.'+$(event.target).attr('class')).each( function( index, el ) {
//       $(el).removeClass( "active" );
//     });
//     $(event.target).addClass("active");
//   }

//   var pastRecordsUnitId = parseInt($('.unitlist.active').attr('id'));
//   var unitDomains = [];
//   for(var industryunit in unitsList){
//     var iUnits = unitsList[industryunit]["units"];
//     for(var unit in iUnits){
//       if(iUnits[unit]["unit_id"] == pastRecordsUnitId){
//         unitDomains = iUnits[unit]["domain_ids"];
//     }
//     }
//   }

//   var str='';
//   $('#domain').empty();
//   $('#act').empty();
//   for(var domain in domainsList){
//     if($.inArray(domainsList[domain]["domain_id"], unitDomains) >= 0){
//       str += '<li id="'+domainsList[domain]["domain_id"]+'" class="domainlist" >'+domainsList[domain]["domain_name"]+'</li>';
//     }
//   }
//   $('#domain').append(str);

//   var str='';
//   $('#frequency').empty();
//   for(var frequency in frequencyList){
//       str += '<li id="'+frequencyList[frequency]["frequency"]+'" class="frequencylist" >'+frequencyList[frequency]["frequency"]+'</li>';

//   }
//   $('#frequency').append(str);
//   $('ul.setup-panel li:eq(2)').addClass('disabled');
// });


// $("#businessgroup").click(function(event){
//   if($(event.target).attr('class') == 'businessgrouplist'){
//     clearValues('businessgroup');
//     $('.'+$(event.target).attr('class')).each( function( index, el ) {
//       $(el).removeClass( "active" );
//     });
//     $(event.target).addClass("active");

//     var str='';
//     var pastRecordsBusinessGroupId = parseInt(event.target.id);
//     legalentityul.empty();
//     for(var legalentity in legalentitiesList){
//       if(legalentitiesList[legalentity]["business_group_id"] == pastRecordsBusinessGroupId){
//         str += '<li id="'+legalentitiesList[legalentity]["legal_entity_id"]+'" class="legalentitylist" >'+legalentitiesList[legalentity]["legal_entity_name"]+'</li>';
//       }
//     }
//     legalentityul.append(str);
//   }
// });

// $("#legalentity").click(function(event){
//   if($(event.target).attr('class') == 'legalentitylist'){
//     clearValues('legalentity');
//     $('.'+$(event.target).attr('class')).each( function( index, el ) {
//       $(el).removeClass( "active" );
//     });
//     $(event.target).addClass("active");
//     var str='';
//     var pastRecordsLegalEntityId = parseInt(event.target.id);
//     divisionul.empty();
//     for(var division in divisionsList){
//       if(divisionsList[division]["legal_entity_id"] == pastRecordsLegalEntityId){
//         str += '<li id="'+divisionsList[division]["division_id"]+'" class="divisionlist" >'+divisionsList[division]["division_name"]+'</li>';
//       }
//     }
//     divisionul.append(str);
//     loadunit();
//   }
// });



function loadDivision(){
  $.each(divisionsList, function(key, value) {
    id = value.div_id;
    text = value.div_name;

    var le_id = legalentityul.find("li.active").attr("id");
    if(le_id == value.le_id){
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

function loadCategory(){
  $.each(categoryList, function(key, value) {
        id = value.cat_id;
        text = value.cat_name;

        var le_id = legalentityul.find("li.active").attr("id");
        var div_id = '';
        if(divisionul.find("li.active").attr("id") != undefined){
          div_id = divisionul.find("li.active").attr("id");
        }
        if(le_id == value.le_id && (div_id == '' || div_id == value.div_id)){
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

function loadDomain(){
  $.each(domainsList, function(key, value) {
        id = value.d_id;
        text = value.d_name;

        var le_id = legalentityul.find("li.active").attr("id");
        
        if(le_id == value.le_id){
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

function loadUnit(){
  $.each(unitsList, function(key, value) {
        id = value.unit_id;
        text = value.unit_code +"-"+value.unit_name;

        var clone = ULRow.clone();
        clone.html(text + '<i></i>');
        clone.attr('id', id);
        unitul.append(clone);
        clone.click(function() {
            activateList(this, 'unit');
        });
    });
}

function loadAct(){
  var d_id = domainul.find("li.active").attr("id");
  $.each(actList, function(key, value) {
      id = key;
      text = value;       
      if(d_id == key){
        for(var i = 0; i<text.length; i++){
          var clone = ULRow.clone();
          clone.html(text[i] + '<i></i>');
          clone.attr('id', id);
          actul.append(clone);
          clone.click(function() {          
            activateList(this, 'act');
          });
        }
      }
        
    });
}

function loadFrequency(){
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


// $("#division").click(function(event){
//   if($(event.target).attr('class') == 'divisionlist'){
//     clearValues('division');
//     $('.'+$(event.target).attr('class')).each( function( index, el ) {
//       $(el).removeClass("active");
//     });
//     $(event.target).addClass("active");
//     loadunit();
//   }
// });

// $("#country").click(function(event){
//   if($(event.target).attr('class') == 'countrylist'){
//       clearValues('country');
//   $('.'+$(event.target).attr('class')).each( function( index, el ) {
//     $(el).removeClass( "active" );
//   });
//   $(event.target).addClass("active");
//   }

//   var str='';
//   $('#businessgroup').empty();
//   for(var businessgroup in businessgroupsList){
//       str += '<li id="'+businessgroupsList[businessgroup]["business_group_id"]+'" class="businessgrouplist" >'+businessgroupsList[businessgroup]["business_group_name"]+'</li>';
//   }
//   $('#businessgroup').append(str);

//   var str1='';
//   legalentityul.empty();
//   for(var legalentity in legalentitiesList){
//     if(legalentitiesList[legalentity]["business_group_id"] == null){
//       str1 += '<li id="'+legalentitiesList[legalentity]["legal_entity_id"]+'" class="legalentitylist" >'+legalentitiesList[legalentity]["legal_entity_name"]+'</li>';
//     }
//   }
//   legalentityul.append(str1);
// });


// $("#domain").click(function(event){
//   if($(event.target).attr('class') == 'domainlist'){
//     $('.'+$(event.target).attr('class')).each( function( index, el ) {
//       $(el).removeClass( "active" );
//     });
//     $(event.target).addClass("active");
//   }

//   var str='';
//   var pastRecordsDomainId = parseInt(event.target.id);
//   $('#act').empty();
//   for(act in actList){
//     var domainAct = actList[act];
//     if(act == pastRecordsDomainId){
//       for(var i=0; i < domainAct.length; i++){
//         str += '<li id="'+domainAct[i]+'" class="actlist" >'+domainAct[i]+'</li>';
//       }
//     }
//   }
//   $('#act').append(str);
//   $('ul.setup-panel li:eq(2)').addClass('disabled');
// });

// $("#act").click(function(event){
//   if($(event.target).attr('class') == 'actlist'){
//     $('.'+$(event.target).attr('class')).each( function( index, el ) {
//       $(el).removeClass( "active" );
//     });
//     $(event.target).addClass("active");
//   }
//   $('ul.setup-panel li:eq(2)').addClass('disabled');
// });

// $("#frequency").click(function(event){
//   if($(event.target).attr('class') == 'frequencylist'){
//     $('.'+$(event.target).attr('class')).each( function( index, el ) {
//       $(el).removeClass( "active" );
//     });
//     $(event.target).addClass("active");
//   }
//   $('ul.setup-panel li:eq(2)').addClass('disabled');
// });


function pageControls(){
  NextButton.click(function() {
        //$('.tbody-compliance-list').empty();
        CURRENT_TAB += 1;
        showTab();
    });
    PreviousButton.click(function() {
        $(".total_count_view").hide();
        CURRENT_TAB = CURRENT_TAB - 1;
        showTab();
    });
    ShowMore.click(function() {
        callAPI(GET_COMPLIANCE);
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


            // var le_id = legalentityul.find("li.active").attr("id");
            // var d_id = domainul.find("li.active").attr("id");
            // client_mirror.getComplianceTotalToAssign(
            //     parseInt(le_id), ACTIVE_UNITS, parseInt(d_id), ACTIVE_FREQUENCY, 
            //     function(error, data) {
            //         if (error == null) {
            //           totalRecord = data.r_count;
            //           callAPI(GET_COMPLIANCE);
            //             hideall();
            //             enabletabevent(2);
            //             $('.tab-step-2').addClass('active')
            //             $('#tab2').addClass('active in');
            //             $('#tab2').show();
            //             PreviousButton.show();
            //             NextButton.show();
            //         } else {
            //             displayMessage(error);
            //             hideLoader();
            //             CURRENT_TAB -= 1;
            //             return false;
            //         }
            //     }
            // );
        }
    } else if (CURRENT_TAB == 3) {

        if (validateSecondTab() == false) {
            CURRENT_TAB -= 1;
            return false;
        } else {

          //displayLoader();
          var le_id = null, u_id = null, d_id = null, actname = null, freqname = null;

          le_id = legalentityul.find("li.active").attr("id");
          u_id = unitul.find("li.active").attr("id");
          d_id = domainul.find("li.active").attr("id");
          actname = actul.find("li.active").text();
          if(frequencyul.find('li.active').attr('id') != undefined) {
              freqname = frequencyul.find("li.active").attr("id");  
          }
          


 // var pastRecordsUnitId = null;
 //  var pastRecordsDomainId = null;
 //  var pastRecordsActId = null;
 //  var pastRecordsFrequencyId = null;
 //  //var pastRecordsCountryId = null;  
 //  console.log("frequencyul.find('.active').attr('id') --"+frequencyul.find('.active').attr('id') );
 //  //if($('.countrylist.active').attr('id') != undefined) pastRecordsCountryId = parseInt($('.countrylist.active').attr('id'));
 //  if(unitul.find('.active').attr('id') != undefined) pastRecordsUnitId = parseInt(unitul.find('.active').attr('id'));
 //  if(domainul.find('.active').attr('id') != undefined) pastRecordsDomainId = parseInt(domainul.find('.active').attr('id'));
 //  if(actul.find('.active').attr('id') != undefined) pastRecordsActId = actul.find('.active').attr('id');
 //  if(frequencyul.find('.active').attr('id') != undefined) pastRecordsFrequencyId = frequencyul.find('.active').attr('id');

          client_mirror.getStatutoriesByUnit(
                parseInt(le_id), parseInt(u_id), parseInt(d_id), actname, freqname, startcount,
                function(error, data) {
                    if (error == null) {                      
                        hideall();
                        //displayLoader();
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
function load_firstwizard(){
  //$('#businessgroup').empty();
  //legalentityul.empty();
  divisionul.empty();
  categoryul.empty();
  unitul.empty();
  //loadDivision();
  // var str='';
  // $('#country').empty();
  //   for(var country in countriesList){
  //     if(countriesList[country]["is_active"] == true){
  //     str += '<li id="'+countriesList[country]["country_id"]+'" class="countrylist">'+countriesList[country]["country_name"]+'</li>';
  //   }
  // }
  // $('#country').append(str);

  // $('#assignee_unit').empty();
  // $("#assignee_unit").append('<option value=""> Select </option>');
  // $("#assignee_unit").append('<option value="all"> All </option>');
  // for (var unitList in unitsList) {
  //   var option = $("<option></option>");
  //   option.val(unitsList[unitList]["unit_id"]);
  //   option.text(unitsList[unitList]["unit_name"]);
  //   $("#assignee_unit").append(option);
  // }

  // $('#concurrence_unit').empty();
  // $("#concurrence_unit").append('<option value=""> Select </option>');
  // $("#concurrence_unit").append('<option value="all"> All </option>');
  // for (var unitList in unitsList) {
  //   var option = $("<option></option>");
  //   option.val(unitsList[unitList]["unit_id"]);
  //   option.text(unitsList[unitList]["unit_name"]);
  //   $("#concurrence_unit").append(option);
  // }

  // $('#approval_unit').empty();
  // $("#approval_unit").append('<option value=""> Select </option>');
  // $("#approval_unit").append('<option value="all"> All </option>');
  // for (var unitList in unitsList) {
  //   var option = $("<option></option>");
  //   option.val(unitsList[unitList]["unit_id"]);
  //   option.text(unitsList[unitList]["unit_name"]);
  //   $("#approval_unit").append(option);
  // }
}

function validateFirstTab() {
    var le_id = legalentityul.find("li.active").attr("id");
    var u_id = unitul.find("li.active").attr("id");

    if(le_id == undefined) {
        displayMessage(message.legalentity_required)
        return false;
    }
    // else if (d_id == undefined) {
    //     displayMessage(message.domain_required)
    //     return false;
    // }
    else if(u_id == undefined) {
        displayMessage(message.unit_required);
        return false;
    }
    // else if (ACTIVE_FREQUENCY.length == 0) {
    //     displayMessage(message.compliancefrequency_required)
    //     return false;
    // } 
    else {
      LastAct = '';
      SCOUNT = 1;
      ACOUNT = 1;
      return true;
    }
};

function validateSecondTab(){
  var d_id = domainul.find("li.active").attr("id");
  var f_id = frequencyul.find("li.active").attr("id");

  if(d_id == undefined) {
      displayMessage(message.domain_required);
      return false;
  }
  else if(f_id == undefined) {
      displayMessage(message.compliancefrequency_required);
      return false; 
  }
  else {
    LastAct = '';
    SCOUNT = 1;
    ACOUNT = 1;
    return true;
  }
}



function getPastRecords () {
  function onSuccess(data){
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
    //load_firstwizard();
    hideLoader();
  }
  function onFailure(error){
    hideLoader();
  }
  client_mirror.getPastRecordsFormData(parseInt(LE_ID),
    function (error, response) {
      if (error == null){
        onSuccess(response);
      }
      else {
        onFailure(error);
      }
    }
  );
}

function getLegalEntity(){
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
  $('#' + levelvalue + ' li').each(function (index, el) {
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
    frequencyul.empty(); 
  }
  else if (levelvalue == 'division') {  
    categoryul.empty();
  }else if (levelvalue == 'category') {
    ACTIVE_UNITS = [];
    unitul.empty();
  }else if (levelvalue == 'unit') {
    ACTIVE_FREQUENCY = [];
  }else if(levelvalue == 'domain'){
    actul.empty();
  }

}

function loadChild(levelvalue) {
  if (levelvalue == 'legalentity') {
    getPastRecords();
  }
  else if(levelvalue == 'division') {  
    loadCategory();
  }
  else if(levelvalue == 'category') {
    loadUnit();
    //callAPI(WIZARD_ONE_UNIT_FILTER);
  }else if(levelvalue == 'unit') {
    
  }else if(levelvalue == 'domain'){
    loadAct();
  }
}


//initialization & master list filter
$(document).ready(function () {
  //getPastRecords ();
  getLegalEntity();
  pageControls();

  $("#filter_domain").keyup( function() {
    var filter = $("#filter_domain").val().toLowerCase();
    var lis = document.getElementsByClassName('domainlist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_act").keyup( function() {
    var filter = $("#filter_act").val().toLowerCase();
    var lis = document.getElementsByClassName('actlist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_frequency").keyup( function() {
    var filter = $("#filter_frequency").val().toLowerCase();
    var lis = document.getElementsByClassName('frequencylist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });


  // $("#filter_country").keyup( function() {
  //   var filter = $("#filter_country").val().toLowerCase();
  //   var lis = document.getElementsByClassName('countrylist');
  //   for (var i = 0; i < lis.length; i++) {
  //     var name = lis[i].innerHTML;
  //     if (~name.toLowerCase().indexOf(filter))
  //       lis[i].style.display = 'list-item';
  //     else
  //       lis[i].style.display = 'none';
  //   }
  // });

  // $("#filter_businessgroup").keyup( function() {
  //   var filter = $("#filter_businessgroup").val().toLowerCase();
  //   var lis = document.getElementsByClassName('businessgrouplist');
  //   for (var i = 0; i < lis.length; i++) {
  //     var name = lis[i].innerHTML;
  //     if (~name.toLowerCase().indexOf(filter))
  //       lis[i].style.display = 'list-item';
  //     else
  //       lis[i].style.display = 'none';
  //   }
  // });

  $("#filter_legalentity").keyup( function() {
    var filter = $("#filter_legalentity").val().toLowerCase();
    var lis = document.getElementsByClassName('legalentitylist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

  $("#filter_division").keyup( function() {
    var filter = $("#filter_division").val().toLowerCase();
    var lis = document.getElementsByClassName('divisionlist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });


  $("#filter_unit").keyup( function() {
    var filter = $("#filter_unit").val().toLowerCase();
    var lis = document.getElementsByClassName('unitlist');
    for (var i = 0; i < lis.length; i++) {
      var name = lis[i].innerHTML;
      if (~name.toLowerCase().indexOf(filter))
        lis[i].style.display = 'list-item';
      else
        lis[i].style.display = 'none';
    }
  });

});

//tool tip initialization
// $( document ).tooltip({
//     position: {
//         my: "center bottom-20",
//         at: "center top",
//         using: function( position, feedback ) {
//             $( this ).css( position );
//             $( "<div>" )
//                 .addClass( "arrow" )
//                 .addClass( feedback.vertical )
//                 .addClass( feedback.horizontal )
//                 .appendTo( this );
//         }
//     }
// });