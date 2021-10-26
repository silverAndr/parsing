from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings



if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(SjruSpider)
    # process.crawl(HhruSpider)
    process.start()
