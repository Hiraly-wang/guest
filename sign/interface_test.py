# -*- coding: utf-8 -*-
# @Time    : 2019/11/20 10:51
# @Author  : Fei.Wang
# @Email   : 415892223@qq.com
# @File    : interface_test.py
# @Software: PyCharm

'''将接口测试集成到unittest单元测试框架中'''

import unittest

import requests

'''查询发布会接口测试'''


class GetEventListTest(unittest.TestCase):

    def setUp(self):
        self.url = 'http://127.0.0.1:8000/api/get_event_list/'

    '''发布会ID为空'''

    def test_get_event_null(self):
        r = requests.get(self.url, params={'eid': ''})
        result = r.json()
        self.assertEqual(result['status'], '10021')
        self.assertEqual(result['message'], 'Parameter error')

    '''发布会ID不存在'''

    def test_get_event_error(self):
        r = requests.get(self.url, params={'eid': '901'})
        result = r.json()
        self.assertEqual(result['status'], '10022')
        self.assertEqual(result['message'], 'query result is empty')
    '''发布会查询成功'''
    def test_event_success(self):
        r=requests.get(self.url,params={'eid':'1'})
        result=r.json()
        self.assertEqual(result['status'],'200')
        self.assertEqual(result['message'],'success')
        self.assertEqual(result['data']['name'],'小米发布会')
        self.assertEqual(result['data']['start_time'],'2019-11-14T23:34:25')


if __name__ == '__main__':
    unittest.main()
