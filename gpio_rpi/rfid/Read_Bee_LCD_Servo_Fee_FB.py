# https://pypi.org/project/mfrc522/
from time import sleep
from gpiozero import Buzzer, Servo
from RPi import GPIO
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# firebase
cred = credentials.Certificate('../../firebase/firebase_key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iotfb-fc0b9.firebaseio.com/'
})

# Servo 設定要先寫
myGPIO = 19
myCorrection = 0
maxPW = (2.0 + myCorrection) / 1000
minPW = (1.0 - myCorrection) / 1000
servo = Servo(myGPIO, min_pulse_width=minPW, max_pulse_width=maxPW)

reader = SimpleMFRC522()
GPIO.setwarnings(False)
buzzer = Buzzer(16)
lcd = CharLCD(i2c_expander='PCF8574', address=0x27)


def close():
    for value in range(0, 21):
        value2 = (float(value) - 10) / 10
        servo.value = value2
        print(value2)
        sleep(0.05)


def open():
    for value in range(20, -1, -1):
        value2 = (float(value) - 10) / 10
        servo.value = value2
        print(value2)
        sleep(0.05)


def lcd_print(id, text):
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("{x}".format(x=id))
    lcd.cursor_pos = (1, 0)
    lcd.write_string("{x}".format(x=text))


if __name__ == '__main__':
    servo.value = 1.0
    try:
        lcd.clear()
        while True:
            print("Hold a tag near the reader")
            id, text = reader.read()
            go = int(text) >= 50
            if go:
                fee = 50
                text = str(int(text) - fee)
                reader.write(text)
                lcd_print(id, text)
                buzzer.beep(0.1, 0.1, 1)
                open()
                sleep(2)
                close()
                sleep(1)
                db.reference('/smarthouse/rfid/'+str(id)).set(int(text))

            else:
                lcd_print(id, text)
                buzzer.beep(0.1, 0.1, 1)
                sleep(0.2)
                buzzer.beep(0.1, 0.1, 1)
                sleep(0.2)
                buzzer.beep(0.1, 0.1, 1)

            print("ID: %s\nText: %s" % (id, text))
            sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()
        raise