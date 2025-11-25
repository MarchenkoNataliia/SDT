from datetime import datetime

class BankAccount:
    """
    Розширений клас банківського рахунку з підтримкою переказів,
    історії транзакцій та статусів.
    """
    def __init__(self, owner: str, initial_balance: float = 0.0, currency: str = "UAH"):
        if initial_balance < 0:
            raise ValueError("Початковий баланс не може бути від'ємним.")
        
        self.owner = owner
        self.balance = initial_balance
        self.currency = currency
        self.is_frozen = False
        self.transaction_history = []  # Список словників з історією
        self._log_transaction("Створення рахунку", initial_balance)

    def _log_transaction(self, action: str, amount: float):
        """Внутрішній метод для запису операції в історію."""
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "amount": amount,
            "balance_after": self.balance
        }
        self.transaction_history.append(record)

    def deposit(self, amount: float):
        """Поповнення рахунку."""
        if self.is_frozen:
            raise PermissionError("Рахунок заморожено. Операції заборонені.")
        if amount <= 0:
            raise ValueError("Сума поповнення має бути більше нуля.")
        
        self.balance += amount
        self._log_transaction("Поповнення", amount)
        return self.balance

    def withdraw(self, amount: float):
        """Зняття коштів."""
        if self.is_frozen:
            raise PermissionError("Рахунок заморожено. Операції заборонені.")
        if amount <= 0:
            raise ValueError("Сума зняття має бути більше нуля.")
        if amount > self.balance:
            raise ValueError("Недостатньо коштів на рахунку.")
        
        self.balance -= amount
        self._log_transaction("Зняття", -amount)
        return self.balance

    def transfer(self, other_account, amount: float):
        """Переказ коштів на інший рахунок."""
        if not isinstance(other_account, BankAccount):
            raise TypeError("Отримувач має бути екземпляром BankAccount.")
        if self.currency != other_account.currency:
            raise ValueError("Переказ можливий тільки між рахунками в одній валюті.")
        
        # Виконуємо зняття (перевірки на заморозку та баланс всередині withdraw)
        self.withdraw(amount)
        # Виконуємо поповнення іншого рахунку
        try:
            other_account.deposit(amount)
        except Exception as e:
            # Якщо поповнення не вдалося (наприклад, той рахунок заморожений), повертаємо гроші
            self.balance += amount 
            raise e

        # Оновлюємо лог, щоб це виглядало як переказ, а не просто зняття
        self.transaction_history[-1]["action"] = f"Переказ до {other_account.owner}"

    def freeze_account(self):
        """Заморозити рахунок."""
        self.is_frozen = True

    def unfreeze_account(self):
        """Розморозити рахунок."""
        self.is_frozen = False

    def apply_interest(self, rate: float):
        """Нарахування відсотків (rate у відсотках, наприклад, 5.0)."""
        if self.is_frozen:
            raise PermissionError("Не можна нараховувати відсотки на заморожений рахунок.")
        if rate <= 0:
            raise ValueError("Відсоткова ставка має бути додатною.")
        
        interest_amount = self.balance * (rate / 100)
        self.balance += interest_amount
        self._log_transaction(f"Відсотки ({rate}%)", interest_amount)
        return self.balance

    def get_history(self):
        """Повертає копію історії транзакцій."""
        return self.transaction_history[:]

    def __str__(self):
        status = "Заморожено" if self.is_frozen else "Активний"
        return f"Рахунок: {self.owner} | Баланс: {self.balance} {self.currency} | Статус: {status}"
