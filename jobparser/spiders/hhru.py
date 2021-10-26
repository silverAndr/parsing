# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://spb.hh.ru/search/vacancy?area=&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        next_page = 'https://spb.hh.ru' \
                    + response.css('a[class="bloko-button"][data-qa="pager-next"]').attrib['href']
        print(next_page)
        response.follow(next_page, callback=self.parse)
        vacansy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header '
            'a.bloko-link::attr(href)'
        ).extract()
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('h1[data-qa="vacancy-title"]::text').get()
        link = response.url
        domen = re.search('https?://([A-Za-z_0-9.-]+).*', link)
        if domen:
            domen = domen.group(1)
        ar_salary = response.css('span[data-qa="vacancy-salary-compensation-type-net"]'
                                      '[class="bloko-header-2 bloko-header-2_lite"]::text').getall()
        salary_min = salary_max = None
        for i in range(len(ar_salary)):
            salary_part = ar_salary[i]
            if salary_part.strip() == "от":
                salary_min = float(re.sub(r"\s+", "", ar_salary[i+1]))
            if salary_part.strip() == "до":
                salary_max = float(re.sub(r"\s+", "", ar_salary[i+1]))

        yield JobparserItem(name=name, salary_min=salary_min, salary_max=salary_max, link=link, source=domen)
