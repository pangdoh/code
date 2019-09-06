import socket
import sys
from urllib import parse

''' 根据域名获取IP地址 '''
def get_ip_list(domain):
    ip_list = []
    try:
        addrs = socket.getaddrinfo(domain, None)
        for item in addrs:
            if item[4][0] not in ip_list:
                ip_list.append(item[4][0])
    except Exception as e:
        print(e)
        sys.exit(0)
    return ip_list

''' url解析 '''
def url_parse(url):
    #初始化对象
    proto, host, port, path = None, None, None, None
    up = parse.urlparse(url)
    dest = up.netloc.split(":")
    host = dest[0]
    if (up.scheme != ""):
        proto = up.scheme
    else:
        if up.path.find('/') != -1:
            host = up.path[:up.path.find('/')]
        else:
            host = up.path

    if (len(dest) == 2):
        port = int(dest[1])
    else:
        if (proto == "http"):
            port = 80
        elif (proto == "https"):
            port = 443
    path = url[url.find(host) + len(host):]
    if path.find("/") == -1:
        path = "/"
    r = dict()
    r['proto'] = proto
    r['host'] = host
    r['port'] = port
    r['path'] = path
    print(r)
    return r

if __name__ == '__main__':
    help_ = 'example :\r\n$ sdomain www.google.com'
    domain = sys.argv[1]
    if domain == '-h' or domain == '-help':
        print(help_)
        sys.exit()

    domain = url_parse(domain)['host']
    result = get_ip_list(domain)
    print(result)