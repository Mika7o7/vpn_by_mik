import sqlite3
from datetime import datetime

# Подключение к базе данных
conn = sqlite3.connect('bot.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблиц
def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT,
            full_name TEXT,
            created_at TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            tariff TEXT,
            start_date TEXT,
            end_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            currency TEXT,
            payment_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    conn.commit()

# Добавление пользователя
def add_user(user_id, username, full_name):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, full_name, created_at)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, full_name, created_at))
    conn.commit()

# Добавление подписки
def add_subscription(user_id, tariff, start_date, end_date):
    cursor.execute('''
        INSERT INTO subscriptions (user_id, tariff, start_date, end_date)
        VALUES (?, ?, ?, ?)
    ''', (user_id, tariff, start_date, end_date))
    conn.commit()

# Добавление платежа
def add_payment(user_id, amount, currency):
    payment_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO payments (user_id, amount, currency, payment_date)
        VALUES (?, ?, ?, ?)
    ''', (user_id, amount, currency, payment_date))
    conn.commit()

# Получение статистики
def get_analysis():
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM subscriptions')
    total_subscriptions = cursor.fetchone()[0]

    cursor.execute('SELECT SUM(amount) FROM payments')
    total_revenue = cursor.fetchone()[0] or 0

    return {
        "total_users": total_users,
        "total_subscriptions": total_subscriptions,
        "total_revenue": total_revenue
    }

# Инициализация базы данных при запуске
init_db()