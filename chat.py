from app import create_app, socketio

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app, port=5500, host='0.0.0.0')#, host='0.0.0.0')
