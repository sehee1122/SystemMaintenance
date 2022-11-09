import paramiko
import getpass
import socket
import datetime
import os

timeout = 3
socket.setdefaulttimeout(timeout)

class maintenance:
    def __init__(self):
        self.port = 22
        self.time = datetime.datetime.now()
        self.strtime = self.time.strftime('%Y-%m-%d %H:%M:%S')
        print(self.strtime)
        self.ssh_connection()
        
    def ssh_connection(self):
        try:
            # ssh server connected class - present pc: client
            ssh = paramiko.SSHClient()
            # ssh session key rule: paramiko.AutoAddPolicy()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            server = '192.168.5.132'
            user = input("Username: ")
            pwd = getpass.getpass("Password: ")
            
            # ssh server connect
            ssh.connect(server, port=22, username=user, password=pwd)
            print('--------------- SSH Connected ---------------\n')
            
            # ssh route directory/file list check
            stdin, stdout, stderr = ssh.exec_command('df -h')
            print(''.join(stdout.readlines()))
            
            self.system_check(server, user, pwd)
            
            ssh.close()
        except Exception as err:
            print(err)
    
    def system_check(self, server, user, pwd):
        try:
            print('--------------- ping test ---------------')
            # -n: number of packet transmissions(1)
            response = os.system("ping -n 1 " + server)
            if response == 0:
                Netstatus = "Network Active"
            else:
                Netstatus = "Network Error"
        except Exception as err:
            print(err)

def main():
    print("main")
    # info = []
    maintenance()

# main script run
if __name__ == "__main__":
    main()
