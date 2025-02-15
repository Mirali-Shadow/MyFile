import sqlite3

DATABASE = 'stars.db'
REFERRAL_POINTS = 10

# 📌 ایجاد اتصال به دیتابیس
conn = sqlite3.connect(DATABASE)  # مقداردهی صحیح
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        points INTEGER DEFAULT 0,
        referrals INTEGER DEFAULT 0,
        inviter_id INTEGER
    );
""")
print("database is ready ..")
conn.commit()

# 📌 دریافت امتیاز کاربر
def get_user_points(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT points FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

# 📌 دریافت تعداد ارجاع‌های کاربر
def get_referral_count(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT referrals FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

# 📌 افزودن کاربر جدید
def add_user(user_id, inviter_id=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.execute("INSERT INTO users (user_id, points, referrals, inviter_id) VALUES (?, 0, 0, ?)", 
                       (user_id, inviter_id))
        if inviter_id:
            cursor.execute("UPDATE users SET referrals = referrals + 1, points = points + ? WHERE user_id = ?", 
                           (REFERRAL_POINTS, inviter_id))
    conn.commit()
    conn.close()

# 📌 دریافت لیست همه کاربران
def get_all_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, points, referrals FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

# 📌 دریافت اطلاعات یک کاربر خاص
def get_user_info(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT points, referrals FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# 📌 بروزرسانی امتیاز کاربر
def update_user_points(user_id, points):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET points = points + ? WHERE user_id = ?", (points, user_id))
    conn.commit()
    conn.close()

cursor.execute("""
CREATE TABLE IF NOT EXISTS temp_referrals (
    user_id INTEGER PRIMARY KEY,
    inviter_id INTEGER
)
""")
conn.commit()

def store_temp_inviter(user_id, inviter_id):
    cursor.execute("INSERT OR REPLACE INTO temp_referrals (user_id, inviter_id) VALUES (?, ?)", (user_id, inviter_id))
    conn.commit()

def get_temp_inviter(user_id):
    cursor.execute("SELECT inviter_id FROM temp_referrals WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def remove_temp_inviter(user_id):
    cursor.execute("DELETE FROM temp_referrals WHERE user_id=?", (user_id,))
    conn.commit()

def is_user_registered(user_id):
    cursor.execute("SELECT COUNT(*) FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()[0] > 0