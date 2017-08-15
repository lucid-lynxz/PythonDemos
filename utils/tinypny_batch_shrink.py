from os.path import dirname
from base64 import b64encode
import requests, json, sys, os, time

# created by qianzui at 2014/05/25
key = "hx84BKJQorWsz3zMk5Ogr6mR92Zv-eby"  # https://tinypng.com/developers 申请自己的key
src_dir = "/Users/lynxz/Desktop/mipmap-xxhdpi"  # 源图片文件所在目录
dest_dir = "/Users/lynxz/Desktop/tinyres_xxhdpi"  # 压缩完成后,下载时要保存到的目录
record = {}

tinypng_shrink_url = "https://api.tinify.com/shrink"

auth = ('api', key)


def tinypng(src_dir, dest_dir):
    if not os.path.isdir(src_dir):
        print("src_dir( %s ) is not a valid folder,please retry..." % src_dir)
        return

    for curfile in os.listdir(src_dir):
        full_path = os.path.join(src_dir, curfile)
        if os.path.isdir(full_path):
            tinypng(full_path, os.path.join(dest_dir, curfile))
        # 处理 png 和 jpg 图像
        elif curfile.lower().find(".png") != -1 \
                or curfile.lower().find(".jpg") != -1:
            print("current tiny image : %s" % full_path)

            # 若要保存的目录不存在,则创建
            if not os.path.isdir(dest_dir):
                os.makedirs(dest_dir)

            data = open(full_path, 'rb').read()
            response = requests.post(tinypng_shrink_url, data=data, auth=auth)
            print(response)
            if response.status_code == 201:
                # Compression was successful, retrieve output from Location header.
                download_url = response.headers['Location']
                print("tinypng download url : " + download_url)
                result = requests.get(download_url)
                output_path = os.path.join(dest_dir, curfile)
                open(output_path, "wb").write(result.content)
                print("download %s Success" % curfile)
            else:
                print("error")
                # Something went wrong! You can parse the JSON body for details.
                # print("error : " + result_json["error"] + "\n message : " + result_json["message"])


# def write_record(record_file):
#     # write result
#     output = open(record_file, 'w')
#     for k, v in record.iteritems():
#         line = "%s\t%s\n" % (k, v)
#         line = line.encode('utf-8')
#         output.write(line)
#     print("write record completed!")
#     output.close()


if __name__ == "__main__":
    # if len(sys.argv) == 3:
    # src_dir = sys.argv[1]
    # dest_dir = sys.argv[2]

    tinypng(src_dir, dest_dir)
    # record_file = os.path.join(dest_dir, time.strftime("%Y%m%d-%H%M%S") + ".txt")
    # write_record(record_file)
    # else:
    #     print("Usage : python image_dir result_dir")
