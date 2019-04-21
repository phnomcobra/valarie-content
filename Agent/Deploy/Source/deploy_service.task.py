#!/usr/bin/python

import traceback

TEMP_NAME = "/tmp/stembot.service"
FILE_NAME = "/etc/systemd/system/stembot.service"
FILE_BODY = """[Unit]
Description=STEMBot Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/stembot
ExecStart=/opt/stembot/server
Restart=on-abort

[Install]
WantedBy=multi-user.target"""

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            cli.writef(filename = TEMP_NAME, body = FILE_BODY)
            
            self.output.append(cli.system("mv -v {0} {1}".format(TEMP_NAME, FILE_NAME)))    
            self.output.append(cli.system("chmod -v 755 {0}".format(FILE_NAME)))
            self.output.append(cli.system("chown -v root:root {0}".format(FILE_NAME)))
            
            self.status = STATUS_INFORMATION
        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status