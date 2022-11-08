import paramiko
import getpass
import socket

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
