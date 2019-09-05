import logging
import sys
from paramiko import AuthenticationException
from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import NoValidConnectionsError


class MySshClient():
    def __init__(self):
        self.ssh_client = SSHClient()

    # 此函数用于输入用户名密码登录主机
    def ssh_login(self,host_ip,username,password):
        try:
            # 设置允许连接known_hosts文件中的主机（默认连接不在known_hosts文件中的主机会拒绝连接抛出SSHException）
            self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            self.ssh_client.connect(host_ip,port=22,username=username,password=password)
        except AuthenticationException:
            logging.warning('username or password error')
            return 1001
        except NoValidConnectionsError:
            logging.warning('connect time out')
            return 1002
        except:
            logging.warning('unknow error')
            print("Unexpected error:", sys.exc_info()[0])
            return 1003
        return 1000

    # 此函数用于执行command参数中的命令并打印命令执行结果
    def execute_some_command(self,command):
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        print(stdout.read().decode())

    # 此函数用于退出登录
    def ssh_logout(self):
        logging.warning('will exit host')
        self.ssh_client.close()

if __name__ == '__main__':
    # 远程主机IP
    host_ip = 'xx.xxx.xx.xx'
    # 远程主机用户名
    username = 'root'
    # 远程主机密码
    password = 'xxxxxxxxx'

    # 实例化
    my_ssh_client = MySshClient()
    # 登录，如果返回结果为1000，那么执行命令，然后退出
    if my_ssh_client.ssh_login(host_ip,username,password) == 1000:
        # logging.warning(f"{host_ip}-login success, will execute command：{command}")
        print("-----已连接-----")
        print("执行:logout命令以退出登录")
        while True:
            command = input('>')
            if command == 'logout':
                break
            my_ssh_client.execute_some_command(command)

        my_ssh_client.ssh_logout()