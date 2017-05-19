import paramiko, traceback

#paramiko.util.log_to_file('/tmp/paramiko.log')  #Debug


class sshSession:

    def __init__(self,hostip,hostuser,userkey,port):



        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.hostip = hostip
        self.hostuser = hostuser
        self.port = port
        self.userkey = userkey
        self.cmd = []



    def openSession(self):
        self.client.connect(self.hostip ,username = self.hostuser, key_filename = self.userkey, port =self.port)

    def closeSession(self):
        self.client.close()

    def addCommand(self,cmd):
        self.cmd.append(cmd)

    def showCommand(self):
        return self.cmd

    def execCMD(self):
        cmdlog = []

        for cmd in self.cmd:
            print(cmd)
            stdin, stdout, stderr = self.client.exec_command(cmd)
            cmdlog.append(stdout.readlines())
            cmdlog.append(stderr.readlines())

        self.cmd = []
        return cmdlog




def execCMD(vhost,cmd):

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=vhost.ipaddr,username = vhost.user, key_filename= vhost.sshkey,port=vhost.sshport)
        #ssh.connect(str(vhost.ipaddr),username = vhost.user, key_filename= vhost.sshkey)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        data = stdout.readlines()
        return data

    except paramiko.AuthenticationException:
        print ("We had an authentication exception!")
        shell = None

    except paramiko.ssh_exception.BadAuthenticationType:
        print ("Paramiko BadAuthenticationType")

    except paramiko.ssh_exception.NoValidConnectionsError:
        print ("Paramiko NoValidConnectionsError")

    except paramiko.ssh_exception.PartialAuthentication:
        print ("Paramiko PartialAuthentication")

    except paramiko.ssh_exception.PasswordRequiredException:
        print ("Paramiko PasswordRequiredException")

    except paramiko.ssh_exception.ProxyCommandFailure:
        print ("Paramiko ProxyCommandFailure")


    except Exception:
        traceback.print_exc()

def execSFTP(vhost,remote_path,local_path,method):


    try:

        #https://stackoverflow.com/questions/3635131/paramikos-sshclient-with-sftp
        #http://docs.paramiko.org/en/1.16/api/sftp.html
        #http://www.iodigitalsec.com/ssh-sftp-paramiko-python/

        #transport = paramiko.Transport((vhost.ipaddr, vhost.sshport))
        #transport.connect(username = vhost.user, pkey = vhost.sshkey )
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=vhost.ipaddr, username=vhost.user, key_filename=vhost.sshkey, port=vhost.sshport)
        #sftp = paramiko.SFTPClient.from_transport(transport)

        if method == "PUT":
            sftp = ssh.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            ssh.close()

        elif method == "GET":
            sftp = ssh.open_sftp()
            sftp.get(remote_path, local_path, callback=None)
            sftp.close()
            ssh.close()

        else:
            print ("ERROR NO METHOD")


    except paramiko.AuthenticationException:
        print ("We had an authentication exception!")
        shell = None

    except paramiko.ssh_exception.BadAuthenticationType:
        print ("Paramiko BadAuthenticationType")

    except paramiko.ssh_exception.NoValidConnectionsError:
        print ("Paramiko NoValidConnectionsError")

    except paramiko.ssh_exception.PartialAuthentication:
        print ("Paramiko PartialAuthentication")

    except paramiko.ssh_exception.PasswordRequiredException:
        print ("Paramiko PasswordRequiredException")

    except paramiko.ssh_exception.ProxyCommandFailure:
        print ("Paramiko ProxyCommandFailure")


    except Exception:
        traceback.print_exc()



