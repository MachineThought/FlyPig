# -*- coding: utf-8 -*-

import json
import re
import time
import urllib
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

# from spider.writelog import *


def dest_list():
    # 访问飞猪旅游目的地页面,获取所有目的地路径集合
    # :return: 返回记录目的地页面地址和中文名称的字典集合
    # 目的地请求地址 固定
    start_url = "https://www.fliggy.com/place/"
    # 结果集
    link_list = []
    headers = {
        # "Host": "https://www.fliggy.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        # "Referer": "https://www.alitrip.com/",
        # "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "ccept-Encoding": "gzip, deflate, br",
        # "Upgrade-Insecure-Requests": "1",
        "Cookie": "cna=NZMpEDkX83oCAXJhyNCKzeCE; l=AkpKIxaeIg5Yx0ty9A/-87VeGjvsOM6E; "
                  "isg=AmtrPvZPt0wEbeubgXFvxMap-o91aH8CQM-zSt3oRKoQfIveZVAPUgneoArp; "
                  "hng=CN%7Czh-cn%7CCNY; uc1=cookie15=W5iHLLyFOGW7aA%3D%3D; tracknick=leekona; "
                  "_l_g_=Ug%3D%3D; unb=1013953910; cookie1=BdLQ5YYRcp2rWefq8iiYogbfAmc6OkErzXgW0I48r6Y%3D; "
                  "cookie17=UoH%2B5fRHjXjPUA%3D%3D; cookie2=f1361b8b4945f6de426fe3d4a512928a; _nk_=leekona; "
                  "uss=WqP3bHsBznckNOw%2F5ul1Av2APVoSMeSqZ8%2F32quQZnM0b%2B0uhHQcm52y; t=1b103ff8ae6035d023fe5d06f72e8651; "
                  "skt=8775973712a23e51; _tb_token_=EZDMe5by9BWV"
    }

    request = urllib.request.Request(start_url)
    for key in headers:
        request.add_header(key, headers[key])
    response = urllib.request.urlopen(request)
    # print(type(response.read))
    # print(response.read)
    dest_page = BeautifulSoup(response, "html.parser")
    for li in dest_page.findAll("li", {"class": "city-item"}):
        a_tag = li.children
        for link in a_tag:
            href = link["href"]
            if href[0] == "/":
                href = "https:" + href
            text = link.string
            # print(href, text)
            link_list.append({"href": href, "cityName": text})
    return link_list


def city_travel(city, page_start=1, page_size=5):
    city_travel_url = "https://place.alitrip.com/ajax/structuredSearch"

    data = {
        "destName": urllib.parse.quote(city),
        "travelType": "",
        "destCity": "",
        "pageStart": str(page_start),
        "pageSize": str(page_size),
        "_ksTS": "",
        "callback": ""
    }
    params = ""
    for key in data:
        params = params + "&" + key + "=" + data[key]

    request = urllib.request.Request(str(city_travel_url + "?" + str(params[1:])))

    response = urllib.request.urlopen(request.get_full_url())
    json_text = response.read().decode("utf8")
    json_obj = json.loads(json_text)
    return json_obj


def list_travel_city(city):
    final_trave_city_list = []
    first_json = city_travel(city)
    second_json = city_travel(city, page_size=first_json["viewtotal"])
    item_json = second_json["items"]
    for item in item_json:
        fields = item["fields"]
        item_info = {}
        item_info["itemId"] = str(fields["itemId"])
        item_info["title"] = fields["title"]
        item_info["sellerNick"] = fields["sellerNick"]
        item_info["wangwang"] = fields["wangwang"]
        item_info["travelType"] = " ".join(list(fields["travelType"]))
        item_info["fromCity"] = " ".join(list(fields["fromCity"]))
        item_info["destCity"] = " ".join(list(fields["destCity"]))
        final_trave_city_list.append(item_info)
    return final_trave_city_list


def city_travle_path():
    return ""


def detail_travle(path_id):
    # 542279358429
    tarvel_info = {}
    detail_travle_url = "https://items.alitrip.com/item.htm"
    headers = {
        "authority": "tdskip.alitrip.com",
        "method": "GET",
        "path": "/item.htm?spm=181.7738645.6.5.VS4WSm&id=" + path_id,
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        # "accept-encoding": "gzip, deflate, sdch, br",
        "accept-language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,it;q=0.2",
        "cache-control": "no-cache",
        "cookie": "hng=CN%7Czh-cn%7CCNY; uc1=cookie15=URm48syIIVrSKA%3D%3D; tracknick=leekona; _l_g_=Ug%3D%3D; unb=1013953910; cookie1=BdLQ5YYRcp2rWefq8iiYogbfAmc6OkErzXgW0I48r6Y%3D; cookie17=UoH%2B5fRHjXjPUA%3D%3D; cookie2=b8741c6c6ccdffd2bbf5414a711af65d; _nk_=leekona; uss=Vy%2FJTjOhpRJsaEn8NrtgeuZd2bo%2B%2BbyWxIHtgCytHVolyyqw6k3aqI%2B7; t=1b103ff8ae6035d023fe5d06f72e8651; skt=88df9484c3299c89; _tb_token_=hipTO0kGrPgf; cna=NZMpEDkX83oCAXJhyNCKzeCE; l=ApWVwXTwZV8rHqRzdxYYvYi-JZtPkkmk; isg=Aj09yDqiOF2oHp3NI1ux2gTjTJlnCnEswlUl_P-CeRTDNl1oxyqB_Avklt2K",
        "pragma": "no-cache",
        "referer": "https://place.alitrip.com/beijing?spm=181.62882.251445.1.hG3Hrs",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
    }
    data = {
        "id": path_id,
        "smToken": "2b38f5a07af7423b9a5fe1b0f71cf7e3",
        "smSign": "dooOG9GY9RyEWF4ksEM9QQ==",
        "spm": "181.7738645.6.5.VS4WSm"
    }
    params = ""
    for key in data:
        params = params + "&" + key + "=" + data[key]

    request = urllib.request.Request(str(detail_travle_url + "?" + str(params[1:])))

    print(request.full_url)
    for key in headers:
        request.add_header(key, headers[key])

    # response = urllib.request.urlopen(request)
    try:
        response = urllib.request.urlopen(request)
    except:
        print("请求详情页出错")
        return tarvel_info

    # file_object = open('detail.html', 'r', encoding='utf-8')
    # detail_page = BeautifulSoup(file_object.read(), "html.parser")
    # file_object.close()
    detail_page = BeautifulSoup(response, "html.parser")

    # print(detail_page)

    shop_name_tag = detail_page.find("a", {"class": "slogo-shopname"})
    h_shopcard_scores = detail_page.select(".h-shopcard-scores a")
    h_shopcard_seller = ""
    try:
        h_shopcard_seller = detail_page.find("div", {"class": "h-shopcard-mid"}).find("dl")
    except:
        sleep_time = 60
        print("验证过期,暂停"+str(sleep_time)+"s")
        time.sleep(sleep_time)
        return {}
    detail_hd = detail_page.find("div", {"class": "detail-hd"}).find("h1")
    # price = detail_page.find("span", {"class": "detail-price J_PriceWrap"})
    # sell_count = detail_page.find("em", {"class": "ml J_SellCount"})
    # grade = detail_page.find("em", {"class": "J_Grade"})
    # comment = detail_page.find("span", {"class": "J_Comment"})
    other_info = detail_page.select("#J_ItemPropWrap > dd")
    if len(other_info) <= 1:
        return {}
    # print(other_info[1].select("span")[0].text.strip())
    store_info = []
    for info in h_shopcard_seller:
        temp = str(info.string).strip()
        if temp != "None" and temp != "":
            store_info.append(temp[temp.find("：") + 1:])

    tarvel_info["shopName"] = list(shop_name_tag)[0]
    tarvel_info["descSorce"] = str(h_shopcard_scores[0].text).strip()
    tarvel_info["serverSorce"] = str(h_shopcard_scores[1].text).strip()
    tarvel_info["logisticsScore"] = str(h_shopcard_scores[2].text).strip()
    tarvel_info["company"] = store_info[-2]
    tarvel_info["location"] = store_info[-1]
    tarvel_info["title"] = str(detail_hd.text).strip().split("\n")[0]
    # tarvel_info["price"] = price.text
    # tarvel_info["sellCount"] = sell_count.text
    # tarvel_info["gradeAvg"] = grade.text
    # tarvel_info["rateTotal"] = comment.text
    # tarvel_info["fromCity"] = other_info[0].text.strip(" \n")
    # tarvel_info["destCity"] = other_info[1].text.strip(" \n")
    tarvel_info["fromCity"] = ""
    tarvel_info["destCity"] = ""
    from_city = other_info[0].select("span")
    for city in from_city:
        tarvel_info["fromCity"] = tarvel_info["fromCity"] + city.text.strip() + " "
    dest_city = other_info[1].select("span")
    for city in dest_city:
        tarvel_info["destCity"] = tarvel_info["destCity"] + city.text.strip() + " "
    try:
        tarvel_info["days"] = re.findall("[0-9]+", other_info[2].text.strip())[0]
    except:
        print("解析天数出错")
        return {}
    tarvel_info["promise"] = ""

    promise_info = other_info[3:]

    for promise in promise_info:
        tarvel_info["promise"] = tarvel_info["promise"] + " " + promise.text.strip().lstrip()
    tarvel_info["promise"] = " ".join(tarvel_info["promise"].split("\n")).strip()

    return tarvel_info


def seller_info(path_id):
    seller_info_url = "https://tdskip.alitrip.com/initItemDetail.do?itemId=" + path_id + "&key&u_channel=&i_channel=&ref=&t_trace_id=&" \
                                                                                         "t_trace_q=&spm=181.7738645.6.5.qDUWvE&_ksTS=1493180286711_133&callback=jsonp134"
    headers = {
        "authority": "tdskip.alitrip.com",
        "method": "GET",
        "path": "/initItemDetail.do?itemId=" + path_id + "&key&u_channel=&i_channel=&ref=&t_trace_id=&t_trace_q=&spm=181.7738645.6.5.qDUWvE&_ksTS=1493180286711_133&callback=jsonp134",
        "scheme": "https",
        "accept": "*/*",
        # "accept-encoding": "gzip, deflate, sdch, br",
        "accept-language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,it;q=0.2",
        "cache-control": "no-cache",
        "cookie": "hng=CN%7Czh-cn%7CCNY; _tb_token_=1xuzFAY3hwI9; uss=AC4JH05gjmjUbBBrWNHbTfT3roMRdX689%2BvtZw59oCJINaHd6cSz0Qf2; tracknick=leekona; cookie2=23047a24a0082071f57fa5261e566302; skt=f799b7ab1b3f9cb1; t=1b103ff8ae6035d023fe5d06f72e8651; cna=NZMpEDkX83oCAXJhyNCKzeCE; l=Av//h4DXg9ODcX5xcQBSXvqfD9mJ5FOG; isg=AgUFcMEV8IRsadUlO0N2f5FwFEEI_7lUui1tVAdqwTxLniUQzxLJJJM23nWS",
        "pragma": "no-cache",
        "referer": "https://items.fliggy.com/item.htm?spm=181.7738645.6.5.qDUWvE&id=" + path_id,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
    }
    request = urllib.request.Request(seller_info_url)
    for header in headers:
        request.add_header(header, headers[header])
    response = urllib.request.urlopen(request)
    data = str(response.read().decode(encoding="utf-8"))
    json_data = data[11:len(data) - 1]
    print(json_data)
    return json.loads(json_data)


def list_dst_info(path_id):
    dst_message = {}
    dst_info_url = "https://dsr-rate.tmall.com/list_dsr_info.htm"
    data = {
        "itemId": path_id,
        "spuId": "0",
        "sellerId": "",
        "_ksTS": "",
        "callback": ""
    }
    params = ""
    for key in data:
        params = params + "&" + key + "=" + data[key]

    request = urllib.request.Request(str(dst_info_url + "?" + str(params[1:])))
    response = urllib.request.urlopen(request.get_full_url())
    json_text = response.read().decode("utf8")
    json_text = json_text[5:len(json_text) - 2]
    json_obj = json.loads(json_text)

    dst_message["gradeAvg"] = json_obj["dsr"]["gradeAvg"]
    dst_message["rateTotal"] = json_obj["dsr"]["rateTotal"]
    # print(dst_message)
    return dst_message


# 查询出最高价和最低价
def catch_price(day_item):
    price = []
    for item in day_item:
        day_data = day_item[item]
        for day in day_data:
            min_price = day_data[day]["minPrice"]
            price.append(min_price)
    if len(price) <= 0:
        return {}
    return {"minPrice": min(price), "maxPrice": max(price)}


# 补全详细信息
def process_detail(item_id):
    tarvel_info = detail_travle(item_id)
    if len(tarvel_info) == 0:
        print("初步获取数据有问题")
        return {}
    dst_message = list_dst_info(item_id)
    seller_message = seller_info(item_id)
    # print(seller_message)
    tarvel_info["gradeAvg"] = dst_message["gradeAvg"]
    tarvel_info["rateTotal"] = dst_message["rateTotal"]
    if seller_message["code"] == 200:
        data = seller_message["data"]
        itemPromotionInfos = data["promotionInfos"]["itemPromotionInfos"]
        sell_count = data["sellCount"]["sellCount"]
        tarvel_info["sellCount"] = sell_count
        min_price = 0
        max_price = 0
        if len(itemPromotionInfos) > 0:
            max_price = itemPromotionInfos[0]["maxPrice"]
            min_price = itemPromotionInfos[0]["minPrice"]
        else:
            price_result = catch_price(data["inventory"]["skuCalendarQuantity"])
            if len(price_result) <= 1:
                print("没有找到价格")
                return {}
            max_price = price_result["maxPrice"]
            min_price = price_result["minPrice"]

        tarvel_info["price"] = str(int(min_price / 100)) + "~" + str(int(max_price / 100))
        tarvel_info["minPrice"] = min_price / 100
        tarvel_info["maxPrice"] = max_price / 100


    return tarvel_info

# print(dest_list())
# print(city_travel("捷克", page_size=5))
# print(process_detail("40609001098"))
# result = detail_travle("17522676302")
# result = process_detail("19818037958")
# print(result)
# # print(len(result))
