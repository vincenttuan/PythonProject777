import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iotfb-fc0b9.firebaseio.com/'
})

db.reference('/company').set({
    'edu':{
        'name': '樂技數位學習',
        'age': 18
    }
})

print('ok')
