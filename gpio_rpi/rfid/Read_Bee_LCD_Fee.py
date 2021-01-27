# https://pypi.org/project/mfrc522/
from time import sleep
from gpiozero import Buzzer
from RPi import GPIO
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD

reader = SimpleMFRC522()
GPIO.setwarnings(False)
buzzer = Buzzer(16)
lcd = CharLCD(i2c_expander='PCF8574', address=0x27)

try:
    lcd.clear()
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        buzzer.beep(0.1, 0.1, 1)
        print("ID: %s\nText: %s" % (id, text))

        fee = 10
        text = str(int(text) - fee)
        reader.write(text)
        print("ID: %s\nText: %s" % (id, text))

        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("{x}".format(x=id))
        lcd.cursor_pos = (1, 0)
        lcd.write_string("{x}".format(x=text))
        sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise