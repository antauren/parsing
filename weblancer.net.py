# https://www.youtube.com/watch?v=KPXPr-KS-qk

import urllib.request
from bs4 import BeautifulSoup
import csv

BASE_URL = 'https://www.weblancer.net/jobs/'

def get_page_count(html):
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find('ul','pagination')
    last_page = str( pagination.find_all('li')[-1].a )[21:-15]
    return int(last_page)

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    div1 = soup.find('div', class_='container-fluid cols_table show_visited')

    jobs = []

    for row in div1.find_all('div', 'row'):
        titles = row.find_all( 'div', 'col-sm-7 col-lg-8' )
        categories = row.find_all( 'div', 'col-xs-12 text-muted' )
        prices = row.find_all( 'div', 'col-sm-1 amount title' )
        order = row.find_all( 'div', 'col-sm-3 text-right text-nowrap hidden-xs' )

        jobs.append({
            'title': titles[0].h2.a.text,
            'categories': categories[0].a.text,
            'prices': prices[0].text.strip(),
            'order': order[0].text.strip()
        })
    return jobs

def save(jobs, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Вакансия', 'Категория', 'Цена', 'Заявки'))

        for job in jobs:
            writer.writerow(( job['title'], job['categories'], job['prices'], job['order'] ))


def main():
    page_count = get_page_count(get_html(BASE_URL))

    print('Всего найдено страниц: %d' %page_count)

    jobs = []

    #page_count = 8 #если задать количество страниц вручную до 8 то ошибок нет
    # Возможно они вкрутили защиту от Парсинга   Тогда можно добавить небольшую задержку между обращениями к сайту

    # заметил что на www.weblancer.net/jobs/ количество страниц уменьшилось на одну, и все заработало, возможно одна из них глюк давала

    # на данный момент работает только с третьей страницы
    for page in range(3, page_count):
        print('Парсинг %d%%' % (page / page_count * 100 ))
        jobs.extend(  parse( get_html(BASE_URL + '?page=%d' % page) )  )

    for job in jobs:
        print(job)

    save(jobs, 'weblanser.net.csv')

    #print(get_page_count(get_html('https://www.weblancer.net/jobs/')))
    #print(parse(get_html('https://www.weblancer.net/jobs/')))

if __name__ == '__main__':
    main()