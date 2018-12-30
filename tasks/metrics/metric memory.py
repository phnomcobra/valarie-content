#!/usr/bin/python

import traceback
import json

from time import time

from valarie.dao.document import Collection

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def memory(self, cli):
        metric = Collection("metrics").get_object()

        try:
            status, stdout, stderr = cli.system("free -m", return_tuple = True)
            
            lines = str(stdout).split("\n") 
                            
            field_names = [x for x in lines[0].split(" ") if x]
            mem_fields = [x for x in lines[1].split(" ") if x][1:]
            swap_fields = [x for x in lines[2].split(" ") if x][1:]
            
            metric.object = {
                "mem" : {},
                "swap" : {},
                "timestamp" : time(),
                "type" : "localhost memory"
            }
                            
            for i, f in enumerate(mem_fields):
                metric.object["mem"][field_names[i]] = int(f)
                            
            for i, f in enumerate(swap_fields):
                metric.object["swap"][field_names[i]] = int(f)
            
            metric.set()
        except Exception as e:
            metric.destroy()
            
            raise(e)
        
        self.output.append(json.dumps(metric.object, indent = 4))

    def execute(self, cli):
        try:
            self.memory(cli)
            self.status = STATUS_SUCCESS
        except:
            self.output.append(traceback.format_exc())
            self.status = STATUS_FAILURE

        return self.status