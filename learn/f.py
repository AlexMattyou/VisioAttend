from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return 'ram sam sam'

# Event for handling new connections
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# Event for handling disconnections
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)