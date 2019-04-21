#!/usr/bin/python

import traceback

from valarie.dao.document import Collection

TEST_OBJUUID = "5c86e00e-7182-0970-b89a-e5537c3d7a8b"

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            inventory = Collection("inventory")
            
            test = inventory.get_object(TEST_OBJUUID)
            
            cli.writef(filename = "/tmp/test.js", body = test.object["body"])
            
            self.output.append(cli.system("dos2unix /tmp/test.js"))
            
            self.output.append('<font color="blue">{0}\n</font>'.format(cli.system("cat /tmp/test.js")))
            
            self.output.append(cli.system("mongo stembot /tmp/test.js"))
            
            status, stdout, stderr = cli.system("mongo stembot /tmp/test.js", return_tuple = True)
            if status:
                self.output.append(str(stdout) + str(stderr))
                self.status = STATUS_FAILURE
            else:
                self.output.append(str(stdout) + str(stderr))
                self.status = STATUS_SUCCESS
            
            self.output.append(cli.system("rm -vf /tmp/init.js"))
        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status