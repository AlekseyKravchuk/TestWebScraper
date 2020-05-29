class ContactsSpider(scrapy.Spider):

    name = 'contact_info'

    def __init__(self, fileName=None):
        if fileName:
            # TO DO: реализовать функции:
            # 1) из полученных ссылок оставляла только уникальные
            # 2) уникальные ссылки записать в файл
            # 3) содержимое файла со ссылками подать на вход конструктора класса ContactsSpider
            with open(fileName, 'r') as f:
                self.start_urls =

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

        html_text = str(response.text)        mail_list = re.findall('\w+@\w+\.{1}\w+', html_text)

        dic = {'email': mail_list, 'link': str(response.url)}
        df = pd.DataFrame(dic)

        df.to_csv(self.path, mode='a', header=False)
        df.to_csv(self.path, mode='a', header=False)
