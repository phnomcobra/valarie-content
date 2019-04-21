#!/usr/bin/python

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            self.status = STATUS_INFORMATION
            
            num_cores = 0
            
            status, stdout, stderr = cli.system("cat /proc/cpuinfo", return_tuple = True)
            if status:
                self.output.append(stderr)
                self.status = STATUS_FAILURE
            else:
                for line in stdout.split("\n"):
                    substrs = [x for x in line.split(" ") if x]
                    if 'cpu' in substrs and \
                       'cores\t:' in substrs:
                        num_cores += int(substrs[2])
            
            mem = ''

            status, stdout, stderr = cli.system("cat /proc/meminfo", return_tuple = True)
            if status:
                self.output.append(stderr)
                self.status = STATUS_FAILURE
            else:
                for line in stdout.split("\n"):
                    substrs = [x for x in line.split(" ") if x]
                    if 'MemTotal:' in substrs:
                        mem = substrs[1] + ' ' + substrs[2]
            
            self.output.append("CPU Cores: {0}\tMemory: {1}".format(num_cores, mem))
            
            self.status = STATUS_INFORMATION
        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status