# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
import time
import hashlib
import json

from shenpeitu.items import ShenpeituItem, ShenpeituDownloadImgItem


class WeshineSpider(scrapy.Spider):
    name = 'weshine_down_gifs'
    allowed_domains = ['weshineapp.com']
    start_urls = ['http://weshineapp.com/']
    headers = {
        "Referer":"https://servicewechat.com/wx73b5c9319faa223d/123/page-frame.html",
        "User-Agent":"Mozilla/5.0 (Linux; Android 5.1; MX4 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.127 Mobile Safari/537.36"
    }
    def get_timestamp(self):
        return int(time.time())

    def get_sign(self,timestamp):
        encoding_str = "weshine@2016#Y2MyZTlmYmUxMWY5MjJkODE1ODE4NzgzNDNmZWI3NDM=#%s"%timestamp
        md5_obj = hashlib.md5()
        md5_obj.update(encoding_str.encode("utf-8"))
        return md5_obj.hexdigest()


    def get_img_url(self,gif_id):
        timestamp = self.get_timestamp()
        return "https://mp.weshineapp.com/2.0/detail?timestamp={}&sign={}&h=b2280b45-8dd2-472d-a334-afb89658d30b&id={}&v=3.6.26".format(timestamp,self.get_sign(timestamp),gif_id)

    def get_img_name(self,url, guid):
        rs = url.split(".")
        extension = rs[-1].split("?")[0]
        name = guid + "." + extension
        # print(name)
        return name

    def start_requests(self):
        with open("weshine_guid_big_url.txt","r",encoding="utf-8") as f:
            count = 0
            while True:
                item = f.readline().strip()
                if len(item)==0:
                    break
                # print(self.get_tag_url())
                count +=1
                if count>=134000:
                    items = item.split(" ")
                    guid = items[0]
                    url = items[1]

                    file_name = self.get_img_name(url,guid)
                    meta = {"name":file_name,"count":count}
                    yield scrapy.Request(method="GET",callback=self.parse_img,url=url,headers=self.headers,meta=meta)


    def parse_img(self,response):
        print("img_parse执行了")
        meta = response.meta
        item = ShenpeituDownloadImgItem()
        # item["tag"] = meta.get("tag")
        item["name"] = meta["name"]
        item["img_data"]=response.body
        item["count"]=meta["count"]
        yield item
