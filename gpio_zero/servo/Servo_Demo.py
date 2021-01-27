# https://www.raspberrypi-spy.co.uk/2018/02/basic-servo-use-with-the-raspberry-pi/

from gpiozero import Servo
from time import sleep

servo = Servo(19)

while True:
    servo.min()
    sleep(2)
    servo.mid()
    sleep(2)
    servo.max()
    sleep(2)
