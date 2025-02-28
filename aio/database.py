import sqlite3

conn = sqlite3.connect("lottery.db")
cursor = conn.cursor()

cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        trons INTEGER DEFAULT 0,
        number_of_bets INTEGER DEFAULT 0,
        joined_time DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS bets (
        bet_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user1_id INTEGER,
        user2_id INTEGER,
        bet_amount INTEGER,
        game_type TEXT CHECK(game_type IN ('dice', 'dart')),
        result TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user1_id) REFERENCES users(user_id),
        FOREIGN KEY (user2_id) REFERENCES users(user_id)
    );

    CREATE TABLE IF NOT EXISTS transactions (
        trx_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount INTEGER,
        trx_type TEXT CHECK(trx_type IN ('deposit', 'withdraw', 'bet_win', 'bet_loss')),
        trx_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

    CREATE TABLE IF NOT EXISTS withdrawals (
        withdraw_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount INTEGER,
        wallet_address TEXT,
        status TEXT CHECK(status IN ('pending', 'approved', 'rejected')),
        request_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
""")

conn.commit() 

def get_user_points(user_id):
    cursor.execute("SELECT trons FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    print(result)
    return result[0] if result else 0
    
def get_full_user_info(user_id):
    cursor.execute("SELECT user_id, trons, number_of_bets, joined_time FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user
