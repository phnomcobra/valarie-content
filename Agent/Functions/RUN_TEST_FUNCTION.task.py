#!/usr/bin/python
################################################################################
# RUN TEST FUNCTION
#
# Justin L. Dierking
# justin.l.dierking.civ@mail.mil
# 614 692 2050
#
# 01/23/2018 Original Construction
################################################################################

import traceback
import json

class Task:
    def __init__(self):
        self.output =[]
        self.status = STATUS_NOT_EXECUTED
	        
    def execute(self, cli):
        try:
            self.output.append(cli.run_function_by_name("test", {}))
            self.status = STATUS_SUCCESS
        except:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status