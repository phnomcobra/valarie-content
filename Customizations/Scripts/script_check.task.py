#!/usr/bin/python

import traceback
import json

from time import strftime, localtime

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            scripts = cli.AGTCollections("scripts", timeout = 15)
            
            self.status = STATUS_INFORMATION

            for script in scripts.find():
                if "name" in script.object:
                    self.output.append("<b>NAME:</b> {0}".format(script.object["name"]))
                
                self.output.append("<b>OBJUUID:</b> {0}".format(script.objuuid))
                self.output.append("<b>AGTUUID:</b> {0}".format(script.agtuuid))
                
                if "status" in script.object:
                    self.output.append("<b>STATUS:</b> {0}".format(script.object["status"]))
                else:
                    self.output.append("<b>STATUS:</b> None")
                    
                self.output.append("")
                
                cron = {}
                for key in ["enabled", "minutes", "hours", "dayofmonth", "dayofweek", "year"]:
                    if key in script.object:
                        cron[key] = script.object[key]
                self.output.append("<b>CRON:</b>")
                self.output.append(json.dumps(cron, indent = 4))
                
                if "body" in script.object:
                    self.output.append("")
                    
                    self.output.append("<b>BODY:</b>")
                    
                    for i, line in enumerate(script.object["body"].split("\n")):
                        self.output.append("{0:03d}: <font color='blue'>{1}</font>".format(i + 1, line))
                
                if "exception" in script.object:
                    self.output.append("")
                    
                    self.output.append("<b>EXCEPTION:</b>")
                    
                    for line in script.object["exception"].split("\n"):
                        self.output.append("<font color='red'>{0}</font>".format(line))
                
                self.output.append("")
                self.output.append("")
                self.output.append("")

        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status