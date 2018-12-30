#!/usr/bin/python

import traceback

from valarie.dao.document import Collection
from time import time

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED
        self.MAX_AGE = 60 * 60 * 24
    
    def cleanup(self):
        current_time = time()
        
        metrics = Collection("metrics")
        
        for mtruuid in metrics.list_objuuids():
            metric = metrics.get_object(mtruuid)
            
            try:
                if current_time - metric.object["timestamp"] > self.MAX_AGE:
                    metric.destroy()
            except:
                metric.destroy()

    def execute(self, cli):
        try:
            self.cleanup()
            self.status = STATUS_SUCCESS
        except:
            self.output.append(traceback.format_exc())
            self.status = STATUS_FAILURE

        return self.status