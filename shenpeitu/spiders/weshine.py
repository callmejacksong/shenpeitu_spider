# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
import time
import hashlib
import json

from shenpeitu.items import ShenpeituItem


class WeshineSpider(scrapy.Spider):
    name = 'weshine'
    allowed_domains = ['weshineapp.com']
    start_urls = ['http://weshineapp.com/']
    h = "b2280b45-8dd2-472d-a334-afb89658d30b"
    v = "3.6.26"
    headers = {
        "Referer":"https://servicewechat.com/wx73b5c9319faa223d/123/page-frame.html",
        "User-Agent":"Mozilla/5.0 (Linux; Android 5.1; MX4 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.127 Mobile Safari/537.36"
    }
    tag_url = "https://mp.weshineapp.com/2.0/text2img/actionlist"
    img_url = "https://mp.weshineapp.com/2.0/text2img/imglist"

    def get_timestamp(self):
        return int(time.time())

    def get_sign(self,timestamp):
        encoding_str = "weshine@2016#Y2MyZTlmYmUxMWY5MjJkODE1ODE4NzgzNDNmZWI3NDM=#%s"%timestamp
        md5_obj = hashlib.md5()
        md5_obj.update(encoding_str.encode("utf-8"))
        return md5_obj.hexdigest()

    def get_tag_url(self):
        timestamp = self.get_timestamp()
        return "https://mp.weshineapp.com/2.0/text2img/actionlist?timestamp={}&sign={}&h=b2280b45-8dd2-472d-a334-afb89658d30b&v=3.6.26".format(timestamp,self.get_sign(timestamp))

    def get_img_url(self):
        timestamp = self.get_timestamp()
        return "https://mp.weshineapp.com/2.0/text2img/imglist?timestamp={}&sign={}&h=b2280b45-8dd2-472d-a334-afb89658d30b&v=3.6.26".format(timestamp,self.get_sign(timestamp))

    def get_big_img_url(self,gif_id):
        timestamp = self.get_timestamp()
        return "https://mp.weshineapp.com/2.0/detail?timestamp={}&sign={}&h=b2280b45-8dd2-472d-a334-afb89658d30b&id={}&v=3.6.26".format(timestamp,self.get_sign(timestamp),gif_id)

    def start_requests(self):
        with open("keyword_net.txt","r",encoding="utf-8") as f:
            count = 0
            while True:
                count+=1
                content = f.readline().strip()
                if len(content)==0:
                    break
                if count>120000:
                    content_list = content.split(" || ")
                    if len(content_list)>=2:
                        text = content_list[1].strip()
                        text_guid = content_list[0].strip()
                        # text = "".join(text.split("\'"))
                        # text = "".join(text.split("""\""""))

                        meta = {"text":text,"text_guid":text_guid}
                        print(text)
                        # print(self.get_tag_url())
                        # print(meta)
                        yield scrapy.FormRequest(method="POST",callback=self.parse_tag,url=self.get_tag_url(),meta=meta,formdata={"text":text},headers=self.headers)

    def parse_tag(self,response):
        # print("parse执行了")
        # print(response.meta)
        # print(response.text)
        # print(type(response.text))
        # print(json.loads(response.text))
        # print(type(json.loads(response.text)))
        tags = json.loads(response.text)
        meta = response.meta
        text = meta["text"]


        tags = tags.get("data")
        tag = ",".join(tags)
        meta["tag"]=tag
        yield scrapy.FormRequest(method="POST", callback=self.parse_img, url=self.get_img_url(), meta=meta,
                                 formdata={"text": text}, headers=self.headers)

    def parse_img(self,response):
        # print("img_parse执行了")
        meta = response.meta
        ret = json.loads(response.text)
        rets = ret.get("data")


        for img in rets:

            meta["small_url"] = img.get("img_path")
            meta["has_text"] = img.get("wordsinpic")
            gif_id=img.get("gif_id")
            meta["gif_id"] = gif_id
            yield scrapy.FormRequest(method="POST", callback=self.parse_big_img, url=self.get_big_img_url(gif_id), meta=meta, headers=self.headers)

    def parse_big_img(self,response):
        print("big_img_parse执行了")
        meta = response.meta
        ret = json.loads(response.text)
        ret_dict = ret.get("data")
        big_url=ret_dict.get("image").get("ori")

        big_url="".join(big_url.split("thumb_"))
        mp4_url = ret_dict.get("image").get("mp4")
        width = ret_dict.get("image").get("w")
        height = ret_dict.get("image").get("h")

        item = ShenpeituItem()
        item["gif_id"] = meta["gif_id"]
        item["width"] = width
        item["height"] = height
        item["small_url"] = meta["small_url"]
        item["has_text"] = meta["has_text"]
        item["text"] = meta["text"]
        item["tag"] = meta["tag"]
        item["big_url"] = big_url
        item["mp4_url"] = mp4_url
        item["text_guid"] = meta["text_guid"]
        yield item

