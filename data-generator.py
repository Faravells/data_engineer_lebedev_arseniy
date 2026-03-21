import mysql.connector
import os

connection = None
try:
    connection = mysql.connector.connect(host='mysql', user='root', password=os.getenv('ROOT_PASSWORD'),
                                         database='user_logs', port=os.getenv('DATABASE_PORT'))
    print("Генератор данных подключен к базе данных")
except mysql.connector.Error as e:
    print(f"Генератору данных не удалось подключиться к базе данных: {e}")
