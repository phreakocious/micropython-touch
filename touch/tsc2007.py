# tsc2007.py MicroPython driver for TSC2007 resistive touch controller.

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2024 Peter Hinch

# Works with the Adafruit TSC2007 resistive touch driver.
# Adafruit product reference http://www.adafruit.com/products/5423

# Reference sources: the TSC2007 datasheet plus Adafruit driver
# https://github.com/adafruit/Adafruit_CircuitPython_TSC2007
# It is minimal, providing only the required functionality for the touh GUI. See
# the Adafruit driver for a more full-featured driver.

from .touch import ABCTouch, PreProcess


class TSC2007(ABCTouch):
    def __init__(self, i2c, height, width, xmin=0, ymin=0, xmax=4095, ymax=4095, addr=0x48):
        prep = PreProcess(self)  # Instantiate a preprocessor
        super().__init__(height, width, xmin, ymin, xmax, ymax, prep)
        self._i2c = i2c
        self._addr = addr
        i2c.writeto(addr, b"\x00")  # Low power/read temp

    def _value(self, buf=bytearray(2)):
        self._i2c.readfrom_into(self._addr, buf)
        return (buf[0] << 4) | (buf[1] >> 4)

    # If touched, populate .row and .col with raw data. Return True.
    # If not touched return False.
    def acquire(self):
        addr = self._addr
        self._i2c.writeto(addr, b"\xE4")  # Z
        if t := (self._value() > 100):  # Touched
            self._i2c.writeto(addr, b"\xC4")  # X
            self._x = self._value()
            self._i2c.writeto(addr, b"\xD4")  # Y
            self._y = self._value()
        self._i2c.writeto(addr, b"\x00")  # Low power/read temp
        return t
