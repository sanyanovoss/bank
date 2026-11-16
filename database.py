import sqlite3
import hashlib
from models import User

class Database:
    def __init__(self, db_name: str = "atm_system.db"):
        self.db_name = db_name
        self._create_tables()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _hash_pin(self, pin: str) -> str:
        return hashlib.sha256(pin.encode("utf-8")).hexdigest()

    def _create_tables(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    card_number TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    pin_hash TEXT NOT NULL,
                    balance REAL NOT NULL,
                    failed_attempts INTEGER DEFAULT 0,
                    is_blocked INTEGER DEFAULT 0
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    card_number TEXT NOT NULL,
                    details TEXT NOT NULL,
                    FOREIGN KEY(card_number) REFERENCES users(card_number)
                )
            """)
            conn.commit()

    def add_user(self, card_number: str, name: str, pin: str, balance: float):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            pin_hash = self._hash_pin(pin)
            cursor.execute(
                "INSERT INTO users (card_number, name, pin_hash, balance) VALUES (?, ?, ?, ?)",
                (card_number, name, pin_hash, balance)
            )
            conn.commit()

    def get_user(self, card_number: str) -> User | None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT card_number, name, balance, failed_attempts, is_blocked FROM users WHERE card_number = ?",
                (card_number,)
            )
            row = cursor.fetchone()
            if row:
                return User(row[0], row[1], row[2], row[3], bool(row[4]))
        return None

    def verify_user_pin(self, card_number: str, pin: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            pin_hash = self._hash_pin(pin)
            cursor.execute(
                "SELECT 1 FROM users WHERE card_number = ? AND pin_hash = ?",
                (card_number, pin_hash)
            )
            return cursor.fetchone() is not None

    def update_user(self, user: User):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET balance = ?, failed_attempts = ?, is_blocked = ? WHERE card_number = ?",
                (user.balance, user.failed_attempts, int(user.is_blocked), user.card_number)
            )
            conn.commit()

    def add_transaction_history(self, card_number: str, details: str):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO history (card_number, details) VALUES (?, ?)",
                (card_number, details)
            )
            conn.commit()

    def get_user_history(self, card_number: str) -> list[str]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT details FROM history WHERE card_number = ? ORDER BY id DESC LIMIT 4",
                (card_number,)
            )
            return [row[0] for row in cursor.fetchall()]

    def get_all_users_stats(self) -> tuple[int, float, int]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*), SUM(balance), SUM(is_blocked) FROM users")
            row = cursor.fetchone()
            return row[0] or 0, row[1] or 0.0, row[2] or 0