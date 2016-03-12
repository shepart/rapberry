#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import MySQLdb

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# GPIO definieren
pin_gas = 26
# definierten GPIO als Eingang setzen
GPIO.setup(pin_gas, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Datenbankverbindung
db = MySQLdb.connect(host="nas1", user="statistik", passwd="statistik", db="statistik")

status_alt=1
while True:
    status_aktuell = GPIO.input(pin_gas)
# REEDKONTAKT geoeffnet
    if status_aktuell == 1:
        print "Kontakt offen"
        status_alt=GPIO.input(pin_gas)
        # REEDKONTAKT geschlossen
    elif status_aktuell==0:
        print "Kontakt geschlossen"
        if status_alt!=status_aktuell:
            status_alt=GPIO.input(pin_gas)
# Datenbank fuettern
            cursor = db.cursor()
            cursor.execute("""INSERT INTO gas (Zaehlerstand) SELECT MAX(Zaehlerstand) + 1 FROM gas""")
            db.commit()
            cursor.close()
    time.sleep(5)
