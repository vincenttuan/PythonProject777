# -*- coding: utf-8 -*-
'''
安裝 RPLCD 套件
pip3 install RPLCD

(可以不用裝)安裝 smbus2 套件 (支援 I2C 功能)
pip3 install smbus2

確認 RPLCD, smbus2 套件皆已正確安裝
pip3 list

尋找 I2C 裝置的位址
i2cdetect -y 1

LCM1602 IIC V1 接腳	Raspberry Pi GPIO 腳位
GND	實體編號 6 (接地)
VCC	實體編號 4 (+5V)
SDA	實體編號 3
SCL	實體編號 5
'''

import sys

from RPLCD.i2c import CharLCD

# PCF8574 PCF8574T 是 I2C 擴展模組
lcd = CharLCD(i2c_expander='PCF8574', address=0x27)

lcd.clear()
lcd.cursor_pos = (0, 0)
lcd.write_string("{x} {y}".format(x="Raspberry", y="Pi"))
lcd.cursor_pos = (1, 0)
lcd.write_string("{}".format(str(sys.version_info[0]) + '.' + str(sys.version_info[1]) + '.' + str(sys.version_info[2])))
print(sys.version_info)
