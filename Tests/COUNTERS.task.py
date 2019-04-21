#!/usr/bin/python

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            grid_data = []
            for k, v in cli.get_counters().iteritems():
                grid_data.append([k, v])
            
            for i in range(0, len(grid_data)):
                for j in range(i, len(grid_data)):
                    if grid_data[i][0] > grid_data[j][0]:
                        grid_data[i], grid_data[j] = grid_data[j], grid_data[i]
            
            for row in grid_data:
                self.output.append("{0} : {1}".format(row[0], row[1]))
            
            self.status = STATUS_SUCCESS
        except Exception:
            self.status = STATUS_EXCEPTION
            self.output.append(traceback.format_exc())
        
        return self.status