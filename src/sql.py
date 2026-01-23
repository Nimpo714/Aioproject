import sqlite3
from time import time

con = sqlite3.connect('data.db')
cursor = con.cursor()

create_tables_scripts = [
    '''CREATE TABLE IF NOT EXISTS admins(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        login_date TEXT
    );''',

    '''CREATE TABLE IF NOT EXISTS questions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quest TEXT,
        ans1 TEXT,
        ans2 TEXT,
        ans3 TEXT,
        ans4 TEXT,
        cor_ans TEXT
    );''',

    '''CREATE TABLE IF NOT EXISTS users_top(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        player_rate REAL DEFAULT 0,  -- REAL для дробных очков
        player_top INTEGER DEFAULT 0,
        played_the_game INTEGER DEFAULT 0, -- Пользователь уже играл?
        start_time REAL DEFAULT 0,    -- Время начала ответов пользователя
        correct_count INTEGER DEFAULT 0 -- Кол-во верных ответов
    );''',

    '''CREATE TABLE IF NOT EXISTS game_data(
        is_active INTEGER DEFAULT 0,  -- 1 если игра идет, 0 если закрыта
        is_closed INTEGER DEFAULT 0
    );''',

    '''CREATE TABLE IF NOT EXISTS promocodes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        promo TEXT
    );'''
]

for table in create_tables_scripts:  # -- Запускаем скрипты
    cursor.execute(table)
    con.commit()

cursor.execute("INSERT INTO game_data (is_active, is_closed) SELECT 0, 0 WHERE NOT EXISTS (SELECT 1 FROM game_data)")
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
    cursor.execute(f"SELECT chat_id FROM {table} WHERE chat_id = ?", [id])
    result = cursor.fetchone()
    if result is None:
        return False
    return True

def top(first_top: int = 10):
    cursor.execute(""" SELECT chat_id FROM users_top WHERE player_top < ? """, [first_top])
    return cursor.fetchall()


def drop_statistic():
    """ Обнуляет топ игроков с сохранением параметров chat_id """
    cursor.execute("""
UPDATE users_top SET 
    player_rate = 0, 
    player_top = 0, 
    start_time = 0, 
    correct_count = 0, 
    played_the_game = 0;
 """)


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
    """ Возращаем вопрос <quest_id> """
    cursor.execute('SELECT quest FROM questions WHERE id = ?', [quest_id])
    return cursor.fetchone()


def select_from_quest(quest_id: int, select: str = '*'):
    """ Возращаем {select} из вопроса <quest_id> """
    cursor.execute(f'SELECT {select} FROM questions WHERE id = ?', [quest_id])
    return cursor.fetchone()


def set_quest(quest_text: str, quest_ans: list, cor_ans: str):
    cursor.execute('''
        INSERT INTO questions (quest, ans1, ans2, ans3, ans4, cor_ans) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', [quest_text, quest_ans[0], quest_ans[1], quest_ans[2], quest_ans[3], cor_ans])
    con.commit()


def clear_questions_table():
    """ Очищает таблицу с вопросами """
    cursor.executescript("DELETE FROM questions; UPDATE sqlite_sequence SET seq = 0 WHERE name = 'questions'")
    con.commit()


def set_game_status(active: int):
    """ Устанавливает игровой статус """
    cursor.execute("UPDATE game_data SET is_active = ?", [1 if active else 0])
    con.commit()

def admin_closed_game(active: bool):
    """ Включает или выключает возможность закрытие игры """
    cursor.execute("UPDATE game_data SET is_closed = ? VALUES(?)", [active])
    con.commit()


def is_game_open():
    """ Проверяет, можно ли сейчас играть """
    cursor.execute("SELECT is_active FROM game_data")
    result = cursor.fetchone()
    return result is not None and result[0] == 1


def is_admin_closed_game():
    """ Проверяет, можно ли сейчас играть """
    cursor.execute("SELECT is_closed FROM game_data")
    result = cursor.fetchone()
    return result is not None and result[0] == 1

def played_the_game(chat_id: int):
    """ Проверка, играл ли пользователь уже в игру """
    cursor.execute("SELECT played_the_game FROM users_top WHERE chat_id = ?", [chat_id])
    result = cursor.fetchone()

    if result:
        # Если запись есть, проверяем флаг (1 - играл, 0 - еще нет)
        is_played = result[0] 
        if is_played:
            return True
        else:
            return False
    else:
        # Если записи нет совсем — добавляем пользователя
        add_user(chat_id)
        return False


def start_user_timer(user_id: int):
    """ Фиксирует время начала теста для пользователя """
    current_time = time()
    cursor.execute("UPDATE users_top SET start_time = ?, correct_count = 0 WHERE chat_id = ?", [current_time, user_id])
    con.commit()


def add_correct_answer(user_id: int):
    """ Увеличивает счетчик правильных ответов """
    cursor.execute("UPDATE users_top SET correct_count = correct_count + 1 WHERE chat_id = ?", (user_id,))
    con.commit()


def finish_user_game(user_id: int):
    """ Рассчитывает финальный рейтинг: Очки / (Текущее_время - Время_начала) """
    cursor.execute("SELECT start_time, correct_count FROM users_top WHERE chat_id = ?", (user_id,))
    data = cursor.fetchone()

    if data and data[0] > 0:
        start_time = data[0]
        corrects = data[1]
        total_time = time() - start_time

        # Избегаем деления на ноль, если ответил мгновенно
        if total_time < 1: total_time = 1

        # Формула: Правильные ответы / потраченное время
        new_rate = round(corrects / total_time, 4)

        cursor.execute("UPDATE users_top SET player_rate = ? WHERE chat_id = ?", (new_rate, user_id))
        con.commit()
        update_player_top_position()
        return new_rate
    return 0


def clear_promo_code():
    """ Очищает таблицу с промо-кодами """
    cursor.executescript("DELETE FROM promocodes; UPDATE sqlite_sequence SET seq = 0 WHERE name = 'promocodes'")
    con.commit()


def add_promo_code(promo_code: str):
    """ Добавляет промокод """
    cursor.execute("INSERT INTO promocodes (promo) VALUES (?)", [promo_code])
    con.commit()