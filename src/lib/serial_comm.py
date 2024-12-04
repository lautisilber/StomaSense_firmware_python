import sys
import select
import asyncio
from time import sleep_ms, ticks_ms, ticks_diff

def read_serial() -> str | None:
    if select.select([sys.stdin],[],[],0)[0]:
        # TODO: check that this reads until it finds a new line!!
        ch = sys.stdin.readline()
        return ch
    return None

def read_serial_blocking(timeout_ms: int = 0, polling_rate_ms: int = 1000) -> str | None:
    if timeout_ms > 0:
        start_time = ticks_ms()
    res = read_serial()
    while res is None:
        if timeout_ms > 0:
            if ticks_diff(ticks_ms(), start_time) > timeout_ms:
                break
        sleep_ms(polling_rate_ms)
        res = read_serial()
    return res

async def read_serial_async(timeout_ms: int = 0, polling_rate_ms: int = 1000) -> str | None:
    if timeout_ms > 0:
        start_time = ticks_ms()
    res = read_serial()
    while res is None:
        if timeout_ms > 0:
            if ticks_diff(ticks_ms(), start_time) > timeout_ms:
                break
        asyncio.sleep_ms(polling_rate_ms)
        res = read_serial()
    return res

if __name__ == "__main__":
    print("Testing serial_comm")
    print("Reading serial blocking")
    res = read_serial_blocking()
    print("Received")
    print(res)