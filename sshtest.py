import paramiko
import getpass
import socket
import datetime
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

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
            self.system_check(ssh, server)
            ssh.close()
            print('\n> SSH disconnect complete <')
        except Exception as err:
            print('SSH connection Failed: ', err)
    
    def system_check(self, ssh, server):
        
        try:
            fail_result = ''
            main_result = ''
            
            print('=============== Ping Test ===============')
            for ser in self.ser:
                ser_name = ser[0]
                
                stdin, stdout, stderr = ssh.exec_command('echo this is paramiko')
                output = stdout.readlines()
                print('output is : ',''.join(output))
                
                main_result += ser_name
                
                for ip_num in range(1,3):
                    # -n: number of packet transmissions(1)
                    response = os.system("ping -n 1 " + ser[ip_num])
                    print(response)
                    if response == 0:
                        Netstatus = ' ' + ser[ip_num] + ": success"
                    else:
                        Netstatus = ' ' + ser[ip_num] + ": fail"
                        fail_result += ser_name + ' -' + Netstatus + '\r\n'
                    main_result += ' -' + Netstatus
                
                file_name = self.save_file(ser_name, main_result)
                print('file name is : ', file_name)
                main_result += '\n'
            
            self.send_mail(file_name, fail_result)
            
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
        return w_file_name
    
    def send_mail(self, file_name, fail_result):
        try:
            print("=============== Start Sending Mail ===============")
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            print(BASE_DIR)
            
            # session creation, smtp connection encapsulation - gmail port: 587
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.starttls()
            smtp.login('(outgoing_mail@gmail.com)', '(app_password)')

            msg = MIMEMultipart()
            msg['subject'] = '[공유] System Access Test'
            if fail_result == '':
                mail_content = '시스템 점검 결과입니다. \n\n통신 테스트(ping test) 결과 모든 시스템이 정상으로 확인되었습니다. \n\n감사합니다.\n'
            else:
                mail_content = '시스템 점검 결과입니다. \n\n통신 테스트(ping test) 결과 실패한 시스템 정보를 아래와 같이 공유드리오니 점검 요청 드립니다. \n\n' + fail_result + '\n\n감사합니다. \n'
            
            print(mail_content)
            msg.attach(MIMEText(mail_content, 'plain'))

            if os.path.isfile(BASE_DIR+'\\'+file_name):
                if os.path.getsize(BASE_DIR+'\\'+file_name) < 10000000:
                    try:
                        attachment = open(BASE_DIR+'\\'+file_name, 'rb')
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload((attachment).read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', "attachment; filename= "+file_name)
                        msg.attach(part)
                        
                    except Exception as err:
                        mail_content += '\n----------\n첨부 에러: 테스트 결과를 첨부할 수 없습니다.\n에러 메시지: ' + err + '\n'
                else:
                    mail_content += '\n----------\n테스트 결과 대용량 파일로 첨부할 수 없습니다.\n'

            smtp.sendmail("(outgoing_mail@gmail.com)", "(incoming_mail@example.com)", msg.as_string())
            print('> Successfully sent the mail <')
            smtp.quit()
            
        except Exception as err:
            print('Mail Transfer Failed: ', err)

def main():
    
    # system arguments value (default 1 - python3 sshtest.py)
    print(sys.argv, len(sys.argv))
    
    if len(sys.argv) == 2:
        ser_check_file = sys.argv[1]
        ser_info = []

        with open(ser_check_file, 'r') as file:
            lines = file.read().splitlines()
            for line in lines:
                line = line.split(",")
                ser_info.append(line)
            # maintenance(ser_info).ssh_connection()
            maintenance(ser_info)
    else:
        print('try python3 sshtest.py ser_info.log')

# main script run
if __name__ == "__main__":
    main()
