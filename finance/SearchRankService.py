import pandas as pd
import pymysql
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from threading import Timer
from slacker import Slacker


class SearchRankService:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, db='db_finance', user='finance',
                                    password='pwforfinance', charset='utf8')

        self.slack = Slacker('xoxb-1550934577952-1527246562034-zU9UVbkjV15KZQVF5hsWcFkO')

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
        ranking_data = self.getSearchRank()

        with self.conn.cursor() as curs:
            curs.execute("select ifnull(max(group_id), 0) + 1 from search_ranking;")
            group_id = curs.fetchone()[0]
            print(f'[{tnow}] Search ranking update start. (groupId: {group_id})')

            curs.execute(f'SELECT ranking, company from search_ranking where group_id = {group_id - 1};')
            ranking_asis = dict(map(reversed, curs.fetchall()))

            # 급등 / 급락
            rise_up_company = []
            fall_down_company = []

            for idx in range(len(ranking_data)):
                ranking = ranking_data.ranking.values[idx]
                company = ranking_data.company.values[idx]
                step = 0

                if ranking_asis.get(company):
                    step = ranking_asis.get(company) - ranking

                print(f'{ranking}. {company} (before ranking: {ranking_asis.get(company)}, step: {step})')

                sql = f"INSERT INTO search_ranking (group_id, ranking, company, step) " \
                      f"VALUES ('{group_id}', '{ranking}', '{company}', '{step}')"
                curs.execute(sql)

                if step > 3:
                    rise_up_company.append(company)

                if step < -3:
                    fall_down_company.append(company)

        self.conn.commit()

        tnow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{tnow}] Search ranking update finish.', flush=True)

        rise_up_text = '*급등*'
        for i in rise_up_company:
            rise_up_text += '`' + i + '`'
            rise_up_text += ' '

        fall_down_text = '*급락*'
        for i in fall_down_company:
            fall_down_text += '`' + i + '`'
            fall_down_text += ' '

        if len(rise_up_company) > 0:
            self.slack.chat.post_message(channel="#info", text=rise_up_text)

        if len(fall_down_company) > 0:
            self.slack.chat.post_message(channel="#info", text=fall_down_text)

        t = Timer(60 * 5, self.setSearchRank)
        # t.start()


if __name__ == '__main__':
    service = SearchRankService()
    service.setSearchRank()
