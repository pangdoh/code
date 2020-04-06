import socket
import time

s = socket.socket()
s.bind(('127.0.0.1', 12345))
s.listen(3)
conn, address = s.accept()
data = conn.recv(1024)
print(data)

time.sleep(10000)
print('时间到了')
