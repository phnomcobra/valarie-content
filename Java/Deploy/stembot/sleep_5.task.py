#!/usr/bin/python
################################################################################
# STOP SERVICE
#
# Justin Dierking
# phnomcobra@gmail.com
# 937 371 6026
#
# 09/16/2018 Original Construction
################################################################################

from time import sleep

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        sleep(5)
        self.status = STATUS_INFORMATION
        return self.status