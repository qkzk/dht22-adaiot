#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
refuse d'envoyer stdout dans un fichier avec 'sudo python file.py >> file.log 2>&1'
solution sauvage : logguer depuis le fichier.
il faudra ajouter les logs des erreurs qui, sinon, risquent d'etre perdues...
"""

# imports
from time import localtime, strftime
from time import sleep
import Adafruit_DHT
from Adafruit_IO import Client, Data    #adafruit io : push data
import tokenss

# fonctions
def releve():
	'''
	releve charge la librairie d'Adafruit,
	lit les capteurs
	renvoie temperature et humidité avec 1 décimale comme des strings
	renvoie None, None en cas d'erreur de lecture
	'''
	# Adafruit_DHT.DHT22
	sensor = Adafruit_DHT.DHT22
	# connected to Raspberry pi GPIO23.
	pin = 23

	# Try to grab a sensor reading.  Use the read_retry method which will retry up
	# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	# Note that sometimes you won't get a reading and
	# the results will be null (because Linux can't
	# guarantee the timing of calls to read the sensor).
	# If this happens try again!
	if humidity is not None and temperature is not None:
	    tempf = "{0:0.1f}".format(temperature)
	    humf = "{0:0.1f}".format(humidity)
	    return(tempf,humf)
	else:
	    print('Failed to get reading. Try again!')
	    return None,None

def displayreleve():
	'''
	affiche les releves :
	* dans la console si lance normalement
	* dans un fichier log (ecriture directe sans passer par log handler)
	* sur IO adafruit
	'''
	fichier_log = "/home/pi/temp_log/temperature.log"
	temperature, humidity = releve()
	heure = strftime("%a, %d %b %Y %H:%M:%S", localtime())
	blabla ="{} : Temp={}*C  Humidity={}%".format(heure, temperature, humidity)
	print(blabla)
	hs = open(fichier_log,"a")
	hs.write(blabla + "\n")
	hs.close()

	# adafuit key
	aio = Client(tokenss.aiokey)
	aio.send('temp', temperature)
	aio.send('humid',humidity)

def refreshauto():
	'''
	releves automatiques toutes les 10 s
	'''
	continuer = True
	while continuer:
		displayreleve()
		sleep(10)

if __name__ == '__main__':
	# releve l'heure, l'affiche et la loggue dans le fichier
	heure = strftime("%a, %d %b %Y %H:%M:%S", localtime())
	texte_lancement = "\n" + heure + "lancement script temperature" + "\n"
	print(texte_lancement)
	hs = open("/home/pi/temp_log/temperature.log","a")
	hs.write(texte_lancement)
	hs.close()

	#a mettre dans un try pour relever les erreurs
	refreshauto()
