#!/usr/bin/python

import traceback
import json

from time import time

from valarie.dao.document import Collection
from valarie.model.kvstore import set as set_kv

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def cpu(self, cli):
        status, stdout, stderr = cli.system("cat /proc/loadavg", return_tuple = True)

        assert status == 0, stdout + stderr
        
        substrs = stdout.strip().split(' ')
        
        procstats = {
            "avg_1" : float(substrs[0]),
            "avg_5" : float(substrs[1]),
            "avg_10" : float(substrs[2]),
            "timestamp" : time()
        }
        
        set_kv("procstats", procstats)
        
        metric = Collection("metrics").get_object()
        
        metric.object["timestamp"] = time()
        metric.object["avg_1"] = float(substrs[0])
        metric.object["avg_5"] = float(substrs[1])
        metric.object["avg_10"] = float(substrs[2])
        metric.object["type"] = "localhost cpu load"
            
        metric.set()
        
        self.output.append(json.dumps(metric.object, indent = 4))

    def execute(self, cli):
        try:
            self.cpu(cli)
            self.status = STATUS_SUCCESS
        except:
            self.output.append(traceback.format_exc())
            self.status = STATUS_FAILURE

        return self.status