#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
自动上传 libSoundBus.so 到爱加密平台进行加密
别名自动添加为so文件所在父目录名,如 folder/a.so ,则别名为 folder
另外, 通过修改变量 prefixAliasStr 的值,可以给别名添加前缀信息
需要先安装requests
'''

import requests, re, os, sys, getopt
import urllib.parse

# 要上传的so文件所在的目录(会遍历其下所有子目录并寻找so文件)
rootFolderPath = './'  # 遍历当前目录请写 ./
prefixAliasStr = ''  # 别名前缀,暂时请勿使用中文

# 爱加密服务器地址
SERVER_URL = "http://192.168.2.199"
# 登录得账号名和密码
userName = 'xxx'
password = 'xxx'
toolInfo = '''爱加密系统自动上传so并加密;
默认从服务器 http://192.168.2.199 使用账户 admin 进行登录并上传指定根目录下所有so(遍历,排除mips架构)
python3 ./aijiami_auto_upload.py -r /Users/lynxz/Desktop/lib  -x  test0727_
-r --root : 指定要上传的so所在的根目录
-s --server : 指定服务器地址
-u --user : 登录账号名
-p --password  : 登录密码
-x --prefix : 值下载拌饭该前缀的文件,并且下载后会删除该前缀
-h --help : 显示帮助信息
'''
opts, args = getopt.getopt(sys.argv[1:], "r:s:u:p:x:", ["root=", "server=", "user=", "password=", "prefix="])
for name, value in opts:
    if name in ("-r", "--root"):  # so所在根目录
        rootFolderPath = value
    if name in ("-s", "--server"):  # 服务器地址
        SERVER_URL = value
    elif name in ("-u", "--user"):  # 登录账号名
        userName = value
    elif name in ("-p", "--password"):  # 登录密码
        password = value
    elif name in ("-x", "--prefix"):  # 前缀
        prefixAliasStr = value
    elif name in ("-h", "--help"):  # 显示帮助信息
        print(toolInfo)
        exit()

session = requests.session()


# 生成完成路径,如 path = hello 时 => http://192.168.2.199/hello
def build_url(path):
    return '/'.join([SERVER_URL, path])


# 刷新cookie成功后开始上传
def start_upload(r, *args, **kwargs):
    print("start_upload ---> ", r.url)
    print(r.status_code, r.cookies)
    print(r.request.headers)
    print(r.headers)
    if r.status_code == 200:
        traverse_folder(rootFolderPath)


# 刷新cookie,用于后续上传so成功后的提交加密操作
def refresh_cookie():
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;',
        'Accept-Language': 'en-US,zh-CN;q=0.8,zh;q=0.6,en;q=0.4'
    }
    data = {
        'loginName': userName,
        'password': password
    }
    # 使用 session 来自动保存本接口返回的 set-cookie 值
    session.post(build_url('CmsSubmit.do'), headers=headers, data=data,
                 hooks=dict(response=start_upload))


# 上传完so文件后,确定提交并开始加密
def add_so_file(soInfo):
    headers = {
        # 注意这里需要登录信息,上传so文件还不需要,提交加密需要,这里使用reqeust.session来保存接口返回的 set-cookie 值
        # 'Cookie': 'OSENC_SESSION=5D294567DA2860CFEF9E4138944F21FB',
        'Content-type': 'application/x-www-form-urlencoded;',
        'Accept-Language': 'en-US,zh-CN;q=0.8,zh;q=0.6,en;q=0.4'
    }

    if (not soInfo or len(soInfo) < 4):
        print("argument invalid ", soInfo)
        return

    # 这里手动转换编码还不行, requests 默认会urlencode,但是使用的是utf-8, 我还不晓得怎么定制成gbk,所以前缀暂时不要用中文,不然乱码
    # alias = urllib.parse.quote(prefixAliasStr + soInfo[3], encoding='gbk')
    alias = prefixAliasStr + soInfo[3]
    data = {
        'pageNo': '1',
        'soBean.soName': soInfo[0],  # 文件名
        'soBean.soSize': soInfo[1],  # 文件大小
        'soBean.soUrl': soInfo[2],  # 文件缓存在tomcat上的路径
        'soBean.soDesc': alias  # 文件描述信息
    }
    response = session.post(build_url('admin/aijiami/so/so_add.do'), headers=headers, data=data)
    if response.status_code == 200:
        print("提交成功...")
    else:
        print("提交失败...", response.text)


# 上传so文件
def upload_so_file(soPath):
    with open(soPath, 'rb') as soFile:
        if os.path.isfile(soPath):
            print("正在上传so文件: ", soPath)
            fileName = os.path.split(soPath)[1]
            parentFolderName = os.path.split(os.path.dirname(soPath))[1]
            if 'mips' in parentFolderName:
                print('爱加密不支持mips,不进行处理')
                return
            # print("文件名称: ", fileName)
            # print("父目录名称: ", parentFolderName)
            data = {
                'Content-type': 'multipart/form-data;',
                'Filename': fileName
            }
            files = {'upload': (fileName, soFile)}
            response = session.post(build_url('soUpload.do'), data=data, files=files)
            print('上传so结果: ', response.status_code, response.text)
            if response.status_code == 200:
                info = re.split(r'\$##\$', response.text)
                info.append(parentFolderName)
                print(info)
                add_so_file(info)


# 遍历指定的根目录下所有扩展名为 extName 的文件
def traverse_folder(rootDirPath, extName='.so'):
    if rootDirPath == '':
        rootDirPath = os.path.abspath(os.curdir)

    print("rootFolderPath --->  ", rootDirPath)
    if os.path.isdir(rootDirPath):
        for parent, dirNames, fileNames in os.walk(rootDirPath):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in fileNames:  # 输出文件信息
                filePath = os.path.join(parent, filename)
                ext = os.path.splitext(filePath)[1]
                if ext == extName:
                    print("搜索到so文件: ", filePath)
                    upload_so_file(filePath)


refresh_cookie()
