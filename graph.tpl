<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jqPlot/1.0.9/jquery.jqplot.min.js"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jqPlot/1.0.9/plugins/jqplot.dateAxisRenderer.js"></script>
<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/jqPlot/1.0.9/jquery.jqplot.min.css"/>

<div id="chart" style="height:300px;"></div>

<script>
$(function() {

  function getData() {
    var data = [[[]]];
    $.ajax({
        async: false,
        url: '/data',
        type: 'GET',
        dataType: 'json',
    }).done(function(json) {
        data = json
    });
    return data;
  };

  var options = {
    title: 'new job positing in Germany',
    axes: {
      xaxis: {
        renderer: $.jqplot.DateAxisRenderer,
        tickOptions: { formatString: '%Y/%m/%d' },
      }
    },
    series: [],
    legend: {
      show: true,
    }  
  };

  var data = getData()
  var titles = data[1]
  for (var i in titles) {
    options.series[i] = { label: titles[i] }
  }
  var jqplot = $.jqplot('chart', data[0], options)
});
</script>
