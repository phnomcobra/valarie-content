#!/usr/bin/python
################################################################################
# CHART TEST
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# 614 692 2050
#
# 05/08/2017 Original Construction
################################################################################

import traceback
import json
from time import strftime, localtime

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
        
        chart["titles"] = [{"text" : "Localhost Memory"}];
        
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
        valueAxis1.title = "MB";
        chart.addValueAxis(valueAxis1);
        
        // GRAPH
        graph1 = new AmCharts.AmGraph();
        //graph1.type = "smoothedLine"; // this line makes the graph smoothed line.
        graph1.valueAxis = valueAxis1;
        graph1.valueField = "free";
        graph1.title = "free";
        //graph1.bullet = "round";
        //graph1.fillAlphas = 0.2;
        graph1.lineThickness = 2;
        chart.addGraph(graph1);
        
        graph2 = new AmCharts.AmGraph();
        //graph2.type = "smoothedLine"; // this line makes the graph smoothed line.
        graph2.valueAxis = valueAxis1;
        graph2.valueField = "used";
        graph2.title = "used";
        //graph2.bullet = "round";
        //graph2.fillAlphas = 0.2;
        graph2.lineThickness = 2;
        chart.addGraph(graph2);
        
        graph3 = new AmCharts.AmGraph();
        //graph3.type = "smoothedLine"; // this line makes the graph smoothed line.
        graph3.valueAxis = valueAxis1;
        graph3.valueField = "cache";
        graph3.title = "cache";
        //graph3.bullet = "round";
        //graph3.fillAlphas = 0.2;
        graph3.lineThickness = 2;
        chart.addGraph(graph3);
        
        graph4 = new AmCharts.AmGraph();
        //graph4.type = "smoothedLine"; // this line makes the graph smoothed line.
        graph4.valueAxis = valueAxis1;
        graph4.valueField = "free+cache";
        graph4.title = "free+cache";
        //graph4.bullet = "round";
        //graph4.fillAlphas = 0.2;
        graph4.lineThickness = 2;
        chart.addGraph(graph4);
        
        graph5 = new AmCharts.AmGraph();
        //graph5.type = "smoothedLine"; // this line makes the graph smoothed line.
        graph5.valueAxis = valueAxis1;
        graph5.valueField = "total";
        graph5.title = "total";
        //graph5.bullet = "round";
        //graph5.fillAlphas = 0.2;
        graph5.lineThickness = 2;
        chart.addGraph(graph5);
        
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
            
            event = {
                "query" : {
                    "type" : "localhost memory"
                }, 
                "collection name" : "metrics"
            }
            
            results = cli.run_function_by_name("get_collection", event)
            
            for result in results:
                if True:
                    grid_data.append({"timestamp" : result["timestamp"], \
                                      "total" : int(result["mem"]["total"]), \
                                      "used" : int(result["mem"]["used"]), \
                                      "free" : int(result["mem"]["free"]), \
                                      "cache" : int(result["mem"]["buff/cache"]), \
                                      "free+cache" : int(result["mem"]["buff/cache"]) + int(result["mem"]["free"]), \
                                      "datetime" : strftime('%Y-%m-%d %H:%M:%S', localtime(int(result["timestamp"])))})
            
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