$(function() {

    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : sParameterName[1];
            }
        }
    };

    // var startDate = moment().subtract(1, 'year');
    // var endDate = moment();
    var startDate = "20171130";
    var endDate = "20181130";
    if (typeof getUrlParameter('daterange') != "undefined") {
        startDate = getUrlParameter('daterange').split('+-+')[0];
        endDate = getUrlParameter('daterange').split('+-+')[1];
    }

    // $('input[name="daterange"]').daterangepicker({
    //     "startDate": startDate,
    //     "endDate": endDate,
    //     "maxDate": "11/30/2018"
    // }, function(start, end, label) {
    //   console.log('New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')');
    // });



    // var start = moment().subtract(29, 'days');
    // var end = moment();

    $('input[name="daterange"]').daterangepicker({
        "showDropdowns": true,
        "ranges": {
           'Past 6 Months': [moment().subtract(6, 'month'), moment()],
           'Past 1 Year': [moment().subtract(1, 'year'), moment()],
           'Past 2 Year': [moment().subtract(2, 'year'), moment()],
           'Past 3 Year': [moment().subtract(3, 'year'), moment()],
           'Past 5 Year': [moment().subtract(5, 'year'), moment()],
           // 'This Month': [moment().startOf('month'), moment().endOf('month')],
           // 'Today': [moment(), moment()],
           // 'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           // 'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        },
        "locale": {
            "format": "YYYYMMDD",
            "separator": " - ",
            "applyLabel": "Apply",
            "cancelLabel": "Cancel",
            "fromLabel": "From",
            "toLabel": "To",
            "customRangeLabel": "Custom",
            "weekLabel": "W",
            "daysOfWeek": [
            "Su",
            "Mo",
            "Tu",
            "We",
            "Th",
            "Fr",
            "Sa"
            ],
            "monthNames": [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
            ],
            "firstDay": 1
        },
        "alwaysShowCalendars": true,
        "startDate": startDate,
        "endDate": endDate,
        "maxDate": "20301130",
        "minDate": "20050101",
        "opens": "center"
    }, function(start, end, label) {
      console.log("New date range selected: ' + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD') + ' (predefined range: ' + label + ')");
  });
});
