# 拼接字符串
print('a'.join('bcd'))
# 拼接多个字符
s1 = ['a','b','c','d']
result = '%s%s%s%s'%tuple(s1)
print(result)

# 大小写转换
print("abc".upper())
print("ABc".lower())



s = "abcdefg"
print(s[0:2])  # ab
print(s[:2])  # ab
print(s[-2:])  # fg
print(s[::2])  # aceg
s1 = s[:] # 表示复制一个
print(s1) # abcdefg