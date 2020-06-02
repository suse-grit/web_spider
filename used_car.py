# 进入汽车之家二手车网爬取前5页数据(并存入MySQL)
# 1.分析目标URL
# https://m.che168.com/beijing/a0_0msdgscncgpi1lto8csp1exa0/
# https://m.che168.com/beijing/a0_0msdgscncgpi1lto8csp4exa0/
# https://m.che168.com/beijing/a0_0msdgscncgpi1lto8csp7exa0/
# https://m.che168.com/{}/a0_0msdgscncgpi1lto8csp{}exa0/.format(‘城市拼音小写’,页码)
# 2.页码
# 第1页-->1
# 第2页-->4
# 第3页-->7
# .......
# 3.确定合适的正则公式匹配响应数据,得到目标数据
import requests
import pymysql
import re
import time
import random
from urllib import parse


class UsedCarInfo:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 '
                                      '(KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
        self.url = 'https://m.che168.com/{}/a0_0msdgscncgpi1lto8csp{}exa0/'  # 目标爬取地址
        # 连接到数据库,准备将结果数据存到MySQL
        self.db = pymysql.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  password='123456',
                                  database='car_info',
                                  charset='utf8')
        self.cur = self.db.cursor()
        self.regex = r'<div class="card-right">.*?<h3>(.*?)</h3>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<i>(.*?)</i>'
        # 创建正则表达式匹配对象
        self.pattern = re.compile(self.regex, re.S)

    def get(self, url):
        res = requests.get(url, headers=self.headers).content.decode(encoding='utf-8')
        self.parse(res)

    def parse(self, html):
        r_list = self.pattern.findall(html)
        self.save(r_list)

    def save(self, r_list):
        # 存入mysql数据库
        for r in r_list:
            car_info = [r[0], r[2], '北京', r[3], r[4]]
            ins = 'insert into used_car values(%s,%s,%s,%s,%s)'
            self.cur.execute(ins, car_info)
            self.db.commit()

    def run(self):
        city = input('请输入你想要爬取的城市（拼音小写）：')
        start_page = int(input('你想要获取的起始页：'))
        end_page = int(input('你想要获取的结束页：'))
        count = 1
        for i in range(start_page, end_page + 1):
            url = self.url.format(parse.quote(city), count)  # URL终端中文需要转码
            count += 3
            self.get(url=url)
            print('已经爬取到{}的二手车平台,第{}页的数据；'.format(city, i))
            time.sleep(random.randint(1, 3))
        self.cur.close()
        self.db.close()


if __name__ == '__main__':
    spider = UsedCarInfo()
    spider.run()
