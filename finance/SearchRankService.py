import pandas as pd
import pymysql
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from threading import Timer

class SearchRankService:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, db='db_finance', user='finance',
                                    password='pwforfinance', charset='utf8')
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

                    search_rank.append(int(no.get_text()))
                    company.append(link.get_text())

            return pd.DataFrame({'ranking': search_rank, 'company': company})

    def setSearchRank(self):
        tnow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rankData = self.getSearchRank()

        with self.conn.cursor() as curs:
            curs.execute("select ifnull(max(group_id), 0) + 1 from search_ranking;")
            group_id = curs.fetchone()[0]
            print(f'[{tnow}] Search ranking update start. (groupId: {group_id})')

            curs.execute(f'SELECT ranking, company from search_ranking where group_id = {group_id - 1};')
            current_ranking = dict(map(reversed, curs.fetchall()))

            print(current_ranking)

            for idx in range(len(rankData)):
                ranking = rankData.ranking.values[idx]
                company = rankData.company.values[idx]
                step = 0

                if current_ranking.get(company):
                    step = current_ranking.get(company) - ranking
                    print(f'{company} before: {current_ranking.get(company)}, after: {ranking}, step: {step}')

                sql = f"INSERT INTO search_ranking (group_id, ranking, company, step) " \
                      f"VALUES ('{group_id}', '{ranking}', '{company}', '{step}')"
                curs.execute(sql)

            self.conn.commit()

            tnow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f'[{tnow}] Search ranking update finish.')

            # t = Timer(60*5, self.setSearchRank)
            # t.start()

if __name__ == '__main__':
    service = SearchRankService()
    service.setSearchRank()
