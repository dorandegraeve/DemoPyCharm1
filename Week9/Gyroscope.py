# ADXL345 Python library for Raspberry Pi
#
# author:  Jonathan Williamson
# license: BSD, see LICENSE.txt included in this package
#
# This is a Raspberry Pi Python implementation to help you get started with
# the Adafruit Triple Axis ADXL345 breakout board:
# http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer

import smbus
from time import sleep
import sys

# select the correct i2c bus for this revision of Raspberry Pi
revision = ([l[12:-1] for l in open('/proc/cpuinfo', 'r').readlines() if l[:8] == "Revision"] + ['0000'])[0]
bus = smbus.SMBus(1 if int(revision, 16) >= 4 else 0)

# ADXL345 constants
EARTH_GRAVITY_MS2 = 9.81
SCALE_MULTIPLIER = 0.004

DATA_FORMAT = 0x31
BW_RATE = 0x2C
POWER_CTL = 0x2D

BW_RATE_100HZ = 0x0B

RANGE_2G = 0x00
RANGE_4G = 0x01
RANGE_8G = 0x02
RANGE_16G = 0x03

MEASURE = 0x08
AXES_DATA = 0x32


class ADXL345:
    address = None

    def __init__(self, address=0x53):
        self.address = address
        self.setBandwidthRate(BW_RATE_100HZ)
        self.setRange(RANGE_2G)
        self.enableMeasurement()

    def enableMeasurement(self):
        bus.write_byte_data(self.address, POWER_CTL, MEASURE)

    def setBandwidthRate(self, rate_flag):
        bus.write_byte_data(self.address, BW_RATE, rate_flag)

    # set the measurement range for 10-bit readings
    def setRange(self, range_flag):
        value = bus.read_byte_data(self.address, DATA_FORMAT)

        value &= ~0x0F
        value |= range_flag
        value |= 0x08

        bus.write_byte_data(self.address, DATA_FORMAT, value)

        # returns the current reading from the sensor for each axis
        #
        # parameter gforce:
        #    False (default): result is returned in m/s^2
        #    True           : result is returned in gs

    def getAxes(self, gforce=False):
        bytes = bus.read_i2c_block_data(self.address, AXES_DATA, 6)

        xForce = bytes[0] | (bytes[1] << 8)
        # if bytes[1] & 0x80:
        #     xForce = xForce ^ 0xFFFF
        #     xForce += 1
        #     xForce *= -1

        if (xForce & (1 << 16 - 1)):
            xForce = xForce - (1 << 16)

        yForce = bytes[2] | (bytes[3] << 8)
        # if bytes[3] & 0x80:
        #     yForce = yForce ^ 0xFFFF
        #     yForce += 1
        #     yForce *= -1
        if (yForce & (1 << 16 - 1)):
            yForce = yForce - (1 << 16)

        zForce = bytes[4] | (bytes[5] << 8)
        # if bytes[5] & 0x80:
        #     zForce = zForce ^ 0xFFFF
        #     zForce += 1
        #     zForce *= -1
        if (zForce & (1 << 16 - 1)):
            zForce = zForce - (1 << 16)

        xForce = xForce * SCALE_MULTIPLIER
        yForce = yForce * SCALE_MULTIPLIER
        zForce = zForce * SCALE_MULTIPLIER

        if gforce == False:
            xForce = xForce * EARTH_GRAVITY_MS2
            yForce = yForce * EARTH_GRAVITY_MS2
            zForce = zForce * EARTH_GRAVITY_MS2

        xForce = round(xForce, 4)
        yForce = round(xForce, 4)
        zForce = round(xForce, 4)

        return {"x": xForce, "y": yForce, "z": zForce}


adxl345 = ADXL345()
while 1:
    axes = adxl345.getAxes(True)
    sys.stdout.write("\r X= " + str(axes['x']) + " y= " + str(axes['y']) + " z= " + str(axes['z']))
    sys.stdout.flush()
    sleep(0.7)
