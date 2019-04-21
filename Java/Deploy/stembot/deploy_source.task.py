import traceback

from valarie.dao.document import Collection
from valarie.model.datastore import File
from valarie.controller.messaging import add_message

ROOT_OBJUUID = "561acd5d-72dc-51d5-b33c-e0ed136bc740"
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
                
                cli.system("rm -rf {0}".format(dirname))
                
                cli.system("mkdir -p -m 755 {0}".format(dirname))
                
                for objuuid in current.object["children"]:
                    self.__execute(cli = cli, \
                                   inventory = inventory, \
                                   objuuid = objuuid, \
                                   output = output, \
                                   pwp = dirname)
                
                add_message(dirname)
            
            elif current.object["type"] == "text file":
                tempname = "/tmp/{0}".format(current.object["name"])
                filename = "/".join([pwp, current.object["name"]])
                
                cli.writef(filename = tempname, body = current.object["body"])
                
                cli.system("mv {0} {1}".format(tempname, filename))
                
                cli.system("dos2unix {0}".format(filename))
                
                add_message(filename)
            
            elif current.object["type"] == "binary file":
                tempname = "/tmp/{0}".format(current.object["name"])
                filename = "/".join([pwp, current.object["name"]])
                
                f = File(current.object["sequuid"])
                
                cli.writebf(filename = tempname, body = f.read())
                cli.system("mv -v {0} {1}".format(tempname, filename))
                
                add_message(filename)

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