def clamp(n: int | float, smallest: int | float, biggest: int | float) -> int | float:
    return smallest if n < smallest else biggest if n > biggest else n