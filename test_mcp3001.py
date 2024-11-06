# MicroPython, Raspberry Pi Pico
# -*- coding: utf-8 -*-

import machine
import mcp3001
import time

spi = machine.SPI(
    0
)  # SPI(0, baudrate=1000000, polarity=0, phase=0, bits=8, sck=18, mosi=19, miso=16)
cs = machine.Pin(17, machine.Pin.OUT, value=1)
adc = mcp3001.MCP3001(spi, cs)

while True:
    print(adc.read())
    time.sleep(3)
