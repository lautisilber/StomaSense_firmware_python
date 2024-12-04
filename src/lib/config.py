import json
import utils

class PositionData:
    _keys = ("stepper_pos", "servo_pos", "pump_time_ms", "pump_strength")
    def __init__(self,
                 stepper_pos: int,
                 servo_pos: int,
                 pump_time_ms: int,
                 pump_strength: int) -> None:
        self.stepper_pos = stepper_pos
        self.servo_pos = servo_pos
        self.pump_time_ms = pump_time_ms
        self.pump_strength = pump_strength
    
    def __str__(self) -> str:
        return f'PositionData(stepper={self.stepper_pos}, servo={self.servo_pos}, pump_t={self.pump_time_ms}, pump_s{self.pump_strength})'

    def __repr__(self) -> str:
        return self.__str__()

class Run:
    _keys = ("interval_bme280_s", "interval_hx711_s", "position_data")
    _keys_int = ("interval_bme280_s", "interval_hx711_s")
    _key_position_data = "position_data"
    def __init__(self,
                 interval_bme280_s: int,
                 interval_hx711_s: int,
                 position_data: tuple[PositionData, ...]) -> None:
        self.interval_bme280_s = interval_bme280_s
        self.interval_hx711_s = interval_hx711_s
        self.position_data = position_data
        
    @staticmethod
    def validate_obj(obj: dict) -> bool:
        # check obj is dict
        if not isinstance(obj, dict):
            return False

        # check right keys
        if not utils.has_keys(obj, Run._keys):
            return False
        
        # check types: ints
        if not all(map(utils.is_number, (v for k, v in obj.items() if k in Run._keys_int))):
            return False
        # check types: PositionData
        if not isinstance(obj[Run._key_position_data], list):
            return False
        for e in obj[Run._key_position_data]:
            if not isinstance(e, list):
                return False
            if len(e) != 4:
                return False
            if not all(map(utils.is_number, e)):
                return False

        return True
    
    @staticmethod
    def cast_obj(obj: dict) -> dict | None:
        if not Run.validate_obj(obj):
            return None
        
        # cast ints
        cast_obj = {k:int(obj[k]) for k in Run._keys_int}
        
        # cast PositionData
        cast_obj[Run._key_position_data] = tuple(
            PositionData(*map(int, e)) for e in obj[Run._key_position_data]
        )
        
        return cast_obj
    
    @staticmethod
    def from_obj(obj: dict) -> "Run | None":
        o = Run.cast_obj(obj)
        if o is None:
            return None
        return Run(**o)
        
    @staticmethod
    def load_json(s: str) -> "Run | None":
        try:
            obj = json.loads(s)
        except ValueError as e:
            print(e)
            return False
        return Run.from_obj(obj)
    
    def __str__(self) -> str:
        return f'Run(bme280={self.interval_bme280_s}, hx711={self.interval_hx711_s}, pos={self.position_data})'

    def __repr__(self) -> str:
        return self.__str__()