#!/usr/bin/python

import traceback
import json

from time import time

from valarie.executor.counters import get as get_count, \
                                      set as set_count
from valarie.dao.document import Collection, \
                                 Document

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def database(self, cli):
        status, stdout, stderr = cli.system("du -BK db.sqlite", return_tuple = True)
        
        assert status == 0, stdout + stderr
        
        db_size_k = int(stdout.split("K")[0])
        db_size_o = len(Document().list_objects())
        
        metric = Collection("metrics").get_object()
        
        metric.object["timestamp"] = time()
        metric.object["KB"] = db_size_k
        metric.object["num objects"] = db_size_o
        metric.object["num writes"] = get_count("sql object writes")
        metric.object["num reads"] = get_count("sql object reads")
        metric.object["type"] = "sql objects"
        
        set_count("sql object writes", 0)
        set_count("sql object reads", 0)
            
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