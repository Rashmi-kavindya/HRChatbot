# app.py

from flask import Flask, request, jsonify, render_template
from db_utils import connect_db
from chatbot_rules import get_hr_response
from db_response import get_db_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    emp_id = request.json.get('emp_id', '1001')
    response = get_hr_response(user_input)

    if response == "I'm sorry, I couldn't understand that. Can you please rephrase?":
        response = get_db_response(user_input, emp_id)

    # Save to DB
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_log (user_input, bot_response) VALUES (%s, %s)", (user_input, response))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
