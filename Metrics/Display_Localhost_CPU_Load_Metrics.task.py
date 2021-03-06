#!/usr/bin/python

import traceback
import json

from time import strftime, localtime

from valarie.dao.document import Collection

chart_page_1 = """<div style="width:inherit;height:calc(100vh - 250px);">
    <img src="/images/throbber.gif" onload='
        var chart;
        var graph;
            
        chart = new AmCharts.AmSerialChart();

        chart.dataProvider = """
chart_page_2 = """;
        chart.marginLeft = 10;
        chart.categoryField = "datetime";
        chart.dataDateFormat = "YYYY/MM/DD JJ:NN";
        
        chart.synchronizeGrid = true; // this makes all axes grid to be at the same intervals
        
        chart["export"] = {"enabled" : true};
        
        chart["titles"] = [{"text" : "Localhost CPU Load"}];
        
        // AXES
        // category
        var categoryAxis = chart.categoryAxis;
        categoryAxis.parseDates = true; // as our data is date-based, we set parseDates to true
        categoryAxis.minPeriod = "mm"; // our data is yearly, so we set minPeriod to YYYY
        categoryAxis.dashLength = 3;
        categoryAxis.minorGridEnabled = true;
        categoryAxis.minorGridAlpha = 0.1;
        categoryAxis.twoLineMode = true;
        categoryAxis.title = "Time";

        // value
        var valueAxis1 = new AmCharts.ValueAxis();
        valueAxis1.axisThickness = 2;
        valueAxis1.title = "Load";
        chart.addValueAxis(valueAxis1);
        
        // GRAPH
        graph = new AmCharts.AmGraph();
        graph.valueAxis = valueAxis1;
        graph.valueField = "avg_1";
        graph.title = "1 Min Avg";
        graph.lineThickness = 2;
        chart.addGraph(graph);
        
        graph = new AmCharts.AmGraph();
        graph.valueAxis = valueAxis1;
        graph.valueField = "avg_5";
        graph.title = "5 Min Avg";
        graph.lineThickness = 2;
        chart.addGraph(graph);
        
        graph = new AmCharts.AmGraph();
        graph.valueAxis = valueAxis1;
        graph.valueField = "avg_10";
        graph.title = "10 Min Avg";
        graph.lineThickness = 2;
        chart.addGraph(graph);

        // CURSOR
        var chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorAlpha = 0.1;
        chartCursor.fullWidth = true;
        chartCursor.valueLineBalloonEnabled = true;
        chartCursor.categoryBalloonDateFormat = "YYYY/MM/DD JJ:NN";
        chart.addChartCursor(chartCursor);

        // SCROLLBAR
        var chartScrollbar = new AmCharts.ChartScrollbar();
        chart.addChartScrollbar(chartScrollbar);
        
        // LEGEND
        var legend = new AmCharts.AmLegend();
        legend.marginLeft = 110;
        legend.useGraphSettings = true;
        chart.addLegend(legend);
        
        // WRITE
        chart.write(this.parentNode);
    '>
</div>"""

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            grid_data = []
            
            metrics = Collection("metrics")
            
            for mtruuid in metrics.find_objuuids(type = "localhost cpu load"):
                metric = metrics.get_object(mtruuid)
                
                if True:
                    grid_data.append({"timestamp" : metric.object["timestamp"], \
                                      "datetime" : strftime('%Y-%m-%d %H:%M:%S', localtime(int(metric.object["timestamp"]))), \
                                      "avg_1" : round(metric.object["avg_1"], 3), \
                                      "avg_5" : round(metric.object["avg_5"], 3), \
                                      "avg_10" : round(metric.object["avg_10"], 3)})
            
            # Insertion sort by dictionary key "timestamp"
            for i in range(0, len(grid_data)):
                for j in range(i, len(grid_data)):
                    if int(grid_data[i]["timestamp"]) > int(grid_data[j]["timestamp"]):
                        grid_data[i], grid_data[j] = grid_data[j], grid_data[i]
                
            self.output.append(chart_page_1 + json.dumps(grid_data) + chart_page_2)
            
            self.status = STATUS_INFORMATION
        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status