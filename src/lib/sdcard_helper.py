from machine import Pin, SPI
import os
#from .sdcard import SDCard
from libs.sdcard import SDCard
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

class SD:
    def __init__(self) -> None:
        self.sd: SDCard | None = None
        self.vfs: os.VfsFat | None = None
    
    def _init(self):
        self.sd = SDCard(spi, pin_cs, True)
        self.vfs = os.VfsFat(self.sd)
        try:
            os.mount(self.vfs, "/sd")
        except OSError(EPERM):
            # already mounted
            pass
        
    def _deinit(self):
        self.sd = None
        self.vsf = None
        try:
            os.umount("/sd")
        except OSError(EINVAL):
            # not mounted
            pass

    def __enter__(self):
        self._init()
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        self._deinit()
    
    def open(self, file: str, mode: str):
        return open("/sd/" + file, mode)
    
    def write(self, file: str, content: str) -> bool:
        try:
            with self.open(file, "w") as f:
                f.write(content)
            return True
        except OSError as e:
            print(e)
            return False
    
    def read(self, file: str) -> str | None:
        try:
            with self.open(file, "r") as f:
                return f.read()
        except OSError as e:
            print(e)
            return None
    
    def append(self, file: str, content: str) -> bool:
        try:
            with open(file, "a") as f:
                f.write(content)
            return True
        except OSError as e:
            print(e)
            return False
        
    def listdir(self, d: str | None) -> list[str] | None:
        self._init()
        try:
            return os.listdir(d)
        except OSError as e:
            print(e)
            return None
        finally:
            self._deinit()
    
    def delete(self, file: str) -> bool:
        self._init()
        try:
            os.remove(file)
            return True
        except OSError as e:
            print(e)
            return False
        finally:
            self._deinit()
            
