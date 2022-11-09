import paramiko
import getpass
import socket
import datetime

timeout = 3
socket.setdefaulttimeout(timeout)

class maintenance:
    def __init__(self):
        self.port = 22
        self.time = datetime.datetime.now()
        self.strtime = self.time.strftime('%Y-%m-%d %H:%M:%S')
        print(self.strtime)
        self.gre_tunnel_checker()
        
    def gre_tunnel_checker(self):
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
            print('ssh connected\n')
            
            # ssh route directory/file list check
            stdin, stdout, stderr = ssh.exec_command('df -h')
            print(''.join(stdout.readlines()))
            
            ssh.close()
        except Exception as err:
            print(err)

def main():
    print("main")
    # info = []
    maintenance()

# main script run
if __name__ == "__main__":
    main()
