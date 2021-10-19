from pprint import pprint
from lxml import html
import requests
import time

articles = []

ya_link = 'https://yandex.ru'
response = requests.get(ya_link+'/news/')
root = html.fromstring(response.text)
news = root.xpath("//article")
for article in news:
    new = {
        'name': article.xpath(".//h2[@class='mg-card__title']/text()")[0],
        'link': article.xpath(".//a[@class='mg-card__link']/@href")[0],
        'source': article.xpath(".//a[@class='mg-card__source-link']/text()")[0],
        'time': article.xpath(".//span[@class='mg-card-source__time']/text()")[0]
    }
    articles.append(new)

lenta_link = 'https://lenta.ru'
response = requests.get(lenta_link+'/')
root = html.fromstring(response.text)
news = root.xpath("//div[@class='item']")
for article in news:
    new = {
        'name': article.xpath(".//a/text()")[0],
        'link': article.xpath(".//a/@href")[0],
        'source': None,
        'time': article.xpath(".//time[@class='g-time']/@datetime")
    }
    articles.append(new)

mail_link = 'https://news.mail.ru'
response = requests.get(mail_link+'/')
root = html.fromstring(response.text)
news = root.xpath("//div[@class='daynews__item' or @class='daynews__item daynews__item_big']")

for article in news:
    new = {
        'name': article.xpath(".//span[@class='photo__captions']/span/text()")[0],
        'link': article.xpath(".//a/@href")[0],
        'source': None,
        'time': None
    }
    articles.append(new)
news2 = root.xpath("//li[@class='list__item']")
for article in news2:
    if article.xpath(".//a"):
        new = {
            'name': article.xpath(".//*[@class='link__text' or @class='list__text']/text()"),
            'link': article.xpath(".//*[@class='link link_flex' or @class='list__text']/@href"),
            'source': None,
            'time': None
        }
    else:
        new = {
            'name': article.xpath(".//s[[@class='list__text']/text()"),
            'link': None,
            'source': None,
            'time': None
        }
    articles.append(new)

print(articles)

