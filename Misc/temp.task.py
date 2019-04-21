#!/usr/bin/python
################################################################################
# NEW TASK
#
# Justin Dierking
# phnomcobra@gmail.com
# 937 371 6026
#
# 10/14/2018 Original Construction
################################################################################

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            status, stdout, stderr = cli.system("free -m", return_tuple = True)
            if status:
                self.output.append(str(stderr))
                self.status = STATUS_FAILURE
            else:
                self.output.append(str(stdout))
                
                for line in str(stdout).split("\n"): 
                    substrs = [x for x in line.split(" ") if x]
                    self.output.append(str(substrs))
                
                self.status = STATUS_SUCCESS
        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status