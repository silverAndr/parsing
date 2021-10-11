
import sys
import pandas as pd
import xlsxwriter # pip install XlsxWriter
import requests # pip install requests
from bs4 import BeautifulSoup as bs # pip install beautifulsoup4

headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
vacancy = input('Укажите название вакансии: ')
base_url = f'https://hh.ru/search/vacancy?area=2&search_period=30&text={vacancy}&page=' # area=1 - Москва, search_period=3 - За 30 последних дня
print(base_url)
pages = int(input('Укажите кол-во страниц для парсинга: '))
jobs =[]

def get_hh_vacancy(div):
    title = div.find('a', attrs = {'data-qa':'vacancy-serp__vacancy-title'}).text
    print(title)
    compensation = div.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
    if compensation == None: # Если зарплата не указана
            compensation = 'None'
    else:
            compensation = div.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
    href = div.find('a', attrs = {'data-qa': 'vacancy-serp__vacancy-title'})['href']
    try:
            company = div.find('a', attrs = {'data-qa': 'vacancy-serp__vacancy-employer'}).text
    except:
            company = 'None'
    object_text1 = div.find('div', attrs = {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'})
    if(type(object_text1) == 'bs4.element.Tag'):
        text1 = object_text1.text
    else:
        text1 = ''
    object_text2 = div.find('div', attrs = {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'})
    if(type(object_text2) == 'bs4.element.Tag'):
        text2 = object_text2.text
    else:
        text2 = ''
    content = text1 + '  ' + text2
    return [title, compensation, company, content, href]

def hh_parse(base_url, headers):
        zero = 0
        while pages > zero:
                zero = str(zero)
                session = requests.Session()
                request = session.get(base_url + zero, headers = headers)
                if request.status_code == 200:
                        soup = bs(request.content, 'lxml')
                        divs = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
                        for div in divs:
                                all_txt = get_hh_vacancy(div)
                                jobs.append(all_txt)
                        zero = int(zero)
                        zero += 1
                else:
                        print('error')
                print('OK')
        df = pd.DataFrame(jobs)
        print(df)
hh_parse(base_url, headers)

