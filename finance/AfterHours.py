import datetime
import pymysql
import requests
from threading import Timer

class AfterHours:
    def __init__(self):
        print('AfterHours init.')
    def __del__(self):
        print('AfterHours end.')

    def fire(self):
        self.conn = pymysql.connect(host='localhost', port=3306, db='db_finance', user='finance', password='pwforfinance', charset='utf8')

        print(f'Crawling Started at {datetime.datetime.now()}')
        self.setRankOfAfterHours('KOSPI')
        self.setRankOfAfterHours('KOSDAQ')
        print(f'Crawling Ended at {datetime.datetime.now()}')

        self.conn.close()

        # Per 24H
        t = Timer(60 * 60 * 24, self.fire)
        t.start()        

    def setRankOfAfterHours(self, market):
        headers = {'authority': 'finance.daum.net','sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"','accept': 'application/json, text/javascript, */*; q=0.01','x-requested-with': 'XMLHttpRequest','sec-ch-ua-mobile': '?0','user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36','sec-ch-ua-platform': '"macOS"','sec-fetch-site': 'same-origin','sec-fetch-mode': 'cors','sec-fetch-dest': 'empty','referer': 'https://finance.daum.net/domestic/after_hours?market=KOSPI','accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}
        url = f'https://finance.daum.net/api/trend/after_hours_spac?page=1&perPage=30&fieldName=changeRate&order=desc&market={market}&type=CHANGE_RISE&pagination=true'
        res = requests.get(url,headers=headers)
        # print(f'Response Data\n{res.text}')

        datas = res.json()['data']
        print(len(datas))
        # print(datas[0])

        with self.conn.cursor() as curs:
            for idx in range(len(datas)):
                row = datas[idx]
                print(row)

                rank = row.get("rank")
                name = row.get("name")
                symbolCode = row.get("symbolCode")
                code = row.get("code")
                tradePrice = row.get("tradePrice")
                changeRate = row.get("changeRate")
                accTradeVolume = row.get("accTradeVolume")
                regularHoursTradePrice = row.get("regularHoursTradePrice")
                regularHoursChange = row.get("regularHoursChange")
                regularHoursChangeRate   = row.get("regularHoursChangeRate")

                sql = f"insert into after_hours (" \
                        f"market," \
                        f"rank," \
                        f"name," \
                        f"symbolCode," \
                        f"code," \
                        f"tradePrice," \
                        f"changeRate," \
                        f"accTradeVolume," \
                        f"regularHoursTradePrice," \
                        f"regularHoursChange," \
                        f"regularHoursChangeRate" \
                        f") values (" \
                        f"'{market}'," \
                        f"'{rank}'," \
                        f"'{name}'," \
                        f"'{symbolCode}'," \
                        f"'{code}'," \
                        f"'{tradePrice}'," \
                        f"'{changeRate}'," \
                        f"'{accTradeVolume}'," \
                        f"'{regularHoursTradePrice}'," \
                        f"'{regularHoursChange}'," \
                        f"'{regularHoursChangeRate}'" \
                        f")"
                curs.execute(sql)
        self.conn.commit()

if __name__ == '__main__':
    service = AfterHours()
    service.fire()
