import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

DATA_0 = 26
DATA_1 = 19
DATA_2 = 13
DATA_3 = 6
DATA_4 = 21
DATA_5 = 20
DATA_6 = 16
DATA_7 = 12

RS = 27
E = 22

DATA_PINS_LIST = [DATA_0, DATA_1, DATA_2, DATA_3, DATA_4, DATA_5, DATA_6, DATA_7]
CONTROL_PINS_LIST = [RS, E]


GPIO.setup(DATA_0, GPIO.OUT)
GPIO.setup(DATA_1, GPIO.OUT)
GPIO.setup(DATA_2, GPIO.OUT)
GPIO.setup(DATA_3, GPIO.OUT)
GPIO.setup(DATA_4, GPIO.OUT)
GPIO.setup(DATA_5, GPIO.OUT)
GPIO.setup(DATA_6, GPIO.OUT)
GPIO.setup(DATA_7, GPIO.OUT)

GPIO.setup(RS, GPIO.OUT)
GPIO.setup(E, GPIO.OUT)


def init():
    reset()
    Init_Data(0x3C)  # function set 0000111100
    Init_Data(0xc)  # display on 0000001100
    Init_Data(0x01)  # clear 0000000001


def Enable():
    GPIO.output(E, GPIO.HIGH)
    time.sleep(0.0004)
    GPIO.output(E, GPIO.LOW)
    time.sleep(0.0004)


def Send_Data_Ready(Data):
    GPIO.output(RS, GPIO.HIGH)
    GPIO.output(DATA_0, bool(Data & 0x01))
    GPIO.output(DATA_1, bool(Data & 0x02))
    GPIO.output(DATA_2, bool(Data & 0x04))
    GPIO.output(DATA_3, bool(Data & 0x08))
    GPIO.output(DATA_4, bool(Data & 0x10))
    GPIO.output(DATA_5, bool(Data & 0x20))
    GPIO.output(DATA_6, bool(Data & 0x40))
    GPIO.output(DATA_7, bool(Data & 0x80))
    Enable()


def Init_Data(Byte):
    GPIO.output(RS, GPIO.LOW)
    GPIO.output(DATA_0, bool(Byte & 0x01))
    GPIO.output(DATA_1, bool(Byte & 0x02))
    GPIO.output(DATA_2, bool(Byte & 0x04))
    GPIO.output(DATA_3, bool(Byte & 0x08))
    GPIO.output(DATA_4, bool(Byte & 0x10))
    GPIO.output(DATA_5, bool(Byte & 0x20))
    GPIO.output(DATA_6, bool(Byte & 0x40))
    GPIO.output(DATA_7, bool(Byte & 0x80))
    Enable()


def Send_Data(Data):
    Init_Data(0x01)
    Init_Data(0x80)
    counter = 0
    for char in Data:
        Send_Data_Ready(ord(char))
        time.sleep(0.01)
        if counter == 15:
            Init_Data(0xA9)
        if counter == 31:
            break
        if len(Data) > 15:
            counter += 1


def reset():
    Init_Data(0x30)
    time.sleep(0.0041)
    Init_Data(0x30)
    time.sleep(0.0001)
    Init_Data(0x30)
    time.sleep(0.0001)
    Init_Data(0x30)
    time.sleep(0.01)


try:
    init()
    while True:
        data = str(input('Geef tekst in: '))
        Send_Data(data)

except KeyboardInterrupt:
    Init_Data(0x08)
    time.sleep(0.01)
    GPIO.cleanup()
