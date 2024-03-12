from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('sit.html')

@socketio.on('accident')
def handle_message(msg):
    print("accident")
    socketio.emit('message', msg)
    
@socketio.on('connect')
def handle_connect():
    print(f"Client connected with SID: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected with SID: {request.sid}")


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0")
