import requests, os
from datetime import datetime

key = "xjmdkNmFzDDDbPsROGveKT5-uDArTu7s"  # https://tinypng.com/developers 申请自己的key
src_dir = "/Users/lynxz/Desktop/test"  # 源图片文件所在目录
dest_dir = "/Users/lynxz/Desktop/test2"  # 压缩完成后,下载时要保存到的目录
record = {}

tinypng_shrink_url = "https://api.tinify.com/shrink"

auth = ('api', key)


def getCurrentTime():
    return datetime.now().strftime('%a, %b %d %H:%M:%S')


def tinypng(srcDir, destDir):
    if not os.path.isdir(srcDir):
        print("%s srcDir( %s ) is not a valid folder,please retry..." % (getCurrentTime(), srcDir))
        return

    srcFiles = os.listdir(srcDir)
    totalSize = len(srcFiles)
    index = 0
    print("%s 当前目录 %s 共有文件: %s 个" % (getCurrentTime(), srcDir, totalSize))
    for curfile in srcFiles:
        full_path = os.path.join(srcDir, curfile)
        index += 1
        if os.path.isdir(full_path):
            tinypng(full_path, os.path.join(destDir, curfile))

        # 处理 png 和 jpg 图像
        elif curfile.lower().find(".png") != -1 \
                or curfile.lower().find(".jpg") != -1:
            print("%s 正在处理image(%s/%s) : %s" % (getCurrentTime(), index, totalSize, full_path))

            # 若要保存的目录不存在,则创建
            if not os.path.isdir(destDir):
                os.makedirs(destDir)

            data = open(full_path, 'rb').read()
            response = requests.post(tinypng_shrink_url, data=data, auth=auth)
            print(response.text)
            if response.status_code == 201:
                download_url = response.headers['Location']
                print("%s tinypng download url : %s" % (getCurrentTime(), download_url))
                result = requests.get(download_url)
                output_path = os.path.join(destDir, curfile)
                open(output_path, "wb").write(result.content)
                print("%s download %s Success" % (getCurrentTime(), curfile))
            else:
                print("%s 发生错误,停止处理..." % getCurrentTime())


if __name__ == "__main__":
    tinypng(src_dir, dest_dir)
