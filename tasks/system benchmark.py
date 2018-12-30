#!/usr/bin/python

import traceback

from time import time

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            st = time()
            N = 10
            
            for n in range(N):
                cli.system("hostname")
            
            et = time() - st
            self.output.append("{0} system commands per second.".format(N / et))
            
            self.status = STATUS_SUCCESS
        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status