# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://spb.superjob.ru/vacancy/search/?keywords=php']

    def parse(self, response: HtmlResponse):
        print('parse:')
        response.follow(response.url, callback=self.vacansy_parse)
        vacansy = response.css(
            'div.f-test-search-result-item a.icMQ_._6AfZ9::attr(href)'
        ).extract()
        print('url: ' + response.url)
        print('len: ' + str(len(vacansy)))
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

        next_page = 'https://spb.superjob.ru' + response.css('a[rel="next"]').attrib['href']
        if next_page:
            yield scrapy.Request(response.follow(next_page), callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('h1::text').get()
        print(name)
        link = response.url
        print(link)
        domen = re.search('https?://([A-Za-z_0-9.-]+).*', link)
        if domen:
            domen = domen.group(1)
        print(domen)
        ar_salary = response.css('.f-test-vacancy-base-info span._2Wp8I._2rfUm._2hCDz::text').extract()
        salary_min = salary_max = None
        if len(ar_salary) == 4:
            salary_min = ar_salary[0] + ar_salary[2] + ar_salary[3]
            salary_max = ar_salary[1] + ar_salary[2] + ar_salary[3]
        else:
            for i in range(len(ar_salary)):
                salary_part = ar_salary[i]
                if salary_part.strip() == "от":
                    salary_min = ar_salary[i+2]
                if salary_part.strip() == "до":
                    salary_max = ar_salary[i+2]
        print(salary_min)
        print(salary_max)
        yield JobparserItem(name=name, salary_min=salary_min, salary_max=salary_max, link=link, source=domen)
