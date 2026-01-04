import sqlite3
from time import time

con = sqlite3.connect('data.db')
cursor = con.cursor()

create_tables_scripts = ['''
CREATE TABLE IF NOT EXISTS users_top(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    player_rate INTEGER,
    player_top INTEGER
);''',
                         '''
CREATE TABLE IF NOT EXISTS admins(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER,
    login_date TEXT
);''',
                         '''
CREATE TABLE IF NOT EXISTS questions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quest TEXT,
    ans1 TEXT,
    ans2 TEXT,
    ans3 TEXT,
    ans4 TEXT,
    cor_ans TEXT
);''']

for table in create_tables_scripts:  # -- Запускаем скрипты
    cursor.execute(table)
    con.commit()


def add_user(id: int):
    """ Добавляет игрока в турнирную таблицу """
    # -- user_id, player_rate, player_top
    cursor.execute('INSERT INTO users_top (chat_id, player_rate, player_top) VALUES (?, 0, 0);', [id])
    con.commit()
    update_player_top_position()


def update_player_rate(user_id: int, new_rate: int):
    """ Обновляет рейтинг игрока """
    cursor.execute('UPDATE users_top SET player_rate = ? WHERE user_id = ?;', [new_rate, user_id])
    con.commit()
    update_player_top_position()


def update_player_top_position():
    """ 
    Обновляет столбец users_top для всех пользователей,
    присваивая им актуальное место в рейтинге.
    """
    sql_update_top_script = '''
    UPDATE users_top 
    SET player_top = Ranked.rank
    FROM (
        SELECT 
            chat_id, 
            RANK() OVER (ORDER BY player_rate DESC) as rank
        FROM 
            users_top
    ) AS Ranked
    WHERE 
        users_top.chat_id = Ranked.chat_id;
    '''
    cursor.execute(sql_update_top_script)
    """
    id:122, rate:10 | id:123, rate:9  | id:124, rate:10 
    id:123, rate:9  | id:124, rate:10 | id:123, rate:9
    """
    con.commit()


def user_in_table(id: int, table: str):
    """ Пользователь в топе или нет? """
    cursor.execute(f'SELECT chat_id FROM {table} WHERE chat_id = ?', [id])
    if cursor.fetchone() is []:
        return False


def top(first_top: int = 10):
    cursor.execute(""" SELECT * FROM top WHERE player_top < ? """, [first_top])
    return cursor.fetchall()


def add_admin(id: int):
    """ Добавляет админов """
    try:
        cursor.execute('INSERT INTO admins (chat_id, login_date) VALUES (?, ?)', (id, str(time())))
        con.commit()
        return f'Админ {id} был добавлен'

    except sqlite3.IntegrityError:
        return 'Админ уже есть!'


def search_admin(id: int):
    """ Поиск админа по базе """
    cursor.execute('SELECT * FROM admins WHERE user_id = ?', (id,))
    return cursor.fetchone()


def quest(quest_id: int):
    """ Возращаем ответ на вопрос <quest_id> """
    cursor.execute('SELECT quest FROM questions WHERE id = ?', [quest_id])
    return cursor.fetchone()


def set_quest(quest_text: str, quest_ans: list, cor_ans: str):
    cursor.execute('''
        INSERT INTO questions (quest, ans1, ans2, ans3, ans4, cor_ans) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', [quest_text, quest_ans[0], quest_ans[1], quest_ans[2], quest_ans[3], cor_ans])
    con.commit()


def clear_questions_table():
    cursor.executescript("DELETE FROM questions; UPDATE sqlite_sequence SET seq = 0 WHERE name = 'questions'")
    con.commit()