import RPi.GPIO as GPIO
import time

# Yentl De Leersnijder 1NMCT3
GPIO.setmode(GPIO.BCM)
AI = 0x40  # Auto increment
FX = 0x44  # Fixed address

C0H = 0xC0
C1H = 0xC1
C2H = 0xC2
C3H = 0xC3

BR1 = 0x81
BR2 = 0x82
BR3 = 0x83
BR4 = 0x84
BR5 = 0x85
BR6 = 0x86
BR7 = 0x87

data_command = [AI, FX]
address_command = [C0H, C1H, C2H, C3H]
display_command = [BR1, BR2, BR3, BR4, BR5, BR6, BR7]


class TMDisplay:
    def __init__(self, par_CLK=20, par_DA=21):
        self.__CLK = par_CLK
        self.__DA = par_DA

    def __setup(self):
        GPIO.setup(self.__CLK, GPIO.OUT)
        GPIO.setup(self.__DA, GPIO.OUT)

    def __start(self):
        GPIO.output(self.__CLK, GPIO.HIGH)
        GPIO.output(self.__DA, GPIO.HIGH)
        GPIO.output(self.__DA, GPIO.LOW)
        GPIO.output(self.__CLK, GPIO.LOW)

    def __stop(self):
        GPIO.output(self.__DA, GPIO.LOW)
        GPIO.output(self.__CLK, GPIO.LOW)
        GPIO.output(self.__CLK, GPIO.HIGH)
        GPIO.output(self.__DA, GPIO.HIGH)

    def __wrtieBit(self, bit):
        GPIO.output(self.__CLK, GPIO.LOW)
        GPIO.output(self.__DA, bit)
        GPIO.output(self.__CLK, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.__CLK, GPIO.LOW)

    def __ack(self):
        print(GPIO.input(self.__DA))
        GPIO.output(self.__CLK, GPIO.LOW)
        GPIO.setup(self.__DA, GPIO.IN, GPIO.PUD_UP)
        print(GPIO.input(self.__DA))
        time.sleep(0.001)
        GPIO.output(self.__CLK, GPIO.HIGH)
        GPIO.setup(self.__DA, GPIO.OUT)

    def __writeByte(self, byte):
        Filter = 0x01
        self.__start()
        for i in range(0, 3):
            if i == 0:
                for t in range(0, 8):
                    self.__wrtieBit(bool(data_command[0] & Filter))
                    Filter *= 2
            if i == 1:
                for t in range(0, 8):
                    self.__wrtieBit(bool(byte & Filter))
                    Filter *= 2
            if i == 2:
                for t in range(0, 8):
                    self.__wrtieBit(bool(byte & Filter))
                    Filter *= 2
            self.__ack()
        self.__stop()
