#!/usr/bin/python

import traceback

from time import time

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            events = cli.AGTCollection("events")
            
            st = time()
            N = 10
            
            for n in range(N):
                event = events.get_object("07580649-0e79-0707-e805-b27d91b63104")
                event.destroy()

            et = time() - st
            self.output.append("{0} object load/stores per second.".format(N / et))
            
            self.status = STATUS_SUCCESS
        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status