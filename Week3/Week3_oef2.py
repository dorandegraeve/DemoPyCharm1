import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pin = 20

GPIO.setup(pin, GPIO.OUT)
pwmFan = GPIO.PWM(pin, 60)
pwmFan.start(0)
pwmFan.ChangeDutyCycle(100)

sensor_file = '/sys/bus/w1/devices/28-80000026c535/w1_slave'


def read_temp_raw():
    f = open(sensor_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp = lines[1]
        temp = temp[29:34]
        temperatuur = int(temp) / 1000.0
        return temperatuur


try:
    while True:
        Temp = read_temp()
        print(Temp)
        if 20 < Temp < 22:
            pwmFan.ChangeDutyCycle(0)
        elif 22 < Temp < 24:
            pwmFan.ChangeDutyCycle(30)
        elif 24 < Temp < 26:
            pwmFan.ChangeDutyCycle(50)
        elif Temp > 26:
            pwmFan.ChangeDutyCycle(100)
except KeyboardInterrupt:
    pwmFan.stop()

    print('STOP')
