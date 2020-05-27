import sys
import platform

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# import os
# print(platform.python_version())

def main():
    # #################### Step 1. Getting the URLs ####################
    fileName = "search_phrases.txt"
    search_strs = getSearchStrings(fileName)
    urls_per_phrase = [[] for i in range(len(search_strs))]

    for i in range(len(search_strs)):
        for url in search(search_strs[i],        # The query you want to run
                          tld = 'com',  # The top level domain
                          lang = 'ru',  # The language
                          num = 10,     # Number of results per page
                          start = 0,    # First result to retrieve
                          stop = 10,  # Last result to retrieve
                          pause = 2.0,  # Lapse between HTTP requests
                          ):
            urls_per_phrase[i].append(url)

    # # print all the urls
    # for i in range(len(urls_per_phrase)):
    #     print()
    #     for j in range(len(urls_per_phrase[i])):
    #         print(urls_per_phrase[i][j])

    # #################### Step 2. Parsing the URLs ####################
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}

    response = requests.get(urls_per_phrase[0][4], headers)
    # response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())
    print(soup.get_text())


    # ####################Step 3. Organizing extracted data ####################


    # urls = makeURLs(search_strs)
    # google(urls)
    # print(type(reqs))

    # google(reqs)

def makeGoogleURLs(search_strs):
    urls = []
    for q in search_strs:
        q = '+'.join(q.split())
        url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8'
        urls.append(url)
    return urls


def google(urls):
    ua = UserAgent()
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
    filePath = os.path.relpath(fileName)

    if not os.path.isfile(filePath):
        print("File path {filePath} does not exist. Exiting...")

    with open(filePath, 'r') as f:
        line = f.readline()
        while line:
            requests.append(line)
            line = f.readline()
    return requests


def printLstObj(lst):
    print()
    for i in range(len(lst)):
        print(lst[i])


if __name__ == '__main__':
    main()
