#!/usr/bin/python

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            self.output.append("Deleting functions...")
            
            functions = cli.AGTCollection("functions")
            
            for function in functions.find():
                if "name" in function.object:
                    self.output.append("deleted {0}".format(function.object["name"]))
                else:
                    self.output.append("deleted {0}".format(function.object["objuuid"]))
                
                function.destroy()

            self.status = STATUS_SUCCESS
        except Exception:
            self.status = STATUS_EXCEPTION
            self.output.append(traceback.format_exc())
        
        return self.status