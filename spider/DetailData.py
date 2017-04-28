# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import random
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver


class DetailSpider():
    def __init__(self):
        self.broswer_client = webdriver.Firefox()
        self.request_url = "https://items.alitrip.com/item.htm"
        self.request_header = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "accept-language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,it;q=0.2",
            "cache-control": "no-cache",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
        }
        self.request_data = {
            "id": "",
            "smToken": "",
            "smSign": "",
            "spm": ""
        }
        self.spider_data = {
            "shopName": "",
            "descSorce": 4.5,
            "serverSorce": 4.5,
            "logisticsScore": 4.5,
            "title": "",
            "company": "",
            "location": "",
            "fromCity": "",
            "destCity": "",
            "price": "",
            "minPrice": 0,
            "maxPrice": 0,
            "sellCount": 0,
            "gradeAvg": 4.5,
            "rateTotal": 0,
            "days": 1,
            "promise": ""
        }
        self.default_spider_data = {
            "shopName": "",
            "descSorce": 4.5,
            "serverSorce": 4.5,
            "logisticsScore": 4.5,
            "title": "",
            "company": "",
            "location": "",
            "fromCity": "",
            "destCity": "",
            "price": "",
            "minPrice": 0,
            "maxPrice": 0,
            "sellCount": 0,
            "gradeAvg": 4.5,
            "rateTotal": 0,
            "days": 1,
            "promise": ""
        }

    def __set_request_data(self, item_id, sm_token="", sm_sign="", spm=""):
        self.request_data["id"] = item_id
        self.request_data["smToken"] = sm_token
        self.request_data["smSign"] = sm_sign
        self.request_data["spm"] = spm

    def set_sm_param(self, sm_token, sm_sign):
        self.__set_request_data(self.request_data["id"], sm_token, sm_sign, self.request_data["spm"])

    def set_item_id(self, item_id):
        self.__set_request_data(item_id, self.request_data["smToken"], self.request_data["smSign"], self.request_data["spm"])

    def __get_url_params(self):
        data = self.request_data
        return "id=%s&smToken=%s&smSign=%s&spm=%s" % (data["id"], data["smToken"], data["smSign"], data["spm"])

    def __get_full_url(self):
        return self.request_url + "?" + self.__get_url_params()

    def reset_data(self):
        for data in self.spider_data:
            self.spider_data[data] = self.default_spider_data[data]

    def __parse_page(self, page):
        detail_page = BeautifulSoup(page, "html.parser")
        # print(type(detail_page))
        shop_name_tag = detail_page.find("a", {"class": "slogo-shopname"})
        h_shopcard_scores = detail_page.select(".h-shopcard-scores a")
        h_shopcard_seller = detail_page.find("div", {"class": "h-shopcard-mid"}).find("dl")
        detail_hd = detail_page.find("div", {"class": "detail-hd"}).find("h1")
        price = detail_page.find("span", {"class": "detail-price J_PriceWrap"})
        sell_count = detail_page.find("em", {"class": "ml J_SellCount"})
        grade = detail_page.find("em", {"class": "J_Grade"})
        comment = detail_page.find("span", {"class": "J_Comment"})
        other_info = detail_page.select("#J_ItemPropWrap > dd")
        if len(other_info) <= 1:
            return {}
        store_info = []
        for info in h_shopcard_seller:
            temp = str(info.string).strip()
            if temp != "None" and temp != "":
                store_info.append(temp[temp.find("：") + 1:])

        self.spider_data["shopName"] = list(shop_name_tag)[0]
        self.spider_data["descSorce"] = str(h_shopcard_scores[0].text).strip()
        self.spider_data["serverSorce"] = str(h_shopcard_scores[1].text).strip()
        self.spider_data["logisticsScore"] = str(h_shopcard_scores[2].text).strip()
        self.spider_data["company"] = store_info[-2]
        self.spider_data["location"] = store_info[-1]
        self.spider_data["title"] = str(detail_hd.text).strip().split("\n")[0]
        self.spider_data["price"] = price.text
        if price.text != "":
            price_list = str(price.text).split("~")
            if len(price_list) == 1:
                self.spider_data["minPrice"] = self.spider_data["maxPrice"] = int(price_list[0])
            elif len(price_list) == 2:
                self.spider_data["minPrice"] = float(price_list[0])
                self.spider_data["maxPrice"] = float(price_list[1])

        self.spider_data["sellCount"] = int(sell_count.text)
        self.spider_data["gradeAvg"] = float(grade.text)
        self.spider_data["rateTotal"] = int(comment.text)
        from_city = other_info[0].select("span")
        # print(from_city)
        for city in from_city:
            self.spider_data["fromCity"] = self.spider_data["fromCity"] + city.text.strip() + " "
        dest_city = other_info[1].select("span")
        # print(dest_city)
        for city in dest_city:
            self.spider_data["destCity"] = self.spider_data["destCity"] + city.text.strip() + " "

        self.spider_data["days"] = int(re.findall("[0-9]+", other_info[2].text.strip())[0])

        promise_info = other_info[3:]
        # print(promise_info)
        for promise in promise_info:
            # print(promise.text.strip())
            self.spider_data["promise"] = self.spider_data["promise"] + " " + promise.text.strip().lstrip()
        self.spider_data["promise"] = " ".join(self.spider_data["promise"].split("\n")).strip()
        # print(self.spider_data)

    def sleep(self, sleep_time, period=10):
        while sleep_time > 0:
            print(sleep_time)
            time.sleep(period)
            sleep_time = sleep_time - period

    def login(self):
        # 输入账户密码
        # 我请求的页面的账户输入框的'id'是username和密码输入框的'name'是password
        time.sleep(random.randint(10, 15))
        # firefox_login.find_element_by_id('J_Quick2Static').click()
        # firefox_login.find_element_by_class_name("login-switch").click()
        self.broswer_client.find_element_by_id('TPL_username_1').clear()
        self.broswer_client.find_element_by_id('TPL_username_1').send_keys(u'leekona')
        self.broswer_client.find_element_by_id('TPL_password_1').clear()
        self.broswer_client.find_element_by_id('TPL_password_1').send_keys(u'41751')
        time.sleep(random.randint(10, 15))
        self.broswer_client.find_element_by_id('J_SubmitStatic').click()
        time.sleep(random(2, 4))
        # current_url = self.broswer_client.current_url

    def reboot(self):
        # 停留50s 用于手动登陆账号
        time.sleep(50)
        self.broswer_client.quit()
        self.broswer_client = webdriver.Firefox()

    def spider(self, item_id):
        self.reset_data()
        # print("打印重置后数据")
        # print(self.spider_data)
        self.set_item_id(item_id)
        self.broswer_client.get(self.__get_full_url())
        page = ""
        try:
            page = self.broswer_client.page_source
            self.__parse_page(page)
        except Exception as err:
            print(err)
            current_url = self.broswer_client.current_url
            if current_url.find("login") > 0:
                self.reboot()
                self.sleep(60, 20)
            return {}

        print("打印解析后的数据")
        print(self.spider_data)
        if self.spider_data["shopName"] == "":
            return {}
        return self.spider_data

# detail_spider = DetailSpider()
# detail_spider.spider("528037383954")
# # print("2199~2498".split("~"))
