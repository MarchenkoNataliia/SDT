import unittest
import sys
import os

from finance_manager import BankAccount

class TestBankAccountExpanded(unittest.TestCase):
    """
    @brief Набір модульних тестів для класу BankAccount.
    
    @details Цей клас містить тестові кейси для перевірки коректності роботи
    фінансових операцій, обробки помилок та логіки безпеки.
    Використовується бібліотека unittest.
    """
    
    def setUp(self):
        """
        @brief Налаштування тестового оточення.
        
        @details Цей метод виконується перед кожним тестом.
        Він створює ізольовані екземпляри рахунків для уникнення залежностей між тестами.
        - self.acc_uah: Рахунок в гривні (1000 UAH).
        - self.acc_usd: Рахунок в доларах (500 USD).
        - self.acc_empty: Порожній рахунок (0 UAH).
        """
        self.acc_uah = BankAccount("User UAH", 1000.0, "UAH")
        self.acc_usd = BankAccount("User USD", 500.0, "USD")
        self.acc_empty = BankAccount("Empty User", 0.0, "UAH")

    # === Блок 1: Ініціалізація ===

    def test_init_correct(self):
        """
        @brief Тест коректної ініціалізації об'єкта.
        @see BankAccount.__init__
        """
        self.assertEqual(self.acc_uah.balance, 1000.0)
        self.assertEqual(self.acc_uah.currency, "UAH")
        self.assertFalse(self.acc_uah.is_frozen)

    def test_init_negative_balance(self):
        """
        @brief Тест заборони створення рахунку з від'ємним балансом.
        @throws ValueError Очікується виключення при initial_balance < 0.
        """
        with self.assertRaises(ValueError):
            BankAccount("Bad User", -100)

    def test_str_representation(self):
        """
        @brief Тест текстового представлення об'єкта.
        @details Перевіряє формат рядка, що повертається методом __str__.
        """
        expected = "Рахунок: User UAH | Баланс: 1000.0 UAH | Статус: Активний"
        self.assertEqual(str(self.acc_uah), expected)

    # === Блок 2: Поповнення (Deposit) ===

    def test_deposit_success(self):
        """
        @brief Тест успішного поповнення рахунку.
        @details Перевіряє збільшення балансу після виклику deposit().
        """
        self.acc_uah.deposit(500)
        self.assertEqual(self.acc_uah.balance, 1500.0)

    def test_deposit_negative_amount(self):
        """
        @brief Тест поповнення від'ємною сумою.
        @throws ValueError Сума поповнення має бути додатною.
        """
        with self.assertRaises(ValueError):
            self.acc_uah.deposit(-50)

    def test_deposit_zero_amount(self):
        """
        @brief Тест поповнення нульовою сумою.
        @throws ValueError Сума поповнення не може дорівнювати 0.
        """
        with self.assertRaises(ValueError):
            self.acc_uah.deposit(0)

    def test_deposit_frozen_account(self):
        """
        @brief Тест заборони поповнення замороженого рахунку.
        @details Спочатку рахунок заморожується, потім робиться спроба поповнення.
        @throws PermissionError Операції із замороженим рахунком заборонені.
        """
        self.acc_uah.freeze_account()
        with self.assertRaises(PermissionError):
            self.acc_uah.deposit(100)

    # === Блок 3: Зняття (Withdraw) ===

    def test_withdraw_success(self):
        """
        @brief Тест успішного зняття коштів.
        @details Перевіряє зменшення балансу після виклику withdraw().
        """
        self.acc_uah.withdraw(200)
        self.assertEqual(self.acc_uah.balance, 800.0)

    def test_withdraw_insufficient_funds(self):
        """
        @brief Тест спроби зняття суми, більшої за залишок.
        @throws ValueError Недостатньо коштів.
        """
        with self.assertRaises(ValueError):
            self.acc_uah.withdraw(2000)

    def test_withdraw_negative(self):
        """
        @brief Тест зняття від'ємної суми.
        @throws ValueError Сума зняття має бути додатною.
        """
        with self.assertRaises(ValueError):
            self.acc_uah.withdraw(-100)

    def test_withdraw_frozen_account(self):
        """
        @brief Тест заборони зняття з замороженого рахунку.
        @throws PermissionError Операції заборонені.
        """
        self.acc_uah.freeze_account()
        with self.assertRaises(PermissionError):
            self.acc_uah.withdraw(100)

    # === Блок 4: Управління статусом (Freeze/Unfreeze) ===

    def test_freeze_account(self):
        """
        @brief Тест блокування рахунку.
        @details Перевіряє зміну прапорця is_frozen та відображення статусу в __str__.
        """
        self.acc_uah.freeze_account()
        self.assertTrue(self.acc_uah.is_frozen)
        self.assertIn("Заморожено", str(self.acc_uah))

    def test_unfreeze_account(self):
        """
        @brief Тест розблокування рахунку.
        @details Перевіряє відновлення можливості фінансових операцій після розморожування.
        """
        self.acc_uah.freeze_account()
        self.acc_uah.unfreeze_account()
        self.assertFalse(self.acc_uah.is_frozen)
        # Перевіряємо, що після розморозки можна проводити операції
        self.acc_uah.deposit(100)
        self.assertEqual(self.acc_uah.balance, 1100.0)

    # === Блок 5: Перекази (Transfer) ===

    def test_transfer_success(self):
        """
        @brief Тест успішного переказу коштів.
        @details Перевіряє списання з одного рахунку та зарахування на інший.
        """
        receiver = BankAccount("Receiver", 0.0, "UAH")
        self.acc_uah.transfer(receiver, 300.0)
        self.assertEqual(self.acc_uah.balance, 700.0)
        self.assertEqual(receiver.balance, 300.0)

    def test_transfer_insufficient_funds(self):
        """
        @brief Тест переказу при недостатньому балансі.
        @throws ValueError Недостатньо коштів для переказу.
        """
        receiver = BankAccount("Receiver", 0.0, "UAH")
        with self.assertRaises(ValueError):
            self.acc_uah.transfer(receiver, 5000.0)

    def test_transfer_different_currencies(self):
        """
        @brief Тест заборони переказу між різними валютами.
        @details Спроба переказу з UAH на USD рахунок.
        @throws ValueError Валюти не співпадають.
        """
        with self.assertRaises(ValueError):
            self.acc_uah.transfer(self.acc_usd, 100.0)

    def test_transfer_to_frozen_account(self):
        """
        @brief Тест транзакційної цілісності при помилці.
        @details Якщо отримувач заморожений, гроші мають повернутися відправнику (rollback).
        """
        receiver = BankAccount("Receiver", 0.0, "UAH")
        receiver.freeze_account()
        # Гроші не мають зникнути з рахунку відправника, якщо отримувач заморожений
        with self.assertRaises(PermissionError):
            self.acc_uah.transfer(receiver, 100.0)
        self.assertEqual(self.acc_uah.balance, 1000.0) # Баланс не змінився

    def test_transfer_invalid_type(self):
        """
        @brief Тест переказу на об'єкт неправильного типу.
        @throws TypeError Отримувач має бути типу BankAccount.
        """
        with self.assertRaises(TypeError):
            self.acc_uah.transfer("Not An Account Object", 100)

    # === Блок 6: Відсотки та Історія ===

    def test_apply_interest(self):
        """
        @brief Тест нарахування відсотків.
        @details Перевіряє правильність математичного розрахунку відсотків.
        """
        self.acc_uah.apply_interest(10) # 10%
        self.assertEqual(self.acc_uah.balance, 1100.0)

    def test_apply_interest_invalid(self):
        """
        @brief Тест нарахування з некоректною ставкою.
        @throws ValueError Ставка <= 0.
        """
        with self.assertRaises(ValueError):
            self.acc_uah.apply_interest(-5)

    def test_transaction_history_logging(self):
        """
        @brief Тест запису історії транзакцій.
        @details Перевіряє, чи зберігаються правильні типи дій (action) та суми в історії.
        """
        self.acc_uah.deposit(500)
        self.acc_uah.withdraw(200)
        history = self.acc_uah.get_history()
        
        # Очікуємо 3 записи: створення, поповнення, зняття
        self.assertEqual(len(history), 3)
        self.assertEqual(history[1]['action'], "Поповнення")
        self.assertEqual(history[1]['amount'], 500)
        self.assertEqual(history[2]['action'], "Зняття")

if __name__ == '__main__':
    unittest.main()
