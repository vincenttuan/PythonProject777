import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iotfb-fc0b9.firebaseio.com/'
})

def listener(event):
    print("age=", event.data)

# 監聽 age 資料
db.reference('/company/edu/age').listen(listener)