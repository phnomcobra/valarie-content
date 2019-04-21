#!/usr/bin/python

import traceback
import json

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            keys = cli.AGTCollection("kvstore")
            
            self.status = STATUS_SUCCESS
            
            for key in keys.find():
                #key.set()
                self.output.append(json.dumps(key.object, indent = 4))
                
        except Exception:
            self.status = STATUS_EXCEPTION
            self.output.append(traceback.format_exc())
        
        return self.status