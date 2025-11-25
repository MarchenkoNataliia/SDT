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

if __name__ == '__main__':
    unittest.main()
