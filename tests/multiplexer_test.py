from machine import Pin
from time import sleep_ms

binary_table = (
    (0, 0, 0, 0),
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (1, 1, 0, 0),
    (0, 0, 1, 0),
    (1, 0, 1, 0),
    (0, 1, 1, 0),
    (1, 1, 1, 0),
    (0, 0, 0, 1),
    (1, 0, 0, 1),
    (0, 1, 0, 1),
    (1, 1, 0, 1),
    (0, 0, 1, 1),
    (1, 0, 1, 1),
    (0, 1, 1, 1),
    (1, 1, 1, 1),
)

sck_pin = Pin(16, Pin.OUT)
dt_pin = Pin(17, Pin.IN)

mux_pin_1 = Pin(5, Pin.OUT)
mux_pin_2 = Pin(6, Pin.OUT)
mux_pin_3 = Pin(7, Pin.OUT)
mux_pin_4 = Pin(4, Pin.OUT)

HX_MULT_INDEX = 0

def main():
    mux_pin_1(binary_table[HX_MULT_INDEX][0])
    mux_pin_2(binary_table[HX_MULT_INDEX][1])
    mux_pin_3(binary_table[HX_MULT_INDEX][2])
    mux_pin_4(binary_table[HX_MULT_INDEX][3])
    print(binary_table[HX_MULT_INDEX])
    
    while True:
        sck_pin.toggle()
        sleep_ms(750)
main()