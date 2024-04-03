from flask import request, Response
from config.mongodb import mongo
from bson import json_util

def saveChatRoom(data):
    if data:
        return mongo.db.Messages.insert_one(data) 
    else:
        return {'error': 'Invalid payload'}, 400 

def getChatMessages(id):
    data = mongo.db.Contacts.find({'room': id})
    return data