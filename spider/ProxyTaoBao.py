# -*- coding: utf-8 -*-

__author__ = 'JustFantasy'

import urllib.request, urllib.parse, urllib.error
import http.cookiejar


class Taobao:
    # 初始化方法
    def __init__(self):
        # 请求的URL
        self.request_url = 'https://items.alitrip.com/item.htm?id=527730376146&spm=181.7738645.6.5.VS4WSm'
        # 代理IP地址，防止自己的IP被封禁
        self.proxy_ip = '120.193.146.97:843'
        # 登录POST数据时发送的头部信息
        self.request_headers = {
            'Host': 'login.taobao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Referer': 'https://login.taobao.com/member/login.jhtml',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'Keep-Alive'
        }
        # post数据
        self.post = {
            'id': '527730376146',
            'spm': '181.7738645.6.5.VS4WSm',
            # 'smToken': '2b38f5a07af7423b9a5fe1b0f71cf7e3',
            # 'smSign': 'smSign=dooOG9GY9RyEWF4ksEM9QQ=='
        }
        # 将POST的数据进行编码转换
        self.post_data = urllib.parse.urlencode(self.post).encode(encoding='utf-8')
        # 设置代理
        self.proxy = urllib.request.ProxyHandler({'http': self.proxy_ip})
        # 设置cookie
        self.cookie = http.cookiejar.LWPCookieJar()
        # 设置cookie处理器
        self.cookieHandler = urllib.request.HTTPCookieProcessor(self.cookie)
        # 设置登录时用到的opener，它的open方法相当于urllib2.urlopen
        self.opener = urllib.request.build_opener(self.cookieHandler, self.proxy, urllib.request.HTTPHandler)
        # 设置请求的openner,且不适用代理
        self.opener_no_proxy = urllib.request.build_opener(self.cookieHandler, urllib.request.HTTPHandler)
        # 登录成功时，需要的Cookie
        self.newCookie = http.cookiejar.CookieJar()
        # 登陆成功时，需要的一个新的opener
        self.newOpener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.newCookie))

    # 程序运行主干
    def main(self):
        # try:
            # 请求登录地址， 此时返回的页面中有两个js的引入
            # 位置是页面的前两个JS的引入，其中都带有token参数
            request = urllib.request.Request(self.request_url, self.post_data, self.request_headers)
            print(request.full_url)
            # print(str(request.data))
            response = self.opener_no_proxy.open(request)
            # response = self.opener.open(request)
            content = response.read().decode('utf-8')
            print(content)

        # except urllib.error.HTTPError as e:
        #     print(u'请求失败，错误信息：', e.msg)


taobao = Taobao()
taobao.main()
