#!/usr/bin/python
################################################################################
# CREATE SERVER CERT
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
            status, stdout, stderr = cli.system('keytool -genkeypair -keyalg RSA -keysize 3072 -alias localhost -dname "CN=localhost,OU=Development,O=My Organization,C=DE" -ext BC:c=ca:false -ext EKU:c=serverAuth -ext "SAN:c=DNS:localhost,IP:127.0.0.1" -validity 3650 -keystore /tmp/server/server.jks -storepass secret -keypass secret', return_tuple = True)
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