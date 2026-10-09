"""Meridian W104 - original USB / Bluetooth LE firmware.
Copy boot.py, code.py, scanner.py, keymap.py and the documented libraries
to CIRCUITPY. Hardware bring-up and real host testing remain required.
"""
import time
import board
import digitalio
import supervisor
import usb_hid
import _bleio
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.keyboard import Keyboard
from scanner import SerialMatrix, Debouncer, output
from keymap import KEYMAP

matrix = SerialMatrix()
debouncer = Debouncer()
caps = output(board.D6)
num = output(board.D7)
scroll = output(board.D8)
button = digitalio.DigitalInOut(board.D9)
button.switch_to_input(pull=digitalio.Pull.UP)

# Battery-only startup must not wait indefinitely for a USB host.
usb_keyboard = None
hid = HIDService()
hid.protocol_mode = 1
ble_keyboard = Keyboard(hid.devices)
radio = BLERadio()
radio.name = "Meridian W104"
advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961  # Bluetooth HID keyboard appearance.
use_usb = supervisor.runtime.usb_connected
active_keyboard = None
reported = set()
button_raw = False
button_stable = False
button_changed_at = 0.0
button_down_at = 0.0
bonds_cleared = False
last_usb_state = supervisor.runtime.usb_connected

def release_transport():
    global active_keyboard, reported
    if active_keyboard is not None:
        try:
            active_keyboard.release_all()
        except (OSError, RuntimeError):
            pass  # The host may have disconnected between readiness and send.
    active_keyboard = None
    reported = set()

while True:
    now = time.monotonic()
    # Connecting or removing USB automatically chooses the available transport.
    usb_state = supervisor.runtime.usb_connected
    if usb_state and usb_keyboard is None:
        try:
            usb_keyboard = Keyboard(usb_hid.devices, timeout=1)
        except OSError:
            pass  # Enumeration can briefly lag cable insertion; retry next frame.
    if usb_state != last_usb_state:
        release_transport()
        use_usb = usb_state
        last_usb_state = usb_state

    pressed_button = not button.value
    if pressed_button != button_raw:
        button_raw = pressed_button
        button_changed_at = now
    elif pressed_button != button_stable and now - button_changed_at >= 0.03:
        button_stable = pressed_button
        if button_stable:
            button_down_at = now
            bonds_cleared = False
        elif not bonds_cleared:
            release_transport()
            use_usb = not use_usb
    if button_stable and not bonds_cleared and now - button_down_at >= 5:
        release_transport()
        if radio.advertising:
            radio.stop_advertising()
        for connection in radio.connections:
            connection.disconnect()
        _bleio.adapter.erase_bonding()
        use_usb = False
        bonds_cleared = True

    if not use_usb and not radio.connected and not radio.advertising:
        radio.start_advertising(advertisement)
    elif use_usb and radio.advertising:
        radio.stop_advertising()

    target = usb_keyboard if use_usb and usb_state else (ble_keyboard if not use_usb and radio.connected else None)
    if target is not active_keyboard:
        release_transport()
        active_keyboard = target

    stable = debouncer.update(matrix.read(), now)
    desired_codes = [KEYMAP[i] for i, value in enumerate(stable) if value and KEYMAP[i]]
    # USB boot HID and the default BLE keyboard report support six ordinary keys
    # plus all eight modifiers. Physical matrix diodes prevent ghosting.
    ordinary = [key for key in desired_codes if key < 224][:6]
    desired = set(ordinary + [key for key in desired_codes if key >= 224])
    if target is not None and desired != reported:
        try:
            released = reported - desired
            added = desired - reported
            if released:
                target.release(*released)
            if added:
                target.press(*added)
            reported = desired
        except (OSError, RuntimeError):
            release_transport()

    if target is None:
        caps.value = False
        scroll.value = False
        num.value = not use_usb and (int(now * 2) % 2 == 0)
    else:
        caps.value = target.led_on(Keyboard.LED_CAPS_LOCK)
        num.value = target.led_on(Keyboard.LED_NUM_LOCK)
        scroll.value = target.led_on(Keyboard.LED_SCROLL_LOCK)
    time.sleep(0.001)
