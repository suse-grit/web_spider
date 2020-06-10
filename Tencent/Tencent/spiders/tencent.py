# -*- coding: utf-8 -*-
import json

import scrapy
import requests
from urllib import parse
from ..items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    # 某个职位类别下的第一页的URL地址
    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1591756517849&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1591756342214&postId={}&language=zh-cn'
    keyword = parse.quote(input('请输入职位类别：'))
    start_urls = [one_url.format(keyword, 1)]  # start_urls中的地址不会去重

    def get_total(self):
        # 获取某个职位的总页数
        url = self.one_url.format(self.keyword, 1)
        headers = {'User-Agent': ''}
        html = requests.get(url=url, headers=headers).json()
        count = html['Data']['Count']
        total = count // 10 if count % 10 == 0 else count // 10 + 1
        return total

    def parse(self, response):
        # 一次性把所有页的请求交给调度器入队列
        total = self.get_total()
        for index in range(1, total + 1):
            url = self.one_url.format(self.keyword, index)
            yield scrapy.Request(
                url=url,
                callback=self.parse_one_page,
                dont_filter=True)  # 是否让此地址参与去重

    def parse_one_page(self, response):
        # 提取一级页面的ID,进行URL拼接
        html = json.loads(response.text)
        for one_job in html['Data']['Posts']:
            post_id = one_job['PostId']
            # 拼接详情页的链接
            two_url = self.two_url.format(post_id)
            yield scrapy.Request(url=two_url, callback=self.parse_two_page)

    def parse_two_page(self, response):
        html = json.loads(response.text)
        item = TencentItem()
        item['job_name'] = html['Data']['RecruitPostName']
        item['job_address'] = html['Data']['LocationName']
        item['job_type'] = html['Data']['CategoryName']
        item['job_time'] = html['Data']['LastUpdateTime']
        item['job_duty'] = html['Data']['Responsibility']
        item['job_acquire'] = html['Data']['Requirement']
        yield item
