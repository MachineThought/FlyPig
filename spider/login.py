# -*- coding: utf-8 -*-

import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


def init():
    firefox_login = webdriver.Firefox()  # 构造模拟浏览器
    return firefox_login


def login(firefox_login):
    # 输入账户密码
    # 我请求的页面的账户输入框的'id'是username和密码输入框的'name'是password
    time.sleep(random.randint(10, 15))
    # firefox_login.find_element_by_id('J_Quick2Static').click()
    # firefox_login.find_element_by_class_name("login-switch").click()
    firefox_login.find_element_by_id('TPL_username_1').clear()
    firefox_login.find_element_by_id('TPL_username_1').send_keys(u'leekona')
    firefox_login.find_element_by_id('TPL_password_1').clear()
    firefox_login.find_element_by_id('TPL_password_1').send_keys(u'yx738026')
    time.sleep(random.randint(10, 15))
    firefox_login.find_element_by_id('J_SubmitStatic').click()
    time.sleep(random(2,4))
    return firefox_login


def parse_page(firefox_login):
    page = firefox_login.page_source
    detail_page = BeautifulSoup(page, "html.parser")
    print(detail_page)
    return page


def request_url(firefox_login, url):
    firefox_login.get(url)


def main(url):
    firefox_login = init()
    request_url(firefox_login,url)
    current_url = firefox_login.current_url
    if current_url.find("login") >= 0:
        firefox_login = login(firefox_login)
    parse_page(firefox_login)

