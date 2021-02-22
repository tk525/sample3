app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on("tes")
def tes(roomname):
    print('んあああ',roomname)
    return roomname

#namespaceが部屋番号っぽい
@socketio.on('message', namespace='/jimin')
# @socketio.on('message')
def handleMessage(msg, roomname):
	print('['+ roomname +'] Message: ' + msg )
	send(msg,
        broadcast=True,
        # namespace=roomname
    )

# @socketio.on("join", namespace='/jimin')
@socketio.on("join")
def join(roomname):
    print(f"A user is joining. roomname is {roomname}")
    join_room(roomname)