import paramiko
import getpass
import socket
import datetime
import os
import sys

timeout = 3
socket.setdefaulttimeout(timeout)

class maintenance:
    def __init__(self, ser_info):
        self.port = 22
        self.ser = ser_info
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
        
        # if server == '192.168.5.132':
        #     file_name = 'server_#1'
        try:
            ser_result_success = {}
            ser_result_fail = {}
            msg_text = ''
            
            print('--------------- ping test ---------------')
            # -n: number of packet transmissions(1)
            response = os.system("ping -n 1 " + server)
            if response == 0:
                Netstatus = "Network Active"
            else:
                Netstatus = "Network Error"
            file_name = self.save_results(server, Netstatus)
            
            
            
        except Exception as err:
            print(err)

    def save_results(self, server, ping_result):
        return 0
    # def send_mail(self, server, ):
    #     return 0
def main():
    
    # system arguments value (default 1)
    print(sys.argv, len(sys.argv))
    
    # c:/Users/user/Desktop/sehee/system/git/sshtest.py
    ser_check_file = sys.argv[0]
    # []: Array / {}: Dictionary / (): Tuple    
    ser_info = []

    with open(ser_check_file, 'r') as file:
        lines = file.read().splitlines()
        for line in lines:
            line = line.split(",")
            ser_info.append(line)
    
    # maintenance(ser_info).ssh_connection()
    maintenance(ser_info)

# main script run
if __name__ == "__main__":
    main()
