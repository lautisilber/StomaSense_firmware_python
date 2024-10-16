import tests

def test() -> None:
    tests.test_stepper_blocking()
    tests.test_stepper_async()

def main() -> None:
    pass

if __name__ == '__main__':
    test()