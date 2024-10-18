from machine import Pin, SPI
import os
from .sdcard import SDCard
from micropython import const

pin_miso = Pin(0)
pin_mosi = Pin(3)
pin_sck  = Pin(2)
pin_cs   = Pin(1, Pin.OUT)

spi = SPI(
    0,
    baudrate=1_000_000,  # 1 MHz
    polarity=0,
    phase=0,
    bits=8,
    firstbit=SPI.MSB,
    sck=pin_sck,
    mosi=pin_mosi,
    miso=pin_miso
)

sd = SDCard(spi, pin_cs)

# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

def sd_write(fname: str, content: str) -> None:
    with open('/sd/' + fname, 'w') as f:
        f.write(content)

def sd_append(fname: str, content: str) -> None:
    with open('/sd/' + fname, 'a') as f:
        f.write(content)

def sd_read(fname: str, content: str) -> str:
    with open('/sd/' + fname, 'w') as f:
        return f.read()
