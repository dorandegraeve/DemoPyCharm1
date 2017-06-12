# Temperatuur
##############################################################
import spidev
import time

spi = spidev.SpiDev()  # Create spi object
spi.open(0, 0)  # Open spi port0, device (CS) 0


def ReadChannel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) | adc[2]
    return data


try:
    while True:
        waarde = ReadChannel(0)
        # temp = (3.3 * waarde * 100) / 1023
        # print(str(temp))
        procent = (waarde / 1023 * 100)
        print('LDR: %s ' % str(procent))
        time.sleep(1)
        temp_waarde = ReadChannel(1)
        temp = temp_waarde / 1023 * 100
        print('Potentiometer: %s' % str(temp))
        time.sleep(1)
except KeyboardInterrupt:
    print("done")


# Servo
##############################################################
# import spidev
# import RPi.GPIO as GPIO
#
# GPIO.setmode(GPIO.BCM)
#
# spi = spidev.SpiDev()
# spi.open(0, 0)
# GPIO.setup(20, GPIO.OUT)
# servo = GPIO.PWM(20, 50)
# servo.start(0)
#
#
# def ReadChannel(channel):
#     adc = spi.xfer2([1, (8 + channel) << 4, 0])
#     data = ((adc[1] & 3) << 8) | adc[2]
#     return data
#
#
# try:
#     while True:
#         waarde = ReadChannel(0)
#         procent = (waarde / 1023 * 100)
#         procent = procent / 100 * 13
#         if procent > 4:
#             servo.ChangeDutyCycle(procent)
#
# except KeyboardInterrupt:
#     print("done")
#     GPIO.cleanup()
