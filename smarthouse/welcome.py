import RPi.GPIO as GPIO
import dht11 # 直接按右鍵即可安裝
import time
import firebase_admin

from RPLCD.i2c import CharLCD
from gpiozero import Button, LED, Buzzer
from signal import pause
from firebase_admin import credentials
from firebase_admin import db

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# pin setup
led = LED(21)
button = Button(20, pull_up=False)
buzeer = Buzzer(16)
instance = dht11.DHT11(pin=26)

# PCF8574 PCF8574T 是 I2C 擴展模組
lcd = CharLCD(i2c_expander='PCF8574', address=0x27)

# Firebase setup
cred = credentials.Certificate("../firebase/firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iotfb-fc0b9.firebaseio.com/'
})

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

def dhtDetect():
    result = instance.read()
    if result.is_valid():
        print("Temperature: %-3.1f C" % result.temperature)
        print("Humidity: %-3.1f %%" % result.humidity)
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("{x}:{y} C".format(x="Temp", y=result.temperature))
        lcd.cursor_pos = (1, 0)
        lcd.write_string("{x}:{y} %".format(x="Humi", y=result.humidity))
        db.reference('/smarthouse/dht/temp').set(result.temperature)
        db.reference('/smarthouse/dht/humi').set(result.humidity)
    else:
        print("Error: %d" % result.error_code)
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("{x}:{y}".format(x="Error", y=result.error_code))
    time.sleep(1)
    dhtDetect()


db.reference('/smarthouse/led/onefloor').listen(listener)
button.when_pressed = on
button.when_released = off
dhtDetect()

pause()
