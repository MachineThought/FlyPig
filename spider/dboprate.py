# -*- coding: utf-8 -*-

import pymysql

# from spider.writelog import *

# 获取数据库连接
db = pymysql.connect(host="192.168.1.11", port=3306, user="root", passwd="root", db="fly_pig")
# 设置字符编码,解决可能出现的字符问题
db.set_charset("utf8")
# 获取数据库游标
cursor = db.cursor()
# 设置数据库连接字符编码
cursor.execute('SET character_set_connection=utf8;')


# 执行sql,包含事务
def excute_sql(sql):
    try:
        cursor.execute(sql)
        db.commit()
        return 1
    except:
        print("執行SQL失败:\n\t" + sql)
        db.rollback()
        return -1


# 获取当前数据库中指定 column 值最大的数
def get_bigger_column(table_name, column):
    max_index = 0
    sql = "select max(%s) from %s" % (column, table_name)
    try:
        cursor.execute(sql)
        for row in cursor.fetchall():
            max_index = row[0]

        if max_index is None:
            max_index = 1
        else:
            max_index = max_index + 1
    except:
        print("查询最大数出错")

    return max_index


# 获取当前表中最大的id并返回 +1 后的值
def get_bigger_id(table_name):
    return get_bigger_column(table_name, "id")


# 添加所有目的地城市
def insert_dest(dest_data):
    result = []
    index = 1
    for city in dest_data:
        sql = "insert into travel_destination(id,request_url,city_name) values(%d,'%s','%s')" % (index, city["href"], city["cityName"])
        flag = excute_sql(sql)
        if flag > 0:
            result.append({"id": str(index), "cityName": city["cityName"]})
            index = index + 1
    return result


# 添加旅游路线记录,根据每个城市的线路进行添加
def insert_city_item(city_item, city_id):
    success = 0
    unsuccess = 0
    for item in city_item:
        max_index = get_bigger_id("city_item")

        sql = "insert into city_item(id,city_id,item_id,title,seller_nick,wangwang,travel_type,from_city,dest_city,is_success) values " \
              "(%d,%d,'%s','%s','%s','%s','%s','%s','%s','0')" % (
                  max_index, city_id, item["itemId"], item["title"], item["sellerNick"], item["wangwang"],
                  item["travelType"], item["fromCity"], item["destCity"])
        flag = excute_sql(sql)
        if flag > 0:
            success = success + 1
        else:
            unsuccess = unsuccess + 1

        print("线路 " + city_item + " " + city_id + " 添加成功,成功:" + success + "  失败:" + unsuccess)


# 查询未完成的中数目
def query_no_item_count():
    count = 0
    count_sql = "select count(1) from city_item where is_success='0'"
    try:
        cursor.execute(count_sql)
        for row in cursor.fetchall():
            count = row[0]
    except Exception as err:
        print(err)
        print("查询总数失败")
    return count


# 获取尚未查询到具体信息的旅游路线
def query_no_item(sql, limit=10):
    items = []
    query_sql = sql + "limit " + str(limit)
    try:
        cursor.execute(query_sql)
        for row in cursor.fetchall():
            items.append(row[0])
        return items
    except Exception as err:
        print(err)
        print("查询未完成记录出错")
        return items


# 正常获取
def query_no_item_normal(limit=10):
    query_sql = "select item_id from city_item where is_success='0'"
    return query_no_item(query_sql, limit)


# 随机获取
def query_no_item_rand(limit=10):
    query_sql = "select item_id from city_item where is_success='0' ORDER BY RAND()"
    return query_no_item(query_sql, limit)


# 更新旅游路线记录,用于表示当前路线已经获得详细记录
def update_city_item(city_item_id, value="1"):
    sql = "update city_item set is_success='%s' where item_id='%s' " % (value, city_item_id)
    return excute_sql(sql)


# 插入详细信息
def insert_detail_info(item_id, detail_data):
    if detail_data["sellCount"] == "":
        detail_data["sellCount"] = "0"

    # print(detail_data)
    max_index = get_bigger_id("item_detail")
    detail_sql = "insert into item_detail(" \
                 "id,item_id,title,shop_name,desc_score,server_score,logistics_score,company," \
                 "location,price,min_price,max_price,sell_count,grade_avg,rate_total,from_city,dest_city,days,promise) " \
                 "values(%d,'%s','%s','%s',%.1f,%.1f,%.1f,'%s','%s','%s',%.2f,%.2f,%d,%.1f,%d,'%s','%s',%d,'%s')" \
                 % (max_index, item_id, detail_data["title"], detail_data["shopName"], float(detail_data["descSorce"]),
                    float(detail_data["serverSorce"]), float(detail_data["logisticsScore"]), detail_data["company"],
                    detail_data["location"], detail_data["price"], detail_data["minPrice"], detail_data["maxPrice"],
                    int(detail_data["sellCount"]), detail_data["gradeAvg"],detail_data["rateTotal"], detail_data["fromCity"],
                    detail_data["destCity"], int(detail_data["days"]),detail_data["promise"])
    flag = excute_sql(detail_sql)
    if flag > 0:
        update_city_item(item_id)
    return flag


def complete_detail_info(city_item_id):
    print("")

#
# detail = {'shopName': '金度旅游专营店', 'descSorce': '4.9', 'serverSorce': '4.9', 'logisticsScore': '4.9', 'company': '北京金牌国际旅行社有限公司',
#           'location': '北京', 'title': '飞猪专线 北京旅游5天4晚跟团游 北京五日游 亲子纯玩 5日旅游团', 'price': '', 'sellCount': '', 'gradeAvg': 4.9,
#           'rateTotal': 914, 'fromCity': '北京', 'destCity': '北京', 'days': '5', 'promise': '纯玩 即时确认'}

# insert_city_item(item_data, 55)
# print(update_city_item("40609001098"))
# print(get_bigger_id("city_item"))
# insert_detail_info("40609001098", detail)
# print(query_no_item())
# print(query_no_item_count())
