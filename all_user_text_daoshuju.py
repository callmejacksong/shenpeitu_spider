import uuid

import time

import unicodedata

from mysql_db import DB
from config import *
from multiprocessing import pool

# mysql_conn_product = DB(host=ProductConfig.MYSQL_HOST,port=ProductConfig.MYSQL_PORT,user=ProductConfig.MYSQL_USER,password=ProductConfig.MYSQL_PASSWORD,db=ProductConfig.MYSQL_DB)


def get_uuid():
    tem_str = str(uuid.uuid1())
    uuid_str = "".join(tem_str.split("-"))
    return uuid_str

def handle_error(word):
    with open("./baidu_err.txt","a",encoding="utf-8") as f:
        f.write("%s   没有插入成功\n"%word)

def task(sql):
    mysql_conn_test = DB(host=TestConfig.MYSQL_HOST, port=TestConfig.MYSQL_PORT, user=TestConfig.MYSQL_USER,
                         password=TestConfig.MYSQL_PASSWORD, db=TestConfig.MYSQL_DB)
    cursor = mysql_conn_test.get_cursor()
    # sql = "insert into all_keywords(guid,text,sfrom) VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE text=%s"
    print(sql)
    # ret = cursor.execute(sql, (get_uuid(), word, "tecent开源词库", word))
    ret = cursor.execute(sql)
    mysql_conn_test.commit()
    # if ret == 0:
        # handle_error(word)



def daodata():
    p = pool.Pool(10)
    # 读取文本文件  all_user_text
    for i in range(5,8):
        print("执行到result_keyword_net_spider_%s.txt"%i)
        with open("./result_keyword_net_spider_%s.txt"%i,"r",encoding="utf-8",errors="ignore") as f:
            count = 0
            sql = ""
            while True:
                item = f.readline()
                if len(item)==0:
                    break
                word_list = item.split("-song-")
                text = word_list[0].strip()
                tag = word_list[1].strip()
                gif_id = word_list[2].strip()
                big_url = word_list[3].strip()
                width = word_list[4]
                height = word_list[5]
                small_url = word_list[6].strip()
                mp4_url = word_list[7].strip()
                has_text = word_list[8]
                text_guid = word_list[9].strip()
                text = "".join(text.split("\'"))
                text = "".join(text.split("\""))

                pic_text = text if int(has_text)==1 else ""

                count += 1
                # cursor.execute(sql,(item["big_url"],item["gif_id"],item["small_url"],item["width"],item["height"],item["has_text"],pic_text,item["tag"],item["mp4_url"],item["text_guid"],item["text"],item["gif_id"],item["text"],item["tag"]))

                sql += "insert ignore into `weshine_gif`(big_url,gif_id,small_url,width,height,has_text,text,tag,mp4_url) values('%s','%s','%s',%s,%s,%s,'%s','%s','%s');"%(big_url,gif_id,small_url,width,height,has_text,pic_text,tag,mp4_url)
                sql += "insert ignore into `weshine_keyword`(guid,text) values('%s','%s');"%(text_guid,text)
                sql += "insert ignore into `weshine_keyword_gif`(gif_id,keyword,tag) values('%s','%s','%s');"%(gif_id,text,tag)

                if count %500 == 0:
                    # print(sql)
                    p.apply_async(task, args=(sql,))
                    sql = ""
            print("全部完成")
            p.close()
            p.join()
            print("全部完成.....")






if __name__ == '__main__':

    daodata()