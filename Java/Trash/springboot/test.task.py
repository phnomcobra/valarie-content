#!/usr/bin/python
################################################################################
# NEW TASK
#
# Justin Dierking
# phnomcobra@gmail.com
# 937 371 6026
#
# 07/31/2018 Original Construction
################################################################################

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            status, stdout, stderr = cli.system("timeout --preserve-status 30 java -jar /tmp/springboot/target/gs-spring-boot-0.1.0.jar", return_tuple = True)
            #status, stdout, stderr = cli.system("timeout --preserve-status 5 java -cp /tmp/springboot/target/dev6-application-0.1.jar dev6.Application", return_tuple = True)
            if status:
                self.output.append(str(stdout) + str(stderr))
                self.status = STATUS_FAILURE
            else:
                self.output.append(str(stdout) + str(stderr))
                self.status = STATUS_SUCCESS
        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status