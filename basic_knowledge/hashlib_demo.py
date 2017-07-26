# -*- coding:utf-8 -*-
import hashlib

data = 'hello world'
md5 = hashlib.md5()
# 需要对元数据进行encode()处理
md5.update(data.encode())
# print(md5.hexdigest())
print(md5.digest())

print(hashlib.sha1(data.encode()).hexdigest())
# 使用digest()返回二进制结果
# print(hashlib.sha1(data.encode()).digest())

# 为了增加复杂度,可以考虑对源数据加盐
salt = 'salt@#$3'
print(hashlib.sha1((data + salt).encode()).hexdigest())
