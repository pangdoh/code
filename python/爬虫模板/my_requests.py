import ssl
from urllib import parse
from bs4 import BeautifulSoup
import socks
import socket
import gzip
import io


def parse_urls(url):
    """
    解析url
    :param url:
    :return: 1.协议，2.域名，3.端口，4.路径，5.参数
    """
    proto = 'http'
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
        else:
            assert False, 'Protocol not supported'

    host = dst[0]
    path = up.path
    query = up.query
    if path is None or path == '':
        path = '/'
    return proto, host, port, path, query


def send(url, data=None, method='GET', allow_redirects=True, headers=None, timeout=None, proxies=None, encode='utf-8',
         auto_encode=True):
    """
    核心方法，用来发送网络请求，处理封装相关数据
    :param url: 请求的url
    :param data: 请求参数
    :param method: 请求方式（GET,POST）
    :param allow_redirects: 重定向自动跟随，默认True
    :param headers: 请求头，字典类型
    :param timeout: 超时时间，秒
    :param proxies: 代理
    :param encode: 解码方式
    :param auto_encode: 是否自动识别页面解码方式，默认True
    :return: Response
    """
    # 解析url
    proto, host, port, path, query = parse_urls(url)

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
    else:
        assert False, 'Protocol not supported'

    if timeout:
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/114.86 (KHTML, like Gecko) \
            Chrome/63.0.4341.21 Safari/352.10',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
        }

    # 构造http请求
    post_data = ""
    if method.upper() == 'POST':
        for key, value in data.items():
            post_data += "%s=%s&" % (key, value)
        if post_data.endswith('&'):
            post_data = post_data[:len(post_data) - 1]

        send_data = "POST %s" % path

        if not headers.get('Content-Type'):
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        if not headers.get('Content-Length'):
            if len(data) > 0:
                data_length = len(post_data)
            else:
                data_length = 0
            headers['Content-Length'] = str(data_length)
    elif method.upper() == 'GET':
        send_data = "GET %s" % path
    else:
        raise ValueError('暂不支持该请求方式:', method)

    send_data += " HTTP/1.1"
    send_data += "\r\n"
    for key, value in headers.items():
        send_data += "%s: %s" % (key, value)
        send_data += "\r\n"
    send_data += "\r\n"
    if method.upper() == 'POST':
        send_data += post_data

    s.send(send_data.encode(encode))
    read_bytes = bytes()

    # 定义响应信息容器
    response = Response()

    # 开始接收响应数据
    while True:
        receive_data = s.recv(4096)
        if not receive_data:
            break
        else:
            read_bytes += receive_data
            # 封装响应头
            if not response.headers:
                if read_bytes.find(b'\r\n\r\n') != -1:
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
            # 接收到尾端跳出
            if response.headers and response.headers.get('Content-Length'):
                content_length = int(response.headers.get('Content-Length'))
                if len(read_bytes[read_bytes.find(b'\r\n\r\n')+4:]) >= content_length:
                    # 封装响应体
                    response.content = read_bytes[read_bytes.find(b'\r\n\r\n') + 4:]
                    break
            elif len(receive_data) == 0:
                break
            else:
                # 处理分块传输方式
                over_flag = False
                if read_bytes.find(b'\r\n\r\n') != -1:
                    res_body = read_bytes[read_bytes.find(b'\r\n\r\n')+4:]
                    block_n = 0
                    prior_end_index = -2
                    temp_res_body = b''
                    while True:
                        block_n += 1
                        if prior_end_index + 2 >= len(res_body):
                            # 当前块还未接收完全
                            break
                        temp_content = res_body[prior_end_index+2:]
                        temp_start_index = temp_content.find(b'\r\n') + 2  # 临时开头索引
                        block_n_start_index = temp_start_index + prior_end_index + 2  # 当前块数据开头索引（包含）
                        block_n_length_hex = temp_content[:temp_start_index - 2]  # 当前块数据长度(十六进制)
                        block_n_length = int(block_n_length_hex, 16)  # 当前块数据长度(十进制)
                        # print("第" + str(block_n) + "块长度：", block_n_length)
                        if block_n_length > 0:
                            block_n_end_index = block_n_start_index + block_n_length  # 当前块数据结束索引（不包含）
                            if len(res_body) < block_n_end_index:
                                # 当前块还未接收完全
                                break
                            block_n_content = res_body[block_n_start_index:block_n_end_index]
                            # print("第" + str(block_n) + "块内容：", block_n_content)
                            prior_end_index = block_n_end_index
                            temp_res_body += block_n_content
                        else:
                            # 封装响应体
                            response.content = temp_res_body
                            over_flag = True
                            break
                if over_flag:
                    break
    try:
        # 状态码
        response.status_code = read_bytes[:read_bytes.find(b'\r\n\r\n')].decode(encode)
        response.status_code = response.status_code[response.status_code.find(' ')+1:response.status_code.find(' ')+4]

        # 是否需要解压缩
        if response.headers.get('Content-Encoding') and response.headers.get('Content-Encoding').find('gzip') != -1:
            # print('接收：', response.content)
            if response.content.startswith(b'\x1f'):
                pass
            else:
                raise ValueError('响应内容格式错误，无法识别的压缩类型')

            buf = io.BytesIO(response.content)
            gf = gzip.GzipFile(fileobj=buf)
            response.content = gf.read()
            # print("解压缩后：", response.content)

        # 响应set-cookie
        response.cookies = response.headers.get('Set-Cookie')

        # 响应内容编码后
        if response.headers.get('Content-Type') and response.headers.get('Content-Type').find('html') != -1:
            if auto_encode:
                encode = get_meta_charset(response.content)
                # print('自动识别编码：' + encode)
            response.text = response.content.decode(encode)

        # 设置重定向自动跟随
        if allow_redirects:
            count_n = 0

            while response.status_code == '302' and response.headers.get('location'):
                count_n += 1
                if count_n > 5:
                    print('重定向循环超过5次！已退出')
                    break
                location = response.headers.get('location')

                if location.startswith('http'):
                    http_url = location
                else:
                    proto, host, port, path, query = parse_urls(url)
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
                proto, host, port, path, query = parse_urls(http_url)
                if headers:
                    headers['Host'] = host
                response = send(http_url, data=data, method=method, allow_redirects=allow_redirects, headers=headers, timeout=timeout, proxies=proxies, encode=encode)
    except Exception as e:
        raise RuntimeError(e)
    return response


def get_meta_charset(res_data):
    """
    自动识别HTML的解码方式
    :param res_data: HTML页面内容
    :return: 编码方式（如：‘utf-8’）
    """
    soup = BeautifulSoup(res_data, 'html.parser')
    meta_lst = soup.head.find_all("meta")
    for meta in meta_lst:
        content = meta.get('content')
        if content:
            content = content.lower()
            if 'charset=' in content:
                return content[content.rindex('charset=') + 8:]


def get(url, headers=None, allow_redirects=True, timeout=None, proxies=None, encode='utf-8'):
    return send(url, headers=headers, method='GET', allow_redirects=allow_redirects, timeout=timeout, encode=encode,
                proxies=proxies)


# POST请求
def post(url, data=None, headers=None, allow_redirects=True, timeout=None, proxies=None, encode='utf-8'):
    return send(url, data=data, headers=headers, method='POST', allow_redirects=allow_redirects, timeout=timeout,
                encode=encode, proxies=proxies)


class Response:
    """
    响应实体，被用来封装响应信息
    """
    headers = None
    status_code = None
    content = None
    text = None
    cookies = None


if __name__ == '__main__':
    # url = 'http://msydqstlz2kzerdg.onion/search/'

    proxies = 'xx.xx.xx.xx:9050'
    # proxies = '192.168.1.131:1080'
    # proxies = None

    data = {
        'p1': 'abc',
        'p2': '123',
    }

    url = 'http://5u56fjmxu63xcmbk.onion/'
    # url = 'https://www.baidu.com/'
    # url = 'https://abc.de/'
    res = get(url, timeout=60, proxies=proxies)
    # res = post(url, data=data, timeout=10, proxies=proxies)
    print("打印响应头：\r\n", res.headers)
    print("打印状态码：", res.status_code)
    print("打印内容：\r\n", res.content)
    print("打印字符串内容：\r\n", res.text)
    print("打印cookies：", res.cookies)
