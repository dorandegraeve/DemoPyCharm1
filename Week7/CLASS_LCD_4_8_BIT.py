import RPi.GPIO as GPIO
import time


# Yentl De Leersnijder 1NMCT3

class LCD_4_8_BIT:
    def __init__(self, par_RS=27, par_E=22, par_DATA_0=26, par_DATA_1=19, par_DATA_2=13, par_DATA_3=6, par_DATA_4=21, par_DATA_5=20, par_DATA_6=16, par_DATA_7=12, par_BITMODE=4):
        self.__BITMODE = par_BITMODE
        self.__RS = par_RS
        self.__E = par_E
        self.__DATA_4 = par_DATA_4
        self.__DATA_5 = par_DATA_5
        self.__DATA_6 = par_DATA_6
        self.__DATA_7 = par_DATA_7
        if self.__BITMODE == 4:
            self.__DATA_PINS_LIST = [self.__DATA_4, self.__DATA_5, self.__DATA_6, self.__DATA_7]
            self.__CONTROL_PINS_LIST = [self.__RS, self.__E]
        elif self.__BITMODE == 8:
            self.__DATA_0 = par_DATA_0
            self.__DATA_1 = par_DATA_1
            self.__DATA_2 = par_DATA_2
            self.__DATA_3 = par_DATA_3
            self.__DATA_PINS_LIST = [self.__DATA_0, self.__DATA_1, self.__DATA_2, self.__DATA_3, self.__DATA_4, self.__DATA_5, self.__DATA_6, self.__DATA_7]
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

    def __LCD_INIT(self):  # Method to initialize the LCD
        self.__LCD_RESET()
        time.sleep(0.01)
        if self.__BITMODE == 4:
            self.__LCD_SEND_INIT(0x33)
            self.__LCD_SEND_INIT(0x32)
            self.__LCD_SEND_INIT(0x28)
            self.__LCD_SEND_INIT(0x0c)
            self.__LCD_SEND_INIT(0x01)
        elif self.__BITMODE == 8:
            self.__LCD_SEND_INIT(0x3C)
            self.__LCD_SEND_INIT(0xc)
            self.__LCD_SEND_INIT(0x01)

        print('LCD INITIALIZATION COMPLETE')

    def __LCD_RESET(self):  # Method to reset the LCD
        if self.__BITMODE == 4:
            self.__LCD_SEND_INIT(0x30)
            time.sleep(0.0041)
            self.__LCD_SEND_INIT(0x30)
            time.sleep(0.0001)
            self.__LCD_SEND_INIT(0x30)
            time.sleep(0.0001)
            self.__LCD_SEND_INIT(0x20)
        elif self.__BITMODE == 8:
            self.__LCD_SEND_INIT(0x30)
            time.sleep(0.0041)
            self.__LCD_SEND_INIT(0x30)
            time.sleep(0.0001)
            self.__LCD_SEND_INIT(0x30)
            time.sleep(0.0001)
            self.__LCD_SEND_INIT(0x30)
        print('LCD RESET COMPLETE')

    def __LCD_ENABLE(self):  # LCD read data command
        GPIO.output(self.__E, GPIO.HIGH)
        time.sleep(0.0004)
        GPIO.output(self.__E, GPIO.LOW)

    def __LCD_SEND_INIT(self, DATA):  # LCD send instruction
        GPIO.output(self.__RS, GPIO.LOW)
        if self.__BITMODE == 4:
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
        elif self.__BITMODE == 8:
            Filter = 0x01
            for pin in self.__DATA_PINS_LIST:
                GPIO.output(pin, bool(DATA & Filter))
                Filter *= 2
                time.sleep(0.001)
            self.__LCD_ENABLE()

    def __LCD_SET_DATA(self, DATA):  # LCD set data on the pins
        GPIO.output(self.__RS, GPIO.HIGH)
        if self.__BITMODE == 4:
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
        elif self.__BITMODE == 8:
            Filter = 0x01
            for pin in self.__DATA_PINS_LIST:
                GPIO.output(pin, bool(DATA & Filter))
                Filter *= 2
                time.sleep(0.001)
            self.__LCD_ENABLE()

    def LCD_SEND_DATA(self, DATA):  # Send data to the LCD
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
    mode = int(input('4 of 8 BIT mode(4/8): '))
    while mode != 4 and mode != 8:
        print('ONLY 4 OR 8 BIT MODE!!!!')
        mode = int(input('4 of 8 BIT mode(4/8): '))
    # ORDER OF PINS (par_RS, par_E, par_DATA_0, par_DATA_1, par_DATA_2, par_DATA_3, par_DATA_4, par_DATA_5, par_DATA_6, par_DATA_7, par_BITMODE)
    LCD1 = LCD_4_8_BIT(par_DATA_4=6, par_DATA_5=5, par_DATA_6=17, par_DATA_7=4, par_BITMODE=mode)
    while True:
        data = str(input('Geef tekst in: '))
        LCD1.LCD_SEND_DATA(data)
except KeyboardInterrupt:
    LCD1.LCD_OFF()
    time.sleep(0.001)
    GPIO.cleanup()
