# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShenpeituItem(scrapy.Item):
    # define the fields for your item here like:
    small_url = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    mp4_url = scrapy.Field()
    gif_id = scrapy.Field()
    big_url = scrapy.Field()
    has_text = scrapy.Field()
    text = scrapy.Field()
    tag = scrapy.Field()
    text_guid=scrapy.Field()
    count=scrapy.Field()


class ShenpeituDownloadImgItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    img_data = scrapy.Field()
    count = scrapy.Field()
