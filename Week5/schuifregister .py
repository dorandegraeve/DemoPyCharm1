import RPi.GPIO as GPIO
import time

# variabelen
delay = 0.0000001
delay_display = 0.000000000001

Display1 = 23
Display2 = 24
Display3 = 25
Display4 = 12
lst_display = [Display1, Display2, Display3, Display4]

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
lst_lijsten = [list0, list1, list2, list3, list4, list5, list6, list7, list8, list9]

# declaratie pinnen
DS = 16  # data set
ST_CP = 20  # storage
SH_CP = 21  # shift
Reset = 19  # dit zet het dislplay op 0
register = 26  # dit wordt zet het schuifregister aan of uit

# init I/O
GPIO.setmode(GPIO.BCM)

# init I/O shift register
GPIO.setup(DS, GPIO.OUT)
GPIO.setup(ST_CP, GPIO.OUT)
GPIO.setup(SH_CP, GPIO.OUT)
GPIO.setup(Reset, GPIO.OUT)
GPIO.setup(register, GPIO.OUT)

GPIO.setup(Display1, GPIO.OUT)
GPIO.setup(Display2, GPIO.OUT)
GPIO.setup(Display3, GPIO.OUT)
GPIO.setup(Display4, GPIO.OUT)
# resetten
GPIO.output(Reset, GPIO.HIGH)

# schuifregister aanzetten
GPIO.output(register, GPIO.LOW)

# display selecteren door kathode tegen te werken of niet
GPIO.output(Display1, GPIO.HIGH)
GPIO.output(Display2, GPIO.HIGH)
GPIO.output(Display3, GPIO.HIGH)
GPIO.output(Display4, GPIO.HIGH)


# byte naar segment schrijven
def write_to_segment(lst_x):
    for index in range(0, len(lst_x)):
        if lst_x[index] == 1:
            GPIO.output(DS, GPIO.HIGH)
        else:
            GPIO.output(DS, GPIO.LOW)
        GPIO.output(SH_CP, GPIO.HIGH)
        GPIO.output(DS, GPIO.LOW)
        GPIO.output(SH_CP, GPIO.LOW)
    copy_to_storage_register()
    return


# data in schuifregister in storage register opslaan
def copy_to_storage_register():
    GPIO.output(ST_CP, GPIO.HIGH)
    time.sleep(0.005)
    GPIO.output(ST_CP, GPIO.LOW)
    return


def multiplex(getal_):
    counter = 0
    getal_in = str(getal_)
    for display in lst_display:
        GPIO.output(display, GPIO.LOW)
        if counter == 0 and len(getal_in)>=1:
            write_to_segment(lst_lijsten[int(getal_in[0])])
        if counter == 1 and len(getal_in)>=2:
            write_to_segment(lst_lijsten[int(getal_in[1])])
        if counter == 2 and len(getal_in)>=3:
            write_to_segment(lst_lijsten[int(getal_in[2])])
        if counter == 3 and len(getal_in)>=4:
            write_to_segment(lst_lijsten[int(getal_in[3])])
        GPIO.output(display, GPIO.HIGH)
        counter += 1


try:
    # print_menu()
    while True:
        multiplex(18)
except KeyboardInterrupt:  # clear display en save de data
    GPIO.cleanup()
