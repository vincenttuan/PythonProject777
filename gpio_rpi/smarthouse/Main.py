# https://pypi.org/project/mfrc522/
import threading
from time import sleep
from gpiozero import Buzzer, Servo, LED, Button
from RPi import GPIO
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import dht11

# firebase
cred = credentials.Certificate('../../firebase/firebase_key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iotfb-fc0b9.firebaseio.com/'
})

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Servo 設定要先寫
myCorrection = 0
maxPW = (2.0 + myCorrection) / 1000
minPW = (1.0 - myCorrection) / 1000
servo1 = Servo(19, min_pulse_width=minPW, max_pulse_width=maxPW)
servo2 = Servo(13, min_pulse_width=minPW, max_pulse_width=maxPW)
servos = {631257378948: servo1, 6141524804: servo2}
servo = 0

# Button
button = Button(20, pull_up=False)

#LED
led = LED(21)

#DHT11
instance = dht11.DHT11(pin = 26)

reader = SimpleMFRC522()
GPIO.setwarnings(False)
buzzer = Buzzer(16)
lcd = CharLCD(i2c_expander='PCF8574', address=0x27)

# 關門
def close():
    for value in range(0, 21):
        value2 = (float(value) - 10) / 10
        servo.value = value2
        print(value2)
        sleep(0.05)

# 開門
def open():
    for value in range(20, -1, -1):
        value2 = (float(value) - 10) / 10
        servo.value = value2
        print(value2)
        sleep(0.05)

def rfid_lcd_print(id, text):
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("{x}".format(x=id))
    lcd.cursor_pos = (1, 0)
    lcd.write_string("{x}".format(x=text))

#偵測溫溼度
def detect_dht11():
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

#監聽 FB 上的 /smarthouse/led/onefloor
def listener_led(event):
    data = event.data
    if data == 1:
        led.on()
    else:
        led.off()
    print(data)

#監聽 FB 上的 /smarthouse/servo/12345678
def listener_servo(event):
    if servo == 0:
        return 0

    data = event.data
    if data == 1:
        open()
    else:
        close()
    print(data)

#按鈕按下
def button_pressed():
    pass

#按鈕放開
def button_released():
    pass

#執行緒(每2秒針測DHT11乙次)
def thread_job():
    while 1:
        print("detect_dht11")
        detect_dht11()
        sleep(2)

#主程式
if __name__ == '__main__':
    servo1.value = 1.0
    servo2.value = 1.0

    button.when_pressed = button_pressed
    button.when_released = button_released

    # 建立一個子執行緒 (偵測 DHT11)
    t = threading.Thread(target=thread_job)
    # 執行該子執行緒
    t.start()

    # 監聽 FB
    db.reference('/smarthouse/led/onefloor').listen(listener_led)
    db.reference('/smarthouse/servo/12345678').listen(listener_servo)

    # RFID
    try:
        lcd.clear()
        while True:
            print("Hold a tag near the reader")
            id, text = reader.read()
            servo = servos[id]  # 根據 卡片 id 取得 servo
            go = int(text) >= 50
            if go:
                fee = 50
                text = str(int(text) - fee)
                reader.write(text)
                rfid_lcd_print(id, text)
                buzzer.beep(0.1, 0.1, 1)
                open()
                sleep(2)
                close()
                sleep(1)
                db.reference('/smarthouse/rfid/'+str(id)).set(int(text))

            else:
                rfid_lcd_print(id, text)
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