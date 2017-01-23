# dht22-adaiot

script python gérant un capteur **dht22** à l'aide des librairies d'**Adafruit.**

Il récupère les données et les affiche localement (print, logs, envoi au serversocket) et dans adaiot

# Montage

![Electronic settings](DHT22-rpi_bb.png?raw=true "Hardware")

# Dépendances
* librairie python `Adafruit_DHT`  
* librairie python `Adafruit_IO`  
* tokenss.py : editer `tokenss_example.py` et renommer en `tokens.py`  

# Crontab
`@reboot sleep 60 && sudo /usr/bin/python /home/pi/dht22/dht22.py >> /home/pi/dht22/temp_log/errors_python.log 2>&1`

attend 1 minute (pour établir la connexion réseau) et lance le script. Les erreurs et prints doivent partir dans `errors_python.log`... mais pour l'instant ça ne fonctionne pas.

# Changelog
* 0.1 : tests et création du git  
adaiot fonctionne  
les logs locaux fonctionnent  
bug avec les `stdout` : impossible d'enregister tous les msg dans un fichier depuis bash
* 0.2 display web server

# todo
* display sur lcd (pb avec le grove lcd qui empeche de tester pour l'instant)
