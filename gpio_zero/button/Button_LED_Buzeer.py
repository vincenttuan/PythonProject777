from gpiozero import Button, LED, Buzzer
from signal import pause
from time import sleep

led = LED(21)
button = Button(20, pull_up=False)
buzeer = Buzzer(16)

def on():
    led.on()
    print(3.3)
    buzeer.on()

def off():
    led.off()
    print(0)
    buzeer.off()

button.when_pressed = on
button.when_released = off

pause()