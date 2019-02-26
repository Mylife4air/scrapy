"""爬取商品一级页面的爬虫，把数据入库"""
import re
import scrapy
from ..dbTool import MongoDb
from scrapy.selector import Selector

headers = {
    "Host": "list.jd.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cookie": "__jdu=15466297164981741029566; ipLoc-djd=1-72-4137-0; areaId=1; listck=3752308ea944a1adabf48b8372dfeddc; __jda=122270672.15466297164981741029566.1546629716.1549169835.1549176334.4; shshshfp=9619802ba3bb1df2baa8ab4143e86bef; shshshfpa=e5bdedfd-e0de-36ca-b787-f4c05b0a238e-1546629851; shshshfpb=eQzMUplmRG4rVIeAlVVY8kQ%3D%3D; unpl=V2_ZzNtbRZTFBN1X04BKR9eA2IBR1hKBRMWdwxOAHgfWVJuBhZeclRCFX0UR1dnGF4UZwAZWURcQhNFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHsdWQJgABpbQlBGHXwIQFF7GF8NYwQVbXJQcyVFDUBVeR5fNWYzE20AAx8dfQ1GXXJUXAFiBBVeSlFDEnAAT1R9HFwEZAsWWkVnQiV2; __jdc=122270672; __jdv=122270672|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_e5f71f9dc73743d49ca2359e274f8452|1549169835146; PCSYCityID=1574; _gcl_au=1.1.809171021.1549169857; 3AB9D23F7A4B3C9B=3DCSDVW7NENWY5TGC2EX62LVGZFPF454FGW2YNMMIWBQKELCMG3NN2TQE2LPWNUC3BG3QLZUKHTESOYFKI5H2QNLMA; shshshsID=0296e7b76fed7732f1e153b76ba3e971_6_1549176369719; __jdb=122270672.8.15466297164981741029566|4.1549176334",
    "Upgrade-Insecure-Requests": "1",
    "TE": "Trailers"

}

url_list = ['https://list.jd.com/list.html?cat=9987,653,655&page=1&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main',
            'https://list.jd.com/list.html?cat=670,671,672&page=1&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main']
db = MongoDb()


class QuotesSpider(scrapy.Spider):
    name = "good_url"

    def start_requests(self):
        for first_url in url_list:
            yield scrapy.Request(first_url, self.parse, meta={'dont_redirect': True}, headers=headers)

    def parse(self, response):
        text_list = response.css('.gl-warp').get()
        next_url = response.xpath('/html/body/div[8]/div[1]/div[3]/div[1]/div/div[4]/div/span[1]/a[10]').get()
        pre_url = response.url.replace(re.findall("page=\d+", response.url)[0], 'page={}')
        if next_url == None:
            return 'ok'
        else:
            next_url = re.findall("page=\d+", next_url)[0][5:]
        url_list = Selector(text=text_list).css('[target]').getall()
        for url in url_list:
            a = url[url.find('href=') + 6:]
            b = a[:a.find('html') + 4]
            db.insert('url_doc', {"url": b})
        yield scrapy.Request(pre_url.format(next_url), self.parse, meta={'dont_redirect': True}, headers=headers)
