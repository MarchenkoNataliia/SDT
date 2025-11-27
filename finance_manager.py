from datetime import datetime

class BankAccount:
    """
    @brief Клас для управління банківським рахунком.
    
    @details Цей клас дозволяє виконувати основні фінансові операції: поповнення, зняття, 
    перекази, а також керувати станом рахунку (заморожування).
    Підтримує ведення історії транзакцій.
    """

    def __init__(self, owner: str, initial_balance: float = 0.0, currency: str = "UAH"):
        """
        @brief Конструктор класу BankAccount.
        
        @param owner Ім'я власника рахунку (str).
        @param initial_balance Початковий баланс (float). За замовчуванням 0.0.
        @param currency Валюта рахунку (str). За замовчуванням "UAH".
        @throws ValueError Якщо initial_balance < 0.
        """
        if initial_balance < 0:
            raise ValueError("Початковий баланс не може бути від'ємним.")
        
        self.owner = owner
        self.balance = initial_balance
        self.currency = currency
        self.is_frozen = False
        self.transaction_history = [] 
        self._log_transaction("Створення рахунку", initial_balance)

    def _log_transaction(self, action: str, amount: float):
        """
        @brief Внутрішній метод для запису операції в історію.
        
        @param action Опис дії (str).
        @param amount Сума операції (float).
        """
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "amount": amount,
            "balance_after": self.balance
        }
        self.transaction_history.append(record)

    def deposit(self, amount: float):
        """
        @brief Поповнення рахунку.
        
        @param amount Сума поповнення (float). Має бути > 0.
        @return Оновлений баланс (float).
        @throws ValueError Якщо amount <= 0.
        @throws PermissionError Якщо рахунок заморожено.
        """
        if self.is_frozen:
            raise PermissionError("Рахунок заморожено. Операції заборонені.")
        if amount <= 0:
            raise ValueError("Сума поповнення має бути більше нуля.")
        
        self.balance += amount
        self._log_transaction("Поповнення", amount)
        return self.balance

    def withdraw(self, amount: float):
        """
        @brief Зняття коштів з рахунку.
        
        @param amount Сума зняття (float).
        @return Оновлений баланс (float).
        @throws ValueError Якщо amount <= 0 або недостатньо коштів.
        @throws PermissionError Якщо рахунок заморожено.
        """
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
        """
        @brief Переказ коштів на інший рахунок.
        
        @param other_account Об'єкт BankAccount отримувача.
        @param amount Сума переказу (float).
        @throws TypeError Якщо other_account не є екземпляром BankAccount.
        @throws ValueError Якщо валюти рахунків відрізняються.
        """
        if not isinstance(other_account, BankAccount):
            raise TypeError("Отримувач має бути екземпляром BankAccount.")
        if self.currency != other_account.currency:
            raise ValueError("Переказ можливий тільки між рахунками в одній валюті.")
        
        self.withdraw(amount)
        try:
            other_account.deposit(amount)
        except Exception as e:
            self.balance += amount 
            raise e

        self.transaction_history[-1]["action"] = f"Переказ до {other_account.owner}"

    def freeze_account(self):
        """@brief Заморозити рахунок (заборонити операції)."""
        self.is_frozen = True

    def unfreeze_account(self):
        """@brief Розморозити рахунок."""
        self.is_frozen = False

    def apply_interest(self, rate: float):
        """
        @brief Нарахування відсотків на залишок.
        
        @param rate Відсоткова ставка (наприклад, 5.0 для 5%).
        @return Оновлений баланс (float).
        @throws PermissionError Якщо рахунок заморожено.
        @throws ValueError Якщо rate <= 0.
        """
        if self.is_frozen:
            raise PermissionError("Не можна нараховувати відсотки на заморожений рахунок.")
        if rate <= 0:
            raise ValueError("Відсоткова ставка має бути додатною.")
        
        interest_amount = self.balance * (rate / 100)
        self.balance += interest_amount
        self._log_transaction(f"Відсотки ({rate}%)", interest_amount)
        return self.balance

    def get_history(self):
        """
        @brief Отримати історію транзакцій.
        @return Список словників (list[dict]) з деталями транзакцій.
        """
        return self.transaction_history[:]

    def __str__(self):
        """@brief Текстове представлення рахунку."""
        status = "Заморожено" if self.is_frozen else "Активний"
        return f"Рахунок: {self.owner} | Баланс: {self.balance} {self.currency} | Статус: {status}"
