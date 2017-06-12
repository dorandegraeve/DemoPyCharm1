import spidev
import time

# Open SPI bus
spi = spidev.SpiDev()  # Create spi object
spi.open(0, 0)  # Open spi port0, device (CS) 0


# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
    # 3 bytes versturen
    # 1,S D2 D1 D0 XXXX,0
    adc = spi.xfer2({1, (8 + channel) << 4, 0})
    data = ((adc[1] & 3) << 8) | adc[2]  # In byte 1 en 2 zit resultaat
    return data
