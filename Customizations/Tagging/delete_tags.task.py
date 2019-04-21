#!/usr/bin/python
################################################################################
# DELETE TAGS
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
            self.output.append("Deleting tags...")
            
            tags = cli.AGTCollection("tags")
            
            for tag in tags.find():
                if "value" in tag.object:
                    self.output.append("deleted {0}".format(tag.object["value"]))
                else:
                    self.output.append("deleted {0}".format(tag.object["objuuid"]))
                
                tag.destroy()

            self.status = STATUS_SUCCESS
        except Exception:
            self.status = STATUS_EXCEPTION
            self.output.append(traceback.format_exc())
        
        return self.status