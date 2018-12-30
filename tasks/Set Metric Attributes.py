#!/usr/bin/python

import traceback

from valarie.dao.document import Collection

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            metrics = Collection("metrics")
            metrics.create_attribute("type", '["type"]')
            
            self.status = STATUS_SUCCESS
        except:
            self.output.append(traceback.format_exc())
            self.status = STATUS_FAILURE

        return self.status