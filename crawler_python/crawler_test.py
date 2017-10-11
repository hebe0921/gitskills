# coding:utf-8
from bs4 import BeautifulSoup
import requests
import codecs

download_url = "https://book.douban.com/top250"


def load_html_page(url):
    html = requests.get(url,headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }).content
    return html


def parser_book_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    book_list_soup = soup.find('div', attrs={'class': 'indent'})
    book_list_name = []
    for book in book_list_soup.find_all("table"):
        detail = book.find('div', attrs={'class': 'pl2'})
        book_name = detail.find('a').get_text()
        book_list_name.append(book_name)
    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return book_list_name,download_url + next_page['href']
    return book_list_name,None






def main():
    url = download_url
    with codecs.open('book','wb',encoding="utf-8") as fp:
        while url:
            html = load_html_page(url)
            book, url = parser_book_html(html)
            fp.write(u'{book}\n'.format(book='\n'.join(book)))

if __name__ == '__main__':
    main()