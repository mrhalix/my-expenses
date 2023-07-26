import os
import mysql.connector as database


class DatabaseConnector:
    def __init__(self, db_host, db_port, db_username, db_password, db_name, table_name):
        self.db_host = db_host
        self.db_port = db_port
        self.db_username = db_username
        self.db_password = db_password
        self.db_name = db_name
        self.table_name = table_name


        print("Connecting to database")
        self.connection = database.connect(
            user=self.db_username,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name)
        print("connection done")
        
        print("Creating cursor")
        self.cursor = self.connection.cursor()
        print("cursor done")
        
        self.create_table_if_not_exists(self.table_name)
        
    def create_table_if_not_exists(self, table_name):
        try:
            # id, date_created, bank_name, account_id, action, amount, month, day, hour, minute, balance, reason
            statement = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP, bank_name VARCHAR(255), account_id VARCHAR(255), action VARCHAR(255), amount VARCHAR(255), month VARCHAR(255), day VARCHAR(255), hour VARCHAR(255), minute VARCHAR(255), balance VARCHAR(255), reason VARCHAR(255))"
            self.cursor.execute(statement)
            print("Successfully created table")
            print(self.cursor._executed)
        except database.Error as e:
            print(f"Error creating table: {e}")

    # def add_new_transaction(self, , last_name):
    def add_new_transaction(self, bank_name, account_id, action, amount, month, day, hour, minute, balance):
        try:
            statement = f"INSERT INTO {self.table_name} (bank_name, account_id, action, amount, month, day, hour, minute, balance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (bank_name, account_id, action, amount, month, day, hour, minute, balance)
            self.cursor = self.connection.cursor()
            self.cursor.execute(statement, data)
            print(self.cursor._executed)
            self.connection.commit()
            print("Successfully added entry to database")
            return self.cursor.lastrowid
        except database.Error as e:
            print(f"Error adding entry to database: {e}")

    def transaction_exists(self, transaction_id):
        try:
            statement = f"SELECT * FROM {self.table_name} WHERE id={transaction_id}"
            self.cursor = self.connection.cursor()
            self.cursor.execute(statement)
            print(self.cursor._executed)
            result = self.cursor.fetchone()
            if result:
                return True
            return False
        except database.Error as e:
            print(f"Error checking if transaction exists: {e}")
        finally:
            self.cursor.close()

    def add_reason(self, transaction_id, reason):
        try:
            if not self.transaction_exists(transaction_id):
                return -1
            statement = f"UPDATE {self.table_name} SET reason=%s WHERE id=%s"
            data = (reason, transaction_id)
            self.cursor = self.connection.cursor()
            self.cursor.execute(statement, data)
            print(self.cursor._executed)
            self.connection.commit()
            print("Successfully updated entry in database")
            return self.cursor.lastrowid
        except database.Error as e:
            print(f"Error updating entry in database: {e}")

    def get_all_transactions(self):
        try:
            statement = f"SELECT * FROM {self.table_name}"
            self.cursor = self.connection.cursor()
            self.cursor.execute(statement)
            print(self.cursor._executed)
            print("Successfully retrieved entries from database")
            output = []
            for (id, date_created, bank_name, account_id, action, amount, month, day, hour, minute, balance, reason) in self.cursor:
                transaction = {
                    "id": id,
                    "date_created": date_created,
                    "bank_name": bank_name,
                    "account_id": account_id,
                    "action": action,
                    "amount": amount,
                    "month": month,
                    "day": day,
                    "hour": hour,
                    "minute": minute,
                    "balance": balance,
                    "reason": reason
                }
                output.append(transaction)
            return output
        except database.Error as e:
            print(f"Error retrieving entries from database: {e}")
    def get_data(self, last_name):
        try:
            statement = f"SELECT first_name, last_name FROM employees WHERE last_name='{last_name}'"
            print("getting data using statement: ", statement)
            self.cursor = self.connection.cursor()
            self.cursor.execute(statement)
            print(self.cursor._executed)
            print("Successfully retrieved entry from database")
            output = []
            for (first_name, last_name) in self.cursor:
                output.append(f"{first_name}, {last_name}")
            return output
        except database.Error as e:
            print(f"Error retrieving entry from database: {e}")

    def update_data(self, first_name, last_name):
        try:
            statement = "UPDATE employees SET first_name=%s WHERE last_name=%s"
            data = (first_name, last_name)
            self.cursor.execute(statement, data)
            print(self.cursor._executed)
            self.connection.commit()
            print("Successfully updated entry in database")
        except database.Error as e:
            print(f"Error updating entry in database: {e}")
    
    def close_connection(self):
        print("WARNING: Closing connection to database")
        self.connection.close()