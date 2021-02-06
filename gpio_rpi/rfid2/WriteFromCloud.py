# https://pypi.org/project/mfrc522/
from time import sleep
import sys
from RPi import GPIO
from gpiozero import Buzzer
from mfrc522 import SimpleMFRC522
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# firebase
cred = credentials.Certificate('../../firebase/firebase_key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iotfb-fc0b9.firebaseio.com/'
})

reader = SimpleMFRC522()
GPIO.setwarnings(False)
buzzer = Buzzer(16)

try:
    while True:
        print('Now place your tag to write.')
        id, text = reader.read()
        text = db.reference('/smarthouse/servo/' + str(id)).get()
        #reader.write(text)
        print(text)
        reader.write(str(text))

        # https://gpiozero.readthedocs.io/en/stable/api_output.html
        # beep(on_time=1, off_time=1, n=None, background=True)
        buzzer.beep(0.1, 0.1, 1)
        print('Written OK')
        sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise