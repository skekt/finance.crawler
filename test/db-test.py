import pymysql

connection = pymysql.connect(host='localhost', port=3306, db='db_finance', autocommit=True,
    user='finance', passwd='pwforfinance')

cursor = connection.cursor()
cursor.execute("SELECT VERSION();")
result = cursor.fetchone()
print("MariaDB version: {}".format(result))

cursor.execute("SELECT count(*) from search_rank;")
result = cursor.fetchone()
print("count of search_rank: {}".format(result))

connection.close()