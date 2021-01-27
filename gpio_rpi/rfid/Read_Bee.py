# https://pypi.org/project/mfrc522/
from time import sleep
from gpiozero import Buzzer
from RPi import GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
GPIO.setwarnings(False)
buzzer = Buzzer(16)

try:
    while True:
        print("Hold a tag near the reader")
        id, text = reader.read()
        # https://gpiozero.readthedocs.io/en/stable/api_output.html
        # beep(on_time=1, off_time=1, n=None, background=True)
        buzzer.beep(0.1, 0.1, 1)
        print("ID: %s\nText: %s" % (id, text))
        sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise