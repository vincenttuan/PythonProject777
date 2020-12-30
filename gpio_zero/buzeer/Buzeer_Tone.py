from gpiozero import TonalBuzzer
import time
b = TonalBuzzer(16)
i=220
while True:
    i=i+20
    b.play(i)
    time.sleep(1)