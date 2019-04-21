#!/usr/bin/python

import paramiko
import select
import socket
import SocketServer
import traceback
import string
import base64
import pickle
import os

from subprocess import Popen, PIPE
from time import time, sleep
from threading import Thread
from random import randrange

from valarie.controller.messaging import add_message
from valarie.dao.document import Collection
from valarie.dao.utils import sucky_uuid

class ForwardServer (SocketServer.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True

def verbose(data):
    output_buffer = ""
    for c in data:
        if str(c).isalpha() or \
           str(c).isdigit() or \
           str(c) in """`~!@#$%^&*()_+-=\][|}{';":/.,?>< """:
            output_buffer += c
        else:
            output_buffer += '.'
    #add_message(output_buffer)

class Handler (SocketServer.BaseRequestHandler):
    def handle(self):
        verbose('Connecting SSH Tunnel...')
        
        try:
            chan = self.ssh_transport.open_channel('direct-tcpip',
                                                   (self.chain_host, self.chain_port),
                                                   self.request.getpeername())
        except Exception as e:
            verbose('Incoming request to %s:%d failed: %s' % (self.chain_host,
                                                              self.chain_port,
                                                              repr(e)))
            return
        if chan is None:
            verbose('Incoming request to %s:%d was rejected by the SSH server.' %
                    (self.chain_host, self.chain_port))
            return

        verbose('Connected!  Tunnel open %r -> %r -> %r' % (self.request.getpeername(),
                                                            chan.getpeername(), (self.chain_host, self.chain_port)))
        
        while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(48)
                if len(data) > 0:
                    verbose("Tunnel: SEND {1} bytes : [{0}]".format(data, len(data)))
                    chan.send(data)
                else:
                    sleep(1)

            if chan in r:
                data = chan.recv(48)
                if len(data) > 0:
                    verbose("Tunnel: RECV {1} bytes : [{0}]".format(data, len(data)))    
                    self.request.send(data)
                else:
                    sleep(1)
                
        peername = self.request.getpeername()
        chan.close()
        self.request.close()
        verbose('Tunnel closed from %r' % (peername,))

class Console:
    def __init__(self, **kargs):
        # Private Members
        self.__ssh = paramiko.SSHClient()
        self.__username = "username"
        self.__password = "password"
        self.__private_key = None
        self.__remote = kargs["host"]["host"]
        self.__session_var = {}
        self.__tunnel = {}
        
        # Public Members
        self.sftp = None
        
        self.connect()
        
        self.__chan = self.__ssh.invoke_shell()

    #### Mutation Methods ########################
    def set_username(self, username):
        self.__username = username
        
    def set_password(self, password):
        self.__password = password
    
    def set_private_key(self, key_filename, password = None):
        self.__private_key = paramiko.RSAKey.from_private_key_file(key_filename, password = password)

    def set_remote_host(self, remote):
        self.__remote = remote
    
    #### Set Key Value ###########################
    def set(self, key, value):
        try:
            self.__session_var[key] = value
        except Exception:
            self.__session_var = {}
            self.__session_var[key] = value
    
    #### Inspection Methods ######################
    def get_username(self):
        return self.__username
    
    def get_password(self):
        return self.__password
    
    def get_remote_host(self):
        return self.__remote
    
    #### Get Key Value ###########################
    # Return key value. If a key error exception is thrown, return none.
    def get(self, key):
        try:
            value = self.__session_var[key]
            return value
        except Exception as e:
            return None
    
    #### Test sudo ###############################
    # Test sudo by sudoing whoami. Credentials are fed into standard input and
    # flushed after executing sudo. If a non-zero return code is recieved a
    # custom exception is raised.
    def __test_sudo(self):
        if not self.__username == "root":
            stdin, stdout, stderr = self.__ssh.exec_command('sudo -S whoami')
            stdin.write(self.__password + '\n')
            stdin.flush()
            if 0 != int(stdout.channel.recv_exit_status()):
                raise NameError('Sudo test failed with {0}@{1}'.format(self.__username, self.__remote))
    
    #### Connect to SSH Server ###################
    # Set host key policy to AutoAddPolicy() and connect to host using credentials
    # from private members. Finally test sudo.
    def connect(self):
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.__private_key:        
            self.__ssh.connect(self.__remote, username = self.__username, pkey = self.__private_key)
        else:
            self.__ssh.connect(self.__remote, username = self.__username, password = self.__password)
        self.__ssh.get_transport().set_keepalive(30)
        self.sftp = self.__ssh.open_sftp()
    
    #### Close Connection ########################
    # Close SFTP and SSH connections
    def close(self):
        self.sftp.close()
        self.__ssh.close()
    
    #### Get Shell ###############################
    # Return channel object for an interactive shell
    def get_shell(self):
        return self.__ssh.invoke_shell()
    
    #### Run Script ##############################
    # Run script. The header remarks of the file
    # is used to determine what interpreter or 
    # program should be used. The script is 
    # selected with its inventory object UUID.
    # The start directory, user to run as, and
    # return format are optional parameters.
    def script(self, \
               objuuid = None, \
               body = None, \
               start_directory = None, \
               run_as = None, \
               return_tuple = False):
        if objuuid != None:
            script = Collection("inventory").get_object(objuuid)
            script_name = script.object["name"]
            script_body = script.object["body"]
        elif body != None:
            script_name = "valarie-" + sucky_uuid()
            script_body = body
        else:
            raise Exception("No objuuid or script body specified!")

        file = self.sftp.open(script_name, "w") 
        file.write(script_body)
        file.close()
        
        self.system("chmod 755 {0}".format(script_name))
        
        if start_directory == None:
            if run_as == None:
                status, stdout, stderr = self.system("./{0}".format(script_name), \
                                                     return_tuple = True)
            else:
                status, stdout, stderr = self.system("sudo -u {1} ./{0}". \
                                                     format(script_name, \
                                                            run_as), \
                                                     return_tuple = True)
            
            self.system("rm -f {0}".format(script_name))
        else:
            self.system("mv -f {0} /{1}/{2}".format(script_name, \
                                                    start_directory, \
                                                    script_name))
            if run_as == None:
                status, stdout, stderr = self.system("bash -c 'cd {0}; ./{1}'". \
                                                     format(start_directory, \
                                                            script_name), \
                                                     return_tuple = True)
            else:
                status, stdout, stderr = self.system("sudo -u {2} bash -c 'cd {0}; ./{1}'". \
                                                     format(start_directory, \
                                                            script_name, \
                                                            run_as), \
                                                     return_tuple = True)
            
            self.system("rm -f /{0}/{1}".format(start_directory, script_name))
        
        if return_tuple == True:
            return status, stdout, stderr
        else:
            return stdout + stderr

    #### System Command ##########################
    # Execute command on SSHClient. If the credentials has a user other than root
    # append the command into a sudo command. If redirection is used with sudo,
    # run the command in its own bash shell to preserve privileges while
    # redirecting to a file. If __debug is set to true, print all three I/O
    # streams during execution. If a non-zero exit code is returned, tag the
    # standard error buffer as red font and add it to the output buffer. If the
    # return tuple parameter is set to true, a tuple of the exit status, standard
    # output buffer, and standard error buffer is returned.
    def system(self, command, return_tuple = False, sudo_command = True):
        if self.__username == "root" or not sudo_command:
            stdin, stdout, stderr = self.__ssh.exec_command(command)
        else:
            if " > " in command or " >> " in command:
                stdin, stdout, stderr = self.__ssh.exec_command("sudo -S bash -c '{0}'".format(command))
            else:
                stdin, stdout, stderr = self.__ssh.exec_command('sudo -S ' + command)
            stdin.write(self.__password + '\n')
            stdin.flush()

        # Lossy ascii character set conversion
        output_buffer = ""
        for c in stdout.read().replace("[sudo] password for {0}:".format(self.__username), ""):
            try:
                output_buffer += c.encode("ascii", "ignore")
            except Exception:
                pass

        # Lossy ascii character set conversion
        stderr_buffer = ""
        for c in stderr.read().replace("[sudo] password for {0}:".format(self.__username), ""):
            try:
                stderr_buffer += c.encode("ascii", "ignore")
            except Exception:
                pass
        
        status = stdout.channel.recv_exit_status()
        
        if return_tuple:
            return status, output_buffer, stderr_buffer
        elif 0 != int(status):
            return '{0}<font color="red"><br>{1}</font><br>'.format(output_buffer, stderr_buffer)
        else:
            return output_buffer
    
    #### SSH Tunnel ##############################
    # Methods for starting and stopping SSH tunnels. 
    def __start_tunnel(self, local_port, remote_host, remote_port):
        transport = self.__ssh.get_transport()
        class SubHandler (Handler):
            chain_host = remote_host
            chain_port = remote_port
            ssh_transport = transport
        self.__tunnel[local_port] = ForwardServer(('', local_port), SubHandler)
        self.__tunnel[local_port].serve_forever()
    
    def start_tunnel(self, local_port, remote_host, remote_port):    
        Thread(target = self.__start_tunnel, args = (local_port, remote_host, remote_port)).start()
        sleep(5)
    
    def stop_tunnel(self, local_port):
        if local_port in self.__tunnel:
            self.__tunnel[local_port].shutdown()
            del self.__tunnel[local_port]
    
    def send(self, input_buffer):
        for c in input_buffer:
            self.__chan.send(c)
    
    def recv(self):
        if self.__chan.recv_ready():
            return self.__chan.recv(9999)
        elif self.__chan.recv_stderr_ready():
            return self.__chan.recv_stderr(9999)
        else:
            return ''
    
    def writef(self, filename, body):
        f = self.sftp.file(filename, mode = "w")
        f.write(body)
        f.close()
    
    def writebf(self, filename, body):
        f = self.sftp.file(filename, mode = "wb")
        f.write(body)
        f.close()
    
    def readf(self, filename):
        f = self.sftp.file(filename, mode = "r")
        body = str(f.read())
        f.close()
        return body
    
    def readbf(self, filename):
        f = self.sftp.file(filename, mode = "rb")
        body = f.read()
        f.close()
        return body

    def putf(self, file):
        self.send("echo Uploading {0}...\n".format(file.filename))
        self.sftp.putfo(file.file, file.filename)
