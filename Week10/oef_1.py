import serial
import time

# ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

ser = serial.Serial('/dev/ttyAMA0', 9600, 8, 'N', 1, 1)

print(ser.name)

try:
    while 1:
        tekst = input("Geef een tekst in: ")
        ser.write(tekst.encode('utf-8'))
        time.sleep(1)
        output = ser.readline()
        print("---------------------------")
        print(output.decode())

except KeyboardInterrupt:
    ser.close()
