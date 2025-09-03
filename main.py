from infographics.infographics import Infographics
from flask import Flask, request, jsonify
import constants as const

app = Flask(__name__)
bot = None
    
@app.route('/login', methods=['POST'])
def login():
    global bot
    if bot is None:
        bot = Infographics()

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    bot.login_user(username=username, password=password)
    return jsonify({'message': 'Login task completed'})

@app.route('/checkout-form', methods=['POST'])
def checkout_form():
    global bot
    if bot is None:
        return jsonify({'error': 'Selenium instance not initialized'}), 500
    
    data = request.get_json()
    request_data = data.get('request_data')
    json_data = data.get('json_data')
    bot.checkout_form(json_data=json_data, request_data=request_data)
    return jsonify({'message': 'Checkout Form completed'})

@app.route('/ob-class-b-pas', methods=['POST'])
def ob_class_b_pas():
    global bot
    if bot is None:
        return jsonify({'error': 'Selenium instance not initialized'}), 500
    
    data = request.get_json()
    request_data = data.get('request_data')
    json_data = data.get('json_data')
    bot.ob_class_b_pas(json_data=json_data, request_data=request_data)
    return jsonify({'message': 'Run script completed.'})

@app.route('/field-condition', methods=['POST'])
def field_condition():
    global bot
    if bot is None:
        return jsonify({'error': 'Selenium instance not initialized'}), 500
    
    data = request.get_json()
    request_data = data.get('request_data')
    json_data = data.get('json_data')
    bot.field_condition(json_data=json_data, request_data=request_data)
    return jsonify({'message': 'Run script completed.'})

if __name__ == "__main__":
    app.run(debug=True)
