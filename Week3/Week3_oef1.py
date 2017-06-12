import time

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


while True:
    print(read_temp())
    time.sleep(0.5)
