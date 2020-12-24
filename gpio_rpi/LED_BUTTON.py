# 按下 BUTTON 會亮燈
# 放開 BUTTON 會熄滅
import RPi.GPIO as GPIO
from time import sleep

led_pin = 21
button_pin = 20
GPIO.setmode(GPIO.BCM)

GPIO.setup(led_pin, GPIO.OUT)
# 接 3.3 + GPIO 20
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    button_status = GPIO.input(button_pin)
    if button_status:
        print(button_status)
        GPIO.output(led_pin, True)
    else:
        print(button_status)
        GPIO.output(led_pin, False)
    sleep(0.05)