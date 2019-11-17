# -*- coding: utf-8 -*-
# @Time    : 2019/11/15 17:31
# @Author  : Fei.Wang
# @Email   : 415892223@qq.com
# @File    : module.py
# @Software: PyCharm

'''简单计算器'''
class Calculator():
    def __init__(self, a, b):
        self.a = int(a)
        self.b = int(b)

    def add(self):
        return self.a + self.b

    def sub(self):
        return self.a - self.b

    def mul(self):
        return self.a * self.b

    def div(self):
        return self.a / self.b