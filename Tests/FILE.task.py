#!/usr/bin/python

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            cli.writebf("/tmp/test1.txt", "Here is a bunch of sadfjklhasdfhjklfasdljhkasfdjhlkafsljhk!")
            cli.writebf("/tmp/test2.txt", cli.readbf("/tmp/test1.txt"))
            
            md5sum1 = cli.system("md5sum /tmp/test1.txt").split(" ")[0]
            md5sum2 = cli.system("md5sum /tmp/test2.txt").split(" ")[0]
            
            self.output.append(cli.system("ls -lh /tmp/test1.txt").strip())
            self.output.append(md5sum1)
            self.output.append(cli.system("hexdump -v /tmp/test1.txt"))
            
            self.output.append(cli.system("ls -lh /tmp/test2.txt").strip())
            self.output.append(md5sum2)
            self.output.append(cli.system("hexdump -v /tmp/test2.txt"))
            
            if(md5sum1 == md5sum2):
                self.status = STATUS_SUCCESS
            else:        
                self.status = STATUS_FAILURE
        except Exception:
            self.status = STATUS_EXCEPTION
            self.output.append(traceback.format_exc())
        
        return self.status