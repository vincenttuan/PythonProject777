from gpiozero import Button, LED, Buzzer
from signal import pause
from time import sleep
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("../../firebase/firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iotfb-fc0b9.firebaseio.com/'
})
# Relay 接法
# IN1 -> 21, GND -> 負極, VCC -> 5V
led = LED(21)
button = Button(20, pull_up=False)
buzeer = Buzzer(16)

def on():
    led.on()
    print(3.3)
    buzeer.on()
    db.reference('/smarthouse/led/onefloor').set(1)

def off():
    led.off()
    print(0)
    buzeer.off()
    db.reference('/smarthouse/led/onefloor').set(0)

def listener(event):
    data = event.data
    if data == 1:
        led.on()
    else:
        led.off()

db.reference('/smarthouse/led/onefloor').listen(listener)
button.when_pressed = on
button.when_released = off

pause()