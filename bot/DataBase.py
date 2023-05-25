import sqlite3

def check_if_db_exists():
    sqlite = sqlite3.connect('sqlite_python.sqlite')
    data = sqlite.cursor()

    try:
        data.execute('SELECT * FROM users')
        data.close()
        return True
    except:
        return False

def create_db():
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.sqlite')
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")

        sqlite_select_query = "SELECT sqlite_version();"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print("Версия базы данных SQLite: ", record)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

def create_tables():
    sqlite = sqlite3.connect('sqlite_python.sqlite')
    data = sqlite.cursor()
    data.execute('CREATE TABLE users (telegramId INTEGER, is_authorized BOOL)')
    sqlite.commit()
    data.close()


def get_user_auth_status(telegramId):
    sqlite = sqlite3.connect('sqlite_python.sqlite')
    data = sqlite.cursor()
    data.execute('SELECT telegramId, is_authorized FROM users WHERE telegramId=?', (telegramId,))
    value = data.fetchone()
    data.close()

    if value is None:
        return False, False
    else:
        return True, value[1]

def add_new_user(telegramId):
    sqlite = sqlite3.connect('sqlite_python.sqlite')
    data = sqlite.cursor()
    data.execute('INSERT INTO users (telegramId, is_authorized) VALUES (?, 0)', (telegramId,))
    sqlite.commit()
    data.close()
    
def set_user_authorized(telegramId):
    sqlite = sqlite3.connect('sqlite_python.sqlite')
    data = sqlite.cursor()
    data.execute('UPDATE users SET is_authorized=1 WHERE telegramId=?', (telegramId,))
    sqlite.commit()
    data.close()
