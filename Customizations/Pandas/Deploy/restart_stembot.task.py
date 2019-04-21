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

from time import sleep

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            cli.system("service stembot restart")
        except:
            pass
        
        self.status = STATUS_INFORMATION

        return self.status