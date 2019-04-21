var chart = new AmCharts.AmSerialChart();
chart.dataProvider = REPLACE_WITH_JSON;
chart.marginLeft = 10;
chart.categoryField = "X";
chart.synchronizeGrid = true;
chart["export"] = {"enabled" : true};
chart["titles"] = [{"text" : "X"}];
        
var categoryAxis = chart.categoryAxis;
categoryAxis.dashLength = 3;
categoryAxis.minorGridEnabled = true;
categoryAxis.minorGridAlpha = 0.1;
categoryAxis.twoLineMode = true;
categoryAxis.title = "X";

var valueAxis = new AmCharts.ValueAxis();
valueAxis.axisThickness = 2;
valueAxis.title = "Y";
valueAxis.offset = 100;
chart.addValueAxis(valueAxis);
        
var graph = new AmCharts.AmGraph();
graph.valueAxis = valueAxis;
graph.valueField = "Y1";
graph.title = "Y1";
graph.lineThickness = 2;
chart.addGraph(graph);

var chartCursor = new AmCharts.ChartCursor();
chartCursor.cursorAlpha = 0.1;
chartCursor.fullWidth = true;
chartCursor.valueLineBalloonEnabled = true;
chart.addChartCursor(chartCursor);

var chartScrollbar = new AmCharts.ChartScrollbar();
chart.addChartScrollbar(chartScrollbar);
        
var legend = new AmCharts.AmLegend();
legend.marginLeft = 110;
legend.useGraphSettings = true;
chart.addLegend(legend);
        
chart.write(this.parentNode);