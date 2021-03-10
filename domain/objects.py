from dataclasses import dataclass

@dataclass
class Candle:
    def __init__(self, dt: str, s: str, o: float, h: float, l: float, c: float, u: str):
        self.s = s
        self.o = o
        self.c = c
        self.h = h
        self.l = l
        self.dt = dt
        self.u = u

@dataclass
class TwoCandles:
    def __init__(self, candle1: Candle, candle2: Candle):
        self.candle1 = candle1
        self.candle2 = candle2


@dataclass
class ThreeCandles:
    def __init__(self, candle1: Candle, candle2: Candle, candle3: Candle):
        self.candle1 = candle1
        self.candle2 = candle2
        self.candle3 = candle3
