from time import sleep
from gpiozero import Servo

myGPIO = 19
myCorrection = 0
maxPW = (2.0 + myCorrection) / 1000
minPW = (1.0 - myCorrection) / 1000

servo = Servo(myGPIO, min_pulse_width=minPW, max_pulse_width=maxPW)

while True:

    print("Set value range -1.0 to +1.0")
    for value in range(0, 21):
        value2 = (float(value) - 10) / 10
        servo.value = value2
        print(value2)
        sleep(0.05)

    sleep(2)

    print("Set value range +1.0 to -1.0")
    for value in range(20, -1, -1):
        value2 = (float(value) - 10) / 10
        servo.value = value2
        print(value2)
        sleep(0.05)
    sleep(2)