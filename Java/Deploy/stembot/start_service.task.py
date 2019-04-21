#!/usr/bin/python
################################################################################
# START SERVICE
#
# Justin Dierking
# phnomcobra@gmail.com
# 937 371 6026
#
# 09/16/2018 Original Construction
################################################################################

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        status, stdout, stderr = cli.system("systemctl start stembotj", return_tuple = True)
        if status: 
            self.status = STATUS_FAILURE
            self.output += stderr.split("\n")
        else:
            self.status = STATUS_SUCCESS
            self.output += stdout.split("\n")
       
        return self.status