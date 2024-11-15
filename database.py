import sqlite3

# ایجاد اتصال به دیتابیس
def get_db_connection():
    # اتصال به دیتابیس و فعال کردن استفاده از آن در نخ‌های مختلف
    return sqlite3.connect('file_links.db', check_same_thread=False)

# ایجاد جدول برای ذخیره فایل‌ها
def create_table():
    conn = get_db_connection()
    c = conn.cursor()
    # جدول برای ذخیره command و file_id
    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT UNIQUE,
            file_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

# اضافه کردن فایل به دیتابیس
def add_file_to_db(command, file_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO files (command, file_id) VALUES (?, ?)", (command, file_id))
    conn.commit()
    conn.close()

# گرفتن لینک فایل از دیتابیس بر اساس دستور
def get_file_link_from_db(command):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT file_id FROM files WHERE command = ?", (command,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
