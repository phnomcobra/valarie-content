#!/usr/bin/python

from subprocess import Popen, PIPE

class Console:
    def __init__(self, **kargs):
        self.__buffer = 'Local Host Test Terminal: '
    
    def get_remote_host(self):
        return "127.0.0.1"
    
    def system(self, command, return_tuple = False, sudo_command = True):
        process = Popen(command, shell = True, stdout = PIPE, stderr = PIPE)
        output_buffer, stderr_buffer = process.communicate()
        status = process.returncode
        
        if return_tuple:
            return status, output_buffer, stderr_buffer
        elif 0 != int(status):
            return '{0}<font color="red"><br>{1}</font><br>'.format(output_buffer, stderr_buffer)
        else:
            return output_buffer
    
    def send(self, input_buffer):
        self.__buffer += input_buffer
        pass
    
    def recv(self):
        output_buffer = self.__buffer
        self.__buffer = ''
        return output_buffer
    
    def putf(self, file):
        self.send("filename: {0}\n".format(file.filename))
        self.send("{0}\n".format(file.file.read()))