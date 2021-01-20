import RPi.GPIO as GPIO
import dht11 # 直接按右鍵即可安裝
import time
from RPLCD.i2c import CharLCD

'''
https://pypi.org/project/dht11/
'''
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin = 26)

# PCF8574 PCF8574T 是 I2C 擴展模組
lcd = CharLCD(i2c_expander='PCF8574', address=0x27)

def detect():
    result = instance.read()
    if result.is_valid():
        print("Temperature: %-3.1f C" % result.temperature)
        print("Humidity: %-3.1f %%" % result.humidity)

        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("T:{x} H:{y} C".format(x=result.temperature, y=result.humidity))
    else:
        print("Error: %d" % result.error_code)
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("{x}:{y}".format(x="Error", y=result.error_code))
    lcd.cursor_pos = (1, 0)
    lcd.write_string("Time: {}".format(time.strftime("%H:%M:%S")))
try:
    print('按下 Ctrl-C 可停止程式')
    while True:
        detect()
        time.sleep(1)
except KeyboardInterrupt:
    print('關閉程式')
finally:
    lcd.clear()
