import RPi.GPIO as GPIO
from Klasses.CLASS_LCD_4_8_BIT import LCD_4_8_BIT
import socket
import time
import glob

def get_ip():
    try:
        ip = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    except:
        ip = '169.254.10.11'
    return ip

def get_name():
    lst_names=[]
    for i in glob.glob('*.py'):
        lst_names.append(i)
    return lst_names
try:
    #mode = int(input('4 of 8 BIT mode(4/8): '))
    #while mode != 4 and mode != 8:
    #    print('ONLY 4 OR 8 BIT MODE!!!!')
    #    mode = int(input('4 of 8 BIT mode(4/8): '))
    ## ORDER OF PINS (par_RS, par_E, par_DATA_0, par_DATA_1, par_DATA_2, par_DATA_3, par_DATA_4, par_DATA_5, par_DATA_6, par_DATA_7, par_BITMODE)
    #LCD1 = LCD_4_8_BIT(par_DATA_4=6, par_DATA_5=5, par_DATA_6=17, par_DATA_7=4, par_BITMODE=mode)
    #LCD1.LCD_SEND_DATA(get_ip())
    #time.sleep(0.01)
    #LCD1.LCD_SEND_LINE_2('TEST')
    for i in get_name():
        print(i)
except KeyboardInterrupt:
    #LCD1.LCD_OFF()
    time.sleep(0.01)
    GPIO.cleanup()
