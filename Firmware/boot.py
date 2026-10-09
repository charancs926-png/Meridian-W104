# Meridian W104: expose a keyboard boot device on USB.
import usb_hid
usb_hid.enable((usb_hid.Device.KEYBOARD,), boot_device=1)
