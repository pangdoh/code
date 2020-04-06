import socket
import time

s = socket.socket()
s.connect(('127.0.0.1', 12345))
s.send(b'123asdasdaf')

time.sleep(5)
print('时间到了')
s.close()
