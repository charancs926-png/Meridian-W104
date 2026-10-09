# Temporarily rename this to code.py for first hardware bring-up.
# Serial console prints physical row/column and USB HID usage for each change.
import time
from scanner import SerialMatrix, Debouncer
from keymap import KEYMAP
matrix = SerialMatrix()
debounce = Debouncer()
previous = set()
while True:
    state = debounce.update(matrix.read(), time.monotonic())
    pressed = {i for i, value in enumerate(state) if value}
    if pressed != previous:
        for i in sorted(pressed - previous):
            print("DOWN", "row", i // 22, "column", i % 22, "HID", KEYMAP[i])
        for i in sorted(previous - pressed):
            print("UP  ", "row", i // 22, "column", i % 22)
        previous = pressed
    time.sleep(0.001)
