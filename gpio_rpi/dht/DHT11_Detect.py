import RPi.GPIO as GPIO
import dht11  # 直接按右鍵即可安裝
'''
https://pypi.org/project/dht11/
'''
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 26
instance = dht11.DHT11(pin=26)


def detect():
    result = instance.read()
    if result.is_valid():
        print("Temperature: %-3.1f C" % result.temperature)
        print("Humidity: %-3.1f %%" % result.humidity)
    else:
        print("Error: %d" % result.error_code)


detect()
