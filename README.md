# dht22-adaiot

script python gérant un capteur **dht22** à l'aide des librairies d'**Adafruit.**

Il récupère les données et les affiche localement (print, logs) et dans adaiot

# Montage

![Electronic settings](DHT22-rpi_bb.png?raw=true "Hardware")

# Dépendances
* librairie python `Adafruit_DHT`  
* librairie python `Adafruit_IO`  
* tokenss.py : editer `tokenss_example.py` et renommer en `tokens.py`  


# Changelog
* 0.1 : tests et création du git  
adaiot fonctionne  
les logs locaux fonctionnent  
bug avec les `stdout` : impossible d'enregister tous les msg dans un fichier depuis bash

# todo
* display web server
* display sur lcd (pb avec le grove lcd qui empeche de tester pour l'instant)
