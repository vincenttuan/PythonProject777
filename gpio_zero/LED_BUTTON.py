from gpiozero import Button, LED
from signal import pause

led = LED(21)
button = Button(20, pull_up=False)

def on():
    led.on()
    print(3.3)

def off():
    led.off()
    print(0)

button.when_pressed = on
button.when_released = off

pause()