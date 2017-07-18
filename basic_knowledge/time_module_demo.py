from datetime import datetime

# 打印现在的时间
now = datetime.now()
print("%s %s" % (now, type(now)))

# 指定日期和时间,timestamp的转换
df = datetime(2017, 3, 3, 14, 35)
timeStamp = df.timestamp()  # 浮点数,小数位表示毫秒
print("%s %s %s" % (df, timeStamp, datetime.fromtimestamp(timeStamp)))

# str 转换为 datetime ,字符串时间得写全
sday = datetime.strptime('2017-03-03 14:39:00', '%Y-%m-%d %H:%M:%S')
print(sday)
print(now.strftime('%a, %b %d %H:%M'))
