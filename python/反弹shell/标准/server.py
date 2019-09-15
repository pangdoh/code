# -*- coding: utf-8 -*-
import socket
import argparse

def connection(s):
    print('Waiting for connection......')
    ss, addr = s.accept()
    print('client %s is connection!' % (addr[0]))
    print('print:\\!q for Disconnect')
    while True:
        cmd = input(str(addr[0]) + ':~#')
        if cmd == '\\!q':
            quitThread = True
            print('-- Disconnected --')
            exit(0)
        ss.send(cmd.encode())
        data = ss.recv(4096)
        print(data.decode())

if __name__ == '__main__':
    # 命令行参数解析对象
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', dest='hostName', default='0.0.0.0', help='Host Name(default=0.0.0.0)')
    parser.add_argument('-port', dest='conPort', default=1234,help='Host Port(default=1234)')
    # 解析命令行参数
    args = parser.parse_args()
    host = args.hostName
    port = args.conPort

    if host == None or port == None:
        print(parser.parse_args(['-h']))
        exit(0)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(512)
    connection(s)

