#!/usr/bin/python

import traceback
import hashlib

from valarie.controller.messaging import add_message
from valarie.controller.flags import touch_flag

from valarie.dao.document import Collection
from valarie.dao.utils import sucky_uuid

from valarie.model.datastore import File, create_binary_file
from valarie.model.textfile import create_text_file
from valarie.model.container import create_container
                                 
PARENT_UUID = "cd971363-742a-418e-129b-6277b517646b"

REMOTE_FS_PATH = "/opt/dev5"

TXT_EXTENSIONS = ["py", "html", "pem", "js", "md", "css", "json", "map", "csv", "txt"]
BIN_EXTENSIONS = ["png", "svg", "gif", "jpg", "ttf", "woff", "woff2", "eot"]

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED
        
        self.containers = {
            "containers" : {},
            "objuuid" : PARENT_UUID
        }
    
    def execute(self, cli):
        try:
            # LIFT DIRECTORIES INTO INVENTORY
            status, stdout, stderr = cli.system("find {} -type d".format(REMOTE_FS_PATH), return_tuple = True)
            if status:
                self.output.append(str(stderr))
                self.status = STATUS_FAILURE
                return self.status
            else:
                for dname in stdout.strip().split("\n"):
                    current_container = self.containers
                    
                    sdnames = dname.strip().split("/")
                    
                    parent_objuuid = self.containers["objuuid"]
                    
                    for sdname in sdnames[len(REMOTE_FS_PATH.split("/")) - 1:]:
                        if sdname not in current_container["containers"]:
                            current_container["containers"][sdname] = {
                                "containers" : {},
                                "objuuid" : sucky_uuid()
                            }
                            
                            create_container(parent_objuuid, \
                                             sdname, \
                                             current_container["containers"][sdname]["objuuid"])
                            
                            self.output.append(dname)
                            add_message(dname)

                        parent_objuuid = current_container["containers"][sdname]["objuuid"]
                        
                        current_container = current_container["containers"][sdname]
            
            
            
                
            # LIFT FILES INTO INVENTORY
            status, stdout, stderr = cli.system("find {} -type f".format(REMOTE_FS_PATH), return_tuple = True)
            if status:
                self.output.append(str(stderr))
                self.status = STATUS_FAILURE
                return self.status
            else:
                for fname in stdout.strip().split("\n"):
                    current_container = self.containers
                    
                    sfnames = fname.strip().split("/")
                    
                    parent_objuuid = self.containers["objuuid"]
                    
                    for i, sfname in enumerate(sfnames[len(REMOTE_FS_PATH.split("/")) - 1:]):
                        if i == len(sfnames[len(REMOTE_FS_PATH.split("/")) - 1:]) - 1:
                            fext = sfname.split('.')[-1]
                            
                            if fext in TXT_EXTENSIONS:
                                tf = create_text_file(parent_objuuid, sfname)
                                tf.object["body"] = cli.readf(fname)
                                tf.set()
                                
                                self.output.append(fname)
                                add_message(fname)
                            elif fext in BIN_EXTENSIONS:
                                # binary file inventory object
                                bf = create_binary_file(parent_objuuid, sfname)
                                
                                # data store file
                                df = File(bf.object["sequuid"])
                                
                                sha1hash = hashlib.sha1()
                                
                                chunk = cli.readbf(fname)
                                df.write(chunk)
                                sha1hash.update(chunk)

                                df.close()

                                bf.object["size"] = df.size()
                                bf.object["sha1sum"] = sha1hash.hexdigest()
                                bf.set()
                                
                                self.output.append(fname)
                                add_message(fname)
                        else:
                            parent_objuuid = current_container["containers"][sfname]["objuuid"]
                        
                            current_container = current_container["containers"][sfname]
                        
            touch_flag("inventoryState")
            self.status = STATUS_SUCCESS
        except:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status