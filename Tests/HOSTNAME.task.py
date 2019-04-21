#!/usr/bin/python

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            status, stdout, stderr = cli.system("hostname", return_tuple = True)
            
            if status:
                self.status = STATUS_FAILURE
                self.output.append(stderr)
            else:
                self.status = STATUS_SUCCESS
                self.output.append(stdout)
        except Exception:
            self.status = STATUS_EXCEPTION
            self.output.append(traceback.format_exc())
        
        return self.status