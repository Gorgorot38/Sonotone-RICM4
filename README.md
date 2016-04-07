# Sonotone-RICM4

## Installation
Tous les modules de ce projet fonctionnent sous Python 2.7 et dépendent de numpy, scipy et matplotlib pour l'affichage de la réponse fréquentielle des filtres utilisés pour ce projet.

Pour installer les dépendances ci-dessus, exécuter les commandes ci-dessous en fonction de la machine utlisée:

### Windows
	python -m pip install matplotlib ou utiliser WinPython ou Anaconda (ide python)
	python -m pip install scipy
	python -m pip install numpy

### Linux
	sudo apt-get install python-matplotlib
	sudo apt-get install python-numpy
	sudo apt-get install python-scipy

## Utilisation
### Programme principal
Le programme principal se trouve dans le package <i>Sonotone</i> sous le nom <i>main.py</i>.

###### Commande d'exécution
	python main.py
Le module va alors lire le fichier <i>config.xml</i> pour connaître réglages des filtres à utiliser, 
pour ensuite les appliquer sur le son acquis par l'entrée microphone de la machine.

L'éxecution du programme étant infini, il suffit de faire <i>Ctrl+C</i> pour l'arrêter.

### Configuration
La configuration des filtres à utiliser se fait par le module <i>gui.py</i> contenu dans le package <i>Sonotone</i>.

###### Commande d'exécution
	python gui.py

Une fenêtre s'ouvre, on peut alors choisir le gain à appliquer grâce à des sliders, un bouton <i>Advanced</i> permet de
passer en mode <i>Avancé</i>, et on peut maintenant choisir la qualité du filtre ainsi que son type comme par exemple:
peaking, lowpass, highpass...

Une fois la configuration terminée, on appuie sur le bouton <i>Save</i> qui sauvegarde la valeur de chaque réglage dans
le fichier <i>config.xml</i>


