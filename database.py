import sqlite3
import json
from typing import Dict, List

class Database:
    def __init__(self, db_path: str = "bot_data.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    telegram_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    referral_link TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id TEXT,
                    client_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (employee_id) REFERENCES employees (telegram_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cryptoclub_referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id TEXT,
                    code TEXT,
                    used BOOLEAN DEFAULT FALSE,
                    client_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (employee_id) REFERENCES employees (telegram_id)
                )
            ''')
            
            conn.commit()
    
    def add_employee(self, telegram_id: str, name: str, referral_link: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO employees (telegram_id, name, referral_link) VALUES (?, ?, ?)",
                (telegram_id, name, referral_link)
            )
            conn.commit()
    
    def get_employees(self) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT telegram_id, name, referral_link FROM employees")
            rows = cursor.fetchall()
            return {row[0]: {'name': row[1], 'referral_link': row[2]} for row in rows}
    
    def add_referral(self, employee_id: str, client_id: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO referrals (employee_id, client_id) VALUES (?, ?)",
                (employee_id, client_id)
            )
            conn.commit()
    
    def get_referrals(self) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT employee_id, client_id FROM referrals")
            rows = cursor.fetchall()
            referrals = {}
            for row in rows:
                if row[0] not in referrals:
                    referrals[row[0]] = []
                referrals[row[0]].append(row[1])
            return referrals
    
    def remove_employee(self, telegram_id: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Удаляем сотрудника
            cursor.execute("DELETE FROM employees WHERE telegram_id = ?", (telegram_id,))
            # Удаляем его рефералов
            cursor.execute("DELETE FROM referrals WHERE employee_id = ?", (telegram_id,))
            conn.commit()