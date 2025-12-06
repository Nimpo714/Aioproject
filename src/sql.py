import sqlite3
from time import time

con = sqlite3.connect('data.db')
cursor = con.cursor()

create_tables_scripts = ['''
CREATE TABLE IF NOT EXISTS top(
    user_id INTEGER,
    player_rate INTEGER,
    player_top INTEGER
);''',
                         '''
CREATE TABLE IF NOT EXISTS admins(
    user_id INTEGER,
    login_date TEXT
);''',
                         '''
CREATE TABLE IF NOT EXISTS questions(
    questions TEXT,
    right_question TEXT
);'''
                         ]

for table in create_tables_scripts:  # -- Запускаем скрипты
    cursor.execute(table)
    con.commit()


def add_user(id: int):
    """ Добавляет игрока в турнирную таблицу """
    # -- user_id, player_rate, player_top
    cursor.execute(f'INSERT INTO top VALUES ({id}, 0, 0);')
    con.commit()


def update_player_rate(user_id: int, new_rate: int):
    """ Обновляет рейтинг игрока """
    cursor.execute(f'UPDATE top SET player_rate = {new_rate} WHERE user_id = {user_id};')
    con.commit()
    update_player_top_position()


def update_player_top_position():
    """ 
    Обновляет столбец top для всех пользователей, 
    присваивая им актуальное место в рейтинге.
    """
    sql_update_top_script = '''
    UPDATE top 
    SET top = Ranked.rank
    FROM (
        SELECT 
            user_id, 
            RANK() OVER (ORDER BY player_rate DESC) as rank
        FROM 
            top
    ) AS Ranked
    WHERE 
        top.user_id = Ranked.user_id;
    '''
    cursor.execute(sql_update_top_script)
    """
    id:122, rate:10 | id:123, rate:9  | id:124, rate:10 
    id:123, rate:9  | id:124, rate:10 | id:123, rate:9
    """
    con.commit()


def top(first_top: int = 10):
    cursor.execute(f""" SELECT * FROM top WHERE player_top < {first_top} """)
    return cursor.fetchall()


def add_admin(id: int):
    """ Добавляет админов """
    try:
        cursor.execute('INSERT INTO admins VALUES (?, ?)', (id, str(time())))
        con.commit()
        return f'Админ {id} был добавлен'

    except sqlite3.IntegrityError:
        return 'Админ уже есть!'


def search_admin(id: int):
    """ Поиск админа по базе """
    cursor.execute('SELECT * FROM admins WHERE user_id = ?', (id,))
    return cursor.fetchone()
