import logging
import tkinter as tk
from database import Database
from bank_system import BankSystem
from ui import ATMApp

logging.basicConfig(
    filename="atm_system.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


def initialize_default_users(bank: BankSystem):
    if bank.db.get_user("4444333322221111") is None:
        bank.db.add_user("4444333322221111", "Oleksandr Novoselskiy", "4321", 1783.0)
    if bank.db.get_user("7777777777777777") is None:
        bank.db.add_user("7777777777777777", "Dmytro Kudryavtsev", "7777", 100000.0)


def main():
    logging.info("=== Запуск системи банкомата ===")

    db = Database()
    bank = BankSystem(db)
    initialize_default_users(bank)

    root = tk.Tk()
    app = ATMApp(root, bank)
    root.mainloop()

    logging.info("=== Роботу системи банкомата завершено ===\n")


if __name__ == "__main__":
    main()