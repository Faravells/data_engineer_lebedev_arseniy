import mysql.connector
import os
import logging
import pandas as pd
from datetime import datetime

def main():
    connection = None
    try:
        connection = mysql.connector.connect(host='mysql', user='root', password=os.getenv('ROOT_PASSWORD'),
                                             database='user_logs', port=os.getenv('DATABASE_PORT'))
        logging.error("Агрегатор данных подключен к базе данных")
    except mysql.connector.Error as e:
        logging.error(f"Агрегатору данных не удалось подключиться к базе данных: {e}")
    
    with open("date-interval.txt", "r") as f:
        #доверяем, что пользователь вводит корректный формат dd.mm.yy-dd.mm.yy с корректными данными
        date_start, date_end = f.readline().split('-')
    date_start = datetime.strptime(date_start, "%d.%m.%Y")
    date_end = datetime.strptime(date_end.strip(), "%d.%m.%Y")
    query1 = """SELECT DATE(time) AS day, COUNT(log_id) AS new_account_amount
                FROM log
                WHERE event_id = 2 AND status = 'success'
                GROUP BY day
                HAVING day BETWEEN %s AND %s"""
    query2 = """SELECT DATE(time) AS day, COUNT(log_id) AS messages_amount,
                    ROUND(COUNT(IF(user_id IS NULL, 1, NULL)) / COUNT(log_id) * 100, 2) AS anon_messages_percentage
                FROM log
                WHERE event_id = 8 AND status = 'success'
                GROUP BY day
                HAVING day BETWEEN %s AND %s"""
    query3 = """SELECT DATE(time) AS day, COUNT(IF(event_id = 5 AND status = 'success', 1, NULL)) -
                    COUNT(IF(event_id = 7 AND status = 'success', 1, NULL)) AS daily_forum_gain
                FROM log
                GROUP BY day"""
    cursor = connection.cursor()
    cursor.execute(query1, (date_start, date_end))
    df1 = pd.DataFrame(cursor.fetchall(), columns=['День', 'Количество созданных новых аккаунтов'])
    cursor.execute(query2, (date_start, date_end))
    df2 = pd.DataFrame(cursor.fetchall(), columns=['День', 'Количество сообщений всего',
                                                   'Количество написанных анонимами сообщений в процентах от всех сообщений'])
    cursor.execute(query3)
    df3 = pd.DataFrame(cursor.fetchall(), columns=['День', 'daily_forum_gain'])
    result = pd.merge(df1, df2, on='День', how='outer')
    cursor.close()
    connection.close()
    
    days = 31
    min_forum_amount = 10000 #кол-во тем до начала записи логов
    forum_amount = [min_forum_amount + df3['daily_forum_gain'][0]]
    for i in range(1, days):
        forum_amount.append(forum_amount[i - 1] + df3['daily_forum_gain'][i])
    df3['forum_amount'] = forum_amount
    df3['Процентное изменение количества тем на форуме относительно предыдущего дня'] = round(df3['daily_forum_gain'] / df3['forum_amount'] * 100, 2)
    df3.drop(columns=['daily_forum_gain', 'forum_amount'], inplace=True)
    df3 = df3[(df3['День'] >= date_start.date()) & (df3['День'] <= date_end.date())]
    result = result.merge(df3, on='День', how='outer')
    result['День'] = pd.to_datetime(result['День']).dt.strftime('%d.%m.%Y')
    
    pd.DataFrame(result).to_csv("output.csv", index=False, encoding='utf-8-sig')
    logging.error(f"{len(result)} строк успешно экспортировано в выходной файл")

if __name__ == '__main__':
    main()
