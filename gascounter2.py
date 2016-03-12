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

offen=False
while True:
	# REEDKONTAKT geoeffnet
    if GPIO.input(pin_gas):
        print "Kontakt offen"
        offen = True
    # REEDKONTAKT geschlossen
    else:
        print "Kontakt geschlossen"
        if offen: # Kontakt war zuvor offen...
            offen = False
            # Datenbank fuettern
            cursor = db.cursor()
            cursor.execute("""INSERT INTO gas (Zaehlerstand) SELECT MAX(Zaehlerstand) + 1 FROM gas""")
            db.commit()
            cursor.close()
    time.sleep(5)
