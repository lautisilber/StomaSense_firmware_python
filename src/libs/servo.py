from machine import PWM
from time import sleep_us

servo_pin = 11

period_ns = 20_000_000
freq_hz = 1000 // (period_ns // 1_000_000)

min_duty_ns = 500_000   # represents angle 0
max_duty_ns = 2_700_000 # represents angle 180

pwm = PWM(servo_pin, freq=freq_hz, duty_ns=period_ns) # 19500000

def attach() -> None:
    global pwm
    pwm.init()

def dettach() -> None:
    global pwm
    pwm.deinit()

def clamp(n: int | float, smallest: int | float, biggest: int | float) -> int | float:
    return smallest if n < smallest else biggest if n > biggest else n

def perc_to_duty_ns(perc: float) -> int:
    # Takes in a value in the range [0,1] that represents an
    # angle in the range [0, 180] == [0, pi]
    # then it inverts the duty_ns in such a way that the
    # pwm output is inverted (i.e. duty_ns = 20 becomes 20 ns of low and period - 20 ns of high)
    # because of the inverter transistor used to translate voltages
    global period_ns, min_duty_ns, max_duty_ns
    perc = clamp(perc, 0, 1)                          # clamp
    ns_range = abs(max_duty_ns - min_duty_ns)         # get new range
    non_inv_ns = int(clamp((ns_range * perc) + min_duty_ns, min_duty_ns, max_duty_ns)) # non-inverted ns
    return period_ns - non_inv_ns

pwm_init_flag = False
curr_ns = perc_to_duty_ns(0.5)

def set_angle(perc: float) -> None:
    global pwm, curr_ns, pwm_init_flag
    if not pwm_init_flag:
        pwm.init()
        pwm_init_flag = True
    ns = perc_to_duty_ns(perc)
    pwm.duty_ns(ns)
    curr_ns = ns

def set_angle_slow_blocking(perc: int | float, delay_us: int=5_000, step: int=5_000) -> None:
    global pwm, curr_ns, pwm_init_flag
    final_ns = perc_to_duty_ns(perc)
    if final_ns == curr_ns: return
    direction = int(final_ns > curr_ns) * 2 - 1 # 1 or -1
    if not pwm_init_flag:
        pwm.init()
        pwm_init_flag = True
    for ns in range(curr_ns, final_ns+direction, step*direction):
        pwm.duty_ns(ns)
        sleep_us(delay_us)
    curr_ns = ns

# async

import asyncio

async def set_angle_slow_async(perc: int | float, delay_ms: int=5, step: int=5_000) -> None:
    global pwm, curr_ns, pwm_init_flag
    final_ns = perc_to_duty_ns(perc)
    if final_ns == curr_ns: return
    direction = int(final_ns > curr_ns) * 2 - 1 # 1 or -1
    if not pwm_init_flag:
        pwm.init()
        pwm_init_flag = True
    for ns in range(curr_ns, final_ns+direction, step*direction):
        pwm.duty_ns(ns)
        await asyncio.sleep_ms(delay_ms)
    curr_ns = ns