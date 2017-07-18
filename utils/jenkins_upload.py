#!/usr/local/bin/python3.5
# -*- coding: utf-8 -*-

'''
jenkins 打包线上代码生成apk后发布到蒲公英
'''

import os
import io
import re
import requests
import json

WORKSPACE = os.getenv("WORKSPACE")  # 获取jenkins环境变量
userName = os.getenv("BUILD_USER")  # 获取用户名
# activeVirutalEnv="source %s/.env/bin/activate"%WORKSPACE
# print("启动虚拟环境的命令: %s"%activeVirutalEnv)
# os.system(activeVirutalEnv)

# 重置默认编码为utf8
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

print("当前编译器版本: %s " % sys.version)
print("python编译器详细信息: ", sys.version_info)

# 获取版本号
# guild.gralde文件所在路径
buildGradleFilePath = "%s/app/build.gradle" % (WORKSPACE)  # 指定文件所在的路径
print("gradlePath is ... ", buildGradleFilePath)

with open(buildGradleFilePath, 'r', encoding='utf-8') as buildGradleFile:
    line = buildGradleFile.readlines()[12:13][0]
    print("line is .... ", line)
    versionName = re.split(r'\"', line)[1]
    print("版本号为: %s" % versionName)

# "获取apk所在路径..."
apkAbsPath = "%s/app/build/outputs/apk/PrivatePhoto_release_v%s.apk" % (WORKSPACE, versionName)

print("上传apk到蒲公英进行发布,apk路径为: %s" % apkAbsPath)


# 上传结束后发出请求通知服务端,进而由服务端发送钉钉消息
def notify_upload_result(msg):
    headers = {'user-agent': 'jenkins_upload_pgyer'}
    params = {'userName': userName, 'msg': msg}  # 字段中值为None的字段不会被添加到url中
    response = requests.get('http://btcserver.site:8080/WebHookServer_war', params=params, headers=headers)
    #response = requests.get('http://localhost:8081', params=params, headers=headers)
    print("通知webhook服务器结果: ", response.text)


# 蒲公英账号信息
pgyerApiKey = "f5630b966aa386e144f5b1f646e477b7"
pgyerUKey = "9f2634129de0e58c06366b6e4c355b6f"

# response=$(curl -F "file=@${apkAbsPath}" -F "uKey=${pgyerUKey}" -F "_api_key=${pgyerApiKey}" -F "updateDescription=${pgyerNotes}" https://qiniu-storage.pgyer.com/apiv1/app/upload | jq .)
# post请求中所需携带的信息
data = {
    '_api_key': pgyerApiKey,
    'uKey': pgyerUKey,
    'updateDescription': '测试python上传文件功能21'
}

files = {'file': open(apkAbsPath, 'rb')}
uploadUrl = 'https://qiniu-storage.pgyer.com/apiv1/app/upload'
response = requests.post(uploadUrl, data=data, files=files)
print(response.status_code, response.text)
if response.status_code == 200:
    print("上传成功,通知webhook服务器...")
    notify_upload_result(response.text)
else:
    print("上传失败,状态码为: %s" % (response.status_code))
