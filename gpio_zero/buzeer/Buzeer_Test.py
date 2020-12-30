from gpiozero import Buzzer
from time import sleep

buzeer = Buzzer(16) # 長針接 GPIO #16, 短針接 GND

for i in range(5):
    buzeer.on()
    sleep(1)
    buzeer.off()
    sleep(1)