import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

DATA_4 = 21
DATA_5 = 20
DATA_6 = 16
DATA_7 = 12

RS = 27
E = 22

GPIO.setup(DATA_4, GPIO.OUT)
GPIO.setup(DATA_5, GPIO.OUT)
GPIO.setup(DATA_6, GPIO.OUT)
GPIO.setup(DATA_7, GPIO.OUT)

GPIO.setup(RS, GPIO.OUT)
GPIO.setup(E, GPIO.OUT)


def init():
    GPIO.output(RS, GPIO.LOW)
    reset()
    time.sleep(0.01)
    Init_Data(0x33)
    Init_Data(0x32)
    Init_Data(0x28)
    Init_Data(0x0c)
    Init_Data(0x01)


def Enable():
    GPIO.output(E, GPIO.HIGH)
    time.sleep(0.0004)
    GPIO.output(E, GPIO.LOW)
    time.sleep(0.0004)


def Send_Data_Ready(Data):
    GPIO.output(RS, GPIO.HIGH)
    GPIO.output(DATA_4, bool(Data & 0x10))
    GPIO.output(DATA_5, bool(Data & 0x20))
    GPIO.output(DATA_6, bool(Data & 0x40))
    GPIO.output(DATA_7, bool(Data & 0x80))
    Enable()


def Init_Data(Byte):
    GPIO.output(RS, GPIO.LOW)
    GPIO.output(DATA_4, bool(Byte & 0x10))
    GPIO.output(DATA_5, bool(Byte & 0x20))
    GPIO.output(DATA_6, bool(Byte & 0x40))
    GPIO.output(DATA_7, bool(Byte & 0x80))
    Enable()
    Byte = (Byte & 0x0F) << 4
    time.sleep(0.001)
    GPIO.output(DATA_4, bool(Byte & 0x10))
    GPIO.output(DATA_5, bool(Byte & 0x20))
    GPIO.output(DATA_6, bool(Byte & 0x40))
    GPIO.output(DATA_7, bool(Byte & 0x80))
    Enable()


def Send_Data(Data):
    Init_Data(0x01)
    time.sleep(0.01)
    Init_Data(0x80)
    counter = 0
    for char in Data:
        Data_char = ord(char)
        Send_Data_Ready(Data_char)
        Data_char = (Data_char & 0x0F) << 4
        Send_Data_Ready(Data_char)
        time.sleep(0.01)
        if counter == 15:
            Init_Data(0xA9)
            time.sleep(0.01)
        if counter == 31:
            break
        if len(Data) > 15:
            counter += 1


def reset():
    Init_Data(0x3)
    time.sleep(0.0041)
    Init_Data(0x3)
    time.sleep(0.0001)
    Init_Data(0x3)
    time.sleep(0.0001)
    Init_Data(0x20)


try:
    init()
    while True:
        data = str(input('Geef tekst in: '))
        Send_Data(data)

except KeyboardInterrupt:
    Init_Data(0x08)
    time.sleep(0.01)
    GPIO.cleanup()
