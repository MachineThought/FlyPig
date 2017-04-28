# -*- coding: utf-8 -*-

import re
import urllib
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

from spider.writelog import *


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
        "cookie": "hng=CN%7Czh-cn%7CCNY; uc1=cookie15=U%2BGCWk%2F75gdr5Q%3D%3D; tracknick=leekona; _l_g_=Ug%3D%3D; unb=1013953910; cookie1=BdLQ5YYRcp2rWefq8iiYogbfAmc6OkErzXgW0I48r6Y%3D; cookie17=UoH%2B5fRHjXjPUA%3D%3D; cookie2=23047a24a0082071f57fa5261e566302; _nk_=leekona; uss=AC4JH05gjmjUbBBrWNHbTfT3roMRdX689%2BvtZw59oCJINaHd6cSz0Qf2; t=1b103ff8ae6035d023fe5d06f72e8651; skt=68b054678804eec6; _tb_token_=1xuzFAY3hwI9; cna=NZMpEDkX83oCAXJhyNCKzeCE; l=Aqeni31EtzVt2NZpmbhq5nIit9FxLHsO; isg=AujoR5pmJYvh3wjyHmC8TTHoudYrbEwbly7QY6IZNGNW_YhnSiEcq34_gyL3",
        "pragma": "no-cache",
        "referer": "https://place.alitrip.com/beijing?spm=181.62882.251445.1.hG3Hrs",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36"
    }
    data = {
        "id": path_id,
        "spm": "181.7738645.6.5.VS4WSm",
        "smToken": "4ac25e690fab463eb69c48c0ba857f42",
        "smSign": "pqi/ZicA38F6kfaAro75aA=="
    }
    params = ""
    for key in data:
        params = params + "&" + key + "=" + data[key]

    request = urllib.request.Request(str(detail_travle_url + "?" + str(params[1:])))

    wirte_log(request.full_url)
    for key in headers:
        request.add_header(key, headers[key])

    # response = urllib.request.urlopen(request)
    # try:
    #     response = urllib.request.urlopen(request)
    # except:
    #     print("请求详情页出错")
    #     return tarvel_info

    file_object = open('detail.html', 'r', encoding='utf-8')
    detail_page = BeautifulSoup(file_object.read(), "html.parser")
    file_object.close()
    # detail_page = BeautifulSoup(response, "html.parser")

    # print(detail_page)

    shop_name_tag = detail_page.find("a", {"class": "slogo-shopname"})
    h_shopcard_scores = detail_page.select(".h-shopcard-scores a")
    h_shopcard_seller = detail_page.find("div", {"class": "h-shopcard-mid"}).find("dl")
    detail_hd = detail_page.find("div", {"class": "detail-hd"}).find("h1")
    # price = detail_page.find("span", {"class": "detail-price J_PriceWrap"})
    # sell_count = detail_page.find("em", {"class": "ml J_SellCount"})
    # grade = detail_page.find("em", {"class": "J_Grade"})
    # comment = detail_page.find("span", {"class": "J_Comment"})
    other_info = detail_page.select("#J_ItemPropWrap > dd")

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
        tarvel_info["promise"] = tarvel_info["promise"] + " " + promise.text.strip()
    tarvel_info["promise"] = " ".join(tarvel_info["promise"].split("\n")).strip()

    return tarvel_info


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


def sql(detail_data):
    print(type(detail_data["days"]))
    detail_sql = "insert into item_detail(" \
                 "id,item_id,title,shop_name,desc_score,server_score,logistics_score,company," \
                 "location,price,min_price,max_price,sell_count,grade_avg,rate_total,from_city,dest_city,days,promise) " \
                 "values(%d,'%s','%s','%s',%.1f,%.1f,%.1f,'%s','%s','%s',%.2f,%.2f,%d,%.1f,%d,'%s','%s',%d,'%s')" \
                 % (12, "", detail_data["title"], detail_data["shopName"], float(detail_data["descSorce"]),
                    float(detail_data["serverSorce"]), float(detail_data["logisticsScore"]), detail_data["company"],
                    detail_data["location"], detail_data["price"], detail_data["minPrice"], detail_data["maxPrice"],
                    int(detail_data["sellCount"]), detail_data["gradeAvg"], detail_data["rateTotal"], detail_data["fromCity"],
                    detail_data["destCity"], detail_data["days"], detail_data["promise"])
    print(detail_sql)


# result = process_detail("19818037958")
# result = detail_travle("37391626802")
# print(result)
# print(len(result))

data = {'shopName': '武夷山大自然旅行社专营店', 'descSorce': '4.8', 'serverSorce': '4.8', 'logisticsScore': '4.9',
        'title': '北京旅游北京五日游 纯玩无购物无自费4晚5日游 含接送 奢靡五星 ', 'company': '武夷山大自然旅行社有限公司', 'location': '福建省,南平市', 'fromCity': '北京 北京 ',
        'destCity': '北京 北京 ', 'price': '1380', 'minPrice': 1380, 'maxPrice': 1380, 'sellCount': 0, 'gradeAvg': 5.0, 'rateTotal': 4,
        'days': 5,'promise': '纯玩 6个工作小时内确认 全店平均确认时长:2小时 全店确认通过率:91%'}

sql(data)
