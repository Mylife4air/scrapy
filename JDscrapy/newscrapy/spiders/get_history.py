"""价格更新爬虫，用于定时更新商品的价格"""
import scrapy
import json
import functools
import re
import logging
import datetime
from ..dbTool import MongoDb

headers = {
    'Host': 'p.zwjhl.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://www.lsjgcx.com/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}
db = MongoDb()
url_list, status = db.getall('ebook_detail')
if status != '成功':
    logging.error("从mogodb获取数据失败")
    exit()


class QuotesSpider(scrapy.Spider):
    name = "get_history"
    custom_settings = {
        "DOWNLOAD_DELAY": 0.5,
    }

    def start_requests(self):
        gwd_url = 'http://p.zwjhl.com/price.aspx?url=https%3a%2f%2fitem.jd.com%2f{}.html'
        for first_url in url_list:
            url = first_url['url']
            id = url[url.rfind('/') + 1:url.rfind('.html')]
            parse = functools.partial(self.price_parse, first_url)
            yield scrapy.Request(gwd_url.format(id), parse)

    def price_parse(self, first_url, response):
        def text_dic(text):
            date = text[text.find('(')+1:text.find(')')]
            price = text[text.find('),')+2:]
            date = date.split(',')
            return {'date_time':datetime.datetime(year=int(date[0]), month=int(date[1]), day=int(date[2])), 'price':price}
        a = scrapy.selector.Selector(text=response.text)
        text = a.xpath('/html/body/div[2]/div/div/div[1]').get()
        text = text[text.find('<script') + 70:text.find('</script>') - 7]
        text_list = text.split('],')
        price_list = [text_dic(x) for x in text_list]
        first_url['price_list'] = price_list
        db.update_one('ebook_detail', {'_id': first_url['_id']}, first_url)
