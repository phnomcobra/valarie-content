#!/usr/bin/python

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            f = cli.file("/tmp/test.txt", "w")
            
            f.write("Here is a bunch of sadfjklhasdfhjklfasdljhkasfdjhlkafsljhk!")
            
            f.close()
            
            f = cli.file("/tmp/test.txt", "r")
            
            self.output.append(str(f.read()))
            
            f.close()
            
            
            self.status = STATUS_SUCCESS
        except Exception:
            self.status = STATUS_EXCEPTION
            self.output.append(traceback.format_exc())
        
        return self.status