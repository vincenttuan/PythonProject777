import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iotfb-fc0b9.firebaseio.com/'
})

data = db.reference('/company').get()
print(data)
data = db.reference('/company/edu').get()
print(data)
data = db.reference('/company/edu/age').get()
print(data)
data = db.reference('/company/edu/name').get()
print(data)