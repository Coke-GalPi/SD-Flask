from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from config.mongodb import mongo
from services.crudUser import *
from services.crudContact import *
from services.crudMessage import *
from flask_socketio import SocketIO, send, join_room, leave_room
from cryptography.fernet import Fernet
import base64

import os

# Cargamos la variable de ambiente
load_dotenv()

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

# Creamos el servidor para Socketio
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

# Agregamos la variable de ambiente a la app
print(os.getenv('MONGO_URI'))
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)

# Generar una clave secreta
key = Fernet.generate_key()
# Convertir la clave a un formato seguro para enviarla al cliente
secure_key = base64.urlsafe_b64encode(key).decode()
# Inicializar el objeto Fernet con la clave generada
cipher_suite = Fernet(key)

# Definimos una ruta y una función de vista index
@app.route('/')
def index():
    return render_template('index.html')

# Definimos una ruta y una función de vista signin (Login)
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    #if 'username' in session:
    #    return redirect(url_for('user'))
    if request.method == 'POST':
        username = request.form.get('username')
        if user_Auth():
            session['username'] = username
            return redirect(url_for('user'))
    return render_template('signin.html')

# Aquí iría tu lógica de cierre de sesión
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Definimos una ruta y una función de vista signup (Registro)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if create_newUser():
        return render_template('signup.html')
    else:
        return render_template('signup.html')

# Definimos una ruta y una función de vista del usuario
@app.route('/user', methods=['GET', 'POST'])
def user():
    if 'username' not in session:
        return redirect(url_for('signin'))
    datos_user = getUser(session['username'])
    if datos_user:
        idUserSession = str(datos_user['_id'])
        datos_contact = getContactUser(idUserSession)
        contactos = {contacto['userNewAdd']: contacto for contacto in datos_contact}
        data = {
            'idUser': idUserSession,
            'username': session['username'],
            'contactos': contactos
        }
        return render_template('users.html', data=data)
    else:
        return redirect(url_for('signin'))

@app.route('/addUser', methods=['POST'])
def addUser():
    if request.method == 'POST':
        if addNewContact():
            return redirect(url_for('user'))
    return redirect(url_for('user'))
@app.route('/deleteUser', methods=['POST'])
def deleteUser():
    if request.method == 'POST':
        if deleteContact():
            return redirect(url_for('user'))
    return redirect(url_for('user'))

# Definimos una ruta y una funcion de vista chat
@app.route('/chat/<id>')
def chat(id):
    datos = getUserID(id)
    datoOpen  = getUser(session['username'])
    data = {
            'IDOpen': datoOpen['_id'],
            'nameOpen': datoOpen['name'],
            'usernameOpen': datoOpen['username'],
            'name': str(datos['name']),
            'surname': str(datos['surname']),
            'username': str(datos['username']),
        }
    return render_template('chat.html', data=data)

# Definimos una ruta y una función de vista Error
@app.route('/error')
def error():
    return render_template('error.html')

@socketio.on('message')
def handleMessage(msg):
    send(msg, broadcast=True)

@socketio.on('private_message')
def handle_private_message(data):
    recipient = data['recipient']
    message = data['message']
    sender = data['sender']
    room_participants = sorted([sender, recipient])
    room = f"{room_participants[0]}-{room_participants[1]}"
    join_room(room)
    
    # Cifrar el mensaje antes de enviarlo
    #encrypted_message = cipher_suite.encrypt(message.encode('utf-8')).decode('utf-8')
    
    socketio.emit('message', {'username': sender, 'message': message}, room=room)
    message_data = {
        'room': room,
        'sender': sender,
        'recipient': recipient,
        'message': message,  # Guardar el mensaje cifrado en la base de datos
        'room': room
    }
    saveChatRoom(message_data)

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)