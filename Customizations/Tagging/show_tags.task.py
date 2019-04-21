#!/usr/bin/python
################################################################################
# DOCUMENTS
#
# Justin Dierking
# justin.l.dierking.civ@mail.mil
# 614 692 2050
#
# 04/22/2018 Original Construction
################################################################################

import traceback
import json

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            keys = cli.AGTCollections("tags")
            
            self.status = STATUS_SUCCESS
            
            for key in keys.find():
                #key.set()
                self.output.append(json.dumps(key.object, indent = 4))

        except Exception:
            self.status = STATUS_EXCEPTION
            self.output.append(traceback.format_exc())
        
        return self.status