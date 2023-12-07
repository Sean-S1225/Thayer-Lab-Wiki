import requests
from bs4 import BeautifulSoup

URL = "https://scholar.google.com/citations?hl=en&user=qw1NDkwAAAAJ&view_op=list_works&sortby=pubdate"
headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"} 
r = requests.get(url=URL, headers=headers) 

soup = BeautifulSoup(r.content, "html5lib")
# print(soup.prettify()) 

table = soup.find("div", attrs={"id": "gsc_a_tw"})
articles = []

for row in table.find_all("tr", attrs={"class": "gsc_a_tr"}):
    article = {}

    info, citations, year = row.find_all("td")

    article["title"] = info.a.text
    authors, journal = [x.text for x in info.find_all("div")]
    journal = journal.split(",")[0]
    article["authors"], article["journal"] = authors, journal

    if citations.a.text:
        article["citations"] = citations.a.text
    else:
        article["citations"] = 0

    article["year"] = year.span.text

    articles.append(article)
