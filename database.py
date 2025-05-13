import sqlite3

DB_NAME = "vacancies.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            city TEXT,
            salary TEXT,
            url TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_vacancies(vacancies):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    for v in vacancies:
        try:
            c.execute("INSERT INTO vacancies (title, company, city, salary, url) VALUES (?, ?, ?, ?, ?)",
                      (v["title"], v["company"], v["city"], v["salary"], v["url"]))
        except Exception as e:
            print(f"Ошибка при сохранении вакансии: {e}")
    conn.commit()
    conn.close()


def clear_vacancies():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM vacancies")
    conn.commit()
    conn.close()
    print("🧹 Все вакансии удалены")


def get_saved_vacancies():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT title, company, city, salary, url FROM vacancies")
    results = c.fetchall()
    conn.close()
    return results