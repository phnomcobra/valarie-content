#!/usr/bin/python
################################################################################
# PIP INSTALL CHERRYPY
#
# Justin L. Dierking
# justin.l.dierking.civ@mail.mil
# 614 692 2050
#
# 09/07/2017 Original Construction
################################################################################

import traceback

class Task:
    def __init__(self):
        self.output = []
        self.status = STATUS_NOT_EXECUTED

    def execute(self, cli):
        try:
            status, stdout, stderr = cli.system("pip install cherrypy==17.4.0", return_tuple = True)
            if status:
                self.output.append(str(stderr))
                self.status = STATUS_FAILURE
            else:
                self.output.append(str(stdout))
                self.status = STATUS_SUCCESS
        except Exception:
            self.output.append(traceback.format_exc())
            self.status = STATUS_EXCEPTION

        return self.status