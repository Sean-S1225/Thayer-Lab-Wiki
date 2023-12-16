import requests
from bs4 import BeautifulSoup
from sys import path
path.append("../")
from  unit_test import UnitTest

def GetPageContent() -> BeautifulSoup:
    """Returns HTML file containing information about recent Thayer lab publications

    Returns:
        BeautifulSoup object containing information about recent publications
    """
    URL = "https://scholar.google.com/citations?hl=en&user=qw1NDkwAAAAJ&view_op=list_works&sortby=pubdate"
    headers = {'User-Agent': 
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"} 
    r = requests.get(url=URL, headers=headers) 

    soup = BeautifulSoup(r.content, "html.parser")

    return soup

def GetRecentPapers(soup: BeautifulSoup) -> list:
    """Gets the recent papers that are published with Kelly Thayer as an author

    Args:
        soup: A BeautifulSoup object containing information about recent publications

    Returns:
        A list of dictionaries containing relevant information about each paper
    """
    
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

    return articles

def GeneratePages(articles: list, dest: str) -> None:
    """Uses a list of articles to generate HTML page containing information about each

    Args:
        articles: The list of articles
        dest: The file to write to
    """
    text = [
        "{% extends \"layout.html\" %}\n",
        "{% block content %}\n",
        "<h1>Recent Publications by the Thayer Lab</h1>\n"
    ]
    for article in articles:
        text.append("<div class=\"paper\">\n")
        text.append(f"<h2>{article['title']}</h2>\n")
        text.append(f"<p>Authors: {article['authors']}</p>\n")
        text.append(f"<p>Year Published: {article['year']}</p>\n")
        text.append(f"<p>Number of Citations: {article['citations']}</p>\n")
        text.append("</div>\n")
        text.append("<br><br>\n\n")

    text.append("{% endblock content %}\n")
    with open(dest, "w") as file:
        file.writelines(text)

def GetPapers(path):
    GeneratePages(GetRecentPapers(GetPageContent()), path)

if __name__ == "__main__":
    # x = GetRecentPapers(GetPageContent())
    # for y in x:
    #     print("{")
    #     for key, val in y.items():
    #         print(f"\t{key}: {val}")
    #     print("}")

    # GeneratePages(GetRecentPapers(GetPageContent()), "./templates/papers.html")

    def Read(fileName):
        with open(fileName, "r") as file:
            return file.read()

    UnitTest(GetRecentPapers, (BeautifulSoup(Read("../tests/RecentPublications/FakePage1.html"), "html5lib"),),
             ([{"title": "Molecular Dynamics of Mismatch Detection–How MutS Uses Indirect Readout to Find Errors in DNA", 
               "authors": "A Jayaraj, KM Thayer, DL Beveridge, MM Hingorani", "journal": "Biophysical Journal", "citations": 0, "year": "2023"}],))
    
    GeneratePages(GetRecentPapers(BeautifulSoup(Read("../tests/RecentPublications/FakePage1.html"), "html5lib")), "../tests/RecentPublications/Output.html")

    UnitTest(Read, ("../tests/RecentPublications/Output.html",), (\
"""{% extends "layout.html" %}
{% block content %}
<h1>Recent Publications by the Thayer Lab</h1>
<div class="paper">
<h2>Molecular Dynamics of Mismatch Detection–How MutS Uses Indirect Readout to Find Errors in DNA</h2>
<p>Authors: A Jayaraj, KM Thayer, DL Beveridge, MM Hingorani</p>
<p>Year Published: 2023</p>
<p>Number of Citations: 0</p>
</div>
<br><br>

{% endblock content %}
""",))