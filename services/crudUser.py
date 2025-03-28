from flask import request, Response
from config.mongodb import mongo
from bson import json_util, ObjectId
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

def check_password(password, password_hash):
    if check_password_hash(password_hash, password):
        return True
    else: 
        return False

# Función para el registro de usuarios
def create_newUser():
    # Usamos request.form para obtener los datos del formulario
    data = request.form
    name = data.get('name')
    surname = data.get('surname', None)
    username = data.get('username', None)
    password = data.get('password', None)
    if name and username and password:
        # Encriptar la contraseña
        hashed_password = generate_password_hash(password)
        response = mongo.db.Users.insert_one({
            'name': name,
            'surname': surname,  # Corregido el error tipográfico
            'username': username,
            'password': hashed_password
        })
        result = {
            'id': str(response.inserted_id),
            'name': name,
            'surname': surname,
            'username': username,
            'password': hashed_password
        }
        # Devuelve un objeto JSON y un código de estado HTTP 200 (OK)
        return result, 200  
    else:
        # Devuelve un objeto JSON y un código de estado HTTP 400 (Bad Request)
        return {'error': 'Invalid payload'}, 400 

def user_Auth():
    # Usamos request.form para obtener los datos del formulario
    datos = request.form
    username = datos.get('username', None)
    password = datos.get('password', None)
    user_data = mongo.db.Users.find_one({'username': username})
    if user_data:
        stored_hash = user_data.get('password', None)
        if stored_hash:
            return check_password(password, stored_hash)
        else:
            return False
    else:
        return False

def getUser(username):
    data = mongo.db.Users.find_one({'username': username})
    return data

def getUserID(id):
    data = mongo.db.Users.find_one({'_id': ObjectId(id)})
    return data