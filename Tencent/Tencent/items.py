# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 名称+地址+类别+时间+职责+要求(提取的最终数据结果)
    job_name = scrapy.Field()
    job_address = scrapy.Field()
    job_type = scrapy.Field()
    job_time = scrapy.Field()
    job_duty = scrapy.Field()
    job_acquire = scrapy.Field()
