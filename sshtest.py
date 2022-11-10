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
            print('=============== SSH Connected ===============\n')
            
            # ssh route directory/file list check
            stdin, stdout, stderr = ssh.exec_command('df -h')
            print(''.join(stdout.readlines()))
            self.system_check(ssh, server, user, pwd)
            ssh.close()
        except Exception as err:
            print('SSH connection Failed: ', err)
    
    def system_check(self, ssh, server, user, pwd):
        
        try:
            ser_result_success = {}
            ser_result_fail = {}
            main_result = ''
            
            print('=============== Ping Test ===============')
            for ser in self.ser:
                
                ser_name = ser[0]
                ser_ip_1 = ser[1]
                ser_ip_2 = ser[2]
                
                stdin, stdout, stderr = ssh.exec_command('echo this is paramiko')
                output = stdout.readlines()
                print('output is : ',''.join(output))
                
                main_result += ser_name
                
                for ip_num in range(1,3):
                    # -n: number of packet transmissions(1)
                    response = os.system("ping -n 1 " + ser[ip_num])
                    print(response)
                    if response == 0:
                        Netstatus = ' ' + ser[ip_num] + ": Active"
                    else:
                        Netstatus = ' ' + ser[ip_num] + ": Error"
                    main_result += ' /' + Netstatus
                
                file_name = self.save_file(ser_name, main_result)
                main_result += '\n'
            
            self.send_mail(file_name, main_result)
            
        except Exception as err:
            print('Ping Test Failed: ', err)

    def save_file(self, server, ping_result):
        try:
            # realpath, abspath
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            w_file_name = self.systime + "_system-active-test_result.log"
            
            with open(os.path.join(BASE_DIR, w_file_name), 'w') as f:
                # for k, v in ping_result.items():
                doc = f"{ping_result}"
                f.write(doc)
                
        except Exception as err:
            print('Fail to save log to file: ', err)
            
    def send_mail(self, file_name, ping_result):
        try:
            print("=============== Start Sending Mail ===============")
            # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            # print(BASE_DIR)
            
        except Exception as err:
            print('Mail Transfer Failed: ', err)

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
