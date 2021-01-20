import RPi.GPIO as GPIO
import dht11 # 直接按右鍵即可安裝
import sys
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
result = instance.read()

# PCF8574 PCF8574T 是 I2C 擴展模組
lcd = CharLCD(i2c_expander='PCF8574', address=0x27)

def detect():
    if result.is_valid():
        print("Temperature: %-3.1f C" % result.temperature)
        print("Humidity: %-3.1f %%" % result.humidity)

        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("{x}:{y} C".format(x="Temp", y=result.temperature))
        lcd.cursor_pos = (1, 0)
        lcd.write_string("{x}:{y} %".format(x="Humi", y=result.humidity))
    else:
        print("Error: %d" % result.error_code)
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("{x}:{y}".format(x="Error", y=result.error_code))

detect()