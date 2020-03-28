import time

# 进程
import multiprocessing

# count = 123


def test1(s, o, l):
    # print(o)
    o['a'] = 123
    # l.acquire()
    # global count
    for i in range(5):
        print(11111)
        print(s, o['a'])
        print(2222222)
        print(s, o['a'])
        time.sleep(0.1)
    # l.release()


'''
p1 = multiprocessing.Process(target=test1, args=('进程1执行中',))
p1.start()
p2 = multiprocessing.Process(target=test1, args=('进程2执行中',))
p2.start()
# p1.join()
# p2.join()
print('结束')
'''

if __name__ == '__main__':
    a = {'a': 'aaa'}
    lock = multiprocessing.Manager().Lock()

    # 进程池
    po = multiprocessing.Pool(3)
    for i in range(10):
        po.apply_async(test1, ('进程%d' % i, a, lock))
    print('开始')
    po.close()
    po.join()  # 等待进程池中进程结束， 必须放在close后
    print('结束')
    print(a)
