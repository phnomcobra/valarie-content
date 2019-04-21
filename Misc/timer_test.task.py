#!/usr/bin/python

import traceback

from threading import Timer
from time import time, sleep

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def test(self):
        sleep(1)
        
        self.output.append(str(time()))

    def execute(self, cli):
        try:
            
            t = Timer(1.0, self.test)
            
            t.start()
            sleep(1.5)
            t.cancel()
            t.join()
            t.cancel()
            
            
            self.status = STATUS_SUCCESS
        except:
            self.output.append(traceback.format_exc())
            self.status = STATUS_FAILURE

        return self.status