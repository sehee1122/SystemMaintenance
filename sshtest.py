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
        self.systime = self.time.strftime('%y%m%d-%H%M%S')
        print(self.systime)
        self.ssh_connection()
        
    def ssh_connection(self):
        try:
            # ssh server connected class - present pc: client
            ssh = paramiko.SSHClient()
            # ssh session key rule: paramiko.AutoAddPolicy()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            server = '192.168.5.132'
            # server2 = '192.168.5.130'
            user = input("Username: ")
            pwd = getpass.getpass("Password: ")
            
            # ssh server connect
            ssh.connect(server, port=22, username=user, password=pwd)
            print('--------------- SSH Connected ---------------\n')
            
            # ssh route directory/file list check
            stdin, stdout, stderr = ssh.exec_command('df -h')
            print(''.join(stdout.readlines()))
            self.system_check(ssh, server, user, pwd)
            ssh.close()
        except Exception as err:
            print('SSH connection Failed: ', err)
    
    def system_check(self, ssh, server, user, pwd):
        
        # if server == '192.168.5.132':
        #     file_name = 'server_#1'
        try:
            ser_result_success = {}
            ser_result_fail = {}
            msg_text = ''
            
            for ser in self.ser:
                ser_name = ser[0]
                ser_ip_1 = ser[1]
                ser_ip_2 = ser[2]
                
                stdin, stdout, stderr = ssh.exec_command('echo this is paramiko')
                output = stdout.readlines()
                print('output is : ',''.join(output))
                
                print('--------------- ping test ---------------')
                # -n: number of packet transmissions(1)
                response = os.system("ping -n 1 " + ser[1])
                print(response)
                if response == 0:
                    Netstatus = ser[1] + ": Active"
                else:
                    Netstatus = ser[1] + ": Error"
                file_name = self.save_file(ser[1], Netstatus)
            
        except Exception as err:
            print('Ping Test Failed: ', err)

    def save_file(self, server, ping_result):
        try:
            # realpath, abspath
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            w_file_name = f'{self.systime}_{server}_result.log'
            # w_file_name = self.systime + "_" + server + "_result.log"
            
            with open(os.path.join(BASE_DIR, w_file_name), 'w') as f:
                # for k, v in ping_result.items():
                doc = f"{ping_result}"
                f.write(doc)
                
        except Exception as err:
            print('Fail to save log to file: ', err)
            
    # def send_mail(self, server, ):
    #     return 0
def main():
    
    # system arguments value (default 1 - python3 sshtest.py)
    print(sys.argv, len(sys.argv))
    
    if len(sys.argv) == 2:
        # c:/Users/user/Desktop/sehee/system/git/sshtest.py
        ser_check_file = sys.argv[1]
        # []: Array / {}: Dictionary / (): Tuple    
        ser_info = []

        with open(ser_check_file, 'r') as file:
            lines = file.read().splitlines()
            for line in lines:
                line = line.split(",")
                ser_info.append(line)
            # maintenance(ser_info).ssh_connection()
            maintenance(ser_info)
    else:
        print('aa')

# main script run
if __name__ == "__main__":
    main()
