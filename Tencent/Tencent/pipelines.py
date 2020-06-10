# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class TencentPipeline(object):
    def process_item(self, item, spider):
        return item


# 管道2,存入MySQL
import pymysql
from .settings import *


class TencentMysqlPipeline:
    def open_spider(self, spider):
        # 连接mysql数据库
        self.db = pymysql.connect(host=MYSQL_HOST,
                                  port=MYSQL_PORT,
                                  user=MYSQL_USER,
                                  password=MYSQL_PASSWORD,
                                  database=MYSQL_DB,
                                  charset=MYSQL_CHARSET, )
        self.cur = self.db.cursor()

    def process_item(self, item, spider):
        item_list = [item['job_name'], item['job_type'], item['job_duty'], item['job_acquire'], item['job_address'],
                     item['job_time']]
        ins = 'insert into tencenttab values(%s,%s,%s,%s,%s,%s)'
        self.cur.execute(ins, item_list)
        self.db.commit()
        return item

    def close_spider(self, spider):
        # 关闭MySQL数据库
        self.cur.close()
        self.db.close()
