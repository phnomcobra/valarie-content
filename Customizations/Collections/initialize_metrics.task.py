#!/usr/bin/python
################################################################################
# INITIALIZE METRICS
#
# Justin Dierking
# phnomcobra@gmail.com
# 937 371 6026
#
# 06/10/2018 Original Construction
################################################################################

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            #cli.AGTCollection("metrics").destroy()
            
            metrics = cli.AGTCollection("metrics")
            metrics.create_attribute("type", '["type"]')
            
            self.status = STATUS_SUCCESS
        except Exception:
            self.status = STATUS_EXCEPTION
            self.output.append(traceback.format_exc())
        
        return self.status