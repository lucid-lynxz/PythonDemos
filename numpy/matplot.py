#! /usr/bin/env python
# coding=utf-8

'''
numpy结合matplotlib
'''

import numpy as np
from matplotlib import pyplot as plt

x = np.arange(1, 10)
y = 2 * x + 5

plt.title("Matplotlib demo")
plt.xlabel("x axis caption")
plt.ylabel("y axis caption")
plt.plot(x, y)
plt.show()
