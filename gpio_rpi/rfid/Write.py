# https://pypi.org/project/mfrc522/
from time import sleep
import sys
from RPi import GPIO
from gpiozero import Buzzer
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
GPIO.setwarnings(False)
buzzer = Buzzer(16)

try:
    while True:
        text = input("Please input message: ")
        print('Now place your tag to write.')
        reader.write(text)
        buzzer.beep(0.1, 0.1, 1)
        print('Written OK')
        sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise