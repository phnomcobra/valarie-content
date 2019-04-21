#!/usr/bin/python

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
        
        chart["titles"] = [{"text" : "Localhost Object Usage"}];
        
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
        var valueAxis2 = new AmCharts.ValueAxis();
        valueAxis2.axisThickness = 2;
        valueAxis2.title = "Objects";
        valueAxis2.offset = 100;
        chart.addValueAxis(valueAxis2);
        
        var valueAxis3 = new AmCharts.ValueAxis();
        valueAxis3.axisThickness = 2;
        valueAxis3.title = "Obj/Sec";
        valueAxis3.offset = 0;
        chart.addValueAxis(valueAxis3);
        
        // GRAPH
        graph = new AmCharts.AmGraph();
        graph.valueAxis = valueAxis2;
        graph.valueField = "num objects";
        graph.title = "Objects";
        graph.lineThickness = 2;
        chart.addGraph(graph);
        
        graph = new AmCharts.AmGraph();
        graph.valueAxis = valueAxis3;
        graph.valueField = "num writes";
        graph.title = "Writes";
        graph.lineThickness = 2;
        chart.addGraph(graph);
        
        graph = new AmCharts.AmGraph();
        graph.valueAxis = valueAxis3;
        graph.valueField = "num reads";
        graph.title = "Reads";
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
            
            event = {
                "query" : {
                    "type" : "ram objects"
                }, 
                "collection name" : "metrics"
            }
            
            results = cli.run_function_by_name("get_collection", event)
            
            for result in results:
                if True:
                    grid_data.append({"timestamp" : result["timestamp"], \
                                      "datetime" : strftime('%Y-%m-%d %H:%M:%S', localtime(int(result["timestamp"]))), \
                                      "num objects" : int(result["num objects"]), \
                                      "num writes" : int(result["num writes"]), \
                                      "num reads" : int(result["num reads"])})
            
            # Insertion sort by dictionary key "timestamp"
            for i in range(0, len(grid_data)):
                for j in range(i, len(grid_data)):
                    if int(grid_data[i]["timestamp"]) > int(grid_data[j]["timestamp"]):
                        grid_data[i], grid_data[j] = grid_data[j], grid_data[i]
            
            # Normalize writes and reads
            for i in range(1, len(grid_data)):
                et = grid_data[i]["timestamp"] - grid_data[i - 1]["timestamp"]
                
                grid_data[i]["num writes"] = round(float(grid_data[i]["num writes"]) / et, 3)
                grid_data[i]["num reads"] = round(float(grid_data[i]["num reads"]) / et, 3)
            
            grid_data[0]["num writes"] = 0    
            grid_data[0]["num reads"] = 0
                
            self.output.append(chart_page_1 + json.dumps(grid_data) + chart_page_2)
            
            self.status = STATUS_INFORMATION
        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status