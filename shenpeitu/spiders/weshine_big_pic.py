# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
import time
import hashlib
import json

from shenpeitu.items import ShenpeituItem


class WeshineSpider(scrapy.Spider):
    name = 'weshine_gif_id'
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

    def start_requests(self):
        with open("weshine_gif_id.txt","r",encoding="utf-8") as f:
            while True:
                gif_id = f.readline().strip()
                if len(gif_id)==0:
                    break
                # print(self.get_tag_url())
                yield scrapy.FormRequest(method="POST",callback=self.parse_img,url=self.get_img_url(gif_id),headers=self.headers)


    def parse_img(self,response):
        print("img_parse执行了")
        ret = json.loads(response.text)
        print("原始data",response.text)
        ret_dict = ret.get("data")
        item = ShenpeituItem()
        # item["tag"] = meta.get("tag")
        item["gif_id"] = ret_dict.get("id")
        item["width"] = ret_dict.get("image").get("w")
        item["height"] = ret_dict.get("image").get("h")
        url = ret_dict.get("image").get("ori")
        item["url"]="".join(url.split("thumb_"))
        item["mp4_url"] = ret_dict.get("image").get("mp4")
        yield item
