"""Meridian W104 serial scanner. One HC595 + three daisy-chained HC165.

D0 SER, D1 row clock, D2 row latch, D3 column serial input,
D4 column clock, D5 /column load, D10 /row output enable.
Rows active LOW. A closed COL2ROW key yields a LOW sense bit.
"""
import time
import board
import digitalio

def output(pin, initial=False):
    io = digitalio.DigitalInOut(pin)
    io.switch_to_output(value=initial)
    return io

class SerialMatrix:
    def __init__(self):
        # Output enable HIGH keeps rows isolated until a known mask is latched.
        self.oe = output(board.D10, True)
        self.data = output(board.D0)
        self.row_clock = output(board.D1)
        self.row_latch = output(board.D2)
        self.column_clock = output(board.D4)
        self.load = output(board.D5, True)
        self.sense = digitalio.DigitalInOut(board.D3)
        self.sense.switch_to_input()
        self.select_row(None)
        self.oe.value = False

    def select_row(self, row):
        mask = 255 if row is None else (255 ^ (1 << row))
        for bit in range(7, -1, -1):
            self.data.value = bool(mask & (1 << bit))
            self.row_clock.value = True
            self.row_clock.value = False
        self.row_latch.value = True
        self.row_latch.value = False

    def sample_columns(self):
        self.column_clock.value = False
        self.load.value = False
        self.load.value = True
        pressed = []
        for serial_index in range(24):
            column = (serial_index // 8) * 8 + 7 - (serial_index % 8)
            if not self.sense.value and column < 22:
                pressed.append(column)
            self.column_clock.value = True
            self.column_clock.value = False
        return pressed

    def read(self):
        frame = [False] * 132
        for row in range(6):
            self.select_row(row)
            time.sleep(0.00003)
            for column in self.sample_columns():
                frame[row * 22 + column] = True
        self.select_row(None)
        return frame

class Debouncer:
    def __init__(self, count=132, interval=0.008):
        self.raw = [False] * count
        self.stable = [False] * count
        self.changed_at = [0.0] * count
        self.interval = interval

    def update(self, frame, now):
        for i, value in enumerate(frame):
            if value != self.raw[i]:
                self.raw[i] = value
                self.changed_at[i] = now
            elif value != self.stable[i] and now - self.changed_at[i] >= self.interval:
                self.stable[i] = value
        return self.stable
