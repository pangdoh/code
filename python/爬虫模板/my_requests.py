import ssl
from urllib import parse
import socks
import socket


# 解析url
def parse_urls(url):
    proto = 80
    up = parse.urlparse(url)
    if up.scheme != "":
        proto = up.scheme
    dst = up.netloc.split(":")
    if len(dst) == 2:
        port = int(dst[1])
    else:
        if proto == "http":
            port = 80
        elif proto == "https":
            port = 443
    host = dst[0]
    path = up.path
    if path is None or path == '':
        path = '/'
    return proto, host, port, path


# 发送接收
def send(url, data=None, method='GET', allow_redirects=True, headers=None, timeout=10, proxies=None, encode='utf-8'):
    # 解析url
    proto, host, port, path = parse_urls(url)

    # 设置代理
    if proxies:
        proxy_address = proxies.split(':')[0]
        proxy_port = proxies.split(':')[1]
        socks.set_default_proxy(socks.SOCKS5, proxy_address, int(proxy_port))
        socket.socket = socks.socksocket

    # 创建套接字
    if proto == "http":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif proto == "https":
        s = ssl.wrap_socket(socket.socket())
    s.settimeout(timeout)
    try:
        s.connect((host, port))
    except Exception as e:
        print("error %s" % e)

    # 设置默认请求头
    if not headers:
        headers = {
            'Host': host,
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/232.36 (KHTML, like Gecko) Chrome/60.0.3412.39 Safari/312.30',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

    # 构造http请求
    if method.upper() == 'POST':
        send_data = "POST %s" % path
    else:
        send_data = "GET %s" % path
    send_data += " HTTP/1.1"
    send_data += "\r\n"
    for key, value in headers.items():
        send_data += "%s: %s" % (key, value)
        send_data += "\r\n"
    send_data += "\r\n"
    if method.upper() == 'POST' and data:
        send_data += data
        send_data += "\r\n"
        send_data += "\r\n"

    # print("发送请求：\r\n%s" % send_data)
    # print('------------------------------------------------------------')
    s.send(send_data.encode(encode))
    read_bytes = bytes()
    while True:
        receive_data = s.recv(512)
        if not receive_data:
            break
        else:
            read_bytes += receive_data
            if receive_data.endswith(b"0\r\n\r\n"):
                break

    # 封装响应信息
    response = Response()
    try:
        # 响应头
        response.headers = read_bytes[:read_bytes.find(b'\r\n\r\n')].decode(encode)
        attr_lines = response.headers.split("\r\n")
        response.headers = {}
        for attr_lien in attr_lines:
            attrs = attr_lien.split(":")
            if len(attrs) == 2:
                key = attrs[0]
                val = attrs[1]
                if val.startswith(" "):
                    val = val[1:]
                response.headers[key] = val

        # 状态码
        response.status_code = read_bytes[:read_bytes.find(b'\r\n\r\n')].decode(encode)
        response.status_code = response.status_code[response.status_code.find(' ') + 1:response.status_code.find(' ') + 4]

        # 响应内容
        response.content = read_bytes[read_bytes.find(b'\r\n\r\n') + 4:]
        response.content = response.content[response.content.find(b'\r\n') + 2:response.content.find(b'\r\n\r\n0')]

        # 响应内容编码后
        response.text = response.content.decode(encode)

        # 响应set-cookie
        response.cookies = response.headers.get('Set-Cookie')

        # 设置重定向自动跟随
        if allow_redirects:
            if response.status_code == '302':
                location = response.headers.get('location')
                print("302, location:", location)
                count_n = 0
                while location:
                    count_n += 1
                    if count_n > 5:
                        print('重定向循环超过5次！已退出')
                        break
                    if location.startswith('http'):
                        http_url = location
                    else:
                        proto, host, port, path = parse_urls(url)
                        while True:
                            if location.startswith("../"):
                                if path.endswith("/"):
                                    path = path[:len(path) - 1]
                                path = path[:path.rfind("/")]
                                location = location[3:]
                            else:
                                break
                        if location.startswith("/"):
                            path = "/"
                        if not path.startswith("/"):
                            path = "/%s" % path
                        if not location.startswith("/"):
                            location = "/%s" % location
                        if location.startswith("/") and path.endswith("/"):
                            location = location[1:]

                        http_url = "%s://%s:%s%s%s" % (proto, host, port, path, location)
                    proto, host, port, path = parse_urls(http_url)
                    if headers:
                        headers['Host'] = host
                    response = send(http_url, data=data, method=method, allow_redirects=allow_redirects, headers=headers, timeout=timeout, proxies=proxies, encode=encode)
                    location = response.headers.get('location')

    except Exception as e:
        print(e)

    return response


# GET请求
def get(url, headers=None, allow_redirects=True, timeout=None, proxies=None, encode='utf-8'):
    return send(url, headers=headers, method='GET', allow_redirects=allow_redirects, timeout=timeout, encode=encode, proxies=proxies)


# POST请求
def post(url, data=None, headers=None, allow_redirects=True, timeout=None, proxies=None, encode='utf-8'):
    return send(url, data=data, headers=headers, method='POST', allow_redirects=allow_redirects, timeout=timeout, encode=encode, proxies=proxies)


class Response:
    headers = None
    status_code = None
    content = None
    text = None
    cookies = None

if __name__ == '__main__':
    url = "https://www.baidu.com"
    # url = 'http://hhtqp7dzcon3ibrt4tonh6mpc3ftve5dwmideorzkyutzxbx6fcgdeid.onion/'
    # url = 'http://msydqstlz2kzerdg.onion/search/'
    # proxies = '192.168.3.69:9011'
    # proxies = '192.168.0.104:1080'
    proxies = None
    res = get(url, allow_redirects=True, proxies=proxies)
    print(res.headers)
    print(res.status_code)
    print(res.content)
    print(res.cookies)
