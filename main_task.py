import json
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://quotes.toscrape.com'

def author_spider(author_url):
    html_doc = requests.get(f"{BASE_URL}{author_url}/")
    soup = BeautifulSoup(html_doc.text, "html.parser")
    author_fullname=soup.select_one(".author-title").get_text()
    if author_fullname=="Alexandre Dumas-fils":
        author_fullname="Alexandre Dumas fils"
    author_dict = {
        "fullname": author_fullname,
        "born_date": soup.select_one(".author-born-date").get_text(),
        "born_location": soup.select_one(".author-born-location").get_text(),
        "description":soup.select_one(".author-description").get_text().strip(),
    }
    return author_dict

def quote_spider(url):
    page_quotes=[]
    page_authors_url_list=[]
    soup=BeautifulSoup(requests.get(url).text, "html.parser")
    quote_divs_list=soup.select("div[class=quote]")
    for quote_div in quote_divs_list:
        page_authors_url_list.append(quote_div.select_one("[href^='/author/']")["href"])
        page_quotes.append({
            "tags":[a.get_text() for a in quote_div.select("a[class=tag]")],
            "author":quote_div.select_one(".author").get_text(),
            "quote":quote_div.select_one(".text").get_text(),
        })
    return  [page_quotes, page_authors_url_list]

def result_to_json(file_name, data):
    with open(f'goit-pyweb-hw-08-task1/{file_name}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def main():
    quotes=[]
    authors_urls=[]
    authors=[]

    counter=1
    while True:
        url_page=f"{BASE_URL}/page/{counter}/"
        next_button_li=BeautifulSoup(requests.get(url_page).text, 'html.parser').select("li[class=next]")
        page_quotes, page_authors_url_list=quote_spider(url_page)
        quotes.extend(page_quotes)
        authors_urls.extend(page_authors_url_list)
        counter += 1
        if not next_button_li:
            break
    result_to_json("qoutes", quotes)

    for author_url in list(set(authors_urls)):
        authors.append(author_spider(author_url))
    result_to_json("authors", authors)


if __name__ == '__main__':
    main()

