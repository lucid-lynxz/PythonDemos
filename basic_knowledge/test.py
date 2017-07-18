import os
import time

print("主目录: ", os.environ['HOME'])
print("主目录: ", os.path.expanduser('~'))
down = os.path.join(os.path.expanduser('~'), "download")
print("主目录: ", down)

needToUploadPgyer = False


def test():
    print("start.... ", 100 % 5, 99 % 5, time.time())
    time.sleep(10)
    if not needToUploadPgyer:
        print("is true ", time.time())
    else:
        print("false ", time.time())


test()
