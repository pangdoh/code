'''爬虫简单模板。这里使用的是requests模块'''
import requests

res = requests.get("http://www.baidu.com/s?wd=杨幂") #一个get请求，如果用post就post('....')
status_code = res.status_code #返回状态码
print(status_code)
content = res.content #响应内容（字节流）
# print(content) #响应内容（字符串）
print('--------------------------------------------------------------------------------------------')
text = res.text
# print(text)
print('--------------------------------------------------------------------------------------------')
data = {
    "wd":"杨幂"
}
res = requests.get("http://www.baidu.com/s",params=data) #参数可以这样写
# print(res.text)

'''在python2中，有些站可能需要加verify=false跳过证书验证'''

# 禁止重定向跟随
res = requests.get(url, allow_redirects=False)

print('分割线#########################################################################################################')

# 请求头设置
#常见请求头
headers = {
"Host": "g.csdnimg.cn",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",
"Accept": "*/*",
"Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
"Accept-Encoding": "gzip, deflate, br",
"Referer": "https://www.baidu.com",
"Connection": "keep-alive"
}

#很多时候我们只用User-Agent即可
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36"
}

'''
常用的User-Agent

chrome
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36
ie
Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)
firefox
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0
opera
Opera/9.80 (X11; Linux x86_64; U; Ubuntu/10.10 (maverick); pl) Presto/2.7.62 Version/11.01
safari
Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; it-it) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27
'''

res = requests.get("http://www.baidu.com/s?wd=杨幂",headers=headers)
# print(res.text)

print('分割线#########################################################################################################')

'''状态码判断例子'''
res = requests.post("http://www.baidu.com/s",data=data,headers=headers)
print("status_code:%d" % res.status_code)
if res.status_code == 404:
    print("404 Not Found")
elif res.status_code == 200:
    print("Request Successfully")

print('分割线#########################################################################################################')

# form-data方式发送
payload = {
    "passwd": (None, "echo 123;"),
}
res = requests.post("http://127.0.0.1/1.php", files=payload, headers=headers)

'''关于cookie'''
cookies = res.cookies
print(cookies)
#遍历出来
for key,value in res.cookies.items():
    print("%s=%s" % (key,value))

print('分割线#########################################################################################################')

'''用同一个会话请求  *很关键'''
s = requests.Session()
res = s.post("http://www.baidu.com/s",data=data,headers=headers)
print("status_code:%d" % res.status_code)

print('分割线#########################################################################################################')

'''代理设置'''
proxy = '127.0.0.1:1080'
'''
#http代理
proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy,
}

#socks5代理
proxies = {
    'http':'socks5://' + proxy,
    'https':'socks5://' + proxy
}
res = requests.get("https://ipinfo.io",proxies=proxies)
print("status_code:%d" % res.status_code)
print(res.text)

#也可以随机选择一个代理
import random
proxy_list = [proxies]
proxy = random.choice(proxy_list)

print('分割线#########################################################################################################')
'''

# 方式二（配置整个会话，并设置密码）
session = requests.session()
session.proxies = {'http': 'socks5://192.168.3.58:9050',
                   'https': 'socks5://192.168.3.58:9050'}
resp = session.get('https://api.github.com', auth=('user', 'pass'))

#外还有一种设置方式，和 Urllib 中的方法相同，使用 socks 模块，也需要像上文一样安装该库，设置方法如下
# pip install PySocks
import requests
import socks
import socket

socks.set_default_proxy(socks.SOCKS5, '39.106.153.182', 1080)
socket.socket = socks.socksocket
try:
    res = requests.get("https://ipinfo.io")
    print(res.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)

print('分割线#########################################################################################################')

'''超时设置'''
from requests import ReadTimeout,ConnectionError,RequestException
try:
    res = requests.get("https://ipinfo.io",timeout=0.5)
    print("status_code:%d" % res.status_code)
except ReadTimeout:
    print("timeout")
except ConnectionError as e:
    print(ConnectionError)
    print(e)
except RequestException as e:
    print(RequestException)
    print(e)
