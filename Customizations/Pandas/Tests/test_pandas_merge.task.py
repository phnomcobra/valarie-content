#!/usr/bin/python
################################################################################
# NEW TASK
#
# Justin Dierking
# phnomcobra@gmail.com
# 937 371 6026
#
# 11/27/2018 Original Construction
################################################################################

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            self.output.append(str(cli.run_function_by_name("test_pandas_merge")))
            
            self.status = STATUS_SUCCESS
        except:
            self.output.append(traceback.format_exc())
            self.status = STATUS_FAILURE

        return self.status