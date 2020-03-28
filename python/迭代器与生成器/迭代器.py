'''
# 迭代器
l1 = [1, 2, 3, 4]
it = iter(l1)    # 创建迭代器对象
# it = l1
print(type(l1))
print(type(it))
for x in it:
    print(x, end=" ")
'''

'''
import sys  # 引入 sys 模块

l1 = [1, 2, 3, 4]
it = iter(l1)  # 创建迭代器对象

while True:
    try:
        print(next(it))
    except StopIteration:
        sys.exit()
'''


# 创建一个迭代器
import sys


class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        if self.a <= 20:
            x = self.a
            self.a += 1
            return x
        else:
            raise StopIteration


myclass = MyNumbers()
myiter = iter(myclass)

while True:
    try:
        print(next(myiter))
    except StopIteration:
        sys.exit()

# for x in myiter:
#     print(x)
