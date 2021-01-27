# https://pypi.org/project/mfrc522/
# 安裝 rfid
# pip3 install mfrc522

from time import sleep
import sys
from RPi import GPIO
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        print("ID: %s\nText: %s" % (id, text))
        sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise