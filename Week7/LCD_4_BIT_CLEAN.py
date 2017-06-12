import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

RS = 27
E = 22

DATA_4 = 21
DATA_5 = 20
DATA_6 = 16
DATA_7 = 12

DATA_PINS_LIST = [DATA_4, DATA_5, DATA_6, DATA_7]
CONTROL_PINS_LIST = [RS, E]


def PIN_INIT():  # Initialize the pins as outputs on the RPI
    for pin in CONTROL_PINS_LIST:
        GPIO.setup(pin, GPIO.OUT)
    for pin in DATA_PINS_LIST:
        GPIO.setup(pin, GPIO.OUT)
    print('PIN INITIALIZATION COMPLETE')


def LCD_INIT():  # Method to initialize the LCD in 8 BIT MODE
    LCD_RESET()
    time.sleep(0.01)
    LCD_SEND_INIT(0x33)
    LCD_SEND_INIT(0x32)
    LCD_SEND_INIT(0x28)
    LCD_SEND_INIT(0x0c)
    LCD_SEND_INIT(0x01)
    print('LCD INITIALIZATION COMPLETE')


def LCD_RESET():  # Method to reset the LCD
    LCD_SEND_INIT(0x30)
    time.sleep(0.0041)
    LCD_SEND_INIT(0x30)
    time.sleep(0.0001)
    LCD_SEND_INIT(0x30)
    time.sleep(0.0001)
    LCD_SEND_INIT(0x20)
    print('LCD RESET COMPLETE')


def LCD_ENABLE():  # LCD read data command
    GPIO.output(E, GPIO.HIGH)
    time.sleep(0.0004)
    GPIO.output(E, GPIO.LOW)


def LCD_SEND_INIT(DATA):
    GPIO.output(RS, GPIO.LOW)
    counter = 0
    while counter != 2:
        Filter = 0x10
        for pin in DATA_PINS_LIST:
            GPIO.output(pin, bool(DATA & Filter))
            Filter *= 2
            time.sleep(0.001)
        LCD_ENABLE()
        DATA = (DATA & 0x0F) << 4
        time.sleep(0.0001)
        counter += 1


def LCD_SET_DATA(DATA):
    GPIO.output(RS, GPIO.HIGH)
    counter = 0
    while counter != 2:
        Filter = 0x10
        for pin in DATA_PINS_LIST:
            GPIO.output(pin, bool(DATA & Filter))
            Filter *= 2
            time.sleep(0.001)
        LCD_ENABLE()
        DATA = (DATA & 0x0F) << 4
        time.sleep(0.0001)
        counter += 1


def LCD_SEND_DATA(DATA):
    LCD_SEND_INIT(0x01)
    LCD_SEND_INIT(0x80)
    counter = 0
    for char in DATA:
        LCD_SET_DATA(ord(char))
        time.sleep(0.001)
        if counter == 15:
            LCD_SEND_INIT(0xA9)
        if counter == 31:
            break
        if len(data) > 15:
            counter += 1
    print('SEND DATA COMPLETE')


try:
    PIN_INIT()
    LCD_INIT()
    while True:
        data = str(input('Geef tekst in: '))
        LCD_SEND_DATA(data)

except KeyboardInterrupt:
    LCD_SEND_INIT(0x08)
    time.sleep(0.001)
    GPIO.cleanup()
