import mysql.connector
import os
import logging
from datetime import datetime
from random import randint
import numpy as np

def generate_event_amounts():
    events = [1, 2, 3, 4, 5, 6, 7, 8]
    repeats = []
    for _ in events:
        repeats.append(randint(5, 20))
    events = np.repeat(events, repeats)
    return events.tolist()

def generate_logs(day, max_forum_id, max_user_id):
    logs = []
    events = generate_event_amounts()
    no_login_error_amount = 2
    for event_id in events:
        desc = ''
        forum_id = randint(10000, max_forum_id)
        user_id = randint(100000, max_user_id)
        status = 'success'
        match event_id:
            case 1:
                user_id = None
                forum_id = None
                desc = 'Новый пользователь зашел на сайт'
            case 2:
                forum_id = None
                max_user_id += 1
                user_id = max_user_id
                desc = f'Пользователь {user_id} зарегистрировался'
            case 3:
                forum_id = None
                desc = f'Пользователь {user_id} вошел в аккаунт'
            case 4:
                forum_id = None
                desc = f'Пользователь {user_id} вышел из аккаунта'
            case 5:
                max_forum_id += 1
                forum_id = max_forum_id
                if randint(1, 10) <= 4:
                    user_id = None
                if no_login_error_amount > 0:
                    user_id = None
                    no_login_error_amount -= 1
                desc = f'Пользователь {user_id} создал тему {forum_id}'
                if user_id is None:
                    status = 'error'
                    desc = f'Пользователю не удалось создать тему'
                    max_forum_id -= 1
                    forum_id = None
            case 6:
                if randint(1, 10) <= 4:
                    user_id = None
                desc = f'Пользователь {user_id} зашел на тему {forum_id}'
                if user_id is None:
                    desc = f'Анонимный пользователь зашел на тему {forum_id}'
            case 7:
                desc = f'Пользователь {user_id} удалил тему {forum_id}'
            case 8:
                if randint(1, 10) <= 5:
                    user_id = None
                desc = f'Пользователь {user_id} написал сообщение в тему {forum_id}'
                if user_id is None:
                    desc = f'Анонимный пользователь написал сообщение в тему {forum_id}'
        logs.append({
            'user_id': user_id,
            'event_id': event_id,
            'desc': desc,
            'forum_id': forum_id,
            'status': status,
            'time': datetime(2026, 1, day, randint(0, 23), randint(0, 59), randint(0, 59))
        })
    return logs, max_forum_id, max_user_id

def main():
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
    max_forum_id = 50000
    max_user_id = 500000
    for i in range(1, days + 1):
        logs, max_forum_id, max_user_id = generate_logs(i, max_forum_id, max_user_id)
        cursor = connection.cursor()
        for log in logs:
            cursor.execute(insert_query, (log['user_id'], log['event_id'], log['desc'], log['forum_id'], log['status'], log['time']))
        connection.commit()
        logging.error(f"Созданы логи за {i} день")
    connection.close()
    logging.error("Создание логов завершено")

if __name__ == '__main__':
    main()
