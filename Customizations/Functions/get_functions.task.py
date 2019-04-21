#!/usr/bin/python

import json

class Task:
    def __init__(self):
        self.output =[]
        self.status = STATUS_NOT_EXECUTED
	        
    def execute(self, cli):
        try:
            functions = cli.AGTCollection("functions")
            
            for function in functions.find(name = "get_coll_size"):
                o = function.object
                
                o["body"] = "..."
                
                self.output.append(json.dumps(o, indent = 4))

            self.status = STATUS_SUCCESS
        except Exception as e:
            self.output.append(str(e))
            self.status = STATUS_EXCEPTION

        return self.status