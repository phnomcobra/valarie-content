#!/usr/bin/python

import traceback

from valarie.controller.messaging import add_message
from valarie.controller.flags import touch_flag
from valarie.dao.document import Collection

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            inventory = Collection("inventory")
            
            for objuuid in inventory.find_objuuids():
                o = inventory.get_object(objuuid)
                
                try:
                    del o.object["context"]["new schedule"]
                    o.set()
                    
                    add_message(objuuid + " Removed.")
                except KeyError:
                    add_message(objuuid + " Missing!")

            touch_flag("inventoryState")
            self.status = STATUS_SUCCESS
        except:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status