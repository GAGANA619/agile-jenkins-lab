from datetime import datetime, timedelta
import threading


class Account:
    def __init__(self, account_id, name, pin):
        self.account_id = account_id
        self.name = name
        self.pin = str(pin)
        self.balance = 0.0
        self.transactions = []
        self.failed_pin_attempts = 0
        self.lock = threading.Lock()


class DigitalWallet:

    DAILY_LIMIT = 50000.0
    LARGE_TRANSACTION_LIMIT = 20000.0
    MAX_TRANSACTIONS_10_MINUTES = 5
    UNUSUAL_AMOUNT_LIMIT = 15000.0

    def __init__(self):
        self.accounts = {}
        self.processed_transactions = set()
        self.system_lock = threading.Lock()

    # Account creation
    def create_account(self, account_id, name, pin):

        if not account_id or not name:
            raise ValueError("Invalid account details")

        if len(str(pin)) != 4 or not str(pin).isdigit():
            raise ValueError("PIN must contain 4 digits")

        with self.system_lock:
            if account_id in self.accounts:
                raise ValueError("Account already exists")

            self.accounts[account_id] = Account(
                account_id,
                name,
                pin
            )

        return True

    # Get account
    def get_account(self, account_id):

        if account_id not in self.accounts:
            raise ValueError("Account not found")

        return self.accounts[account_id]

    # PIN verification
    def verify_pin(self, account_id, pin):

        account = self.get_account(account_id)

        with account.lock:

            if account.pin == str(pin):
                account.failed_pin_attempts = 0
                return True

            account.failed_pin_attempts += 1

            return False

    # Fraud detection
    def fraud_check(self, account, amount):

        suspicious_reasons = []

        current_time = datetime.now()

        recent_transactions = [
            transaction
            for transaction in account.transactions
            if current_time - transaction["time"]
            <= timedelta(minutes=10)
        ]

        if len(recent_transactions) >= 5:
            suspicious_reasons.append(
                "More than 5 transactions in 10 minutes"
            )

        if amount > self.LARGE_TRANSACTION_LIMIT:
            suspicious_reasons.append(
                "Large transaction"
            )

        if account.failed_pin_attempts >= 3:
            suspicious_reasons.append(
                "Multiple failed PIN attempts"
            )

        if amount > self.UNUSUAL_AMOUNT_LIMIT:
            suspicious_reasons.append(
                "Unusual transaction amount"
            )

        return suspicious_reasons

    # Deposit
    def deposit(self, account_id, amount, pin, transaction_id=None):

        if amount <= 0:
            raise ValueError("Amount must be positive")

        account = self.get_account(account_id)

        if not self.verify_pin(account_id, pin):
            raise ValueError("Invalid PIN")

        with account.lock:

            if transaction_id:
                if transaction_id in self.processed_transactions:
                    raise ValueError("Duplicate transaction")

            fraud_reasons = self.fraud_check(
                account,
                amount
            )

            account.balance += amount

            transaction = {
                "id": transaction_id,
                "type": "Deposit",
                "amount": amount,
                "time": datetime.now(),
                "suspicious": len(fraud_reasons) > 0,
                "reasons": fraud_reasons
            }

            account.transactions.append(transaction)

            if transaction_id:
                self.processed_transactions.add(transaction_id)

            return transaction

    # Withdrawal
    def withdraw(self, account_id, amount, pin, transaction_id=None):

        if amount <= 0:
            raise ValueError("Amount must be positive")

        account = self.get_account(account_id)

        if not self.verify_pin(account_id, pin):
            raise ValueError("Invalid PIN")

        with account.lock:

            if transaction_id:
                if transaction_id in self.processed_transactions:
                    raise ValueError("Duplicate transaction")

            if amount > account.balance:
                raise ValueError("Insufficient balance")

            today = datetime.now().date()

            daily_total = sum(
                transaction["amount"]
                for transaction in account.transactions
                if transaction["time"].date() == today
                and transaction["type"] == "Withdrawal"
            )

            if daily_total + amount > self.DAILY_LIMIT:
                raise ValueError("Daily transaction limit exceeded")

            fraud_reasons = self.fraud_check(
                account,
                amount
            )

            account.balance -= amount

            transaction = {
                "id": transaction_id,
                "type": "Withdrawal",
                "amount": amount,
                "time": datetime.now(),
                "suspicious": len(fraud_reasons) > 0,
                "reasons": fraud_reasons
            }

            account.transactions.append(transaction)

            if transaction_id:
                self.processed_transactions.add(transaction_id)

            return transaction

    # Money transfer
    def transfer(self, sender_id, receiver_id, amount,
                 pin, transaction_id=None):

        if amount <= 0:
            raise ValueError("Amount must be positive")

        if sender_id == receiver_id:
            raise ValueError("Cannot transfer to same account")

        sender = self.get_account(sender_id)
        receiver = self.get_account(receiver_id)

        if not self.verify_pin(sender_id, pin):
            raise ValueError("Invalid PIN")

        with sender.lock:

            if transaction_id:
                if transaction_id in self.processed_transactions:
                    raise ValueError("Duplicate transaction")

            if amount > sender.balance:
                raise ValueError("Insufficient balance")

            today = datetime.now().date()

            daily_total = sum(
                transaction["amount"]
                for transaction in sender.transactions
                if transaction["time"].date() == today
                and transaction["type"] == "Transfer"
            )

            if daily_total + amount > self.DAILY_LIMIT:
                raise ValueError("Daily transaction limit exceeded")

            fraud_reasons = self.fraud_check(
                sender,
                amount
            )

            sender.balance -= amount

            transaction = {
                "id": transaction_id,
                "type": "Transfer",
                "amount": amount,
                "to": receiver_id,
                "time": datetime.now(),
                "suspicious": len(fraud_reasons) > 0,
                "reasons": fraud_reasons
            }

            sender.transactions.append(transaction)

            if transaction_id:
                self.processed_transactions.add(transaction_id)

        with receiver.lock:
            receiver.balance += amount

        return transaction

    # Balance verification
    def get_balance(self, account_id, pin):

        account = self.get_account(account_id)

        if not self.verify_pin(account_id, pin):
            raise ValueError("Invalid PIN")

        with account.lock:
            return account.balance

    # Transaction history
    def transaction_history(self, account_id, pin):

        account = self.get_account(account_id)

        if not self.verify_pin(account_id, pin):
            raise ValueError("Invalid PIN")

        with account.lock:
            return list(account.transactions)

    # Check whether account has suspicious transactions
    def suspicious_transactions(self, account_id):

        account = self.get_account(account_id)

        with account.lock:
            return [
                transaction
                for transaction in account.transactions
                if transaction["suspicious"]
            ]


if __name__ == "__main__":

    wallet = DigitalWallet()

    wallet.create_account(
        "A001",
        "Rahul",
        "1234"
    )

    wallet.create_account(
        "A002",
        "Anita",
        "5678"
    )

    wallet.deposit(
        "A001",
        30000,
        "1234",
        "T001"
    )

    transaction = wallet.transfer(
        "A001",
        "A002",
        5000,
        "1234",
        "T002"
    )

    print("Transfer Successful")
    print("Amount:", transaction["amount"])
    print("Suspicious:", transaction["suspicious"])

    print(
        "Rahul Balance:",
        wallet.get_balance("A001", "1234")
    )

    print(
        "Anita Balance:",
        wallet.get_balance("A002", "5678")
    )