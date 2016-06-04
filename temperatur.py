#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import der Module
import sys
import os
import MySQLdb


# 1-Wire Slave-Liste lesen
file = open('/sys/devices/w1_bus_master1/w1_master_slaves')
w1_slaves = file.readlines()
file.close()

# Fuer jeden 1-Wire Slave aktuelle Temperatur ausgeben
for line in w1_slaves:
  # 1-wire Slave extrahieren
  w1_slave = line.split("\n")[0]
  # 1-wire Slave Datei lesen
  file = open('/sys/bus/w1/devices/' + str(w1_slave) + '/w1_slave')
  filecontent = file.read()
  file.close()

  # Temperaturwerte auslesen und konvertieren
  stringvalue = filecontent.split("\n")[1].split(" ")[9]
  temperature = float(stringvalue[2:]) / 1000

  #DB Verbindung
db = MySQLdb.connect(host="nas1", user="statistik", passwd="statistik", db="statistik")
cursor = db.cursor()
cursor.execute("""INSERT INTO temp (sensor_id,temperatur) VALUES ($w1_slave,$temperature""")
db.commit()
cursor.close()
time.sleep(5)


  # Temperatur ausgeben


print(str(w1_slave) + ': %6.2f °C' % temperature)

sys.exit(0)
