# stepper
import libs.stepper as stepper
import asyncio

def test_stepper_blocking() -> None:
    print('Running stepper blocking test')

    n_steps = 10
    print(f'Making {n_steps} steps forward and then backwards, beggining at 0')
    
    stepper.begin()

    stepper.curr_step = 0
    for i in range(3):
        print('testing', 'step_wave' if i == 0 else 'step_normal' if i == 1 else 'step_half')
        stepper.choose_step_type(i)
        stepper.move_to_step_blocking(n_steps, 500*1000)
        stepper.move_to_step_blocking(0, 500*1000)

    print('Finished test')

def test_stepper_async() -> None:
    print('Running stepper async test')

    n_steps = 10
    print(f'Making {n_steps} steps forward and then backwards, beggining at 0')
    
    stepper.begin()

    stepper.curr_step = 0
    for i in range(3):
        print('testing', 'step_wave' if i == 0 else 'step_normal' if i == 1 else 'step_half')
        stepper.choose_step_type(i)
        ayncio.run(stepper.move_to_step_async(n_steps, 1*1000))
        ayncio.run(stepper.move_to_step_async(0, 1*1000))

    print('Finished test')

# servo
import libs.servo as servo

def test_servo_blocking() -> None:
    print('Running servo blocking test')

    servo.set_angle_slow_blocking(0.5)
    servo.set_angle_slow_blocking(1)
    servo.set_angle_slow_blocking(0)
    servo.set_angle_slow_blocking(0.5)
    servo.dettach()

    print('Finished test')

def test_servo_async() -> None:
    print('Running servo blocking test')

    asyncio.run(servo.set_angle_slow_async(0.5))
    asyncio.run(servo.set_angle_slow_async(1))
    asyncio.run(servo.set_angle_slow_async(0))
    asyncio.run(servo.set_angle_slow_async(0.5))
    servo.dettach()

    print('Finished test')

# bme280
from libs.bme280_i2c import BME280_I2C
from time import sleep_ms

def test_bme280():
    print('Running bme280 test')

    bme = BME280_I2C()

    for _ in range(20):
        print(bme.values)
        sleep_ms(1000)

    print('Finished test')
    