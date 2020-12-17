import pandas as pd
import pymysql
from datetime import datetime

def get_search_rankins(query):
    # DB Connection
    conn = pymysql.connect(host='localhost', port=3306, db='db_finance', user='finance',
                                password='pwforfinance', charset='utf8')

    # start time
    start_tm = datetime.now()

    # Get a DataFrame
    global query_result

    query_result = pd.read_sql(query, conn)

    # Close connection
    end_tm = datetime.now()

    print('START TIME : ', str(start_tm))
    print('END TIME : ', str(end_tm))
    print('ELAP time :', str(end_tm - start_tm))
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
    print(company1)
    print(company2)

    # print(company1.group_id)
    # print(company1.ranking)

    # graph_data = {'a': company1.ranking, 'b': company2.ranking}
    # df = pd.DataFrame(graph_data, index=company1.group_id)
    # df.plot()

    graph_data = {'a': company1.ranking}
    df = pd.DataFrame(graph_data)

    # graph_data = {'a': company1.ranking, 'b': company2.ranking}
    # df = pd.DataFrame(graph_data, index=company1.group_id)

    print(df)
    df.plot()

    plt.title("Search Ranking")
    plt.plot(df['a'], 'ro--')
    # plt.plot(df['b'], 'bo--')
    # plt.xticks(company1.group_id)
    # plt.yticks(company1.ranking)
    plt.grid(True)
    plt.show()


sql = f"select group_id, company, ranking " \
      f"from search_ranking where created_at >= '2020-12-17' "

rankings = get_search_rankins(sql)

showGraph(rankings)
