from googlesearch import search

for url in search('Sony 16-35mm f2.8 GM lens', tld='com', stop=10):
    print(type(search))
