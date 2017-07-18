import requests

r = requests.get('https://github.com/timeline.json')
print(r.json())
print("==> message is : ", r.json()['message'])

# get请求
params = {'q': 'python', 'test': None}  # 字段中值为None的字段不会被添加到url中
r = requests.get('http://www.bing.com/search', params=params)
print(r.status_code, r.headers['content-type'], r.encoding)
print(r.url)

# post请求上传文件

import requests
import json
# 蒲公英相关参数
pgyerApiKey = "f5630b966aa386e144f5b1f646e477b7"
pgyerUKey = "9f2634129de0e58c06366b6e4c355b6f"

# 要上传的文件路径
apkPath = '/Users/lynxz/.jenkins/workspace/Test01/app/build/outputs/apk/PrivatePhoto_release_v0.1.1.apk'
# post请求中所需携带的信息
data = {
    '_api_key': pgyerApiKey,
    'uKey': pgyerUKey,
    'updateDescription': '测试python上传文件功能'
}

files = {'file': open(apkPath, 'rb')}
uploadUrl = 'https://qiniu-storage.pgyer.com/apiv1/app/upload'
response = requests.post(uploadUrl, data=data, files=files)
print(response)
