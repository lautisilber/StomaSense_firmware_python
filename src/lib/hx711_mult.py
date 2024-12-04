from machine import Pin
from micropython import const
from .hx711_single import HX711
#from libs.hx711_single import HX711
import libs.utils as utils
import libs.serial_comm as serial_comm
import libs.stats as stats

sck_pin = Pin(16, Pin.OUT)
dt_pin = Pin(17, Pin.IN)

mux_pin_1 = Pin(5, Pin.OUT)
mux_pin_2 = Pin(6, Pin.OUT)
mux_pin_3 = Pin(7, Pin.OUT)
mux_pin_4 = Pin(4, Pin.OUT)

hx = HX711(pd_sck=sck_pin, d_out=dt_pin)

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

curr_slot: int | None = None
def set_slot(slot: int) -> None:
    global curr_slot, hx
    if curr_slot is not None and slot == curr_slot:
        return
    hx.power_off()
    if slot < 0 or slot >= n_slots:
        raise Exception(f"slot number {slot} isn't in the accepted range [0,{n_slots}]")
    states = binary_table[slot]
    mux_pin_1.value(states[1])
    mux_pin_2.value(states[2])
    mux_pin_3.value(states[3])
    mux_pin_4.value(states[0])
    curr_slot = slot
    hx.power_on()

def get_value_raw(slot: int) -> int | None:
    global hx, rate, timeout_us
    set_slot(slot)
    #hx.wait_settle(rate)
    val = hx.read()
    return val

def get_value_raw_stats(slot: int, n: int) -> tuple[float, float] | None:
    if n <= 1:
        raw = get_value_raw(slot)
        if raw is None:
            return None
        return raw, -1
    raws = list()
    for i in range(n):
        raw = get_value_raw(slot)
        if raw is None:
            continue
        raws.append(raw)
    return stats.mean_and_stdev(raws)
    

class Calibration:
    def __init__(self, offset: int | None, slope: int | None, offset_e: int | None, slope_e: int | None) -> None:
        self.offset = offset
        self.slope = slope
        self.offset_e = offset_e
        self.slope_e = slope_e

    @property
    def is_ready(self) -> bool:
        for e in (self.offset, self.slope, self.offset_e, self.slope_e):
            if e is None:
                return False
        return True

    def to_list(self) -> list[int] | None:
        if not self.is_ready:
            return None
        return [
            self.offset,
            self.slope,
            self.offset_e,
            self.slope_e
        ]

_N_MODULES = 16
_SAVE_FILE = "CALIB.JSN"

calibration = tuple(Calibration(None, None, None, None) for _ in range(_N_MODULES))

def calibration_from_obj(arr: list) -> bool:
    global calibration

    if not isinstance(arr, list):
        return False
    
    if len(arr) != _N_MODULES:
        return False
    
    for c in arr:
        if not isinstance(c, list):
            return False
        if len(c) != 4:
            return False
        if not all(map(utils.is_number, v)):
            return False

    for i in range(_N_MODULES):
        calibration[i] = Calibration(*tuple(map(int, arr[i])))

    return True

def calibration_to_obj(self) -> list[list[int]] | None:
    global calibration
    if any(not c.is_ready for c in calibration):
        return None
    return [c.to_list() for c in calibration]

def calibration_load() -> bool:
    obj = utils.load_json_sd(_SAVE_FILE)
    if obj is None:
        return None
    return calibration_from_obj(obj)

def calibration_dump() -> bool:
    obj = calibration_to_obj()
    if obj is None:
        return False
    return utils.dump_json_sd(_SAVE_FILE, obj)

def calibrate_slot(slot: int) -> bool:
    print("Remove weight and press enter.")
    serial_comm.read_serial_blocking()



    res = serial_comm.read_serial_blocking()
    if not utils.is_number(res):
        return False




# calibration consists of 4 numbers: offset, slope and their respective errors
#calibrations = [[0]*4]*n_slots

# TODO: finish implementing calibration of balanzas
