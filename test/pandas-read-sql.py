def get_search_rankins(query):
    import pandas as pd
    import pymysql
    from datetime import datetime

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
    print(rankings.company)
    # plt.title("Search Ranking")
    # plt.plot(rankings, 'bs--')
    # plt.xticks(rankings.index)
    # plt.yticks(rankings.values)
    # plt.grid(True)
    # plt.show()


sql = f"select group_id, company, ranking " \
      f"from search_ranking where created_at >= '2020-12-15' "\
      f"group by group_id, company, ranking"

rankings = get_search_rankins(sql)

showGraph(rankings)
