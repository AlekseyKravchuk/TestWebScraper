from googlesearch import search
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from importlib import import_module

libNames = ['yaml', 'os', 'urllib', 're']

for libname in libNames:
    try:
        lib = import_module(libname)
    except ImportError as err:
        print('Error:', err)
    else:
        globals()[libname] = lib


def main():
    # #################### Step 1. Getting the URLs using Google search engine ####################
    # file name to extract search strings from
    with open(r'scraper-conf.yaml') as f:
        env = yaml.load(f, Loader=yaml.FullLoader)

    fileName = env['fileNameWithSearchStrings']
    search_strs = getSearchStrings(fileName)

    # extract base URLs and store only unique ones
    urls = getBaseUrls(getURLs(search_strs))

    # url = urls[5]  # URL to test:
    url = "https://sprint5.ru/"
    print(f"\ncurrent url to test: {url}")
    html = getHTMLPageAsString(url)

    # #################### Step 2. Parsing the URLs ####################

    # use regular expression from scraper-conf.yaml configuration file
    combined_mails_re = '|'.join(env['regexp_mails'])
    emails_matches = re.findall(combined_mails_re, html)
    emails = set(emails_matches)

    combined_phones_re = '|'.join(env['regexp_phones'])
    phone_matches = re.findall(combined_phones_re, html)
    phones = set(phone_matches)

    print("EMAILS:")
    for mail in emails:
        print(f"\t{mail}")

    print("PHONES:")
    for phone in phones:
        print(f"\t{phone}")

    # extract all the <a> tags from page(string) html
    soup = BeautifulSoup(html, "html.parser")
    links = []
    tags = soup.find_all('a')
    accepted_strings = {'Контакты', 'О компании'}

    for tag in tags:
        if tag.text in env['contact_patterns']:
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
        while True:
            line = f.readline()
            if not line:
                break
            if line != '\n':
                requests.append(line)
    return requests


def getBaseUrls(urls):
    # Parse a URL into six components, returning a 6-item named tuple.
    parsed = [urllib.parse.urlparse(url) for url in urls]
    urls = list(set([x.scheme + '://' + x.hostname + '/' for x in parsed]))
    return urls


def getURLs(search_strs):
    urls = []
    for str in search_strs:
        for url in search(str,  # The query you want to run
                          tld='com',  # The top level domain
                          lang='ru',  # The language
                          num=10,  # Number of results per page
                          start=0,  # First result to retrieve
                          stop=10,  # Last result to retrieve
                          pause=2.0,  # Lapse between HTTP requests
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
