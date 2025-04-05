from flask import Flask, request
from flask_socketio import SocketIO, send
from flask_cors import CORS
from Crypto.Cipher import AES
import base64
import json

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="https://socket-chat-frontend-gold.vercel.app")

AES_SECRET = b'ThisIsASecretKey123'  

def pad(s): return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
def unpad(s): return s[:-ord(s[len(s)-1:])]

def decrypt_aes(ciphertext_b64):
    raw = base64.b64decode(ciphertext_b64)
    cipher = AES.new(AES_SECRET, AES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(raw)).decode()
    return decrypted

def encrypt_aes(plaintext):
    cipher = AES.new(AES_SECRET, AES.MODE_ECB)
    padded = pad(plaintext)
    encrypted = cipher.encrypt(padded.encode())
    return base64.b64encode(encrypted).decode()

@app.route('/')
def index():
    return "Socket Server is Running"

@socketio.on('message')
def handle_message(msg):
    print(f"[RECEIVED] {msg}")
    try:
        data = json.loads(msg)
        send(msg, broadcast=True)
        print("[SENT]")
    except Exception as e:
        print("[ERROR]", e)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
