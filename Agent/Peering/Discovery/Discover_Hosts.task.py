#!/usr/bin/python

import urllib2
import json
import traceback
import ssl
import hashlib

from base64 import b64decode

from valarie.model.host import create_host
from valarie.model.container import create_container
from valarie.dao.document import Collection
from valarie.controller.flags import touch_flag

CONSOLE_UUID = "8b91d444-a1d3-8584-b956-39ba482d1759"
PARENT_UUID = "c5615178-2a13-ccdd-e47a-35a5a66666de"

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        inventory = Collection("inventory")
        try:
            request = {
                "type" : "process sync",
                "command" : "hostname"
            }
            
            message = {
                "type" : "create cascade sync",
                "timeout" : 10,
                "request" : request,
                "etags" : [],
                "ftags" : []
            }
            
            h = hashlib.sha256()
            h.update(hashlib.sha256("changeme").hexdigest())
            h.update(json.dumps(message))
            
            headers = {
                'Content-Type' : 'application/json',
                'Signature' : h.hexdigest()
            }
            
            req = urllib2.Request(url = 'https://127.0.0.1:53443/mpi', \
                                  data = json.dumps(message), \
                                  headers = headers)
            
            f = urllib2.urlopen(url = req, \
                                context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
            
            container = create_container(PARENT_UUID, "Discovered Hosts")
            
            for cascade_response in json.loads(f.read()):
                agtuuid = cascade_response["src"]
                hostname = b64decode(cascade_response["response"]["stdout"])
                
                self.output.append("AGTUUID: {0} HOSTNAME: {1}".format(str(agtuuid), str(hostname)))
                
                if agtuuid and hostname:
                    host = create_host(container.objuuid, hostname)
                    host.object["console"] = CONSOLE_UUID
                    host.object["host"] = agtuuid
                    host.set()

            f.close()
            
            touch_flag("inventoryState")
            
            self.status = STATUS_SUCCESS
        except Exception:
            self.status = STATUS_FAILURE
            self.output.append(traceback.format_exc())
        
        return self.status