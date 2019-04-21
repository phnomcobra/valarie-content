#!/usr/bin/python
################################################################################
# CREATE SERVER CERT DIRECTORY
#
# Justin Dierking
# phnomcobra@gmail.com
# 937 371 6026
#
# 09/15/2018 Original Construction
################################################################################

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            self.output.append(cli.system("mkdir -v /tmp/server"))
            
            self.status = STATUS_INFORMATION
        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status