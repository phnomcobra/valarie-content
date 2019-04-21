#!/usr/bin/python
################################################################################
# TEST PANDAS IMPORT
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
            self.output.append(str(cli.run_function_by_name("test_pandas_import")))
            
            self.status = STATUS_SUCCESS
        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_FAILURE

        return self.status