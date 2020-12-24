import RPi.GPIO as GPIO
from time import sleep

led_pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
while True:
    GPIO.output(led_pin, True)
    print(3.3)
    sleep(1)
    GPIO.output(led_pin, False)
    print(0)
    sleep(1)


