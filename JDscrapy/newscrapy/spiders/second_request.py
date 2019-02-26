"""一级商品数据还有二级商品目录，所以要从一级商品url找出二级商品目录，存入另外的数据库，数据也要去重，假定数据量比较大，也需要用hadoop来多机器来处理"""
import scrapy
import json
import functools
import logging
import datetime
from ..dbTool import MongoDb
from scrapy.selector import Selector

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
url_list, status = db.getall('url_doc')
if status != '成功':
    logging.error("从mogodb获取数据失败")
    exit()


class QuotesSpider(scrapy.Spider):
    name = "second_url"

    def start_requests(self):
        for first_url in url_list:
            yield scrapy.Request('https:' + first_url['url'], self.parse, headers=headers)

    def price_parse(self, dic, response):
        pric_dic = json.loads(response.text[20:-1])
        dic['price_list'] =[{"price": pric_dic['accessories']['data']['wMaprice'], "date_time":datetime.datetime.now()}]
        db.insert('ebook_detail', dic)

    def parse(self, response):
        data_text = response.css('.Ptable').get()
        detail_se = Selector(text=data_text)
        detail_list = detail_se.css('.clearfix').getall()
        dic = {}
        dic['url'] = response.url
        for text in detail_list:
            title = text[text.find('<dt>') + 4:text.find("</dt>")]
            inner = text[text.rfind('<dd>') + 4:text.rfind('</dd>')]
            if title.find('.') != -1:
                title = title.replace('.', '')
            dic[title] = inner
        url = response.url
        sku = url[url.rfind('/') + 1:url.rfind('.html')]
        dic[
            'price_url'] = 'https://c.3.cn/recommend?callback=handleComboCallback&methods=accessories&p=103003&sku={}&cat=670,671,1105&lid=1&uuid=513893367&pin=&ck=pin,ipLocation,atw,aview&lim=5&cuuid=513893367&csid=122270672.7.513893367|4.1549611668&_=1549612484096'.format(
            sku)
        parice = functools.partial(self.price_parse, dic)
        yield scrapy.Request(dic['price_url'], parice)
