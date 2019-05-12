# -*- coding: utf-8 -*-
import csv
import json
import re
import sys
from lxml import etree

reload(sys)
sys.setdefaultencoding("utf-8")

import requests
from jsonpath import jsonpath


class Taobao_spider(object):
    def __init__(self):
        self.headers1 = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.headers = {
            "cookie": "thw=cn; t=3982a34c6cf3c41d9613ee6a8973f266; cna=9uFQFEFMGE4CAXBgwPd0byjy; tracknick=%5Cu7B49%5Cu5F85%5Cu7199%5Cu671B; lgc=%5Cu7B49%5Cu5F85%5Cu7199%5Cu671B; _cc_=UtASsssmfA%3D%3D; tg=0; enc=EdcI9trLOacWkVGYktJgKdP6PdoZmKObXl1ridzEDlM54dt16z%2B8atSCGbPWUZPlYuCSfbGXcDn2tiUbexu5Hw%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; _m_h5_tk=06ce77a23e4343aa13de11fa4c4b897e_1540382790378; _m_h5_tk_enc=aca3f12fbd0397e2b9e5e691b26d8840; _uab_collina=154037776337314922100364; _umdata=ED82BDCEC1AA6EB9EC3224F1B26662F8B9C7F997A513924BB75B8FE7816FF34789B143CB49C1C8F4CD43AD3E795C914CA2FDD446926A7E5481CE31A0C86F4354; mt=ci=9_1&np=; cookie2=1aa4e711ed3af32ee3c11f40c68bf496; _tb_token_=eeeef3ee38d68; v=0; swfstore=217233; unb=1714211597; sg=%E6%9C%9B75; _l_g_=Ug%3D%3D; skt=1298126900e60755; cookie1=Vy%2FMWFwS7ChQa7nSNK3u3Q%2Fk43mBxq5IOm7b02z0SCA%3D; csg=43cf280e; uc3=vt3=F8dByRjJN82GC9i5E30%3D&id2=UoYfparsUTHRWw%3D%3D&nk2=1oenv%2F8EXSw%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; existShop=MTU0MDY1NTIzOA%3D%3D; dnk=%5Cu7B49%5Cu5F85%5Cu7199%5Cu671B; _nk_=%5Cu7B49%5Cu5F85%5Cu7199%5Cu671B; cookie17=UoYfparsUTHRWw%3D%3D; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; uc1=cookie14=UoTYNkHV4o4xcg%3D%3D&lng=zh_CN&cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&existShop=false&cookie21=VFC%2FuZ9aiKCaj7AzMHh1&tag=8&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&pas=0; JSESSIONID=424EA1EC2E358EC43681525B541D0ED4; isg=BHBwqn2E36erZ4OnLQ4FhuagQT4CEX-7Oeals2rDwUmNJRHPEsgTky9XeW3gtQzb; whl=-1%260%260%261540656623248",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"
        }
        self.base_url = "https://s.taobao.com/search?"
        self.page = 1
        self.good = raw_input("请输入要爬取的商品：")
        self.filter_tianmao = "tmall"
        self.item_list = []
        self.item = {}
        self.base_rateurl = "https://dsr-rate.tmall.com/list_dsr_info.htm?itemId="


    def send_request(self,query_dict):
        html = requests.get(self.base_url,params=query_dict,headers=self.headers).content
        print("列表页的长度是{}".format(len(html)))
        return html

    def parse_page(self,html):
        pattern = re.findall(r"g_page_config = (.*);",html)[0]
        python_obj = json.loads(pattern)
        goods_list = jsonpath(python_obj,"$..auctions")[0]
        print("商品列表信息是{}".format(goods_list))
        for goods in goods_list:
            self.item["view_sales"] = goods["view_sales"].encode("utf-8")
            self.item["nid"] = goods["nid"].encode("utf-8")
            self.item["raw_title"] = goods["raw_title"].encode("utf-8")
            # item["detail_url"] = "https:" + goods["detail_url"].encode("utf-8")
            detail_url = goods["detail_url"].encode("utf-8")
            if detail_url.startswith("https"):
                self.item["detail_url"] = detail_url
            else:
                self.item["detail_url"] = "https:" + detail_url
            self.item["view_price"] = goods["view_price"].encode("utf-8")
            self.item["item_loc"] = goods["item_loc"].encode("utf-8")
            self.item["nick"] = goods["nick"].encode("utf-8")
            # item["shopLink"] = "https:" + goods["shopLink"].encode("utf-8")
            shopLink = goods["shopLink"].encode("utf-8")
            if shopLink.startswith("https:"):
                self.item["shopLink"] = shopLink
            else:
                self.item["shopLink"] = "https:" + shopLink
            detail_url1 = self.item["detail_url"]
            try:
                self.parse_detail(detail_url1)
            except Exception as e:
                print("访问详情页失败{}".format(e))
            self.item_list.append(self.item)
        self.save_info(self.item_list)



    def parse_detail(self,detail_url1):
        html1 = requests.get(detail_url1,headers=self.headers1).content
        print("详情页的长度是{}".format(len(html1)))
        pattern = re.search(r'{"valItemInfo"(.*)',html1).group().decode("gbk")
        python_obj = json.loads(pattern)
        goods1 = jsonpath(python_obj,"$..skuList")[0]
        item_list1 = []
        for good1 in goods1:
            item1 = {}
            item1["names"] = good1["names"]
            item1["skuId"] = eval(json.dumps(good1["skuId"]))
            item_list1.append(item1)

        goods = jsonpath(python_obj,"$..skuMap")[0]
        goods2 = goods.values()
        item_list2 = []
        for good2 in goods2:
            item2 = {}
            item2["skuId"] = eval(json.dumps(good2["skuId"]))
            item2["price"] = eval(json.dumps(good2["price"]))
            item2["stock"] = eval(json.dumps(good2["stock"]))
            item_list2.append(item2)

        s = ""
        for i1 in item_list1:
            for i2 in item_list2:
                if i1["skuId"] == i2["skuId"]:
                    i1.update(i2)
                    # print("此时的i1为{}".format(i1))
                    for k in i1.values():
                        s = s + str(k) + ","
        self.item["type_money"] = s

        pictures = jsonpath(python_obj,"$..propertyPics")[0]
        item_list4 = []
        pics2 = pictures.values()
        for p in pics2:
            if len(p) > 1:
                for i in p:
                    item_list4.append(eval(json.dumps('https:' + i)))
            else:
                item_list4.append(eval(json.dumps('https:' + p[0])))
        self.item["pictures"] = item_list4
        score = self.parse_score(html1)
        self.item["score"] = score
        nid = self.item["nid"]
        rateurl = self.base_rateurl + str(nid)
        rate_number = self.get_rate(rateurl)
        self.item["rate_number"] = rate_number

    def get_rate(self,rateurl):
        html2 = requests.get(rateurl,headers=self.headers1).content
        print("评价数量的内容是{}".format(html2))
        rate_number = re.findall(r'"rateTotal":([0-9]+)',html2)[0]
        return rate_number



    def parse_score(self,html1):
        html_obj = etree.HTML(html1)
        score = html_obj.xpath("//div[@id='shop-info']//span[@class='shopdsr-score-con']/text()")
        return score


    def save_info(self,item_list):
        print("正在保存第{}页数据".format(self.page))
        with open("taobao7.csv","a") as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=['raw_title','detail_url','view_price','view_sales','item_loc','nick','shopLink','score','rate_number','type_money','pictures'])
            # 写入列标题，即DictWriter构造方法的fieldnames参数
            writer.writeheader()
            for data in item_list:
                writer.writerow({'raw_title':data['raw_title'],'detail_url':data['detail_url'],'view_price':data['view_price'],'view_sales':data['view_sales'],'item_loc':data['item_loc'],'nick':data['nick'],'shopLink':data['shopLink'],'score':data['score'],'rate_number':data['rate_number'],'type_money':data['type_money'],'pictures':data['pictures']})

    def main(self):
        while self.page <= 100:
            s = (self.page - 1) * 44
            q = self.good
            filter = self.filter_tianmao
            query_dict = {"s":s,"q":q,"filter":filter}
            html = self.send_request(query_dict)
            self.parse_page(html)
            self.page += 1


if __name__ == '__main__':
    spider = Taobao_spider()
    spider.main()