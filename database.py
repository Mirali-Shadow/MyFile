import sqlite3

# اتصال به پایگاه داده
def connect_db():
    conn = sqlite3.connect('files.db')
    return conn

# ایجاد جدول اگر وجود نداشته باشد
def create_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT NOT NULL,
                file_id TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# افزودن فایل به پایگاه داده
def add_file_to_db(command, file_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO files (command, file_id) VALUES (?, ?)", (command, file_id))
    conn.commit()
    conn.close()

# دریافت لینک فایل از پایگاه داده بر اساس دستور
def get_file_link_from_db(command):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT file_id FROM files WHERE command=?", (command,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
