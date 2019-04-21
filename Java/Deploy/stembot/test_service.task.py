#!/usr/bin/python

import urllib2
import json
import traceback
import ssl
import hashlib
import httplib

from random import random
from time import sleep, time
from base64 import b64encode, b64decode

from valarie.controller.messaging import add_message

class MPIClient:
    def __init__(self, url, secret_digest):
        self.secret_digest = secret_digest
        self.url = url

    def send_json(self, json_in):
        try:
            return self.__send_json(json_in)
        except:
            pass
        
        sleep(random() * 5.0)
        
        try:
            return self.__send_json(json_in)
        except:
            pass
        
        sleep(random() * 5.0)
        
        return self.__send_json(json_in)

    def __send_json(self, json_in):
        raw_json_in = json.dumps(json_in)
        
        h = hashlib.sha256()
        h.update(self.secret_digest)
        h.update(raw_json_in)
        
        headers = {
            'Content-Type' : 'application/json',
            'Signature' : h.hexdigest()
        }
        
        req = urllib2.Request(url = self.url)
        
        connection = httplib.HTTPSConnection(req.get_host(), context = ssl._create_unverified_context())
        
        connection.request("POST", \
                           req.get_full_url(), \
                           raw_json_in, \
                           headers)
        
        response = connection.getresponse()
        
        signature = response.getheader("Signature")

        raw_json_out = response.read()
        
        h = hashlib.sha256()
        h.update(self.secret_digest)
        h.update(raw_json_out)
        
        if h.hexdigest() != signature:
            add_message("Signature mismatch encountered!")
            add_message("Signature1: {0}".format(str(signature)))
            add_message("Signature2: {0}".format(str(h.hexdigest())))
            add_message("Output:\n{0}".format(str(raw_json_out)))
            
            raise Exception("Signature mismatch encountered!")
        
        json_out = json.loads(raw_json_out)

        return json_out


class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            client = MPIClient(url = "https://{0}:53444/mpi".format(cli.get_remote_host()), \
                               secret_digest = hashlib.sha256("changeme").hexdigest())
            
            
            
            message = {
                "type" : "create info event",
                "isrc" : "3aab7347-a81e-4e23-9e3c-f31017e92f6a"
            }
            
            message = client.send_json(message)
                
            self.output.append(json.dumps(message, indent = 4))
            
            
            '''
            message = {
                "type" : "route advertisement",
                "isrc" : "7086a790-3d31-4ec8-b49e-226c937d3e99",
                "agtuuid" : "7086a790-3d31-4ec8-b49e-226c937d3e99",
                "routes" : [
                    {
                        "agtuuid" : "2f09caa3-df14-439b-8867-6afc6eddf32d",
                        "weight" : 0
                    },
                    {
                        "agtuuid" : "03b96fa0-2390-492f-84e7-c156446aa7b6",
                        "weight" : 1
                    },
                    {
                        "agtuuid" : "03b96fa0-2390-492f-84e7-c156446aa7b6",
                        "weight" : 1
                    }
                ]
            }
            
            message = client.send_json(message)
                
            self.output.append(json.dumps(message, indent = 4))
            '''
            
            message = {
                "dest" : "dbf7d6b0-9f92-4dcc-fc7f-fdc92c31d568",
                "type" : "create info event",
                "isrc" : "3aab7347-a81e-4e23-9e3c-f31017e92f6a"
            }
            
            message = client.send_json(message)
                
            self.output.append(json.dumps(message, indent = 4))
            
            
            
            message = {
                "type" : "pull messages",
                "isrc" : "3aab7347-a81e-4e23-9e3c-f31017e92f6a"
                #"isrc" : "402fc6ea-0aa2-21a8-47ba-e8192ad77027"
            }
            
            message = client.send_json(message)
                
            self.output.append(json.dumps(message, indent = 4))
            
            self.status = STATUS_SUCCESS
        except:
            self.status = STATUS_FAILURE
            self.output.append(traceback.format_exc())
        
        return self.status