import pandas as pd
import pymysql
from datetime import datetime

def get_search_rankins(query):
    # DB Connection
    conn = pymysql.connect(host='localhost', port=3306, db='db_finance', user='finance',
                                password='pwforfinance', charset='utf8')

    # Get a DataFrame
    global query_result
    query_result = pd.read_sql(query, conn)

    # Close connection
    conn.close()

    return query_result

def showGraph(rankings):
    import matplotlib.pyplot as plt

    print(rankings)
    # print(rankings.company)
    # print(f"Distinct entries: {rankings.groupby(['company'])}")

    companies = rankings['company'].unique();
    print(companies)

    company1 = rankings[rankings.company.eq('메디톡스')]
    company2 = rankings[rankings.company.eq('대웅')]
    company3 = rankings[rankings.company.eq('NAVER')]
    print(company1)
    print(company2)
    print(company3)

    # print(company1.group_id)
    # print(company1.ranking)

    # graph_data = {'a': company1.ranking, 'b': company2.ranking}
    # df = pd.DataFrame(graph_data, index=company1.group_id)
    # df.plot()

    # graph_data = {'a': company1.ranking}
    # df = pd.DataFrame(graph_data)

    # graph_data = {'a': company1.ranking, 'b': company2.ranking}
    # df = pd.DataFrame(graph_data, index=company1.group_id)

    # print(df)
    # df.plot()

    plt.title("Search Ranking")
    # plt.plot(df['a'], 'ro--')
    # plt.plot(df.index, df.a, 'bs--', label='a')
    plt.plot(company1.group_id, company1.ranking, 'bs--', label='a')
    plt.plot(company2.group_id, company2.ranking, 'rs--', label='b')
    plt.plot(company3.group_id, company3.ranking, 'gs--', label='c')

    # plt.plot(df['b'], 'bo--')
    # plt.xticks(company1.group_id)
    # plt.yticks(company1.ranking)
    plt.grid(True)
    plt.legend(loc='best')
    plt.show()


sql = f"select group_id, company, ranking " \
      f"  from search_ranking " \
      f" where created_at >= '2020-12-17 12:00'" \
      f"   and created_at < '2020-12-17 14:00'" \

rankings = get_search_rankins(sql)

showGraph(rankings)
