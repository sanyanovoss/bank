import random
from database import Database
from models import User, AbstractTransaction, TransferTransaction


class BankSystem:
    def __init__(self, db: Database):
        self.db = db

    def generate_luhn_card(self) -> str:
        while True:
            digits = [random.randint(0, 9) for _ in range(15)]
            checksum = self._calculate_luhn_checksum(digits)
            digits.append(checksum)

            card_str = "".join(map(str, digits))
            formatted = f"{card_str[:4]}-{card_str[4:8]}-{card_str[8:12]}-{card_str[12:]}"

            if not self.db.get_user(formatted):
                return formatted

    def _calculate_luhn_checksum(self, digits: list[int]) -> int:
        total = 0
        for i, d in enumerate(reversed(digits)):
            if i % 2 == 0:
                d *= 2
                if d > 9:
                    d -= 9
            total += d
        return (10 - (total % 10)) % 10

    def is_valid_luhn(self, card_number: str) -> bool:
        clean_number = card_number.replace("-", "")
        if not clean_number.isdigit() or len(clean_number) != 16:
            return False
        digits = [int(x) for x in clean_number]
        checksum = digits.pop()
        return self._calculate_luhn_checksum(digits) == checksum

    def register_client(self, name: str, pin: str, balance: float) -> str:
        if len(name.split()) < 2:
            raise ValueError("Введіть повне ПІБ!")
        if not pin.isdigit() or len(pin) != 4:
            raise ValueError("PIN має містити 4 цифри!")
        if balance < 0:
            raise ValueError("Баланс не може бути від'ємним!")

        card_number = self.generate_luhn_card()
        self.db.add_user(card_number, name, pin, balance)
        return card_number

    def authenticate(self, card_number: str, pin: str) -> User:
        user = self.db.get_user(card_number)
        if not user:
            raise ValueError("Картку не знайдено!")
        if user.is_blocked:
            raise ValueError("Картку заблоковано банком!")

        if not self.db.verify_user_pin(card_number, pin):
            user.increment_failed_attempts()
            self.db.update_user(user)
            if user.is_blocked:
                raise ValueError("Картку заблоковано через 3 невірні спроби!")
            raise ValueError(f"Невірний PIN! Залишилось спроб: {3 - user.failed_attempts}")

        user.reset_failed_attempts()
        self.db.update_user(user)
        return user

    def process_transaction(self, user: User, transaction: AbstractTransaction) -> bool:
        if transaction.execute(user):
            self.db.update_user(user)
            self.db.add_transaction_history(user.card_number, transaction.get_details())

            if isinstance(transaction, TransferTransaction):
                target_user = transaction._target_user
                self.db.update_user(target_user)
                self.db.add_transaction_history(target_user.card_number,
                                                transaction.get_target_details(user.card_number))

            return True
        return False

    def unblock_user_card(self, card_number: str):
        user = self.db.get_user(card_number)
        if not user:
            raise ValueError("Користувача не знайдено!")
        if not user.is_blocked:
            raise ValueError("Картка не заблокована!")
        user.unblock()
        self.db.update_user(user)

    def get_admin_stats(self) -> str:
        total_users, total_money, blocked = self.db.get_all_users_stats()
        return f"Клієнтів: {total_users}\nКапітал: {total_money:,.2f} UAH\nЗаблоковано: {blocked}"