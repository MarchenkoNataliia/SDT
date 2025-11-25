import unittest
import sys
import os

from finance_manager import BankAccount

class TestBankAccountExpanded(unittest.TestCase):
    
    def setUp(self):
        """Створюємо тестові об'єкти перед кожним тестом."""
        self.acc_uah = BankAccount("User UAH", 1000.0, "UAH")
        self.acc_usd = BankAccount("User USD", 500.0, "USD")
        self.acc_empty = BankAccount("Empty User", 0.0, "UAH")

    # === Блок 1: Ініціалізація (3 тести) ===
    def test_init_correct(self):
        self.assertEqual(self.acc_uah.balance, 1000.0)
        self.assertEqual(self.acc_uah.currency, "UAH")
        self.assertFalse(self.acc_uah.is_frozen)

    def test_init_negative_balance(self):
        with self.assertRaises(ValueError):
            BankAccount("Bad User", -100)

    def test_str_representation(self):
        expected = "Рахунок: User UAH | Баланс: 1000.0 UAH | Статус: Активний"
        self.assertEqual(str(self.acc_uah), expected)
        
    # === Блок 2: Поповнення (Deposit) (4 тести) ===
    def test_deposit_success(self):
        self.acc_uah.deposit(500)
        self.assertEqual(self.acc_uah.balance, 1500.0)

    def test_deposit_negative_amount(self):
        with self.assertRaises(ValueError):
            self.acc_uah.deposit(-50)

    def test_deposit_zero_amount(self):
        with self.assertRaises(ValueError):
            self.acc_uah.deposit(0)

    def test_deposit_frozen_account(self):
        self.acc_uah.freeze_account()
        with self.assertRaises(PermissionError):
            self.acc_uah.deposit(100)

if __name__ == '__main__':
    unittest.main()
