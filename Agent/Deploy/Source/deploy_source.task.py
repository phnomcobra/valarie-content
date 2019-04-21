#!/usr/bin/python

import traceback

from valarie.dao.document import Collection

ROOT_OBJUUID = "c054d448-d20c-1dab-7d03-49080e62bb4a"
ROOT_PATH = "/opt"

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def __execute(self, cli, inventory, objuuid, output, pwp):
        current = inventory.get_object(objuuid)

        if "type" in current.object:
            if current.object["type"] == "container":
                dirname = "/".join([pwp, current.object["name"]])
                
                output.append(cli.system("rm -rfv {0}".format(dirname)))
                
                output.append(cli.system("mkdir -pv -m 755 {0}".format(dirname)))
                
                for objuuid in current.object["children"]:
                    self.__execute(cli = cli, \
                                   inventory = inventory, \
                                   objuuid = objuuid, \
                                   output = output, \
                                   pwp = dirname)
            
            elif current.object["type"] == "text file":
                tempname = "/tmp/{0}".format(current.object["name"])
                filename = "/".join([pwp, current.object["name"]])
                
                cli.writef(filename = tempname, body = current.object["body"])
                
                output.append("wrote " + tempname)
                
                output.append(cli.system("mv -v {0} {1}".format(tempname, filename)))
                
                output.append(cli.system("dos2unix {0}".format(filename)))
                
                # These are the driving scripts
                if current.object["name"] in ["aglookup", "kvs", "net", "server", "tvs", "cscexec"]:
                    output.append(cli.system("chmod -v 755 {0}".format(filename)))

    def execute(self, cli):
        try:
            inventory = Collection("inventory")
            
            self.__execute(cli = cli, \
                           inventory = inventory, \
                           objuuid = ROOT_OBJUUID, \
                           output = self.output, \
                           pwp = ROOT_PATH)
            
            self.status = STATUS_SUCCESS
        except:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION
        return self.status