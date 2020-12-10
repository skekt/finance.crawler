import pandas as pd
import pymysql
from urllib.request import urlopen
from bs4 import BeautifulSoup

class SearchRankService:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, db='db_finance', user='finance',
                                    password='pwforfinance', charset='utf8')
        self.codes = dict()

    def __del__(self):
        self.conn.close()

    def getSearchRank(self):
        search_rank = []
        company = []

        url = 'https://finance.naver.com/sise/lastsearch2.nhn'
        with urlopen(url) as doc:
            html = BeautifulSoup(doc, 'lxml', from_encoding='ecu-kr')
            _table = html.find('table', class_='type_5')
            _trs = _table.findAll('tr')

            for n in _trs:
                if n.find('td', class_='no'):
                    no = n.find('td', class_='no')
                    link = n.find('a', class_='tltle')

                    search_rank.append(no.get_text())
                    company.append(link.get_text())

            return pd.DataFrame({'ranking': search_rank, 'company': company})

    def setSearchRank(self):
        rankData = self.getSearchRank()

        with self.conn.cursor() as curs:
            for idx in range(len(rankData)):
                ranking = rankData.ranking.values[idx]
                company = rankData.company.values[idx]
                sql = f"INSERT INTO search_ranking (ranking, company) " \
                      f"VALUES ('{ranking}', '{company}')"
                curs.execute(sql)

            self.conn.commit()

if __name__ == '__main__':
    service = SearchRankService()
    service.setSearchRank()
