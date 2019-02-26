from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


scope = 'all'
process = CrawlerProcess(settings=get_project_settings())

process.crawl('update_price')
process.start()
