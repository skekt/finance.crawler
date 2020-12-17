import pymysql
import pandas as pd

connection = pymysql.connect(host='localhost', port=3306, db='db_finance', autocommit=True,
    user='finance', passwd='pwforfinance')

cursor = connection.cursor()
cursor.execute("SELECT VERSION();")
result = cursor.fetchone()
print("MariaDB version: {}".format(result))

cursor.execute("SELECT count(*) from search_ranking;")
result = cursor.fetchone()
print("count of search_rank: {}".format(result))

cursor.execute("SELECT ranking, company from search_ranking where group_id = 54 order by 1;")
result = cursor.fetchall()
print(result)

df = pd.DataFrame(result)
print(result)

ret = dict(map(reversed, result))
print(ret)

company = '신풍제약'
if ret.get(company):
    print('exists')
    print(ret.get(company))
else:
    print('not exists')


connection.close()