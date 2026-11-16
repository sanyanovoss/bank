from abc import ABC, abstractmethod

class User:
    def __init__(self, card_number: str, name: str, balance: float, failed_attempts: int, is_blocked: bool):
        self.__card_number = card_number
        self.__name = name
        self.__balance = balance
        self.__failed_attempts = failed_attempts
        self.__is_blocked = is_blocked

    @property
    def card_number(self) -> str:
        return self.__card_number

    @property
    def name(self) -> str:
        return self.__name

    @property
    def balance(self) -> float:
        return self.__balance

    @property
    def failed_attempts(self) -> int:
        return self.__failed_attempts

    @property
    def is_blocked(self) -> bool:
        return self.__is_blocked

    def add_funds(self, amount: float):
        if amount <= 0:
            raise ValueError("Сума має бути більшою за нуль!")
        self.__balance += amount

    def deduct_funds(self, amount: float):
        if amount <= 0:
            raise ValueError("Сума має бути більшою за нуль!")
        if amount > self.__balance:
            raise ValueError("Недостатньо коштів!")
        self.__balance -= amount

    def increment_failed_attempts(self):
        self.__failed_attempts += 1
        if self.__failed_attempts >= 3:
            self.__is_blocked = True

    def reset_failed_attempts(self):
        self.__failed_attempts = 0

    def unblock(self):
        self.__is_blocked = False
        self.__failed_attempts = 0


class AbstractTransaction(ABC):
    def __init__(self, amount: float):
        if amount <= 0:
            raise ValueError("Сума транзакції повинна бути більшою за нуль!")
        self._amount = float(amount)
        self._is_executed = False

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def is_executed(self) -> bool:
        return self._is_executed

    @abstractmethod
    def execute(self, user: User) -> bool:
        pass

    @abstractmethod
    def get_details(self) -> str:
        pass


class DepositTransaction(AbstractTransaction):
    def execute(self, user: User) -> bool:
        if self._is_executed:
            return False
        user.add_funds(self._amount)
        self._is_executed = True
        return True

    def get_details(self) -> str:
        return f"Поповнення: +{self._amount:.2f} UAH"


class WithdrawTransaction(AbstractTransaction):
    def execute(self, user: User) -> bool:
        if self._is_executed:
            return False
        user.deduct_funds(self._amount)
        self._is_executed = True
        return True

    def get_details(self) -> str:
        return f"Зняття: -{self._amount:.2f} UAH"


class TransferTransaction(AbstractTransaction):
    def __init__(self, amount: float, target_user: User):
        super().__init__(amount)
        self._target_user = target_user

    def execute(self, user: User) -> bool:
        if self._is_executed:
            return False
        user.deduct_funds(self._amount)
        self._target_user.add_funds(self._amount)
        self._is_executed = True
        return True

    def get_details(self) -> str:
        return f"Переказ на {self._target_user.card_number[-4:]}: -{self._amount:.2f} UAH"

    def get_target_details(self, source_card: str) -> str:
        return f"Отримано від {source_card[-4:]}: +{self._amount:.2f} UAH"