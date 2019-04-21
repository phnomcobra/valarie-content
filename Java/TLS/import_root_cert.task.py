#!/usr/bin/python
################################################################################
# IMPORT ROOT CERT
#
# Justin Dierking
# phnomcobra@gmail.com
# 937 371 6026
#
# 09/15/2018 Original Construction
################################################################################

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            status, stdout, stderr = cli.system("keytool -importcert -noprompt -keystore /tmp/server/server.jks -storepass secret -alias root-ca -keypass secret -file /tmp/root-ca/ca.pem", return_tuple = True)
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