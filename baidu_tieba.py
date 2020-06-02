# 将百度贴吧某主题吧内容按页存在本地
import requests
import time
import random
from urllib import parse


class BaiDuTieBa:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 '
                                      '(KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
        self.url = 'https://tieba.baidu.com/f?kw={}&pn={}'  # 目标爬取地址

    def get(self, url):
        res = requests.get(url, headers=self.headers).content.decode(encoding='utf-8')
        return res

    def parse(self, html):
        pass

    def save(self, data, filename):
        with open(filename, 'w') as f:
            f.write(data)

    def run(self):
        subject = input('你想获取哪个贴吧的内容：')
        start_page = int(input('你想要获取的起始页：'))
        end_page = int(input('你想要获取的结束页：'))
        for index in range(start_page, end_page + 1):
            print('爬取到{}吧,第{}页数据！'.format(subject, index))
            # 确定url
            url = self.url.format(parse.quote(subject), (index - 1) * 10)  # URL中的中文需要进行转码
            res = self.get(url)
            filename = 'spider_data/{}_{}.html'.format(subject, index)
            self.save(res, filename)
            time.sleep(random.randint(1, 3))  # 控制网络爬取速度


if __name__ == '__main__':
    spider = BaiDuTieBa()
    spider.run()
