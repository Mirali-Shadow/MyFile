import sqlite3

# اتصال به دیتابیس و ایجاد جدول (اگر وجود نداشته باشد)
def initialize_database():
    connection = sqlite3.connect('bot_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- شناسه یکتا
            file_id TEXT NOT NULL,                 -- آیدی فایل
            file_name TEXT NOT NULL,               -- نام فایل
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- تاریخ ایجاد
        )
    ''')
    connection.commit()
    connection.close()

# افزودن فایل به دیتابیس
def add_file(file_id, file_name):
    connection = sqlite3.connect('bot_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO files (file_id, file_name)
        VALUES (?, ?)
    ''', (file_id, file_name))
    connection.commit()
    connection.close()

# دریافت آیدی فایل بر اساس نام فایل
def get_file(file_name):
    connection = sqlite3.connect('bot_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT file_id FROM files
        WHERE file_name = ?
    ''', (file_name,))
    result = cursor.fetchone()
    connection.close()

    return result[0] if result else None
