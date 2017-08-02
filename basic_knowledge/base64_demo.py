#!/usr/local/bin/python3.5
# -*- coding: utf-8 -*-

'''
base64简单的加解密
'''

import base64

src = '长夜漫漫无心睡眠'

result = base64.b64encode(src.encode(encoding='utf8'))
print('encode result is: %s' % result)

decode_result = base64.b64decode(result)
print(str(decode_result, 'utf8'))
