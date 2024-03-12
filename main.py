from datetime import datetime
from flask import Flask, request, jsonify
import MetaTrader5 as mt5

app = Flask(__name__)

def login_data():
    login_data = request.get_json()
    login = login_data.get('login')
    password = login_data.get('password')
    server = login_data.get('server')
    
    return login, password, server

def login_error():
    return jsonify({'success': False, 'message': 'Missing login credentials'})
    
def mt5_login(login: str, password: str, server: str):        
    # Connect to MetaTrader 5
    if not mt5.initialize(login=int(login), server=server, password=password):
        return False, None
    else:
        account_info = mt5.account_info()
        return True, str(account_info)    
    
def mt5_get_deals():
    from_date = datetime(2020,1,1)
    to_date = datetime(2025,1,1)
    deals = mt5.history_deals_get(from_date, to_date)
    return str(deals)

def mt5_get_orders():
    from_date = datetime(2020,1,1)
    to_date = datetime(2025,1,1)
    orders = mt5.history_orders_get(from_date, to_date)
    return str(orders)

# ---------- Flask routes ----------
@app.route('/account', methods=['POST'])
def login():
    login, password, server = login_data()
    
    if not login or not password or not server:
        return login_error()
    
    success, account_info = mt5_login(login, password, server)
    
    return jsonify({'success': success, 'account': account_info})

@app.route('/history', methods=['POST'])
def orders():
    login, password, server = login_data()

    if not login or not password or not server:
        return login_error()
    
    mt5_login(login, password, server)
    deals = mt5_get_deals()
    orders = mt5_get_orders()
    
    return jsonify({'success': True, 'deals': deals , 'orders': orders })

if __name__ == '__main__':
    app.run(debug=True)
