#!/usr/bin/python

import traceback

from valarie.dao.document import Collection

INIT_OBJUUID = "869080cd-1c41-5e75-2eab-bd26c5d29397"

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            inventory = Collection("inventory")
            
            init = inventory.get_object(INIT_OBJUUID)
            cli.writef(filename = "/tmp/init.js", body = init.object["body"])
            
            self.output.append(cli.system("dos2unix /tmp/init.js"))
            
            self.output.append('<font color="blue">{0}\n</font>'.format(cli.system("cat /tmp/init.js")))
            
            self.output.append(cli.system("mongo stembot /tmp/init.js"))
            self.output.append(cli.system("rm -vf /tmp/init.js"))
            
            self.status = STATUS_INFORMATION
        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status