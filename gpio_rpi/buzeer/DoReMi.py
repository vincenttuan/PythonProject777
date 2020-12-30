import time
import RPi.GPIO as GPIO

def doReMi():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT) # GPIO.PWM(channel, frequency)
    p = GPIO.PWM(16, 50)
    p.start(15) # 代表占空比（范围：0.0 <= dc >= 100.0）

    print("Do")
    p.ChangeFrequency(523)
    time.sleep(1)

    print("Re")
    p.ChangeFrequency(587)
    time.sleep(1)

    print("Mi")
    p.ChangeFrequency(659)
    time.sleep(1)

    p.stop()
    GPIO.cleanup()


doReMi()