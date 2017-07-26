# -*- coding:utf-8 -*-

import random

# 生成 [0,1.0) 之间的随机浮点数
print(random.random())
# 生成指定范围内的随机浮点数 [from,to]
print(random.uniform(1, 5))
# 生成指定范围内的随机整数 [from,to]
print(random.randint(1, 5))
# 从指定的range中随机获取一个数
print(random.randrange(1, 10, 2))

# 从sequence中随机获取一个
print(random.choice("hello"))
print(random.choice(['hello', 'nice', 'world']))

# 将原有序列表进行乱序排列
src = ["Python", "is", "powerful", "simple", "and so on..."]
random.shuffle(src)  # 返回None
print(src)
