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
    form_id = data.get('id')
    json_data = data.get('json_data')
    count = data.get('count')
    bot.checkout_form(json_data=json_data, form_id=form_id, count=count)
    return jsonify({'message': 'Checkout Form completed'})

if __name__ == "__main__":
    app.run(debug=True)
