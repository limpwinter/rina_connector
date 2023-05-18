import sqlite3

def CheckIfDBExists():
    sqlite = sqlite3.connect('sqlite_python.sqlite')
    data = sqlite.cursor()

    try:
        data.execute('SELECT * FROM users')
        data.close()
        return True
    except:
        return False

def CreateDB():
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

def CreateTables():
    sqlite = sqlite3.connect('sqlite_python.sqlite')
    data = sqlite.cursor()
    data.execute('CREATE TABLE users (telegramId INTEGER, is_authorized BOOL)')
    sqlite.commit()
    data.close()


def UserRegCheck(telegramId):
    sqlite = sqlite3.connect('sqlite_python.sqlite')
    data = sqlite.cursor()
    data.execute('SELECT telegramId FROM users')
    value = data.fetchall()
    data.close()

    # Превращаем "Список кортежей" в список.
    value = [x[0] for x in value]
    if telegramId in value:
        return True
    else:
        return False

def InsertUser(telegramId, is_authorized):
    sqlite = sqlite3.connect('sqlite_python.sqlite')
    data = sqlite.cursor()
    data.execute('INSERT INTO users (telegramId, is_authorized) VALUES (?,?)', (telegramId, is_authorized))
    sqlite.commit()
    data.close()