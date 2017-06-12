import RPi.GPIO as GPIO
import time

# variabelen
delay = 0.01
delay_display = 1

lst_0 = [0, 0, 1, 1, 1, 1, 1, 1]
lst_1 = [0, 0, 0, 0, 0, 1, 1, 0]
lst_2 = [0, 1, 0, 1, 1, 0, 1, 1]
lst_3 = [0, 1, 0, 0, 1, 1, 1, 1]
lst_4 = [0, 1, 1, 0, 0, 1, 1, 0]
lst_5 = [0, 1, 1, 0, 1, 1, 0, 1]
lst_6 = [0, 1, 1, 1, 1, 1, 0, 1]
lst_7 = [0, 0, 0, 0, 0, 1, 1, 1]
lst_8 = [0, 1, 1, 1, 1, 1, 1, 1]
lst_9 = [0, 1, 1, 0, 1, 1, 1, 1]
lst_lijsten = [lst_0, lst_1, lst_2, lst_3, lst_4, lst_5, lst_6, lst_7, lst_8, lst_9]  # inputs

# declaratie pinnen
DS = 16  # data set
ST_CP  = 20  # storage
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

# resetten
GPIO.output(Reset, GPIO.HIGH)

# schuifregister aanzetten
GPIO.output(register, GPIO.HIGH)


# byte naar segment schrijven
def write_to_segment(lst_x):
    for index in range(0, len(lst_x)):
        if lst_x[index] == 1:
            GPIO.output(DS, GPIO.HIGH)
        else:
            GPIO.output(DS, GPIO.LOW)

        time.sleep(delay)
        GPIO.output(SH_CP, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(DS, GPIO.LOW)
        GPIO.output(SH_CP, GPIO.LOW)
        time.sleep(delay)
    copy_to_storage_register()
    return


# data in schuifregister in storage register opslaan
def copy_to_storage_register():

    # GPIO.output(ST_CP, GPIO.HIGH)
    # time.sleep(0.01)
    # GPIO.output(ST_CP, GPIO.LOW)
    return


# schuifregister aan- of uitzetten
def register_on_off(status):
    if status == "on":
        # schuifregister aanzetten
        GPIO.output(register, GPIO.HIGH)

        # clear display en save de data
        GPIO.output(Reset, GPIO.LOW)
        copy_to_storage_register()

    else:
        # clear display en save de data
        GPIO.output(Reset, GPIO.LOW)
        copy_to_storage_register()

        # schuifregister uitzetten
        GPIO.output(register, GPIO.LOW)
    return


# menu printen
def print_menu():
    print("1. Teller van 0 tot 9\n2. Display getal van gebruiker\n3. Schuifregister aanzetten en display clearen\n4. Schuifregister uitzetten\n")
    return


print("Program is running!!!\n")

try:
    print_menu()
    while True:
        keuze = input("Maak een keuze: ")

        if keuze == "1":
            for teller in range(0, len(lst_lijsten)):  # lst_lijsten aflopen
                write_to_segment(lst_lijsten[teller])  # inhoud van de variabele op plaats teller in lst_lijsten tonen op display
                print("Display: %d" % teller)
                time.sleep(delay_display)

            # clear display en save de data
            GPIO.output(Reset, GPIO.LOW)
            copy_to_storage_register()

        elif keuze == "2":
            getal = input("Geef getal in: ")
            write_to_segment(lst_lijsten[int(getal)])  # inhoud van de variabele op plaats getal in lst_lijsten tonen op display
            print("Display: %s\n" % getal)
            time.sleep(delay_display)

        elif keuze == "3":
            register_on_off("on")  # schuifregister aanzetten
            print("Schuifregister staat aan en display is clear.\n")

        elif keuze == "4":
            register_on_off("off")  # schuifregister uitzetten
            print("Schuifregister staat uit.\n")

        print_menu()  # menu printen

except KeyboardInterrupt:
    # clear display en save de data
    GPIO.output(Reset, GPIO.LOW)
    copy_to_storage_register()
    time.sleep(0.01)

print("EINDE")
GPIO.cleanup()
