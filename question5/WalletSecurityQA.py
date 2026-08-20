import unittest
import threading

from DigitalWallet import DigitalWallet


class WalletSecurityQA(unittest.TestCase):

    def setUp(self):

        self.wallet = DigitalWallet()

        self.wallet.create_account(
            "A001",
            "Rahul",
            "1234"
        )

        self.wallet.create_account(
            "A002",
            "Anita",
            "5678"
        )

        self.wallet.deposit(
            "A001",
            50000,
            "1234",
            "INIT001"
        )

    # 1. Normal transaction
    def test_normal_transaction(self):

        transaction = self.wallet.withdraw(
            "A001",
            5000,
            "1234",
            "TX001"
        )

        self.assertEqual(
            transaction["amount"],
            5000
        )

        self.assertFalse(
            transaction["suspicious"]
        )

        self.assertEqual(
            self.wallet.get_balance("A001", "1234"),
            45000
        )

    # 2. Insufficient balance
    def test_insufficient_balance(self):

        with self.assertRaises(ValueError):

            self.wallet.withdraw(
                "A001",
                100000,
                "1234",
                "TX002"
            )

    # 3. Daily transaction limit
    def test_daily_limit(self):

        with self.assertRaises(ValueError):

            self.wallet.withdraw(
                "A001",
                50001,
                "1234",
                "TX003"
            )

    # 4. Multiple failed PIN attempts
    def test_multiple_failed_pins(self):

        for _ in range(3):

            with self.assertRaises(ValueError):

                self.wallet.withdraw(
                    "A001",
                    1000,
                    "9999",
                    "BAD"
                )

        account = self.wallet.get_account("A001")

        self.assertEqual(
            account.failed_pin_attempts,
            3
        )

    # 5. Suspicious large transaction
    def test_suspicious_transaction(self):

        transaction = self.wallet.withdraw(
            "A001",
            25000,
            "1234",
            "TX005"
        )

        self.assertTrue(
            transaction["suspicious"]
        )

        self.assertTrue(
            len(transaction["reasons"]) > 0
        )

    # 6. Duplicate transaction
    def test_duplicate_transaction(self):

        self.wallet.withdraw(
            "A001",
            1000,
            "1234",
            "TX006"
        )

        with self.assertRaises(ValueError):

            self.wallet.withdraw(
                "A001",
                1000,
                "1234",
                "TX006"
            )

    # 7. Negative amount
    def test_negative_amount(self):

        with self.assertRaises(ValueError):

            self.wallet.deposit(
                "A001",
                -1000,
                "1234",
                "TX007"
            )

        with self.assertRaises(ValueError):

            self.wallet.withdraw(
                "A001",
                -500,
                "1234",
                "TX008"
            )

    # 8. Zero amount
    def test_zero_amount(self):

        with self.assertRaises(ValueError):

            self.wallet.deposit(
                "A001",
                0,
                "1234",
                "TX009"
            )

    # 9. Money transfer
    def test_money_transfer(self):

        transaction = self.wallet.transfer(
            "A001",
            "A002",
            5000,
            "1234",
            "TX010"
        )

        self.assertEqual(
            transaction["amount"],
            5000
        )

        self.assertEqual(
            self.wallet.get_balance("A001", "1234"),
            45000
        )

        self.assertEqual(
            self.wallet.get_balance("A002", "5678"),
            5000
        )

    # 10. Balance verification
    def test_balance_verification(self):

        balance = self.wallet.get_balance(
            "A001",
            "1234"
        )

        self.assertEqual(
            balance,
            50000
        )

    # 11. Transaction history
    def test_transaction_history(self):

        self.wallet.withdraw(
            "A001",
            1000,
            "1234",
            "TX011"
        )

        history = self.wallet.transaction_history(
            "A001",
            "1234"
        )

        self.assertGreaterEqual(
            len(history),
            2
        )

    # 12. More than 5 transactions in 10 minutes
    def test_many_transactions_fraud(self):

        for i in range(5):

            self.wallet.withdraw(
                "A001",
                100,
                "1234",
                "M" + str(i)
            )

        transaction = self.wallet.withdraw(
            "A001",
            100,
            "1234",
            "M5"
        )

        self.assertTrue(
            transaction["suspicious"]
        )

    # 13. Invalid account
    def test_invalid_account(self):

        with self.assertRaises(ValueError):

            self.wallet.get_balance(
                "INVALID",
                "1234"
            )

    # 14. Concurrent transactions
    def test_concurrent_transactions(self):

        results = []
        errors = []

        def make_transaction(number):

            try:

                transaction = self.wallet.withdraw(
                    "A001",
                    100,
                    "1234",
                    "CONCURRENT" + str(number)
                )

                results.append(transaction)

            except Exception as error:
                errors.append(error)

        threads = []

        for i in range(5):

            thread = threading.Thread(
                target=make_transaction,
                args=(i,)
            )

            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(
            len(results),
            5
        )

        self.assertEqual(
            len(errors),
            0
        )


if __name__ == "__main__":
    unittest.main()