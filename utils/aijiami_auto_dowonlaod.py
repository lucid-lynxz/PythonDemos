#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
自动下载爱加密服务器上已加密完成的so文件,并在当前目录下按so别名创建子目录并将so文件存入子目录中;
程序会尝试下载so列表中前 maxSoFileCount 条记录中文件别名前缀为 prefixAlias 的so文件(若前缀 prefixAlias 为 '', 则不做过滤判断);
注意:
    1. 同一个目录下,若so文件已存在,则不会重新下载;
    2. 若爱加密so文件加密失败,则不进行下载;
    3. 需要先安装 BeautifulSoup 和 lmxl
        pip install beautifulsoup4
        pip install lxml

so加密记录页面: http://192.168.2.199/admin/aijiami/so/so_all.do
'''

import re, os, sys, getopt, requests
from bs4 import BeautifulSoup

prefixAlias = ''  # 设置so别名前缀,只下载该别名前缀的文件,并且创建目录时会删除前缀部分
targetFolder = './'  # 下载后的so文件所要存放的根目录,会根据so别名创建子目录,并在子目录中存放下载的so文件
maxSoFileCount = 7  # 最多尝试下载so列表中前N个文件(单页20条数据,因此最大请限制20)

# 爱加密服务器地址
SERVER_URL = "http://192.168.2.199"
# 登录得账号名和密码
userName = 'xxx'
password = 'xxx'

toolInfo = '''爱加密系统自动下载功能;
默认从服务器 http://192.168.2.199 使用账户 admin 进行登录并下载so加密结果页面第一页的最多7个文件
python3 ./aijiami_auto_download.py -t /Users/lynxz/Desktop/lib  -x  test0727_
-s --server : 指定服务器地址
-u --user : 登录账号名
-p --password  : 登录密码
-t --target  : 下载的so要存放的根目录路径
-x --prefix : 值下载拌饭该前缀的文件,并且下载后会删除该前缀
-h --help : 显示帮助信息
'''

opts, args = getopt.getopt(sys.argv[1:], "hs:u:p:t:x:", ["help", "server=", "user=", "target=", "password=", "prefix="])
for name, value in opts:
    if name in ("-s", "--server"):  # 服务器地址
        SERVER_URL = value
    elif name in ("-u", "--user"):  # 登录账号名
        userName = value
    elif name in ("-p", "--password"):  # 登录密码
        password = value
    elif name in ("-t", "--target"):  # 下载后要保存的目录路径
        targetFolder = value
    elif name in ("-x", "--prefix"):  # 下载成功后要删掉的文件名前缀
        prefixAlias = value
    elif name in ("-h", "--help"):  # 显示帮助信息
        print(toolInfo)
        exit()

session = requests.session()


class SoBean(object):
    def __init__(self, status=None, soName=None, aliasName=None, id=None, time=None):
        self.status = status  # 加密状态: 已完成/加密失败/加密中
        self.soName = soName  # so文件名称
        self.aliasName = aliasName  # 加密文件别名
        self.soId = id  # so文件id,用于下载
        self.uploadTime = time  # 文件添加时间

    @classmethod
    def fetchSoIdByHref(self, href):
        '''
        处理页面中的 '下载' 链接,截取id值
        href = javascript:_operate(so_down,'94');
        '''
        soID = href
        ids = re.split(r'\'', href)
        if (len(ids) > 1):
            soID = ids[1]
        return soID

    def updateData(self, index, value):
        if index == 0:
            self.status = value
        elif index == 1:
            self.soName = value
        elif index == 3:
            self.aliasName = value
        elif index == 4:
            self.uploadTime = value
        elif index == 7:
            self.soId = self.fetchSoIdByHref(value)


def build_url(path):
    return '/'.join([SERVER_URL, path])


# 刷新cookie成功后获取so加密列表页面源码
def get_so_page(r, *args, **kwargs):
    if r.status_code == 200:
        res = session.get(build_url('admin/aijiami/so/so_all.do'))
        soup = BeautifulSoup(res.text, 'lxml')
        all_tr = soup.find('tbody', attrs={'class': 'pn-ltbody'}).find_all('tr')
        soBeanArr = []
        for tr in all_tr:
            bean = SoBean()
            all_td = tr.find_all('td')
            for tdIndex, td in enumerate(all_td):
                value = ''

                all_div = td.find_all('div')
                if len(all_div) > 0:
                    value = all_div[0]['title']

                all_a = td.find_all('a', attrs={'class': 'pn-loperator'})
                if len(all_a) > 0:
                    value = all_a[0]['href']

                bean.updateData(tdIndex, value)

            soBeanArr.append(bean)
        start_download_so(soBeanArr)


# 从给定的so加密列表中下载已完成的项,每种别名下载一次,若已下载过,则不再下载
def start_download_so(soBeanArr):
    if len(soBeanArr) >= maxSoFileCount:
        soBeanArr = soBeanArr[:maxSoFileCount]

    for bean in soBeanArr:
        if prefixAlias != '':
            if bean.aliasName.startswith(prefixAlias):
                bean.aliasName = bean.aliasName[len(prefixAlias):]
            else:
                continue

        r = session.post(build_url('admin/aijiami/so/so_down.do'), data={'id': bean.soId})
        if r.status_code == 200:
            targetSoFolderPath = os.path.join(targetFolder, bean.aliasName)
            if not os.path.exists(targetSoFolderPath):
                os.makedirs(targetSoFolderPath)
                # os.mkdir(targetSoFolderPath)

            libPath = os.path.join(targetSoFolderPath, bean.soName)
            # 之前指定别名目录下未下载过该so文件,且so文件已加密完成才下载
            if os.path.exists(libPath):
                print('===> 下载失败: 本地 %s 已存在,不再重复下载爱加密文件(id =%s),文件上传时间:%s' % (libPath, bean.soId, bean.uploadTime))
            else:
                if bean.status == '已完成':
                    with open(libPath, 'wb') as f:
                        f.write(r.content)
                    print("%s 下载成功" % libPath)
                else:
                    print("===> 下载失败: 爱加密 %s(id=%s),状态为:%s,不进行下载,请稍后尝试,文件上传时间为:%s" % (
                        libPath, bean.soId, bean.status, bean.uploadTime))


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
                 hooks=dict(response=get_so_page))


refresh_cookie()
