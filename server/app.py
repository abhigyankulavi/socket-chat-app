from flask import Flask, request
from flask_socketio import SocketIO, send
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

socketio = SocketIO(app, cors_allowed_origins="https://socket-chat-frontend-gold.vercel.app") 

@app.route('/')
def index():
    return "Socket Server is Running"

@socketio.on('message')
def handle_message(msg):
    print(f"[RECEIVED] {msg}")
    ack_msg = f"ACK: {msg}"
    send(ack_msg, broadcast=True)
    print(f"[SENT] {ack_msg}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
