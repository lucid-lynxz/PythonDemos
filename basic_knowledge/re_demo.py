import re

# 判断是否匹配,若匹配则返回 Match 对象,否则返回 None
# match从开头开始匹配
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

# match判定字符串是否符合给定的规则,从头开始判定
# search可以提取按给定规则提取子串,匹配第一次
# finall 匹配所有满足条件的子串
s = '=?UTF-8?Q?Re:_supersonic-android_|_=E5=8D=87=E7=BA=A7oifi-sdk?=\r\n=?UTF-8?Q?_1.8.1_=28#30=29?='
match = re.search(r'=\?.*\?=', s)
print(s, "   搜索子串结果:   ", match)
all_sub = re.findall(r'=\?.*\?=', s)
print("匹配所有子串结果: ", len(all_sub), type(all_sub))

for index in range(len(all_sub)):
    print("   子串 ==> ",all_sub[index])

if match:
    result = match.group()
    print('获取子串成功: ', result)
else:
    print('获取子串失败')


# 正则替换
content = "lynxz-333ha(h|(a)"
link = re.compile("\d+")
info = re.sub(link,'_',content)
print("替换数字后:  ",info)
# 替换竖线
vline = re.compile("\|")
info = re.sub(vline,'_',content)
print("替换竖线: ",info)
bracket = re.compile("\(|\)")
info = re.sub(bracket,'_',content)
print("替换括号:  ",info)

