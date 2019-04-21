#!/usr/bin/python

import traceback
import json

SCRIPT_BODY = """
from stembot.counters import increment
increment("agt script test")
"""

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            scripts = cli.AGTCollection("scripts")
            
            for script in scripts.find(name = "agt script test"):
                self.output.append(json.dumps(script.object, indent = 4))
                script.destroy()
            
            script = scripts.get_object()
            
            script.object["name"] = "agt script test"
            script.object["enabled"] = True
            script.object["body"] = SCRIPT_BODY
            script.set()
            
            self.status = STATUS_SUCCESS
        except Exception:
            self.status = STATUS_EXCEPTION
            self.output.append(traceback.format_exc())
        
        return self.status