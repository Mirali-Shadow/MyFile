import sqlite3
import time

DATABASE = 'stars.db'
REFERRAL_POINTS = 10

conn = sqlite3.connect(DATABASE) 
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        points INTEGER DEFAULT 0,
        referrals INTEGER DEFAULT 0,
        inviter_id INTEGER
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        tx_id TEXT PRIMARY KEY,
        user_id INTEGER,
        amount REAL
    );
""")
conn.commit()

print("Database is ready ..")

def get_user_points_trx(user_id):
    cursor.execute("SELECT points FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0

def update_user_points_trx(user_id, points):
    cursor.execute("INSERT INTO users (user_id, points) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET points = ?", (user_id, points, points))
    conn.commit()

def add_transaction_trx(tx_id, user_id, amount):
    cursor.execute("INSERT INTO transactions (tx_id, user_id, amount) VALUES (?, ?, ?)", (tx_id, user_id, amount))
    conn.commit()

def is_transaction_exists_trx(tx_id):
    cursor.execute("SELECT 1 FROM transactions WHERE tx_id = ?", (tx_id,))
    return cursor.fetchone() is not None

def get_user_transaction_count_trx(user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions WHERE user_id = ?", (user_id,))
    count = cursor.fetchone()
    return count[0] if count else 0

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

# 📌 تابع دریافت لیست کاربران
def get_all_users_public():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
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

# 📌 دریافت اطلاعات کامل کاربر (امتیاز، ارجاع‌ها، و دعوت‌کننده)
def get_full_user_info(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, points, referrals, inviter_id FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# 📌 دریافت نام و امتیاز همه کاربران برای نمایش لیست در حساب کاربری
def get_all_users_info():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, points, referrals FROM users ORDER BY points DESC")
    users = cursor.fetchall()
    conn.close()
    return users

# 📌 بررسی اینکه آیا کاربری دعوت‌کننده داشته است یا نه
def get_inviter(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT inviter_id FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def user_exists(user_id):
    """بررسی می‌کند که آیا کاربر از قبل در دیتابیس هست یا نه"""
    cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is not None

def update_all_users_points(points):
    """افزایش یا کاهش امتیاز تمام کاربران"""
    cursor.execute("UPDATE users SET points = points + ?", (points,))
    conn.commit()

def get_all_users_for_all():
    """دریافت لیست همه کاربران"""
    cursor.execute("SELECT user_id FROM users")
    return [row[0] for row in cursor.fetchall()]
#__________________________________________________________
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

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,  -- نوع سفارش (استارز روی پست یا برای اکانت)
        quantity INTEGER,  -- تعداد استارز
        total_price INTEGER,  -- قیمت کل سفارش (امتیاز)
        post_link TEXT,  -- لینک پست (فقط برای سفارش استارز روی پست)
        username TEXT,  -- یوزرنیم اکانت (فقط برای سفارش استارز برای اکانت)
        status TEXT,  -- وضعیت سفارش (در حال پردازش، تکمیل شده)
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- زمان ثبت سفارش
    );
""")
conn.commit()

def add_order(user_id, order_type, quantity, total_price, post_link=None, username=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    status = "در حال پردازش"
    cursor.execute("""
        INSERT INTO orders (user_id, type, quantity, total_price, post_link, username, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, order_type, quantity, total_price, post_link, username, status))
    
    conn.commit()
    conn.close()

def update_order_status(order_id, status):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (status, order_id))
    conn.commit()
    conn.close()

def get_user_orders(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    orders = cursor.fetchall()
    conn.close()
    return orders

def decrease_user_points_for_order(user_id, total_price):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET points = points - ? WHERE user_id = ?", (total_price, user_id))
    conn.commit()
    conn.close()

# _____________________________________________________

# ایجاد جدول برای ذخیره آخرین زمان دریافت جایزه روزانه
cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_rewards (
        user_id INTEGER PRIMARY KEY,
        last_claim INTEGER
    );
""")

conn.commit()

def can_claim_reward(user_id):
    """بررسی می‌کند که آیا کاربر می‌تواند جایزه روزانه دریافت کند یا نه"""
    cursor.execute("SELECT last_claim FROM daily_rewards WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        last_claim = result[0]
        if time.time() - last_claim < 86400: 
            return False 

    return True 

def update_last_claim(user_id):
    """بروزرسانی زمان آخرین دریافت جایزه"""
    cursor.execute("""
        INSERT INTO daily_rewards (user_id, last_claim)
        VALUES (?, ?) 
        ON CONFLICT(user_id) DO UPDATE SET last_claim = excluded.last_claim;
    """, (user_id, int(time.time())))
    conn.commit()

def add_points(user_id, points):
    """افزودن امتیاز به حساب کاربر"""
    cursor.execute("""
        INSERT INTO users (user_id, points) 
        VALUES (?, ?) 
        ON CONFLICT(user_id) DO UPDATE SET points = points + excluded.points;
    """, (user_id, points))
    conn.commit()
    
#__________________________________________________________________________________

cursor.execute("""
CREATE TABLE IF NOT EXISTS channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    display_link TEXT,
    channel_id INTEGER,
    display_name TEXT
)
""")
conn.commit()

def add_channel_to_db(display_link, channel_id, display_name):
    cursor.execute("INSERT INTO channels (display_link, channel_id, display_name) VALUES (?, ?, ?)", (display_link, channel_id, display_name))
    conn.commit()

def delete_channel_from_db(channel_id):
    cursor.execute("DELETE FROM channels WHERE id = ?", (channel_id,))
    conn.commit()

def get_all_channels():
    cursor.execute("SELECT id, display_name FROM channels")
    return cursor.fetchall()

def get_channels_list():
    cursor.execute("SELECT display_name, display_link, channel_id FROM channels")
    return cursor.fetchall()

def get_channels_from_db():
    cursor.execute("SELECT display_link, channel_id, display_name FROM channels")
    return cursor.fetchall()

#_________________________________________________________________


def user_exists_t(user_id):
    """بررسی می‌کند که آیا کاربر در دیتابیس وجود دارد یا نه"""
    cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is not None


def add_user_t(user_id, inviter_id=None):
    """افزودن کاربر جدید به دیتابیس"""
    if not user_exists(user_id):
        cursor.execute("INSERT INTO users (user_id, points, referrals, inviter_id) VALUES (?, 0, 0, ?)", (user_id, inviter_id))
        conn.commit()


def get_user_points_t(user_id):
    """دریافت موجودی کاربر"""
    cursor.execute("SELECT points FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0


def update_user_points_t(user_id, new_points):
    """به‌روزرسانی امتیاز کاربر"""
    cursor.execute("UPDATE users SET points = ? WHERE user_id = ?", (new_points, user_id))
    conn.commit()


# def record_transaction_t(tx_id, user_id, amount):
#     """ثبت تراکنش در دیتابیس"""
#     cursor.execute("INSERT INTO transactions (tx_id, user_id, amount) VALUES (?, ?, ?)", (tx_id, user_id, amount))
#     conn.commit()
