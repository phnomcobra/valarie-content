#!/usr/bin/python

from valarie.dao.document import Collection as SQLCollection

ROOT_DIR_UUID = "2769a155-2ad8-1639-a595-53dd24042991"

class Task:
    def __init__(self):
        self.output =[]
        self.status = STATUS_NOT_EXECUTED
	        
    def execute(self, cli):
        inventory = SQLCollection("inventory")
        
        functions = cli.AGTCollection("functions")
        
        try:
            container = inventory.get_object(ROOT_DIR_UUID)
            
            for objuuid in container.object["children"]:
                temp = inventory.get_object(objuuid)
                
                if "type" in temp.object:
                    if temp.object["type"] == "text file":
                        function = functions.get_object(temp.object["objuuid"])
                        
                        function.object["name"] = temp.object["name"]
                        function.object["body"] = temp.object["body"]
                        
                        function.set()
                        
                        self.output.append(function.object["name"])
            
            self.status = STATUS_SUCCESS
        except Exception as e:
            self.output.append(str(e))
            self.status = STATUS_EXCEPTION

        return self.status