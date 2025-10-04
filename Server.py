from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room
import random, string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'degistir-gerekirse'
socketio = SocketIO(app, cors_allowed_origins="*")

users = {}  # numara -> socket id eşleştirmesi

def generate_number():
    return ''.join(random.choices(string.digits, k=6))

@app.route('/register', methods=['POST'])
def register():
    number = generate_number()
    return jsonify({'number': number})

@socketio.on('join')
def on_join(data):
    num = data.get('number')
    if num:
        users[num] = request.sid
        join_room(num)
        print(f"{num} bağlandı.")

@socketio.on('send_message')
def on_send(data):
    to = data.get('to')
    sender = data.get('from')
    payload = data.get('payload')
    if to in users:
        emit('message', {'from': sender, 'payload': payload}, room=to)
    else:
        emit('error', {'msg': 'Kullanıcı çevrimdışı.'}, room=sender)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=10000)
