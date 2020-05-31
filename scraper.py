import os
import urllib.request
import shutil
import tempfile
# import pandas as pd
# import re
# import scrapy
# from scrapy.crawler import CrawlerProcess
# from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

# import requests
# from bs4 import BeautifulSoup

# simple prevention measure against being blocked - to fake a browser visit
from fake_useragent import UserAgent


def main():
    # #################### Step 1. Getting the URLs ####################
    fileName = "search_phrases.txt"
    search_strs = getSearchStrings(fileName)

    # Print all search strings
    # print()
    # for i in search_strs:
    #     print(i)


    urls_per_phrase = [[] for i in range(len(search_strs))]

    for i in range(len(search_strs)):
        for url in search(search_strs[i],  # The query you want to run
                          tld='com',     # The top level domain
                          lang='ru',     # The language
                          num=10,        # Number of results per page
                          start=0,       # First result to retrieve
                          stop=10,       # Last result to retrieve
                          pause=2.0,     # Lapse between HTTP requests
                          ):
            urls_per_phrase[i].append(url)

    # print all the urls
    # for i in range(len(urls_per_phrase)):
    #     print()
    #     for j in range(len(urls_per_phrase[i])):
    #         print(urls_per_phrase[i][j])

    # links_lst = toLstOfStrs(urls_per_phrase)
    # # for i in range(len(links_lst)):
    # #     print(links_lst[i])


    # # #################### Step 2. Parsing the URLs ####################
    url = urls_per_phrase[0][7]
    print(f"current url to test: {url}")
    # with urllib.request.urlopen(url) as response:
    #     html = response.read()
    fileNameToWritePageContent = "test.html"

    # create headers for http-requests using fake user-agent
    ua = UserAgent()
    request = urllib.request.Request(
        url,
        data=None,
        headers={'User-Agent': ua.google}
        )

    # open connection to a given URL using urllib
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            conn = response.read()
    except timeout:
        raise ValueError('Timeout ERROR')

    except (HTTPError, URLError):
        raise ValueError('Bad Url ERROR')

    print(f"response status code = {response.getcode()}")
    print(f"content_type = {response.info().get_content_type()}")

    # write contents of conn to the file
    try:
        with open(fileNameToWritePageContent, 'wb') as file:
            file.write(conn)
    except OSError as e:
        print('open() or file.__enter__() failed', e)

    # # ua = UserAgent()
    # # headers = {'User-Agent': ua.chrome}
    # # response = requests.get(urls_per_phrase[0][5], headers)
    # # soup = BeautifulSoup(response.content, "html.parser")
    # # result_div = soup.find_all('div', attrs = {'class': 'hfeed site'})
    # # print(result_div.prettify())


    # # ####################Step 3. Organizing extracted data ####################


def makeGoogleURLs(search_strs):
    urls = []
    for q in search_strs:
        q = '+'.join(q.split())
        url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
        urls.append(url)
    return urls


def google(urls):
    print(ua.chrome)
    headers = {'User-Agent': ua.chrome}

    # делаем запрос, передав заголовок
    resp = requests.get(urls[0], headers=headers)
    print(resp.content)
    # s = requests.Session()

    # for i in q:
    #     print()

    # q = '+'.join(q.split())
    # url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
    # r = s.get(url, headers=headers_Get)

    # soup = BeautifulSoup(r.text, "html.parser")
    # output = []
    # for searchWrapper in soup.find_all('h3', {'class':'r'}): #this line may change in future based on google's web page structure
    #     url = searchWrapper.find('a')["href"]
    #     text = searchWrapper.find('a').text.strip()
    #     result = {'text': text, 'url': url}
    #     output.append(result)

    # return output


def getSearchStrings(fileName):
    requests = []
    # filepath = sys.argv[1]
    # filePath = os.path.relpath(fileName)

    if not os.path.isfile(fileName):
        print("File path {fileName} does not exist. Exiting...")

    with open(fileName, 'r') as f:
        line = f.readline()
        while line:
            requests.append(line)
            line = f.readline()
    return requests


def printLstObj(lst):
    print()
    for i in range(len(lst)):
        print(lst[i])


def toLstOfStrs(lst_of_lst):
    l = []
    for lst in lst_of_lst:
        for str in lst:
            l.append(str)
    return l


class MailSpider(scrapy.Spider):

    name = 'email'

    def parse(self, response):

        links = LxmlLinkExtractor(allow=()).extract_links(response)
        links = [str(link.url) for link in links]
        links.append(str(response.url))

        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_link)

    def parse_link(self, response):

        for word in self.reject:
            if word in str(response.url):
                return

        html_text = str(response.text)
        mail_list = re.findall('\w+@\w+\.{1}\w+', html_text)

        dic = {'email': mail_list, 'link': str(response.url)}
        df = pd.DataFrame(dic)

        df.to_csv(self.path, mode='a', header=False)
        df.to_csv(self.path, mode='a', header=False)


if __name__ == '__main__':
    main()
