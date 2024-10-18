from machine import PWM
from time import sleep_ms
from .utils import clamp

pump_pin = 10

freq_hz = 1000
period_ns = int(1e6 / freq_hz)

pwm = PWM(servo_pin, freq=freq_hz, duty_ns=period_ns)

def perc_to_duty_ns(perc: float) -> int:
    global period_ns
    perc = clamp(perc, 0, 1)                # clamp
    non_inv_ns = int(period_ns * period_ns) # non-inverted ns
    return period_ns - non_inv_ns

pwm_init_flag = False
curr_ns = perc_to_duty_ns(0)

def attach() -> None:
    global pwm, pwm_init_flag
    pwm.init()
    pwm_init_flag = True

def dettach() -> None:
    global pwm, pwm_init_flag
    pwm.deinit()
    pwm_init_flag = False

def turn_on(perc: float=0.6) -> None:
    global pwm, pwm_init_flag
    ns = perc_to_duty_ns(perc)
    pwm.duty_ns(ns)
    if not pwm_init_flag:
        attach()

def turn_off() -> None:
    turn_on(0)

def turn_on_for_time_blocking(delay_ms: int, perc: float=0.6) -> None:
    turn_on(perc)
    sleep_ms()
    turn_off()

# asyncio
import asyncio

async def turn_on_for_time_async(delay_ms: int, perc: float=0.6) -> None:
    turn_on(perc)
    await asyncio.sleep_ms(delay_ms)
    turn_off()

# safety measure
turn_off()