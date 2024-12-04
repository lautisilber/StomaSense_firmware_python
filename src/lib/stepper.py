from machine import Pin
from time import sleep_us

step_wave = (
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 0, 1, 0),
    (0, 0, 0, 1)
)

step_normal = (
    (1, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 1),
    (1, 0, 0, 1)
)

step_half = (
    (1, 0, 0, 0),
    (1, 1, 0, 0),
    (0, 1, 0, 0),
    (0, 1, 1, 0),
    (0, 0, 1, 0),
    (0, 0, 1, 1),
    (0, 0, 0, 1),
    (1, 0, 0, 1)
)

selected_step = step_half
curr_step = 0
curr_pos = 0

pin_1 = None
pin_2 = None
pin_3 = None
pin_4 = None

begin_flag = False

def begin(p1: int = 15, p2: int = 14, p3: int = 13, p4: int = 12) -> None:
    global pin_1, pin_2, pin_3, pin_4, begin_flag
    if begin_flag: return
    pin_1 = Pin(p1, Pin.OUT)
    pin_2 = Pin(p2, Pin.OUT)
    pin_3 = Pin(p3, Pin.OUT)
    pin_4 = Pin(p4, Pin.OUT)
    begin_flag = True

def engage() -> None:
    (state_1, state_2, state_3, state_4) = selected_step[curr_step]

    pin_1.value(state_1)
    pin_2.value(state_2)
    pin_3.value(state_3)
    pin_4.value(state_4)

def release() -> None:
    pin_1.value(0)
    pin_2.value(0)
    pin_3.value(0)
    pin_4.value(0)

def choose_step_type(step_type: str, engage_after: bool = True) -> None:
    global selected_step, curr_step
    if step_type == 0:
        selected_step = step_wave
    elif step_type == 1:
        selected_step = step_normal
    elif step_type == 2:
        selected_step = step_half
    else:
        raise Exception(f'step_type should be in range [0,2] but was {step_type}')

    curr_step = 0
    if engage_after:
        engage()

def make_step_forward() -> None:
    global selected_step, curr_step, curr_pos

    curr_step = 0 if curr_step >= len(selected_step) - 1 else curr_step + 1
    engage()
    curr_pos += 1

def make_step_backward() -> None:
    global selected_step, curr_step, curr_pos

    curr_step = len(selected_step) - 1 if curr_step <= 0 else curr_step - 1
    engage()
    curr_pos -= 1

def move_blocking(steps: int, delay_us: int, release_after: bool = True) -> None:
    if steps == 0: return
    cb = make_step_forward if steps > 0 else make_step_backward
    for _ in range(abs(steps)):
        cb()
        sleep_us(delay_us)
    if release_after:
        release()

def move_to_step_blocking(step: int, delay_us, release_after: bool = True) -> None:
    global curr_pos
    move_blocking(step - curr_pos, delay_us, release_after)

# async

import asyncio

async def move_async(steps: int, delay_ms: int, release_after: bool = True) -> None:
    if steps == 0: return
    cb = make_step_forward if steps > 0 else make_step_backward
    for _ in range(abs(steps)):
        cb()
        await asyncio.sleep_ms(delay_ms)
    if release_after:
        release()

async def move_to_step_async(step: int, delay_ms: int, release_after: bool = True) -> None:
    global curr_pos
    await move_async(step - curr_pos, delay_ms, release_after)
    