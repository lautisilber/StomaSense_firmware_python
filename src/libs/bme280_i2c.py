from machine import I2C
from .bme280 import *

sda_pin = 8
scl_pin = 9
i2c_nr  = 0

class BME280_I2C(BME280):
    def __init__(self, mode=BME280_OSAMPLE_8):
        global i2c_nr, sda_pin, scl_pin
        i2c = I2C(i2c_nr, sda=sda_pin, scl=scl_pin, freq=100_000)
        super().__init__(mode, BME280_I2CADDR, i2c)