import pandas as pd
import pymysql
from datetime import datetime

class DBUpdater:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, db='db_finance', user='finance', password='pwforfinance', charset='utf8')
        self.codes = dict()

    def __del__(self):
        self.conn.close()

    def read_krx_code(self):
        """한국거래소 상장기업 목록"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드', '회사명']]
        krx = krx.rename(columns={'종목코드':'code', '회사명':'company'})
        krx.code = krx.code.map('{:06d}'.format)
        print(krx)

        return krx

    def update_company_info(self):
        sql = "select * from company_info"
        df = pd.read_sql(sql, self.conn)
        print(df)

        for idx in range(len(df)):
            self.codes[df['code'].values[idx]] = df['company'].values[idx]

        with self.conn.cursor() as curs:
            sql = "select max(updated_at) from company_info"
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')

            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:
                krx = self.read_krx_code()
                for idx in range(len(krx)):
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]
                    sql = f"REPLACE INTO company_info (code, company, updated_at) " \
                          f"VALUES ('{code}', '{company}', '{today}')"
                    curs.execute(sql)
                    self.codes[code] = company
                    print(sql)
                self.conn.commit()

if __name__ == '__main__':
    dbu = DBUpdater()
    # dbu.read_krx_code()
    dbu.update_company_info()
