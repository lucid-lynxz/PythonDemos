import os
import subprocess

print(os.name)  # posix 表示系统未linux/unix/mac os
print(os.uname())  # 显示详细的系统信息

os.environ["PATH"]
print(os.environ.get("PATH"))  # 获取系统环境变量中的 "PATH" 的值,大小写敏感,获取不到返回None
currentPath = os.path.abspath('.')  # 显示当前目录的绝对路径

newPath = os.path.join(currentPath, 'test_dir')  # 合成新路径
print(">>> newPath %s" % newPath)

# os.mkdir(newPath)  # 创建指定路径的目录
if os.path.exists(newPath):  # 判断指定路径的文件/目录是否存在
    if os.path.isfile(newPath):
        os.remove(newPath)  # 删除文件
    else:
        os.rmdir(newPath)  # 删除指定路径的目录

filePath = '/Users/lynxz/.jenkins/workspace/Sonicmoving_android/app/build.gradle'
command = "sed -n \'17p\' %s| cut -d \" -f 2 " % (filePath)
print("command = %s" % (command))
# os.system(command)

# 读取build.gralde指定行,获取属性值
import re

gradleFile = open(filePath, 'r', encoding='utf-8')
line = gradleFile.readlines()[16:17][0]
print(re.split(r'\"', line)[1])
gradleFile.close()

versionNameTest = re.split(r'\"', line)[1]
print("版本号为: %s" % versionNameTest)

with open(filePath, 'r', encoding='utf-8') as buildGradleFile:
    line = buildGradleFile.readlines()[16:17][0]
    versionName = re.split(r'\"', line)[1]
    print(versionName)

import io

with io.open(filePath, 'r', encoding='utf-8') as buildGradleFile:
    line = buildGradleFile.readlines()[16:17][0]
    versionName = re.split(r'\"', line)[1]
    print("sdfs ", versionName)

import sys

print("当前编译器版本: ", sys.version)
print(sys.version_info)
