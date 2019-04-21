#!/usr/bin/python

import urllib2
import json
import traceback
import ssl
import hashlib

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            message = {
                "type" : "delete peers"
            }
            
            h = hashlib.sha256()
            h.update(hashlib.sha256("changeme").hexdigest())
            h.update(json.dumps(message))
            
            headers = {
                'Content-Type' : 'application/json',
                'Signature' : h.hexdigest()
            }
            
            req = urllib2.Request(url = "https://{0}:53443/mpi".format(cli.get_remote_host()), \
                                  data = json.dumps(message), \
                                  headers = headers)
            
            f = urllib2.urlopen(url = req, \
                                context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
            
            self.output.append(f.read())

            f.close()

            self.status = STATUS_SUCCESS
        except Exception:
            self.status = STATUS_FAILURE
            self.output.append(traceback.format_exc())
        
        return self.status