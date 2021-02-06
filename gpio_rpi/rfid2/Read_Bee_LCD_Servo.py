# https://pypi.org/project/mfrc522/
from time import sleep
from gpiozero import Buzzer, Servo
from RPi import GPIO
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD

# 631257378948, 19
# 6141524804, 13

# Servo 設定要先寫
myCorrection = 0
maxPW = (2.0 + myCorrection) / 1000
minPW = (1.0 - myCorrection) / 1000
servo1 = Servo(19, min_pulse_width=minPW, max_pulse_width=maxPW)
servo2 = Servo(13, min_pulse_width=minPW, max_pulse_width=maxPW)
servos = {631257378948: servo1, 6141524804: servo2}
servo = 0

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


if __name__ == '__main__':
    #servo.value = 1.0
    try:
        lcd.clear()
        while True:
            print("Hold a tag near the reader")
            id, text = reader.read()
            servo = servos[id]  # 根據 卡片 id 取得 servo

            # https://gpiozero.readthedocs.io/en/stable/api_output.html
            # beep(on_time=1, off_time=1, n=None, background=True)
            buzzer.beep(0.1, 0.1, 1)
            print("ID: %s\nText: %s" % (id, text))
            lcd.clear()
            lcd.cursor_pos = (0, 0)
            lcd.write_string("{x}".format(x=id))
            lcd.cursor_pos = (1, 0)
            lcd.write_string("{x}".format(x=text))

            open()
            sleep(2)
            close()
            sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        raise