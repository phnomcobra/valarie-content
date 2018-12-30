#!/usr/bin/python

import traceback
import json

from time import time

from valarie.dao.document import Collection
from valarie.model.kvstore import get as get_kv, \
                                  set as set_kv

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def network(self, cli):
        try:
            netstats = get_kv("netstats")
            
            tx0 = netstats["tx"]
            rx0 = netstats["rx"]
            
            time0 = netstats["timestamp"]
            
            for i in range(len(tx0)):
                int(tx0[i]) + int(rx0[i])
        except:
            tx0 = []
            rx0 = []
            time0 = 0.0
        
        status, stdout, stderr = cli.system("ifconfig", return_tuple = True)
        
        assert status == 0, stdout + stderr
        
        rx1 = []
        tx1 = []
        time1 = time()
                        
        for line in stdout.split("\n"):
            substrs = [x for x in line.split(" ") if x]
                            
            if "RX" in substrs and "bytes" in substrs:
                rx1.append(int(substrs[4]))
        
            if "TX" in substrs and "bytes" in substrs:
                tx1.append(int(substrs[4]))
        
        try:
            rx_sum = 0
            tx_sum = 0
            
            for i in range(len(rx0)):
                rx_sum = rx_sum + rx1[i] - rx0[i]
                tx_sum = tx_sum + tx1[i] - tx0[i]
            
            netstats = {
                "tx" : tx1,
                "rx" : rx1,
                "timestamp" : time1,
                "rx_rate" : rx_sum / (time1 - time0),
                "tx_rate" : tx_sum / (time1 - time0)
            }
            
            metric = Collection("metrics").get_object()
        
            metric.object["timestamp"] = time1
            metric.object["tx_rate"] = tx_sum / (time1 - time0)
            metric.object["rx_rate"] = rx_sum / (time1 - time0)
            metric.object["type"] = "localhost network throughput"
                
            metric.set()
        except Exception as e:
            netstats = {
                "tx" : tx1,
                "rx" : rx1,
                "timestamp" : time1,
                "error" : str(e)
            }
        
        set_kv("netstats", netstats)
        
        self.output.append(json.dumps(metric.object, indent = 4))
    
    def execute(self, cli):
        try:
            self.network(cli)
            self.status = STATUS_SUCCESS
        except:
            self.output.append(traceback.format_exc())
            self.status = STATUS_FAILURE

        return self.status