from flask import request
from config.mongodb import mongo
from bson import json_util, ObjectId

def addNewContact():
    data = request.form
    idUserSession = data.get('idUser', None)
    usernameNewAdd = data.get('userSearch', None)
    if usernameNewAdd:
        datos = mongo.db.Users.find_one({'username': usernameNewAdd})
        if data:
            result = mongo.db.Contacts.insert_one({
                'idUserSession': idUserSession,
                'idUserAdd': datos['_id'],
                'userNewAdd': usernameNewAdd
            })
            return result, 200
    else:
        return {'error': 'Invalid payload'}, 400 

def deleteContact():
    data = request.form
    deleteID = data.get('deleteID', None)
    if deleteID:
        if mongo.db.Contacts.delete_one({'_id': ObjectId(deleteID)}):
            return True
        else:
            return False
    else:
        return False

def getContactUser(id):
    data = mongo.db.Contacts.find({'idUserSession': id})
    return data