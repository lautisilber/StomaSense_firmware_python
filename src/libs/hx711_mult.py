from machine import Pin
from micropython import const
from .hx711_single import hx711

sck_pin = Pin(16, Pin.OUT)
dt_pin = Pin(17, Pin.IN)

mux_pin_1 = Pin(5, Pin.OUT)
mux_pin_2 = Pin(6, Pin.OUT)
mux_pin_3 = Pin(7, Pin.OUT)
mux_pin_4 = Pin(4, Pin.OUT)

hx = hx711(sck_pin=sck_pin, dat=dt_pin)
hx.set_gain(hx711.gain.gain_128)

# could be hx711.rate.rate_80
rate = hx711.rate.rate_10

timeout_us = const(5_000_000)

binary_table = (
    (0, 0, 0, 0),
    (0, 0, 0, 1),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 1, 0, 0),
    (0, 1, 0, 1),
    (0, 1, 1, 0),
    (0, 1, 1, 1),
    (1, 0, 0, 0),
    (1, 0, 0, 1),
    (1, 0, 1, 0),
    (1, 0, 1, 1),
    (1, 1, 0, 0),
    (1, 1, 0, 1),
    (1, 1, 1, 0),
    (1, 1, 1, 1)
)

n_slots = const(16)

assert(len(binary_table) == n_slots)

def set_slot(slot: int) -> None:
    if slot < 0 or slot >= n_slots:
        raise Exception(f"slot number {slot} isn't in the accepted range [0,{n_slots}]")
    states = binary_table[slot]
    mux_pin_1.value(states[0])
    mux_pin_2.value(states[1])
    mux_pin_3.value(states[2])
    mux_pin_4.value(states[3])

def get_value_raw(slot: int) -> int | None:
    global hx, rate, timeout_us
    set_slot(slot)
    hx711.wait_settle(rate)
    val = hx711.get_value_timeout(timeout_us)
    return val

# calibration consists of 4 numbers: offset, slope and their respective errors
calibrations = [[0]*4]*n_slots

# TODO: finish implementing calibration of balanzas
