import RPi.GPIO as GPIO
import time


class LCD_4_BIT:
    def __init__(self, par_RS=27, par_E=22, par_DATA_4=21, par_DATA_5=20, par_DATA_6=16, par_DATA_7=12, par_BITMODE=0):  # 0 = 4 en 1 = 8
        self.__BITMODE = par_BITMODE
        self.__RS = par_RS
        self.__E = par_E
        self.__DATA_4 = par_DATA_4
        self.__DATA_5 = par_DATA_5
        self.__DATA_6 = par_DATA_6
        self.__DATA_7 = par_DATA_7
        self.__DATA_PINS_LIST = [self.__DATA_4, self.__DATA_5, self.__DATA_6, self.__DATA_7]
        self.__CONTROL_PINS_LIST = [self.__RS, self.__E]
        self.__PIN_INIT()
        self.__LCD_INIT()

    def __PIN_INIT(self):  # Initialize the pins as outputs on the RPI
        GPIO.setmode(GPIO.BCM)
        for pin in self.__CONTROL_PINS_LIST:
            GPIO.setup(pin, GPIO.OUT)
        for pin in self.__DATA_PINS_LIST:
            GPIO.setup(pin, GPIO.OUT)
        print('PIN INITIALIZATION COMPLETE')

    def __LCD_INIT(self):  # Method to initialize the LCD in 8 BIT MODE
        self.__LCD_RESET()
        time.sleep(0.01)
        self.__LCD_SEND_INIT(0x33)
        self.__LCD_SEND_INIT(0x32)
        self.__LCD_SEND_INIT(0x28)
        self.__LCD_SEND_INIT(0x0c)
        self.__LCD_SEND_INIT(0x01)
        print('LCD INITIALIZATION COMPLETE')

    def __LCD_RESET(self):  # Method to reset the LCD

        self.__LCD_SEND_INIT(0x30)
        time.sleep(0.0041)
        self.__LCD_SEND_INIT(0x30)
        time.sleep(0.0001)
        self.__LCD_SEND_INIT(0x30)
        time.sleep(0.0001)
        self.__LCD_SEND_INIT(0x20)
        print('LCD RESET COMPLETE')

    def __LCD_ENABLE(self):  # LCD read data command
        GPIO.output(self.__E, GPIO.HIGH)
        time.sleep(0.0004)
        GPIO.output(self.__E, GPIO.LOW)

    def __LCD_SEND_INIT(self, DATA):
        GPIO.output(self.__RS, GPIO.LOW)
        counter = 0
        while counter != 2:
            Filter = 0x10
            for pin in self.__DATA_PINS_LIST:
                GPIO.output(pin, bool(DATA & Filter))
                Filter *= 2
                time.sleep(0.001)
            self.__LCD_ENABLE()
            DATA = (DATA & 0x0F) << 4
            time.sleep(0.0001)
            counter += 1

    def __LCD_SET_DATA(self, DATA):
        GPIO.output(self.__RS, GPIO.HIGH)
        counter = 0
        while counter != 2:
            Filter = 0x10
            for pin in self.__DATA_PINS_LIST:
                GPIO.output(pin, bool(DATA & Filter))
                Filter *= 2
                time.sleep(0.001)
            self.__LCD_ENABLE()
            DATA = (DATA & 0x0F) << 4
            time.sleep(0.0001)
            counter += 1

    def LCD_SEND_DATA(self, DATA):
        self.__LCD_SEND_INIT(0x01)
        self.__LCD_SEND_INIT(0x80)
        counter = 0
        for char in DATA:
            self.__LCD_SET_DATA(ord(char))
            time.sleep(0.001)
            if counter == 15:
                self.__LCD_SEND_INIT(0xA9)
            if counter == 31:
                break
            if len(DATA) > 15:
                counter += 1
        print('SEND DATA COMPLETE')

    def LCD_OFF(self):
        self.__LCD_SEND_INIT(0X08)


try:
    LCD1 = LCD_4_BIT()
    while True:
        data = str(input('Geef tekst in: '))
        LCD1.LCD_SEND_DATA(data)

except KeyboardInterrupt:
    LCD1.LCD_OFF()
    time.sleep(0.001)
    GPIO.cleanup()
