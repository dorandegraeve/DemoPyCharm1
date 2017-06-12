import RPi.GPIO as GPIO
import time

DataSet = 16  # dit is de waarde die je op het display wilt brengen
Reset = 19  # dit zet het dislplay op 0
StorigePuls = 20  # deze puls zorgt ervoor dat de waarde wordt door gestuurd naar je register
ShiftPuls = 21  # deze puls toont de waarde op het display

#        D. G  F  E  D  C  B  A
list0 = [0, 0, 1, 1, 1, 1, 1, 1]
list1 = [0, 0, 0, 0, 0, 1, 1, 0]
list2 = [0, 1, 0, 1, 1, 0, 1, 1]
list3 = [0, 1, 0, 0, 1, 1, 1, 1]
list4 = [0, 1, 1, 0, 0, 1, 1, 0]
list5 = [0, 1, 1, 0, 1, 1, 0, 1]
list6 = [0, 1, 1, 1, 1, 1, 0, 1]
list7 = [0, 0, 0, 0, 0, 1, 1, 1]
list8 = [0, 1, 1, 1, 1, 1, 1, 1]
list9 = [0, 1, 1, 0, 1, 1, 1, 1]
list_lijsten = [list0, list1, list2, list3, list4, list5, list6, list7, list8, list9]

GPIO.setmode(GPIO.BCM)
GPIO.setup(DataSet, GPIO.OUT)
GPIO.setup(Reset, GPIO.OUT)
GPIO.setup(StorigePuls, GPIO.OUT)
GPIO.setup(ShiftPuls, GPIO.OUT)

Display1 = 23
Display2 = 24
Display3 = 25
Display4 = 12
lst_display = [Display1, Display2, Display3,Display4]
GPIO.setup(Display1, GPIO.OUT)
GPIO.setup(Display2, GPIO.OUT)
GPIO.setup(Display3, GPIO.OUT)
GPIO.setup(Display4, GPIO.OUT)
GPIO.output(Display1, GPIO.LOW)
GPIO.output(Display2, GPIO.LOW)
GPIO.output(Display1, GPIO.LOW)
GPIO.output(Display1, GPIO.LOW)

def initDisplay():
    GPIO.output(Reset, GPIO.HIGH)
    GPIO.output(DataSet, GPIO.LOW)
    GPIO.output(StorigePuls, GPIO.LOW)
    GPIO.output(ShiftPuls, GPIO.LOW)


def ToonWaardeOpDisplay():
    GPIO.output(StorigePuls, GPIO.HIGH)
    time.sleep(0.005)
    GPIO.output(StorigePuls, GPIO.LOW)


def toon(display):
    for i in range(0, len(display)):
        if display[i] == 1:
            GPIO.output(DataSet, GPIO.HIGH)
            time.sleep(0.005)
            GPIO.output(ShiftPuls, GPIO.HIGH)
            time.sleep(0.005)
            GPIO.output(DataSet, GPIO.LOW)
            GPIO.output(ShiftPuls, GPIO.LOW)
        else:
            GPIO.output(DataSet, GPIO.LOW)
            time.sleep(0.005)
            GPIO.output(ShiftPuls, GPIO.HIGH)
            time.sleep(0.005)
            GPIO.output(DataSet, GPIO.LOW)
            GPIO.output(ShiftPuls, GPIO.LOW)
        ToonWaardeOpDisplay()


print("programming is running!!!")

try:
    initDisplay()

    while True:
        for teller in range(0, len(list_lijsten)):
            toon(list_lijsten[teller])
            time.sleep(0.5)
            print("display: %d" % teller)

except KeyboardInterrupt:
    GPIO.output(Reset, GPIO.LOW)
    GPIO.output(StorigePuls, GPIO.HIGH)
    time.sleep(0.005)
    GPIO.output(StorigePuls, GPIO.LOW)

print("einde")
GPIO.cleanup()
