# 协程 pip3 install gevent
import gevent


# def eat(name):
#     global a
#     a = 123
#     print('%s eat 1' % name)
#     gevent.sleep(2)
#     print('%s eat 2' % name)
#
#
# def play(name):
#     global a
#     print(a)
#     print('%s play 1' % name)
#     gevent.sleep(1)
#     print('%s play 2' % name)
#
#
# if __name__ == '__main__':
#     g1 = gevent.spawn(eat, 'egon')
#     g2 = gevent.spawn(play, name='egon')
#     # g1.start()
#     g2.join()
#     g1.join()
#     # 或者gevent.joinall([g1,g2])
#     print('end')


from gevent import monkey

monkey.patch_all()
import gevent
from urllib import request
import time


def f(url):
    print('GET: %s' % url)
    resp = request.urlopen(url)
    data = resp.read()
    print('%d bytes received from %s.' % (len(data), url))


start = time.time()

gevent.joinall([
    gevent.spawn(f, 'https://itk.org/'),
    gevent.spawn(f, 'https://www.github.com/'),
    gevent.spawn(f, 'https://zhihu.com/'),
])


print(time.time() - start)
