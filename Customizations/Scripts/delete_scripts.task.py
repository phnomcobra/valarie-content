#!/usr/bin/python
################################################################################
# DELETE SCRIPTS
#
# Justin Dierking
# phnomcobra@gmail.com
# 937 371 6026
#
# 06/10/2018 Original Construction
################################################################################

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            self.output.append("Deleting scripts...")
            
            scripts = cli.AGTCollection("scripts")
            
            for script in scripts.find():
                if "name" in script.object:
                    self.output.append("deleted {0}".format(script.object["name"]))
                else:
                    self.output.append("deleted {0}".format(script.object["objuuid"]))
                
                script.destroy()

            self.status = STATUS_SUCCESS
        except Exception:
            self.status = STATUS_EXCEPTION
            self.output.append(traceback.format_exc())
        
        return self.status