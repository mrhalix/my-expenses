from flask import Flask, request, jsonify

from db_connector import DatabaseConnector
import os

app = Flask(__name__)

print("Starting app")

db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_DATABASE")
table_name = os.environ.get("DB_TABLE_NAME")
db = DatabaseConnector(db_host, db_port, db_username, db_password, db_name, table_name)


@app.route('/expenses', methods = ['GET', 'POST', 'DELETE'])
def manage_expenses():
    if request.method == 'GET':
        try:
            transactions = db.get_all_transactions()
            return jsonify(transactions)
        except Exception as e:
            return 'Internal Server Error', 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            bank_name = data['bank_name']
            account_id = data['account_id']
            action = data['action']
            amount = data['amount']
            month = data['month']
            day = data['day']
            hour = data['hour']
            minute = data['minute']
            balance = data['balance']
        except KeyError as e:
            return 'Bad Request, missing ' + e.args[0], 400
        action = action.replace('-', 'withdraw').replace('+', 'deposit')
        db_query = db.add_new_transaction(bank_name, account_id, action, amount, month, day, hour, minute, balance)
        return jsonify({'status':'success', 'transaction_id': db_query})

    elif request.method == 'DELETE':
        return 'DELETE'
    else:
        # POST Error 405 Method Not Allowed
        return 'Method Not Allowed', 405

@app.route('/expenses/reason', methods = ['POST'])
def expenses_reason():
    if request.method == 'POST':
        try:
            data = request.get_json()
            transaction_id = data['transaction_id']
            reason = data['reason']
        except KeyError as e:
            return 'Bad Request, missing ' + e.args[0], 400
        db_query = db.add_reason(transaction_id, reason)
        if db_query == -1:
            return 'Bad Request, transaction_id does not exist', 400
        return jsonify({'status':'success'})
    else:
        # POST Error 405 Method Not Allowed
        return 'Method Not Allowed', 405

def main():
    try:
        # app.run(debug=True)
        app.run()
    finally:
        # db.close_connection()
        print('closing app')

if __name__=='__main__':
    main()