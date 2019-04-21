#!/usr/bin/python

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            self.output.append("Deleting events...")
            
            cli.AGTCollection("events").destroy()

            self.status = STATUS_SUCCESS
        except Exception:
            self.status = STATUS_EXCEPTION
            self.output.append(traceback.format_exc())
        
        return self.status