# -*- coding: utf-8 -*-

from spider.DetailData import DetailSpider
from spider.FlyPigSpider import *
from spider.dboprate import *


# 初步获取数据,首先获取所有目的地城市,然后根据目的地城市获取所有旅游线路,
# 并将这些数据存入数据库
def spider_items():
    dest = insert_dest(dest_list())
    for item in dest:
        insert_city_item(list_travel_city(item["cityName"]), int(item["id"]))


# 生成时间间隔
def generate_period(total):
    return total * 10


# 休眠时间
def wait_time(sleep_time):
    if sleep_time >= 0:
        sleep_time = 5
    while True:
        if sleep_time <= 0:
            return
        print(sleep_time)
        time.sleep(5)
        sleep_time = sleep_time - 5


# 详细信息爬取并入库
def complete_detail_info(items,detail_spider, params):
    for item in items:
        print("开始请求数据--" + item)
        flag = 1
        detail_data = detail_spider.spider(item)
        if len(detail_data) <= 0:
            print("不合格")
            print(detail_data)
            update_city_item(item, "2")
            flag = -1
        else:
            flag = insert_detail_info(item, detail_data)

        if flag < 0:
            params["except_total"] = params["except_total"] + 1
            params["period"] = params["period"] + generate_period(params["except_total"])

        print("下次请求间隔时间: " + str(params["period"]) + "s")
        wait_time(5)
    return params


# 开始
def do_spider(times=5):
    params = {"period": 5, "except_total": 0}
    detail_spider = DetailSpider()
    while times > 0:
        total = query_no_item_count()
        if total > 0:
            items = query_no_item_rand(10)
            print(items)
            params = complete_detail_info(items,detail_spider, params)
        else:
            return
        times = times - 1


# complete_detail_info(["40609001098", "40609001098"],{"period": 5, "except_total": 0})
if __name__ == "__main__":
    do_spider(10000)
