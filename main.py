import re
import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://quotes.toscrape.com'


def get_urls():
    urls=[]
    counter=1
    while True:
        url_path=f"{BASE_URL}/page/{counter}/"
        next_button_li=BeautifulSoup(requests.get(url_path).text, 'html.parser').select("li[class=next]")
        urls.append(url_path)
        counter += 1
        if not next_button_li:
            break
    print(urls)
    return urls



def author_spider(author_url):
    html_doc = requests.get(f"{BASE_URL}{author_url}/")
    soup = BeautifulSoup(html_doc.text, "html.parser")
    author_dict = {
        "fullname": soup.select_one(".author-title").get_text(),
        "born_date": soup.select_one(".author-born-date").get_text(),
        "born_location": soup.select_one(".author-born-location").get_text(),
        "description":soup.select_one(".author-description").get_text().strip(),
    }
    return author_dict



def spider(url):
    url_quotes=[]
    authors_list=[]
    url_authors=[]
    soup=BeautifulSoup(requests.get(url).text, "html.parser")
    quote_divs_list=soup.select("div[class=quote]")
    for quote_div in quote_divs_list:
        author=quote_div.select_one(".author").get_text()
        if author not in authors_list:
            authors_list.append(author)
            url_authors.append(author_spider(quote_div.select_one("[href^='/author/']")["href"]))
        url_quotes.append({
            "tags":[a.get_text() for a in quote_div.select("a[class=tag]")],
            "author":author,
            "qoute":quote_div.select_one(".text").get_text(),
        })


    return  



def main(urls):
    data = []
    for url in urls:
        data.extend(spider(url))
    return data


if __name__ == '__main__':
    # result = main(get_urls())
    # print(result)
    spider("https://quotes.toscrape.com/page/1/")


    # print(result := main(get_urls()))
    # with open('kacapy.json', 'w', encoding='utf-8') as fd:
    #     json.dump(result, fd, ensure_ascii=False, indent=2)
