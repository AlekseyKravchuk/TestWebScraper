import os
from googlesearch import search
import urllib
from fake_useragent import UserAgent
import re
from bs4 import BeautifulSoup


def main():
    # #################### Step 1. Getting the URLs using Google search engine ####################
    # file name to extract search strings from
    fileName = "search_phrases.txt"

    search_strs = getSearchStrings(fileName)

    # extract base URLs and store only unique ones
    urls = getBaseUrls( getURLs(search_strs) )

    # for url in urls:
    #     print(url)

    url = urls[3]  # URL to test:
    print(f"\ncurrent url to test: {url}")
    html = getHTMLPageAsString(url)

    # #################### Step 2. Parsing the URLs ####################

    # use regular expression to extract emails from main page
    emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', html)
    # emails = re.findall('\w+@\w+\.{1}\w+', html)
    # phones = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', html)
    phones = re.findall("[(][\d]{3}[)][ ]?[\d]{3}-[\d]{4}", html)
    # phone_number_regex_pattern = r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}"
    unique_phones = set(phones)
    unique_emails = set(emails)

    print("EMAILS:")
    for mail in unique_emails:
        print(f"\t{mail}")

    print("PHONES:")
    for mail in unique_phones:
        print(f"\t{phones}")

    # extract all the <a> tags from page(string) html
    soup = BeautifulSoup(html, "lxml")
    links = []
    tags = soup.find_all('a')
    accepted_strings = {'Контакты', 'О компании'}

    for tag in tags:
        if (tag.text in accepted_strings):
            links.append(tag.attrs['href'])

    unique_links = set(links)

    #  links of interest to follow in next commit
    print("LINKS:")
    for link in unique_links:
        print(f"\t{link}")

    # # ####################Step 3. Organizing extracted data ####################


    # #################### FUNCTIONS ####################

def getSearchStrings(fileName):
    requests = []
    if not os.path.isfile(fileName):
        print("File path {fileName} does not exist. Exiting...")

    with open(fileName, 'r') as f:
        line = f.readline()
        while line:
            requests.append(line)
            line = f.readline()
    return requests


def getBaseUrls(urls):
    # Parse a URL into six components, returning a 6-item named tuple.
    parsed = [urllib.parse.urlparse(url) for url in urls]
    urls = list(set([x.scheme + '://' + x.hostname + '/' for x in parsed ]))
    return urls

def getURLs(search_strs):
    urls = []
    for str in search_strs:
        for url in search(str,             # The query you want to run
                          tld='com',       # The top level domain
                          lang='ru',       # The language
                          num=10,          # Number of results per page
                          start=0,         # First result to retrieve
                          stop=10,         # Last result to retrieve
                          pause=2.0,       # Lapse between HTTP requests
        ):
            urls.append(url)
    return urls


def getHTMLPageAsString(url):
    # create headers for http-requests using fake user-agent
    # simple prevention measure against being blocked - to fake a browser visit
    ua = UserAgent()
    request = urllib.request.Request(
        url,
        data=None,
        headers={'User-Agent': ua.google}
        )
    # print(f"type(request) = {type(request)}")

    # urllib.request.urlopen(...) returns object of type: http.client.HTTPResponse
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            raw_data = response.read()
    except timeout:
        raise ValueError('Timeout ERROR')
    except (HTTPError, URLError):
        raise ValueError('Bad Url ERROR')

    # print(f"type(response = {type(response)}")

    status = response.status
    contentType = response.info().get_content_type()
    charset = response.info().get_content_charset()

    if (status != 200):
        raise ValueError('Server returned BAD STATUS code.')
    if (contentType != 'text/html'):
        raise ValueError('contentType is not text/html, handler hasn\'t implemented yet')
    if (charset != 'utf-8'):
        raise ValueError('charset is not utf-8, handler hasn\'t implemented yet')

    # convert bytes to string using the proper charset
    html = raw_data.decode(charset)

    return html


if __name__ == '__main__':
    main()
