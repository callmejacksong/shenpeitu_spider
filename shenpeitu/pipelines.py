# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import uuid
import pymysql
import json


class DB(object):

    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    def get_con(self):
        self.conn = pymysql.connect(charset="utf8",host=self.host,port=self.port,user=self.user,password=self.password, database=self.db)

    def get_cursor(self):
        try:
            self.conn.ping()
            print("ping ok")
        except:
            self.get_con()
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.conn.cursor().close()
        self.conn.close()
        print("mysql数据库连接已关闭")
        return True

class TestConfig(object):
    # mysql数据库配置
    MYSQL_HOST = "rm-bp1664spovq6woabo.mysql.rds.aliyuncs.com"
    MYSQL_PORT = 3306
    MYSQL_USER = "bqss"
    MYSQL_PASSWORD = "665Fbt7Nxkcj"
    MYSQL_DB = "net_pic"


class ProductConfig(object):
    MYSQL_PORT = 3306
    MYSQL_HOST="rm-bp15gczz2b6835281.mysql.rds.aliyuncs.com"
    MYSQL_DB="net_pic"
    MYSQL_USER="bqss"
    MYSQL_PASSWORD="665Fbt7Nxkcj"




class ShenpeituPipeline(object):


    def open_spider(self,spider):
        print("开始蜘蛛执行了")
        self.f = open("result_keyword_net_spider.txt","a",encoding="utf-8",newline="\n")
        self.mysql_con =DB(host=TestConfig.MYSQL_HOST, port=TestConfig.MYSQL_PORT, user=TestConfig.MYSQL_USER,
                         password=TestConfig.MYSQL_PASSWORD, db=TestConfig.MYSQL_DB)

    
    def close_spider(self,spider):
        self.f.close()
        self.mysql_con.close()
        print("结束蜘蛛执行了")

    def get_guid(self):
        return "".join(str(uuid.uuid1()).split("-"))
    
    def process_item(self, item, spider):
        # content = json.dumps(dict(item))
        content = "%s-song-%s-song-%s-song-%s-song-%s-song-%s-song-%s-song-%s-song-%s-song-%s"%(item["text"],item["tag"],item["gif_id"],item["big_url"],item["width"],item["height"],item["big_url"],item["mp4_url"],item["has_text"],item["text_guid"])
        self.f.write(content+"\n")
        pic_text = item["text"] if int(item["has_text"])==1 else ""
        sql = "insert ignore into `weshine_gif`(big_url,gif_id,small_url,width,height,has_text,text,tag,mp4_url) values('%s','%s','%s',%s,%s,%s,'%s','%s','%s');"%(item["big_url"],item["gif_id"],item["small_url"],item["width"],item["height"],item["has_text"],pic_text,item["tag"],item["mp4_url"])
        sql += "insert ignore into `weshine_keyword`(guid,text) values('%s','%s');"%(item["text_guid"],item["text"])
        sql += "insert ignore into `weshine_keyword_gif`(gif_id,keyword,tag) values('%s','%s','%s');"%(item["gif_id"],item["text"],item["tag"])
        cursor = self.mysql_con.get_cursor()
        cursor.execute(sql)
        self.mysql_con.commit()

        return item

class ShenpeituDownloadPicPipeline(object):

    def process_item(self, item, spider):
        # content = json.dumps(dict(item))
        with open("./weshine_imgs/%s"%item["name"],"wb") as f:
            f.write(item["img_data"])
            print("执行到%s"%item["count"])
        return item

