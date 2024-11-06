"""
MicroPython Library for MCP3001 10-bit single-channel ADC with SPI

Datasheet for the MCP3001:
https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/21293C.pdf

Based on Romilly Cocking's MCP3008 library:
https://github.com/romilly/pico-code/blob/master/src/pico_code/pico/mcp3008/mcp3008.py

Unlike the multi-channel MCP300x chips, the MCP3001 has no channel select code
or mode settings. A reading is made by pulling CS low, then reading two bytes from the SPI bus.
The ADC reading is the last 10 bits of these bytes (0..1023)

scruss, 2024-11
"""

import machine


class MCP3001:

    def __init__(self, spi, cs, ref_voltage=3.3):
        """
        Create MCP 3001 instance

        Args:
            spi: 			configured SPI bus
            cs:				pin used for chip select (active low)
            ref_voltage:	Vref value
        """
        self.cs = cs
        self.cs(1)  # deselect for now
        self._spi = spi
        self._in_buf = bytearray(2)
        self._ref_voltage = ref_voltage

    def reference_voltage(self) -> float:
        """Returns reference voltage as float"""
        return self._ref_voltage

    def read(self) -> int:
        """
        Read MCP3001 10-bit value
        Takes no arguments
        """
        self.cs(0)  # enable and read
        self._spi.readinto(self._in_buf)
        self.cs(1)  # off
        return ((self._in_buf[0] & 0x03) << 8) | self._in_buf[1]

    def read_v(self) -> float:
        """
        Read MCP3001 and return as voltage, based on ref_voltage
        """
        return self.read() * self._ref_voltage / 1023

    def read_u16(self) -> int:
        """
        Read MCP3001 and return a properly-scaled 16-bit value
        using a Taylor expansion
        """
        tmp = self.read()
        return tmp << 6 | tmp >> 4
