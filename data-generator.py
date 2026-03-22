import mysql.connector
import os
import logging

def generate_logs(day):
    return []

connection = None
try:
    connection = mysql.connector.connect(host='mysql', user='root', password=os.getenv('ROOT_PASSWORD'),
                                         database='user_logs', port=os.getenv('DATABASE_PORT'))
    logging.error("Генератор данных подключен к базе данных")
except mysql.connector.Error as e:
    logging.error(f"Генератору данных не удалось подключиться к базе данных: {e}")

insert_query = ("""INSERT INTO log (user_id, event_id, description, forum_id, status, time)
                VALUES (%s, %s, %s, %s, %s, %s)""")
days = 31
for i in range(1, days + 1):
    logs = generate_logs(i)
    cursor = connection.cursor()
    for log in logs:
        cursor.execute(query, (log['user_id'], log['event_id'], log['desc'], log['forum_id'], log['status'], log['time']))
    connection.commit()
    logging.error(f"Созданы логи за {i} день")
connection.close()
logging.error("Создание логов завершено")
