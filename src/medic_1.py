from libs.hx711_mult import *
from time import sleep_ms
from libs.sdcard_helper import SD
from time import ticks_ms
import machine

# La idea es ver como varian las mediciones de peso durante un tiempo largo
# Queme la balanza 4, conectada al slot 1

led = machine.Pin(22, Pin.OUT)
led.value(0)

def measure(fname: str):
    slot_to_scale_mapping = [
        3,
        0,
        7,
        None,
        5,
        None,
    ]

    n_measurements_per_cycle = 50
    curr_measurements_in_cycle = 0
    curr_cycle = 0

    scale_n = [0]*n_measurements_per_cycle
    raw_times = [0]*n_measurements_per_cycle
    raw_means = [0]*n_measurements_per_cycle
    raw_stdevs = [0]*n_measurements_per_cycle

    while True:
        for scale, slot in enumerate(slot_to_scale_mapping):
            if slot is None: continue

            led.value(0)
            res = get_value_raw_stats(slot, 30)
            led.value(1)

            mean = None if res is None else res[0]
            stdev = None if res is None else res[1]

            scale_n[curr_measurements_in_cycle] = scale+1
            raw_times[curr_measurements_in_cycle] = ticks_ms()
            raw_means[curr_measurements_in_cycle] = mean
            raw_stdevs[curr_measurements_in_cycle] = stdev

            print(f"({scale+1}, {raw_times[curr_measurements_in_cycle]}, {mean}, {stdev}) - {curr_measurements_in_cycle}, {curr_cycle}")
            curr_measurements_in_cycle += 1

            if curr_measurements_in_cycle >= n_measurements_per_cycle:
                s = "time;scale;mean;stdev\n"
                for i in range(n_measurements_per_cycle):
                    n = scale_n[i]
                    t = raw_times[i]
                    m = raw_means[i]
                    e = raw_stdevs[i]
                    s += f'{n};{t};{m};{e}\n'

                file = f'{fname}{curr_cycle}.TXT'
                with SD() as sd:
                    if sd is None:
                        with open(file, "w") as f:
                            f.write(s)
                    else:
                        with sd.open(file, "w") as f:
                            f.write(s)
                curr_cycle += 1
                curr_measurements_in_cycle = 0

def run_0():
    print("Running zero")
    try:
        measure('TAR')
    except Exception as e:
        print(e)
    finally:
        hx.power_off()

def run_weight():
    print("Running weight")
    try:
        measure('W')
    except Exception as e:
        print(e)
    finally:
        hx.power_off()
