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
from Adafruit_IO import *    #adafruit io : push data
import tokenss
import socket

# globals
fichier_log = "/home/pi/dht22/temp_log/temperature.log"
# sleeptime = 60
sleeptime = 10

# adafuit key
aio = Client(tokenss.aiokey)

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

	temperature, humidity = releve()
	heure = strftime("%a, %d %b %Y %H:%M:%S", localtime())
	blabla ="{} : Temp={}*C  Humidity={}%".format(heure, temperature, humidity)
	#exemple : "Mon, 23 Jan 2017 17:18:45 : Temp=22.4*C  Humidity=42.6%"

	# logs locaux
	print(blabla)
	lines = open(fichier_log).readlines()
	#ne garde que les 5000 dernieres lignes
	if len(lines)>=5000:
		open(fichier_log, 'w').writelines(lines[len(lines)-4999:len(lines)])
	#ajout d'une ligne au log
	hs = open(fichier_log,"a")
	hs.write(blabla + "\n")
	hs.close()

	# envoi au webserver
	socketconnect(blabla)

	# adafruit io
	aiosend('temp', temperature)
	aiosend('humid',humidity)

def refreshauto():
	'''
	releves automatiques
	'''
	continuer = True
	while continuer:
		displayreleve()
		sleep(sleeptime)

# def aiosend(sendmsg,feed):
# 	# marche tjrs pas
# 	"""
# 	envoie les releves a adafruit io
# 	"""
# 	# catch les exceptions
# 	try:
# 		aio.send(sendmsg,feed)
# 	except errors.RequestError as e:
# 		print e
# 		pass
# 	except ConnectionError as e:
# 		print # coding=utf-8
# 		pass
# 	except Exception as e:
# 		print e
# 		raise
def aiosend(sendmsg,feed):
	# la grosse lose
	"""
	envoie les releves a adafruit io
	"""
	# catch les exceptions
	try:
		aio.send(sendmsg,feed)
	except Exception as e:
		print e
		pass

#connexion au socket du rpi2Camera log si connexion impossible
#parameters : socketmsg le corps du msg
#appelé régulierement pour check le statut (open, close)
#appelé à intervalle régulier (heartbeat)
def socketconnect(socketmsg):
	mylist = [socketmsg] #met le msg dans une liste
	mylist.append(strftime("%Y-%m-%d %H:%M:%S"))

	print mylist[0] #affiche le msg envoyé - à retirer une fois terminé
	address = tokenss.address #rpiCamera
	port = tokenss.port #port random, meme que server
	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #parametres du socket
	try: #pour eviter de planter si le server est down
		clientsocket.connect((address, port)) #ouvre la connexion
		clientsocket.send(str(mylist[1])+" "+str(mylist[0])) #envoie le msg
	except Exception as e:
		print("Erreur de connexion SOCKET : %s:%d. Exception is %s" % (address, port, e)) #log un msg si erreur
	finally:
		clientsocket.close() #dans tous les cas ferme la connexion

##########################################

if __name__ == '__main__':
	# releve l'heure, l'affiche et la loggue dans le fichier
	heure = strftime("%a, %d %b %Y %H:%M:%S", localtime())
	texte_lancement = "\n" + heure + " lancement script temperature" + "\n"
	print(texte_lancement)
	hs = open(fichier_log,"a")
	hs.write(texte_lancement)
	hs.close()

	#a mettre dans un try pour relever les erreurs
	refreshauto()
