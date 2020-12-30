import RPi.GPIO as GPIO
from time import sleep

button_pin = 20
GPIO.setmode(GPIO.BCM)

# 接 GND + GPIO 20
# GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# 接 3.3 + GPIO 20
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    button_status = GPIO.input(button_pin)
    print(button_status)
    sleep(0.05)