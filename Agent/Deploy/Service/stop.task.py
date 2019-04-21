#!/usr/bin/python

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        status, stdout, stderr = cli.system("systemctl stop stembot", return_tuple = True)
        if status: 
            self.status = STATUS_FAILURE
            self.output += stderr.split("\n")
        else:
            self.status = STATUS_SUCCESS
            self.output += stdout.split("\n")
       
        return self.status