from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'https://finance.naver.com/sise/lastsearch2.nhn'
with urlopen(url) as doc:
    html = BeautifulSoup(doc, 'lxml', from_encoding='ecu-kr')
    _table = html.find('table', class_='type_5')
    _trs = _table.findAll('tr')

    for n in _trs:
        if n.find('td', class_='no'):
            no = n.find('td', class_='no')
            link = n.find('a', class_='tltle')
            print('{}. {}'.format(no.get_text(), link.get_text()))
            # print(no.get_text() + ' ' + link.get_text())
