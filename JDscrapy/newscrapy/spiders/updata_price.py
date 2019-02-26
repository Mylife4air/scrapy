"""价格更新爬虫，用于定时更新商品的价格"""
import scrapy
import json
import functools
import logging
import datetime
from ..dbTool import MongoDb

headers = {
    "Host": "item.jd.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cookie": " __jda=122270672.513893367.1549263502.1549263502.1549263505.1; unpl=V2_ZzNtbUcFQUF2WkJReBtZUmJQGg8RUhYVIQlCUXIYVQwwA0FUclRCFX0UR1dnGFkUZwYZWUtcQBZFCEdkex5fDGQzFlxDUUsTdg92ZHgZbARXBxJfS19BF3IOdmR7EVg1V9eH9prc1Ec0Sp%2fk3s%2f2q1cEF1pEXkoQcThHZHopF2tmThZdQF5LF3cPQGR6KV8%3d; __jdb=122270672.10.513893367|1.1549263505; __jdc=122270672; __jdv=122270672|c.duomai.com|t_16282_50079726|tuiguang|4c3e2c54234f4b9cb4d1e0548088f1b8|1549263505115; __jdu=513893367; user-key=6041521b-748a-4521-862f-1e83aaabd36e; cn=1; PCSYCityID=1574; shshshfp=bf39ee2a18b406aa73b31221a7d43da3; shshshfpa=9537ad2f-e986-8e55-4dca-889195e53e8f-1549263512; shshshsID=4c9aad60ee1d2ba8e211c70cabbd48b2_6_1549265130797; shshshfpb=teFOnVdE9i3FubH1YbAjHsw%3D%3D; ipLoc-djd=1-72-4137-0; areaId=1; _gcl_au=1.1.1744889439.1549263528; 3AB9D23F7A4B3C9B=DDBE6BA4NAKAWFJ43JADEJT3GGIMRTQUUHH3JMR667NJP3YTTQYFD7P3HDQAM4EFG5QOKY75VPCYIR2MFOTOQI2NZA",
    "Upgrade-Insecure-Requests": "1",

}

db = MongoDb()
url_list, status = db.getall('ebook_detail')
if status != '成功':
    logging.error("从mogodb获取数据失败")
    exit()


class QuotesSpider(scrapy.Spider):
    name = "update_price"

    def start_requests(self):
        for first_url in url_list:
            parse = functools.partial(self.price_parse, first_url)
            yield scrapy.Request(first_url['price_url'], parse)

    def price_parse(self, first_url, response):
        dic = {}
        pric_dic = json.loads(response.text[20:-1])
        dic['price'] = pric_dic['accessories']['data']['wMaprice']
        dic['date_time'] = datetime.datetime.now()
        first_url['price_list'].append(dic)
        db.update_one('ebook_detail', {'_id': first_url['_id']},first_url)
