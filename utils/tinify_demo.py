import tinify
import os

'''
https://github.com/saitjr/STTinyPNG-Python/blob/master/STTinyPNG-Python.py
tinify库批量压缩图片
需要先安装tinify库: pip install --upgrade tinify
不支持目录嵌套
'''
tinify.key = "****"  # AppKey, 到 https://tinypng.com/developers 申请
fromFilePath = "/Users/lynxz/Desktop/tinypng"  # 源路径
toFilePath = "/Users/lynxz/Desktop/test2"  # 输出路径

for root, dirs, files in os.walk(fromFilePath):
    for name in files:
        fileName, fileSuffix = os.path.splitext(name)
        if fileSuffix == '.png' or fileSuffix == '.jpg':
            toFullPath = toFilePath + root[len(fromFilePath):]
            toFullName = toFullPath + '/' + name

            if not os.path.isdir(toFullPath):
                os.mkdir(toFullPath)

            srcFilePath = os.path.join(fromFilePath, name)

            with open(srcFilePath, 'rb') as source:
                source_data = source.read()
                result_data = tinify.from_buffer(source_data).to_buffer()
                with open(toFullName, 'wb') as target:
                    target.write(result_data)
                    print("write %s success " % name)