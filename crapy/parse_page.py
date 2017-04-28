# -*- encoding=utf-8 -*-
from bs4 import BeautifulSoup


# 本类用于解析html格式的文本并返回相应的数据
class ParseHtml:
    def __init__(self):
        self.parse_type = "html.parser"
        self.parse_data = {}

    # 读取指定的文件并返回内容
    def read_file(self, filename):
        page = ""
        with open(filename, "r", encoding="utf-8") as page_file:
            page = page_file.read()
        page_file.close()
        return page

    # 解析html页面
    def parse_page(self, page):
        bs_page = BeautifulSoup(page, self.parse_type)
        try:
            self.parse_shop(bs_page)
        except Exception as err:
            print("解析商店信息出错：%s " % err)
            return {"message": "error"}
        try:
            self.parse_sell(bs_page)
        except Exception as err:
            print("解析销售信息出错：%s " % err)
            return {"message": "error"}
        try:
            self.parse_prop(bs_page)
        except Exception as err:
            print("解析商品信息出错：%s " % err)
            return {"message": "error"}
        print(self.parse_data)
        return self.parse_data

    # 解析店铺信息
    def parse_shop(self, bs_page):
        shop_data = {}
        info = []
        shop_info = bs_page.select("#J_HShopInfo")
        if len(shop_info) == 0:
            print("无商店信息")
            return
        sorces = bs_page.select(".h-shopcard-scores a")
        self.parse_data["descSorce"] = float(str(sorces[0].text).strip())
        self.parse_data["serverSorce"] = float(str(sorces[1].text).strip())
        self.parse_data["logisticsScore"] = float(str(sorces[2].text).strip())

        company_info = bs_page.select(".h-shopcard-seller > dd")
        for company in company_info:
            temp = str(company.text).strip().split("：")[1]
            if temp != "":
                info.append(temp)
        self.parse_data["shopName"] = info[0]
        self.parse_data["company"] = info[1]
        self.parse_data["location"] = info[2]

    # 解析销售信息
    def parse_sell(self, bs_page):
        sell_data = {"sellCount": 0, "grade": 0.0, "comment": 0, "mboth": 0}
        if len(bs_page.select("#J_SellCountLink")) == 0:
            print("未找到销售信息，该产品无销售记录或已经下架")
            return
        sell_count = bs_page.find("em", {"class": "ml J_SellCount"}).text
        grade = bs_page.find("em", {"class": "J_Grade"}).text
        comment = bs_page.find("span", {"class": "J_Comment"}).text
        # 校验销量
        if sell_count == "":
            self.parse_data["sellCount"] = 0
        else:
            self.parse_data["sellCount"] = int(sell_count)
        # 校验评分
        if grade == "--":
            self.parse_data["grade"] = 0
        else:
            self.parse_data["grade"] = float(grade)
        # 校验评论
        if comment == "":
            self.parse_data["comment"] = 0
        else:
            self.parse_data["comment"] = int(comment)

    # 解析出发地,目的地,天数等数据
    def parse_prop(self, bs_page):
        if len(bs_page.select("#J_ItemPropWrap")) == 0:
            print("未找到商品信息，该产品无商品信息或已经下架")
            return
        item_prop_dt = bs_page.select("#J_ItemPropWrap > dt")
        item_prop_dd = bs_page.select("#J_ItemPropWrap > dd")
        prop = {}
        if len(item_prop_dt) != len(item_prop_dd):
            print("数据不匹配")
        index = 0
        while index < len(item_prop_dt):
            dt = item_prop_dt[index]
            dd = item_prop_dd[index]
            # 选取 dt,dd下的span
            dt_span = dt.select("span")
            dd_span = dd.select("span")
            key = ""
            value = ""
            # span的长度可能为0，也可能大于0
            # 如果为0则直接取值，否则循环取span下的值
            if len(dt_span) == 0:
                key = str(dt.text).strip()
            else:
                for item in dt_span:
                    key += str(item.text).strip()
            if len(dd_span) == 0:
                value = str(dd.text).strip()
            else:
                for item in dd_span:
                    # 每次在追加数据之前,使用空格进行占位区别
                    value += " "
                    text = str(item.text).strip()
                    # 因为此循环中包含重复的和不规范的数据,所以需要做相应的处理
                    if text.find("\n") > 0:
                        value += text[0:text.find("\n")]
                    elif text.find(" ") > 0:
                        value += text[0:text.find(" ")]
                    else:
                        value += text
            prop[key.strip()] = value.strip()
            index += 1
        self.field_asign(prop)

    # 解析出来的商品信息不一定每个都有,所以只选择有的字段进行赋值
    def field_asign(self, prop):
        prop_data = {"fromCity": "", "destCity": "", "days": "", "proInclude": "", "promise": ""}
        for item in prop:
            if item == "出发地":
                prop_data["fromCity"] = prop[item]
            elif item == "目的地":
                prop_data["destCity"] = prop[item]
            elif item == "行程天数":
                prop_data["days"] = prop[item]
            elif item == "商品包含":
                prop_data["proInclude"] = prop[item]
            elif item == "服务承诺":
                prop_data["promise"] = prop[item]
        # 以上的信息不一定每个都有，所以为了安全做以下操作
        for data in prop_data:
            self.parse_data[data] = prop_data[data]

    # 执行主程序
    def main(self, filename):
       return self.parse_page(self.read_file(filename))


if __name__ == "__main__":
    parser = ParseHtml()
    parser.main("promise_long.html")
