#!/usr/bin/python

import traceback
import json

from time import time

from valarie.dao.document import Collection
from valarie.dao.ramdocument import Document
from valarie.executor.counters import get as get_count, \
                                      set as set_count

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def database(self, cli):
        db_size_o = len(Document().list_objects())
        
        metric = Collection("metrics").get_object()
        
        metric.object["timestamp"] = time()
        metric.object["num objects"] = db_size_o
        metric.object["num writes"] = get_count("ram object writes")
        metric.object["num reads"] = get_count("ram object reads")
        metric.object["type"] = "ram objects"
        
        set_count("ram object writes", 0)
        set_count("ram object reads", 0)
            
        metric.set()
        
        self.output.append(json.dumps(metric.object, indent = 4))
    
    def execute(self, cli):
        try:
            self.database(cli)
            self.status = STATUS_SUCCESS
        except:
            self.output.append(traceback.format_exc())
            self.status = STATUS_FAILURE

        return self.status