import traceback

from valarie.dao.document import Collection
from valarie.model.datastore import File
from valarie.controller.messaging import add_message

ROOT_OBJUUID = "013b8780-3256-32c6-1404-4230e61a3b74"
ROOT_PATH = "/root/valarie-content"

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def __execute(self, cli, inventory, objuuid, output, pwp):
        current = inventory.get_object(objuuid)

        if "type" in current.object:
            if current.object["type"] == "container":
                dirname = "/".join([pwp, current.object["name"]])
                dirname = dirname.replace(" ", "_")
                
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
                tempname = "/tmp/tmp.dat"
                filename = "/".join([pwp, current.object["name"]])
                filename = filename.replace(" ", "_")
                
                cli.writef(filename = tempname, body = current.object["body"])
                
                cli.system("mv {0} {1}".format(tempname, filename))
                
                cli.system("dos2unix {0}".format(filename))
                
                add_message(filename)
            
            elif current.object["type"] == "task":
                tempname = "/tmp/tmp.dat"
                filename = "/".join([pwp, current.object["name"] + ".task.py"])
                filename = filename.replace(" ", "_")
                
                cli.writef(filename = tempname, body = current.object["body"])
                
                cli.system("mv {0} {1}".format(tempname, filename))
                
                cli.system("dos2unix {0}".format(filename))
                
                add_message(filename)
            
            elif current.object["type"] == "console":
                tempname = "/tmp/tmp.dat"
                filename = "/".join([pwp, current.object["name"] + ".console.py"])
                filename = filename.replace(" ", "_")
                
                cli.writef(filename = tempname, body = current.object["body"])
                
                cli.system("mv {0} {1}".format(tempname, filename))
                
                cli.system("dos2unix {0}".format(filename))
                
                add_message(filename)
            
            '''
            elif current.object["type"] == "binary file":
                tempname = "/tmp/tmp.dat"
                filename = "/".join([pwp, current.object["name"]])
                filename = filename.replace(" ", "_")
                
                f = File(current.object["sequuid"])
                
                cli.writebf(filename = tempname, body = f.read())
                cli.system("mv -v {0} {1}".format(tempname, filename))
                
                add_message(filename)
            '''
            
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