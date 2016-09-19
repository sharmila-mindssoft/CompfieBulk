function initialize() {
  function success(status, data) {
    loadIndustriesData(data);
  }
  function failure(status, data) {
  }
  mirror.getIndustryList(success, failure);
}
function loadIndustriesData(industriesList) {
  var sno = 0;
  var title;
  for (var i in industriesList) {    
    var industry = industriesList[i];
    for (var j in industry) {
      var isActive = industry[j].is_active;
      if (isActive == 1) {
        title = 'Active';
      } else {
        title = 'Inacive';
      }
      var tableRow = $('#templates .table-industry-report .table-row');
      var clone = tableRow.clone();
      sno = sno + 1;
      $('.sno', clone).text(sno);
      $('.country-name', clone).text(industry[j].country_name);
      $('.domain-name', clone).text(industry[j].domain_name);
      $('.industry-name', clone).text(industry[j].industry_name);
      $('.is-active', clone).text(title);
      $('.tbody-industry-list').append(clone);
    }
  }
  $('#total-records').html('Total : ' + sno + ' records');
}
$('#search-industry-name').keyup(function () {
  var count = 0;
  var value = this.value.toLowerCase();
  $('table').find('tr:not(:first):not(:last)').each(function (index) {
    if (index === 0)
      return;
    var id = $(this).find('.industry-name').text().toLowerCase();
    $(this).toggle(id.indexOf(value) !== -1);
  });
  count = $('tr:visible').length - 3;
  $('#total-records').html('Total : ' + count + ' records');
});
$('#search-country-name').keyup(function () {
  var count = 0;
  var value = this.value.toLowerCase();
  $('table').find('tr:not(:first):not(:last)').each(function (index) {
    if (index === 0)
      return;
    var id = $(this).find('.country-name').text().toLowerCase();
    $(this).toggle(id.indexOf(value) !== -1);
  });
  count = $('tr:visible').length - 3;
  $('#total-records').html('Total : ' + count + ' records');
});
$('#search-domain-name').keyup(function () {
  var count = 0;
  var value = this.value.toLowerCase();
  $('table').find('tr:not(:first):not(:last)').each(function (index) {
    if (index === 0)
      return;
    var id = $(this).find('.domain-name').text().toLowerCase();
    $(this).toggle(id.indexOf(value) !== -1);
  });
  count = $('tr:visible').length - 3;
  $('#total-records').html('Total : ' + count + ' records');
});

$(function () {
  initialize();
});