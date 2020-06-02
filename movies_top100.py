# 猫眼电影网TOP100榜电影信息获取
# 名称
# 主演
# 上映时间
import requests
import re
import time
import random
import pymysql


class MaoYanSpider:
    # 请求数据--> 解析响应数据-->得到目标数据-->数据入库（MySQL）
    def __init__(self):
        # 定义常用变量
        self.regex = r'<div class="movie-item-info">.*?title="(.*?)".*?' \
                     r'<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>'  # 数据解析正则匹配式
        self.url = 'https://maoyan.com/board/4?offset={}'  # 请求url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 '
                                      '(KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}  # 自定义headers,防基本反爬
        # 连接数据库
        self.db = pymysql.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  password='123456',
                                  database='maoyan_movies',
                                  charset='utf8')  # 连接数据库
        self.cur = self.db.cursor()

    def get_html(self, url):
        # 请求数据
        html = requests.get(url=url, headers=self.headers).content.decode(encoding='utf-8')
        self.parse_html(html)

    def parse_html(self, html):
        # 正则解析函数
        pattern = re.compile(self.regex, re.S)
        r_list = pattern.findall(html)
        self.save_html(r_list)

    def save_html(self, r_list):
        ins = 'insert into movie_top values(%s,%s,%s)'
        for r in r_list:
            li = [item.strip() for item in r]
            self.cur.execute(ins, li)
            self.db.commit()

    def run(self):
        # 循环请求数据取前10页
        for offset in range(0, 91, 10):
            page_url = self.url.format(offset)
            self.get_html(url=page_url)
            time.sleep(random.uniform(1, 3))
            print('第{}数据爬取完成；'.format((offset // 10) + 1))
        self.cur.close()
        self.db.close()


if __name__ == '__main__':
    spider = MaoYanSpider()
    spider.run()
