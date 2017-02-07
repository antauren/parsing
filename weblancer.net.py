# https://www.youtube.com/watch?v=KPXPr-KS-qk

import urllib.request
from bs4 import BeautifulSoup

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    div1 = soup.find('div', class_='container-fluid cols_table show_visited')
    #print(div.prettify())

    jobs = []

    for row in div1.find_all('div', 'row'):
        cols = row.find_all('div', 'col-sm-7 col-lg-8' )

        #print(cols)

        jobs.append({'title':cols[0].h2.a.text})

        for job in jobs:
            print(job)

def main():
    parse(get_html('https://www.weblancer.net/jobs/'))

if __name__ == '__main__':
    main()