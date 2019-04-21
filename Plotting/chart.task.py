#!/usr/bin/python

import traceback
import json

from math import sin

from valarie.dao.document import Collection

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED
        
        self.html_template_objuuid = "40068590-c241-257e-d293-5a459ecc2e43"
        self.js_template_objuuid = "9e2a5755-670b-3ca0-e99a-d18a7c5208ce"

    def execute(self, cli):
        try:
            grid_data = []
            
            inventory = Collection("inventory")
            
            for i in range(1000):
                x = float(i) / 100
                
                grid_data.append({
                    "X" : x, 
                    "Y1" : sin(x)
                })
                
            # Insertion sort
            for i in range(0, len(grid_data)):
                for j in range(i, len(grid_data)):
                    if int(grid_data[i]["X"]) > int(grid_data[j]["X"]):
                        grid_data[i], grid_data[j] = grid_data[j], grid_data[i]
            
            html_template = inventory.get_object(self.html_template_objuuid).object["body"]
            js_template = inventory.get_object(self.js_template_objuuid).object["body"]
            
            page = html_template.replace("REPLACE_WITH_JS", js_template) \
                                .replace("REPLACE_WITH_JSON", json.dumps(grid_data))
            
            self.output.append(page)
            
            self.status = STATUS_INFORMATION
        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status