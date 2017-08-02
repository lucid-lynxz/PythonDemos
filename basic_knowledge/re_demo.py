import re

# 判断是否匹配,若匹配则返回 Match 对象,否则返回 None
obj = re.match(r'^\d{3}-\d{3,8}$', '010-12345')
if obj:
    print("匹配成功")
else:
    print("匹配失败")

# 正则切分字符串
s = 'a b  c    d'
split = s.split(' ')
# 常规的 split 方法无法处理多个空格的问题
for sp in split:
    print(sp)

# 正则切分,多个空格情况
split = re.split(r'\s+', s)
for sp in split:
    print(sp)

# 正则表达式配合 '()' 表示分组,可以提取单独分组的内容
m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
print("group大小: ", len(m.groups()))
print(m.group(0))  # 返回原始字符串
print(m.group(1))  # 返回第1个子串
print(m.group(2))  # 返回第2个子串

# match判定字符串是否符合给定的规则
# search可以提取按给定规则提取子串
s = '"=?gb2312?B?zNrRtsbz0rXTys/k?="'
match = re.search(r'=\?.*\?=', s)
print(s, "   搜索子串结果:   ", match)
if match:
    result = match.group()
    print('获取子串成功: ', result)
else:
    print('获取子串失败')
