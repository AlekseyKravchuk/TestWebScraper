import os
from googlesearch import search
import urllib
from fake_useragent import UserAgent
import re
from bs4 import BeautifulSoup


def main():
    # #################### Step 1. Getting the URLs ####################
    fileName = "search_phrases.txt"
    search_strs = getSearchStrings(fileName)

    urls = []
    for i in range(len(search_strs)):
        for url in search(search_strs[i],  # The query you want to run
                          tld='com',       # The top level domain
                          lang='ru',       # The language
                          num=10,          # Number of results per page
                          start=0,         # First result to retrieve
                          stop=10,         # Last result to retrieve
                          pause=2.0,       # Lapse between HTTP requests
                          ):
            urls.append(url)
    # #################### Step 2. Parsing the URLs ####################
    # Get rid of URL duplicates (extract base URLs and store only unique ones)
    base_urls = getBaseUrls(urls)
    urls = list(set(base_urls))

    # print unique_urls
    # print("unique_urls: ")
    # for url in urls:
    #     print(url)

    # URL to test:
    url = urls[7]
    print(f"\ncurrent url to test: {url}")

    # create headers for http-requests using fake user-agent
    # simple prevention measure against being blocked - to fake a browser visit
    ua = UserAgent()
    request = urllib.request.Request(
        url,
        data=None,
        headers={'User-Agent': ua.google}
        )

    try:
        # urllib.request.urlopen(...) returns object of type: http.client.HTTPResponse
        with urllib.request.urlopen(request, timeout=10) as response:
            raw_data = response.read()
    except timeout:
        raise ValueError('Timeout ERROR')
    except (HTTPError, URLError):
        raise ValueError('Bad Url ERROR')

    status = response.status
    contentType = response.info().get_content_type()
    charset = response.info().get_content_charset()

    if (status != 200):
        raise ValueError('Server returned BAD STATUS code.')
    if (contentType != 'text/html'):
        raise ValueError('contentType is not text/html, handler hasn\'t implemented yet')
    if (charset != 'utf-8'):
        raise ValueError('charset is not utf-8, handler hasn\'t implemented yet')

    # suppose it will work for other than utf-8 charsets
    # convert bytes to string using the proper charset
    html = raw_data.decode(charset)

    # try to use regular expression directly to extract emails
    emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', html)
    print("EMAILS:")
    for mail in emails:
        print(f"\t{mail}")

    # try to extract all the links in html page
    soup = BeautifulSoup(html, "lxml")

    links = soup.find_all(re.compile('^a'))
    print("LINKS:")
    for link in links:
        print(f"\t{link}")

    # # ####################Step 3. Organizing extracted data ####################


    # #################### FUNCTIONS ####################

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


def getBaseUrls(urls):
    parsed = [urllib.parse.urlparse(url) for url in urls]
    return [x.scheme + '://' + x.hostname + '/' for x in parsed ]


if __name__ == '__main__':
    main()
